> 本文为简体中文机器翻译，使用 Google Translate 公开接口并统一技术术语，尚未经逐句人工校对。代码、链接和公式按原文保留；实验数字及技术结论请对照原文。
> [查看本地英文原文](../../collection/papers/2026-05-12-LongMemEval-V2-Evaluating-Long-Term-Agent-Memory-Toward-Experienced-Colleagues-1c5d49ed.md) · [原始来源](https://arxiv.org/abs/2605.12493)

# LongMemEval-V2：评估智能体长期记忆，迈向经验丰富的协作伙伴

- 来源: https://arxiv.org/abs/2605.12493- 发布日期: 2026-05-12- 日期依据: page metadata: citation_date- 类型: paper- 主题: 长期记忆评估、LongMemEval-V2- 抓取状态: full_text_html- 正文来源: https://arxiv.org/html/2605.12493- 抓取时间 UTC: 2026-10-26T09:36:31.340418+00:00 - 作者: Wu, Di, Ji, Zixiang, Kawatkar, Asmi, Kwan, Bryan, Gu, Jia-Chen, Peng, Nanyun, Chang, Kai-Wei

## 来源摘要/页面简介

摘要：长期记忆对于专门网络环境中的智能体至关重要，其中的成功取决于对界面可供性、状态动态、工作流程和重复出现的故障模式的回忆。然而，现有的智能体记忆基准主要关注用户历史、短踪迹或下游任务成功，如何直接评估记忆系统是否有效地内化特定环境的体验仍然是一个悬而未决的问题。为了解决这一差距，我们引入了 LongMemEval-V2 (LME-V2)，这是一个评估内存系统是否可以帮助智能体获得在定制环境中成为知识渊博的同事所需的经验的基准。 LME-V2 包含 451 个手动策划的问题，涵盖 Web 智能体的五种核心记忆能力：静态回忆、动态状态跟踪、工作流程知识、环境陷阱和前提感知。问题与历史轨迹配对，其中包含多达 500 条轨迹和 1.15 亿个词元。我们使用上下文收集公式：记忆系统消耗历史轨迹并返回下游问答的紧凑证据。我们提出了一套两种内存方法：AgentRunbook-R，一种基于 RAG 的高效内存，具有用于原始状态观察、事件和策略注释的知识池；以及 AgentRunbook-C，它将轨迹存储为文件并调用编码智能体在增强沙箱中收集证据。实验表明，AgentRunbook-C 实现了最佳性能，平均准确率为 72.5%，优于最强的 RAG 基线 (48.5%) 和现成的编码智能体基线 (69.3%)。尽管性能提升显着，但基于编码智能体的方法具有很高的延迟成本。虽然 AgentRunbook-C 提高了准确性-延迟帕累托边界，但仍然存在很大的改进空间。总之，这些结果使 LME-V2 成为开发环境体验长期记忆系统的具有挑战性的测试平台。

## 抓取正文（中文翻译）

# LongMemEval-V2：针对经验丰富的同事评估长期智能体记忆

Di Wu ††感谢：通讯至 {diwu,kwchang}@cs.ucla.edu。
  
季子祥
  
阿斯米·卡瓦特卡
  
布莱恩·关 (Bryan Kwan) 隶属关系：顾嘉晨 (Jia-Chen Gu)
  
彭南云
  
Kai-Wei Chang 所属机构：加州大学洛杉矶分校 所属机构：<https://xiaowu0162.github.io/longmemeval-v2/>

###### 摘要

长期记忆对于专门网络环境中的智能体至关重要，其中成功取决于回忆界面功能、状态动态、工作流程和重复出现的故障模式。然而，现有的智能体记忆基准主要关注用户历史、短踪迹或下游任务成功，如何直接评估记忆系统是否有效地内化特定环境的体验仍然是一个悬而未决的问题。为了解决这一差距，我们引入了 LongMemEval-V2 (LME-V2)，这是一个评估内存系统是否可以帮助智能体获得在定制环境中成为知识渊博的同事所需的经验的基准。 LME-V2 包含 451 个手动策划的问题，涵盖 Web 智能体的五种核心记忆能力：静态回忆、动态状态跟踪、工作流程知识、环境陷阱和前提感知。这些问题与包含多达 500 条轨迹和 1.15 亿个词元的历史轨迹配对。我们使用上下文收集公式：记忆系统消耗历史轨迹并返回下游问答的紧凑证据。作为这一具有挑战性的设置的初始基线，我们提出了一套两种内存方法：AgentRunbook-R，一种基于 RAG 的高效内存，具有用于原始状态观察、事件和策略注释的知识池；以及 AgentRunbook-C，它将轨迹存储为文件并调用编码智能体在增强沙箱中收集证据。实验表明，AgentRunbook-C 实现了最佳性能，平均准确率为 72.5%，优于最强的 RAG 基线 (48.5%) 和现成的编码智能体基线 (69.3%)。尽管性能提升显着，但基于编码智能体的方法具有很高的延迟成本。虽然 AgentRunbook-C 提高了准确性-延迟帕累托边界，但仍然存在很大的改进空间。总之，这些结果使 LME-V2 成为开发长期记忆系统的具有挑战性的测试平台，将累积的智能体轨迹转化为可重用的环境经验。

## 1 简介

长期记忆通过长期存储和回忆信息，帮助大型语言模型 (LLM) 超越其上下文和参数进行操作（[Wu et al., 2022](https://arxiv.org/html/2605.12493#bib.bib43)；[Packer et al., 2023](https://arxiv.org/html/2605.12493#bib.bib32)；[Wang et al., 2024b](https://arxiv.org/html/2605.12493#bib.bib38))。内存对于智能体系统尤其重要，在智能体系统中，LLM 通过许多步骤与专门环境进行交互。最近的研究表明，记住任务过程、界面可供性和隐藏的故障模式可以提高智能体在推理时的性能（[Wang et al., 2024a](https://arxiv.org/html/2605.12493#bib.bib37); [Zhao et al., 2024](https://arxiv.org/html/2605.12493#bib.bib49); [Bouzenia et al., 2025](https://arxiv.org/html/2605.12493#bib.bib4)；[Wang 等人，2025b](https://arxiv.org/html/2605.12493#bib.bib40)；[Tang 等人，2025](https://arxiv.org/html/2605.12493#bib.bib34))。

然而，智能体环境中的记忆基准仍然有限。现有的记忆工作主要评估长文档或用户聊天历史的检索和推理（[Hsieh et al., 2024](https://arxiv.org/html/2605.12493#bib.bib13); [Bai et al., 2025](https://arxiv.org/html/2605.12493#bib.bib2); [Wu et al., 2025a](https://arxiv.org/html/2605.12493#bib.bib41); [Maharana等人，2024](https://arxiv.org/html/2605.12493#bib.bib25)；[Tavakoli 等人，2025](https://arxiv.org/html/2605.12493#bib.bib35))。最近的工作考虑评估智能体轨迹的记忆，但经常使用简化的游戏环境（[Fang et al., 2026](https://arxiv.org/html/2605.12493#bib.bib10); [Li et al., 2026](https://arxiv.org/html/2605.12493#bib.bib21)），强调一个或几个轨迹内的有限依赖性（[He et al., 2026](https://arxiv.org/html/2605.12493#bib.bib12)；[Zhao et al., 2026b](https://arxiv.org/html/2605.12493#bib.bib51))，或通过下游任务成功间接评估([He et al., 2026](https://arxiv.org/html/2605.12493#bib.bib12))。因此，对于记忆系统是否可以通过与复杂环境的持续交互来积累整体的、特定于环境的知识，它们提供的见解有限。为了强调这一观点，本文使用以下框架：

高质量的记忆使座席成为专业环境中经验丰富的同事。

在这种观点的推动下，我们引入了 LongMemEval-V2 (LME-V2)，这是一个评估内存系统是否可以帮助网络智能体获得成为知识渊博的同事所需的经验的基准。 LME-V2 利用定制网站，包括 Magento 购物、购物管理、Postmill 论坛以及来自 WebArena ([Zhou et al., 2024](https://arxiv.org/html/2605.12493#bib.bib52)) 和 WorkArena ([Drouin et al., 2024](https://arxiv.org/html/2605.12493#bib.bib8)) 的 ServiceNow；[Boisvert et al., 2024](https://arxiv.org/html/2605.12493#bib.bib3))。从解决任务的网络智能体轨迹中，我们手动策划了 451 个问题，涵盖五种核心记忆能力：静态回忆、动态状态跟踪、工作流程知识、环境陷阱和前提意识。我们在[图 1](https://arxiv.org/html/2605.12493#S1.F1“1 简介 ‣ LongMemEval-V2：评估经验丰富的同事的长期智能体记忆”)中提供了示例，并在§[3.1](https://arxiv.org/html/2605.12493#S3.SS1“3.1 核心记忆能力定义 ‣ 3 LongMemEval-V2 ‣”中提供了能力定义LongMemEval-V2：针对经验丰富的同事评估长期智能体记忆”）。这些问题是特定于定制环境的，因此最近的前沿法学硕士通常无法回答（§[3.4](https://arxiv.org/html/2605.12493#S3.SS4“3.4 试点研究 ‣ 3 LongMemEval-V2 ‣ LongMemEval-V2：评估经验丰富的同事的长期智能体记忆”)）。 LME-V2 进一步将问题与一系列网络智能体轨迹（“干草堆”，遵循 [Kamradt (2023)](https://arxiv.org/html/2605.12493#bib.bib17)）配对，其中只有一小部分包含每个问题的答案（“针”）。 LME-V2-Small 提供了所有问题共享的 100 条轨迹干草堆，LME-V2-Medium 提供了 500 条轨迹问题特定干草堆。与之前的基准相比，LME-V2 以其深层上下文（中小型层中的 25M/115M 词元）和全面的记忆能力覆盖范围提出了新的挑战（[表 1](https://arxiv.org/html/2605.12493#S1.T1“1 简介 ‣ LongMemEval-V2：针对经验丰富的同事评估长期智能体记忆”)）。

![参考说明](https://arxiv.org/html/2605.12493v1/main_figure.png)

图 1：LongMemEval-V2 问题示例。我们显示来自 WorkArena 域的示例。 LME-V2 问题锻炼了不同的记忆能力：静态（第 1 行）、动态（第 2 行）、工作流程（第 3 行）、陷阱（第 4 行）和前提意识（右列）。

LME-V2 使用上下文收集公式来评估记忆（§[3.3](https://arxiv.org/html/2605.12493#S3.SS3“3.3 评估公式 ‣ 3 LongMemEval-V2 ‣ LongMemEval-V2：评估经验丰富的同事的长期智能体记忆”)）。内存系统实现两个 API：Insert（消耗轨迹）和 Query（返回问题的多模式内存上下文）。对于每个问题，我们将相关的轨迹按顺序流式传输到内存中，调用查询，将返回的上下文截断为固定的词元预算，并要求固定的读者 LLM 来回答。这通过下游智能体将使用的实用接口提供了对内存质量的直接评估。我们报告答案准确性和查询延迟。

表 1：与现有内存和长上下文基准测试的比较。 # Sess.、# Tok. 和 # Q 表示会话或词元的历史记录大小以及问题总数。 MM 表示上下文或问题是否是文本和图像的多模态混合。对于具有多个预设长度层的基准，我们报告最小长度层和最大长度层之间的范围。对于其他基准，我们报告所有示例的平均上下文大小。

|  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|基准|域名 |背景简介| | |问题简介 | |记忆能力| | | | |
| # 赛斯。 | #托克。 | MM | # 问 | MM |静态|动态 |工作流程 |陷阱 |前提|
|一般长上下文 | | | | | | | | | | | |
|长凳 V2 |混合|不适用 | 26万| ✗ | 503 | 503 ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| MemoryAgentBench |混合|不适用 | 285k | 285k ✗ | 2,071 | 2,071 ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| CL-长凳|混合|不适用 | 10k | ✗ | 1,899 | 1,899 ✗ | ✓ | ✗ | ✓ | ✗ | ✗ |
|会话长上下文 | | | | | | | | | | | |
| LoCoMo | User-user chat | 28 | ∼\sim16k | ✓ | 7,512 | ✗ | ✓ | ✓ | ✗ | ✗ | ✓ |
| LongMemEval-V1 |用户助理聊天 | 48–475 | 48–475 115k–1.5M | ✗ | 500 | 500 ✗ | ✓ | ✓ | ✗ | ✗ | ✓ |
|人物记忆 |用户助理聊天 | 5–60 | 26k–951k | ✗ | 5,990 | 5,990 ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| PersonaMem-v2 |用户助理聊天 | 10-20 | 10-20 33k–124k | ✓ | 5,000 | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
|梁|用户助理聊天 | 4.5–100 | 124k–10M | ✗ | 2,000 | ✗ | ✓ | ✓ | ✗ | ✗ | ✓ |
|智能体长上下文 | | | | | | | | | | | |
|记忆竞技场 |智能体（混合）| 7 | 40k+ | ✗ | 766 | 766 ✗ | ✓ | ✗ | ✓ | ✓ | ✗ |
|特工LongBench |游戏智能体| 1 | 31k–4M | ✗ | 6,400 | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| EMemBench | Game agent | 1 | 2k–∞\infty | ✓ | 1,280+ | ✗ | ✓ | ✗ | ✓ | ✓ | ✓ |
| FileGramBench |文件系统智能体 | 12 | 12 11k | ✓ | 4,333 | 4,333 ✗ | ✓ | ✗ | ✓ | ✗ | ✗ |
| AMA 长凳 |智能体（混合）| 1 | 57k | ✗ | 2,496 | 2,496 ✗ | ✓ | ✓ | ✓ | ✓ | ✗ |
| LongMemEval-V2 |网络智能体| 100–498 | 25M–115M | ✓ | 451 | 451 ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

为了在 LME-V2 中取得成功，记忆系统需要智能地存储和过滤来自嘈杂智能体轨迹的信息，保留低级观察以及更高级的环境动态和程序知识。因此，流行的智能体记忆方法的天真应用可能是无效的，因为它们偏向于噪音较小的对话环境（[Chhikara et al., 2025](https://arxiv.org/html/2605.12493#bib.bib6)）或高级战略知识（[Wang et al., 2025b](https://arxiv.org/html/2605.12493#bib.bib40); [Ouyang et al., 2025](https://arxiv.org/html/2605.12493#bib.bib31))。在本文中，我们提出了 AgentRunbook，这是一个简单而有效的基线，由两个变体组成，分别针对效率和准确性进行了优化。 AgentRunbook-R 是一种高效的检索增强生成 (RAG) 管道，其灵感来自于智能体记忆工作，例如 [Xu 等人。 (2025)](https://arxiv.org/html/2605.12493#bib.bib45)。它提示 LLM 控制器更新并主动查询三个知识池：原始观察、状态转换事件和高级策略注释（§[4.1](https://arxiv.org/html/2605.12493#S4.SS1“4.1 AgentRunbook-R ‣ 4 AgentRunbook ‣ LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”)）。 AgentRunbook-R 效率很高，涵盖了主要的记忆能力，但其简单的设计并未针对详细的证据选择进行优化。受到 [Cao 等人。 (2026)](https://arxiv.org/html/2605.12493#bib.bib5)，我们提出了 AgentRunbook-C，一种基于编码智能体的内存方法，将内存管理视为文件管理问题。 AgentRunbook-C 将原始轨迹直接存储为文件。在查询时，它使用工作流文档、内存清单和帮助程序脚本增强现成的编码智能体工具，然后调用智能体来组装紧凑的证据集（§[4.2](https://arxiv.org/html/2605.12493#S4.SS2“4.2 AgentRunbook-C ‣ 4 AgentRunbook ‣ LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”)）。

我们评估了 LME-V2 中小型层的内存设计。首先，检索状态切片的简单 RAG 方法只能实现 40.1% 的总体准确率，而 AgentRunbook-R 进一步提高到 57.8%。在准确性方面，我们发现现成的 Codex 智能体（[OpenAI,](https://arxiv.org/html/2605.12493#bib.bib27)）具有竞争性的性能，达到了令人惊讶的 69.3% 的准确率。然而，该智能体以每次查询约 182 秒的成本实现这一目标，比 AgentRunbook-R 慢约 6.9 倍。通过我们的专业化设计，AgentRunbook-C 的整体性能最佳，准确率达到 72.5%，同时查询时间比 Codex 快 32%。我们的进一步分析表明，AgentRunbook-C 显着提高了准确性-延迟边界，但未来改进的空间仍然很大（§[5.2](https://arxiv.org/html/2605.12493#S5.SS2“5.2 准确性和延迟权衡 ‣ 5 个实验 ‣ LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”)）。总体而言，LME-V2 制定了智能体记忆评估的新标准，并为内存模块提供了具体的测试平台，使长期运行的智能体在现实环境中更加可靠、适应性强和有用。

## 2 相关工作

#### 长上下文和记忆评估

长期记忆评估可以被视为评估法学硕士和检索系统在跨扩展上下文中回忆信息的长期努力的一部分。早期的基准测试侧重于测试长输入文档的信息检索、聚合和指令跟踪（[Hsieh et al., 2024](https://arxiv.org/html/2605.12493#bib.bib13)；[Karpinska et al., 2024](https://arxiv.org/html/2605.12493#bib.bib18)；[Modarressi et al., 2025](https://arxiv.org/html/2605.12493#bib.bib26)； [Bai 等人，2025](https://arxiv.org/html/2605.12493#bib.bib2)；[Dou 等人，2026](https://arxiv.org/html/2605.12493#bib.bib7))。随后的工作将重点扩展到个性化记忆，涵盖显式用户事实和隐式偏好，基准包括 LoCoMo ([Maharana et al., 2024](https://arxiv.org/html/2605.12493#bib.bib25))、DialSim ([Kim et al., 2024](https://arxiv.org/html/2605.12493#bib.bib19))、PerLTQA ([Du et al., 2024](https://arxiv.org/html/2605.12493#bib.bib9))、LongMemEval ([Wu et al., 2025a](https://arxiv.org/html/2605.12493#bib.bib41))、PersonaMem ([Jiang et al., 2025a](https://arxiv.org/html/2605.12493#bib.bib15); [Jiang et al., 2025b](https://arxiv.org/html/2605.12493#bib.bib16)) 和 BEAM ([Tavakoli et al., 2025](https://arxiv.org/html/2605.12493#bib.bib35))。 LMEB（[Zhao et al., 2026a](https://arxiv.org/html/2605.12493#bib.bib50)）隔离检索组件并评估密集检索器的内存工作负载。相比之下，在一系列新的努力中，LME-V2 的目标是利用从网络智能体历史轨迹构建的上下文来体验记忆。这种转变引入了更加复杂的环境、新的能力分类法以及以智能体体验为中心的记忆设计。

#### 智能体的内存系统

随着 LLM 智能体在复杂环境中处理长期任务，记忆对于回忆早期详细轨迹上下文（[Hu et al., 2025](https://arxiv.org/html/2605.12493#bib.bib14)）和巩固跨轨迹的高级知识（[Wang et al., 2025b](https://arxiv.org/html/2605.12493#bib.bib40)；[Ouyang et al., 2025](https://arxiv.org/html/2605.12493#bib.bib31)；[吴等人，2025b](https://arxiv.org/html/2605.12493#bib.bib42))。记忆还通过延长探索和睡眠时间离线巩固来提高推理时间性能（[Ouyang et al., 2025](https://arxiv.org/html/2605.12493#bib.bib31); [Lin et al., 2025](https://arxiv.org/html/2605.12493#bib.bib22)）。尽管取得了这些进展，但对智能体设置中的记忆质量的直接评估仍然有限。 MemoryArena（[He et al., 2026](https://arxiv.org/html/2605.12493#bib.bib12)）通过相互依赖的任务序列的成功率间接测量内存。 AgentLongBench ([Fang et al., 2026](https://arxiv.org/html/2605.12493#bib.bib10)) 和 EMemBench ([Li et al., 2026](https://arxiv.org/html/2605.12493#bib.bib21)) 使用合成智能体历史记录并测试对这些痕迹中细节的回忆。 FileGram（[Liu et al., 2026a](https://arxiv.org/html/2605.12493#bib.bib23)）研究文件系统行为跟踪的推理。 AMA-Bench（[Zhao et al., 2026b](https://arxiv.org/html/2605.12493#bib.bib51)）最接近我们的设置，因为它从不同领域（例如实体、网络和游戏智能体）的智能体轨迹中提出问题。然而，AMA-Bench 侧重于理解一种轨迹，而 LME-V2 则侧重于从许多过去轨迹中归纳出的环境知识。据我们所知，LME-V2也是该设置中第一个将历史长度扩展到数十甚至超过1亿词元的基准。

#### 智能体作为内存控制器

最近关于智能体记忆的工作提出了内存系统，其中内存写入和读取操作由 LLM 而不是固定管道控制。 MemGPT ([Packer et al., 2023](https://arxiv.org/html/2605.12493#bib.bib32)) 和 StateLM ([Liu et al., 2026b](https://arxiv.org/html/2605.12493#bib.bib24)) 使模型能够以编程方式管理上下文。 A-MEM ([Xu et al., 2025](https://arxiv.org/html/2605.12493#bib.bib45)) 和 Mem0 ([Chhikara et al., 2025](https://arxiv.org/html/2605.12493#bib.bib6)) 引入了脚手架，允许法学硕士随着时间的推移演变记忆内容和结构。 Memory-R1 ([Yan et al., 2025](https://arxiv.org/html/2605.12493#bib.bib46)) 和 Mem-α\alpha ([Wang et al., 2025a](https://arxiv.org/html/2605.12493#bib.bib39)) 通过强化学习学习记忆更新动作。 MemSkill（[Zhang et al., 2026](https://arxiv.org/html/2605.12493#bib.bib48)）学习记忆技能，以更细粒度指导记忆更新行为。在这项工作中，我们进一步扩展了主体记忆的概念。受到 [Cao 等人。 (2026)](https://arxiv.org/html/2605.12493#bib.bib5) 和 [团队等人。 (2026)](https://arxiv.org/html/2605.12493#bib.bib36)，我们将具有工具使用和文件系统操作能力的通用编码智能体视为基于文件的内存的强大控制器。基于这个角度，我们设计了 AgentRunbook-C，它通过工作流文档、查询时渲染工件和帮助脚本增强了现成的编码智能体工具，从而在 LME-V2 上实现了强大的准确性与延迟权衡。

## 3 LongMemEval-V2

### 3.1 核心内存能力定义

经验丰富的同事在反复工作的环境中会内化什么？我们将学到的经验分为五种记忆能力：

*•

  静态回忆。经验丰富的同事会记住重要的地标、页面布局、模块可供性以及不同状态之间的细微差异。
*•

  动态状态跟踪。经验丰富的同事可以充当环境的世界模型：给定状态和操作，他们了解环境如何变化。
*•

  工作流程知识。经验丰富的同事知道在定制环境中执行常见任务所需的步骤。
*•

  环境陷阱。经验丰富的同事了解当前环境中常见的重复出现问题，并且可以避免特定于环境的故障。
*•

  前提意识。经验丰富的同事可以识别在另一种环境中有效但在当前环境中错误的假设。

### 3.2 注释

为了全面评估这些记忆能力，我们从多模式网络智能体轨迹中策划了 LongMemEval-V2。标注有四个步骤：轨迹收集、问题标注、答案轨迹标注、干草堆创建。我们在附录 [附录 A](https://arxiv.org/html/2605.12493#A1“附录 A LongMemEval-V2：进一步的基准构建详细信息 ‣ LongMemEval-V2：评估经验丰富的同事的长期智能体记忆”）中提供了完整的详细信息。

#### 轨迹收集

我们从三个网络智能体基准测试中收集轨迹：WebArena ([Zhou et al., 2024](https://arxiv.org/html/2605.12493#bib.bib52))、WorkArena ([Drouin et al., 2024](https://arxiv.org/html/2605.12493#bib.bib8)) 和 WorkArena++ ([Boisvert et al., 2024](https://arxiv.org/html/2605.12493#bib.bib3))，利用其 OneStopShop、CMS、Reddit、ServiceNow 环境。使用 AgentLab11 1 <https://github.com/ServiceNow/AgentLab> 收集轨迹。库，它提供统一的状态表示、动作空间和 ReAct 风格的基本智能体实现（[Yao et al., 2023](https://arxiv.org/html/2605.12493#bib.bib47)）。使用基础智能体和 Codex ([OpenAI,](https://arxiv.org/html/2605.12493#bib.bib27) )，我们使用 GPT-5.2 ([OpenAI, 2025](https://arxiv.org/html/2605.12493#bib.bib28)) 和 GPT-5-mini ([OpenAI, 2026](https://arxiv.org/html/2605.12493#bib.bib29)) 作为法学硕士。最终池包含来自 WebArena 的 599 个轨迹和来自 WorkArena/WorkArena++ 的 941 个轨迹。总体成功率为52.0%，每个轨迹平均包含28.1个状态。

图 2：LME-V2 问题涵盖不同的源域、问题类型和格式。

####问题注释

所有问题均通过手动注释构建。按照记忆能力分类，人类专家首先检查轨迹，以确定有经验的同事自然会学到的各种信息。然后，我们策划和过滤问题，以确保强大的专有法学硕士无法仅凭参数知识来回答22 2 我们手动测试了 Gemini-3-Pro ([Google DeepMind, 2025](https://arxiv.org/html/2605.12493#bib.bib11))、GPT-5.2 ([OpenAI, 2025](https://arxiv.org/html/2605.12493#bib.bib28))、Grok-4.1-thinking ([xAI, 2025](https://arxiv.org/html/2605.12493#bib.bib44)) 和 Claude-Opus-4.6 ([Anthropic, 2026](https://arxiv.org/html/2605.12493#bib.bib1)) 并确保四个模型中至少有两个错误地回答了问题。陷阱问题被框架为没有经验的工作人员发送带有屏幕截图的消息的场景，而其他问题表示为纯文本的真/假题、多项选择题或简答题。最后，根据现有的静态、动态和工作流程问题，我们策划了带有错误前提的弃权问题，模型必须识别这些问题才能成功。 [图 1](https://arxiv.org/html/2605.12493#S1.F1“1 简介 ‣ LongMemEval-V2：针对经验丰富的同事评估长期智能体记忆”）显示了每个类别中的示例问题。 [图2](https://arxiv.org/html/2605.12493#S3.F2“轨迹集合中‣3.2注释‣3LongMemEval-V2‣LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”）显示了最终问题池的源域、类型和格式分布。平均而言，问题需要 1.4 个轨迹才能回答（最少 1 个，最多 5 个）。然而，许多动态和工作流程问题需要从支持轨迹内的许多状态综合证据。

#### 答案轨迹标记

在注释过程中，注释者会为每个问题确定一组包含答案的轨迹种子集。为了构建共享历史干草​​堆，我们可以共同最小化所有问题的答案轨迹数量，我们执行额外的注释来标记包含每个问题答案的所有轨迹。我们使用 Codex 编码智能体来生成初始提案。然后，人类专家验证最终核心干草堆集中包含的轨迹的问题轨迹对应关系。我们在[附录 A](https://arxiv.org/html/2605.12493#A1“附录 A LongMemEval-V2：进一步的基准构建详细信息 ‣ LongMemEval-V2：针对经验丰富的同事评估长期智能体记忆”）中提供了详细信息。

图3：LME-V2中历史干草堆的基本统计。中小型层涵盖大量状态和词元（左）。与此同时，包含每个问题答案的轨迹在大海捞针中通常仍然稀疏（右）。

#### 干草堆创建

根据答案轨迹标签，我们以编程方式组装两层历史轨迹大海捞针：一个小型变体，包含所有问题共享的 100 个轨迹；一个中等变体，每个问题包含大约 500 个轨迹。在本文的其余部分中，我们将它们称为 LME-V2-Small 和 LME-V2-Medium。对于 LME-V2-Small，我们为 ServiceNow 问题创建了一个干草堆，并为 WebArena 域创建了一个干草堆。所有的大海捞针都包含成功和失败轨迹的均衡比例，许多问题只能从失败的轨迹中得到答案。 [图 3](https://arxiv.org/html/2605.12493#S3.F3“答案轨迹标记‣ 3.2 注释 ‣ 3 LongMemEval-V2 ‣ LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”) 提供了干草堆的进一步统计数据。 LME-V2-Small 和 LME-V2-Medium 的最终历史长度分别约为 25M 和 115M 个词元，而每个问题的答案轨迹集在大海捞针中仍然稀疏。

[表 1](https://arxiv.org/html/2605.12493#S1.T1“1 简介 ‣ LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”）将 LME-V2 与之前的长期记忆基准进行了比较。 LME-V2 的历史比之前的长期记忆基准要长得多，自然包括多模式评估，并提供了关键智能体记忆功能的广泛覆盖。

### 3.3 评估公式

我们将 LME-V2 制定为上下文收集任务。对于每个带有黄金答案yiy\_{i},的问题qiq\_{i}，内存系统都会收到一个有序的轨迹干草堆ℋi={hi,1,…,hi,mi}\mathcal{H}\_{i}=\{h\_{i,1},\ldots,h\_{i,m\_{i}}\},，其中每个hi,jh\_{i,j}都是一个轨迹。系统必须支持两个API，Insert​(h)\texttt{Insert}(h)和Query​(q)\texttt{Query}(q).我们将所有轨迹依次插入到ℋi\mathcal{H}\_{i},中，通过qiq\_{i},查询最终内存，得到返回的上下文cic\_{i}:

|  |  |  |  |
| ---| ---| ---| ---|
|  | ℳi,j\displaystyle\mathcal{M}\_{i,j} | =Insertℳi,j−1​(hi,j),\displaystyle=\texttt{Insert}\_{\mathcal{M}\_{i,j-1}}(h\_{i,j}), |  |
|  |  |  |  |
| ---| ---| ---| ---|
|  | ci\displaystyle c\_{i} | =Queryℳi,mi​(qi).\displaystyle=\texttt{Query}\_{\mathcal{M}\_{i,m\_{i}}}(q\_{i}). |  |

固定阅读器模型 RR 从问题和有限内存上下文中给出答案：y^i=R⁡(qi,Trunc⁡(ci))\hat{y}\_{i}=R(q\_{i},\mathrm{Trunc}(c\_{i}))33 3 我们根据经验将截断预算设置为 200k 词元。我们报告答案准确性和查询延迟。准确性是通过结构化答案的规范化字符串匹配和自由格式答案的法学硕士判断来计算的。

### 3.4 试点研究

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|背景 |总体 |静态|动态 |工作流程|陷阱 |
| Qwen3.5-9B（思考启用）| | | | | |
|没有上下文 | 0.016 | 0.000 | 0.000 0.015 | 0.015 0.155 | 0.155 0.136 | 0.136
|甲骨文轨迹 | 0.596 | 0.596 0.566 | 0.566 0.668 | 0.668 0.718 | 0.718 0.310 |
| Oracle 切片+笔记 | 0.825 | 0.825 0.908 | 0.908 0.879 | 0.879 0.750 | 0.750 0.484 | 0.484
| GPT-5.4-mini（中等推理）| | | | | |
|没有上下文 | 0.045 | 0.045 0.025 | 0.025 0.010 | 0.010 0.075 | 0.075 0.171 | 0.171
|甲骨文轨迹 | 0.653 | 0.653 0.660 | 0.660 0.696 | 0.696 0.697 | 0.697 0.484 | 0.484
| Oracle 切片+笔记 | 0.863 | 0.863 0.950 | 0.950 0.843 | 0.843 0.905 | 0.905 0.467 | 0.467
| Codex + GPT-5.4-mini（xhigh 推理）| | | | | |
| Oracle 轨迹文件 | 0.897 | 0.897 0.986 | 0.986 0.947 | 0.947 0.815 | 0.815 0.517 | 0.517

图4： 
LME-V2 非弃权问题的试点研究。 (a) 前沿法学硕士在没有轨迹历史的情况下表现不佳，这表明仅参数知识对于 LME-V2 来说是不够的。 (b) 即使使用预言机答案承载轨迹和优化（例如带注释的证据切片或使用编码智能体工具来帮助提高性能），LME-V2 也很难回答。

我们进行了两项试点研究。首先，我们评估 LME-V2 问题是否需要特定环境的轨迹证据。然后，我们合理地检查承载答案的轨迹是否足以可靠地回答问题。这些研究使用直接问答设置，而不是主要实验中使用的上下文收集公式，并且仅评估非弃权问题。附录 [附录 B](https://arxiv.org/html/2605.12493#A2“附录 B LongMemEval-V2：试点研究 ‣ LongMemEval-V2：针对经验丰富的同事评估长期智能体记忆”）中提供了完整的按类别结果、提示和沙箱说明。

首先，最近的前沿法学硕士能否在没有轨迹历史的情况下回答 LME-V2 问题？我们只用问题来提示优秀的法学硕士。如图4](https://arxiv.org/html/2605.12493#S3.F4“在3.4试点研究中‣3 LongMemEval-V2‣LongMemEval-V2：评估经验丰富的同事的长期智能体记忆”）（左），所有LLM在此设置中表现不佳：最好的模型仅达到14.1％的总体准确率，这表明LME-V2问题通常无法从仅公共或参数知识。

其次，我们让模型预言机能够访问包含答案的轨迹，以隔离阅读和接地轨迹证据的困难。长上下文提示显示出更高的准确性，但由于轨迹大小超出了模型的上下文窗口，因此仍然受到限制。我们进一步考虑两种技术：1）注释包含证据的真实状态并仅提供围绕它们的半径为 1 的证据切片；2）总结包含轨迹中识别的重要过程和陷阱的策略注释。这两种技术将直接 QA 分别进一步提高到 82.5% 和 86.3%。最后，我们将轨迹表示为文件，并使用现成的 Codex 编码智能体直接回答问题。令人惊讶的是，使用 Codex 工具的GPT-5.4-mini比提示方法更好地回答了问题，这表明通过多步骤工具使用进行详细的证据检查对于理解智能体轨迹是有效的，并且编码智能体作为内存控制器可能具有良好的性能。总的来说，这些发现证实了答案轨迹标记足够准确，并激发了我们的记忆方法设计。

## 4 智能体运行手册

LME-V2 具有挑战性，因为问题所需的证据可能会混合低级 UI 观察、状态转换和可重用任务过程。因此，内存模块需要将嘈杂的智能体轨迹组织成紧凑的表示形式，并对它们进行索引以进行有针对性的召回。我们提出了两种内存设计：AgentRunbook-R，一种具有独立知识池的结构化 RAG 管道，以及 AgentRunbook-C，一种基于编码智能体的方法，将记忆智能体上下文视为文件管理问题。 [图 5](https://arxiv.org/html/2605.12493#S4.F5“在 4 AgentRunbook ‣ LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”）说明了两种方法的工作流程。

![参考说明](https://arxiv.org/html/2605.12493v1/agentrunbook_method_v1.png)

图 5：AgentRunbook 内存模块的图示。 (a) AgentRunbook-R 在插入时消化轨迹并为原始状态、事件和注释创建专用知识池。在查询时，LLM 控制器为每个池生成多流查询。 (b) AgentRunbook-C 在插入时将轨迹存储为文件，并使用专门的指令和清单构建沙箱工作区，以便编码智能体有效地收集所需的证据。

### 4.1 AgentRunbook-R

AgentRunbook-R（其中 R 表示 RAG）在插入时提取结构化内存项并在查询时检索它们。为了回忆不同粒度的信息，AgentRunbook-R 使用单独的知识池和这些池上的检索机制。给定轨迹 hh，AgentRunbook-R 构建三个内存池。原始状态切片池存储以轨迹状态为中心的窗口，包括本地 UI 观察和附近的操作。该池保留了细粒度的视觉和文本证据。状态转换事件池存储从连续状态中提取的事件。这些事件描述了行为如何改变环境，为环境世界模型积累证据。过程和提示注释池存储轨迹级注释，捕获可重用的工作流程、导航模式和特定于环境的陷阱。该池的灵感来自于先前将轨迹经验整合为紧凑的可重用知识的工作（[Wang et al., 2025b](https://arxiv.org/html/2605.12493#bib.bib40); [Ouyang et al., 2025](https://arxiv.org/html/2605.12493#bib.bib31)）。

在查询时，AgentRunbook-R 使用 LLM 控制器对查询和当前内存快照进行推理，然后生成知识池的检索查询：针对精确 UI 证据的多个原始状态查询、针对重要状态更改的事件查询以及针对程序知识的注释查询。控制器可以跳过不相关的流。每个查询都使用密集检索从其相应的池中检索，并将结果呈现为多模式内存上下文cic\_{i}.这种设计可以保持较低的查询延迟，同时支持不同粒度的证据。

### 4.2 AgentRunbook-C

AgentRunbook-C（其中 C 表示编码智能体）的动机是观察到通用编码智能体是有效的文件系统操纵者和工具用户（[Cao et al., 2026](https://arxiv.org/html/2605.12493#bib.bib5)）。 AgentRunbook-C 不是将检索行为压缩到固定的矢量搜索管道中，而是将轨迹直接存储为文件，并使用编码智能体在查询时搜索、检查和选择证据。

然而，现成的编码智能体并未作为存储器模块进行优化。它可能会过度探索、探索不足或检查数据效率低下。 AgentRunbook-C 向编码智能体添加了三个轻量级脚手架组件。首先，工作流程文档指示智能体充当内存模块，并概述收集证据的步骤。其次，查询时清单工件总结了当前的内存布局，帮助智能体在详细检查之前列出相关轨迹。第三，帮助程序脚本公开常见的轨迹检查操作，例如查看状态范围或在轨迹内搜索。在插入时，AgentRunbook-C 将每个轨迹存储在磁盘上。在查询时，它会创建一个沙箱，其中包含问题、工作流文档、帮助程序脚本和渲染的清单工件。然后，编码智能体写入一个结构化检索输出，其中包含短记忆注释和选定的轨迹状态范围，这些输出被渲染为cic\_{i}.

## 5 个实验

我们在上下文收集公式下评估了 LME-V2 上的所有方法。返回的内存上下文被截断为 200K 个词元，并由固定的 Qwen3.5-9B 阅读器进行应答（[Qwen Team, 2026](https://arxiv.org/html/2605.12493#bib.bib33)）。对于 RAG 方法，我们使用 Qwen3.5-9B 作为内存控制器，并使用 Qwen3-Embedding-8B 进行检索。对于编码智能体方法，我们使用 Codex 和 GPT-5.4-mini 进行不同的推理工作。 AgentRunbook 和基线的完整实现细节在 [附录 C](https://arxiv.org/html/2605.12493#A3“附录 C 实现细节 ‣ LongMemEval-V2：针对经验丰富的同事评估长期智能体记忆”）中提供。

### 5.1 主要结果

表 2：带有基线和消融的主要结果。下游读取器始终为Qwen3.5-9B。我们将每个方法系列中的最佳结果加粗。 ✣ 表示通过配对引导测试统计显着优于非消融基线 (p<0.05p<0.05)。 AgentRunbook 的性能远远优于 RAG 系列的基准，并在编码智能体系列中实现了出色的延迟。

|  |  |  |  |  |  |  |  |  |  |  |  |  |
| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---|
|方法| LME-V2-小| | | | | | LME-V2-中| | | | | |
|总体 |静态|动态 |工作流程|陷阱 |延迟|总体 |静态|动态 |工作流程|陷阱 |延迟|
|暂无检索 | 0.013 | 0.013 0.000 | 0.000 0.008 | 0.008 0.094 | 0.094 0.138 | 0.138 0 秒 | 0.013 | 0.013 0.000 | 0.000 0.008 | 0.008 0.094 | 0.094 0.138 | 0.138 0 秒 |
| RAG 方法（控制器 = Qwen3.5 9B，启用思考）| | | | | | | | | | | | |
| RAG: query →\rightarrow slice | 0.428 | 0.471 | 0.425 | 0.415 | 0.207 | 0.1s | 0.381 | 0.434 | 0.405 | 0.293 | 0.242 | 0.1s |
| RAG: query →\rightarrow slice + notes | 0.510 | 0.524 | 0.496 | 0.528 | 0.414 | 0.2s | 0.459 | 0.487 | 0.472 | 0.434 | 0.310 | 0.3s |
| AgentRunbook-R | 0.586✣| 0.661✣| 0.583✣| 0.528 | 0.528 0.310 | 26.9 秒 | 0.570✣| 0.630✣| 0.614✣| 0.472✣| 0.345 | 0.345 25.8 秒 |
| – 原始切片池 | 0.423 | 0.423 0.286 | 0.286 0.551 | 0.551 0.538 | 0.538 0.345 | 0.345 16.7 秒 | 0.335 | 0.335 0.233 | 0.233 0.433 | 0.433 0.377 | 0.377 0.413 | 0.413 17.1秒|
| – 事件池 | 0.556 | 0.556 0.614 | 0.614 0.559 | 0.559 0.528 | 0.528 0.276 | 0.276 19.1秒| 0.484 | 0.484 0.534 | 0.534 0.496 | 0.496 0.434 | 0.434 0.276 | 0.276 18.5 秒 |
| – 笔记池 | 0.579 | 0.579 0.651 | 0.651 0.614 | 0.614 0.481 | 0.481 0.310 | 22.8 秒 | 0.499 | 0.499 0.561 | 0.561 0.543 | 0.543 0.396 | 0.396 0.276 | 0.276 20.5 秒 |
|编码智能体方法（控制器 = GPT-5.4-mini，xhigh 推理）| | | | | | | | | | | | |
|法典| 0.699 | 0.699 0.804 | 0.804 0.670 | 0.670 0.575 | 0.575 0.586 | 0.586 177.2秒| 0.687 | 0.687 0.783 | 0.783 0.646 | 0.646 0.613 | 0.613 0.517 | 0.517 185.8秒|
| AgentRunbook-C | 0.749✣| 0.820✣| 0.724✣| 0.726✣| 0.483 | 0.483 108.3秒| 0.701 | 0.701 0.788 | 0.701✣| 0.613 | 0.613 0.449 | 0.449 139.9秒|
| – 工作流程| 0.701 | 0.701 0.772 | 0.772 0.677 | 0.677 0.632 | 0.632 0.586 | 0.586 167.9 秒 | 0.641 | 0.641 0.709 | 0.709 0.646 | 0.646 0.575 | 0.575 0.414 | 0.414 231.9秒|
| – 明显的工件| 0.747 | 0.747 0.847 | 0.847 0.709 | 0.709 0.698 | 0.698 0.448 | 0.448 155.0 秒 | 0.681 | 0.681 0.767 | 0.767 0.685 | 0.685 0.576 | 0.576 0.483 | 0.483 211.6秒|
| – 辅助函数 | 0.714 | 0.714 0.783 | 0.783 0.724 | 0.724 0.660 | 0.660 0.414 | 0.414 145.9秒| 0.718 | 0.718 0.804 | 0.804 0.693 | 0.693 0.689 | 0.689 0.380 | 0.380 182.5秒|

如[表2](https://arxiv.org/html/2605.12493#S5.T2“在5.1主要结果‣5个实验‣LongMemEval-V2：评估经验丰富的同事的长期智能体记忆”）中，无检索基线接近于零，证实读者在没有记忆上下文的情况下无法回答。简单的查询到切片 RAG 基线在 LME-V2-Small 上达到 42.8%，在 LME-V2-Medium 上达到 38.1%，而添加轨迹注释将性能提高到 51.0% 和 45.9%。 AgentRunbook-R further improves over the strongest RAG baseline, reaching 58.6% on LME-V2-Small and 57.0% on LME-V2-Medium.消融表明原始切片池对于静态问题很重要，而删除事件池会损害静态、动态和陷阱问题。工作流问题受益于将轨迹经验整合到可重复使用的事件和注释中，而不是仅仅检索本地观察结果。

AgentRunbook-C 实现了最佳的整体准确率，在 LME-V2-Small 上达到 74.9%，在 LME-V2-Medium 上达到 70.1%。 It also improves over vanilla Codex, which reaches 69.9% and 68.7%, respectively. The ablations show that workflow instructions are consistently important, while manifest artifacts mainly improve efficiency.辅助函数以混合方式影响性能：与最昂贵的消融相比，它们改善了小层结果并减少了延迟，但它们对中层精度的影响并不总是积极的。 Overall, the results show that coding 智能体 can serve as strong memory controllers with a proper file-based environment.在[附录D](https://arxiv.org/html/2605.12493#A4“附录D进一步分析‣LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”）中，我们进一步分析了AgentRunbook-C的错误模式和工具调用行为。

### 5.2 准确性和延迟权衡

Figure 6: AgentRunbook improves the query accuracy-latency frontier of memory modules.

An ideal memory method should support both accurate and efficient querying. Across multiple factors, we find the reasoning effort of the memory controller has a large and direct effects on the overall query latency. We thus use it to analyze the methods across different operating points.如图 6（https://arxiv.org/html/2605.12493#S5.F6“在 5.2 准确性和延迟权衡 ‣ 5 个实验 ‣ LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”）所示，AgentRunbook-R 提供了中等精度、低延迟的基线：它比切片加音符基线有了显着改进，同时将延迟保持在 26 秒左右，或者不假思索地低得多。 This makes it a strong choice when query efficiency is prioritized. AgentRunbook-C moves the accuracy and latency frontier upward.在推理工作设置中，支架式编码智能体记忆始终比直接使用现成的编码智能体提供更好的权衡。这表明，当与明确的工作流程指导、清单和轨迹检查工具配合使用时，编码智能体作为内存控制器会更有效。

## 6 结论

我们推出了 LongMemEval-V2，这是一个长期记忆基准测试，它为智能体记忆评估制定了新标准：内存系统应该帮助智能体成为专业环境中经验丰富的操作员。 LME-V2 全面涵盖了五种内存能力，并通过来自大型多模式网络智能体历史的超过 100M 词元上下文提高了内存基准的上下文深度。我们进一步提出了 AgentRunbook-R，它通过专用内存池改进了基于 RAG 的标准方法，以及 AgentRunbook-C，它利用编码智能体的文件操作能力，并通过轻量级工作流指导、清单和检查工具进一步提高准确性和延迟。我们希望 LME-V2 为内存模块提供一个具体的测试平台，使长期运行的智能体在现实环境中更加智能和可靠。

## 附录 A LongMemEval-V2：进一步的基准构建细节

### A.1 轨迹采集

#### 领域和任务选择。

我们从 WebArena、WorkArena 和 WorkArena++ 收集轨迹。对于 WebArena，我们使用 OneStopShop、CMS 和 Reddit 任务，因为我们的试点检查发现这些网站比 Wikipedia、Map 和 GitLab 包含更多特定于环境的自定义内容。 WorkArena 和 WorkArena++ 均基于 ServiceNow，因此我们包含两个基准测试中的所有任务。

#### AgentLab 工具和操作空间。

我们使用 AgentLab 在统一的 Web 智能体界面下收集轨迹。 AgentLab 提供基准包装器、观察预处理、高级浏览器操作和轨迹记录。该智能体观察可访问性树表示和屏幕截图，并通过高级 BrowserGym 操作 API 与浏览器交互。元素由可访问性树中的出价标识符引用，并且智能体在每一步都会发出一个类似 Python 的操作调用。

对于 WorkArena 和 WorkArena++，我们使用以下操作空间：

|  |  |  |
| ---| ---| ---|
|  | noop(wait\_ms=1000),scroll(delta\_x, delta\_y),fill(bid, value, enable\_autocomplete\_menu=False),select\_option(bid, options),click(bid, button=’left’, modifiers=[]),dblclick(bid, button=’left’, modifiers=[]),hover(bid),press(bid, key\_comb),focus(bid),clear(bid),drag\_and\_drop(from\_bid, to\_bid),tab\_focus(index),new\_tab(),tab\_close(),go\_back(),go\_forward(),goto(url),send\_msg\_to\_user(text),report\_infeasible(reason).\begin{gathered}\texttt{noop(wait\\_ms=1000)},\quad\texttt{scroll(delta\\_x, delta\\_y)},\quad\\ \texttt{fill(bid, value, enable\\_autocomplete\\_menu=False)},\\ \texttt{select\\_option(bid, options)},\quad\texttt{click(bid, button='left', modifiers=[])},\quad\\ \texttt{dblclick(bid, button='left', modifiers=[])},\\ \texttt{hover(bid)},\quad\texttt{press(bid, key\\_comb)},\quad\texttt{focus(bid)},\quad\texttt{clear(bid)},\\ \texttt{drag\\_and\\_drop(from\\_bid, to\\_bid)},\quad\texttt{tab\\_focus(index)},\quad\texttt{new\\_tab()},\quad\texttt{tab\\_close()},\\ \texttt{go\\_back()},\quad\texttt{go\\_forward()},\quad\texttt{goto(url)},\quad\\ \texttt{send\\_msg\\_to\\_user(text)},\quad\texttt{report\\_infeasible(reason)}.\end{gathered} |  |

对于 WebArena，我们使用：

|  |  |  |
| ---| ---| ---|
|  | noop(wait\_ms=1000),scroll(delta\_x, delta\_y),keyboard\_press(key),click(bid, button=’left’, modifiers=[]),fill(bid, value, enable\_autocomplete\_menu=False),hover(bid),tab\_focus(index),new\_tab(),go\_back(),go\_forward(),goto(url),tab\_close(),select\_option(bid, options),send\_msg\_to\_user(text),report\_infeasible(reason).\begin{gathered}\texttt{noop(wait\\_ms=1000)},\quad\texttt{scroll(delta\\_x, delta\\_y)},\quad\texttt{keyboard\\_press(key)},\\ \texttt{click(bid, button='left', modifiers=[])},\quad\\ \texttt{fill(bid, value, enable\\_autocomplete\\_menu=False)},\quad\texttt{hover(bid)},\\ \texttt{tab\\_focus(index)},\quad\texttt{new\\_tab()},\quad\texttt{go\\_back()},\quad\texttt{go\\_forward()},\quad\texttt{goto(url)},\\ \texttt{tab\\_close()},\quad\texttt{select\\_option(bid, options)},\quad\\ \texttt{send\\_msg\\_to\\_user(text)},\quad\texttt{report\\_infeasible(reason)}.\end{gathered} |  |

主要区别在于 WebArena 包括 keyboard\_press(key),，而 WorkArena 和 WorkArena++ 包括其他特定于元素的操作，例如 dblclick、按、焦点、清除和 drag\_and\_drop.

#### 轨迹收集智能体。

大多数轨迹是使用 AgentLab 的通用 ReAct 风格智能体收集的，使用 GPT-5-mini 和 GPT-5.2 作为底层 LLM。此外，我们使用由 Codex 控制的手动操作智能体，具有GPT-5.2，推理工作量很高。手动动作智能体不会改变环境界面或动作空间。它显示当前的观察结果，接受操作员建议的高级操作字符串，根据相同的 BrowserGym 操作 API 对其进行验证，并以标准 AgentLab 轨迹格式记录结果转换。我们主要将这种由 Codex 控制的手动操作设置用于 3 级 WorkArena++ 任务，其中需要额外的目标收集才能获得跨任务类别的成功轨迹。

#### 拒绝采样和轨迹过滤。

我们在拒绝采样期间的主要目标是获得每项任务的成功轨迹，同时保留有用的失败轨迹。我们最初的目标是在可能的情况下为每个任务实例收集一个成功的轨迹和一个失败的轨迹。在实践中，许多任务最终只有一个成功或一个失败的轨迹，因为额外的采样成本很高。最终轨迹池包含 599 个 WebArena 轨迹和 941 个 WorkArena/WorkArena++ 轨迹。轨迹平均包含 28.1 个状态。总体而言，73.1％的轨迹来自GPT-5-mini，22.9％来自GPT-5.2，4.0％来自Codex的GPT-5.2（xhigh推理）。

我们还考虑了通过官方 WebArena 排行榜发布的轨迹，但没有将其作为主要数据源。一些公共轨迹缺乏屏幕截图，这对于我们的多模式干草堆设计至关重要。此外，许多排行榜轨迹是由专门用于WebArena的智能体生成的，并且通常非常短，这使得它们不太适合研究一般智能体积累的环境经验。相比之下，GPT-5-mini和GPT-5.2生成的轨迹使用强大的通用模型，并在所有选定的任务类别中提供成功的示例。我们很少使用 Codex，因为它更昂贵，而且编码智能体设置可能会无意中从网络搜索等中引入额外的外部知识。

#### 最终轨迹工件和目标清理。

对于每个保留的轨迹，最终的工件由任务目标和状态-动作对的有序序列组成。每个状态都包含屏幕截图和可访问性树，每个操作都是该步骤发出的高级 BrowserGym 操作。对于 WorkArena 和 WorkArena++ Level-2 和 Level-3 任务，原始目标描述有时包含详细的导航提示，这可以通过直接从目标读取路线而不是从轨迹中学习来使过程问题变得可回答。因此，我们清理目标描述，同时保留任务意图和特定于任务的有效负载。我们还清理了轨迹状态中重复出现的原始目标，例如初始任务描述和后来复制的任务文本。 [表 3](https://arxiv.org/html/2605.12493#A1.T3“在最终轨迹工件和目标清理中。‣ A.1 轨迹集合 ‣ 附录 A LongMemEval-V2：进一步的基准构建详细信息 ‣ LongMemEval-V2：针对经验丰富的同事评估长期智能体记忆”）显示了代表性示例。

表 3：WorkArena 和 WorkArena++ 2/3 级轨迹的目标清理示例。重写的目标保留了任务意图和特定于任务的值，同时删除了显式导航路线和分步模块提示。

|  |  |  |
| --- | --- | --- |
|任务族|原始进球摘录 |净化后的目标摘录|
|重复问题清理|清理重复的问题。具体来说，导航到“问题”应用程序的“分配给我”模块。创建一个过滤器，其中“问题陈述”包含#SERIES-5ea261ef-8。将问题与重复的问题陈述标记为同样的问题。 |清理重复的问题。查看您自己分配的问题，其中“问题陈述”包含#SERIES-5ea261ef-8。将问题与重复的问题陈述标记为同样的问题。 |
|仪表板驱动的目录补货 |从标题为 #CAT012007808 的图表中检索信息。导航到报告 > 查看/运行，搜索报告，然后导航到自助服务 > 服务目录并为最少可用的项目下订单。 |从标题为 #CAT012007808 的图表中检索信息。在图表中找到最大的库存价值和最少的可用商品。对于最少可用的商品，请订购额外的商品，使其数量与您找到的价值相匹配。 |
|请求的商品重新订购 |订购与 Kathryn-Lisa Ibarra-Stewart 相同的商品。导航至“自助服务”的“请求项目”模块，按“请求”进行筛选，然后导航至“服务目录”模块并订购具有指定数量和配置的项目。 |订购与 Kathryn-Lisa Ibarra-Stewart 相同的商品。找到之前为凯瑟琳-丽莎·伊瓦拉-斯图尔特请求的物品。订购具有指定数量和配置的项目。 |
|硬件资产查找|查找 Julia-Dylan Ray-Mclean 笔记本电脑的保修到期日期。导航到产品组合 > 硬件资产，筛选“分配给”为 Julia-Dylan Ray-Mclean 的位置，然后提取“保修到期”字段。 |查找 Julia-Dylan Ray-Mclean 笔记本电脑的保修到期日期并报告。 |

### A.2 问题注释

注释团队由一名研究生和三名本科生组成。在编写问题之前，注释者通过与沙箱网站交互并检查收集的轨迹来熟悉目标环境。项目负责人解释我们在正文中定义的记忆能力定义，注释者在整个过程中与项目负责人讨论不明确的情况。

注释者首先检查轨迹，以识别经验丰富的同事应该知道的特定于环境的事实、状态变化、工作流程和陷阱。然后，他们写出问题，其答案需要这种经验，而不是公共基础平台的一般知识。每个问题都由至少一名附加注释员验证，该注释员检查问题是否可以根据预期轨迹证据进行回答、答案是否正确以及问题类型是否与预期记忆能力相匹配。当不确定性仍然存在时，注释者会通过与项目负责人的讨论来解决它。

我们使用 LMArena 网页44 4 <https://arena.ai/> 来测试强大的法学硕士是否可以仅通过参数知识回答候选人的问题。根据经验，我们发现模型通常会正确回答许多候选人的问题，因为它们知道 Magento、Postmill 和 ServiceNow 的公共版本。因此，我们过滤了许多问题并重写或扰乱其他问题，直到模型失败。在某些情况下，我们首先编写一个自由形式的问题，观察模型的错误答案，然后使用这些错误答案作为干扰因素来构建更具挑战性的多项选择题。在最终的上下文收集评估中，还会提示读者根据返回的记忆上下文进行回答并避免猜测，这进一步减少了准确性来自参数化知识而不是检索到的经验的机会。

对于所有问题，注释者都会验证相关答案证据是否在屏幕截图中可见。尽管可访问性树有时比屏幕截图更清楚地暴露信息，特别是对于隐藏标签或结构化字段，但我们避免了只能从可访问性树而不是视觉轨迹证据中推断出答案的问题。

### A.3 答案轨迹标记

在问题注释过程中，注释者会记录一组种子轨迹，其中包含每个问题的答案。然而，最终的干草堆是跨问题共享的，因此我们执行额外的答案轨迹标记过程，以识别包含每个问题的足够证据的所有轨迹。此步骤的输出是从每个问题 ID 到包含答案的轨迹 ID 集的覆盖图。对于需要多个独立证据的问题，例如跨形式比较或涉及症状和解决方案的问题，覆盖图还记录了所需的证据跳跃。干草堆构建器稍后强制为每个所需的跳跃选择至少一个轨迹。

我们使用 Codex 来协助此标签流程。每个工作人员都会被分配一小批问题以及相关的轨迹池、元数据和工作流程规则。我们发现批处理对于准确性很重要：它让智能体专注于连贯的问题系列，例如静态形式比较、动态转换、工作流程或陷阱问题，同时保持搜索空间足够小以进行仔细检查。该工作流程强调召回率和精确度。智能体首先使用元数据、任务族、URL 模式和轨迹摘要缩小候选轨迹，然后直接检查候选轨迹。纳入需要屏幕截图可见的证据；可访问性树和字符串匹配可用于分类，但不足以包含。失败轨迹与成功轨迹同等对待，因为许多问题只能通过失败或部分完成的运行来回答。当证据不明确时，智能体会将轨迹记录为不确定并给出理由，而不是强制做出纳入决定。

该工作流程还强制执行特定于问题类型的规则。静态问题需要相关页面、字段、值或表单的直接视觉证据。动态问题需要相关状态更改之前/之后的证据，而不仅仅是相关任务系列的证据。程序问题需要轨迹来显示关键的程序步骤，而不仅仅是类似的实体或目标。默认情况下，陷阱问题被标记为高风险，因为所需的证据通常很微妙且依赖于上下文。对于多跳问题，每个跳必须有自己的候选轨迹集，并且只有当引用的屏幕截图直接支持每个跳时，单个轨迹才能满足多个跳。

在 Codex 辅助的传递之后，人类手动解决由智能体标记的不明确的情况，并手动验证最终核心大海捞针集中包含的轨迹的问题轨迹对应关系。验证器检查每个选定的轨迹是否包含预期的证据，证据在屏幕截图中是否可见，以及多跳约束是否得到满足。最终的人工验证用于确保大海捞针构建中使用的最小答案核心保留答案覆盖范围，同时避免虚假的答案承载轨迹。

### A.4 Haystack Creation

我们分三个阶段构建干草堆：答案核心选择、小干草堆扩展和中干草堆扩展。构建器的输入是上一步的最终覆盖图，其中列出了每个问题的所有答案轨迹。有些问题需要多个证据跳跃，因此覆盖图可以指定多个所需的跳跃，每个跳跃都有自己的候选轨迹集。没有直接答案轨迹的弃权问题通过手动验证的锚映射到相应的源问题来单独处理。

#### Minimal answer core.

我们首先为每个领域构建一个最小的答案核心。目标是选择一小部分共享轨迹，以便每个非零支持问题对于每个所需的跳跃都至少有一个选定的答案承载轨迹。我们将其表述为分配问题：对于每个问题跳跃要求，程序从其候选答案集合中选择一个轨迹。该目标有利于覆盖更多问题和更多要求的轨迹，同时也鼓励稀疏覆盖，避免不必要的过度覆盖，控制成功/失败比率，并最大限度地减少唯一选定轨迹的数量。我们通过确定性贪婪初始化和多次重新启动的本地搜索来解决分配问题。生成的核心包含 WebArena 的 44 个轨迹和 ServiceNow 的 49 个轨迹。然后，我们手动验证最小核心，以确保所选轨迹包含问题的预期证据并代表多跳要求。

#### 小干草堆。

从经过验证的最小核心开始，我们将每个域扩展为共享的 100 条轨迹干草堆。 WebArena 问题共享一个 100 轨迹干草堆，ServiceNow 问题共享另一个。填充物是从最小核心之外的轨迹中选择的。填充排名鼓励任务系列的多样性，更喜欢全局答案支持计数较低的轨迹，对较难的轨迹应用弱偏好，并将成功/失败平衡控制为 1:1 的比例。构建后，轨迹顺序被确定性地重新排列。

#### 中等干草堆。

中间层是根据问题构建的，而不是作为单个共享的干草堆。重要的是，它重用了小草堆构建器选择的相同的每个问题答案种子，因此答案承载核心在层之间不会改变。对于每个问题，构建器从为其所需跳跃选择的答案轨迹开始，然后添加填充物，直到达到目标大小，使用报告的中等层的 500 个轨迹。在排除该问题的完整答案集后对填充物进行采样，以确保扩展不会引入超出所选种子的额外答案轨迹。填充排名促进了任务族的多样性、填充目标和答案核心目标之间的低重叠、低全局答案支持计数以及结果平衡。对于零支持弃权问题，构建者准确地重复使用了手动验证的锚定问题的干草堆。

### A.5 评估

我们使用上下文收集协议评估每个记忆系统。对于每个问题，评估工具首先将问题大海捞针中的所有轨迹插入内存模块，用问题查询最终内存，验证返回的上下文仅包含文本和图像项，并将上下文截断为 200K Qwen3.5-9B 标记。然后，固定阅读器接收特定于领域的系统提示、返回的记忆上下文、问题文本和问题图像（如果存在）。通过提取最后一个\boxed{}表达式来解析阅读器输出；如果未找到盒装答案，则将完整响应用作预测。就准确性而言，“未知”的预测始终被视为不正确。

结构化答案由每个问题指定的确定性评估器进行评分，包括标准化短语匹配、有序短语匹配、单选匹配和多选选择匹配。陷阱和弃权问题由法学硕士法官进行评估，因为它们需要与参考见解或有缺陷的前提解释进行语义比较。评委输出一个二进制 JSON 标签，作为最终得分。我们汇总整套数据的准确性，并报告类别级别的细分。

#### 实验细节

对于固定读取器模型，我们在具有 Nvidia A100 GPU 的本地计算机上使用 vllm [[Kwon et al., 2023](https://arxiv.org/html/2605.12493#bib.bib20)] 托管的 Qwen3.5-9B 模型。我们使用温度0.6、top\_p0.95、top\_k20进行抽样评估。我们执行手动提示调整以确保提示模板可靠，以便（1）在没有内存上下文的情况下，模型的性能接近于零；（2）在使用oracle图像+文本状态切片的情况下，模型的性能尽可能高。为了评估弃权和陷阱问题的正确性，我们使用具有中等推理能力的GPT-5.2模型作为LLM法官。

表 4：主要上下文收集评估中使用的读者提示。所有内存系统都使用相同的模板。

|  |  |
| ---| ---|
|组件|模板|
| System prompt, WebArena | You are an experienced colleague in a web browsing environment that has a customized Magento-based shopping website, a customized Magento-based shopping admin CMS website, as well as a customized forum website based on Reddit/Postmill. Answer based on your memory of the environment. If you do not know the answer, output exactly \boxed{UNKNOWN}. Do not guess. Never attempt to guess an answer if you are not sure. If you believe the question’s construction/premise is wrong, provide an explanation in \boxed{} explaining why the question is flawed. |
| System prompt, WorkArena | You are an experienced colleague working in a customized ServiceNow environment. Answer based on your memory of the environment. If you do not know the answer, output exactly \boxed{UNKNOWN}. Do not guess. Never attempt to guess an answer if you are not sure. If you believe the question’s construction/premise is wrong, provide an explanation in \boxed{} explaining why the question is flawed. |
|用户提示 | ### 内存上下文：{内存模块返回的内存上下文，截断后} ### 要回答的问题：{问题文本} 如果问题包含图像，则图像将附加在问题文本之后。 |

表 5：法学硕士法官提示对弃权和陷阱问题进行语义评估。两个法官都返回带有二进制标签的 JSON。

|  |  |
| ---| ---|
|法官|提示|
| Abstention judge | System: You are a strict grader for flawed-premise (abstention) questions. Judge whether a model answer correctly identifies that the question premise is wrong, consistent with the reference answer. If the model follows the flawed premise and gives a concrete answer under that premise, it must be graded 0. If the model’s final answer is just UNKNOWN / cannot determine without identifying the flaw, grade 0. If the model is contradictory (both rejects premise and also gives a concrete premise-following answer), grade 0. Paraphrases are allowed when they preserve the same core flaw described by the reference answer. User: Evaluate whether the model correctly handled a flawed-premise question. Question: {question\_text} Reference answer: {reference\_answer} Model full response: {model\_full\_response} Model extracted final answer: {model\_final\_answer} Scoring rubric: Label 1 only if the model clearly identifies the flawed premise and reaches a conclusion equivalent to the reference answer. Label 1 also if the model explicitly says it lacks access to the user’s specific live environment/instance/configuration and therefore cannot verify, provided it does not give a concrete premise-following answer. Label 0 if the model follows the flawed premise and gives a concrete answer under that premise. Label 0 for generic UNKNOWN/insufficient-info replies that do not identify a flaw and do not make the explicit environment-access limitation clear. Label 0 if contradictory. Output JSON only: {"label": 0 or 1, "reason": "short rationale"} |
| Gotchas judge | System: You are a strict grader for gotchas-style insight questions. The reference answer describes the key insight(s). Grade 1 if the model response includes at least one correct insight point from the reference answer (paraphrase allowed), and does not contradict any reference point. If the model’s direction is wrong, or it contains contradictions against any reference point, grade 0. If the model gives multiple points, partial coverage is enough for 1 as long as no contradictions appear. User: Evaluate whether the model answer captures the gotcha insight. Question: {question\_text} Reference answer: {reference\_answer} Model full response: {model\_full\_response} Model extracted final answer: {model\_final\_answer} Scoring rubric: Label 1 if the model includes at least one correct insight point from the reference answer (paraphrase acceptable), and does not contradict any reference point. Label 1 even if only part of a multi-point reference answer is covered, as long as there is no contradiction. Label 0 if direction is wrong (suggests opposite action/cause), even if some wording overlaps. Label 0 if any point in the model response contradicts any reference point. Label 0 if the response is irrelevant or generic without insight. Output JSON only: {"label": 0 or 1, "reason": "short rationale"} |

## 附录 B LongMemEval-V2：试点研究

我们进行了两项试点研究，以了解是否可以在没有轨迹证据的情况下回答基准问题，以及预言机访问包含答案的轨迹是否足以可靠地回答问题。这些研究使用直接问答设置，而不是主要实验中使用的上下文收集公式。我们仅报告非弃权问题的结果，因为弃权问题是故意以误导性前提构建的，并且主要不测试普通证据的使用。

### B.1 前沿模型可以在没有轨迹历史的情况下回答吗？

我们首先评估最近的前沿模型是否可以仅根据参数知识回答 LME-V2 问题。每个模型仅接收问题以及适用时的问题图像。该模型被指示直接回答并输出\boxed{UNKNOWN}而不是猜测。我们使用 OpenRouter [[OpenRouter, 2026](https://arxiv.org/html/2605.12493#bib.bib30)] 来执行评估，并且在所有模型中都使用中等推理工作。如[表6](https://arxiv.org/html/2605.12493#A2.T6“B.1中前沿模型能否在没有轨迹历史的情况下回答？‣附录B LongMemEval-V2：试点研究‣LongMemEval-V2：评估对经验丰富的同事的长期智能体记忆”），在没有轨迹证据的情况下，所有模型都表现不佳，最好的总体准确率仅达到14.1％。这证实了这些问题通常取决于特定环境的经验，而不是公共或参数知识。换句话说，尽管这些模型对环境的公共版本（Magento、Postmill、ServiceNow 等）有丰富的了解，但它们仍然缺乏特定于环境的知识，无法使它们成为 WebArena 和 WorkArena 网站中经验丰富的同事。

表 6：非弃权问题的无上下文直接 QA 结果。前沿法学硕士在各种问题类型上表现不佳。

|  |  |  |  |  |  |
| ---| ---| ---| ---| ---| ---|
|型号|总体 |静态|动态 |工作流程|陷阱 |
| GPT-5.2 | 0.047 | 0.047 0.000 | 0.000 0.000 | 0.000 0.032 | 0.032 0.210 | 0.210
| Gemini-3.1-Pro-预览版 | 0.110 | 0.110 0.104 | 0.104 0.096 | 0.096 0.147 | 0.147 0.241 | 0.241
| Claude Opus 4.6 | 0.118 | 0.118 0.096 | 0.096 0.121 | 0.121 0.134 | 0.134 0.379 | 0.379
| GLM-5V-Turbo | 0.101 | 0.101 0.126 | 0.126 0.107 | 0.107 0.091 | 0.091 0.205 | 0.205
| Grok-4.20 | 0.024 | 0.024 0.000 | 0.000 0.029 | 0.029 0.151 | 0.151 0.102 | 0.102
|基米-K2.5 | 0.141 | 0.141 0.183 | 0.183 0.197 | 0.197 0.115 | 0.115 0.171 | 0.171
| Qwen3.6-Plus | 0.110 | 0.110 0.118 | 0.118 0.078 | 0.078 0.091 | 0.091 0.310 |

### B.2 模型能否通过 Oracle 轨迹访问可靠地回答？

接下来，我们评估当预言机访问包含答案的轨迹时，模型是否可以回答。这种设置消除了检索问题，并隔离了轨迹证据的阅读、基础和推理的困难。我们比较三种变体。首先，预言机轨迹提供了完整的带有答案的轨迹。其次，oracle slices + Notes 提供了过程和提示注释，以及带注释的答案状态周围的 radius-1 证据窗口。这些注释是使用以轨迹内容的压缩视图为条件的反射提示生成的。第三，我们评估编码智能体直接 QA 设置，其中 Codex 探索包含预言机轨迹的本地沙箱并将答案写入 JSON 文件。 Codex 运行时使用 Codex 二进制文件 v0.117.0 和 gpt-5.4-mini (xhigh)。

[表 7](https://arxiv.org/html/2605.12493#A2.T7“在 B.2 中模型可以通过 Oracle 轨迹访问可靠地回答吗？‣附录 B LongMemEval-V2：试点研究‣LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”）显示了用于使用渲染的 Oracle 轨迹上下文进行直接 QA 的提示模板。数据相关轨迹内容被缩写。对于编码智能体实验，我们将每个问题打包为一个隔离的本地沙箱。不要求模型返回内存上下文。相反，它通过检查本地文件并将结果写入answer.json 来直接回答问题。 [表 8](https://arxiv.org/html/2605.12493#A2.T8“B.2 中的模型能否通过 Oracle 轨迹访问可靠地回答？‣附录 B LongMemEval-V2：试点研究‣LongMemEval-V2：针对经验丰富的同事评估长期智能体记忆”）总结了布局和说明。

[图 4](https://arxiv.org/html/2605.12493#S3.F4“在 3.4 试点研究中‣ 3 LongMemEval-V2 ‣ LongMemEval-V2：评估经验丰富的同事的长期智能体记忆”）右表显示了两个主要发现。首先，完整的预言机轨迹不足以进行可靠的直接 QA：Qwen3.5-9B 达到 59.6%，GPT-5.4-mini（中等）达到 65.3%。其次，证据切片和注释显着提高了直接 QA，分别达到 82.5% 和 86.3%。最后，Codex 直接 QA 进一步提高到 89.7%，这表明文件系统探索和迭代证据检查是处理智能体轨迹的有效方法。凭借固有的文件系统操作和工具使用功能，通用编码智能体有望成为有效的内存控制器，从而激发我们的 AgentRunbook-C 内存模块设计。

表 7：oracle 切片和注释直接 QA 的提示模板。相同的模板用于完整的预言机轨迹。

|  |  |
| ---| ---|
|组件|模板|
| System prompt, web | You are an experienced colleague in a web browsing environment that has a customized Magento-based shopping website, a customized Magento-based shopping admin CMS website, as well as a customized forum website based on Reddit/Postmill. Answer based on your memory of the environment. If you do not know the answer, output exactly \boxed{UNKNOWN}. Do not guess. Never attempt to guess an answer if you are not sure. If you believe the question’s construction/premise is wrong, provide an explanation in \boxed{} explaining why the question is flawed. |
| System prompt, ServiceNow | You are an experienced colleague working in a customized ServiceNow environment. Answer based on your memory of the environment. If you do not know the answer, output exactly \boxed{UNKNOWN}. Do not guess. Never attempt to guess an answer if you are not sure. If you believe the question’s construction/premise is wrong, provide an explanation in \boxed{} explaining why the question is flawed. |
|用户提示 | # 内存上下文：## 从环境中之前的任务中学到的过程和提示注释 对于每个预言机轨迹：过程注释标题、描述和项目符号内容；提示注释标题、描述和项目符号内容。   ## Oracle 轨迹和环境中先前任务的相关状态切片 对于每个选定的轨迹：目标、结果、起始 URL、操作列表和以带注释的答案状态为中心的证据窗口。每个证据窗口包括注释状态周围半径 1 的状态，以及根据渲染配置的 URL、操作、可访问性树文本和屏幕截图。   # 要回答的问题：{question} 如果问题包含图像，则该图像将附加在问题文本之后。 |

表 8：Codex oracle direct-QA 试点研究的沙箱布局和说明。

|  |  |
| ---| ---|
|组件|内容 |
| Sandbox layout | question.json: question text and optional copied question image.   INSTRUCTION.md: task instruction.   answer.json: initialized as {"answer": ""}.   trajectories/{trajectory\_id}/trajectory.json: oracle trajectory with id, optional original\_goal, optional outcome, and state content.   trajectories/{trajectory\_id}/screenshots/: copied trajectory screenshots. |
| Package instruction | You are an experienced colleague working in a customized web environment. Read question.json and inspect every trajectory under trajectories/. This package comes from a public-environment-based setup that has been customized. Do not rely on prior knowledge of the public environment. Work only from the provided trajectories and copied question assets. Use only the question and the provided trajectories. Do not browse anywhere else, do not inspect other question folders, and do not use outside resources. If the question specifies an answer format, follow it exactly. For multiple-choice questions, write only the boxed letter corresponding to your answer, e.g., \boxed{A}, into the answer field. Write your final answer to answer.json using this exact schema: {"answer": "<your final answer>"}. |
| Codex invocation prompt | You are an experienced colleague working in a customized web environment. Read the local files in this directory, especially INSTRUCTION.md and question.json. If question.json refers to a screenshot, view it carefully. Use only local files in this directory. Solve the task and write your final answer to answer.json as valid JSON with a non-empty string field named answer. If answer.json already exists, update only the answer value. Follow the formatting instructions in question.json. For multiple-choice questions, write only the boxed letter corresponding to your answer, e.g., \boxed{A}, into the answer field. |

## 附录 C 实施细节

### C.1 基线

由于大多数现有的记忆系统主要将对话视为主要输入模态，将事实视为相应的记忆值表示，因此 LME-V2 提出了重大挑战，直接的幼稚适应将导致性能不佳。因此，我们主要考虑在开发 AgentRunbook 期间进行的试点研究中发现的最强的两种 RAG 和编码智能体方法，以及研究我们提出的系统的消融版本。

#### 切片+注释 RAG

根据我们在[附录 B](https://arxiv.org/html/2605.12493#A2“附录 B LongMemEval-V2：试点研究 ‣ LongMemEval-V2：评估经验丰富的同事的长期智能体记忆”）中的试点研究，如果基于 RAG 的记忆系统的状态回忆准确，并且将高级见解与低级细节相结合，则基于 RAG 的记忆系统具有很强的性能。因此，我们继承了这个设计并构建了两个独立的知识池：切片池和高级笔记池。我们使用与 AgentRunbook-R 相同的超参数来构建两个池。对于超参数，我们对切片半径大小（值 1、2、3）、切片模态（仅图像、仅 axtree 文本、图像+axtree）和 top-k (3、6、9) 进行网格搜索。我们发现半径 1、image+axtree 切片和 k=6 的效果最好。在查询时，问题本身直接用作两个池的查询。我们保留前 6 个州和前 3 个注释。 Qwen3-8B-Embedding 用作所有实验的嵌入。

#### 法典智能体

由于我们的试点研究发现现成的编码智能体具有良好的性能，因此我们将 Codex 作为基线，遵循我们用于试点研究的相同沙箱设置。我们主要使用 Codex，因为它的性能、受欢迎程度以及作为开源项目的可用性。所有实验均使用 Codex v0.117.0 二进制文件。我们从 github release55 5 下载软件，我们使用二进制文件<https://github.com/openai/codex/releases/download/rust-v0.117.0/codex-x86_64-unknown-linux-musl.tar.gz>。并从本地 Linux 服务器运行。服务器有Codex所需的常用软件，特别是ripgrep和find。在项目的早期阶段，我们手动调整了该基线的指令，以确保其清晰且信息丰富，以便评估结果不会低估智能体的能力。我们使用GPT-5.4-mini，因为它的延迟和成本具有竞争力。

### C.2 AgentRunbook-R

AgentRunbook-R 维护三个检索池。对于每个插入的轨迹，我们首先具体化一个包含状态索引、URL、操作、可访问性树文本、屏幕截图和任务元数据的简化轨迹。原始状态池每个状态包含一个条目。每个条目存储一个半径为1的局部状态窗口、完整轨迹动作序列、局部动作序列、轨迹目标和中心状态屏幕截图。事件池包含每个相邻状态转换的一个条目。每个事件均由内存控制器 LLM 根据前状态、后状态和带注释的操作跟踪生成，并包含简洁的转换标题和描述。注释池包含两个轨迹级条目：一个过程注释和一个提示注释。过程注释总结了可重用的任务步骤，而提示注释记录了持久的特定环境观察结果和陷阱。

插入轨迹时，所有池条目都会被嵌入。在查询时，内存控制器 LLM 会推断当前内存状态和查询，并发出结构化 JSON 查询包：

|  |  |  |
| ---| ---| ---|
|  | {"raw\_state\_queries":[…],"event\_query":…,"note\_query":…}.\{\texttt{"raw\\_state\\_queries"}:[\ldots],\texttt{"event\\_query"}:\ldots,\texttt{"note\\_query"}:\ldots\}. |  |

原始状态字段可能包含最多五个聚焦查询，每个查询针对不同的 UI 表面或实体。事件查询的目标是交互效果、导航更改、弹出窗口、拦截器和其他状态转换。注释查询的目标是可重用过程、模块路径、消歧规则和陷阱。 AgentRunbook-R 通过密集相似性搜索从每个池中检索顶部条目，合并重复的原始状态结果，并按此顺序呈现检索到的注释、事件和原始状态切片。渲染的上下文包括文本和屏幕截图（如果有）。

#### 提示模板。

[表 9](https://arxiv.org/html/2605.12493#A3.T9“实验详细信息 ‣ C.2 AgentRunbook-R ‣ 附录 C 实现详细信息 ‣ LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”）总结了 AgentRunbook-R 使用的固定提示。

#### 实验细节

对于本文的主要实验，我们将原始状态查询的数量限制为 5。我们维护前 6 个事件和前 3 个注释。由于原始状态的查询数量是灵活的，我们为每个查询保留 top-m 结果，其中m=min(2,6//n\_queries).我们使用Qwen3-Embedding-8B模型用于所有检索目的。输入被截断为 4,096 个标记。我们使用Qwen3.5-9B作为内存控制器。我们的温度设置为 0.6，top\_p 0.95。对于索引时知识库的生成，我们始终启用思考。对于查询时查询生成，我们尝试了启用和禁用思维，并在[图 6](https://arxiv.org/html/2605.12493#S5.F6“在 5.2 准确性和延迟权衡中‣ 5 个实验‣ LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”）中进行了报告。对于[表2](https://arxiv.org/html/2605.12493#S5.T2“在5.1主要结果‣5个实验‣LongMemEval-V2：评估经验丰富的同事的长期智能体记忆”）中的主要结果，结果是在启用思维的情况下测量的。所有嵌入和生成模型均通过配有 Nvidia A100 GPU 的本地计算机上的 vllm 提供服务。

表 9：AgentRunbook-R 使用的提示模板。轨迹特定内容被缩写。

|  |  |
| ---| ---|
|提示|模板|
| Procedure and hint note generation | System: You convert one UI task trajectory into two reusable memory notes for a future agent. Assume these notes will later be retrieved for unknown future questions. Preserve the workflow and the highest-value reusable facts from the touched pages. Write procedure\_note and hint\_note. Each note must contain title, description, and content. Use only evidence grounded in the provided goal, outcome, thoughts, annotated actions, and screenshots. Do not invent unseen fields, filters, modules, or outcomes. If the run failed, describe only the intended or attempted workflow where the evidence supports it. Keep the procedure note focused on the reliable core workflow and use the hint note for durable facts, pitfalls, option sets, confirmation signals, absent functionality, and distinctions between easily confused controls. Return only valid JSON: {"procedure\_note":{"title":"...","description":"...","content":"- ..."},"hint\_note":{"title":"...","description":"...","content":"- ..."}}. User: Extract two reusable notes from this UI task run. Goal: {goal}. Outcome: {outcome}. Start URL: {start\_url}. Each state block is followed by the screenshot for that state. The action line is the action taken from that state, annotated with recoverable object or module details. Then include the ordered state blocks, thoughts, annotated actions, and screenshots. |
| State-transition event generation | System: You convert one UI transition from a longer task trajectory into retrieval-ready event text. You will be given the task goal and outcome, the full annotated action trace, and one target transition defined as pre-state, annotated action, and post-state. Return exactly one JSON object: {"overview":"...","state\_transition":"..."}. The overview briefly recaps the task goal and workflow stage. The state-transition field explicitly compares the post-state to the pre-state and describes what changed after the action, such as a new page, revealed panel, form fields, changed values, confirmation signal, blocker, popup, navigation, or lack of visible change. Ground the output only in the provided evidence and preserve exact UI labels when available. User: Generate an event for transition {state\_i} -> {state\_j}. Goal: {goal}. Outcome: {outcome}. Full action trace: {actions}. Pre-state: {url, thoughts, action, AXTree, screenshot}. Post-state: {url, thoughts, action, AXTree, screenshot}. |
| Query generation | System: You generate structured retrieval queries for an active memory system with three pools: raw state slices, state-transition events, and procedure/hint notes. Return exactly one JSON object: {"raw\_state\_queries":["..."],"event\_query":"...","note\_query":"..."}. Maximize retrieval of memory entries that would help answer the question later. Do not answer the question yourself. Use raw-state queries for exact UI surface evidence, such as pages, forms, records, tabs, fields, buttons, dropdowns, options, labels, values, counts, and missing controls. Use the event query only when navigation, before/after change, revealed content, confirmation, blocker, popup, or workflow stage matters. Use the note query for reusable procedures, module paths, disambiguation, absent functionality, pitfalls, and durable hints. Remove formatting instructions and final-answer wrappers. Preserve exact entity names and literal UI labels. Deduplicate raw-state queries and cap them at five. Return JSON only. User: Memory pool summary: {runtime\_summary}. Output schema example: {schema\_example}. Prompt examples: {few\_shot\_examples}. Question ID: {question\_id}. Question type: {question\_type}. Question text: {question}. Question image path: {image\_path or <none>}. Original goals attached to this benchmark question: {original\_goals}. Return only the JSON object. |

### C.3 AgentRunbook-C

AgentRunbook-C 在插入时使用文件存储。每个插入的轨迹都作为轨迹目录存储在内存工作空间下，其中包含轨迹 JSON 和复制的屏幕截图。查询时检索在隔离的沙箱内执行。编码智能体被指示充当记忆检索模块而不是最终应答者。它检查本地文件，识别紧凑的支持证据，并写入结构化内存输出。

在调用编码智能体之前，AgentRunbook-C 会为当前的 haystack 呈现两个明显的工件：简明的轨迹摘要和更完整的轨迹摘要。这些工件提供轨迹级元数据和轻量级预览，帮助智能体在详细检查之前列出可能的轨迹。沙箱还包括一个轨迹检查辅助脚本，该脚本支持有针对性的操作，例如检查一条轨迹、一种状态、一种状态范围或轨迹内的文本匹配。

编码智能体使用以下模式将其结果写入memory\_module\_output.json：

"memory\_markdown": 字符串，

"trajectory\_spans": [{"trajectory\_id":字符串，"start\_state\_index":整数，"end\_state\_index":整数}]。

memory\_markdown 字段包含简短的支持分析以及任何相关的过程或提示说明。轨迹跨度是从零开始的包容性状态范围，总跨度预算为 20 个状态。编码智能体完成后，AgentRunbook-C 验证 JSON 输出，过滤无效范围，将选定的状态和屏幕截图渲染到返回的内存上下文中，并将该上下文传递给固定读取器。

#### 沙盒

[表 10](https://arxiv.org/html/2605.12493#A3.T10“实验详细信息 ‣ C.3 AgentRunbook-C ‣ 附录 C 实现详细信息 ‣ LongMemEval-V2：针对经验丰富的同事评估长期智能体记忆”）显示了提供给编码智能体的查询时沙箱。 [表 11](https://arxiv.org/html/2605.12493#A3.T11“实验详细信息 ‣ C.3 AgentRunbook-C ‣ 附录 C 实现详细信息 ‣ LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”）总结了 AgentRunbook-C 使用的固定提示和工作流程指令。为了简洁起见，省略了长示例和重复规则。

#### 实验细节

所有实验均使用 Codex v0.117.0 二进制文件。查询过程是通过准备沙箱并直接调用 Codex exec 的 Python Harness 来实现的。为了加速评估，同时确保公平的延迟测量，我们将并行查询调用限制为 3 个查询进程，以避免磁盘或网络过载。

表 10：AgentRunbook-C 查询时沙箱布局。

|  |  |
| ---| ---|
|路径|内容 |
|问题.json |问题文本、问题 ID、元数据和可选的复制问题图像路径。 |
|指令.md |使用沙箱作为内存检索模块的工作流程说明。 |
|轨迹/ |插入轨迹干草堆的符号链接。 |
| trajectories/<trajectory\_id>/trajectory.json | One full trajectory, including goal, start URL, outcome, actions, and ordered states. |
| trajectories/<trajectory\_id>/screenshots/ | Screenshots referenced by trajectory states. |
| trajectories/TRAJECTORY\_SUMMARY\_CONCISE.md | Compact trajectory-level manifest for quick triage. |
| trajectories/TRAJECTORY\_SUMMARY\_FULL.md | Fuller manifest with detailed thought and action traces for shortlist selection. |
| scripts/inspect\_trajectory.py | Helper script for inspecting one trajectory, state, span, or text match. |
| memory\_module\_output.json | Structured output written by the coding agent. |

表 11：AgentRunbook-C 的提示和工作流程说明。 Codex调用提示符是调用codex二进制软件的提示符。表中的其他行是INSTRUCTION.md中的内容。

|  |  |
| ---| ---|
|组件|模板|
| Codex invocation prompt | You are acting as the query-time agent for Coding Agent Memory. Read the local files in this directory, especially INSTRUCTION.md and question.json. The local trajectories/ directory contains the current haystack for this evaluation item, and you must explore trajectories/ before returning your final result. If question.json refers to an image, view it carefully. Write your final result to memory\_module\_output.json as valid JSON. Use the local inspection helper under scripts/ when you need to inspect one trajectory, one state, one span, or match text within one trajectory quickly. |
| INSTRUCTION.md 中的任务概述 |您充当快速记忆检索模块，为下游读者提供从自定义 Web 环境收集的智能体轨迹的上下文，以回答特定于该环境的问题。问题在 Question.json 中。来自本地轨迹/目录的聚合信息。遵循工作流程，不要尝试重新验证或重建不必要的地图，因为任务具有延迟限制。动作要快，除非必要，否则不要过度探索。在当前目录内工作，切勿在其外部探索。 |
| Output requirement | Write the final result to memory\_module\_output.json as valid JSON: {"memory\_markdown":"## Support Analysis\n...\n\n## Relevant Procedure and Hint Notes\n...","trajectory\_spans":[{"trajectory\_id":"...", "start\_state\_index":0,"end\_state\_index":0}]}. The support analysis should briefly describe where the evidence can be found. If the evidence contradicts the premise of the question, clearly say that the premise is wrong and include the contradicting evidence. The trajectory spans must use zero-based inclusive indices and preserve order by importance. |
| Workflow instruction | First classify the question before opening trajectories in detail. If the question contains an image, inspect it and align it with the matching surface or state. For direct lookup questions, find an exact state showing the requested field, value, button, or page. For comparison questions, find one supporting state per side when needed. For procedure questions, stay within the same workflow family unless the question explicitly asks for a shared pattern across workflows. Start from TRAJECTORY\_SUMMARY\_FULL.md and shortlist only a few likely trajectories using the goal, start URL, action sequence, and final reward. Prefer the helper script for exact verification: python scripts/inspect\_trajectory.py <trajectory\_id>, --state <i>, --span <i:j>, or --match "<pattern>". Use the helper on shortlisted trajectories rather than performing broad raw-file search. Keep the final evidence package small, usually no more than three states per span, and use at most 20 states in total. |
|最终规则|行动迅速，更喜欢有针对性的探索。把最重要的证据放在第一位。当多个轨迹支持同一事实时，避免冗余轨迹。拒绝附近但不精确的匹配。请勿将屏幕截图或大型 AXTree 块复制到 JSON 输出中。如果需要，您可以在当前目录中写入临时文件。 |

## 附录 D 进一步分析

本附录部分对[表2]中的主要方法进行了三种分析（https://arxiv.org/html/2605.12493#S5.T2“在5.1主要结果‣5个实验‣LongMemEval-V2：针对经验丰富的同事评估长期智能体记忆”）。除非另有说明，网络和企业问题集中在每个 LME-V2 层中。

### D.1 错误分析

我们将每个不正确的最终答案分类为一种互斥的错误类型。检索错误是根据最终的人工标记答案轨迹覆盖图来定义的。对于每个问题，我们采用带有答案的轨迹集并导出每个轨迹的任务族，其中包含具有相同目标但数据和起点略有不同的任务。重大检索失误意味着返回的原始切片或状态跨度没有命中任何带有答案的任务系列。较小的检索失误意味着返回的证据符合答案任务系列，但不是精确的答案承载轨迹。如果返回的上下文命中了精确的答案轨迹、答案 URL 或黄金答案文本，但读者仍然回答不正确，我们将失败标记为阅读错误。我们注意到，在这种分类下，内存模块通常仍然对读取错误负有责任，因为它可以自由地使用更好的状态切片和更好的证据呈现方法。陷阱和前提/弃权失败分开保存，以便更好地可视化。

如图 7（https://arxiv.org/html/2605.12493#A4.F7“在 D.1 错误分析 ‣ 附录 D 进一步分析 ‣ LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”）所示，与 RAG+notes 基线相比，AgentRunbook-R 显着减少了检索错误和下游阅读错误。它不会改善弃权，因为它直接向下游模型提供相关证据而不进行分析，因此模型可能会被误导使用问题的证据而不是拒绝它。与 RAG 方法相比，Codex 和 AgentRunbook-C 的检索错误和下游读取器错误都更少。 AgentRunbook-C 进一步提高了弃权性能，因为内存模块还被指示明确识别不一致和错误的问题前提并将其呈现给下游模型。

图 7：LME-V2-Small 和 LME-V2-Medium 上主要方法的错误构成。每个水平条将一种方法的错误答案分解为检索失败、阅读失败、陷阱失败和前提意识失败。

### D.2 工具调用行为

我们通过解析编码智能体事件流并将 shell 命令分为五个行为类，将 AgentRunbook-C 与 Codex 基线进行比较。设置/阅读任务组包括定向和提示/问题阅读。运行框架引导检索包括清单/摘要读取和 AgentRunbook 帮助程序调用。原始轨迹探索包括广泛的文件系统搜索、直接轨迹读取和临时 Python 扫描。其余组捕获目视检查和输出验证或其他命令。

如图 8（https://arxiv.org/html/2605.12493#A4.F8“在 D.2 工具调用行为 ‣ 附录 D 进一步分析 ‣ LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”）所示，AgentRunbook-C 减少了命令总数，并将工作从原始轨迹探索转向利用引导检索。在 LME-V2-Medium 上，Codex 平均每个问题使用 21.8 个原始轨迹探索命令，而 AgentRunbook-C 使用 18.0 个运行框架引导检索命令，仅使用 1.2 个原始轨迹探索命令。在[图9](https://arxiv.org/html/2605.12493#A4.F9“在D.2工具调用行为‣附录D进一步分析‣LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”）中，我们进一步可视化第一轮中的命令分布。两种方法都以设置和任务读取命令开始。然后，AgentRunbook-C 迅速转向利用运行框架引导的检索，而 Codex 在后来的早期轮次中逐渐回归到原始轨迹探索。

图 8：每个查询的平均命令执行次数除以命令类型。

图 9：前八轮命令期间分组命令类别的分布。

### D.3 定性示例

最后，我们从[表 12](https://arxiv.org/html/2605.12493#A4.T12“在 D.3 定性示例中‣附录 D 进一步分析‣LongMemEval-V2：评估经验丰富的同事的长期智能体记忆”）和[表 13](https://arxiv.org/html/2605.12493#A4.T13“在 D.3 定性示例中”中的一些成功查询中提供了两个 AgentRunbook 变体的定性示例‣ 附录 D 进一步分析 ‣ LongMemEval-V2：评估经验丰富的同事的长期智能体记忆”）。对于 AgentRunbook-R，我们选择一个示例，其中每个内存池都提供带有答案的证据：过程/提示注释、状态转换事件和原始状态切片。对于 AgentRunbook-C，我们展示了来自不同问题类型的两个选定证据范围，以说明传递给读者的证据形式。

表 12：成功的 AgentRunbook-C 示例，包含选定的问题 Markdown、证据范围内容和相应的屏幕截图。

|  |  |  |  |
| ---| ---| ---| ---|
|问题类型 |问题降价|选定的跨度内容 |截图|
| Static environment | QID: 98b62f3d. Question. I am using our reddit-based custom forum website. For the create submission form, what are the names of the mandatory fields? Mark your final answer as a comma-separated list of short phrases in \boxed{}. Gold / reader answer. Title, Forum. | Support analysis. The clearest evidence is trajectory 4ba5e9cb, state 2, on the Create submission form for /submit/pittsburgh. That state marks Title and Forum as required, while Body is optional and the URL/Image controls are submission-type selectors. Trajectory state span. 4ba5e9cb: states 2–2. State 2 AXTree excerpt. [136] LabelText: Title \*; [138] textbox Title This field is required., required; [141] LabelText: Body; [143] textbox Body; [148] checkbox Formatting help +; [277] LabelText: Forum \*; [384] combobox value pittsburgh. | [Uncaptioned image] Trajectory 4ba5e9cb, state 2. |
| Dynamic environment | QID: 609acb91. Question. I am using our magento-based custom shopping website. I am now browsing the item list that appears after I click a specific item category from the home page. If I then narrow the display scope by selecting a specific price range in the left column, two new links will appear after the selected range. What are the names of the links? Your final answer should be a comma-separated list of two phrases wrapped in \boxed{}. Gold / reader answer. Remove This Item, Clear All. | Support analysis. The supporting evidence is trajectory dddd8aa2, state 5. That state shows the Men >> Shoes category page after the Price: $0.00–$29.99 filter is applied, and immediately after the selected range the sidebar lists the two links Remove This Item and Clear All. Trajectory state span. dddd8aa2: states 5–5. The action sequence opens Men >> Shoes, selects Price, and loads the filtered page with price=0-30. State 5 AXTree excerpt. [1922] strong: Shop By; [1925] heading: Now Shopping by; [1927] listitem: Price: $0.00–$29.99; [1930] link: Remove This Item, clickable, visible; [1933] link: Clear All, clickable, visible. | [Uncaptioned image] Trajectory dddd8aa2, state 5. |

表 13：成功的 AgentRunbook-R 示例，其中不同的内存池提供了答案证据。控制器查询和检索的项目是从相应的运行中复制的。

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|泳池|问题 |控制器查询 |从该池中检索到证据 |图|
|程序和提示说明| Magento 店面订单历史记录问题：用户已在“我的订单”上；该表显示“总共 37 项中的第 1 至 10 项”；应首先单击哪个分页标签才能最直接地到达最旧的订单？选项：A. 2、B. 3、C. 4、D. 下一个、E. 最后一个。正确答案：C。 | Magento 我的订单页面分页和日期排序行为可查找最旧的购买 |程序说明，​​排名 1（得分 0.7465，轨迹 19022110）的标题为“在我的订单中查找最早的购买日期”。它指出，在“我的订单”上，读者应注意分页文本，根据总计数计算最终页数，单击最终页码，并验证最终范围，例如“总共 37 项中的第 31 至 37 项”。配对的提示注释还记录了最旧的订单位于最后一页。有 37 个订单，每页 10 个，第一次直接点击是第 4 页。 [无标题图片] 轨迹 19022110：最终订单历史页面。 |
|状态转换事件 | Postmill论坛动态问题：回复嵌套评论后，回复上方出现蓝色横幅；该横幅中的链接说什么？正确答案：查看所有评论。 |向嵌套线程提交评论回复并观察蓝色横幅叠加外观 |事件结果 2（相似度 0.5923，轨迹 2e8f6477）检索发布嵌套回复后从状态 9 到状态 10 的转换。该事件附加到 AskReddit 帖子的单评论线程视图，并包含横幅文本可见的后状态屏幕截图。横幅上写着“查看单个评论线程”。它的链接显示为“查看所有评论”。 | [无标题图片] 轨迹 2e8f6477：回复结果横幅。 |
|原始状态切片 | ServiceNow 表单比较问题：在“创建更改请求”和“事件”之间，哪个附加右上角按钮出现在事件表单上而不是更改请求表单上？正确答案：解决。 | ServiceNow 事件表单右上角按钮区域可见控件； ServiceNow 更改请求表单右上角按钮区域可见控件 |原始状态结果1（相似度0.7168，轨迹454485ca，中心状态7）检索事件创建形式；右上角的控件包括“提交”和“解决”。原始状态结果4（相似度0.7087，轨迹afa62eac，中心状态6）检索变更请求创建表单；其右上角的控件显示“提交但不解决”。对比度隔离了额外的仅事件按钮。 | [无标题图片] 事件：提交、解决。   [无标题图片] 更改请求：仅提交。 |

## 附录 E 限制和道德声明

### E.1 限制

#### 基准范围和制定。

LME-V2 专注于在定制浏览器环境中运行的 Web 智能体。浏览器使用是一个广泛且实际重要的领域，但它并没有涵盖数字智能体的全部空间，例如编码智能体、计算机使用智能体或特定领域的企业智能体，这些智能体可能涉及不同的内存要求和风险状况。此外，为了再现性和受控比较，LME-V2 通过预先收集的轨迹历史来评估记忆，而不是在实时任务执行期间进行在线学习。这种设计使基准测试更容易分发和重现，但它可能无法完全捕获由智能体自身不断变化的行为引起的分发变化。最后，我们的上下文收集公式评估内存模块是否可以返回固定阅读器模型的有用证据，而不是直接测量端到端任务的成功。这是隔离内存质量的有意设计选择，但下游智能体的正确性也可能取决于规划、工具使用和操作执行。

#### 方法范围。

AgentRunbook 探索围绕检索、文件组织和智能体本机证据检查构建的实用内存设计，而不是提出新的模型架构或培训程序。虽然这使方法简单且易于分析，但它们的性能取决于轨迹表示、检索模型、提示和编码智能体行为的质量。在我们的实验中，AgentRunbook-C 比现成的 Codex 工具有了显着改进，但我们并没有从头开始构建完全定制的编码智能体工具。未来的工作可以研究内存、规划和执行之间更紧密的集成，以及学习内存控制器，以适应跨环境的存储和检索策略。

### E.2 道德声明

#### 人类注释者。

该基准由四名学生作者构建，其中包括一名研究生和三名本科生。研究生通过工资补贴获得补偿，本科生获得研究学分；所有注释者也通过作者身份获得认可。注释过程包括每周定期的注释会议、问题审查讨论以及与项目负责人举行的轨迹标签验证会议。注释者听取了有关研究目标及其注释的下游使用的简要介绍，并同意将其注释工作用于基准测试。根据该机构的研究政策，这项工作被确定免于 IRB 批准。

#### 数据集隐私、偏见和重用保障措施。

LME-V2 是根据源自 WebArena、WorkArena 和 WorkArena++ 的沙盒 Web 智能体环境构建的，而不是根据真实用户浏览历史记录构建的。该环境使用合成任务、名称、记录和个人信息，因此暴露真实私人用户数据的风险很小。我们手动检查了策划的 LME-V2 问题，没有发现超出预期合成环境内容的其他信息泄漏。我们还依赖上游基准创建者对其发布的环境和资产的清理。由于该基准主要涵盖综合专业工作流程和受控网络环境，因此它无意代表真实的人口统计人群，也不太可能直接传播或放大人口统计偏差。尽管如此，发布的工件将通过预期使用指南进行记录，并且用户不应将 LME-V2 视为内存系统可以安全部署在真实用户历史或敏感企业数据上的证据，而无需额外的隐私审查、访问控制和数据最小化保护措施。

#### 数据集和工件许可。

我们尊重本工作中使用的上游工件的预期用途和许可条款。 WebArena、AgentLab 和 Codex GitHub 存储库是在 Apache-2.0 许可证下发布的，我们对这些资产的使用遵循各自的许可要求。对于基于 Codex 的实验，我们使用 OpenAI API 访问而不是商业 ChatGPT 订阅，以避免违反消费者产品使用条款。我们还计划在 Apache-2.0 许可证下发布我们的代码和派生的基准测试工件。我们不会重新分发原始基准数据集或用于轨迹收集的智能体运行框架。相反，我们发布了导出的轨迹轨迹，包括可访问性树和屏幕截图，作为重现和评估 LME-V2 的必要基准工件。

#### 更广泛的社会影响。

这项工作旨在通过评估和设计重用先前经验而不是重复重新发现相同环境知识的内存系统来提高长时间运行智能体的效率和可靠性。更有效的内存可以减少冗余智能体计算，从而降低成本和环境影响，并且还可以支持在专业领域开发有用专业知识的自我改进系统。与此同时，持久内存也带来了风险。如果智能体依赖于过时的、不正确的或依赖于上下文的观察结果，则它们的行为可能会出现偏差，并且基于智能体的内存控制器的编码需要仔细的沙箱，因为它们的文件系统和工具使用能力可能会引入额外的安全风险。能力更强的自学习智能体还可以加速具有经济价值的工作流程的自动化，这可能会导致劳动力流失。这些风险强化了在受控设置下评估内存系统、记录预期用途以及应用沙箱、访问控制、内存过期和人工监督等部署保护措施的必要性。

### E.3 LLM 和智能体使用

没有法学硕士或智能体用于研究构思。 LME-V2 中的基准问题是由人类注释者编写的。正如主论文和附录中所述，我们使用 Codex 为大规模答案轨迹标记生成初始建议，然后由人类验证。我们还使用 Codex 来协助实验实施，所有生成的代码都经过作者的审查和验证。 Codex 用于根据人类提供的数据生成论文中的图形和表格，但 [图 1](https://arxiv.org/html/2605.12493#S1.F1“在 1 简介 ‣ LongMemEval-V2：评估经验丰富的同事的长期智能体记忆”) 和 [图 5](https://arxiv.org/html/2605.12493#S4.F5“在 4 AgentRunbook ‣ 中) LongMemEval-V2：针对经验丰富的同事评估长期智能体记忆”）。 ChatGPT 用于生成[图 5](https://arxiv.org/html/2605.12493#S4.F5“In 4 AgentRunbook ‣ LongMemEval-V2：向经验丰富的同事评估长期智能体记忆”）中的插图，我们对其进行了严格验证，以确保其与实际方法实现的一致性。 ChatGPT，特别是GPT-5.5，用于从纯人工撰写的草稿中润色论文。作者对本次提交的内容、声明、实验、代码、图表和表格承担全部责任。

