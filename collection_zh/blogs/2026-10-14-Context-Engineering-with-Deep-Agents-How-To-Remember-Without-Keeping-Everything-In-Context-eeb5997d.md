> 本文为简体中文机器翻译，使用 Google Translate 公开接口并统一技术术语，尚未经逐句人工校对。代码、链接和公式按原文保留；实验数字及技术结论请对照原文。
> [查看本地英文原文](../../collection/blogs/2026-10-14-Context-Engineering-with-Deep-Agents-How-To-Remember-Without-Keeping-Everything-In-Context-eeb5997d.md) · [原始来源](https://www.langchain.com/blog/context-engineering-deep-agents-remember)

# Deep Agents 上下文工程：如何在不把一切塞进上下文的情况下保留记忆

- 来源: https://www.langchain.com/blog/context-engineering-deep-agents-remember- 发布日期: 2026-10-14- 日期依据: JSON-LD datePublished- 类型: blog- 主题: 上下文卸载、压缩、长期记忆- 抓取状态: article_html- 正文来源: https://www.langchain.com/blog/context-engineering-deep-agents-remember- 抓取时间 UTC: 2026-10-26T09:27:58.676918+00:00

## 来源摘要/页面简介

长时间运行的智能体会随着上下文的堆积而降级。了解卸载、摘要、技能、子智能体和内存如何使智能体的上下文窗口保持集中。

## 抓取正文（中文翻译）

Deep Agents

概念指南

# 上下文工程：智能体的记忆深度如何

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6acfb8492227373b922e7719_Screenshot%202026-10-14%20at%2010.12.17%E2%80%AFAM.png)

翁洁丝

2026 年 10 月 14 日

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69ce2c533137196179bae949_Icon-7.svg)

10

分钟

