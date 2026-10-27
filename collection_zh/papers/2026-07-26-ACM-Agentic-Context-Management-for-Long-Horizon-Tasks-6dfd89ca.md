> 本文为简体中文机器翻译，使用 Google Translate 公开接口并统一技术术语，尚未经逐句人工校对。代码、链接和公式按原文保留；实验数字及技术结论请对照原文。
> [查看本地英文原文](../../collection/papers/2026-07-26-ACM-Agentic-Context-Management-for-Long-Horizon-Tasks-6dfd89ca.md) · [原始来源](https://arxiv.org/abs/2607.23809)

# ACM：面向长程任务的智能体上下文管理

- 来源: https://arxiv.org/abs/2607.23809- 发布日期: 2026-07-26- 日期依据: page metadata: citation_date- 类型: paper- 主题: Agentic Context Management、长程任务- 抓取状态: full_text_html- 正文来源: https://arxiv.org/html/2607.23809- 抓取时间 UTC: 2026-10-26T09:35:56.721089+00:00 - 作者: Li, Xiaochuan, Ming, Ryan, Chu, Meng, Shao, Shuai, Jin, Rong, Xiong, Chenyan

## 来源摘要/页面简介

摘要：智能体任务本质上是长程和多轮次的，通过与环境的交互不断积累上下文。现有的上下文压缩方法不可避免地会导致信息丢失，并且由严格的启发式规则触发，导致它们与智能体不断发展的推理焦点不一致。我们提出了智能体上下文管理（ACM），这是一个为智能体配备专用上下文编辑工具的框架，用于无损上下文管理。受短期和长期人类记忆之间相互作用的启发，智能体自主决定何时压缩其上下文，将丢弃的内容卸载到外部存储系统，并按需查询以供以后检索。在此框架的基础上，我们进一步开发了一个训练后管道，该管道构建高质量的上下文管理演示，并提高智能体搜索和编码任务的模型性能。进一步的分析表明，有效的上下文管理可以降低峰值词元压力，实现扩展探索，并在独立试验中产生更一致的解决方案。代码、数据和模型检查点可从此 https URL 获取。

## 抓取正文（中文翻译）

# ACM：长期任务的智能体上下文管理

李晓川1*  明明1*  孟初1

邵帅2  荣进2  熊晨艳1
  
  
1卡内基梅隆大学 2Meta
  
{xiaochu4,cx}@andrew.cmu.edu

###### 摘要

智能体任务本质上是长程和多轮次的，通过与环境的交互不断积累上下文。现有的上下文压缩方法不可避免地会导致信息丢失，并且由严格的启发式规则触发，导致它们与智能体不断发展的推理焦点不一致。我们提出了智能体上下文管理（ACM），这是一个为智能体配备专用上下文编辑工具的框架，用于无损上下文管理。受短期和长期人类记忆之间相互作用的启发，智能体自主决定何时压缩其上下文，将丢弃的内容卸载到外部存储系统，并按需查询以供以后检索。在此框架的基础上，我们进一步开发了一个训练后管道，该管道构建高质量的上下文管理演示，并提高智能体搜索和编码任务的模型性能。进一步的分析表明，有效的上下文管理可以降低峰值词元压力，实现扩展探索，并在独立试验中产生更一致的解决方案。代码、数据和模型检查点可在<https://github.com/lixiaochuan2020/agentic-context-management>获取。

††脚注文本：\* 平等贡献。所有实验、数据收集和处理活动均由卡耐基梅隆大学进行。 Meta 仅发挥咨询作用，未在 Meta 基础设施上进行任何实验、数据收集或处理活动。通讯作者：李小川<xiaochu4@andrew.cmu.edu>

## 1 简介

|方法|紧凑|可培训|无损|智能体初始化 |开源数据|
| ---| ---| ---| ---| ---| ---|
| ACE（[Zhang et al., 2026](https://arxiv.org/html/2607.23809#bib.bib53)）| ✗ | ✗ | ✗ | ✗ | ✓ |
| Mem1（[周等人，2025](https://arxiv.org/html/2607.23809#bib.bib54)）| ✗ | ✓ | ✗ | ✗ | ✓ |
| ReSum（[Wu et al., 2025](https://arxiv.org/html/2607.23809#bib.bib41)）| ✓ | ✓ | ✗ | ✗ | ✗ |
| ACON（[Kang 等人，2025](https://arxiv.org/html/2607.23809#bib.bib17)）| ✓ | ✗ | ✗ | ✗ | ✓ |
| SUPO（[Lu et al., 2025](https://arxiv.org/html/2607.23809#bib.bib23)）| ✓ | ✓ | ✗ | ✗ | ✗ |
| AgentFold（[叶等人，2025](https://arxiv.org/html/2607.23809#bib.bib49)）| ✓ | ✓ | ✗ | ✓ | ✗ |
| ACM（我们的）| ✓ | ✓ | ✓ | ✓ | ✓ |

表 1：上下文管理方法的比较。紧凑：主动压缩工作环境。可培训：管理政策是在培训中学习的。无损：保留原始内容以供以后检索。 智能体-init：压缩由智能体本身触发。开源数据：上下文管理策略的训练数据公开发布。更多详细信息请参阅附录 [A](https://arxiv.org/html/2607.23809#A1“附录 A 基线详细信息 ‣ ACM：长期任务的智能体上下文管理”)。

智能体任务已成为 LLM 支持的自主智能体的核心挑战（[Xu 等人，2024](https://arxiv.org/html/2607.23809#bib.bib43)；[Xie 等人，2024](https://arxiv.org/html/2607.23809#bib.bib42)；[Deng 等人，2025](https://arxiv.org/html/2607.23809#bib.bib9)；[Yang 等人， 2024](https://arxiv.org/html/2607.23809#bib.bib46)；[Wang 等人，2024b](https://arxiv.org/html/2607.23809#bib.bib39)；[人类，2024](https://arxiv.org/html/2607.23809#bib.bib2)；[OpenAI，2025a](https://arxiv.org/html/2607.23809#bib.bib24)）。这些任务要求智能体制定适应性计划，调用工具（[Schick et al., 2023](https://arxiv.org/html/2607.23809#bib.bib30)），并根据环境反馈调整其行动。然而，长期智能体任务产生的痕迹本质上是冗长且嘈杂的。在现实环境中，冗长的工具输出通常与失败的尝试和冗余的观察交织在一起。当与智能体自身的推理轨迹相结合时，它们会积累成超出智能体有效上下文容量的历史记录，即使底层模型支持数百万个词元的名义上下文窗口（[Gemini Team, Google, 2024](https://arxiv.org/html/2607.23809#bib.bib11); [Anthropic, 2025](https://arxiv.org/html/2607.23809#bib.bib3); [OpenAI, 2025b](https://arxiv.org/html/2607.23809#bib.bib25))。

之前的工作已经探索了几个方向来减轻这种限制。长上下文预训练扩展了窗口，但表现出可测量的退化（[Liu et al., 2024](https://arxiv.org/html/2607.23809#bib.bib21); [Hsieh et al., 2024](https://arxiv.org/html/2607.23809#bib.bib15); [Bai et al., 2024](https://arxiv.org/html/2607.23809#bib.bib5); [Hong等人，2025](https://arxiv.org/html/2607.23809#bib.bib14))。混合注意力降低了处理长输入的成本，但仍然基本上受到上下文窗口的限制（[Dao and Gu, 2024](https://arxiv.org/html/2607.23809#bib.bib8); [Liu et al., 2025](https://arxiv.org/html/2607.23809#bib.bib20); [Lenz et al., 2025](https://arxiv.org/html/2607.23809#bib.bib19))。上下文压缩管道——将历史截​​断、总结或重新呈现为更密集的格式——代表了一个有前途的方向（[Wei et al., 2025](https://arxiv.org/html/2607.23809#bib.bib40); [Kang et al., 2025](https://arxiv.org/html/2607.23809#bib.bib17)）。然而，这些方法通过强制的、手工制作的外部监视器来控制压缩时间，依赖于与模型自身推理过程不太一致的启发式规则。

在本文中，我们提出了一个能够实现模型固有且无损上下文管理的框架。具体来说，通过为智能体配备一套精心设计的内存工具，我们允许智能体自己决定何时以及如何管理其上下文：识别不相关的信息，总结并将其卸载到外部存储器，并按需查询。我们的设计从人类认知中短期记忆和长期记忆之间的分离中汲取灵感（[Atkinson and Shiffrin, 1968](https://arxiv.org/html/2607.23809#bib.bib4); [Packer et al., 2023](https://arxiv.org/html/2607.23809#bib.bib27)）——上下文消息充当专注于推理的紧凑工作记忆缓冲区，而外部存储充当为未来做好准备的长期记忆检索。这种机制使智能体能够随着对任务进展的理解的发展而扩展或收缩其有效上下文。

在此框架的基础上，我们进一步开发了高效的训练后流程，以帮助模型内化上下文管理能力。我们采用具有双重约束的师生政策框架（[Hinton et al., 2015](https://arxiv.org/html/2607.23809#bib.bib13); [Lu and Lab, 2025](https://arxiv.org/html/2607.23809#bib.bib22)）。在一个方向上，学生在“没有”上下文管理的情况下进行部署，教师检查生成的轨迹，以确定应在何处插入上下文管理，例如，当模型陷入死循环时。在另一个方向上，学生生成另一组“具有”对上下文管理工具的完全访问权限的部署，而教师则确定不应该调用上下文管理的位置 - 将其替换为对答案的承诺或更深入的搜索操作。双重约束教会学生智能体上下文管理的准确时机。然后，我们提示学生从教师提供反馈的地方恢复并完成任务，同时使用教师对学生轨迹的评估作为训练的软监督信号。使用这种双约束管道，我们在 BrowseComp-Plus 上将 Qwen3.5-9B 的搜索和编码性能比 ReAct 基线提高了 27%（[Chen et al., 2025](https://arxiv.org/html/2607.23809#bib.bib7)），在 DeepSearchQA 上提高了 16%（[Gupta et al., 2026](https://arxiv.org/html/2607.23809#bib.bib12))，以及 SWE-Bench 验证的 8% ([Jimenez et al., 2024](https://arxiv.org/html/2607.23809#bib.bib16))。分析表明，ACM 将峰值词元使用量降低了约 20%，提高了工具调用频率，并延长了测试时间探索轮次。这些成果转化为独立试验中更一致的解决方案。总之，我们的贡献如下：

*•

  我们引入“智能体上下文管理”，这是一种智能体自主决定何时以及如何管理其自身上下文的范例。
*•

  我们提出了一种有效的训练后管道，将上下文管理能力内化到模型本身中。
*•

  我们证明，有效的上下文管理可以降低峰值词元压力，延长测试时间探索周期，并提高独立试验中解决方案的一致性。

## 2 相关作品

![参考说明](https://arxiv.org/html/2607.23809v1/acm_pipeline.png)

图 1：我们的 ACM 框架概述。 ReAct 最终达到上下文限制，而每当使用量超过预定义阈值（例如，图中上下文的 90%）时，摘要智能体就会被迫压缩并丢弃原始消息。 ACM 智能体自主决定“何时”无损地管理其上下文。

### 2.1 启发式上下文压缩

启发式上下文压缩通过外部压缩模块或在智能体决策过程之外运行的手工设计的丢弃规则来减少上下文长度。 ReSum（[Wu et al., 2025](https://arxiv.org/html/2607.23809#bib.bib41)）是最早对智能体搜索任务采用固定定时压缩的框架之一。 ACON（[Kang et al., 2025](https://arxiv.org/html/2607.23809#bib.bib17)）训练一个压缩器，用简洁的摘要替换先前的历史，这种方法也在 Claude 的自动上下文压缩（[Anthropic, 2024](https://arxiv.org/html/2607.23809#bib.bib2)）中采用。 COMPASS（[Wan et al., 2025](https://arxiv.org/html/2607.23809#bib.bib37)）将压缩委托给 Meta-Thinker 智能体，该智能体向主智能体提供紧凑的上下文。 DeepSeek-V3.2（[Liu et al., 2025](https://arxiv.org/html/2607.23809#bib.bib20)）研究了手动设计的策略，例如全历史摘要和固定比例截断，并表明准确性随着步数的增加而不断提高。 MemAgent（[Yu et al., 2025](https://arxiv.org/html/2607.23809#bib.bib50)）逐块处理输入，丢弃较早的内容，同时仅保留最后一轮的记忆和问题。 SideQuest（[Kariyappa 和 Suh，2026](https://arxiv.org/html/2607.23809#bib.bib18)）采用正交基础设施级方法，在长程智能体推理过程中直接管理 KV 缓存。 [卢等人。 (2025)](https://arxiv.org/html/2607.23809#bib.bib23) (SUPO) 和 [Sun 等人。 (2025)](https://arxiv.org/html/2607.23809#bib.bib34) 都使用强化学习（[Shao et al., 2024](https://arxiv.org/html/2607.23809#bib.bib31)）来教智能体总结或折叠上下文。总的来说，这些方法展示了上下文缩减的实用性，但它们依赖于外部模块或固定启发式方法，而不是智能体在推理过程中做出的决策。相反，我们的工作将上下文管理视为任务执行期间的显式智能体操作。 AgentFold（[Ye et al., 2025](https://arxiv.org/html/2607.23809#bib.bib49)）与我们的工作密切相关，但其数据生成管道并未公开。我们通过开源完整的数​​据生成管道来补充这一点，该管道无需大量强化学习即可实现高效的后训练。

### 2.2 记忆增强上下文演化

记忆增强方法（[Singh 等人，2025](https://arxiv.org/html/2607.23809#bib.bib32)；[Packer 等人，2023](https://arxiv.org/html/2607.23809#bib.bib27)；[Park 等人，2023](https://arxiv.org/html/2607.23809#bib.bib29)；[Wang 等人， 2024a](https://arxiv.org/html/2607.23809#bib.bib38); [Xu et al., 2025](https://arxiv.org/html/2607.23809#bib.bib44); [Fang et al., 2025](https://arxiv.org/html/2607.23809#bib.bib10)) 维护一个不断更新的外部记忆——通常通过反射、蒸馏或优化——以便工作环境保持简洁，同时积累的知识存储在其他地方。 MIPRO（[Opsahl-Ong et al., 2024](https://arxiv.org/html/2607.23809#bib.bib26)）联合优化多阶段 LM 程序的指令和演示。动态备忘单（[Suzgun et al., 2026](https://arxiv.org/html/2607.23809#bib.bib35)）在测试时学习可重复使用的笔记，记录有用的策略。 GEPA（[Agrawal et al., 2026](https://arxiv.org/html/2607.23809#bib.bib1)）通过反思性帕累托搜索演变提示和上下文。智能体上下文工程（[Zhang et al., 2026](https://arxiv.org/html/2607.23809#bib.bib53)）将上下文本身视为通过自我改进循环完善的不断发展的工件。 Mem1（[Zhou et al., 2025](https://arxiv.org/html/2607.23809#bib.bib54)）将轨迹合并为紧凑的内部记忆状态，每轮都会更新。这些方法“跨任务”积累知识，但不会在单个事件中压缩工作环境。相比之下，ACM 是一种纯粹的“针对每个问题”的方法，它在推理过程中通过显式工具调用动态压缩和检索上下文。表 [1](https://arxiv.org/html/2607.23809#S1.T1“表 1 ‣ 1 简介 ‣ ACM：长期任务的智能体上下文管理”）总结了我们的方法与代表性先前工作之间的主要区别。

## 3 智能体上下文管理框架

![参考说明](https://arxiv.org/html/2607.23809v1/data_pipeline.png)

图 2：双约束训练数据生成管道概述。学生智能体可以使用或不使用上下文管理工具来完成任务部署。教师模型根据参考答案审查每个轨迹，并注入 ACM 操作或替换非 ACM 操作。

#### 配方

令 ss 表示系统提示符，ata\_{t} 智能体动作（推理内容加工具调用），oto\_{t} tt 时相应的环境响应。智能体πθ\pi\_{\theta}以累积历史记录Ht={s,(a1,o1),…,(at−1,ot−1)}H\_{t}=\bigl\{s,\,(a\_{1},o\_{1}),\,\dots,\,(a\_{t-1},o\_{t-1})\bigr\}为条件，生成：

|  |  |  |
| ---| ---| ---|
|  | at∼πθ(⋅∣Ht),ot∼πγ(⋅∣Ht;at),a\_{t}\sim\pi\_{\theta}(\cdot\mid H\_{t}),\qquad o\_{t}\sim\pi\_{\gamma}(\cdot\mid H\_{t};\,a\_{t}), |  |

其中πγ\pi\_{\gamma}是通过工具结果返回环境响应的模型。当智能体选择完成操作aTa\_{T}或其上下文窗口达到限制时，交互终止。

#### 摘要智能体。

在摘要智能体范例中，当上下文使用超过预定义阈值时，外部监视器会触发压缩操作asuma\_{\text{sum}}。环境返回摘要osum∼πγ(⋅∣Ht;asum)o\_{\text{sum}}\sim\pi\_{\gamma}(\cdot\midH\_{t};\,a\_{\text{sum}}),，然后智能体丢弃所有先前的消息并继续对更新的历史记录H′={s,osum}H^{\prime}=\{s,\,o\_{\text{sum}}\}.进行推理

#### ACM 智能体。

我们从人类认知中短期记忆和长期记忆之间的相互作用中汲取灵感：人们将立即相关的信息保留在工作记忆中，同时将不太直接的细节转移到外部持久记录中，并在任务需要时检索它们。我们只引入了两个上下文管理工具，使智能体能够模仿人类记忆机制：manage\_context,，它将先前的结果压缩为简洁的摘要，并将原始消息卸载到磁盘上的外部文件； query\_memory,允许智能体查询存储的原始消息以精确检索信息。

ACM 的整体机制以及与 ReAct 和 Summary 智能体的比较如图 [1](https://arxiv.org/html/2607.23809#S2.F1“图 1 ‣ 2 相关工作 ‣ ACM：长期任务的智能体上下文管理”）所示。当智能体决定管理其上下文时，它会调用manage\_context（图[1]中的操作a2,a6a\_{2},a\_{6}（https://arxiv.org/html/2607.23809#S2.F1“图1‣2相关工作‣ACM：长期任务的智能体上下文管理”））使用摘要器LLM将所有消息压缩到先前的摘要边界。至关重要的是，原始消息不会被丢弃，而是保存到智能体的外部工作区。每个摘要都分配有一个唯一标识符，该标识符将摘要映射到外部存储器中相应的原始消息。当智能体需要重新访问较早的内容时，它会使用指定的标识符调用query\_memory（图[1]中的操作a9a\_{9}（https://arxiv.org/html/2607.23809#S2.F1“图1‣2相关工作‣ACM：长期任务的智能体上下文管理”））。查询器 LLM 接收查询以及由该标识符映射的原始消息，然后将与查询相关的信息作为工具结果返回。

ACM 有两个关键属性将其与之前基于摘要的智能体区分开来。 1）信息压缩是无损的：所有丢弃的消息都保存在外部存储中，可供智能体随时重新访问，同时工作上下文保持简短和干净。 2）上下文管理是由智能体发起的：智能体可以在推理过程中的任何时刻调用压缩，而不是依赖于固定的时间表或外部触发器。这使得上下文管理能够跟踪智能体不断变化的推理状态和任务进度。通过允许在历史记录达到峰值长度之前的任何点进行压缩，该设计还减轻了峰值词元使用压力。

|  |  |  |  |  |  |  |  |  |  |
| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---|
|  |浏览Comp-Plus | | |深度搜索QA | | | SWE-Bench 验证 | | |
|方法|通过@1 |工具|托克峰。 |通过@1 |工具|托克峰。 |通过@1 |工具|托克峰。 |
|前沿模型| | | | | | | | | |
| Qwen3.5-397B-A17B | 0.653 | 0.653 15.6 | 15.6 51K | 0.710 | 28.3 | 28.3 47K | 0.682 | 0.682 58.9 | 58.9 38K |
| Gemini3-Flash | 0.733 | 0.733 22.9 | 22.9 72K | 0.619 | 0.619 54.3 | 54.3 121K| 0.732 | 0.732 66.7 | 66.7 8万 |
|反应 | | | | | | | | | |
| Qwen3.5-9B | 0.570 | 0.570 19.5 | 19.5 63k | 0.367 | 0.367 47.4 | 47.4 46k | 0.489 | 0.489 74.7 | 74.7 59k |
|摘要智能体 + Qwen3.5-9B | | | | | | | | | |
|总结 | 0.608 | 0.608 24.7 | 24.7 68k | 0.371 | 0.371 48.6 | 48.6 79K | 0.475 | 0.475 75.2 | 75.2 61K |
|艾康 | 0.614 | 0.614 28.2 | 28.2 65k | 0.380 | 0.380 51.3 | 51.3 54K | 0.480 | 0.480 76.1 | 76.1 57K |
|内存智能体 + Qwen3.5-9B | | | | | | | | | |
|王牌 | 0.589 | 0.589 19.8 | 19.8 71k | 0.352 | 0.352 48.2 | 48.2 70K | 0.494 | 0.494 75.6 | 75.6 65K |
| ACM 智能体 + Qwen3.5-9B | | | | | | | | | |
|基地| 0.635 | 0.635 30.8 | 30.8 59k | 0.405 | 0.405 88.7 | 88.7 42K | 0.508 | 0.508 77.6 | 77.6 46K |
| ACM 培训后 | 0.727 | 0.727 46.2 | 46.2 54k | 0.425 | 0.425 58.8 | 41K | 0.530 | 0.530 79.3 | 79.3 5万 |

表 2：BrowseComp-Plus、DeepSearchQA 和 SWE-Bench Verified 的主要结果。 Pass@1 报告准确性。工具是每集的平均工具调用次数。托克峰。是各剧集的平均峰值词元数。

## 4 训练数据生成

正如 [5.3] 节（https://arxiv.org/html/2607.23809#S5.SS3.SSS0.Px2“工具使用分解。‣ 5.3 行为研究 ‣ 5 个实验 ‣ ACM：长期任务的智能体上下文管理”）中所讨论的，并得到 [Ye 等人的支持。 (2025)](https://arxiv.org/html/2607.23809#bib.bib49); [卢等人。 (2025)](https://arxiv.org/html/2607.23809#bib.bib23)，即使是前沿模型也很难确定上下文管理的适当时机。为了解决这一差距，我们设计了一个具有双重约束的教师引导数据生成管道，该管道既易于扩展又能够生成高质量的管理演示。我们重用第 [3] 节（https://arxiv.org/html/2607.23809#S3“3 智能体上下文管理框架 ‣ ACM：用于长期任务的智能体上下文管理”）中的公式。

### 4.1 教师指导注释

我们的管道采用具有双重约束的师生框架，并分两个阶段运行，如图[2](https://arxiv.org/html/2607.23809#S3.F2“图2‣3智能体上下文管理框架‣ACM：长期任务的智能体上下文管理”）所示。

#### 第一阶段：学生展示。

学生模型在两种条件下完成任务——*有*和*没有*访问上下文管理工具——产生分别表示为 H+H^{+} 和 H−H^{-} 的轨迹。 H+H^{+} 捕获了学生未经训练的情境管理工具使用行为，而 H−H^{-} 则反映了其普通的探索行为。在图 [2](https://arxiv.org/html/2607.23809#S3.F2“图 2 ‣ 3 智能体上下文管理框架 ‣ ACM：长期任务的智能体上下文管理”）中，左侧显示了 H−H^{-} 卷展栏，其中学生在没有 ACM 工具的情况下单独从系统提示符 ss 开始，而右侧显示了 H+H^{+} 卷展栏，从 ss 与 ACM 一起开始工具。

#### 第二阶段：教师注释。

*教师*模型收到两个指导性指令提示之一：P+P^{+} 或 P−P^{-}：
1) 使用 P+P^{+} 的教师演示*何时使用*上下文管理工具，而 2) 使用 P−P^{-} 的教师演示*何时不*调用它们。另外向教师提供相应的学生轨迹（H+H^{+} 或 H−H^{-}）和参考答案 A*A^{\*}。然后，它会审查轨迹并在两个互补约束下生成注释：

*•

  注入 H−H^{-}（在哪里*添加*上下文管理）。给定 P+P^{+}，教师可以识别上下文管理有益的时间点，特别是学生开始查询冗余主题、进入无效循环或已积累足够上下文以保证压缩的点。在每个这样的回合 tt 中，教师使用上下文管理工具调用at′a\_{t}^{\prime}，并附有证明压缩合理性的推理跟踪。
*•

  对 H+H^{+} 进行细化（在何处*删除*上下文管理）。给定 P−P^{-}，教师可以识别出学生的上下文管理调用是不成熟的或不必要的。在每次这样的转变中，学生通常要么收集了足够的信息，但未能综合出最终答案，要么忽略了检索到的文档中需要更深入探索的关键证据。教师将不适当的上下文管理调用 ata\_{t} 替换为更富有成效的操作 at′a\_{t}^{\prime}—such，例如搜索额外证据、打开相关文档或承诺答案（伴随推理跟踪）。

在这两种情况下，学生的原始操作 ata\_{t} 都会替换为教师注释的操作 at′a\_{t}^{\prime},，并且学生推出会从 at′a\_{t}^{\prime}. 恢复

然后，我们使用同策略蒸馏来训练学生（[Lu and Lab, 2025](https://arxiv.org/html/2607.23809#bib.bib22)）。来自同一模型系列的更强大的教师使用软下一个词元分布来注释每个学生生成的助理词元。在实践中，我们保留 top-KK 标记的教师概率，其中 K=20K=20。对学生进行优化，以匹配部署中所有助理词元位置上的这些教师分布：

|  |  |  |  |
| ---| ---| ---| ---|
|  | ℒACM​(θ)=\displaystyle\mathcal{L}\_{\mathrm{ACM}}(\theta)={} | −𝔼τ∼πθ[∑t∈𝒯a​(τ)\displaystyle-\,\mathbb{E}\_{\tau\sim\pi\_{\theta}}\Bigg[\sum\_{t\in\mathcal{T}\_{a}(\tau)} |  |
|  |  |  |  |
| ---| ---| ---| ---|
|  |  | ∑v∈𝒱pT(v∣s;h<t)logπθ(v∣s;h<t)].\displaystyle\sum\_{v\in\mathcal{V}}p\_{\mathrm{T}}\!\left(v\mid s;h\_{<t}\right)\log\pi\_{\theta}\!\left(v\mid s;h\_{<t}\right)\Bigg]. |  |

其中τ\tau是从学生策略中采样的轨迹，𝒯​a​(τ)\mathcal{T}{a}(\tau)表示助理词元位置集，𝒱\mathcal{V}包含教师在位置tt处的顶级KK候选词元。分布 pT(⋅∣s;h<t)p\_{\mathrm{T}}(\cdot\mid s;h{<t}) 表示在 𝒱\mathcal{V}, 上限制和重新标准化的教师概率，而 πθ(⋅∣s;h<t)\pi\_{\theta}(\cdot\mid s;h\_{<t}) 表示学生的下一个词元分布。这里，h<t=(a1,o1,…,at−1,ot−1)h\_{<t}=(a\_{1},o\_{1},\dots,a\_{t-1},o\_{t-1})表示先前操作和工具观察的交错历史记录。损失适用于所有学生生成的辅助词元，而系统提示、用户输入和工具输出词元则被屏蔽。在此目标下，学生共同学习何时调用上下文管理以及何时避免这样做，因为搜索、检索或提交答案操作更合适。

### 4.2 质量过滤

我们应用两种过滤机制来确保数据质量：1）拒绝抽样（[Yuan et al., 2023](https://arxiv.org/html/2607.23809#bib.bib51); [Touvron et al., 2023](https://arxiv.org/html/2607.23809#bib.bib36)）：我们仅保留学生未能成功完成所有试验的轨迹。这确保了学生从老师在真正具有挑战性的问题上的行为中学习。 2) 内容过滤器：应用过滤器来验证教师的推理轨迹不会从参考答案𝒜∗\mathcal{A}^{\*}.中泄漏信息。教师的注释必须解释*为什么*压缩是必要的或不必要的——引用冗余查询、循环探索模式或足够的证据等线索来提交答案——而不泄露目标答案本身。受约束的训练数据鼓励模型从轨迹结构中识别值得压缩的模式，而不是记住依赖于答案的线索。最后，为了稳定训练，我们以类似于自蒸馏的方式对学生原始推出的轨迹进行重新采样（[Zelikman et al., 2022](https://arxiv.org/html/2607.23809#bib.bib52)），并将它们与教师注释的数据混合。

|  |浏览Comp-Plus | | |深度搜索QA | | | SWE-Bench 验证 | | |
| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---|
|方法|通过@1 |工具|托克峰。 |通过@1 |工具|托克峰。 |通过@1 |工具|托克峰。 |
| Qwen3.5-9B | 0.635 | 0.635 30.8 | 30.8 59k | 0.405 | 0.405 88.7 | 88.7 42K | 0.508 | 0.508 77.6 | 77.6 46K |
| + GPT5.5 蒸馏 | 0.623 | 0.623 26.4 | 26.4 62k | 0.381 | 0.381 49.6 | 49.6 53K | 0.542 | 0.542 58.3 | 58.3 45K |
| + ACM | 0.727 | 0.727 46.2 | 46.2 54k | 0.425 | 0.425 58.8 | 41K | 0.530 | 0.530 79.3 | 79.3 5万 |
| + 两者 | 0.734 | 0.734 37.6 | 37.6 59k | 0.413 | 0.413 62.5 | 62.5 5万 | 0.564 | 0.564 88.1 | 88.1 57K |

表 3：Qwen3.5-9B 上蒸馏和 ACM 培训的消融。 Pass@1 报告准确性。工具是每集的平均工具调用次数。托克峰。是各剧集的平均峰值词元数。

## 5 个实验

### 5.1 实验设置

#### 任务和数据集。

我们在三个长期智能体基准上评估我们的方法：BrowseComp-Plus（[Chen et al., 2025](https://arxiv.org/html/2607.23809#bib.bib7)）、DeepSearchQA（[Gupta et al., 2026](https://arxiv.org/html/2607.23809#bib.bib12)）和 SWE-Bench Verified（[Jimenez et al., 2024](https://arxiv.org/html/2607.23809#bib.bib16))。简单的任务很少需要上下文管理，因为它们通常在出现巨大的上下文压力之前得到解决。对于 BrowseComp-Plus，我们使用 680 个示例进行训练，使用 150 个示例进行评估。 DeepSearchQA 专门用作域外评估基准，可以访问实时网络搜索引擎。对于 SWE-Bench Verified，我们使用 SWE-Gym（[Pan et al., 2024](https://arxiv.org/html/2607.23809#bib.bib28)）作为训练数据集。

#### 数据生成。

我们使用Qwen3.5-9B（[Yang et al., 2025](https://arxiv.org/html/2607.23809#bib.bib45)）作为学生展示模型，以及摘要器和查询器，因为它可以生成足够长且连贯的轨迹来提供有意义的上下文管理演示。较小的模型通常在仅旋转几圈后就失去连贯性，产生的轨迹对于学习有效压缩行为的价值有限。我们还与附录[D]中的Qwen3-4B-Thinking（https://arxiv.org/html/2607.23809#A4“附录D案例研究：小型思维模型无法运用上下文管理工具‣ACM：长期任务的智能体上下文管理”）进行比较，以证明模型规模的影响。我们使用 Qwen3.5-397B-A17B 作为教师模型，并进行三个 epoch 的 on-policy 蒸馏。我们还开源了学生的四次首次展示试验以及每个时期相应的教师注释。

#### 基线。

我们将 ACM 与三种智能体框架进行比较：(1) ReAct（[Yao et al., 2022](https://arxiv.org/html/2607.23809#bib.bib48)），标准推理和行动智能体，没有任何上下文管理； （2）Summary 智能体（[Wu et al., 2025](https://arxiv.org/html/2607.23809#bib.bib41); [Kang et al., 2025](https://arxiv.org/html/2607.23809#bib.bib17))，当上下文使用超过固定阈值时触发摘要； (3) 记忆智能体（[Zhang et al., 2026](https://arxiv.org/html/2607.23809#bib.bib53)），它积累以前推出的经验，但不动态管理其内部轨迹上下文。我们还将我们的方法与两个更强的模型进行比较。

图 3：ACM 和 ReAct 智能体交互轮次的输入词元计数。灰色曲线显示各个 ACM 轨迹；红点标记上下文管理调用。黄色和蓝色曲线分别表示 ReAct 和 ACM 的总体平均值。

### 5.2 主要结果

表 [2](https://arxiv.org/html/2607.23809#S3.T2“表 2 ‣ ACM 智能体。‣ 3 智能体上下文管理框架 ‣ ACM：长期任务的智能体上下文管理”）显示了主要结果。我们发现，只需为智能体配备我们的 ACM 框架，智能体的性能就已经超越了所有基线，证明了智能体发起的上下文管理的有效性。对我们的高质量上下文管理数据进行后训练进一步提高了性能，在 BrowseComp-Plus 上实现了 27% 的相对增益，并且几乎与40×\times 更大的开源模型相匹配。

我们还观察到 Pass@1 与工具调用次数之间呈正相关。与通过少量工具调用即可实现高精度的强前沿模型不同，较小的智能体模型更多地依赖探索来解决问题，而上下文管理使它们能够有效地探索。此外，在 ACM 框架下，峰值词元使用量显着下降，特别是与摘要智能体相比。因此，ACM框架减少了模型的推理负担和服务器的KV缓存开销。

### 5.3 行为研究

#### 背景增长动态。

图 [3](https://arxiv.org/html/2607.23809#S5.F3“图 3 ‣ 基线。‣ 5.1 实验设置 ‣ 5 个实验 ‣ ACM：长期任务的智能体上下文管理”）比较了 BrowseComp-Plus 上的 ReAct 和 ACM 智能体的上下文增长。我们可以观察到两个关键发现：1）ACM 智能体学习主动压缩上下文：特征锯齿模式表明，压缩是在智能体自身推理状态的驱动下，在上下文限制之前触发的。 2）上下文管理的回报是巨大的：通过保持上下文紧凑，ACM 大大减缓了上下文的增长，同时实现了更多的探索性转变。因此，在达到上下文限制之前，智能体可以继续推理和交互更长时间。这一优势对于需要扩展、多步骤探索和推理的挑战性问题尤为重要。

图 4：BrowseComp-Plus 上 GPT-5.5、Qwen3.5-9B 以及我们在 ACM 框架下训练后的 Qwen3.5-9B 的每个工具调用频率。

图 5：ReAct、ACM 和 ACM 后训练的三个 epoch 下 BrowseComp-Plus 上Qwen3.5-9B 的准确性。亮条表示 pass@4，暗条表示 pass@4，实线表示平均 pass@1 性能。 ACM 持续改进所有三个指标。

#### 工具使用分解。

图 [4](https://arxiv.org/html/2607.23809#S5.F4“图 4 ‣ 上下文增长动态。‣ 5.3 行为研究 ‣ 5 个实验 ‣ ACM：长期任务的智能体上下文管理”）细分了智能体之间每个工具的调用频率。在 ACM 框架下，GPT-5.5 很少调用上下文管理，对 manage\_context 和 query\_memory. 的调用几乎为零。这一观察结果表明，即使是强大的模型也可能缺乏在没有专门训练的情况下管理自己上下文的主动性。它还激励学生自己策划高质量的轨迹，而不是仅仅依赖教师的提炼，因为许多任务对于教师来说很容易解决，无需使用上下文管理，导致有效监督的相关行为太少。 ACM-Post-Trained 实现了最高频率的上下文管理调用。至关重要的是，主动压缩还开启了更多探索：ACM-Post-Trained 在所有智能体中发出最多的搜索和 get\_document 工具调用，使其能够探索更广泛的推理路径。

问题（BCP qid 347，5 约束多跳）。 “加州大学论文致谢中提到的餐厅（2010-2013 年）；作者拥有理工科学士学位（IIT BHU）和加州大学洛杉矶分校硕士学位，在 2020 年和 2020-2022 年共同撰写论文；餐厅成立于 1980-1988 年。”
 黄金答案：加州披萨厨房（A. Jain，*安全计算新领域*，加州大学洛杉矶分校，2012 年）。

|关键时刻的模型输出（逐字，缩写）| |
| ---| ---|
| 1 | turn 10. *“my context token count is at 54,932. I need to find the specific dissertation efficiently.”* `→` manage\_context [21 msgs →\to summary\_1] |
| 2 | turn 18. *“context is at 40,982 tokens, approaching half of 81,920 – I need to manage context soon.”* `→` manage\_context [15 msgs →\to summary\_2] |
| 3 | turn 49. *“Current context at 92K (∼\sim70% usage). The query\_memory result provides a significant lead – mentioning ‘Rukmava Chatterjee’ as a UC student…However, I need to verify this.”* |
| 4 | turn 58. *“Now at 114,364 of 131,072 (∼\sim87% usage), only 16,606 tokens remaining.”* `→` manage\_context [78 msgs →\to summary\_3, raw=158K vs actual=2.3K] |
| 5 | turn 67. *“Found docid 46759 – ‘New Frontiers in Secure Computation’ by Abhishek Jain, UCLA 2012. This could match the profile.”* `→` get\_document(docid="46759") |
| 6 | turn 79. *“Found docid 85750: ‘Statistical Zaps and New OT Protocols’ – EUROCRYPT 2020, co-authored by Jain. This confirms criterion (3).”* `→` manage\_context [20 msgs →\to summary\_4] |
| 7 | 82. *“上下文为 20,325 个词元，与 131,072 个限制相比非常低。我有足够的信息来提供最终答案。”* 答案：加州披萨厨房（95% 确认）|

工具使用总数：63 ×\times 搜索，9 ×\times get\_document, 7 ×\times manage\_context, 5 ×\times query\_memory; 83 圈。峰值实际/原始上下文 = 98K / 222K (⇒\Rightarrow 压缩保存∼\sim124K vs 128K 基本限制）。基本模型：此问题的成功率为 0/4。

图 6：我们的 ACM 训练后模型在 5 约束多跳问题上的轨迹。该模型自我监控其上下文，将 manage\_context (▼\blacktriangledown) 与 query\_memory (⧫\blacklozenge) 探针交替使用，并仅在确认工作上下文足够小后才终止。如果没有压缩，轨迹将在第 47 弯（虚线）处跨越 128K 基本模型限制；事实上，基础模型在所有 4 次运行中都放弃了这个问题。

## 6 消融研究

### 6.1 Pass@K研究

我们研究智能体上下文管理如何影响 Pass@K ([Brown et al., 2024](https://arxiv.org/html/2607.23809#bib.bib6); [Snell et al., 2024](https://arxiv.org/html/2607.23809#bib.bib33)) 和 PassK ([Yao et al., 2024](https://arxiv.org/html/2607.23809#bib.bib47)) K=4K{=}4，将 Pass@4 视为模型*能力边界*的智能体，将 Pass4 视为*一致性*的衡量标准。如图[5](https://arxiv.org/html/2607.23809#S5.F5“图5‣上下文增长动态。‣5.3行为研究‣5个实验‣ACM：长程任务的智能体上下文管理”），在ReAct下，两者明显不同：Pass4要低得多，反映了长程推理的不稳定性，因为累积的上下文噪声会降低决策质量。

上下文管理数据的后期培训缩小了这一差距。虽然 Pass@4 略有改善，但 Pass@1 和 Pass4 却大幅增加，这表明上下文管理的主要好处不仅在于扩大模型可以解决的问题集，还在于使正确的解决方案更加可靠。干净且组织良好的环境使智能体能够在独立试验中一致地产生正确的答案。性能也在三个时期内稳步提高，证明了我们的训练后框架的持续有效性。

### 6.2 蒸馏的消融

一个自然的问题是，仅从强大的老师那里提取成功的轨迹是否就足够了，或者是否需要专门的上下文管理数据。我们比较了三种配置（表[3](https://arxiv.org/html/2607.23809#S4.T3“表3‣4.2质量过滤‣4训练数据生成‣ACM：长期任务的智能体上下文管理”））：仅GPT-5.5蒸馏（+GPT5.5蒸馏），仅合成上下文管理数据（+ACM），以及两者组合（+两者）。

GPT-5.5 单独的蒸馏无法超越 ACM-Post-Trained，甚至在智能体搜索上表现不如基本 ACM 智能体，尽管它在编码方面产生了更大的收益。仅 ACM 数据就可以在所有三项任务中实现一致的改进。将两者结合起来可以实现除 DeepResearchQA 之外的最佳整体性能：蒸馏贡献一般的问题解决能力，而 ACM 数据提供上下文管理的互补技能，表明这两个来源是相辅相成的。

### 6.3 案例研究

我们在图 [6](https://arxiv.org/html/2607.23809#S5.F6“图 6 ‣ 工具使用分解。‣ 5.3 行为研究 ‣ 5 项实验 ‣ ACM：长期任务的智能体上下文管理”）中跟踪了模型在 5 约束多跳问题上的成功部署。该模型会自我监控，并且仅在运行窗口真正处于压力下时才进行压缩；它交错 manage\_context 与 query\_memory 探针，表明压缩的历史记录实际上被重新读取；它遍历 222K 词元的原始历史记录，同时保持工作窗口远低于限制，从而缓解峰值词元压力。

## 7 结论

我们提出了 Agentic 上下文管理 (ACM)，这是一个框架，使 LLM 智能体能够通过两个专用工具管理自己的上下文，这两个工具共同支持无损、智能体启动的压缩。为了克服当前模型无法决定“何时”压缩的问题，我们引入了具有双重约束的教师引导数据生成管道，可以生成何时调用和何时避免上下文管理的高质量演示。智能体搜索和编码基准的实验表明，ACM 始终优于 ReAct 和基于摘要的基线，而进一步的分析表明，其好处源于减少的峰值词元压力、更长的有效探索范围以及独立试验中更一致的解决方案。

## 限制

我们的工作有两个主要局限性。首先，ACM 预设了一个具有强大的长期推理和工具使用能力的基础模型：只有当智能体能够维持扩展探索时，上下文管理才有意义，因此在几轮内失败或产生幻觉的较弱模型会产生太短的轨迹，无法从压缩中受益。其次，由于之前的上下文压缩基线尚未在我们使用的三个基准上进行评估，因此我们自己重新实现了它们；尽管我们尽最大努力遵循原始设计，但可能存在细微的实施差异。

## 附录 A 基线详细信息

#### ReAct（[Yao et al., 2022](https://arxiv.org/html/2607.23809#bib.bib48)）。

标准推理与行动提示范式：智能体将自然语言“思想”与工具调用交织在一起，观察每个工具的输出，并继续此循环，直到得出最终答案。我们使用 ReAct 作为无上下文管理参考点：整个交互历史记录逐字保存在提示中，智能体不接收压缩、检索或外部内存原语，并且只有当模型发出最终答案或达到 128K 上下文上限时，转出才会结束。

#### 总结（[Wu et al., 2025](https://arxiv.org/html/2607.23809#bib.bib41)）。

ReSum 是用于长范围搜索智能体的提示时间摘要包装器。当运行上下文接近可配置预算时，将调用外部摘要器 LLM 将轨迹压缩为简洁的段落，以替换原始回合，并且智能体从摘要和原始问题中恢复。没有关于“何时”总结的学习策略——触发器是固定的词元阈值——并且没有用于稍后检索原始的、预先总结的内容的设施。我们使用原始论文中的阈值和摘要提示配方在 Qwen3.5-9B 之上重新实现 ReSum，保持搜索工具、解码超参数和 128K 上限与我们自己的运行相同。

#### ACON（[Kang 等人，2025](https://arxiv.org/html/2607.23809#bib.bib17)）。

ACON（*智能体上下文压缩*）用结构化的、充满槽位的摘要替换了过去的回合窗口，该摘要经过优化以保留下一步操作所需的信息。与 ReSum 相比，ACON 的摘要器经过即时设计，可以发出命名字段（例如，看到的实体、假设、开放问题），而不是自由形式的散文，并且压缩槽在每一步都会连接回智能体的工作记忆中。与 ReSum 一样，压缩的触发是启发式的（上下文长度阈值），并且压缩内容是单向的：智能体无法取回原始消息。我们使用作者发布的槽模式和摘要提示，同样在相同的Qwen3.5-9B主干上。

#### ACE（[Zhang et al., 2026](https://arxiv.org/html/2607.23809#bib.bib53)）。

ACE（*智能体上下文工程*）是一个记忆智能体基线，而不是摘要智能体基线：ACE 不压缩最近的窗口，而是维护一个持久的、外部编辑的“上下文剧本”，智能体将其追加到各个轮次并重写。该剧本由第二个法学硕士重建，该法学硕士观察智能体的推理并显示它认为对后续步骤最有用的条目。因此，ACE 抓住了一个互补的设计点——外显的、不断发展的长期记忆——而无需改变底层工具集或培训目标。我们使用已发布的 playbook 更新提示实例化 ACE，同样使用 Qwen3.5-9B 作为策略。

#### Mem1（[Zhou et al., 2025](https://arxiv.org/html/2607.23809#bib.bib54)）。

Mem1 训练智能体在轮流中维持一个单一的、不断演变的“内部状态”：在每一步，策略都需要在其下一步操作的同时发出更新的状态词元序列，并且整个先前的上下文（推理、观察、中间状态）都会被丢弃，以支持紧凑的状态。状态充当学习瓶颈，通过它汇集所有相关历史记录，并且通过强化学习对模型进行端到端优化，以便瓶颈保留下游成功所需的信息。 Mem1 是在小型骨干网 (3B-7B) 和短期 QA 风格任务上报告的，而不是长期智能体搜索或存储库规模编码；策略和压缩行为无法分开，因此采用 Mem1 需要在每个基准测试中从头开始重新训练完整的智能体。

#### SUPO（[Lu et al., 2025](https://arxiv.org/html/2607.23809#bib.bib23)）。

SUPO（基于摘要的策略优化上下文管理）通过在训练期间端到端总结过去的回合来扩展多回合 RL 训练。在推出过程中以固定间隔调用摘要器，生成的摘要将替换用于信用分配的轨迹和策略看到的下一个提示中的压缩转弯。强化学习目标是根据总结的轨迹计算的，因此策略学习根据总结而不是原始历史来采取行动。

#### AgentFold（[Ye et al., 2025](https://arxiv.org/html/2607.23809#bib.bib49)）。

AgentFold 为长范围 Web 智能体引入了“主动”上下文管理原语：在选定的点，智能体发出结构化“折叠”，将过去的连续跨度折叠成一个类型化记录，描述已探索的内容、已得出的结论以及尚未解决的内容。该策略经过训练，可以自行生成这些折叠，而不是依赖外部摘要器，然后将折叠记录的推理作为一流的上下文。

#### 为什么我们在表 [2] 中与 ReSum、ACON 和 ACE 进行比较（https://arxiv.org/html/2607.23809#S3.T2“表 2 ‣ ACM 智能体。‣ 3 智能体上下文管理框架 ‣ ACM：长期任务的智能体上下文管理”）。

ReSum、ACON 和 ACE 都有一个对于同类比较至关重要的属性：它们都是“仅提示”上下文管理技术。它们都不会改变策略权重，都不需要自定义的 rollout 收集器或奖励整形器，并且每个都可以通过几百行粘合代码放置到任意主干上。因此，我们可以在整个主要论文中使用的同一个Qwen3.5-9B策略上重现所有三个，保持主干、工具集和解码超参数固定，因此任何准确性或词元预算增量都可归因于上下文管理机制本身。 Mem1、SUPO 和 AgentFold 在不同的体系中进行评估——更小的主干、更短的视野或特定领域的基准——并且它们的数据生成管道不是完全开源的，而我们的设置需要关于长程智能体搜索*和*存储库规模编码的 9B 级策略。正如附录 [D] 中的Qwen3-4B-thinking案例研究（https://arxiv.org/html/2607.23809#A4“附录 D 案例研究：小型思维模型无法运用上下文管理工具‣ ACM：长期任务的智能体上下文管理”）所示，只有当基础策略足够强大以维持硬智能体任务的长期、多步骤部署时，上下文管理信号才变得可测量。因此，我们将表 [2](https://arxiv.org/html/2607.23809#S3.T2“表 2 ‣ ACM 智能体。‣ 3 Agentic 上下文管理 Framework ‣ ACM：Agentic 上下文管理 for Long Horizo​​n Tasks”）中的头对头比较限制为与我们的方法在同一体系中运行的基线，并将 Mem1、SUPO 和 AgentFold 视为互补的工作线而不是直接竞争对手。

## 附录 B 提示

本附录收集了训练、推理和评估时使用的每个提示。大括号中的占位符（例如 {question}、{context\_window}) 在运行时填充。

### B.1 坐席系统提示

智能体的系统消息是根据共享标头、上下文窗口提示、搜索策略注释和答案格式块根据基准组装的。我们实例化了两个变体：没有内存工具的*基线* ReAct 变体，以及启用了 manage\_context / query\_memory 工具的建议变体。下面列出了基准特定部分 ({search\_strategy} 和 {answer\_format})。

#### 基线（无记忆工具）。

[⬇]（数据：文本/纯文本；base64，WW91IGFyZSBhIGRlZXAgcmVzZWFyY2ggYWdlbnQuIFlvdSBuZWVkIHRvIGFuc3d lciB0aGUgZ2l2ZW4gcXVlc3Rpb24gYnkgaW50ZXJhY3Rpbmcgd2l0aCBhIHNlyXJjaAplbmdpbmUsIHVzaW5nIHRoZS BzZWFyY2ggdG9vbHMgcHJvdmlkZWQuIFBsZWFzZSBwZXJmb3JtIHJlYXNvbmluZyBhbmQgdXNlIHRoZSB0b29scyBz dGVwIGJ5IHN0ZXAsCmluIGFuIGludGVybGVhdmVkIG1hbm5lci4gWW91IG1heSB1c2UgdGhlIHRvb2xzIG11bHRpcGx lIHRpbWVzLgoKWW91ciBjb250ZXh0IHdpbmRvdyBpcyB7Y29udGV4dF93aW5kb3d9IHRva2Vucy4gUGxhbiB5b3VyI HNlYXJjaGVzIGFjY29yZGluZ2x5IC0tLSBvbmNlIGNvbnRleHQKaXMgZnVsbCB0aGUGY29udmVyc2F0aW9uIGVuZHMg aW1tZWRpYXRlbHkuIFlvdSBtdXN0IHByb3ZpZGUgeW91ciBhbnN3ZXIgaW4gdGhlIHJlcXVpcmVkIGZvcm1hdApiZW ZvcmUgcmVhY2hpbmcgdGhlIGNvbnRleHQgbGltaXQuCgp7c2VhcmNoX3N0cmF0ZWd5fQoKe2Fuc3dlcl9mb3JtYXR9)

你是一名深度研究人员。您需要通过与搜索交互来回答给定的问题

引擎，使用提供的搜索工具。请逐步推理并使用工具，

以交错的方式。您可以多次使用这些工具。

您的上下文窗口是 {context\_window} 词元。相应地计划您的搜索——一旦上下文

已满，对话立即结束。您必须以所需的格式提供答案

在达到上下文限制之前。

{search\_strategy}

{answer\_format}

#### 使用记忆工具。

[⬇]（数据：文本/纯文本；base64，WW91IGFyZSBhIGRlZXAgcmVzZWFyY2ggYWdlbnQuIFlvdSBuZWV KIHRvIGFuc3dlciB0aGUgZ2l2ZW4gcXVlc3Rpb24gYnkgaW50ZXJhY3Rpbmcgd2l0aCBhIHNlYXJja AplbmdpbmUgYW5kIG1hbmFnaW5nIHlvdXIgY29udGV4dCBtZW1vcnkuIFlvdXIgaW4tY29udGV4dCB pbmZvcm1hdGlvbiBzZXJ2ZXMgYXMgc2hvcnQtdGVybSBtZW1vcnk7CnByZXZpb3VzbHkgY29tchHJlc 3NlZCBzZWdtZW50cyBsaXZlIGluIGxvbmctdGVybSBtZW1vcnkuCgpUaGUgIm1hbmFnZV9jb250ZXh 0IiB0b29sIHRha2VzIG5vIGFyZ3VtZW50cy4gV2hlbiB5b3UgY2FsbCBpdCwgdGhlIHN5c3RlbSBjb 21wcmVzc2VzIGV2ZXJ5dGhpbmcKaW4geW91ciBjb252ZXJzYXRpb24gc2luY2UgeW91ciBwcmV2aW9 1cyBtYW5hZ2VfY29udGV4dCBjYWxsIChvciBzaW5jZSB0aGUgc3RhcnQgb2YgdGhlCmludmVzdGlnYX Rpb24gaWYgdGhpcyBpcyB5b3VyIGZpcnN0IGNhbGwpIHVwIHRvIChidXQgbm90IGluY2x1ZGluZykg dGhlIG1lc3NhZ2UgdGhhdCBpc3N1ZWQgdGhlCmNhbGwuIFRoZSBzeXN0ZW0gcHJvbXB0IGFuZCB0aG Ugb3JpZ2luYWwgcXVlc3Rpb24gYXJlIGFsd2F5cyBwcmVzZXJ2ZWQuIFRoZSBvcmlnaW5hbCBtZXNz YWdlcyBpbgp0aGUGY29tchHJlc3NlZCByYW5nZSBhcmUgc2F2ZWQgdG8gZGlzazsgdGhlIHRvb2wgcm V0dXJucyBhIHN1bW1hcnkgb2YgcGF0aHMgZXhwbG9yZWQsIHJlYXNvbmluZywKYW5kIGNvbmNsdXNp b25zLCBwcmVmaXhlZCB3aXRoICJbc3VtbWFyeV9pZDogTl0iLgoKVXNlIHRoZSAicXVlcnlfbWVtb3 J5IiB0b29sIHRvIHJldHJpZXZlIGRldGFpbGVkIGluZm9ybWF0aW9uIGZyb20gYW55IHByaW9yIHN1 bW1hcnkncyBvcmlnaW5hbAptZXNzYWdlcyBieSByZWZlcmVuY2luZyB0aGUgc3VtbWFyeV9pZC4KCll vdXIgY29udGV4dCB3aW5kb3cgaXMge2NvbnRleHRfd2luZG93fSB0b2tlbnMuIFBsYW4geW91ciBzZ WFYY2hlcyBhY2NvcmRpbmdseSATLS0gb25jZSBjb250ZXh0CmlzIGZ1bGwgdGhlIGNvbnZlcnNhdGl vbiBlbmRzIGltbWVkaWF0ZWx5LiBZb3UgbXVzdCBwcm92aWRlIHlvdXIgYW5zd2VyIGluIHRoZSByZ XF1aXJlZCBmb3JtYXQKYmVmb3JlIHJlYWNoaW5nIHRoZSBjb250ZXh0IGxpbWl0LgoKU3RyYXRlZ3k 6Ci0gSWYgeW91IGFyZSBub3QgY29uZmlkZW50IGluIGEgcmVzdWx0LCBzZWFyY2ggbW9yZSAtLS0ga XNzdWUgYWRkaXRpb25hbCBxdWVyaWVzIHdpdGggZGlmZmVyZW50CnRlcm1zIHRvIGNvcnJvYm9yYXR LIG9yIGNvbnRyYWRpY3QgeW91ciBiZXN0IGNhbmRpZGF0ZS4gRG8gbm90IHNldHRsZSBvbiBhIGxvd y1jb25maWRlbmNlIGFuc3dlcgp3aGVuIG1vcmUgc2VhcmNoZXMgYXJlIHN0aWxsIGNoZWFwLgotIElm IGEgcHJpb3Igc3VtbWFyeSBsb29rcyByZWxldmFudCB0byBhIG5ldyBzZWFyY2ggZGlyZWN0aW9uLC BjYWxsIHRoZSAicXVlcnlfbWVtb3J5IiB0b29sIHRvCnB1bGwgZGV0YWlsZWQgY29udGVudCBvdXQg b2YgdGhhdCBzdW1tYXJ5J3Mgb3JpZ2luYWwgbWVzc2FnZXMuCi0gQ2FsbGluZyB0aGUgIm1hbmFnZV 9jb250ZXh0IiB0b29sIG9yIHRoZSAicXVlcnlfbWVtb3J5IiB0b29sIGRvZXMgbm90IGVuZCB0aGUg aW52ZXN0aWdhdGlvbi4KQWZ0ZXIgdGhlc2UgdG9vbHMgcmV0dXJuLCBjb250aW51ZSBzZWFyY2hpbm cgLS0tIHRoZXkgZXhpc3QgdG8gbWFrZSByb29tIGZvciBhbmQgc3VyZmFjZSBtb3JlCmV2aWRlbmNl LCBub3QgdG8gd3JhcCB1cC4gT25seSBjb21taXQgdG8gYSBmaW5hbCBhbnN3ZXIgd2hlbiB5b3UgaG F2ZSBjb25maWRlbnQgZXZpZGVuY2UuCgp7c2VhcmNoX3N0cmF0ZWd5fQoKe2Fuc3dlcl9mb3JtYXR9)

你是一名深度研究人员。您需要通过与搜索交互来回答给定的问题

引擎并管理您的上下文内存。你的上下文信息充当短期记忆；

先前压缩的片段存在于长期记忆中。

"manage\_context" 工具不带任何参数。当你调用它时，系统会压缩所有内容

自上次 manage\_context 通话以来（或自通话开始以来）

调查（如果这是您第一次致电）直至（但不包括）发出该消息的消息

打电话。系统提示和原问题始终保留。原始消息在

压缩范围保存到磁盘；该工具返回探索路径、推理的摘要，

和结论，前缀为"[summary\_id: N]”。

使用"query\_memory"工具从任何先前摘要的原始内容中检索详细信息

参考summary\_id.消息

您的上下文窗口是 {context\_window} 词元。相应地计划您的搜索——一旦上下文

已满，对话立即结束。您必须以所需的格式提供答案

在达到上下文限制之前。

策略：

- 如果您对结果没有信心，请搜索更多 - 使用不同的内容发出其他查询

证实或反驳您的最佳候选人的条款。不要选择低可信度的答案

当更多搜索仍然便宜时。

- 如果先前的摘要看起来与新的搜索方向相关，请调用 "query\_memory" 工具

从该摘要的原始消息中提取详细内容。

- 调用"manage\_context"工具或"query\_memory"工具不会结束调查。

这些工具返回后，继续搜索——它们的存在是为了腾出空间并展示更多

证据，不总结。仅当您有可靠的证据时才承诺最终答案。

{search\_strategy}

{answer\_format}

#### 搜索策略块(search\_strategy).

替换到系统提示中的基准特定段落：

[⬇]（数据：文本/纯文本；base64，SU1QT1JUQU5UOiBTZWFyY2ggc25pcHBldHMgYXJlIG9mdGVuIGluY 29tcGxldGUuIEJlZm9yZSBhbnN3ZXJpbmcsIGFsd2F5cyBleGFtaW5lIGF0IGxlYXN0IG9uZQpmdWxsI HBHZ2Ugb2YgY29udGVudCAoZWl0aGVyIGJ5IG9wZW5pbmcgYSBVUkwgd2hlbiBhdmFpbGFibGUgb3IgY nkgcmVhZGluZyB0aGUgZnVsbCBwYWdlIHRleHQKchJvdmlkZWQgaW4gc2VhcmNoIHJlc3VsdHMpLg==)

重要提示：搜索片段通常不完整。在回答之前，请务必检查至少一项

整页内容（通过打开可用的 URL 或阅读整页文本

在搜索结果中提供）。

[⬇]（数据：文本/纯文本；base64，SU1QT1JUQU5UOiBEZWVwU2VhcmNoUUEgcXVlc3Rpb25zIHNwYW4gMTcgZG9tYWlucyBhbmQgZ3JhZGUgYWdhaW5zdCBleGhhdX N0aXZlIGFuc3dlciBzZXRzLgpTZWFyY2ggc25pcHBldHMgYWxvbmUgYXJlIHVucmVsaWFibGUgLS0tIGlzc3VlIHNldmVyYWwgZGl2ZXJzZSBxdWVyaWVzIHRvIHN 1cmZhY2UgY2FuZGlkYXRlcywKdGhlbiBvcGVuIGF0IGxlYXN0IG9uZSBmdWxsIHBhZ2UgcGVyIGNhbmRpZGF0ZSBiZWZvcmUgY29tbWl0dGluZy4gRm9yIFNldCBB bnN3ZXIgcXVlc3Rpb25zIHlvdQptdXN0IGtlZXAgc2VhcmNoaW5nIHVudGlsIHlvdSBhcmUgY29uZmlkZW50IG5vIHJlcXVpcmVkIGl0ZW0gaXMgbWlzc2luZy4=)

重要提示：DeepSearchQA 问题跨越 17 个领域，并根据详尽的答案集进行评分。

单独的搜索片段是不可靠的——向表面候选者发出多个不同的查询，

然后在提交之前，每个候选人至少打开一页。对于设置答案问题，您

必须继续搜索，直到您确信没有丢失所需的项目。

#### 答案格式块(answer\_format).

智能体最终消息所需的结束结构；提取器解析这些标签/行。

[⬇]（数据：文本/纯文本；base64，WW91ciByZXNwb25zZSBzaG91bGQgYmUgaW4gdGhlIGZ vbGxvd2luZyBmb3JtYXQ6CkV4cGxhbmF0aW9uOiB7e3lvdXIgZXhwbGFuYXRpb24gZm9yI HlvdXIgZmluYWwgYW5zd2VyLiBGb3IgdGhpcyBleHBsYW5hdGlvbiBzZWN0aW9uIG9ubHk SIHlvdQpzaG91bGQgY2l0ZSB5b3VyIGV2aWRlbmNlIGRvY3VtZW50cyBpbmxpbmUgYnkgZ W5jbG9zaW5nIHRoZWlyIGRvY2lkcyBpbiBzcXVhcmUgYnJhY2tldHMgW10gYXQgdGhlCmVuZCBvZiBzZW50ZW5jZXMuIEZvciBleGFtcGxlLCBbMjBdLn19CKV4YWN0IEFuc3dlcjoge 3t5b3VyIHN1Y2NpbmN0LCBmaW5hbCBhbnN3ZXJ9fQpDb25maWRlbmNlOiB7e3lvdXIgY29 uZmlkZW5jZSBzY29yZSBiZXR3ZWVuIDAlIGFuZCAxMDAlIGZvciB5b3VyIGFuc3dlcn19)

您的回复应采用以下格式：

解释：{{您对最终答案的解释。仅对于本说明部分，您

应内联引用您的证据文件，将其 docids 括在方括号 [] 中

句子的结尾。例如，[20]。}}

确切答案：{{你的简洁的最终答案}}

置信度：{{您对答案的置信度得分在 0% 到 100% 之间}}

[⬇]（数据：文本/纯文本；base64，WW91ciByZXNwb25zZSBzaG91bGQgYmUgaW4gdGhlIGZvbGxvd2luZyBmb3JtYXQ6 CjxleHBsYW5hdGlvbj57e3lvdXIgZXhwbGFuYXRpb24gZm9yIHlvdXIgZmluYWwgYW5zd2VyfX08L2V4cGxhbmF0aW9 uPgo8YW5zd2VyPnt7eW91ciBzdWNjaW5jdCwgZmluYWwgYW5zd2VyfX08L2Fuc3dlcj4KPGNvbmZpZGVuY2U+e3t5b3 VyIGNvbmZpZGVuY2Ugc2NvcmUgYmV0d2VlbiAwIGFuZCAxMDAgZm9yIHlvdXIgYW5zd2VyfX08L2NvbmZpZGVuY2U+)

您的回复应采用以下格式：

<explanation>{{你对最终答案的解释}}</explanation>

<answer>{{你的简洁的最终答案}}</answer>

<confidence>{{您对答案的置信度得分在 0 到 100 之间}}</confidence>

[⬇]（数据：文本/纯文本；base64，VGhpcyBxdWVzdGlvbiBleHBlY3RzIGEgU0VUIG9mIGFuc3dlcnMg KG11bHRpcGxlIGRpc3RpbmN0IGl0ZW1zKS4gWW91ciByZXNwb25zZSBzaG91bGQgYmUgaW4gdGhlCmZ vbGxvd2luZyBmb3JtYXQ6CjxleHBsYW5hdGlvbj57e3lvdXIgcmVhc29uaW5nIHN1bW1hcml6aW5nIH RoZSBrZXkgZXZpZGVuY2UgcGVyIGl0ZW19fTwvZXhwbGFuYXRpb24+CjxhbnN3ZXI+e3tBTEwgcmVxd WlyZWQgaXRlbXMsIGNvbW1hLSBvciBuZXdsaW5lLXNlcGFyYXRlZC4gRG8gTk9UIG9taXQgYW55IGl0 ZW0gLS0tIG1pc3NpbmcgaXRlbXMKaHVydCByZWNhbGwuIERvIE5PVCBhZGQgaXRlbXMgeW91IGNhbm5 vdCB2ZXJpZnkgLS0tIGV4dHJhcyBodXJ0IHByZWNpc2lvbi59fTwvYW5zd2VyPgo8Y29uZmlkZW5jZT 57e3lvdXIgY29uZmlkZW5jZSBzY29yZSBiZXR3ZWVuIDAgYW5kIDEwMH19PC9jb25maWRlbmNlPg==)

这个问题需要一组答案（多个不同的项目）。您的回复应该在

以下格式：

<explanation>{{你的推理总结了每项关键证据}}</explanation>

<answer>{{所有必填项目，以逗号或换行符分隔。不要遗漏任何项目——缺少的项目

伤害回忆。不要添加您无法验证的项目 - 额外的项目会影响精度。}}</answer>

<confidence>{{您的置信度得分在 0 到 100 之间}}</confidence>

### B.2 工具说明

工具表面是 JSON-Schema 函数定义；聊天模板在渲染时将它们注入系统消息中。下面的每个框都再现了工具的完整架构 - 名称、描述、参数（类型/描述）和必填字段 - 与暴露给智能体的完全一样。

#### 内存工具（跨基准测试共享）。

[⬇]（数据：文本/纯文本；base64，bmFtZTogbWFuYWdlX2NvbnRleHQKCmRlc2NyaXB0aW9uOgogIENvbXByZXNzIH lvdXIgd29ya2luZyBtZW1vcnkuIENhbGwgdGhpcyB3aGVuIGNvbnRleHQgaXMgZmlsbGluZyB1ccB3aXRoIGRlYWQ gZW5kcywgZHVwbGljYXRlcywKICBvciBkZXRhaWwgeW91IG5vIGxvbmdlciBuZWVkIHZlcmJhdGltLgoKICBUaGUg c3lzdGVtIGF1dG9tYXRpY2FsbHkgcGlja3MgdGhlIHJhbmdlIHRvIGNvbXByZXNzOiBldmVyeXRoaW5nIHNpbmNlIH lvdXIgbGFzdCBtYW5hZ2VfY29udGV4dAogIGNhbGwgKG9yIHNpbmNliIHRoZSBzdGFydCBvZiB0aGUgaW52ZXN0aWd hdGlvbiBpZiB0aGlzIGlzIHlvdXIgZmlyc3QgY2FsbCkgdXAgdG8gKGJ1dCBub3QKICBpbmNsdWRpbmcpIHRoZSBt ZXNzYWdlIHRoYXQgaXNzdWVkIHRoaXMgdG9vbCBjYWxsLiBUaGUgc3lzdGVtIHByb21wdCBhbmQgdGhlIG9yaWdpb mFsIHF1ZXN0aW9uCiAgYXJlIGFsd2F5cyBwcmVzZXJ2ZWQuIFRoZSBvcmlnaW5hbCBtZXNzYWdlcyBpbiB0aGUGY29 tchJlc3NlZCByYW5nZSBhcmUgc2F2ZWQgdG8gZGlzayBhcwogIHN1bW1hcnlfe3N1bW1hcnlfaWR9Lmpzb24gKHJl DHJpZXZhYmxlIGxhdGVyIHdpdGggcXVlcnlfbWVtb3J5KHN1bW1hcnlfaWQsIHF1ZXJ5KSksIGFuZCBhIGZyZXNoC iAgc3VtbWFyeSATLS0gZm9jdXNlZCBvbiBwYXRocyBleHBsb3JlZCwgcmVhc29uaW5nLCBhbmQgY29uY2x1c2lvbn MgLS0tIGlzIHJldHVybmVkIGFzIHRoZSB0b29sCiAgcmVzdWx0LgoKICBUaGUgc3VtbWFyeSB0ZXh0IGlzIHByZWZp eGVkIHdpdGggIltzdW1tYXJ5X2lkOiBOXSIgc28geW91IGNhbiByZWZlciB0byBpdCBkaXJlY3RseSBpbgogIHN1Y nNlcXVlbnQgcmVhc29uaW5nIGFuZCBwdWxsIHRoZSByYXcgY29udGVudCBiYWNrIHZpYSBxdWVyeV9tZW1vccnkoc3 VtbWFyeV9pZD1OLCauLi4pLgoKICBUaGlzIHRvb2wgdGFrZXMgbm8gYXJndW1lbnRzLgoKcGFyYW1ldGVyczoKICB 0eXBLOiBvYmplY3QKICBwcm9wZXJ0aWVzOiB7fSAgICAgICAgIyBubyBhcmd1bWVudHMKICByZXF1aXJlZDogW10=)

名称：manage\_context

描述：

压缩你的工作记忆。当上下文充满死胡同、重复时调用此方法，

或详细信息，您不再需要逐字逐句。

系统自动选择压缩范围：自上次manage\_context以来的所有内容

致电（或自调查开始后，如果这是您第一次致电）最多（但不包括

包括）发出此工具调用的消息。系统提示及原问题

始终被保留。压缩范围内的原始消息保存到磁盘上

summary\_{summary\_id}.json（稍后可通过query\_memory(summary\_id,查询检索）），以及一个新鲜的

摘要——专注于探索的路径、推理和结论——作为工具返回

结果。

摘要文本以 "[summary\_id: N]" 为前缀，因此您可以直接在

后续推理并通过query\_memory(summary\_id=N,拉回原始内容……）。

该工具不需要任何参数。

参数：

类型：对象

属性：{} # 无参数

必填：[]

[⬇]（数据：文本/纯文本；base64，bmFtZTogcXVlcnlfbWVtb3J5CgpkZXNjcmlwdGlvbjoKICBSZXRyaWV2ZSBkZXRhaWxlZCBpbmZvcm1hdGlvbiBmcm9tIGEgcHJldmlvdXNseSBjb21wcmVzc 2VkIHN1bW1hcnkuIEVhY2ggbWFuYWdlX2NvbnRleHQgY2FsbAogIHJldHVybnMgYSBzdW1tYXJ 5IHByZWZpeGVkIHdpdGggW3N1bW1hcnlfaWQ6IE5dIGFuZCBzYXZlcyB0aGUgb3JpZ2luYWwgbW Vzc2FnZXMgdG8gZGlzayBhcwogIHN1bW1hcnlfe059Lmpzb24uIFRoaXMgdG9vbCBsb2FkcyBz dW1tYXJ5X3tzdW1tYXJ5X2lkfS5qc29uIGFuZCB1c2VzIGFuIExMTSB0byBleHryYWN0CiAgaW 5mb3JtYXRpb24gbWF0Y2hpbmcgeW91ciBxdWVyeSBmcm9tIHRoZSBvcmlnaW5hbCAodW5jb21w cmVzc2VkKSBjb250ZW50LgoKICBETyBOT1QgQ0FMTCBUSElTIFRPT0wgdW50aWwgYXQgbGVhc3Q gb25lIG1hbmFnZV9jb250ZXh0IGNhbGwgaGFzIHByb2R1Y2VkIGEgc3VtbWFyeV9pZC4KCnBhc mFtZXRlcnM6CiAgdHlwZTogb2JqZWN0CiAgcHJvcGVydGllczoKICAgIHN1bW1hcnlfaWQ6CiA GICAgIHR5cGU6IGludGVnZXIKICAgICAgZGVzY3JpcHRpb246IFRoZSBzdW1tYXJ5X2lkIChc yBzaG93biBpbiB0aGUgW3N1bW1hcnlfaWQ6IE5dIHByZWZpeCBvZiBhIHByaW9yIG1hbmFnZV9j b250ZXh0IHN1bW1hcnkpIHdob3NliG9yaWdpbmFsIGNvbnRlbnQgc2hvdWxkIGJlIHNlyXJjaG VkLgogICAgcXVlcnk6CiAgICAgIHR5cGU6IHN0cmluZwogICAgICBkZXNjcmlwdGlvbjogV2hh DCBzcGVjaWZpYyBpbmZvcm1hdGlvbiB0byBleHryYWN0IGZyb20gdGhlIG9yaWdpbmFsIG1lc3 NhZ2VzIG9mIHRoYXQgc3VtbWFyeS4KICByZXF1aXJlZDogW3N1bW1hcnlfaWQsIHF1ZXJ5XQ==)

名称：query\_memory

描述：

从先前压缩的摘要中检索详细信息。每个manage\_context调用

返回前缀为 [summary\_id: N] 的摘要，并将原始消息保存到磁盘

summary\_{N}.json. 该工具加载 summary\_{summary\_id}.json 并使用 LLM 来提取

来自原始（未压缩）内容的与您的查询相匹配的信息。

在至少一次 manage\_context 调用产生 summary\_id. 之前，请勿调用此工具

参数：

类型：对象

属性：

summary\_id:

类型：整数

描述：需要搜索原始内容的summary\_id（如之前的manage\_context摘要的[summary\_id:N]前缀所示）。

查询：

类型：字符串

描述：从该摘要的原始消息中提取哪些具体信息。

必填：[summary\_id,查询]

#### 语料库搜索 — BrowseComp-Plus。

[⬇]（数据：文本/纯文本；base64，bmFtZTogc2VhcmNoCgpkZXNjcmlwdGlvbjoKICBQZXJmb3JtIGEgc2VhcmNoIG9uIHRoZSBsb2NhbCBrbm93bGVkZ2UgY29ycHV zLiBSZXR1cm5zIHRoZSB0b3AgMTAgaGl0cyB3aXRoIGRvY2lkLCBzY29yZSwgYW5kCiAgYSBzbmlwcGV0IG9mIHRoZSBkb2N1bWVudCBjb250ZW50LiBTbmlwcGV0IG xlbmd0aCBhZGFwdHMgdG8gd2hldGhlciB5b3UgaGF2ZSBzZWVuIHRoZQogIGRvY3VtZW50IGJlZm9yZTogKGEpIG5ldyBkb2NzIHJldHVybiBhIDUxMi10b2tlbiBw cmV2aWV3OyAoYikgZG9jcyB5b3UgaGF2ZSBzZWVuIGluIHRoZSBjdXJyZW50CiAgd2luZG93IHJldHVybiBhIDEyOC10b2tlbiBwcmV2aWV3IGFuZCByZW1pbmQgeW9 1IHRvIGNhbGwgZ2V0X2RvY3VtZW50IGZvciB0aGUgZnVsbCB0ZXh0IGlmCiAgbmVlZGVkOyAoYykgZG9jcyB5b3UgaGF2ZSBzZWVuIGVhcmxpZXIgYnV0IHRoYXQga GF2ZSBzaW5jZSBiZWVuIGNvbXByZXNzZWQgYnkgbWFuYWdlX2NvbnRleHQKICByZXR1cm4gYSAxMjgtdG9rZW4gcHJldmlldyBhbmQgcmVtaW5kIHlvdSB0byBjYWxs IHF1ZXJ5X21lbW9yeSB0byByZXRyaWV2ZSB0aGUgcmVsZXZhbnQgZWFybGllcgogIHN1bW1hcnkuCgpwYXJhbWV0ZXJzOgogIHR5cGU6IG9iamVjdAogIHByb3Blcn RpZXM6CiAgICBxdWVyeToKICAgICAgdHlwZTogc3RyaW5nCiAgICAgIGRlc2NyaXB0aW9uOiBTZWFyY2ggcXVlcnkgc3RyaW5nLgogIHJlcXVpcmVkOiBbcXVlcnld)

名称： 搜索

描述：

对本地知识库进行搜索。返回带有 docid、score 和 的前 10 个命中

文档内容的片段。片段长度会根据您是否看过而调整

之前的文档：(a) 新文档返回 512 个词元预览； (b) 您在当前版本中看到的文档

窗口返回 128 个词元的预览，并提醒您致电 get\_document 获取全文，如果

需要； (c) 您之前见过但已被 manage\_context 压缩的文档

返回128个token的预览并提醒您调用query\_memory提前检索相关

总结。

参数：

类型：对象

属性：

查询：

类型：字符串

描述：搜索查询字符串。

必填：[查询]

[⬇]（数据：文本/纯文本；base64，bmFtZTogZ2V0X2RvY3VtZW50CgpkZXNjcmlwdGlvbjoKICBSZXRyaWV2ZSBhIGRvY3VtZW50IG J5IGl0cyBkb2NpZC4gVGhlIHJldHVybmVkIHRleHQgaXMgY2FwcGVkIGF0IDgxOTIgdG9rZW5zOyBsb25nZXIgZG9jdW1lbnRzCiA gYXJlIHRydW5jYXRlZC4KCnBhcmFtZXRlcnM6CiAgdHlwZTogb2JqZWN0CiAgcHJvcGVydGllczoKICAgIGRvY2lkOgogICAgICB0 EXBLOiBzdHJpbmcKICAgICAgZGVzY3JpcHRpb246IERvY3VtZW50IEElEIHRvIHJldHJpZXZlLgogIHJlcXVpcmVkOiBbZG9jaWRd)

名称：get\_document

描述：

通过文档的 docid 检索文档。返回的文本上限为 8192 个词元；更长的文件

被截断。

参数：

类型：对象

属性：

文档：

类型：字符串

描述：要检索的文档 ID。

必需：[文档]

#### 实时网络工具 - DeepSearchQA。

[⬇]（数据：文本/纯文本；base64，bmFtZTogc2VhcmNoCgpkZXNjcmlwdGlvbjoKICBTZWFyY2ggdGhlI GxpdmUgd2ViLiBSZXR1cm5zIHRoZSB0b3AgcmVzdWx0cyB3aXRoIHRpdGxlcywgc25pcHBldHMsIGFuZC BVUkxzLiBEZWVwU2VhcmNoUUEKICBxdWVzdGlvbnMgc3BhbiAxNyBkb21haW5zIGFuZCBhcmUgZ3JhZG VkIGFnYWluc3QgZXhoYXVzdGl2ZSBhbnN3ZXIgc2V0cyAtLS0gaXNzdWUgc2V2ZXJhbAogIGRpdmVyc2U gcXVlcmllcyB0byBzdXJmYWNlIGV2ZXJ5IHJlbGV2YW50IGVudGl0eSwgdGhlbiByZWFkIGZ1bGwgcGF nZXMgd2l0aCB0aGUgb3BlbiB0b29sCiAgYmVmb3JlIGNvbW1pdHRpbmcuCgpwYXJhbWV0ZXJzOgogIHR5 cGU6IG9iamVjdAogIHByb3BlcnRpZXM6CiAgICBxdWVyeToKICAgICAgdHlwZTogc3RyaW5nCiagICAg IGRlc2NyaXB0aW9uOiBUaGUgc2VhcmNoIHF1ZXJ5IHN0cmluZy4KICByZXF1aXJlZDogW3F1ZXJ5XQ==)

名称： 搜索

描述：

搜索实时网络。返回带有标题、摘要和 URL 的热门结果。深度搜索QA

问题跨越 17 个领域，并根据详尽的答案集进行评分 - 问题有几个

多样化的查询来显示每个相关实体，然后使用打开的工具阅读整页

在提交之前。

参数：

类型：对象

属性：

查询：

类型：字符串

描述：搜索查询字符串。

必填：[查询]

[⬇]（数据：文本/纯文本；base64，bmFtZTogb3BlbgoKZGVzY3JpcHRpb246CiAgT3BlbiBhIFVSTCBhbmQgcmVhZCB0aGUgd2VicGFnZSBjb250ZW50LiBSZXR1cm5zIHRoZSBwYWdlIH RleHQgd2l0aCBsaW5lIG51bWJlcnM7IGxvbmcgcGFnZXMKICBhcmUgdHJ1bmNhdGVkLiBVc2UgdGhpcyB0byB2ZXJpZnkgY2FuZGlkYXRlcyBmcm9tIHNlYXJjaCBzbmlwcGV0cyAtLS0 gRFNRQSBwZW5hbGlzZXMgYm90aAogIG1pc3NpbmcgaXRlbXMgKHJly2FsbCkgYW5kIG92ZXItYW5zd2VyaW5nIChwcmVjaXNpb24pLgoKcGFyYW1ldGVyczoKICB0eXBlOiBvYmplY3QK ICBwcm9wZXJ0aWVzOgogICAgdXJsOgogICAgICB0eXBlOiBzdHJpbmcKICAgICAgZGVzY3JpcHRpb246IFRoZSBVUkwgdG8gb3BlbiBhbmQgcmVhZC4KICByZXF1aXJlZDogW3VybF0=)

名称：开放

描述：

打开 URL 并读取网页内容。返回带有行号的页面文本；长页

被截断。使用它来验证搜索片段中的候选者 - DSQA 对两者都进行惩罚

缺失项目（召回）和多答（精确）。

参数：

类型：对象

属性：

网址：

类型：字符串

描述：要打开和阅读的 URL。

必需：[网址]

#### 存储库编辑工具 — SWE-bench 已验证。

由每个实例 Modal 沙箱支持的三工具表面，其图像到达时已在 /testbed 中的 base\_commit 处签出。

[⬇]（数据：文本/纯文本；base64，bmFtZTogZXhlY3V0ZV9iYXNoCgpkZXNjcmlwdGlvbjoKICBFeGVjdXRlIGEgYmFzaCBjb21tYW5kIGluc2lkZSB0aGUgcmVwb3NpdG9yeSBzYW5kYm94 IChjd2Q9L3Rlc3RiZWQpLiBVc2UgdGhpcyB0byBpbnNwZWN0IHRoZQogIGNvZGViYXNliCh scywgZmluZCwgZ3JlcCwgY2F0KSwgcnVuIHNTYWxsIHNjcmlwdHMsIG9yIHJ1biB0aGUgcHJ vamVjdCdzIHRlc3RzLiBMb25nIG91dHB1dCBpcwogIHRydW5jYXRlZC4GRRWFjaCBjYWxsIGhhcyBhIDMwMHMgdGltZW91dC4KCnBhcmFtZXRlcnM6CiAgdHlwZTogb2JqZWN0CiAgcHJvcG VydGllczoKICAgIGNvbW1hbmQ6CiAgICAgIHR5cGU6IHN0cmluZwogICAgICBkZXNjcmlwdGlvbjogVGhlIHNoZWxsIGNvbW1hbmQgdG8gcnVulgogIHJlcXVpcmVkOiBbY29tbWFuZF0=)

名称：execute\_bash

描述：

在存储库沙箱内执行 bash 命令 (cwd=/testbed)。用它来检查

代码库（ls、find、grep、cat）、运行小脚本或运行项目的测试。长输出是

被截断。每个调用都有 300 秒的超时时间。

参数：

类型：对象

属性：

命令：

类型：字符串

描述：要运行的 shell 命令。

必需：[命令]

[⬇]（数据：文本/纯文本；base64，bmFtZTogc3RyX3JlcGxhY2VfZWRpdG9yCgpkZXNjcmlwdGlvbjoKICBSZWFkIG9yIGVkaXQgZmls ZXMgaW4gdGhlIHJlcG9zaXRvcnkgc2FuZGJveC4gU3ViY29tbWFuZHM6ICd2aWV3JyBpbnNwZWN0cyBmaWxlIG9yIGRpcmVjdG9yeQog IChmaWxlIG91dHB1dCBpcyBsaW5lLW51bWJlcmVkKSwgJ2NyZWF0ZScgbWFrZXMgYSBuZXcgZmlsZSwgJ3N0cl9yZXBsYWNlJyBzd2F wcyBhIHVuaXF1ZQogIHN1YnN0cmluZywgJ2luc2VydCcgYWRkcyB0ZXh0IGFmdGVyIGEgZ2l2ZW4gbGluZSwgJ3VuZG9fZWRpdCcgcmV 2ZXJ0cyB0aGUgbW9zdCByZWNlbnQgZWRpdCBvbiBhCiAgZmlsZS4KCnBhcmFtZXRlcnM6CiAgdHlwZTogb2JqZWN0CiAgcHJvcGVydG llczoKICAgIGNvbW1hbmQ6CiagICAgIHR5cGU6IHN0cmluZwogICAgICBlbnVtOiBbdmlldywgY3JlyXRlLCBzdHJfcmVwbGFjZSwgaW 5zZXJ0LCB1bmRvX2VkaXRdCiAgICAgIGGRlc2NyaXB0aW9uOiBXaGljaCBzdWItY29tbWFuZCB0byBydW4uCiAgICBwYXRoOgogICAgI CB0eXBlOiBzdHJpbmcKICAgICAgZGVzY3JpcHRpb246IEFic29sdXRlIHBhdGggaW5zaWRlIHRoZSBzYW5kYm94IChlLmcuIC90ZXN0Y mVkL2RqYW5nby9kYi8uLi4pLgogICAgZmlsZV90ZXh0OgogICAgICB0eXBlOiBzdHJpbmcKICAgICAgZGVzY3JpcHRpb246IEZvciAn Y3JLYXRlJzogZnVsbCBmaWxlIGNvbnRlbnRzLgogICAgb2xkX3N0cjoKICAgICAgdHlwZTogc3RyaW5nCiAgICAgIGGRlc2NyaXB0aW9u OiBGb3IgJ3N0cl9yZXBsYWNlJzogc3Vic3RyaW5nIHRvIHJlcGxhY2UgKG11c3QgYmUgdW5pcXVlIGluIHRoZSBmaWxlKS4KICAgIG5 ld19zdHI6CiAgICAgIHR5cGU6IHN0cmluZwogICAgICBkZXNjcmlwdGlvbjogRm9yICdzdHJfcmVwbGFjZScgLyAnaW5zZXJ0JzogbmV 3IHRleHQuCiAgICPBNNLCNRFBGLUZTOKICAGICAgdHlwZTogaW50ZWdlcgogICAgICBkZXNjcmlwdGlvbjogRm9yICdpbnNlcnQnoi BSAW5LIG51bWJlciB0byBpbnNlcnQgQUZURVIgKDAgPSB0b3Agb2YgZmlsZSkuCiAgICB2aWV3X3JhbmdlOgogICAgICB0eXBlOiBhcn JheQogICAgICBpdGVtczoge3R5cGU6IGludGVnZXJ9CiAgICAgIGRlc2NyaXB0aW9uOiBGb3IgJ3ZpZXcnOiBvcHRpb25hbCBbc3Rhc nQsIGVuZF0gMS1pbmRleGVkIGluY2x1c2l2ZSBsaW5lIHJhbmdlOyAtMSA9IEVPRi4KICByZXF1aXJlZDogW2NvbW1hbmQsIHBhdGhd)

名称：str\_replace\_editor

描述：

读取或编辑存储库沙箱中的文件。子命令：“view”检查文件或目录

（文件输出按行编号），“create”创建一个新文件，’str\_replace’ 交换唯一的

子字符串，“插入”在给定行后添加文本，’undo\_edit’ 恢复最近编辑

文件。

参数：

类型：对象

属性：

命令：

类型：字符串

枚举：[查看、创建、str\_replace,插入、undo\_edit]

描述：要运行哪个子命令。

路径：

类型：字符串

描述：沙箱内的绝对路径（例如/testbed/django/db/...）。

file\_text:

类型：字符串

描述：对于“创建”：完整文件内容。

old\_str:

类型：字符串

描述：用于’str\_replace’:要替换的子字符串（在文件中必须是唯一的）。

new\_str:

类型：字符串

描述：对于’str\_replace’ /“插入”：新文本。

insert\_line:

类型：整数

描述：对于“插入”：要在之后插入的行号（0 = 文件顶部）。

view\_range:

类型：数组

项目：{类型：整数}

描述：对于“视图”：可选 [start, end] 1 索引包含行范围； -1 = 结束符。

必需：[命令，路径]

[⬇]（数据：文本/纯文本；base64，bmFtZTogc3VibWl0X3BhdGNoCgpkZXNjcmlwdGlvbjoKICBTaWduYWwgdGhhdCB5b3VyIGZpeCBpcyBjb21wbGV0Z S4gVGhlIHN5c3RlbSB3aWxsIHJ1biBgZ2l0IGRpZmZgIGFnYWluc3QgYmFzZV9jb21taXQgYW5kIHN1Ym1pdAogIHRoZSByZXN1bHRpbmcgdW5pZmllZ CBkaWZmIGFzIHlvdXIgYW5zd2VyLiBDYWxsIHRoaXMgZXhhY3RseSBvbmNlIHdoZW4gdGhlIGZpeCBpcyByZWFkeS4gVGFrZXMKICBubyBhcmd1bWVud HMuCgpwYXJhbWV0ZXJzOgogIHR5cGU6IG9iamVjdAogIHByb3BlcnRpZXM6IHt9ICAgICAgICAjIG5vIGFyZ3VtZW50cwogIHJlcXVpcmVkOiBbXQ==)

名称：submit\_patch

描述：

表明您的修复已完成。系统将针对base\_commit运行“git diff”并提交

由此产生的统一差异作为您的答案。当修复准备就绪时，只调用一次。需要

没有争论。

参数：

类型：对象

属性：{} # 无参数

必填：[]

### B.3 摘要器提示

当智能体调用 manage\_context, 时，系统会序列化要压缩的消息范围，并使用以下指令发出单个 LLM 调用。摘要器输出作为工具结果返回给智能体。

[⬇]（数据：文本/纯文本；base64，T3JpZ2luYWwgcXVlc3Rpb246IHtxdWVzdGlvbn0KCkNvbnZlcn NhdGlvbiB0byBjb21wcmVzczoKCntjb252ZXJzYXRpb259CgpDb21wcmVzcyB0aGUgY29udmVyc2F0 aW9uIGFib3ZlIGludG8gYSB3b3JraW5nLW1lbW9yeSBlbnRyeS4gVGhpcyBlbnRyeSByZXBsYWNlcy B0aGUGYXJjaGl2ZWQKbWVzc2FnZXMgaW4gdGhlIGFnZW50J3Mgd29ya2luZyBjb250ZXh0OyBmdXR1 cmUgY2FsbHMgdG8gcXVlcnlfbWVtb3J5KHN1bW1hcnlfaWQsIHF1ZXJ5KSB3aWxsCnNlYXJjaCB0aG lzIHRleHQuCgpDb3ZlcmFnZToKLSBLbm93bGVkZ2Ugc3RhdGUgLS0tIGZhY3RzIGVzdGFibGlzaGVk IHdpdGggW2RvY2lkXSBjaXRhdGlvbnMsIGNhbmRpZGF0ZSBhbnN3ZXJzIGFuZCB0aGUKZXZpZGVuY2 Ugc3VwcG9ydGluZyBvciBjb250cmFkaWN0aW5nIGVhY2gsIGh5cG90aGVzZXMgYWxyZWFkeSBydWxl ZCBvdXQgd2l0aCB0aGUgW2RvY2lkXSB0aGF0CmVsaW1pbmF0ZWQgdGhlbSwgYW5kIHJlbWFpbmluZ yBvcGVuIHN1Yi1xdWVzdGlvbnMuCi0gVGhvdWdodHMgLS0tIGEgY29uY2lzZSBkaXN0aWxsYXRpb24 gb2YgdGhlIG1vc3QgcmVjZW50IHJlYXNvbmluZyBjaGFpbiBmcm9tIHRoZSBsYXRlc3QKYXNzaXN0Y W50IHR1cm5zICh3aGF0IGRpcmVjdGlvbiB0aGUGYWdlbnQgaGFzIGNvbnZlcmdlZCBvbiBhbmQgd2h 5KSwgQU5EIHRoZSBjb25jcmV0ZSBuZXh0IHN0ZXAKdGhlIGFnZW50IHNob3VsZCB0YWtlIGFmdGVyI HRoaXMgY29tchJlc3Npb24gKHNwZWNpZmljIHNlYXJjaCB2b2NhYnVsYXJ5IC8gZG9jdW1lbnQgdG8 gZmV0Y2ggLwptZW1vcnkgcXVlcnkgLS0tIG5vdCBhIGdlbmVyaWMgImNvbnRpbnVliHNlyXJjaGluZ yIpLgoKT3V0CHV0IGV4YWN0bHkgb25lIDxtZW1vcnk+Li4uPC9tZW1vcnk+IGJsb2NrIHdpdGggdGh lIHR3byBzZWN0aW9ucyBpbiB0aGlzIG9yZGVyOgoKPG1lbW9yeT4KIyMgS25vd2xlZGdlIHN0YXRl CjxmYWN0cywgY2FuZGlkYXRlcywgZWxpbWluYXRlZCBoeXBvdGhlc2VzLCBvcGVuIHN1Yi1xdWVzdG lvbnMsIluIHNob3J0IHByb3NlPgoKIyMgVGhvdWdodHMKPGEgZmV3IHNlbnRlbmNlcyBkaXN0aWxs AW5nIHRoZSBsYXRlc3QgcmVhc29uaW5nIHRocmVhZCwgZm9sbG93ZWQgYnkgMS0yIHNlbnRlbmNlcy购买YW1pbmcgdGhlIGNvbmNyZXRlIG5leHQgc3RlcD4KPC9tZW1vcnk+CgotIDw9IDQwOTYgdG9rZW5z IHRvdGFsIGluc2lkZSB0aGUgYmxvY2ssIHNvIHRyeSB0byBiZSBjb25jaXNlIGJ1dCBzdGlsbCBjb3 ZlciBhbGwgdGhlIGltcG9ydGFudCBpbmZvcm1hdGlvbi4KLSBQcmVzZXJ2ZSBpZGVudGlmaWVycyB2 ZXJiYXRpbSAtLS0gZG9jaWQsIG5hbWVkIGVudGl0aWVzLCBkYXRlcywgbnVtYmVycy4KLSBEbyBub3 QgZW51bWVyYXRlIGV2ZXJ5IHNlYXJjaCBxdWVyeSBvciBkb2NpZCB5b3UgdHJpZWQuCi0gQWZ0ZXI GY2xvc2luZyB0aGUGY2hhdC10ZW1wbGF0ZS1vcGVuZWQgPC90aGluaz4sIHlvdXIgdmVyeSBuZXh0I HRva2VuIG11c3QgYmUgPG1lbW9yeT4uIERvIE5PVCBlbWl0IGFueSBwcmVhbWJsZSBiZXR3ZWVuIDw vdGhpbms+IGFuZCA8bWVtb3J5PiAtLS0gbm8gIlRoaW5raW5nIFByb2Nlc3M6IiBoZWFkaW5nLCBub yBudW1iZXJlZCBwbGFubmluZyBsaXN0LCBubyAiQW5hbHlzaXM6IiAvICJQbGFuOiIgLyAiTGV0IG1 LIC4uLiIgbGVhZC1pbiwgbm8gcmUtc3RhdGVkIHJ1bGVzLCBubyByZS1xdW90ZWQgcXVlc3Rpb24uI FBSYW4gaW5zaWRlIDx0aGluaz4gaWYgeW91IG5lZWQgdG8gcGxhbjsgdGhlIHZpc2libGUgb3V0cHV 0IHN0YXJ0cyBkaXJlY3RseSB3aXRoIDxtZW1vcnk+IGFuZCBlbmRzIHdpdGggPC9tZW1vcnk+Lg==)

原始问题：{问题}

要压缩的对话：

{对话}

将上面的对话压缩到工作记忆条目中。此条目替换存档的

智能体工作环境中的消息；未来调用query\_memory(summary\_id,查询）将

搜索此文本。

覆盖范围：

- 知识状态——通过[docid]引文、候选答案和

支持或反驳每一个的证据，已经用 [docid] 排除了假设

消除了它们，并保留了未解决的子问题。

- 思考——对最新推理链的简洁提炼

助理转向（智能体向哪个方向汇聚以及为什么），以及下一步的具体步骤

智能体应在压缩后采取（特定搜索词汇/要获取的文档/

内存查询——不是通用的“继续搜索”）。

精确输出一个 <memory>…</memory> 块，其中两个部分按以下顺序：

<memory>

## 知识状态

<facts, candidates, eliminated hypotheses, open sub-questions, in short prose>

## 想法

<a few sentences distilling the latest reasoning thread, followed by 1-2 sentences naming the concrete next step>

</memory>

- 块内总共 <= 4096 个词元，因此尽量简洁，但仍涵盖所有重要信息。

- 逐字保留标识符 — docid、命名实体、日期、数字。

- 不要枚举您尝试过的每个搜索查询或文档。

- 关闭聊天模板打开的</think>后，您的下一个词元必须是<memory>。不要在</think>和<memory>之间发出任何序言——没有“思考过程：”标题，没有编号的计划列表，没有“分析：”/“计划：”/“让我……”导入，没有重新陈述的规则，没有重新引用的问题。如果需要计划，请在<think>内计划；可见输出直接以<memory>开始，以</memory>结束。

### B.4 query\_memory 召回提示

当智能体调用query\_memory(summary\_id,查询时），系统加载该摘要ID下的原始存档消息并调用以下召回提示；返回的项目符号成为工具结果。

[⬇]（数据：文本/纯文本；base64，U2F2ZWQgbWVzc2FnZXMgdW5kZXIgc3VtbWFyeV9pZD17c3VtbWFy EV9pZH06Cgp7aGlzdG9yeX0KClJly2FsbCByZXF1ZXN0IC0tLSBleHRyYWN0IGNvbnRlbnQgcmVsZXZ hbnQgdG86IHtxdWVyeX0KCk91dHB1dCBmb3JtYXQgKHN0cmljdCk6Ci0gUHV0IGFueSBpbnRlcm5hbC作者：ZWFzb25pbmcgaW5zaWRlIDx0aGluaz4uLi48L3RoaW5rPiAtLS0gdGhlc2Ugd2lsbCBiZSBzdHJpcH BLZC4KLSBBZnRlciA8L3RoaW5rPiwgd3JpdGUgdGhlIHJly2FsbCBhcyBjb21wYWN0IGJ1bGxldHMgb 25seS4gTm8gcHJvc2UgchHJlyW1ibGUuIE5vIHJlc3RhdGVtZW50IG9mCnRoZSBxdWVyeS4gTm8gYWRk cmVzcyB0byB0aGUgcmVhZGVyIChubyAidGhlIHVzZXIiLCAidGhlIGFnZW50IiwgInlvdSIplgotiev hY2ggYnVsbGV0IG11c3QgY2FycnkgY29uY3JldGUgaWRlbnRpZmllcnMgKGRvY2lkcywgVVJMcywgbnV tYmVycywgbmFtZXMpiHZlcmJhdGltIC0tLSBuZXZlcgpwYXJhcGhyYXNLIG51bWVyaWNhbCBldmlkZW 5jZS4KLSBHcm91cCBpbnRvIHVwIHRvIHRocmVlIHNly3Rpb25zIChvbWl0IGFueSB0aGF0IGFyZSBlb XB0eSK6CiAgLSAqKlJlbGV2YW50IGZpbmRpbmdzOioqIGZhY3RzIHRoYXQgYmVhciBvbiB0aGUgcXVl CNKSIHdpdGggc3VwcG9ydGluZyBkb2NpZHMvVVJMCy4KICAtICoqRGVhZCBlbmRzOioqIHF1ZXJpZXMg LyBkb2NpZHMgLyBoeXBvdGhlc2VzIHRyaWVkIHRoYXQgcHJvZHVjZWQgbm90aGluZy4KICATICOQT3B LbiAvIHVucmVzb2x2ZWQ6KiogbW9zdCBwcm9taXNpbmcgZGlyZWN0aW9uIHN0aWxsIHRvIHZlcmlmes 4KLSBJZiBub3RoaW5nIGluIHRoZSBzYXZlZCBtZXNzYWdlcyBpcyByZWxldmFudCwgb3V0cHV0IGV4Y WN0bHk6IGAobm90aGluZyByZWxldmFudCB1bmRlcgpzdW1tYXJ5X2lkPXtzdW1tYXJ5X2lkfSlgLg==)

在summary\_id={summary\_id}:下保存的消息

{历史}

召回请求 - 提取与以下内容相关的内容：{query}

输出格式（严格）：

- 将任何内部推理放入<think>…</think> - 这些将被剥离。

- 在</think>之后，仅将召回写为紧凑项目符号。无散文序言。没有重述

查询。没有对读者的称呼（没有“用户”、“智能体”、“您”）。

- 每个项目符号必须逐字携带具体标识符（docids、URL、数字、名称）——绝不

解释数字证据。

- 最多分为三个部分（忽略任何空的部分）：

- \*\*相关发现：\*\* 与查询有关的事实，以及支持的 docids/URL。

- \*\*死胡同：\*\* 查询/文档/假设尝试没有产生任何结果。

- \*\*开放/未解决：\*\* 最有希望的方向仍有待验证。

- 如果保存的消息中没有任何相关内容，则准确输出：“（以下没有任何相关内容）

summary\_id={summary\_id})‘.

### B.5 教师提示（SFT数据生成）

两个教师提示产生用于训练策略的监督微调数据。两者都改写了失败学生轨迹的一步；重写的步骤替换了 SFT 示例中的原始步骤。

#### 注释老师：确定何时调用记忆工具。

鉴于推出失败，教师选择最早的消息索引，其中 manage\_context 或 query\_memory 调用会有所帮助，并写下智能体似乎已产生的第一人称理由。

[⬇]（数据：文本/纯文本；base64，WW91IGFyZSByZXZpZXdpbmcgYW4gYWdlbnQncyByZXNlYXJjaCB0cmFqZWN0b3J5IG9uIGEga GFyZCBmYWN0LWZpbmRpbmcgcXVlc3Rpb24uIFRoZSBhZ2VudApmYWlsZWQ6IGVpdGhlciBpdCBwcm9kdWNlZCBhIHdyb25nIGFuc 3dlciwgZXhoYXVzdGVkIGl0cyB0dXJuIGJ1ZGdldCwgb3IgaXRzIHdvcmtpbmcgY29udGV4dApvdmVyZmxvd2VkIGJlZm9yZSByZ WFjaGluZyBhbiBhbnN3ZXIuCgpZb3VyIHNpbmdsZSBqb2I6IGlkZW50aWZ5IHRoZSBFQVJMSUVTVCBwb2ludCBpbiB0aGUgdHJha mVjdG9yeSB3aGVyZSB0aGUgYWdlbnQgc2hvdWxkIGhhdmUKaW52b2tlZCBhIGNvbnRleHQtbWFuYWdlbWVudCBvcGVyYXRpb24gL S0tIGVpdGhlciBgbWFuYWdlX2NvbnRleHRgIChjb21wcmVzcyB3b3JraW5nIG1lbW9yeSkgb3IKYHF1ZXJ5X21lbW9yeWAgKHJld HJpZXZlIGZyb20gcHJpb3Igc3VtbWFyaWVzKSAtLS0gYW5kIHdyaXRlIHRoZSBmaXJzdC1wZXJzb24gcmF0aW9uYWxlIHRoZSBhZ 2VudAp3aWxsIGFwcGVhciB0byBoYXZlIHByb2R1Y2VkIGZvciB0aGF0IGNhbGwuCgojIFFVRVNUSU9OCntxdWVzdGlvbn0KCiMgR 09MREVOIEFOU1dFUiAgKEZPUiBZT1VSIFJFRkVSRU5DRSBPTkxZIC0tLSBORVZFUiByZXZlYWwgb3IgaGludCBhdCB0aGlzKQp7Y 29ycmVjdF9hbnN3ZXJ9CgojIEdPTERFTiBFVklERU5DRSAgKEZPUiBZT1VSIFJFRkVSRU5DRSBPTkxZIC0tLSBuZXZlciBjaXRli GRvY2lkcyBmcm9tIHRoZXNlLCBxdW90ZSwgb3IKcGFyYXBocmFzZSkKe2dvbGRfZG9jc19ibG9ja30KCiMgQUdFTlQgVFJBSkVDV E9SWQpFYWNoIG1lc3NhZ2UgaXMgcHJlZml4ZWQgd2l0aCBgW2lkPU4sIHJvbGU9Ul1gLiBBc3Npc3RhbnQgYHRvb2xfY2FsbHNgI GFuZCB0b29sIHJlc3BvbnNlcyBhcmUKaW5saW5lZCB1bmRlciB0aGUgcmVsZXZhbnQgbWVzc2FnZS4KCntudW1iZXJlZF9oaXN0b 3J5fQoKIyBXT1JLU1BBQ0UgU1RBVEUKc3VtbWFyeV9pZHMgY3VycmVudGx5IHN0b3JlZCBmcm9tIHByaW9yIG1hbmFnZV9jb250Z Xh0IGNhbGxzOiB7c3VtbWFyeV9pZHN9CgojiIEFWQUlMQUJMRSBBQ1RJT05TCi0gYG1jYCATLS0gY29tchHJlc3MgYWxsIG1lc3NhZ 2VzIHNpbmNlIHRoZSBsYXN0IGNvbXByZXNzaW9uIGJvdW5kYXJ5IGludG8gYSBzdW1tYXJ5IHN0b3JlZCBpbiBsb25nLXRlcm0gb WVtb3J5LiBVc2Ugd2hlbjoKICAgICogdGhlIGFnZW50IGlzIGN5Y2xpbmcgdGhyb3VnaCByZXBlYXRlZCBxdWVyaWVzIHdpdGhvd XQgZmluZGluZyBuZXcgZXZpZGVuY2UKICAgICogbG9uZyB0b29sIHJlc3BvbnNlcyAoc2VhcmNoIHJlc3VsdHMsIGZldGNoZWQgZ G9jdW1lbnRzKSBhY2N1bXVsYXRlZCBpbiB3b3JraW5nIGNvbnRleHQgYXJLIG5vIGxvbmdlciBsb2FkLWJlYXJpbmcKICAgICogd 29ya2luZyBjb250ZXh0IGlzIGFwchJvYWNoaW5nIHRva2VuIHNhdHVyYXRpb24KLSBgcW1gIC0tLSBxdWVyeSBhIHByaW9yIHN1b W1hcnkgYnkgbmF0dXJhbC1sYW5ndWFnZSBxdWVyeS4gT05MWSBWQUxJRCBJRiB0aGUgc3VtbWFyeV9pZHMgbGlzdCBhYm92ZSBpc yBub24tZW1wdHkuCi0gYG5vX2FjdGlvbl9uZWVkZWRgIC0tLSBlbWl0IHRoaXMgaWYgbm8gbWMvcW0gaW50ZXJ2ZW50aW9uIHBya W9yIHRvIHRoZSB0cmFqZWN0b3J5J3MgZmFpbHVyZSBwb2ludCB3b3VsZCBoYXZLIG1hdGVyaWFsbHkgaGVscGVkLgoKIyBDT05TV FJBSU5UUyBPTiBgYWZ0ZXJfaWRgCi0gTXVzdCBzYXRpc2Z5IGAwIDw9IGFmdGVyX2lkIDw9IGxhc3RfaWRgLgotIFRoZSBtZXNzY WdlIGF0IGlkPWFmdGVyX2lkIG11c3QgaGF2ZSByb2xlIGluIHtzeXN0ZW0sIHVzZXIsIHRvb2x9LiBJbnNlcnRpbmcgYWZ0ZXIgY W4gYXNzaXN0YW50CnR1cm4gdGhhdCBoYXMgcGVuZGluZyB0b29sX2NhbGxzIHdvdWxkIG9ycGhhbiB0aG9zZSBjYWxscy4KLSBQa WNrIHRoZSBTTUFMTEVTVCB2YWxpZCBgYWZ0ZXJfaWRgIHdoZXJlIHRoZSBhY3Rpb24gd291bGQgbWF0ZXJpYWxseSBoZWxwLiBJZ iBtdWx0aXBsZQpwb3NpdGlvbnMgYXJlIGVxdWFsbHkgdmFsaWQsIHBpY2sgdGhlIGVhcmxpZXN0LgoKIyBDT05TVFJBSU5UUyBPT iBgcW1gCi0gSWYgc3VtbWFyeV9pZHMgYWJvdmUgaXMgZW1wdHksIHlvdSBNVVNUIE5PVCBjaG9vc2UgYHFtYC4gUGljayBgbWNGI G9yIGBub19hY3Rpb25fbmVlZGVkYC4KCiMgT1VUUFVUIEZPUk1BVCATLS0gU1RSSUNUIEPTT04sIE9ORSBPQkpFQ1QsIE5PIFBST 1NFIEJFRk9SRSBPUiBBRlRFUgoKewogICJkZWNpc2lvbiI6ICJtYyIgfCAicW0iIHwgIm5vX2FjdGlvbl9uZWVkZWQiLAOGICJhZ nRlcl9pZCI6IDxpbnRlZ2VyOyB1c2UgLTEgaWYgZGVjaXNpb24gaXMgbm9fYWN0aW9uX25lZWRlZD4sCiAgInRoaW5rIjogIjxmaXJzdC1wZXJzb24gcmF0aW9uYWxlLCBzZWUgcnVsZXMgYmVsb3c+IiwKICAicW1fcXVlcnkiOiAiPG5hdHVyYWwtbGFuZ3VhZ2UgcXVlcnk7IHJlc XVpcmVkIGlmZiBkZWNpc2lvbj0ncW0nPiIKfQoKIyBSVUxFUyBGT1IgYHRoaW5rYApgdGhpbmtgIGlzIHRoZSBmaXJzdC1wZXJzb24gcmVhc29uaW 5nIHRoZSBhZ2VudCB3aWxsIGFwcGVhciB0byBoYXZlIHByb2R1Y2VkIGp1c3QgYmVmb3JlIGNhbGxpbmcKbWMvcW0uIEl0IG11c3QgcmVhZCBhcyB HDXRoZW50aWMgYWdlbnQgcmVhc29uaW5nLgoKUkVRVUlSRU1FTlRTOgoxLiBGaXJzdC1wZXJzb24gb25seSAoIkkgbm90aWNlLi4uIiwgIm15IHNl YXJjaGVzLi4uIiwgIm15IHdvcmtpbmcgY29udGV4dC4uLiIpLiBObyB0aGlyZC1wZXJzb24gc2VsZi1yZWZlcmVuY2UsIG5vIG5hbWluZyBvciBh bGx1ZGluZyB0byBhbnkgZXh0ZXJuYWwgcGFydHkuCjIuIEdyb3VuZCB0aGUgcmF0aW9uYWxlIE9OTFkgaW4gb2JzZXJ2YWJsZSB0cmFqZWN0b3J5I HNpZ25hbHMsIGUuZy46CiAgICAqIHRoZSBzYW1lIG9yIG5lYXItaWRlbnRpY2FsIHF1ZXJ5IGtleXdvcmRzIHJlcGVhdGVkIGFjcm9zcyBtdWx0aX BsZSBzZWFyY2ggdHVybnMKICAgICogYWNjdW11bGF0ZWQgaW5wdXQgdG9rZW5zIC8gY29udGV4dC13aW5kb3cgcHJlc3N1cmUKICAgICogdGhlIGx hc3QgTiB0dXJucyBwcm9kdWNlZCBubyBuZXcgZG9jaWRzIGFuZCBubyBuZXcgZXZpZGVuY2UKICAgICogdGhlIHJldHJpZXZlZCBkb2NpZCBzZXQ gaXMgc21hbGwgYW5kIGN5Y2xpbmcKICAgICogKGZvciBxbSBvbmx5KSBhIHJlbGV2YW50IGVhcmxpZXIgc3VtbWFyeSBleGlzdHMgdGhhdCBoYXMg bm90IGJlZW4gcmUtcXVlcmllZAozLiBTVFJJQ1RMWSBGT1JCSURERU46CiAgICAqIG1lbnRpb25pbmcsIG5hbWluZywgb3IgZGVzY3JpYmluZyBhb nkgcGFydCBvZiB0aGUgZ29sZGVuIGFuc3dlcgogICAgKiBuYW1pbmcgYW55IGRvY2lkIHRoZSBhZ2VudCBoYXMgTk9UIHJldHJpZXZlZCBpbiB0aG lzIHRyYWplY3RvcnkKICAgICogYW55IG9mIHRoZXNlIHdvcmRzOiBgY29hY2hgLCBgY29hY2hlc2AsIGBjb2FjaGluZ2AsIGBmZWVkymFja2AsIG作者ZXZpZXdgLCBgcmV2aWV3ZXJgLCBgcmV2aWV3ZWRgLCBgZXh0ZXJuYWxgLCBgYWR2aXNlZGAsIGBhZHZpc29yYCwgYGd1aWRhbmNlYCwgYHRvbGQ gbWVgLCBgc29tZW9uZSBzYWlkYCwgYGluc3RydWN0ZWRgCjQuIExlbmd0aDogYmV0d2VlbiAyMDAgYW5kIDEyMDAgY2hhcmFjdGVycy4KCk91dHB1 DCB0aGUgSlNPTiBvYmplY3Qgb25seS4gTm8gchHJlYW1ibGUsIG5vIGNsb3NpbmcgcmVtYXJrcywgbm8gcHJvc2Ugb3V0c2lkZSB0aGUgSlNPTi4=)

您正在审查智能体在一个困难的事实调查问题上的研究轨迹。智能体

失败：要么产生了错误的答案，耗尽了轮次预算，要么是其工作环境

overflowed before reaching an answer.

您的唯一工作：确定智能体应该具有的轨迹中最早的点

调用上下文管理操作 - ‘manage\_context‘（压缩工作内存）或

‘query\_memory‘（从之前的摘要中检索）——并以第一人称的方式写下智能体的理由

will appear to have produced for that call.

# 问题

{问题}

# 黄金答案（仅供参考——切勿透露或暗示这一点）

{correct\_answer}

# 黄金证据（仅供参考——切勿引用其中的文档、引用或

释义）

{gold\_docs\_block}

# 特工轨迹

每条消息都以“[id=N, role=R]”为前缀。 Assistant ‘tool\_calls‘ and tool responses are

inlined under the relevant message.

{numbered\_history}

# 工作区状态

summary\_ids 当前从之前的 manage\_context 调用中存储：{summary\_ids}

# 可用的操作

- ‘mc’ — 将自上次压缩边界以来的所有消息压缩为存储在长期记忆中的摘要。使用时：

\* 智能体循环重复查询而没有找到新的证据

\* 在工作上下文中积累的长工具响应（搜索结果、获取的文档）不再承重

\* 工作环境正接近词元饱和

- ‘qm’ — 通过自然语言查询查询先前的摘要。仅当上面的summary\_ids列表非空时才有效。

- ‘no\_action\_needed‘ — 如果在轨迹故障点之前没有 mc/qm 干预会有实质性帮助，则发出此消息。

# ‘after\_id‘ 的限制

- 必须满足‘0 <= after\_id <= last\_id‘.

- id=after\_id 处的消息必须在{系统、用户、工具}中具有角色。在助手之后插入

已挂起的 tool\_calls 将孤立这些调用。

- 选择最有效的 ‘after\_id‘ ，其中该行动将有实质性帮助。如果有多个

职位同等有效，选择最早的。

# 对“qm”的限制

- 如果上面的summary\_ids为空，则不得选择“qm”。选择“mc”或‘no\_action\_needed‘.

# 输出格式 — 严格的 JSON、一个对象、前后无散文

{

“决定”：“MC” | “qm”| "no\_action\_needed",

"after\_id":<integer; use -1 if decision is no\_action\_needed>，

“认为”：“<first-person rationale, see rules below>”，

"qm\_query":“<natural-language query; required iff decision=’qm’>”

}

# “思考”的规则

“思考”是客服人员在致电之前做出的第一人称推理

MC/质量管理。它必须被解读为真实的智能体推理。

要求：

1. 仅第一人称（“我注意到……”、“我的搜索……”、“我的工作环境……”）。没有第三人称自我引用，没有点名或暗示任何外部人士。

2. 仅将基本原理基于可观察的轨迹信号，例如：

\* 在多个搜索轮次中重复相同或几乎相同的查询关键字

\* 累积输入标记/上下文窗口压力

\* 最后 N 回合没有产生新的 docids，也没有新的证据

\* 检索到的 docid 集很小并且循环

\* （仅适用于 qm）存在尚未重新查询的相关早期摘要

3. 严格禁止：

\* 提及、命名或描述黄金答案的任何部分

\* 命名智能体在此轨迹中未检索到的任何 docid

\* 以下任何单词：“教练”、“教练”、“辅导”、“反馈”、“评论”、“评论者”、“评论”、“外部”、“建议”、“顾问”、“指导”、“告诉我”、“有人说”、“指示”

4. 长度：200 至 1200 个字符之间。

仅输出 JSON 对象。没有序言，没有结束语，没有 JSON 之外的散文。

####纠错老师：重写一个没有效果的mc步骤。

补充教师针对以失败为主的痕迹
*过度压缩*：它选择一个 mc 步骤，该步骤应该
相反，（i）提交，（ii）更高效的搜索，或者
(iii) get\_document 获取已经片段化的 docid，
并写入替换回合。

[⬇]（数据：文本/纯文本；base64，WW91IGFyZSByZXZpZXdpbmcgYSByZXNlYXJjaCBhZ2VudCdzIHJvbGxvdXQuIFRoZSBhZ2Vud CBoYWQgZm91ciB0b29scyAtLS0gYHNlyXJjaGAsCmBnZXRfZG9jdW1lbnRgLCBgbWFuYWdlX2NvbnRleHRgIChtYyksIGBxdWVye V9tZW1vcnlgIChxbSkgLS0tIGFuZCBlXRoZXIgcmVhY2hlZCBhbiBpbmNvcnJlY3QKZmluYWwgYW5zd2VyIG9yIGV4aGF1c3RlZ CBpdHMgdHVybiBidWRnZXQgd2l0aG91dCBjb21taXR0aW5nLgoKWW91ciBqb2I6IGZpbmQgYSBzaW5nbGUgbWMgc3RlcCB0byZ XBsYWNlIHdpdGggYSBtb3JlIHByb2R1Y3RpdmUgYWN0aW9uLiBUaHJlZSBwb3NzaWJsZQppbnRlcnZlbnRpb25zLCBpbiAqKmdsb 2JhbCBwcmlvcml0eSBvcmRlcioqIChhY3Rpb24gdHlwZSBmaXJzdCwgdGhlbiBlYXJsaWVzdCBtYyBzdGVwKToKICAxLiBjb21ta XQgLS0tIGF0IFNPTUUgbWMgc3RlcCwgdGhlIGluLWNvbnRleHQgZXZpZGVuY2UgaXMgYWxyZWFkeSBlbm91Z2ggdG8gYW5zd2VyL iBSZXBsYWNlIHRoYXQgbWMgY2FsbCB3aXRoIGEgZmluYWwtYW5zd2VyIHR1cm4uCiAgMi4gcmVwbGFjZV93aXRoX3NlYXJjaCATL S0gYXQgU09NRSBtYyBzdGVwLCBhIHNwZWNpZmljIHNlYXJjaCBxdWVyeSB5b3UgcHJvcG9zZSB3b3VsZCBoYXZlIGJlZW4gbW9yZ SBwcm9kdWN0aXZlIHRoYW4gY29tchHJlc3NpbmcuIFRoZSBxdWVyeSBtdXN0IE5PVCBkdXBsaWNhdGUgYW55IHF1ZXJ5IHRoZSBhZ 2VudCBoYXMgYWxyZWFkeSB0cmllZC4KICAzLiByZXBsYWNlX3dpdGhfZ2V0X2RvY3VtZW50IC0tLSBhdCBTT01FIG1jIHN0ZXASI GEgc3BlY2lmaWMgZG9jaWQgdGhhdCB3YXMgQUxSRUFEWSB2aXNpYmxlIGluIGEgcHJpb3Igc2VhcmNoLXJlc3VsdCBzbmlwcGV0I HNob3VsZCBoYXZlIGJlZW4gZmV0Y2hlZC4gVGhlIGRvY2lkIG11c3QgYmUgaW4gdGhlIGN1bXVsYXRpdmUgcmV0cmlldmVkIHNld CBhdCBoaXN0b3J5WzpyZXBsYWNlX2lkXS4KCkFsZ29yaXRobSAtLS0gZ2xvYmFsIGFjdGlvbiBwcmlvcml0eSwgZWFybGllc3Qgc 3RlcCB3aXRoaW4gdGhlIGNOB3NlbiBhY3Rpb246CiAgU3RlcCAxLibTY2FuIEFMTCBjYW5kaWRhdGUgbWMgc3RlcHMgaW4gY2hyb 25vbG9naWNhbCBvcmRlci4gSWYgQU5ZIHN0ZXAgaXMgY29tbWl0LWZlyXNpYmxlICgKICBpbi1jb250ZXh0IGV2aWRlbmNlIHN1c HBvcnRzIHRoZSBnb2xkIGFuc3dlciBhdCB0aGF0IHBvaW50KSwgcGljayB0aGUgRUFSTElFU1Qgc3VjaCBzdGVwIGFuZAogIG91d HB1dCBkZWNpc2lvbiA9ICJjb21taXQiLiBTVE9QLgogIFN0ZXAgMi4gRWxzZSAobm8gY29tbWl0IGZlYXNpYmxlIGFueXdoZXJlK Swgc2NhbiBhbGwgY2FuZGlkYXRlIG1jIHN0ZXBzIGluIGNocm9ub2xvZ2ljYWwgb3JkZXIuCiAgSWYgQU5ZIHN0ZXAgaXMgc2Vhc mNoLWZlyXNpYmxlICh5b3UgY2FuIHdyaXRlIGEgbm92ZWwsIHByb2R1Y3RpdmUgcXVlcnkgZGlzdGluY3QgZnJvbSBwcmlvcgogI HF1ZXJpZXMpLCBwaWNrIHRoZSBFQVJMSUVTVCBzdWNoIHN0ZXAgYW5kIG91dHB1dCBkZWNpc2lvbiA9ICJyZXBsYWNlX3dpdGhfc 2VhcmNoIi4gU1RPUC4KICBTdGVwIDMuIEVsc2UsIHNjYW4gYWxsIGNhbmRpZGF0ZSBtYyBzdGVwcyBpbiBjaHJvbm9sb2dpY2FsI G9yZGVyLiBJZiBBTlkgc3RlcCBpcyBnZXRfZG9jdW1lbnQtCiAgZmVhc2libGUgKGEgc3BlY2lmaWMgZG9jaWQgaW4gdGhlIGN1b XVsYXRpdmUgcmV0cmlldmVkIHNldCB3b3VsZCwgaWYgZmV0Y2hlZCwgbGlrZWx5IHlpZWxkIHRoZQogIGFuc3dlciksIHBpY2sgd GhlIEVBUkxJRVNUIHN1Y2ggc3RlcCBhbmQgb3V0chV0IGRLY2lzaW9uID0gInJlcGxhY2Vfd2l0aF9nZXRfZG9jdW1lbnQiLiBTV E9QLgogIFN0ZXAgNC4gRWxzZSwgb3V0chHV0IGRLY2lzaW9uID0gIm5vX3JlcGxhY2VtZW50X3Bvc3NpYmxlIi4KCkNSSVRJQ0FMO iBjb21taXQgaXMgdGhlIGhpZ2hlc3QtchHJpb3JpdHkgYWN0aW9uIEdMT0JBTExZLiBEbyBOT1Qgc2hvcnQtY2lyY3VpdCB0bwpyZ XBsYWNlX3dpdGhfc2VhcmNoIGp1c3QgYmVjYXVzZSBjb21taXQgaXNuJ3QgZmVhc2libGUgYXQgdHVybiAyIC0tLSBmaxJzdCBja GVjayBpZiBjb21taXQgaXMKZmVhc2libGUGYXQgQU5ZIGxhdGVyIGNhbmRpZGF0ZSBtYyBzdGVwLgoKIyBRVUVTVElPTgp7cXVlc 3RPB259CgoJIEdPTERFTiBBTlNXRVIKE2NvcnJly3RfYW5zd2VyfQoKIyBHT0xERU4gRVZJREVOQ0UgICh1c2Ugb25seSB0byBkZ XNpZ24gYSBnb29kIHNlYXJjaF9xdWVyeSBvciB0byB2ZXJpZnkgY29tbWl0IGZlYXNpYmlsaXR5KQp7Z29sZF9kb2NzX2Jsb2Nrf QoKIyBBR0VOVCBUUkFKRUNUT1JZICAobnVtYmVyZWQpCkVhY2ggbWVzc2FnZSBpcyBwcmVmaXhlZCB3aXRoIGBbaWQ9Tiwgcm9sZT1SXWAuIEFzc2lzdGFudCBgdG9vbF9jYWxsc2AgYW5kIHRvb2wgcmVzcG9uc2VzIGFyZQppbmxpbmVkLgoKe251bWJlcmVkX2hpc 3Rvcnl9CgojIENBTkRJREFURSBtYyBTVEVQUwpgcmVwbGFjZV9pZGAgTVVTVCBiZSBvbmUgb2YgdGhlc2UgYXNzaXN0YW50IHR1c m4gaWRzICh3aGVyZSB0aGUGYWdlbnQgY2FsbGVkIG1hbmFnZV9jb250ZXh0KToKCntjYW5kaWRhdGVfbWNfaWRzfQoKIyBET0NJR FMgVEhFIEFHRU5UIEhBUyBBTFJFQURZIFJFVFJJRVZFRCAgKGN1bXVsYXRpdmUsIHBlciBjYW5kaWRhdGUgbWMgdHVybikKWW91I G1heSBjaXRlIE9OTFkgdGhlc2UgZG9jaWRzIluIGB0aGlua2AgLyBgZXhwbGFuYXRpb25gLiBGb3IgYHJlcGxhY2Vfd2l0aF9nZ XRfZG9jdW1lbnRgLApgZG9jaWRfdG9fZ2V0YCBtdXN0IGJlIG9uZSBvZiB0aGVzZSBhdCB0aGUgY2hvc2VuIGByZXBsYWNlX2lkY C4KCntyZXRyaWV2ZWRfZG9jaWRzX2J5X3R1cm59CgojIEFHRU5UJ1MgUFJJT1IgU0VBUkNIIFFVRVJJRVMgIChkbyBOT1QgcmVwZ WF0IGFueSBvZiB0aGVzZSBmb3IgYHNlYXJjaF9xdWVyeWApCgp7chHJpb3Jfc2VhcmNoX3F1ZXJpZXN9CgojIE9VVFBVVCBGT1JNQ VQgLS0tIFNUUklDVCBKU09OLCBPTkUgT0JKRUNULCBOTyBQUk9TRSBCRUZPUkUgT1IgQUZURVIKCnsKICAiZGVjaXNpb24iOiAiY 29tbWl0IiB8ICJyZXBsYWNlX3dpdGhfc2VhcmNoIiB8ICJyZXBsYWNlX3dpdGhfZ2V0X2RvY3VtZW50IiB8ICJub19yZXBsYWNlb WVudF9wb3NzaWJsZSIsCiAgInJlcGxhY2VfaWQiOiA8aW50ZWdlciBpbiBDQU5ESURBVEUgbWMgU1RFUFMsIG9yIC0xIGlmIG5vX 3JlcGxhY2VtZW50X3Bvc3NpYmxlPiwKICAidGhpbmsiOiAiPGZpcnN0LXBlcnNvbiBzdHVkZW50LXZvaWNlIHJlZmxlY3Rpb247I HNlZSBydWxlcz4iLAogICJyYXRpb25hbGUIOiAiPG9uZSBzZW50ZW5jZSB0byB0aGUgZXhwZXJpbWVudGVyIC0tLSB3aHkgVEhJU yByZXBsYWNlX2lkIGFuZCBUSElTIGFjdGlvbjsgZm9yIGh1bWFuIHJldmlldyBvbmx5PiIsCgogIC8vIGZpZWxkcyBmb3IgZGVja XNpb249J2NvbW1pdCc6CiAgImV4cGxhbmF0aW9uIjogIjxzaG9ydCBCQ1Atc3R5bGUgZXhwbGFuYXRpb247IG1heSBjaXRlIHJld HJpZXZlZCBkb2NpZHM7IDEtMyBzZW50ZW5jZXM+IiwKICAiZXhhY3RfYW5zd2VyIjogIjxmaW5hbCBhbnN3ZXIgdGV4dCwgZnJlZ S1mb3JtPiIsCiAgImNvbmZpZGVuY2UiOiA8aW50ZWdlciAwLTEwMD4sCgogIC8vIGZpZWxkIGZvciBkZWNpc2lvbj0ncmVwbGFjZ V93aXRoX3NlYXJjaCc6CiAgInNlYXJjaF9xdWVyeSI6ICI8cXVlcnkgc3RyaW5nIHRoZSBhZ2VudCBzaG91bGQgaGF2ZSBpc3N1Z WQgaW5zdGVhZCBvZiBtYz4iLAoKICAvLyBmaWVsZCBmb3IgZGVjaXNpb249J3JlcGxhY2Vfd2l0aF9nZXRfZG9jdW1lbnQnOgogI CJkb2NpZF90b19nZXQiOiA8aW50ZWdlciBkb2NpZDsgTVVTVCBiZSBpbiB0aGUgY3VtdWxhdGl2ZSByZXRyaWV2ZWQgc2V0IGF0I Ghpc3RvcnlbOnJlcGxhY2VfaWRdPgp9CgpJbmNsdWRlIE9OTFkgdGhlIGZpZWxkcyByZWxldmFudCB0byB5b3VyIGNob3NlbiBkZ WNpc2lvbjsgb21pdCBvciBudWxsIHRoZSBvdGhlcnMuCgojIFJVTEVTIEZPUiBgdGhpbmtgCgpgdGhpbmtgIGlzIHRoZSBmaXJzd C1wZXJzb24gcmVhc29uaW5nIHRoZSBhZ2VudCB3aWxsIGFwcGVhciB0byBoYXZlIHByb2R1Y2VkIGF0IHR1cm4gYHJlcGxhY2Vfa WRgLgoyMDAtMTUwMCBjaGFyYWN0ZXJzLiBNdXN0IHJlYWQgYXMgYXV0aGVudGljIGFnZW50IHJlYXNvbmluZy4KClJFUVVJUKVNR U5UUyBieSBkZWNpc2lvbjoKLSBjb21taXQ6IGV4cGxhaW4gd2h5IHRoZSBldmlkZW5jZSBBTFJFQURZIGluIGNvbnRleHQgaXMgZ W5vdWdoOyBjaXRlIHJldHJpZXZlZCBkb2NpZHMuCi0gcmVwbGFjZV93aXRoX3NlYXJjaDogZXhwbGFpbiB3aHkgcHJpb3IgcXVlc mllcyBoYXZliIHN0YWxsZWQgYW5kIHdoeSB0aGUgcHJvcG9zZWQgcXVlcnkgdGFyZ2V0cwphIHByb2R1Y3RpdmUgbmV3IGRpcmVjd Glvbi4KLSByZXBsYWNlX3dpdGhfZ2V0X2RvY3VtZW50OiBleHBsYWluIHdoaWNoIHNlYXJjaCByZXN1bHQgc25pcHBldCB5b3Unc mUgZm9sbG93aW5nIHVwIG9uLCBjaXRlIHRoZQpvcmlnaW5hdGluZyBkb2NpZF90b19nZXQuCgpTVFJJQ1RMWSBGT1JCSURERU4ga W4gYWxsIGNhc2VzOgotIENpdGluZyBhbnkgZG9jaWQgTk9UIGluIHRoZSBjdW11bGF0aXZlIHJldHJpZXZlZCBzZXQgYXQgaGlzd G9yeVs6cmVwbGFjZV9pZF0uCi0gQ29hY2gtZnJhbWluZyB3b3JkczogYGNvYWNoYCwgYGNvYWNoaW5nYCwgYGZlZWRiYWNrYCwgY HJldmlld2AsIGByZXZpZXdlcmAsIGBhZHZpc2VkYCwKYGd1aWRhbmNlYCwgYHRvbGQgbWVgLCBgc29tZW9uZSBzYWlkYCwgYGV4dGVybmFsYCwgYGluc3RydWN0ZWRgLgotIE1lbnRpb25pbmcgYSB1c2VyLCB0ZWFjaGVyLCB0cmFpbmVyLCBvciBhbnkgZXh0ZXJuYWwgcGFydHkuCgojIFJVTEVTIEZPUiBgc2VhcmNo X3F1ZXJ5YCAgKG9ubHkgd2hlbiBkZWNpc2lvbj0ncmVwbGFjZV93aXRoX3NlYXJjaCcpCi0gTGVuZ3RoOiAyLTEyIHdvcmRzLgotIE1VU1QgTk9UIGJlIHN1YnN0cmluZy1lcXVhbCAo Y2FzZS1pbnNlbnNpdGl2ZSkgdG8gYW55IHF1ZXJ5IGluICJQUklPUiBTRUFSQ0ggUVVFUklFUyIuCi0gU0hPVUxEIHVzZSBkaXN0aW5jdGl2ZSB0ZXJtcyBkcmF3biBmcm9tIHRoZSB nb2xkIGV2aWRlbmNlIHRoYXQgdGhlIGFnZW50IGhhc24ndCB0cmllZC4KLSBTSE9VTEQgYmUgYSBzaW5nbGUgY29uY3JldGUgcXVlcnksIG5vdCBhIG11bHRpLXBhcnQgZGlzanVuY3R pb24uCgojIFJVTEVTIEZPUiBgZG9jaWRfdG9fZ2V0YCAgKG9ubHkgd2hlbiBkZWNpc2lvbj0ncmVwbGFjZV93aXRoX2dldF9kb2N1bWVudCcpCi0gSW50ZWdlciBtYXRjaGluZyBhIG RvY2lkIHRoYXQgYXBwZWFycyBpbiB0aGUgY3VtdWxhdGl2ZSByZXRyaWV2ZWQgc2V0IGF0IGhpc3RvcnlbOnJlcGxhY2VfaWRdLgooaS5lLiwgdGhlIGFnZW50IGhhcyBzZWVuIHRoaX MgZG9jaWQgYXMgYSBzZWFyY2ggc25pcHBldCBidXQgaGFzIE5PVCB5ZXQgZmV0Y2hlZCBpdHMgZnVsbCB0ZXh0LikKLSBQaWNrIGEgZG9jaWQgd2hvc2Ugc25pcHBldCBwcmV2aWV3I HN1Z2dlc3RzIGl0IGxpa2VseSBjb250YWlucyB0aGUgYW5zd2VyLgoKT3V0cHV0IHRoZSBKU09OIG9iamVjdCBvbmx5LiBObyBwcmVhbWJsZSwgbm8gY2xvc2luZyByZW1hcmtzLg==)

您正在审查研究智能体的推出。该智能体有四个工具——“搜索”、

‘get\_document‘, ‘manage\_context‘ (mc)、‘query\_memory‘ (qm) — 且任一达到错误

最终答案或用尽其回合预算而不做出承诺。

你的工作：找到一个MC步骤来替换为一个更有成效的行动。三种可能

干预，按照\*\*全局优先顺序\*\*（首先是操作类型，然后是最早的 mc 步骤）：

1. 提交——在某些 mc 步骤中，上下文证据已经足以回答。将 mc 呼叫替换为最终应答回合。

2. replace\_with\_search — 在某些 mc 步骤中，您建议的特定搜索查询比压缩更有效率。该查询不得与智能体已尝试过的任何查询重复。

3. replace\_with\_get\_document — 在某些 mc 步骤中，应该已获取先前搜索结果片段中已经可见的特定 docid。该docid必须位于history[:replace\_id].的累积检索集中

算法 - 全局操作优先级，所选操作中的最早步骤：

步骤 1. 按时间顺序扫描所有候选 mc 步骤。如果任何步骤都是可行的（

上下文证据支持此时的黄金答案），选择最早的此类步骤并

输出决策=“提交”。停止。

步骤 2. 否则（任何地方都没有可行的提交），按时间顺序扫描所有候选 mc 步骤。

如果任何步骤都是搜索可行的（您可以编写一个与之前不同的新颖的、高效的查询）

查询），选择最早的此类步骤并输出决策 = "replace\_with\_search". STOP。

步骤 3. 否则，按时间顺序扫描所有候选 mc 步骤。如果任何步骤是 get\_document-

可行（累积检索集中的特定 docid，如果获取，可能会产生

答案），选择最早的这样的步骤并输出决策="replace\_with\_get\_document".停止。

步骤 4. 否则，输出决策 = "no\_replacement\_possible".

关键：提交是全球最高优先级的操作。请勿短路

replace\_with\_search 只是因为提交在第 2 轮不可行——首先检查提交是否可行

在任何后续候选 mc 步骤中都是可行的。

# 问题

{问题}

# 黄金答案

{correct\_answer}

# 黄金证据（仅用于设计良好的search\_query或验证提交可行性）

{gold\_docs\_block}

# 特工轨迹（编号）

每条消息都以“[id=N, role=R]”为前缀。助手‘tool\_calls‘和工具响应是

内联。

{numbered\_history}

# 候选 mc 步骤

‘replace\_id‘ 必须是这些助理轮次 ID 之一（智能体调用manage\_context):

{candidate\_mc\_ids}

# DOCIDS 智能体已检索（累积，每个候选人 mc 回合）

您只能在“思考”/“解释”中引用这些文档。对于‘replace\_with\_get\_document‘,

‘docid\_to\_get‘ 必须是所选‘replace\_id‘. 中的其中之一

{retrieved\_docids\_by\_turn}

# 智能体之前的搜索查询（请勿对 ‘search\_query‘) 重复任何这些查询）

{prior\_search\_queries}

# 输出格式 — 严格的 JSON、一个对象、前后无散文

{

“决定”：“提交”| "replace\_with\_search" | "replace\_with\_get\_document" | "no\_replacement\_possible",

"replace\_id":<integer in CANDIDATE mc STEPS, or -1 if no\_replacement\_possible>，

“认为”：“<first-person student-voice reflection; see rules>”，

“基本原理”：“<one sentence to the experimenter — why THIS replace\_id and THIS action; for human review only>”，

// 决策字段='commit':

"解释": "<short BCP-style explanation; may cite retrieved docids; 1-3 sentences>",

"exact\_answer":“<final answer text, free-form>”，

“信心”：<integer 0-100>，

// decision=’replace\_with\_search’: 的字段

"search\_query":“<query string the agent should have issued instead of mc>”，

// decision=’replace\_with\_get\_document’: 的字段

"docid\_to\_get":<integer docid; MUST be in the cumulative retrieved set at history[:replace\_id]>

}

仅包含与您选择的决定相关的字段；忽略或取消其他。

# “思考”的规则

“思考”是智能体依次产生的第一人称推理‘replace\_id‘.

200-1500 个字符。必须作为真实的智能体推理来阅读。

决定要求：

- 提交：解释为什么上下文中的证据就足够了；引用检索到的文档。

- replace\_with\_search: 解释为什么先前的查询已停止以及为什么建议的查询目标

一个富有成效的新方向。

- replace\_with\_get\_document: 解释您正在跟踪哪个搜索结果片段，引用

始发docid\_to\_get.

在所有情况下都严格禁止：

- 引用不在 history[:replace\_id]. 累积检索集中的任何文档

- 教练框架词：“教练”、“辅导”、“反馈”、“评论”、“评论者”、“建议”、

‘指导’、‘告诉我’、‘有人说’、‘外部’、‘指示’。

- 提及用户、教师、培训师或任何外部团体。

# ‘search\_query‘ 的规则（仅当decision=’replace\_with\_search’)

- 长度：2-12 个字。

- 不得与“PRIOR SEARCH QUERIES”中的任何查询子字符串相等（不区分大小写）。

- 应使用从特工未尝试过的黄金证据中提取的独特术语。

- 应该是单个具体查询，而不是多部分析取。

# ‘docid\_to\_get‘ 的规则（仅当 decision=’replace\_with\_get\_document’) 时）

- 与 history[:replace\_id]. 处的累积检索集中出现的 docid 匹配的整数

（即，智能体已将此 docid 视为搜索片段，但尚未获取其全文。）

- 选择一个文档，其片段预览表明它可能包含答案。

仅输出 JSON 对象。没有序言，没有结束语。

### B.6 裁判（评分者）提示

最终答案由法学硕士法官使用官方的 simple-evals 模板进行评分。我们将其用于 BrowseComp-Plus 和 DeepSearchQA。

[⬇]（数据：文本/纯文本；base64，SnVkZ2Ugd2hldGhlciB0aGUgZm9sbG93aW5nIFtyZXNwb25zZV0gdG8gW3F1ZXN0aW9uXSBpcyBjb3JyZ WN0IG9yIG5vdcBiYXNlZCBvbiB0aGUgchHJlY2lzZSBhbmQKdW5hbWJpZ3VvdXMgW2NvcnJlY3RfYW5zd2VyXSBiZWxvdy4KCltxdWVzdGlvb l06IHtxdWVzdGlvbn0KCltyZXNwb25zZV06IHtyZXNwb25zZX0KCllvdXIganVkZ2VtZW50IG11c3QgYmUgaW4gdGhlIGZvcm1hdCBhbmQgY 3JpdGVyaWEgc3BlY2lmaWVkIGJlbG93OgoKW2NvcnJlY3RfYW5zd2VyXToge2NvcnJlY3RfYW5zd2VyfQoKZXh0cmFjdGVkX2ZpbmFsX2Fuc3 dlcjogVGhlIGZpbmFsIGV4YWN0IGFuc3dlciBleHryYWN0ZWQgZnJvbSB0aGUgW3Jlc3BvbnNlXS4gUHV0IHRoZSBleHRyYWN0ZWQKYW5zd2 VyIGFzICdOb25lJyBpZiB0aGVyZSBpcyBubyBleGFjdCwgZmluYWwgYW5zd2VyIHRvIGV4dHJhY3QgZnJvbSB0aGUgcmVzcG9uc2UuCgoKcm Vhc29uaW5nOiBFeHBsYWluIHdoeSB0aGUgZXh0cmFjdGVkX2ZpbmFsX2Fuc3dlciBpcyBjb3JyZWN0IG9yIGluY29ycmVjdCBiYXNlZCBvbg pbY29ycmVjdF9hbnN3ZXJdLCBmb2N1c2luZyBvbmx5IG9uIGlmIHRoZXJlIGFyZSBtZWFuaW5nZnVsIGRpZmZlcmVuY2VzIGJldHdlZW4gW2N vcnJly3RfYW5zd2VyXQphbmQgdGhlIGV4dHJhY3RlZF9maW5hbF9hbnN3ZXIuIERvIG5vdCBjb21tZW50IG9uIGFueSBiYWNrZ3JvdW5kIHR vIHRoZSBwcm9ibGVtLCBkbyBub3QgYXR0ZW1wdAp0byBzb2x2ZSB0aGUgcHJvYmxlbSwgZG8gbm90IGFyZ3VlIGZvciBhbnkgYW5zd2VyIGR pZmZlcmVudCB0aGFuIFtjb3JyZWN0X2Fuc3dlcl0sIGZvY3VzIG9ubHkgb24Kd2hldGhlciB0aGUgYW5zd2VycyBtYXRjaC4KCmNvcnJlY3Q 6IEFuc3dlciAneWVzJyBpZiBleHryYWN0ZWRfZmluYWxfYW5zd2VyIG1hdGNoZXMgdGhlIFtjb3JyZWN0X2Fuc3dlcl0gZ2l2ZW4gYWJvdmUs IG9yIGlzCndpdGhpbiBhIHNtYWxsIG1hcmdpbiBvZiBlcnJvciBmb3IgbnVtZXJpY2FsIHByb2JsZW1zLiBBbnN3ZXIgJ25vJyBvdGhlcndp c2UsIGkuZS4gaWYgdGhlcmUgaXMKYW55IGluY29uc2lzdGVuY3ksIGFtYmlndWl0eSwgbm9uLWVxdWl2YWxlbmN5LCBvciBpZiB0aGUgZXh0 cmFjdGVkIGFuc3dlciBpcyBpbmNvcnJly3QuCgpjb25maWRlbmNlOiBUaGUgZXh0cmFjdGVkIGNvbmZpZGVuY2Ugc2NvcmUgYmV0d2VlbiAw JSBhbmQgMTAwJSBmcm9tIFtyZXNwb25zZV0uIFB1dCAxMDAgaWYgdGhlcmUKaXMgbm8gY29uZmlkZW5jZSBzZWN0aW9uIGF2YWlsYWJsZS4=)

根据精确和正确的信息判断以下对[问题]的[回答]是否正确

明确如下[correct\_answer]。

[问题]：{问题}

[回复]：{回复}

您的判断必须采用以下指定的格式和标准：

[correct\_answer]:{correct\_answer}

extracted\_final\_answer: 从[回复]中提取的最终准确答案。把提取出来的

如果没有从响应中提取准确的最终答案，则回答“无”。

推理：根据以下内容解释为什么extracted\_final\_answer是正确或不正确的

[correct\_answer], 仅关注[correct\_answer] 之间是否存在有意义的差异

和extracted\_final\_answer.不要评论问题的任何背景，不要尝试

为了解决问题，不要争论任何不同于[correct\_answer],的答案，只关注

答案是否匹配。

正确：如果 extracted\_final\_answer 与上面给出的 [correct\_answer] 匹配，或者是

对于数值问题，误差范围很小。否则回答“否”，即如果有

任何不一致、歧义、不等价，或者提取的答案是否不正确。

置信度：从 [response] 中提取的介于 0% 和 100% 之间的置信度得分。如果有就填100

没有可用的置信部分。

·

## 附录C 探索多样性分析

### C.1 实验目的

为了调查我们的训练方法是否鼓励模型在长程检索期间探索不同的假设，我们测量了智能体在轨迹过程中“枢转”（即转向有意义的不同搜索方向）的频率。我们想要研究这个问题：与基本模型或标准 ReAct 智能体相比，使用记忆工具进行微调是否会导致更广泛、更多样化的信息搜索行为？

### C.2 实验设置

#### 枢轴检测。

在每个步骤tt，智能体发出搜索查询qtq\_{t}.我们使用双编码器（Qwen3-Embedding-8B)嵌入连续的查询对(qt−1,qt)(q\_{t-1},q\_{t})并计算它们的余弦相似度sts\_{t}.当st<τs\_{t}<\tau达到预定义阈值时声明*枢轴* τ\tau, 表示智能体已切换到性质不同的查询线路。

#### 枢轴分数。

我们计算*运行枢轴分数*：

|  |  |  |  |
| ---| ---| ---| ---|
|  | ft=1t∑i=1t𝟏[si<τ],f\_{t}=\frac{1}{t}{\sum\_{i=1}^{t}\mathbf{1}[s\_{i}<\tau]}, |  | (1) |

这是旋转到步骤 tt 的查询转换的比例。该数量限制在 [0,1][0,1] 范围内，并收敛于长期平均主元速率 t→∞t\to\infty,，而与总查询数无关。

#### 阈值τ\tau.

我们报告四个阈值下的结果τ∈{0.3,0.4,0.5,0.6}\tau\in\{0.3,0.4,0.5,0.6\}（图[7](https://arxiv.org/html/2607.23809#A3.F7“图7‣C.3结果和分析‣附录C探索多样性分析‣ACM：长期任务的智能体上下文管理”））。较低的阈值需要较大的语义转变才能算作枢轴（更严格的标准）；门槛越高，越宽松。跨多个阈值的报告可以防止对任何单一选择的敏感性。

#### 相对进度轴。

水平轴通过除以轨迹的总词元预算，将每个轨迹的词元位置归一化为 [0,1][0,1]。这确保了每个轨迹（无论长度如何）对每个位置箱都有统一的贡献，从而消除了由于 ReAct 轨迹比 ACM/ACM-Post-Trained 轨迹短而可能出现的生存偏差。

### C.3 结果与分析

![参考说明](https://arxiv.org/html/2607.23809v1/figs/analysis_exploration.png)

图 7：在 ReAct、ACM 和 ACM-Post-Trained 的相对轨迹进度上运行枢轴分数，跨越四个余弦相似性阈值 τ\tau. 阴影带表示跨轨迹的 ±\pm1 标准差。

#### 培训鼓励探索。

如图 [7](https://arxiv.org/html/2607.23809#A3.F7“图 7 ‣ C.3 结果和分析 ‣ 附录 C 探索多样性分析 ‣ ACM：长期任务的智能体上下文管理”），ACM-Post-Trained（橙色）在整个轨迹的所有四个阈值上始终保持比 ACM（绿色）和 ReAct（蓝色）更高的枢轴分数。差距在τ=0.6\tau=0.6,处清晰可见，其中 ACM-Post-Trained 稳定在大约 0.500.50–0.550.55，而 ACM 和 ReAct 均收敛于 0.450.45–0.500.50 附近。值得注意的是，ACM 在所有阈值上密切跟踪 ReAct，这表明单独访问记忆工具（没有相应的训练信号）不会引起太多的探索行为。

####跨阈值的稳健性。

ACM-Post-Trained 在每个阈值下都实现了最高的平均枢轴分数 τ∈{0.3,0.4,0.5,0.6}\tau\in\{0.3,0.4,0.5,0.6\}. 尽管绝对差距在较高阈值下缩小，但相对顺序始终保持不变，这证实了行为差异不是任何特定相似性截止的人为因素。

#### 轨迹之间的高方差。

如图 [7](https://arxiv.org/html/2607.23809#A3.F7“图 7 ‣ C.3 结果和分析 ‣ 附录 C 探索多样性分析 ‣ ACM：长期任务的智能体上下文管理”）中的宽标准差带所示，枢轴行为在每个设置中表现出显着的轨迹间变化，这归因于基础任务的固有多样性。尽管存在这种差异，设置之间的相对顺序仍然保持一致 - ACM-Post-Trained 在所有轨迹位置和阈值上保持比 ACM 和 ReAct 更高的平均枢轴分数。

## 附录 D 案例研究：小型思维模型无法运用情境管理工具

一个自然的问题是，主论文中报告的上下文管理收益是否会转移到更小的思维蒸馏模型，例如Qwen3-4B-thinking。我们发现它们没有，因为工具本身的“上游”原因：在这种规模下，模型将每次 BrowseComp-Plus 推出折叠成两轮轨迹（一次浅搜索，然后猜测），并且永远不会达到manage\_context或query\_memory有任何工作要做的状态。表[4](https://arxiv.org/html/2607.23809#A4.T4“表4‣附录D案例研究：小型思维模型无法运用上下文管理工具‣ACM：长期任务的智能体上下文管理”)将推出统计数据与主论文中使用的9B基线进行比较，表[5](https://arxiv.org/html/2607.23809#A4.T5“表5‣附录D案例研究：小型思维”模型无法运用上下文管理工具‣ ACM：长期任务的智能体上下文管理”）追踪了一个代表性示例，图 [8](https://arxiv.org/html/2607.23809#A4.F8“图 8 ‣附录 D 案例研究：小型思维模型无法执行上下文管理工具‣ ACM：长期任务的智能体上下文管理”）重现了解释提前终止的逐字思维文本。

有两个观察结果值得强调。首先，4B 和 9B 之间的差距是“推理能力”差距，而不是上下文管理差距：9B 基线每个问题发出的工具调用多出一个数量级（16.2 比 1.2），并且运行次数几乎是其十倍（平均 19.4 比 2.0），在相同基准上，准确率分别为 57.3% 和 3.4%。其次，4B 模型的放弃并不是断章取义。当它承诺对一个抽样问题给出最终答案时，它仅消耗了 131K 词元预算中的 23K，并明确地自我报告（图 [8](https://arxiv.org/html/2607.23809#A4.F8“图 8 ‣ 附录 D 案例研究：小型思维模型无法运用上下文管理工具 ‣ ACM：长期任务的智能体上下文管理”)，蓝色）它“可以做到”更多搜索。”然而，在下一个句子（红色）中，它产生了“我无法进行真正的搜索”这一约束的幻觉，并以低置信度的猜测结束。上下文管理是“长期”部署的一个属性：在第 2 轮终止且使用的预算 <20%<\!20\% 的策略永远不会进入压缩或检索能够获得回报的状态，因此推理时间评估和 RL 训练都无法将任何信号归因于这些工具。因此，我们使用Qwen3.5-9B——这个系列中最小的模型，它产生足够长的轨迹，使上下文管理发挥作用——作为整个主要论文的策略。

问题（BrowseComp-Plus，qid 124）。 “一位艾美奖得主在 2018 年发表了一篇关于纸牌游戏起源的文章。该作者还撰写了一系列儿童读物，在 2020 年的一篇文章中引用了一位名字和姓氏都以 KW 开头的作者所写的文章。KW 引用了什么作为该系列的标题？”黄金答案：神奇妈妈故事 标准答案：生命的游戏（置信度 70%，错误）。

|型号|圈数（平均/最大）|搜索 |附件|
| ---| ---| ---| ---|
| Qwen3-4B-thinking | 2.0 / 2 | 1.2 | 1.2 3.4% |
| Qwen3.5-9B | 19.4 / 46 | 16.2 | 16.2 57.3% |

表 4：ReAct 框架下 BrowseComp-Plus 上的推出长度崩溃。 Qwen3-4B-thinking 通过 ∼\sim1 工具调用在恰好两圈处终止每次推出，比主论文中使用的 9B 基线短一个数量级。准确率差距（3.4% vs. 57.3%）是由这种崩溃造成的，而不是由于缺乏上下文管理工具。

| qid 124 (Qwen3-4B-thinking) 上的轨迹形状 | |
| ---| ---|
| turn 1 | 20,599 chars of thinking →\to search(…) (1 call). Query: “Emmy award winner 2018 article card game origins”. |
|工具|返回 10 条文档； *没有*提到艾美奖+纸牌游戏+儿童读物。 |
| turn 2 | 7,104 chars of thinking →\to final answer (no further tool calls). |
| total | 1 tool call, 2 turns, 50 s, ∼\sim23K / 131K tokens used. |

表 5：qid 124 上的轨迹形状。该模型发出单个广泛搜索，接收无用文档，并在不进行任何进一步检索的情况下进行猜测。终止时的词元使用量是可用预算的∼\sim18%——没有需要管理的上下文压力。

Turn-2思维痕迹（逐字摘录，单次搜索后没有返回任何有用的文档）。
  
*“嗯，也许关键在儿童读物部分。 ……
搜索结果似乎没有任何有关纸牌游戏的直接信息
艾美奖得主的文章。 ……或者，答案是“游戏”
的生活’作为常见的儿童读物系列标题。”*
*“当前上下文词元是 23,033，
仍然低于 131,072 的限制，所以我可以进行更多搜索。
让我尝试另一个搜索：“儿童读物艾美奖得主卡”
游戏’。*
*但是由于我无法进行真正的搜索，所以我
必须思考。”*
*“鉴于我花费的时间以及缺乏直接信息
搜索结果中，我会选择“The Game of Life”作为答案，
70 % 的置信度。”*

图 8：模型为何提前终止。蓝色的 4B 模型正确地自我报告，它仅使用了 131K 词元预算中的 23K，并且“可以”继续搜索；在下一个句子（红色）中，它会产生“我无法进行真正的搜索”的约束并做出猜测。失败不是上下文预算失败，而是未能维持长期计划，因此上下文管理工具没有机会提供帮助。

