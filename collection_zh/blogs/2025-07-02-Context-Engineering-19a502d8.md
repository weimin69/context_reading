> 本文为简体中文机器翻译，使用 Google Translate 公开接口并统一技术术语，尚未经逐句人工校对。代码、链接和公式按原文保留；实验数字及技术结论请对照原文。
> [查看本地英文原文](../../collection/blogs/2025-07-02-Context-Engineering-19a502d8.md) · [原始来源](https://www.langchain.com/blog/context-engineering-for-agents)

# 上下文工程

- 来源: https://www.langchain.com/blog/context-engineering-for-agents- 发布日期: 2025-07-02- 日期依据: JSON-LD datePublished- 类型: blog- 主题: 上下文工程、写入、选择、压缩、隔离- 抓取状态: article_html- 正文来源: https://www.langchain.com/blog/context-engineering-for-agents- 抓取时间 UTC: 2026-10-26T09:26:38.743473+00:00

## 来源摘要/页面简介

AI 智能体的上下文工程策略：编写、选择、压缩和隔离上下文以优化性能并管理长时间运行的任务。

## 抓取正文（中文翻译）

教程和操作方法

郎图

部署

# 上下文工程

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69d50051c5c24f19b81fd73a_Group%202147239256-2.svg)

浪链团队

2025 年 7 月 2 日

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69ce2c533137196179bae949_Icon-7.svg)

14

分钟

