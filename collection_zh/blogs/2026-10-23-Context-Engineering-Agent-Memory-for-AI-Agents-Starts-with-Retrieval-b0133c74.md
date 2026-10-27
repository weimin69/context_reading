> 本文为简体中文机器翻译，使用 Google Translate 公开接口并统一技术术语，尚未经逐句人工校对。代码、链接和公式按原文保留；实验数字及技术结论请对照原文。
> [查看本地英文原文](../../collection/blogs/2026-10-23-Context-Engineering-Agent-Memory-for-AI-Agents-Starts-with-Retrieval-b0133c74.md) · [原始来源](https://www.langchain.com/blog/context-engineering-starts-with-retrieval)

# 智能体上下文工程（智能体记忆）从检索开始

- 来源: https://www.langchain.com/blog/context-engineering-starts-with-retrieval- 发布日期: 2026-10-23- 日期依据: JSON-LD datePublished- 类型: blog- 主题: 上下文选择、检索- 抓取状态: article_html- 正文来源: https://www.langchain.com/blog/context-engineering-starts-with-retrieval- 抓取时间 UTC: 2026-10-26T09:28:02.471505+00:00

## 来源摘要/页面简介

智能体将时间和上下文浪费在笨拙的搜索、过大的结果和过时的数据上。了解 LangChain 的 Deep Agents 利用的检索技术来获取正确的上下文。

## 抓取正文（中文翻译）

Deep Agents

概念指南

# 上下文工程从检索开始

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6acfb8492227373b922e7719_Screenshot%202026-10-14%20at%2010.12.17%E2%80%AFAM.png)

翁洁丝

2026 年 10 月 23 日

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69ce2c533137196179bae949_Icon-7.svg)

11

分钟