[返回博客](https://www.langchain.com/blog)

[创建智能体](https://www.langchain.com/blog/context-engineering-deep-agents-remember#)

[创建智能体](https://www.langchain.com/blog/context-engineering-deep-agents-remember#)

分享

## 要点

* 当长时间运行的智能体建立的上下文超出模型所能容纳的范围时，就会发生“上下文腐烂”，从而导致准确性下降。
* Deep Agents 是 LangChain 的开源智能体工具，它使用五种技术将上下文移出活动窗口（而不删除它），以防止上下文腐烂。
* Deep Agents 中智能体的内存以纯文件形式存储在您控制的存储中，因此您可以切换模型或提供程序，同时保留其学到的所有内容。

如果你曾经在考试前一天晚上临时抱佛脚，你就会知道这种感觉：你学得越多，前面的章节就越容易滑落。

智能体也有同样的问题。当他们承担更长的任务时，他们会接受越来越多的信息（指令、工具结果、文件等）；最终，这变得太多的[上下文](https://docs.langchain.com/oss/python/langchain/context-engineering)无法轻松地适应模型的*上下文窗口*。模型承载的历史、噪声和工具输出越多，其准确性和推理能力就越差。

在智能体工程领域，我们称之为“上下文腐烂”(https://news.ycombinator.com/item?id=44308711#44310054)。本博客介绍了管理智能体上下文窗口的技术，以及Deep Agents如何利用称为中间件的概念将它们注入智能体的运行中。

‍

### 了解上下文工程技术

简单来说，智能体只是一个带有运行框架的模型。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ac7d0681e478429d6f14812_agent-harness-light.png)

运行框架 = 包围模型 (LLM)

智能体可以使用的解决上下文失效问题的上下文工程技术主要分为两类：

* 防止不必要的信息“进入”上下文窗口
* 管理和过滤上下文窗口中*已有的内容

该工具有策略地应用这些方法，以便为给定任务（[检索](https://www.langchain.com/blog/context-engineering-starts-with-retrieval)）提供模型**在正确的时间**正确的上下文。

现在，连接一个能做到这一点的运行框架说起来容易做起来难，并且需要大量的工作（如果你是那种前一天晚上临时抱佛脚的人，工作量可能太大了）。

[Deep Agents](https://www.langchain.com/deep-agents)是LangChain的开源工具。它使用将上下文移出活动窗口（进入文件、摘要或单独的智能体）的技术来包装您选择的模型，以便主智能体仅携带其需要的内容（并且可以在以后需要时恢复原始数据）：

1. **卸载：**大型工具结果和用户消息保存到文件系统，模型可以看到预览。
2. **摘要：**当对话接近上下文限制时，较旧的消息将被压缩为摘要。
3. **技能：**任务知识仅在模型认为相关时才会加载。
4. **子智能体：** 嘈杂的工作在单独的上下文窗口中运行，并且仅返回结果。
5. **长期记忆：** 智能体学到的内容会保存到文件中，并延续到下一次对话。

‍

## 将上下文工程应用于常见用例

让我们看看如何将上述技术应用于现实世界的用例：竞争分析智能体。每个星期一，该智能体都会研究五名竞争对手，并在团队的模板中编写一份报告。单次运行看起来像这样：

1、拉出A公司的一个市场数据导出（几万行）
2.搜索新闻，阅读几篇文章，并做笔记
3. 对公司 B 至 E 重复上述操作
4. 起草报告，根据您的反馈进行修改并格式化

到第 4 步，智能体已在每个模型调用中携带了 5 个原始导出、数十个搜索结果和两个过时的草稿。其中大部分与最终报告的格式无关。

检索方法（[RAG](https://docs.langchain.com/oss/python/deepagents/rag)，或文件系统搜索）帮助智能体“仅”提取它需要的内容，但这仍然只能解决一半的问题。即使是精确的智能体也会积累不必要的消息、工具结果和中间工作，因此该工具还必须管理上下文窗口中及其周围已有的内容。

‍

## 如何实现这些技术：中间件

智能体在循环中运行：模型决定要做什么，调用工具，读取结果，然后重复直到任务完成。 [中间件](https://docs.langchain.com/oss/python/langchain/middleware/overview) 是插入该循环中特定点的代码：例如在智能体启动之前、每个模型调用周围或每个工具调用周围。

* 在每个点上，它都可以读取上下文并在下一步运行之前更改它。
* 这篇文章中的每一项上下文工程技术都是一个与这些点挂钩的中间件。    
  + 其中大部分都是内置的，因此您不需要编写任何中间件来使用这些技术（除非您想自定义特定的东西）。

‍

## 卸载：将其排除在上下文窗口之外

我们的智能体并不总是需要查看从每个工具调用或人工消息返回的“所有”数据，特别是当数据量很大时。

例如，每个pull\_market\_report工具调用都会返回完整的数据导出（数千行）；但是，智能体只需要其中的几个数字，因此可以将模型限制为仅查看这些行。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ac7d16728e8261fa2436c9a_context-offloading-light.gif)

工具结果卸载过程（动画）

FilesystemMiddleware 每次调用工具时都会运行：

1. 当工具结果超过大约 20,000 个词元时，完整结果会在进入对话之前写入/large\_tool\_results/{tool\_call\_id}。
2. 模型只能看到一个简短的预览（第一行和最后几行）以及文件路径。
3. 当智能体稍后需要B公司的季度收入时，它会通过read\_file.翻阅该文件

超大的用户/人类消息，例如粘贴的通话记录，在更高的阈值（50,000 个词元）下获得相同的处理，并保存到/conversation\_history/.

‍

## 总结：压缩已有内容

尽管我们可能会尝试卸载冗长的工具调用，但从长远来看，上下文将逐渐开始堆积（例如，五家公司的搜索、注释和草稿）。总结可用于将智能体的整个上下文窗口压缩为迄今为止所发生事件的摘要，以使其能够继续执行其研究任务。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ac7d1ec1e9634285e74f7ec_context-management-light-1.png)

卸载会阻止小峰值，而总结会“重置”整体爬升

* 峰值是大型工具结果/人工消息到达；卸载会在模型看到之前将每个内容交换为简短的预览，因此上下文只会增长一点点。
* 摘要处理缓慢的爬升：一旦使用率达到 85%，较旧的消息将被压缩为摘要，并且上下文会回落。

SummarizationMiddleware 在每次模型调用之前检查词元使用情况：

1. 一旦使用量超过阈值（默认为模型上下文窗口的 85%），单独的 LLM 调用会将旧消息压缩为单个摘要
2. 较旧的消息将从上下文窗口中删除，而最新消息则逐字保留。
3. 模型现在首先看到摘要，然后是最近的消息（因此最近的消息不会被解释）。

两个重要细节：

* **它是可恢复的。** 汇总的消息被写入/conversation\_history/{session\_id}.md. 如果智能体在起草时需要 A 公司研究的详细信息，它可以将其读回。
* **它循环。** 随着运行的继续，使用率再次攀升，下一个摘要包括上一个摘要。

**您还可以在主题发生变化时进行总结**，而不仅仅是在某个词元阈值时进行总结。自定义摘要提示会很有帮助。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6acfbe0540e67f7ab8076547_offloading-vs-summarization-table-transparent.png)

我们关于[Deep Agents的上下文管理](https://www.langchain.com/blog/context-management-for-deepagents) 的文章更详细地介绍了这两个方面。

## 技巧：仅在需要时加载信息

假设您的销售团队有特定的季度业务审查格式。智能体每季度只需要一次这些指令，因此将它们保留在系统提示中意味着每次调用时都要为其付费（以令​​牌和响应时间为单位）。相反，您可以将此信息打包为技能。

技能是一个指令文件夹（带有可选脚本和参考文档），为智能体提供完成专门任务所需的信息。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ac7d428941b180be1e389ce_skill-anatomy-light.png)

技能文件夹剖析

智能体会在前面看到一个简短的描述，并且仅当 QBR 出现时才加载 qbr-report 的完整指令（其他任务从不携带它们）。

技能会分层加载上下文，因此窗口会保持很小，直到某些内容真正相关为止。这称为渐进式披露：模型会预先看到一个“菜单”，并在需要时提取完整的配方，因此十项技能的上下文成本与十项俏皮话的成本差不多。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ac7d44dddd1bd24cf8c1560_skills-progressive-disclosure-light.gif)

渐进式披露（动画）

您将智能体指向您的技能，SkillsMiddleware 使用两个钩子：

1. 在智能体启动之前，它会扫描技能文件夹并仅读取每个 SKILL.md 的标头。
2. 在每次模型调用时，它都会将这些名称和描述添加到系统提示符中。

仅当模型确定技能相关时（并使用read\_file工具读取它），完整的指令才会进入上下文，因此我们的智能体在没有模板的情况下进行研究，并且仅在格式化 QBR 时才加载它。

‍

## 子智能体：隔离嘈杂的工作

卸载可以有效地解决过大的结果，但是对于您已经“知道”会很嘈杂的工作（例如通过数十个搜索和页面研究一家公司），子智能体是一个很好的设计选择。子智能体在自己的上下文窗口中执行此操作，并仅返回最终结果，以便主智能体永远不会看到“噪音”。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ac7d4926b0fa2c1f904c517_subagents-light-still.png)

SubAgentMiddleware 允许我们自定义子智能体可用的系统提示和工具。

```
market_researcher = {
    "name": "market-researcher",
    "description": "Researches a company and returns the 3 most notable developments.",
    "system_prompt": "Use pull_market_report, then return 3 short bullet points. Do not return the raw report.",
    "tools": [pull_market_report],
}

agent = create_deep_agent(model=model, subagents=[market_researcher])
```
 在我们的例子中，主智能体将每家公司交给市场研究子智能体。

研究人员子智能体在自己的上下文中读取完整报告并仅返回三个项目符号，因此主智能体只能看到这三个项目符号（甚至看不到原始报告的预览）。此外，由于子智能体任务往往较小且范围广泛，因此它们通常可以在更便宜的模型上并行运行。

‍

## 长期记忆：在对话中持续存在

到最后，您的智能体将会学到很多东西。有些有用，有些则没有。

假设您告诉您的智能体，“在摘要中使用要点，而不是段落。”如果没有记忆，你可能每周都会重复这样的事情。在 Deep Agents 中，长期记忆是一个 markdown 文件。您用一个参数将智能体指向它，MemoryMiddleware 会处理其余的事情：

1. **加载：** 在运行开始时读取文件。
2. **Inject：** 其内容会在每次模型调用时添加到系统提示符中。
3. **更新：** 当智能体了解到值得保留的内容（例如您的格式首选项）时，它会更新文件。

‍

## 交换模型，保留内存

Deep Agents 与提供商无关，并且可以牢记在心。因为内存是您自己存储中的普通文件（不是提供者保留的东西），所以您可以将相同的后端指向不同的模型：

```
agent = create_deep_agent(
    model="openai:gpt-6",  # different provider, same memory
    memory=["/memories/AGENTS.md"],
    backend=backend,
    store=store,
)
```
 下周，不同的模型可以读取相同的文件，并且仍然以项目符号形式写入摘要。

## 要记住的上下文工程策略

无论您是基于 Deep Agents 进行构建、使用其他工具还是自己构建工具，都需要注意以下事项：

* **大输入应该被卸载，而不是被截断。** 截断是有损的；卸载使其可恢复。
* **压缩应该是可恢复的。** 汇总后，智能体仍然可以获取它需要的详细信息。
* **专业知识应按需加载。** 系统中每项任务的说明都会在每次调用时提示成本上下文。
* **嘈杂的工作应该被隔离。** 具有自己上下文的子智能体可以让主智能体保持专注。
* **您应该拥有内存。** 您控制的存储中的内存在模型或提供商切换后仍然存在。
* **默认值应该是可定制的。** 适合一项任务的阈值很少适合所有任务。

## 尝试一下

```
uv add deepagents
```
 想向现场讲师学习更多信息吗？我将在 11 月 3 日对此进行报道：[此处](https://events.langchain.com/register/agent-memory-101-context-engineering/) 注册！

‍

**管理上下文只是故事的一半。另一半是从一开始就获取正确的信息。阅读** [**检索博客**](https://www.langchain.com/blog/context-engineering-starts-with-retrieval) **下一步。**

要深入了解上下文工程，请查看我们免费的自定进度的【浪链学院Deep Agents课程】(https://about:blank)

###相关内容

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6add442530f2704b9d5e03af_HVZbWoXb0AAOzqm.png)

Deep Agents

#### 构建“公司运行框架”的五个组成部分

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6a056ea05f3880a1361b47cf_Harrison.avif)

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6a56f3a3a4a725f72a70441f_caspar-b.jpeg)

哈里森·蔡斯

卡斯帕·布罗克赫伊森

2026 年 10 月 24 日

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

6

分钟

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6adb940c2b1a77d3a87ae860_dark-52%20characters%20max.png)

Deep Agents

概念指南

#### 上下文工程从检索开始

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6acfb8492227373b922e7719_Screenshot%202026-10-14%20at%2010.12.17%E2%80%AFAM.png)

翁洁丝

2026 年 10 月 23 日

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

11

分钟

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ac91132385fb9bbe1cb53b1_mda-reactions-blog-cover-navy-1200x675.png)

Deep Agents

教程和操作方法

#### 使用托管Deep Agents构建出色的开箱即用用户体验

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ab416d4dafca27a7246c1d0_Nathan%20Drezner.jpg)

内森·德雷兹纳

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