[返回博客](https://www.langchain.com/blog)

[创建智能体](https://www.langchain.com/blog/context-engineering-for-agents#)

[创建智能体](https://www.langchain.com/blog/context-engineering-for-agents#)

分享

## 长篇大论；博士

智能体需要上下文来执行任务。上下文工程是在智能体轨迹的每一步用正确的信息填充上下文窗口的艺术和科学。在这篇文章中，我们通过回顾各种流行的智能体和论文，分解了上下文工程的一些常见策略 - **编写、选择、压缩和隔离 -**。然后我们解释 LangGraph 是如何设计来支持它们的！

**另外，请观看我们有关上下文工程的视频** [**此处**](https://youtu.be/4GiqzUHD5AA?ref=blog.langchain.com)**.**

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69cbaaa8d3aab32815f859f4_image-4.png)

上下文工程的一般类别

## 上下文工程

正如 Andrej Karpathy 所说，法学硕士就像一种[新型操作系统](https://www.youtube.com/watch?si=-aKY-x57ILAmWTdw&t=620&v=LCEmiRjPEtQ&feature=youtu.be&ref=blog.langchain.com)。 LLM就像CPU，它的[上下文窗口](https://docs.anthropic.com/en/docs/build-with-claude/context-windows?ref=blog.langchain.com)就像RAM，作为​​模型的工作内存。就像 RAM 一样，LLM 上下文窗口处理各种上下文源的[容量](https://lilianweng.github.io/posts/2023-06-23-agent/?ref=blog.langchain.com) 是有限的。正如操作系统管理 CPU RAM 中的内容一样，我们可以认为“上下文工程”扮演着类似的角色。 [Karpathy总结得很好](https://x.com/karpathy/status/1937902205765607626?ref=blog.langchain.com)：

> *[上下文工程是]“……用下一步正确的信息填充上下文窗口的精致艺术和科学。”*

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69cbaaa8d3aab32815f859e3_image-1.png)

LLM申请中常用的上下文类型

在构建 LLM 应用程序时，我们需要管理哪些类型的上下文？上下文工程作为一个[保护伞](https://x.com/dexhorthy/status/1933283008863482067?ref=blog.langchain.com)，适用于几种不同的上下文类型：

* **说明** – 提示、记忆、少量示例、工具说明等
* **知识** – 事实、记忆等
* **工具** – 来自工具调用的反馈

## 智能体的上下文工程

今年，随着法学硕士在[推理](https://platform.openai.com/docs/guides/reasoning?api-mode=responses&ref=blog.langchain.com)和[工具调用](https://www.anthropic.com/engineering/building-effective-agents?ref=blog.langchain.com)方面变得更好，对[智能体](https://www.anthropic.com/engineering/building-effective-agents?ref=blog.langchain.com)的兴趣急剧增长。 [智能体](https://www.anthropic.com/engineering/building-effective-agents?ref=blog.langchain.com) 交错[LLM 调用和工具调用](https://www.anthropic.com/engineering/building-effective-agents?ref=blog.langchain.com)，通常用于[长时间运行的任务](https://blog.langchain.com/introducing-ambient-agents/)。智能体交错[LLM调用和工具调用](https://www.anthropic.com/engineering/building-effective-agents?ref=blog.langchain.com)，使用工具反馈来决定下一步。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69cbaaa8d3aab32815f859dd_image-2.png)

智能体交错[LLM调用和工具调用](https://www.anthropic.com/engineering/building-effective-agents?ref=blog.langchain.com)，使用工具反馈来决定下一步

然而，长时间运行的任务和积累的工具调用反馈意味着智能体通常会使用大量词元。这可能会导致许多问题：它可能[超出上下文窗口的大小](https://cognition.ai/blog/kevin-32b?ref=blog.langchain.com)、增加成本/延迟或降低智能体性能。 Drew Breunig [很好地概述了](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html?ref=blog.langchain.com) 较长上下文可能导致执行问题的一些具体方式，包括：

* [情境中毒：当幻觉进入情境时](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html?ref=blog.langchain.com#context-poisoning)
* [情境干扰：当情境压倒训练时](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html?ref=blog.langchain.com#context-distraction)
* [上下文混乱：当多余的上下文影响响应时](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html?ref=blog.langchain.com#context-confusion)
* [语境冲突：当部分语境不一致时](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html?ref=blog.langchain.com#context-clash)

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69cbaaa8d3aab32815f859e0_image-3.png)

来自工具调用的上下文会在多个智能体轮流中累积

考虑到这一点，[认知](https://cognition.ai/blog/dont-build-multi-agents?ref=blog.langchain.com)强调了上下文工程的重要性：

> *“上下文工程”……实际上是构建 AI 智能体的工程师的首要工作。*

[人择](https://www.anthropic.com/engineering/built-multi-agent-research-system?ref=blog.langchain.com)也说得很清楚：

> *智能体经常进行数百轮对话，需要仔细的上下文管理策略。*

那么，今天人们如何应对这一挑战呢？我们将智能体上下文工程的常见策略分为四个部分 - **编写、选择、压缩和隔离 -** 并通过对一些流行智能体产品和论文的评论给出了每种策略的示例。然后我们解释 LangGraph 是如何设计来支持它们的！

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69cbaaa8d3aab32815f859f4_image-4.png)

上下文工程的一般类别

## 写入上下文

*写入上下文意味着将其保存在上下文窗口之外以帮助智能体执行任务。*

**便签本**

当人类解决任务时，我们会做笔记并记住未来相关任务的内容。特工也正在获得这些能力！通过“[便笺本](https://www.anthropic.com/engineering/claude-think-tool?ref=blog.langchain.com)”做笔记是在智能体执行任务时保存信息的一种方法。这个想法是将信息保存在上下文窗口之外，以便智能体可以使用。 [Anthropic 的多智能体研究员](https://www.anthropic.com/engineering/built-multi-agent-research-system?ref=blog.langchain.com) 说明了一个明显的例子：

> *LeadResearcher 首先思考该方法并将其计划保存到内存中以保留上下文，因为如果上下文窗口超过 200,000 个标记，它将被截断，因此保留该计划非常重要。*

便签本可以通过几种不同的方式来实现。它们可以是简单地[写入文件](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem?ref=blog.langchain.com)的[工具调用](https://www.anthropic.com/engineering/claude-think-tool?ref=blog.langchain.com)。它们也可以是在会话期间持续存在的运行时[状态对象](https://langchain-ai.github.io/langgraph/concepts/low_level/?ref=blog.langchain.com#state)中的字段。无论哪种情况，便签本都可以让智能体保存有用的信息来帮助他们完成任务。

**回忆**

便签本可以帮助智能体在给定会话（或[线程](https://langchain-ai.github.io/langgraph/concepts/persistence/?ref=blog.langchain.com#threads)）内解决任务，但有时智能体可以从*许多*会话中记住事情中受益！ [反射](https://arxiv.org/abs/2303.11366?ref=blog.langchain.com) 引入了在每次智能体转弯后进行反射并重新使用这些自我生成的记忆的想法。 [生成智能体](https://ar5iv.labs.arxiv.org/html/2304.03442?ref=blog.langchain.com) 根据过去智能体反馈的集合定期合成记忆。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69cbaaa8d3aab32815f859f1_image-5.png)

法学硕士可用于更新或创建记忆

这些概念融入了 [ChatGPT](https://help.openai.com/en/articles/8590148-memory-faq?ref=blog.langchain.com)、[Cursor](https://forum.cursor.com/t/0-51-memories-feature/98509?ref=blog.langchain.com) 和 [Windsurf](https://docs.windsurf.com/windsurf/cascade/memories?ref=blog.langchain.com) 等流行产品中，这些产品都具有自动生成长期记忆的机制，这些长期记忆可以基于用户智能体交互在会话中持续存在。

## 选择上下文

*选择上下文意味着将其拉入上下文窗口以帮助智能体执行任务。*

**便签本**

从暂存器选择上下文的机制取决于暂存器的实现方式。如果它是一个[工具](https://www.anthropic.com/engineering/claude-think-tool?ref=blog.langchain.com)，那么智能体可以通过调用工具来简单地读取它。如果它是智能体运行时状态的一部分，那么开发人员可以选择每一步向智能体公开哪些状态部分。这提供了细粒度的控制，以便在以后向 LLM 公开暂存器上下文。

**回忆**

如果智能体有能力保存记忆，他们还需要有能力选择与他们正在执行的任务相关的记忆。由于几个原因，这可能很有用。智能体可能会选择少量示例（[情景](https://langchain-ai.github.io/langgraph/concepts/memory/?ref=blog.langchain.com#memory-types) [记忆](https://arxiv.org/pdf/2309.02427?ref=blog.langchain.com)) 作为所需行为的示例、指导行为的指令（[程序](https://langchain-ai.github.io/langgraph/concepts/memory/?ref=blog.langchain.com#memory-types) [记忆](https://arxiv.org/pdf/2309.02427?ref=blog.langchain.com)) 或事实([语义](https://langchain-ai.github.io/langgraph/concepts/memory/?ref=blog.langchain.com#memory-types) [记忆](https://arxiv.org/pdf/2309.02427?ref=blog.langchain.com)) 用于与任务相关的上下文。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69cbaaa8d3aab32815f859e6_image-6.png)

一项挑战是确保选择相关记忆。一些流行的智能体只是使用一组狭窄的文件，这些文件“总是”被拉入上下文。例如，许多代码智能体使用特定文件来保存指令（“程序”存储器），或者在某些情况下保存示例（“情景”存储器）。克劳德代码使用[`CLAUDE.md`](http://claude.md/?ref=blog.langchain.com)。 [光标](https://docs.cursor.com/context/rules?ref=blog.langchain.com)和[风帆](https://windsurf.com/editor/directory?ref=blog.langchain.com)使用规则文件。

但是，如果智能体存储更大的[集合](https://langchain-ai.github.io/langgraph/concepts/memory/?ref=blog.langchain.com#collection)事实和/或关系（例如，[语义](https://langchain-ai.github.io/langgraph/concepts/memory/?ref=blog.langchain.com#memory-types)记忆），选择就更困难。 [ChatGPT](https://help.openai.com/en/articles/8590148-memory-faq?ref=blog.langchain.com) 是一个流行产品的一个很好的例子，它可以存储大量用户特定的记忆并从中进行选择。

用于内存索引的嵌入和/或[知识](https://arxiv.org/html/2501.13956v1?ref=blog.langchain.com#:~:text=In%20Zep%2C%20memory%20is%20powered,subgraph%2C%20and%20a%20community%20subgraph)[图表](https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/?ref=blog.langchain.com#:~:text=changes%20since%20updates%20can%20trigger,and%20holistic%20memory%20for%20agentic)通常用于协助选择。尽管如此，内存选择仍然具有挑战性。  在 AIEngineer 世界博览会上，[Simon Willison 分享](https://simonwillison.net/2025/Jun/6/six-months-in-llms/?ref=blog.langchain.com) 一个选择错误的示例：ChatGPT 从内存中获取了他的位置，并意外地将其注入到请求的图像中。这种类型的意外或不需要的内存检索可能会让一些用户感觉上下文窗口“*不再属于他们*”！

**工具**

智能体使用工具，但如果提供太多工具，他们可能会变得过载。这通常是因为工具描述重叠，导致模型对使用哪个工具感到困惑。一种方法是[将 RAG（检索增强生成）应用于工具描述](https://arxiv.org/abs/2410.14594?ref=blog.langchain.com)，以便仅获取与任务最相关的工具。一些[最近的论文](https://arxiv.org/abs/2505.03275?ref=blog.langchain.com) 表明，这可以将工具选择的准确性提高 3 倍。

**知识**

[RAG](https://github.com/langchain-ai/rag-from-scratch?ref=blog.langchain.com) 是一个丰富的主题，它[可以成为一个中心上下文工程挑战](https://x.com/_mohansolo/status/1899630246862966837?ref=blog.langchain.com)。代码智能体是大规模生产中 RAG 的一些最佳示例。 Windsurf 的 Varun 很好地抓住了其中一些挑战：

> *索引代码≠上下文检索……[我们正在做索引和嵌入搜索……[使用]AST解析代码并沿着语义上有意义的边界进行分块……随着代码库大小的增长，嵌入搜索作为检索启发式变得不可靠……我们必须依靠 grep/文件搜索、基于知识图的检索等技术的组合，以及……重新排名步骤，其中[上下文]按相关性顺序排名。*

## 压缩上下文

*压缩上下文涉及仅保留执行任务所需的词元。*

**上下文总结**

智能体交互可以跨越[数百轮](https://www.anthropic.com/engineering/built-multi-agent-research-system?ref=blog.langchain.com)并使用大量词元的工具调用。总结是应对这些挑战的一种常见方法。如果您使用过 Claude Code，您就会看到它的实际效果。在超过上下文窗口的 95% 后，Claude Code 会运行“[auto-compact](https://docs.anthropic.com/en/docs/claude-code/costs?ref=blog.langchain.com)”，它将总结用户智能体交互的完整轨迹。这种跨[智能体轨迹](https://langchain-ai.github.io/langgraph/concepts/memory/?ref=blog.langchain.com#manage-short-term-memory)的压缩可以使用各种策略，例如[递归](https://arxiv.org/pdf/2308.15022?ref=blog.langchain.com#:~:text=the%20retrieved%20utterances%20capture%20the,based%203)或[分层](https://alignment.anthropic.com/2025/summarization-for-monitoring/?ref=blog.langchain.com#:~:text=We%20addressed%20these%20issues%20by,of%20our%20computer%20use%20capability)汇总。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69cbaaa8d3aab32815f859fd_image-7.png)

几个可以应用总结的地方

在智能体设计中的特定点[添加摘要](https://github.com/langchain-ai/open_deep_research/blob/e5a5160a398a3699857d00d8569cb7fd0ac48a4f/src/open_deep_research/utils.py?ref=blog.langchain.com#L1407)也很有用。例如，它可用于后处理某些工具调用（例如，大量词元的搜索工具）。作为第二个例子，[认知](https://cognition.ai/blog/dont-build-multi-agents?ref=blog.langchain.com#a-theory-of-building-long-running-agents)提到了在智能体-智能体边界处进行汇总，以减少知识传递期间的词元。如果需要捕获特定事件或决策，总结可能是一个挑战。 [认知](https://cognition.ai/blog/dont-build-multi-agents?ref=blog.langchain.com#a-theory-of-building-long-running-agents) 为此使用了一个微调模型，这强调了这一步需要做多少工作。

**上下文修剪**

总结通常使用法学硕士来提取最相关的上下文，而修剪通常可以过滤或如 Drew Breunig 指出的“[prune](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html?ref=blog.langchain.com)”上下文。这可以使用硬编码启发式方法，例如从列表中删除[旧消息](https://python.langchain.com/docs/how_to/trim_messages/?ref=blog.langchain.com)。德鲁还提到了 [Provence](https://arxiv.org/abs/2501.16214?ref=blog.langchain.com)，一个训练有素的问答上下文修剪器。

## 隔离上下文

*隔离上下文涉及将其拆分以帮助智能体执行任务。*

**多智能体**

隔离上下文的最流行的方法之一是将其拆分到子智能体之间。 OpenAI [Swarm](https://github.com/openai/swarm?ref=blog.langchain.com) 库的动机是[关注点分离](https://openai.github.io/openai-agents-python/ref/agent/?ref=blog.langchain.com)，其中一组智能体可以处理特定的子任务。每个智能体都有一组特定的工具、指令和自己的上下文窗口。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69cbaaa8d3aab32815f85a00_image-8.png)

跨多个智能体分割上下文

Anthropic 的[多智能体研究员](https://www.anthropic.com/engineering/built-multi-agent-research-system?ref=blog.langchain.com) 对此进行了论证：许多具有隔离上下文的智能体的性能优于单智能体，很大程度上是因为每个子智能体上下文窗口可以分配给更窄的子任务。正如博客所说：

> *[子智能体操作]与自己的上下文窗口并行，同时探索问题的不同方面。*

当然，多智能体的挑战包括词元使用（例如，根据 Anthropic 的报告，比聊天多 [15 倍的词元](https://www.anthropic.com/engineering/built-multi-agent-research-system?ref=blog.langchain.com)）、需要仔细的[提示工程](https://www.anthropic.com/engineering/built-multi-agent-research-system?ref=blog.langchain.com) 来规划子智能体工作以及子智能体的协调。

**与环境的上下文隔离**

HuggingFace 的[深度研究员](https://huggingface.co/blog/open-deep-research?ref=blog.langchain.com#:~:text=From%20building%20,it%20can%20still%20use%20it)展示了上下文隔离的另一个有趣的例子。大多数智能体使用[工具调用 API](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview?ref=blog.langchain.com)，它返回 JSON 对象（工具参数），这些对象可以传递给工具（例如搜索 API）以获取工具反馈（例如搜索结果）。 HuggingFace 使用 [CodeAgent](https://huggingface.co/papers/2402.01030?ref=blog.langchain.com)，其输出包含所需的工具调用。然后代码在[沙箱](https://e2b.dev/?ref=blog.langchain.com)中运行。然后将工具调用中选定的上下文（例如返回值）传递回 LLM。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69cbaaa8d3aab32815f859fa_image-9.png)

沙箱可以将上下文与法学硕士隔离。

这使得上下文可以与环境中的 LLM 隔离。 Hugging Face 指出，这是隔离大量词元对象的好方法，特别是：

> *[代码智能体允许]更好地处理状态……需要存储此图像/音频/其他内容以供以后使用？没问题，只需将其分配为变量* [*在您的状态中并且您[稍后使用它]*](https://deepwiki.com/search/i-am-wondering-if-state-that-i_0e153539-282a-437c-b2b0-d2d68e51b873?ref=blog.langchain.com)*.*

**状态**

值得一提的是，智能体的运行时[状态对象](https://langchain-ai.github.io/langgraph/concepts/low_level/?ref=blog.langchain.com#state)也可以是隔离上下文的好方法。这可以起到与沙箱相同的作用。可以使用具有可写入上下文的字段的[模式](https://langchain-ai.github.io/langgraph/concepts/low_level/?ref=blog.langchain.com#schema)来设计状态对象。模式的一个字段（例如，`messages`)可以在智能体的每一回合向 LLM 公开，但模式可以隔离其他字段中的信息，以便更有选择性地使用。

## 使用 LangSmith / LangGraph 进行上下文工程

那么，如何应用这些想法呢？在开始之前，有两个有用的基础部分。首先，确保您有办法[查看您的数据](https://hamel.dev/blog/posts/evals/?ref=blog.langchain.com) 并跟踪整个智能体的词元使用情况。这有助于了解在哪里最好地应用工作环境工程。 [LangSmith](https://docs.smith.langchain.com/?ref=blog.langchain.com) 非常适合智能体[追踪/可观察性](https://docs.smith.langchain.com/observability?ref=blog.langchain.com)，并提供了一种很好的方法来做到这一点。其次，确保您有一种简单的方法来测试上下文工程是否会损害或提高智能体性能。 LangSmith 启用[智能体评估](https://docs.smith.langchain.com/evaluation/tutorials/agents?ref=blog.langchain.com) 来测试任何上下文工程工作的影响。

**写上下文**

LangGraph 的设计同时具有线程范围（[短期](https://langchain-ai.github.io/langgraph/concepts/memory/?ref=blog.langchain.com#short-term-memory)）和[长期记忆](https://langchain-ai.github.io/langgraph/concepts/memory/?ref=blog.langchain.com#long-term-memory)。短期记忆使用[检查点](https://langchain-ai.github.io/langgraph/concepts/persistence/?ref=blog.langchain.com)在智能体的所有步骤中持久保存[智能体状态](https://langchain-ai.github.io/langgraph/concepts/low_level/?ref=blog.langchain.com#state)。这作为“便签本”非常有用，允许您编写信息以在智能体轨迹的任何步骤中声明和获取它。

LangGraph 的长期记忆可让您与智能体保持*跨多个会话*的上下文。它很灵活，允许您保存小组[文件](https://langchain-ai.github.io/langgraph/concepts/memory/?ref=blog.langchain.com#profile)（例如用户配置文件或规则）或更大的[集合](https://langchain-ai.github.io/langgraph/concepts/memory/?ref=blog.langchain.com#collection)记忆。此外，[LangMem](https://langchain-ai.github.io/langmem/?ref=blog.langchain.com) 提供了一组广泛的有用抽象来帮助 LangGraph 内存管理。

**选择上下文**

在 LangGraph 智能体的每个节点（步骤）中，您可以获取 [state](https://langchain-ai.github.io/langgraph/concepts/low_level/?ref=blog.langchain.com#state)。这使您可以精细控制在每个智能体步骤中向 LLM 提供的上下文。

此外，LangGraph 的长期记忆可在每个节点内访问，并支持各种类型的检索（例如，获取文件以及[对记忆集合进行基于嵌入的检索]。](https://langchain-ai.github.io/langgraph/cloud/reference/cli/?ref=blog.langchain.com#adding-semantic-search-to-the-store)有关长期记忆的概述，请参阅[我们的 Deeplearning.ai 课程](https://www.deeplearning.ai/short-courses/long-term-agentic-memory-with-langgraph/?ref=blog.langchain.com)。对于应用于特定智能体的内存入口点，请参阅我们的[环境智能体](https://academy.langchain.com/courses/ambient-agents?ref=blog.langchain.com)课程。这展示了如何在长期运行的智能体中使用 LangGraph 内存，该智能体可以管理您的电子邮件并从您的反馈中学习。

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69cbaaa8d3aab32815f859f7_image-10.png)

具有用户反馈和长期记忆的电子邮件智能体

对于工具选择，[LangGraph Bigtool](https://github.com/langchain-ai/langgraph-bigtool?ref=blog.langchain.com) 库是对工具描述应用语义搜索的好方法。这有助于在使用大量工具时为任务选择最相关的工具。最后，我们有几个[教程和视频](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/?ref=blog.langchain.com)，展示了如何将各种类型的 RAG 与 LangGraph 结合使用。

**压缩上下文**

因为 LangGraph [是一个低级编排框架](https://blog.langchain.com/how-to-think-about-agent-frameworks/)，所以您[将智能体布局为一组节点](https://www.youtube.com/watch?v=aHCDrAbH_go&ref=blog.langchain.com)，[定义](https://blog.langchain.com/how-to-think-about-agent-frameworks/)每个节点内的逻辑，并定义在它们之间传递的状态对象。该控件提供了多种压缩上下文的方法。

一种常见的方法是使用消息列表作为智能体状态，并定期使用[一些内置实用程序](https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/?ref=blog.langchain.com#manage-short-term-memory)对其进行[总结或修剪](https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/?ref=blog.langchain.com#manage-short-term-memory)。但是，您还可以通过几种不同的方式添加逻辑到后处理[工具调用](https://github.com/langchain-ai/open_deep_research/blob/e5a5160a398a3699857d00d8569cb7fd0ac48a4f/src/open_deep_research/utils.py?ref=blog.langchain.com#L1407) 或智能体的工作阶段。您可以在特定点添加汇总节点，也可以向工具调用节点添加汇总逻辑，以压缩特定工具调用的输出。

**隔离上下文**

LangGraph 是围绕 [state](https://langchain-ai.github.io/langgraph/concepts/low_level/?ref=blog.langchain.com#state) 对象设计的，允许您在每个智能体步骤指定状态模式和访问状态。例如，您可以将工具调用的上下文存储在状态的某些字段中，将它们与 LLM 隔离，直到需要该上下文为止。除了状态之外，LangGraph 还支持使用沙箱进行上下文隔离。请参阅此 [repo](https://github.com/jacoblee93/mini-chat-langchain?tab=readme-ov-file&ref=blog.langchain.com)，了解使用 [E2B 沙箱](https://e2b.dev/?ref=blog.langchain.com) 进行工具调用的示例 LangGraph 智能体。请参阅此[视频](https://www.youtube.com/watch?v=FBnER2sxt0w&ref=blog.langchain.com)，了解使用 Pyodide 进行沙箱保存状态的示例。 LangGraph还对构建多智能体架构有很多支持，例如[supervisor](https://github.com/langchain-ai/langgraph-supervisor-py?ref=blog.langchain.com)和[swarm](https://github.com/langchain-ai/langgraph-swarm-py?ref=blog.langchain.com)库。您可以[参见](https://www.youtube.com/watch?v=4nZl32FwU-o&ref=blog.langchain.com)[这些](https://www.youtube.com/watch?v=JeyDrn1dSUQ&ref=blog.langchain.com)[视频](https://www.youtube.com/watch?v=B_0TNuYi56w&ref=blog.langchain.com)了解有关在 LangGraph 中使用多智能体的更多详细信息。

## 结论

上下文工程正在成为智能体构建者应该掌握的一门手艺。在这里，我们介绍了当今许多流行智能体中常见的一些模式：

* *写入上下文 - 将其保存在上下文窗口之外以帮助智能体执行任务。*
* *选择上下文 - 将其拉入上下文窗口以帮助智能体执行任务。*
* *压缩上下文 - 仅保留执行任务所需的词元。*
* *隔离上下文 - 将其分割以帮助智能体执行任务。*

LangGraph 可以轻松实现它们中的每一个，并且 LangSmith 提供了一种简单的方法来测试智能体并跟踪上下文使用情况。 LangGraph 和 LangGraph 共同实现了良性反馈循环，用于识别应用上下文工程、实施、测试和重复的最佳机会。

###相关内容

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

![可以付费的智能体：使用 Stripe 的 Link 和托管Deep Agents构建 Restock](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ac718f4c65195ca032e3790_restock-cover.png)

Deep Agents

教程和操作方法

合伙人

#### 可以付费的智能体：使用 Stripe 的 Link 和 Managed Deep Agents 构建 Restock

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6a4db1f172cf600d53600698_srimanth-t.jpeg)

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69dcee60745f0e15b18ad4d5_sydney-runkle.png)

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ab416d4dafca27a7246c1d0_Nathan%20Drezner.jpg)

斯里曼斯·唐吉迪帕利

悉尼·朗克尔

内森·德雷兹纳

2026 年 10 月 8 日

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

6

分钟

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ab6ba616821ea2bd3edd56a_webflow-cover-light-building-prod-jev-langgraph-1600x900.png)

开源

智能体架构

郎图

#### 使用 Jev 和 LangGraph 构建产品

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69dcee60745f0e15b18ad4d5_sydney-runkle.png)

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69e12735c02bb07c894a067a_hunter-lovell.png)

悉尼·朗克尔

亨特·洛弗尔

2026 年 9 月 25 日

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

9

分钟

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69ce01ea562f8cc223cabf25_Frame%202147254328.svg)

谢谢！您的提交已收到！

哎呀！提交表单时出现问题。

### 查看您的智能体真正在做什么

LangSmith 是我们的智能体工程平台，可帮助开发人员调试每个智能体决策、评估更改并一键部署。

[尝试 LangSmith](https://smith.langchain.com/)[获取演示](https://www.langchain.com/contact-sales)