[返回博客](https://www.langchain.com/blog)

[创建智能体](https://www.langchain.com/blog/context-engineering-starts-with-retrieval#)

[创建智能体](https://www.langchain.com/blog/context-engineering-starts-with-retrieval#)

分享

## 要点

* 智能体在有限的上下文窗口中工作，信息检索会以三种方式中断：搜索效率低下、一次性上下文过多以及上下文不相关或陈旧。
* Deep Agents 工具使搜索保持开箱即用的小规模。内置文件系统工具在读取之前进行搜索：glob 匹配文件名，grep 查找匹配行，以及 read\_file 一次读取一页。超大工具结果被卸载：完整结果保存到文件中，但智能体仅获取路径和预览。
* 对于自定义搜索工具（如 RAG），请使用“检索、卸载、委托”：将结果保存到文件、返回路径并让子智能体读取它们。主要智能体只看到相关的内容。

想象一下，您正在参加一场开卷考试：从技术上讲，您已经拥有所有答案，但不知何故，这使得找到*正确的*答案变得更加困难。

* 您从哪里开始搜索？
* 您什么时候知道您的消息来源是正确的？
* 你如何优化你的时间，这样你就不会把所有的精力都花在多余的搜索上？

有效地找到正确的信息并不是那么简单。

向智能体提出一个问题，它会遇到类似的困境：它的上下文窗口有限，所以像我们人类一样，它必须**检索**信息来完成某些任务（而不是记住所有内容）。在搜索时，智能体会遇到以下问题：

* **搜索效率低下：**每次搜索都需要花费词元和时间。笨拙搜索的智能体（例如打开每个文件只是为了查看里面的内容，或者不断改写相同的查询）可以在找到任何有用的内容之前用搜索结果填充其上下文。
* **一次上下文太多：** 一次转储完整数据导出的搜索或一打文档一次性填满上下文窗口，没有为工作本身留下空间。
* **不相关或过时的上下文：** 过时或偏离主题的信息对于模型来说看起来与正确答案一样令人信服。一旦它进入上下文窗口，智能体就可以在它的基础上进行构建（并且错误将贯穿之后的每一步）。

幸运的是，智能体可以使用多种技术来检索“正确”信息。 [智能体工具](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness) 的工作是战略性地应用这些技术，让模型在正确的时间**获得正确的上下文**来完成给定的任务。

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada6def0e658ad27256aef7_harness-embedded%20(1).png)

本博客介绍了智能体检索的挑战（仅查找和提取手头任务所需的信息）、我们可以使用的技术来应对这些挑战，以及在设计智能体工具时如何牢记这些挑战（以 [LangChain 的Deep Agents](https://www.langchain.com/deep-agents) 工具为例）。

有关如何在上下文窗口中管理上下文的更多信息，请查看此[有关上下文工程的博客](https://www.langchain.com/blog/context-engineering-deep-agents-remember)。

## 我们的示例：竞争分析智能体

让我们看看如何将其应用到现实世界的用例中：竞争分析智能体。每个星期一，智能体都会研究数百名竞争对手，并在团队的模板中撰写报告。它需要：

* 查找上周有关 A 公司的笔记
* 在海量市场数据导出中查找具体收入数字
* 在新闻档案中搜索任何新内容

其中每一种都是不同类型的检索，因此面临不同的问题。我们使用[Deep Agents工具](https://docs.langchain.com/oss/python/deepagents/overview)构建了我们的智能体，因此我们可以立即应用一些技术来最大限度地减少这些问题。

## 1. 搜索效率低下

我们的智能体必须为每个竞争对手找到三件事。如果每个都需要十几次尝试（打开文件只是为了看看里面有什么，或者因为源使用不同的单词而重新编写搜索），那么它的上下文窗口在写出报告的一个字之前就会充满失败的搜索。

因此，最好的搜索是智能体不必重复的搜索，这意味着为每项工作使用正确的工具。

### 从内置文件系统工具开始

智能体搜索信息的最常见方法之一是使用文件系统。然而，如果我们的智能体打开每个文件来查看里面的内容，那么它的搜索效率非常低：它读取的每个文件都位于其上下文窗口中，因此只需查看它就可以填满。

更好的方法是首先检查**名称**和**关键字**（就像在开卷考试期间扫描书籍索引而不是阅读每一页的方式）。两个常见的文件系统工具正是这样做的：

* `glob` 按名称模式查找文件。例如，`**/company-a*.md` 查找上周有关 A 公司的笔记。
* `grep` 搜索文件内部，而不将它们加载到上下文窗口中。它匹配文字文本，并可以返回匹配的文件、匹配的行或计数。

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada6e01fd3bbf8a61b345c3_d1-scan-first.png)

每个Deep Agents都附带[内置这些工具](https://docs.langchain.com/oss/python/deepagents/tools#built-in-harness-tools)，以及`ls`、`read_file`、`write_file`和`edit_file`。无论文件位于何处（智能体状态、本地磁盘、持久存储或沙箱），相同的工具都可以工作，因为它们都通过智能体的[后端](https://docs.langchain.com/oss/python/deepagents/backends)。

### 添加关键词不够时的检索工具

当您知道要查找哪些单词时，[Grep](https://reference.langchain.com/python/deepagents/backends/protocol/BackendProtocol/grep) 非常有用，但它仅与您提供的“精确”文本匹配。这是我们示例中的第三项工作的问题：在新闻档案中搜索任何新内容。如果我们的智能体搜索“A 公司融资”，它将错过一篇标题为“A 公司关闭了 5000 万美元 B 轮融资”的文章，尽管这正是它正在寻找的内容。

要按含义而不是确切的单词进行搜索（语义搜索），您可以添加一个由 [向量存储](https://docs.langchain.com/oss/python/integrations/vectorstores) 支持的 [**检索工具**](https://docs.langchain.com/oss/python/deepagents/retrieval)。检索工具是智能体可以调用​​来获取信息的任何工具：它进行查询，在某些数据源中查找，然后返回找到的内容（最接近的匹配项）。

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada6e1017deb689203baeb8_d2-grep-vs-semantic%20(1).png)

检索工具如何匹配取决于其背后的数据源。在向量存储的支持下，它按含义进行匹配，但检索工具也可以位于其他数据源之上：

* SQL 数据库，用于结构化查找（如销售数据或客户记录）
* 搜索 API（用于来自网络的最新信息）
* [MCP 服务器](https://docs.langchain.com/oss/python/deepagents/tools#mcp-tools)（用于其他人已经构建的工具，例如文档搜索）

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada6e26b85ddacbcd3d660f_d3-retrieval-tool%20(1).png)

要更深入地了解语义搜索的工作原理，请参阅[LangChain指南](https://docs.langchain.com/oss/python/langchain/knowledge-base)。

### 让智能体决定何时搜索

许多检索设置在开始时搜索一次，然后回答。这适用于常见问题解答机器人（[2-step RAG](https://docs.langchain.com/oss/python/deepagents/retrieval#2-step-rag)），但不适用于我们的智能体。假设在 C 公司研究过程中，它发现了一篇关于其不了解的产品发布的文章，现在它需要该产品的定价（它一开始就无法知道要查找的价格）。只要一查，报告就没有了。

研究智能体需要[智能体检索](https://docs.langchain.com/oss/python/deepagents/retrieval#agentic-rag)（而不是2步RAG）：智能体决定何时搜索、搜索什么以及是否需要更多。对于 Deep Agents，默认情况下它已经以这种方式工作：智能体在循环中运行，并且可以根据需要多次调用任何工具。

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada6e34e5e14ab012badab9_d4-rag-vs-agentic%20(1).png)

### 将您的搜索知识打包为一项技能

为了帮助智能体更好地进行搜索，您可以将搜索技巧打包为[技能](https://docs.langchain.com/oss/python/deepagents/skills)：一组针对特定任务的说明（例如使用哪个索引、如何表达查询以及如何格式化引文）。

智能体只能看到每个技能的名称和简短描述，直到任务需要它为止；然后它加载完整的指令，因此在需要时就可以找到利基知识，而无需在其余时间占用上下文（一种称为[渐进式披露](https://docs.langchain.com/oss/python/deepagents/skills#how-skills-work)的技术）。这是[视频解释](https://www.youtube.com/watch?v=bv1qgkbWhms)。

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada779317deb68920402eca_skills-progressive-disclosure-light%20(1).gif)

渐进式披露（动画）

## 2. 一次太多的上下文

然而，尽管优化了搜索过程，即使是“正确”的搜索也可能返回太多内容。我们的智能体只需要市场数据导出中的一个数字（B 公司的季度收入），但加载所有 40,000 行后发现它会填充其上下文窗口。我们的检索工具也存在同样的问题：如果它将每一篇新闻文章都直接返回到模型中，则五家公司的每次搜索都会快速添加四个结果。

### 一次一页读取大文件

文件系统工具的构建是为了返回尽可能少的结果。 `read_file` 一次一页读取文件（默认为 100 行），智能体可以设置偏移量（从哪一行开始）和限制（读取多少行）以跳转到所需的部分。因此，为了找到 B 公司的收入，智能体需要进行 grep 查找，然后只读取匹配项周围的几行内容。

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada717e600aacfde1b63063_p1-paged-reading.png)

### 让运行框架卸载过大的结果

有时，工具的回报无论如何都会超出预期。当工具结果太大（超过大约 20,000 个词元）时，工具会将其保存到/large\_tool\_results/下的文件中，并向智能体提供路径以及简短的预览（第一行和最后几行）。然后，智能体可以使用 `read_file` 的偏移量和限制来读回其所需的部分。

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada718d18a99d15b175faf2_p2-offload-results%20(1).png)

### 让您的检索工具返回文件路径

您可以将相同的想法应用于您自己的检索工具，而不是等待大小限制：让它将每个结果写入文件并仅返回路径。这是名为“检索、卸载、委托”模式的第一部分（[LangChain 的 RAG 指南](https://docs.langchain.com/oss/python/deepagents/rag) 完整介绍了该模式）。

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada719604267bfb9db5b667_p3-search-paths.png)

这是一个简化的检索工具。它运行搜索，将每个结果保存为智能体的[后端](https://docs.langchain.com/oss/python/deepagents/backends#statebackend)中的文件，并仅返回文件路径列表：

```
backend = StateBackend()

@tool
def search_news(query: str) -> str:
    """Search the news archive and save each result to a file."""
    docs = vector_store.similarity_search(query, k=4)
    files = [(f"/retrieved/result_{i}.md", doc.page_content.encode()) for i, doc in enumerate(docs)]
    backend.upload_files(files)
    return "Saved results to: " + ", ".join(path for path, _ in files)
```
 现在主智能体看到四个短路径而不是四个完整的文章。

## 3. 不相关或过时的上下文

如果结果是“错误的”，那么小结果就没有帮助。这四个文件中的任何一个都可能是关于名称相似的不同公司，或者是两年前的故事。对于模型来说，偏离主题或过时的文本看起来与正确答案一样令人信服，因此目标是将其完全排除在主要智能体的上下文之外。

### 让子智能体过滤结果

然而，主智能体*仍然*必须读取这些文件以找出哪些文件重要（并且它打开的每一篇离题文章都在其上下文中）。这就是“检索、卸载、委托”模式的“委托”部分的用武之地：[子智能体](https://docs.langchain.com/oss/python/deepagents/subagents) 读取每个检索到的文件并仅返回关键事实。

1. 定义子智能体：描述告诉主智能体何时使用它（每次调用一个文件），系统提示告诉子智能体如何处理该文件。

```
chunk_analyst = {
		"name": "chunk-analyst",
		"description": "Analyze one retrieved file. Pass the question and a single path under /retrieved/.",
		"system_prompt": "Use read_file to read the assigned file. Return the key facts and the source URL.",
}
```

2. 为主智能体提供检索工具和子智能体。传递您在`search_news`中使用的相同后端，以便子智能体可以读取工具保存的文件。

```
agent = create_deep_agent(
		model=model,
		tools=[search_news],
		backend=backend,  # same instance, so read_file can see /retrieved/
		subagents=[chunk_analyst],
)
```
 现在流程是：

1. **搜索**：主智能体调用`search_news`并返回4条路径。
2. **委托**：它将每个路径发送到块分析子智能体，并且它们可以并行运行。
3. **综合**：每位分析师返回一份简短的摘要及其来源。主智能体将它们组合起来，如果有东西丢失，就会再次搜索。

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada7251706d82f584744c9d_s1-subagents-filter%20(1).png)

原始结果进入文件，嘈杂的读取发生在具有自己的上下文窗口的子智能体中，而主智能体只能看到结论。任何偏离主题的内容都会保留在子智能体的上下文中，并且主智能体的上下文窗口保持清晰！

### 从最新来源获取

过滤确实可以排除偏离主题的结果，但无法修复过时的结果。我们的竞争分析智能体每周一运行，因此上个月的指数不会反映本周的新闻。

解决方案：搜索 API 或 MCP 服务器可以为智能体提供当前信息（而不是几个月前索引的信息）。如果您的数据有日期，在检索工具中按日期过滤也会排除旧结果。

### 小心检索到的文本

另一方面，相关的当前结果可能会引起问题！由于检索到的文本是数据，而不是指令，因此您检索到的任何内容都可能包含[提示注入](https://docs.langchain.com/oss/python/deepagents/rag#security-considerations)（并且没有提示或分隔符策略完全阻止这种情况）。确保验证输出：检查答案是否引用了您期望的来源以及声明是否与其匹配。

## 要记住的检索策略

以下是需要注意的事项（无论您使用哪种运行框架）：

* **使用最有效的工具。** 如果您知道这些单词，grep 会胜过嵌入查找。将语义搜索保存到您真正需要的时候。
* **页面而不是加载**。分块读取大文件而不是一次读取全部文件。
* **返回指针而不是有效负载。** 将检索到的内容写入文件并将路径交给智能体。
* **委托阅读**。让子智能体阅读并总结，这样主智能体只能看到结论。
* **验证接地**。根据检索到的内容检查答案，并将检索到的文本视为不可信。

## 尝试一下

```
uv add deepagents
```
 想向现场讲师学习更多信息吗？我将在 11 月 9 日对此进行报道：[此处](https://events.langchain.com/register/agent-memory-102-context-retrieval-storage/) 注册！

‍

**检索只是故事的一半：信息如何到达智能体。当智能体的上下文窗口随着时间的推移开始构建信息时，我们如何管理它？**

*要了解更多信息，请查看：*

* 关于 [使用Deep Agents进行上下文工程] 的博客(https://www.langchain.com/blog/context-engineering-deep-agents-remember)
* 浪链学院【Deep Agents课程】(https://academy.langchain.com/courses/foundation-introduction-to-deepagents)（免费、在线、自定进度）。

### Related content

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6add442530f2704b9d5e03af_HVZbWoXb0AAOzqm.png)

Deep Agents

#### 构建“公司运行框架”的五个组成部分

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6a056ea05f3880a1361b47cf_Harrison.avif)

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6a56f3a3a4a725f72a70441f_caspar-b.jpeg)

Harrison Chase

Caspar Broekhuizen

2026 年 10 月 24 日

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

6

分钟

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ac6d12e05f73fc9690266a8_dark-74%20characters%20max.png)

Deep Agents

概念指南

#### 上下文工程：智能体的记忆有多深

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6acfb8492227373b922e7719_Screenshot%202026-10-14%20at%2010.12.17%E2%80%AFAM.png)

翁洁丝

2026 年 10 月 14 日

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

10

分钟

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ac91132385fb9bbe1cb53b1_mda-reactions-blog-cover-navy-1200x675.png)

Deep Agents

Tutorials & How-Tos

#### 使用托管Deep Agents构建出色的开箱即用用户体验

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ab416d4dafca27a7246c1d0_Nathan%20Drezner.jpg)

Nathan Drezner

2026 年 10 月 9 日

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

5

分钟

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69ce01ea562f8cc223cabf25_Frame%202147254328.svg)

谢谢！您的提交已收到！

哎呀！提交表单时出现问题。

### 查看您的智能体真正在做什么

LangSmith 是我们的智能体工程平台，可帮助开发人员调试每个智能体决策、评估更改并一键部署。

[尝试 LangSmith](https://smith.langchain.com/)[获取演示](https://www.langchain.com/contact-sales)

