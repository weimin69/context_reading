> 本文为简体中文机器翻译，使用 Google Translate 公开接口并统一技术术语，尚未经逐句人工校对。代码、链接和公式按原文保留；实验数字及技术结论请对照原文。
> [查看本地英文原文](../../collection/papers/2026-08-06-Towards-Reliable-Context-Compression-for-Long-Horizon-Agents-An-Empirical-Study-of-Execution-Instabi-d88aafae.md) · [原始来源](https://arxiv.org/abs/2608.06503)

# 迈向长程智能体的可靠上下文压缩：执行不稳定性的实证研究

- 来源: https://arxiv.org/abs/2608.06503- 发布日期: 2026-08-06- 日期依据: page metadata: citation_date- 类型: paper- 主题: 压缩可靠性、长程Agent- 抓取状态: full_text_html- 正文来源: https://arxiv.org/html/2608.06503- 抓取时间 UTC: 2026-10-26T09:35:23.034501+00:00 - 作者: Min, Guanghui, Wu, Liang, Darbari, Mayank, Chen, Chen, Hong, Liangjie

## 来源摘要/页面简介

摘要：周期性上下文压缩控制着长程智能体的上下文增长，但其行为影响仍然知之甚少。在这项初步的实证研究中，我们表明压缩可以削弱最近相互作用的影响，增加阻塞动作、重复探索和运行中的不稳定性。受这些观察的启发，我们引入了 TRACE，这是一个验证者引导的框架，它通过来自同一环境状态的成对闭环延续来评估单个压缩事件，并使用摘要偏好来优化自然语言压缩提示，同时保持所有模型冻结。 AppWorld 的初步结果显示，在任务性能、多运行可靠性和上下文执行效率方面，现有压缩基准有所改进。这些发现为边界局部评估提供了早期证据，作为可靠的智能体上下文压缩的有希望的方向。

## 抓取正文（中文翻译）

# 面向长程智能体的可靠上下文压缩：执行不稳定性的实证研究

闵光辉 单位：美国弗吉尼亚州夏洛茨维尔弗吉尼亚大学计算机科学系 单位：美国加利福尼亚州桑尼维尔市诺基亚 电子邮件：[jjm8vr@virginia.edu](mailto:)
  
吴亮 单位：美国加利福尼亚州桑尼维尔市诺基亚电子邮件：[zrh6du@virginia.edu](mailto:)
  
Mayank Darbari 所属机构：美国加利福尼亚州桑尼维尔市诺基亚电子邮件：[liang.wu@nokia.com](mailto:)
  
Chen Chen 单位：美国弗吉尼亚州夏洛茨维尔弗吉尼亚大学计算机科学系电子邮件：[mayank.darbari@nokia.com](mailto:)
  
洪亮杰 单位：美国加利福尼亚州桑尼维尔市诺基亚电子邮件：[liangjie.hong@nokia.com](mailto:)

###### 摘要

周期性上下文压缩控制着长程智能体的上下文增长，但其行为影响仍然知之甚少。在这项初步的实证研究中，我们表明压缩可以削弱最近相互作用的影响，增加阻塞动作、重复探索和运行中的不稳定性。受这些观察的启发，我们引入了 TRACE，这是一个验证者引导的框架，它通过来自同一环境状态的成对闭环延续来评估单个压缩事件，并使用摘要偏好来优化自然语言压缩提示，同时保持所有模型冻结。 AppWorld 的初步结果显示，在任务性能、多运行可靠性和上下文执行效率方面，现有压缩基准有所改进。这些发现为边界局部评估提供了早期证据，作为可靠的智能体上下文压缩的有希望的方向。我们的代码位于<https://github.com/nokia-applied-research/Trace>。

|  |
| ---|
|  |

## 1 简介

大型语言模型越来越多地在长期、不断变化的上下文中运行，而不是在孤立的提示下运行。此类设置包括交叉推理、行动、观察和计划修订的交互智能体（[Yao et al., 2023](https://arxiv.org/html/2608.06503#bib.bib1)；[Shinn et al., 2023](https://arxiv.org/html/2608.06503#bib.bib2)；[Wang et al., 2024b](https://arxiv.org/html/2608.06503#bib.bib3))；需要与外部系统进行扩展交互的浏览器、应用程序、API 和办公环境（[Zhou et al., 2024](https://arxiv.org/html/2608.06503#bib.bib23)；[Trivedi et al., 2024](https://arxiv.org/html/2608.06503#bib.bib24)；[Wang et al., 2024c](https://arxiv.org/html/2608.06503#bib.bib25)）；受策略约束的对话工作流程；以及通过多个步骤积累证据的检索密集型研究任务。在所有这些设置中，上下文随着每个工具输出、检索的源、中间决策、用户澄清和部分结果而增长。重复提供完整的历史记录会增加推理成本和峰值上下文压力，同时使下一个决策所需的信息越来越难以定位。因此，上下文压缩对于可扩展的长期 LLM 系统至关重要。

之前的工作已逐步从文档级提示压缩转向轨迹感知上下文管理。一般提示压缩方法会修剪、重写或提取输入标记，以降低推理成本，同时保留语义内容或下游任务质量（[Li et al. 等，2023](https://arxiv.org/html/2608.06503#bib.bib5)； [Jiang 等，2023](https://arxiv.org/html/2608.06503#bib.bib6)； [Jiang et al., 2024](https://arxiv.org/html/2608.06503#bib.bib7)； [潘等人，2024](https://arxiv.org/html/2608.06503#bib.bib8)； [徐等人，2024](https://arxiv.org/html/2608.06503#bib.bib9)； [Shandilya 等人，2025](https://arxiv.org/html/2608.06503#bib.bib10))。对于长程智能体，最近的方法认识到上下文包含的内容比普通智能体更多 散文：它 记录行动观察历史、中间计划和不断变化的交互状态。因此，ReSum 和 SUPO 与下游智能体行为共同优化摘要（[Wu et al., 2025](https://arxiv.org/html/2608.06503#bib.bib17)；[Lu et al., 2025](https://arxiv.org/html/2608.06503#bib.bib18)）； ACON 通过对比成功的全上下文轨迹与失败的压缩轨迹来改进压缩指南（[Kang et al., 2026](https://arxiv.org/html/2608.06503#bib.bib19)）；实用系统将长会话压缩为结构化自然语言检查点（[OpenClaw 贡献者，2026a](https://arxiv.org/html/2608.06503#bib.bib20)；[OpenClaw 贡献者，2026b](https://arxiv.org/html/2608.06503#bib.bib21)；[Nous 研究， 2026](https://arxiv.org/html/2608.06503#bib.bib22))。这些进步表明，智能体上下文应该与静态文档区别对待。

然而，这些方法都有一个隐含的替代假设：一旦较短的检查点保留了与任务相关的内容，它就可以代替原始的交互历史。这种假设忽视了历史在长期执行中的方向性作用。原始轨迹不仅记录事实，而且记录事实。它的有序操作-观察序列锚定了已经完成的内容、当前执行的位置以及任务是否准备好终止。总结可以将这个定向过程扁平化为对过去进展和未来计划的声明性描述。因此，即使保留显着实体和进度标签，冻结智能体也可能会失去其在轨迹中的本地位置、重放已完成的动作或继续在终端边界之外执行操作。因此，核心挑战是压缩历史记录，同时保留表示，冻结智能体可以从中可靠地识别其当前执行状态。

我们提出了 TRACE（Trajectory-Relative 智能体 上下文压缩），这是一个验证者引导的框架，用于优化冻结长程智能体的循环上下文压缩。 TRACE 不是从最终任务结果推断压缩质量，而是直接评估每个压缩边界。从相同的环境状态，它比较压缩前后的成对闭环延续，并测量由摘要引起的额外阻塞或重复探索。这些边界局部分数产生候选摘要之间的偏好。冻结的提议者仅观察首选的摘要，而不是后续的操作、观察或错误信号，并使用这些偏好来修改自然语言压缩模板。压缩器模型、下游智能体、工具和解码配置始终保持固定。

我们的贡献有三方面：

*•

  行为诊断。
  我们表明，反复压缩可以减弱最近的影响
  交互，增加阻塞执行和重复探索
  降低多次运行的可靠性。
*•

  边界局部压缩优化。
  我们引入了一个配对的闭环验证器，可以将
  压缩引起的执行回归来自冻结智能体的内在
  行为变异性，并使用其摘要偏好来优化
  压缩模板而不向提议者暴露推出细节。
*•

  实证评价。
  在 AppWorld 上，TRACE 始终优于现有压缩
  跨任务难度级别的基线，提高重复运行的可靠性，以及
  保持平均执行步骤接近完整上下文，同时大幅减少
  峰值上下文使用情况。此外，模板还通过 MiniMax-M3 传输进行了优化
  Kimi-K2.7-Code 无需进一步优化，性能优于所有压缩
  整体准确度和 Pass2 方面甚至超过了完整上下文。

## 2 预备赛

### 2.1 冻结长程智能体的上下文压缩

注释。我们研究与外部环境交互的固定下游智能体ℳ\mathcal{M}的上下文压缩ℰ\mathcal{E}.智能体是固定的，因为它的语言模型、系统提示、操作界面、输出解析器和解码过程都没有修改。令 𝒟={ui}i=1|𝒟|\mathcal{D}=\{u\_{i}\}\_{i=1}^{|\mathcal{D}|} 表示长程任务的分布，其中每个任务以指令 uu 开始。推出由τ=(u,a1,o1,…,aT,oT)\tau=(u,a\_{1},o\_{1},\ldots,a\_{T},o\_{T}).表示，在决策步骤tt之前，完整的交互历史记录为ht=(u,a1,o1,…,at−1,ot−1)h\_{t}=(u,a\_{1},o\_{1},\ldots,a\_{t-1},o\_{t-1}),，其中aia\_{i}是智能体操作，oi=ℰ⁡(ai)o\_{i}=\mathcal{E}(a\_{i})是相应的环境观察。我们将完整的交互历史hth\_{t}与提供给冻结智能体的智能体可见上下文ztz\_{t}区分开来。给定ztz\_{t},，智能体生成at∼ℳ(⋅∣zt)a\_{t}\sim\mathcal{M}(\cdot\midz\_{t})并接收ot=ℰ⁡(at)o\_{t}=\mathcal{E}(a\_{t}).全上下文执行使用zt=htz\_{t}=h\_{t}.自|ht||h\_{t}|通常随着 tt 的增长，完整的历史最终可能会超出长期执行的实际上下文预算。

### 2.2 问题定义

长程智能体必须定期用有界文本表示替换其不断增长的工作环境（[Kang et al., 2026](https://arxiv.org/html/2608.06503#bib.bib19); [Lu et al., 2025](https://arxiv.org/html/2608.06503#bib.bib18); [Wang et al., 2024a](https://arxiv.org/html/2608.06503#bib.bib26); [Nous Research, 2026](https://arxiv.org/html/2608.06503#bib.bib22)；[OpenClaw 贡献者，2026a](https://arxiv.org/html/2608.06503#bib.bib20))。让 𝒞\mathcal{C} 表示压缩器，BB 表示上下文预算。给定当前智能体可见上下文ztz\_{t},操作ata\_{t},和观察oto\_{t},将预压缩上下文定义为z¯t+1=zt⊕(at,ot)\bar{z}\_{t+1}=z\_{t}\oplus(a\_{t},o\_{t}),其中⊕\oplus表示文本连接。下一个决策步骤提供的上下文将递归更新为

|  |  |  |  |
| ---| ---| ---| ---|
|  | zt+1={z¯t+1,|z¯t+1|≤B,𝒞⁡(z¯t+1,B),|z¯t+1|>B.z\_{t+1}=\begin{cases}\bar{z}\_{t+1},&|\bar{z}\_{t+1}|\leq B,\\ \mathcal{C}(\bar{z}\_{t+1};B),&|\bar{z}\_{t+1}|>B.\end{cases} |  | (1) |

因此，在压缩事件之后，替换上下文zt+1z\_{t+1}成为冻结智能体和后续压缩步骤可用的唯一历史记录。对于压缩器 𝒞\mathcal{C}, 让 p𝒞,B​(τ∣u)p\_{\mathcal{C},B}(\tau\mid u) 表示由冻结智能体 ℳ\mathcal{M}, 环境 ℰ\mathcal{E}, 和方程[1]中的递归上下文转换引起的转出分布（https://arxiv.org/html/2608.06503#S2.E1“方程 1 ‣ 2.2 问题定义‣ 2 预备知识‣ 实现长程智能体的可靠上下文压缩：执行不稳定性的实证研究》）。让R⁡(τ)R(\tau)表示环境定义的终端奖励。

## 3 实证研究：情境压缩的行为影响

在本节中，我们首先表明循环压缩会降低任务的成功率和可靠性，尤其是在较长的轨迹上。然后，我们将这种退化追溯到执行状态错误定位，并检查它如何表现为阻塞执行和压缩后的重复探索。

### 3.1 重复压缩会降低智能体行为

(a) 压缩性能。

(b) 交叉运行行为不稳定。

(c) 长期退化。

图 1：尽管可重新获取信息，但重复的上下文替换会降低智能体行为。 AppWorld 允许智能体重新查询持久应用程序状态，因此先前观察到的信息在压缩后仍然可恢复。 (a) 随着背景预算的缩减，平均通过率下降。 (b) P​@​2P@2 和 P2P^{2} 之间不断扩大的差距表明重复运行的可靠性降低。 (c) 即使使用基于摘要的压缩，对于具有较长全上下文参考范围的任务来说，退化也会严重得多。

Equation ([1](https://arxiv.org/html/2608.06503#S2.E1 "Equation 1 ‣ 2.2 Problem Definition ‣ 2 Preliminaries ‣ Towards Reliable 上下文压缩 for Long-Horizon 智能体: An Empirical Study of Execution Instability")) makes 上下文压缩 a recurrent intervention: once the working 上下文 exceeds the budget, the replacement 上下文 becomes the input to both subsequent decisions and later compaction事件。因此，不能通过单独的替代品来单独评估其质量。一旦被反复重用为智能体的工作环境，本地合理的摘要仍然可能会改变下游的部署。

我们评估了对 147 任务 AppWorld 训练-开发拆分的影响（[Trivedi et al., 2024](https://arxiv.org/html/2608.06503#bib.bib24)）。 AppWorld is a stateful API-use benchmark: 智能体 interact with persistent simulated applications through API calls, and earlier observations can be recovered by re-querying the underlying application state. This setting differs from knowledge-intensive tasks, where summary-based 压缩整合 is expected to outperform FIFO truncation because it preserves facts that would otherwise be permanently discarded.在 AppWorld 中，从工作上下文中删除观察并不一定会导致其内容永久无法访问。我们使用 MiniMax-M3 作为压缩机和下游智能体（[MiniMax，2026](https://arxiv.org/html/2608.06503#bib.bib27)）。 Our evaluation harness adapts OpenClaw’s recurrent 压缩整合 loop11 1 Adapted from the OpenClaw 智能体-core harness, <https://github.com/openclaw/openclaw/blob/0e7b5c34292cc28707a0e5a0b730cff295ef0f8a/packages/agent-core/src/harness/compaction/compaction.ts> (commit 0e7b5c34292cc28707a0e5a0b730cff295ef0f8a). （[OpenClaw 贡献者，2026a](https://arxiv.org/html/2608.06503#bib.bib20)）。 This common runtime pattern is also used in other agentic frameworks such as AG2 and Hermes 智能体 ([Wang et al., 2024a](https://arxiv.org/html/2608.06503#bib.bib26); [Nous Research, 2026](https://arxiv.org/html/2608.06503#bib.bib22)).

Figure [1](https://arxiv.org/html/2608.06503#S3.F1 "Figure 1 ‣ 3.1 Repeated Compression Degrades 智能体 Behavior ‣ 3 Empirical Study: Behavioral Effects of 上下文压缩 ‣ Towards Reliable 上下文压缩 for Long-Horizon 智能体: An Empirical Study of Execution Instability") reveals a surprising budget-dependent pattern. Summary-based 压缩整合 does not uniformly outperform FIFO truncation: at 1616K, 88K, and 44K, FIFO matches or slightly exceeds summary-based execution.它们的差异仅在最紧张的预算下才会出现，其中基于摘要的压缩达到 72.8%72.8%，而 FIFO 下降到 42.2%42.2%。 Thus, in this information-refetchable setting, the advantage of summarization over recency-only truncation appears only under severe compression.然而，这两项政策仍低于全面绩效。

仅平均通过率并不能完全表征这种退化。遵循τ\tau-bench和τ2\tau^{2}-bench 中使用的重复运行可靠性指标（[Yao et al., 2025](https://arxiv.org/html/2608.06503#bib.bib30); [Barres et al., 2025](https://arxiv.org/html/2608.06503#bib.bib29))，PkP^{k} 表示所有任务中解决的任务比例kk 独立运行，而 P​@​kP@k 表示至少在一次 kk 运行中求解的分数。我们始终使用 k=2k=2。在更强的压缩下，P​@​2P@2 和 P2P^{2} 之间的差距大幅拉大。因此，压缩不仅仅从智能体的可达范围中删除任务子集：它将一些可靠解决的任务转换为仅在相同运行时条件下间歇性解决的任务。

这种不稳定性在具有较长全上下文执行范围的任务上更为明显，这是通过成功的全上下文运行中的步骤中位数来衡量的。即使在基于摘要的压缩下，随着预算的缩减，长期任务的退化也会更加剧烈，这与重复上下文替换的累积效应一致。

总之，这些结果表明，成功的压缩不仅取决于保留全局相关信息，还取决于维持锚定智能体当前执行位置的局部连续性。尽管丢弃了最早期的历史，先进先出保留了最近的动作观察连续性，而重复的摘要替换可能会逐渐削弱较长轨迹上的局部锚点。接下来我们在匹配的决策点隔离这种影响。

要点：与单独的单次运行性能相比，多次运行稳定性能更好地反映压缩机质量。

### 3.2 超越信息丢失：执行状态错误定位

图 2：终端完成。总高度表示终止率；黑色部分表示以所需形式终止。

[3.1]节（https://arxiv.org/html/2608.06503#S3.SS1“3.1 重复压缩降低智能体行为‣ 3 实证研究：上下文压缩的行为影响‣ 实现长程智能体的可靠上下文压缩：执行不稳定性的实证研究”）中的降级通常归因于摘要过程中事实、变量或任务进度的丢失。这个说明在我们的设置中是不完整的：早期的观察结果在 AppWorld 中仍然可以重新查询，而 FIFO 截断尽管丢弃了大多数早期历史，但在适度的预算下仍然具有竞争力。因此，我们要问压缩是否也会削弱智能体恢复其当前执行状态的能力——什么已经完成，什么仍然可操作，以及执行应该继续还是终止。

摘要 更换会中断终端的完成。我们首先在终止前探讨最终决定。对于至少进行一次压缩的每条轨迹，我们固定任务、环境、智能体头和决策点，并比较实际的摘要上下文、相同预算下的 FIFO 截断以及完整的终端前历史记录。所有回合均以其本机交互格式重建，并且我们在每次渲染下对 1010 个下一步动作进行采样。

图 [2](https://arxiv.org/html/2608.06503#S3.F2“图 2 ‣ 3.2 超越信息丢失：执行状态误定位 ‣ 3 实证研究：上下文压缩的行为影响 ‣ 实现长程智能体的可靠上下文压缩：执行不稳定性的实证研究”）显示，在 22K 时，汇总条件仅终止于44.6%44.6\% 的样本，其中 37.3%37.3\% 使用所需的形式，而 FIFO 为 77.2%77.2\%/68.1%68.1\%，完整历史记录为 66.6%66.6\%/60.6%60.6\%。赤字持续在 44K 和 88K。当正确完成不需要实质性响应时，这种情况最为明显：摘要条件智能体更经常继续行动或提供不必要的内容，而不是直接终止。因此，摘要替换会损害完成识别和对所需输出形式的遵守。

要点：压缩会削弱行动承诺和对所需输出形式的遵守。

压缩会削弱最近的交互更新。接下来我们检查这种效果是否在摘要的整个生命周期中持续存在。对于每次压缩，让 St−1S\_{t-1} 表示先前的摘要，Δt\Delta\_{t} 表示新的原始交互历史记录，St=C⁡(St−1,Δt)S\_{t}=C(S\_{t-1},\Delta\_{t}) 表示更新的摘要。在下一次压缩之前的每个记录的决策边界上，我们构建四个匹配的上下文：完整的原始前缀； St−1S\_{t-1} 随后是未压缩的 Δt\Delta\_{t}; 更新后的摘要 StS\_{t}; 和 St−1S\_{t-1}，其中省略了 Δt\Delta\_{t}。每个条件后面都跟有相同的记录后缀，并在相同的决策点结束。

图 3：近期互动的效果。当新的交互历史记录被逐字保留、压缩或省略时，与完整历史记录行为的背离。误差线表示任务级别 95%95% bootstrap 置信区间。

我们在每个上下文下独立采样 2424 个下一步动作。采样的操作既不会执行，也不会反馈给智能体。我们规范化主要 API 调用，并计算其与完整历史分布的噪声校正总变异散度，首先对摘要生命周期中的所有决策点进行平均，然后对任务进行平均。图[3](https://arxiv.org/html/2608.06503#S3.F3“图3‣3.2超越信息丢失：执行状态错误定位‣3实证研究：上下文压缩的行为影响‣走向长程智能体的可靠上下文压缩：执行不稳定性的实证研究”）显示了明显的梯度。保留原始更新会产生最小的分歧 (0.1490.149)；将其压缩到更新的摘要中将散度增加到 0.2330.233；完全省略它会产生最大的偏移 (0.2890.289)。因此，OpenClaw 保留了最近交互的部分行为影响，但相对于逐字保留它们，系统地削弱了它。

总之，这些探测发现了循环压缩的一个常见功能故障：应修改执行的最近交互在被吸收到摘要中后对后续决策产生较弱或扭曲的影响。这可能是由于遗漏信息、扭曲进度或保留信息使用不当造成的；我们的实验并没有完全区分这些原因。目标修改、工具失败、意外结果和完成事件之所以重要，正是因为它们应该改变智能体的继续方式。这促使使用其下游执行结果而不是最终结果或静态文本保真度来评估发生压缩的边界。

### 3.3 压缩引发回归探索

前面的干预表明，压缩保留了最近互动的部分行为影响，但相对于逐字保留它们而言，它减弱了。接下来我们研究这种衰减在闭环执行期间如何表现。

在每个压缩边界，我们恢复相同的 AppWorld 执行状态，并在两个上下文渲染下独立推出冻结的智能体。 PRE 保留压缩之前可用的原始交互更新，而 POST 使用更新的摘要以及 OpenClaw 保留的原始轮流。这些是使用原始 AppWorld 工具的自由运行闭环部署：执行每个生成的操作，并在下一个决策之前返回其实际观察结果。我们评估了 590590 个边界和 4,6404{,}640 个展开，每次渲染使用 5 个样本进行首次压缩，使用 3 个样本进行后续压缩，每个样本最多执行 5 个操作。

图 4：阻塞执行和回归探索。压缩后前五个操作中每个操作的边际 POST-minus-PRE 效果。阻止/错误操作遵循 AppWorld 的本机错误契约；重新获取/重播表示先前在边界之前或同一推出中较早观察到的确切操作签名。 Error bars denote boundary-level 95%95\% bootstrap confidence intervals.

图 [4](https://arxiv.org/html/2608.06503#S3.F4“图 4 ‣ 3.3 压缩引发回归探索 ‣ 3 实证研究：上下文压缩的行为影响 ‣ 实现长程智能体的可靠上下文压缩：执行不稳定性的实证研究”）报告了每个操作步骤的边际效应，而不是该步骤的累积效应。压缩会立即增加阻塞执行：POST 在第一个操作中比 PRE 产生多 0.1080.108 个阻塞/错误操作，并且在整个延续过程中效果保持积极。重新取值最初较弱 (0.0310.031)，但在第二次操作时上升，此后保持正值。

这种时间模式与最近交互更新减弱的两个互补后果是一致的。压缩首先可以使先前建立的执行状态难以直接访问，从而产生显式块，并随后引发额外的工作来恢复或重建该状态。因此，保留的信息可以保持可恢复，同时对于继续执行来说变得不太可操作。

结论：压缩增加了回归探索，削弱了上下文窗口中保留的交互的影响。

## 4 Trace：优化压缩提示

第 [3] 节（https://arxiv.org/html/2608.06503#S3“3 实证研究：上下文压缩的行为影响 ‣ 实现长程智能体的可靠上下文压缩：执行不稳定性的实证研究”）表明，压缩会使最近建立的执行状态变得不太可操作，从而导致操作受阻和重复探索。 TRACE，如图 [5](https://arxiv.org/html/2608.06503#S4.F5“图 5 ‣ 4.1 边界局部执行验证器 ‣ 4 Trace：优化压缩提示 ‣ 实现长程智能体的可靠上下文压缩：执行不稳定性的实证研究”）所示，将此观察结果转换为边界局部优化信号。所有模型参数保持冻结：我们仅优化压缩器使用的自然语言压缩模板。

先前的提示优化方法（例如 ACON）从轨迹构建反馈，其中智能体在完整上下文中成功，但在压缩上下文中失败（[Kang et al., 2026](https://arxiv.org/html/2608.06503#bib.bib19)）。然而，这种轨迹级监督无法将压缩引起的错误与智能体的内在行为变化和下游意外事件隔离开来。成功的轨迹并不意味着每个中间压缩都是忠实的，因为压缩缺陷可能永远不会被执行或可能通过随后的环境交互来恢复。相反，失败的轨迹并不意味着其总结很差，因为失败可能与压缩无关。因此，我们使用来自相同执行状态的成对闭环延续直接在各个压缩边界构建监督。

### 4.1 边界局部执行验证器

我们的验证器测量压缩事件是否引入了额外的可观察执行回归，可操作为被环境阻止的操作或重复已执行的工具调用。我们不是将最终的任务结果归因于轨迹上的每个摘要，而是在它替换原始交互历史的边界处本地评估每个摘要。

考虑压缩边界 bb。让 xb−x\_{b}^{-} 表示替换之前的上下文，由先前的循环摘要（如果有）组成，后面是新累积的原始交互。给定一个候选摘要 ss，让 xb+​(s)x\_{b}^{+}(s) 表示相应的压缩后上下文，包括压缩策略保留的最近的原始轮次。

从相同的环境状态开始，我们在xb−x\_{b}^{-}和xb+​(s)x\_{b}^{+}(s).下独立推出冻结智能体。PRE和POST延续都是完全闭环的：生成的动作通过原始工具执行，并将结果观察结果返回给智能体。因此，PRE 充当冻结智能体的内在执行行为的配对本地控制，而 POST 则捕获通过用摘要 ss 替换历史记录而引起的任何额外负担。

![参考说明](https://arxiv.org/html/2608.06503v2/trace_pipeline.png)

图 5：TRACE 概述。在每个压缩边界，从相同的环境状态评估成对的闭环延续。 PRE 保留压缩之前可用的上下文，而 POST 用候选摘要替换可压缩历史记录。验证者测量由此导致的被阻止或重复操作的增加，并对候选摘要进行排名。冻结的提议者接收下游系统提示、现有压缩提示以及由此产生的摘要偏好，但不接收转出操作、观察结果、错误或验证者分解。然后，它会生成候选压缩模板，这些模板是通过对开发拆分进行端到端评估来选择的。

让zj​(τ)z\_{j}(\tau)指示连续τ\tau中的第jj个动作是否构成可观察的执行回归。我们将短期执行负担定义为

|  |  |  |  |
| ---| ---| ---| ---|
|  | G⁡(τ)=∑j=1Kzj​(τ),G(\tau)=\sum\_{j=1}^{K}z\_{j}(\tau), |  | (2) |

其中 KK 是固定的推出范围。候选摘要 ss 的压缩引起的负担为

|  |  |  |  |
| ---| ---| ---| ---|
|  | Δ​Gb​(s)=𝔼⁡[G⁡(τb+​(s))]−𝔼⁡[G⁡(τb−)],\Delta G\_{b}(s)=\mathbb{E}\!\left[G\!\left(\tau\_{b}^{+}(s)\right)\right]-\mathbb{E}\!\left[G\!\left(\tau\_{b}^{-}\right)\right], |  | (3) |

验证者得分为

|  |  |  |  |
| ---| ---| ---| ---|
|  | Qb​(s)=−Δ​Gb​(s).Q\_{b}(s)=-\Delta G\_{b}(s). |  | (4) |

分数越高表示摘要相对于保留预压缩上下文引入的额外执行回归越少。

在 AppWorld 中，我们将 zjz\_{j} 实例化为两个可观察事件的并集。当某个操作触发 AppWorld 的本机执行错误合约时，该操作就会被“阻止”。当一个操作的规范化工具调用签名与边界之前或同一延续中较早执行的操作相匹配时，该操作将被“重复”。他们的联合被计算一次，包括当一个动作满足这两个条件时。这些信号捕获立即执行失败和恢复信息的冗余尝试或重复压缩之前已经探索过的操作。

重要的是，PRE 并不被视为最佳轨迹。它仅充当来自相同执行状态的配对控制，允许验证者在估计压缩的局部效果时控制冻结智能体的内在随机性和执行错误。

### 4.2 验证者引导的提示优化

遵循 ACON（[Kang et al., 2026](https://arxiv.org/html/2608.06503#bib.bib19)），我们在自然语言提示空间中优化压缩器，而不是更新模型参数。区别在于监督的构建方式。 TRACE 不是对比最终成功和失败的轨迹，而是在同一压缩边界评估的摘要之间构建偏好。

#### 训练边界选择。

我们首先使用冻结基础压缩器收集 AppWorld 训练分割中压缩边界的 PRE 和 POST 延续。从这些延续中，我们识别出表现出被阻止操作的边界，并根据 AppWorld 的本机执行错误类型对它们进行分组。然后，我们通过对这些错误类别进行分层抽样，选择 12 个边界。这提供了涵盖多种形式的执行阻塞的优化示例，而不是专注于最常见的错误类型。

#### 候选生成和边界局部评分。

令P0P\_{0}表示基本压缩模板，IbI\_{b}表示边界bb处的压缩器输入，包括之前的摘要、新累积的交互历史、保留的最近回合和压缩预算。冻结基础压缩器独立生成三个候选摘要：

|  |  |  |  |
| ---| ---| ---| ---|
|  | sb,n=S⁡(Ib,P0),n∈{1,2,3}.s\_{b,n}=S(I\_{b};P\_{0}),\qquad n\in\{1,2,3\}. |  | (5) |

对于每个候选者，我们在 xb+​(sb,n)x\_{b}^{+}(s\_{b,n}). 下生成特定于候选者的 POST 延续。为边界 bb 收集的 PRE 延续保持冻结，并在所有三个候选者中重用。每个摘要均使用方程 [4](https://arxiv.org/html/2608.06503#S4.E4“方程 4 ‣ 4.1 边界局部执行验证器 ‣ 4 Trace：优化压缩提示 ‣ 实现长程智能体的可靠上下文压缩：执行不稳定性的实证研究”）进行评分，因此候选者之间的差异仅源于其 POST 行为，而不是源于其 POST 行为来自 PRE 控制的变化。

对于每个边界，我们保留得分最高和最低的候选者，

|  |  |  |  |
| ---| ---| ---| ---|
|  | sb+=arg⁡maxsb,n​Qb​(sb,n),sb−=arg⁡minsb,n​Qb​(sb,n),s\_{b}^{+}=\arg\max\_{s\_{b,n}}Q\_{b}(s\_{b,n}),\qquad s\_{b}^{-}=\arg\min\_{s\_{b,n}}Q\_{b}(s\_{b,n}), |  | (6) |

形成12个边界匹配对比示例：

|  |  |  |  |
| ---| ---| ---| ---|
|  | 𝒟pref={(Ib,sb+,sb−)}b=112.\mathcal{D}\_{\mathrm{pref}}=\left\{\bigl(I\_{b},s\_{b}^{+},s\_{b}^{-}\bigr)\right\}\_{b=1}^{12}. |  | (7) |

#### 系统感知提示建议。

在初步实验中，我们发现仅从对比总结中推断出的指导方针可能与冻结的下游系统提示相矛盾。例如，当摘要中的错误变量名称导致执行错误时，提议者通常会添加诸如“不保留先前会话中的变量”之类的规则，即使系统提示明确指出“您可以在后续代码块中使用先前代码块中的变量”。

因此，除了现有的压缩模板和偏好示例之外，我们还为提议者提供下游系统提示。指示提议者首先检查一对摘要是否引入了与系统提示不一致的信息或指令，然后使用对比对来推断对压缩策略的修订。

提议者仅观察压缩器输入和更好-更差的摘要对。它不会观察后续的推出操作、环境观察、阻塞操作错误、重复调用指示器或验证者分解。这可以防止它直接将单独的推出失败编码到模板中。

冻结的提议者会生成五个完整的候选模板：

|  |  |  |  |
| ---| ---| ---| ---|
|  | {P1,…,P5}=G⁡(P0,Hsys,𝒟pref),\{P\_{1},\ldots,P\_{5}\}=G\!\left(P\_{0},H\_{\mathrm{sys}},\mathcal{D}\_{\mathrm{pref}}\right), |  | (8) |

其中HsysH\_{\mathrm{sys}}是冻结的下游系统提示符。每个候选者都保留原始摘要模式、部分结构、占位符、渲染器、压缩预算和下游接口。仅修改管理压缩器保留、更新和删除内容的自然语言指令。

#### 端到端的开发选择。

边界局部验证者分数用于构建对比监督，但最终模板是根据端到端智能体性能选择的。对于每个建议的模板PmP\_{m},，我们在 AppWorld 开发部分的每个任务上运行完整的循环压缩和执行管道两次。让Yt,r​(Pm)∈{0,1}Y\_{t,r}(P\_{m})\in\{0,1\}指示运行r∈{1,2}r\in\{1,2\}是否在任务tt上成功。我们计算

|  |  |  |  |
| ---| ---| ---| ---|
|  | Pass2​(Pm)=1|𝒟dev|​∑t∈𝒟devYt,1​(Pm)​Yt,2​(Pm),\mathrm{Pass}^{2}(P\_{m})=\frac{1}{|\mathcal{D}\_{\mathrm{dev}}|}\sum\_{t\in\mathcal{D}\_{\mathrm{dev}}}Y\_{t,1}(P\_{m})Y\_{t,2}(P\_{m}), |  | (9) |

它衡量两次运行中成功完成的开发任务的比例。所选模板是

|  |  |  |  |
| ---| ---| ---| ---|
|  | P⋆=arg⁡maxPm,m∈{1,…,5}​Pass2​(Pm).P^{\star}=\arg\max\_{P\_{m},\;m\in\{1,\ldots,5\}}\mathrm{Pass}^{2}(P\_{m}). |  | (10) |

因此，最终结果不用于构建单独的摘要偏好：这些偏好完全由边界本地执行验证器确定。终端性能仅在开发拆分的最终模型选择阶段使用。选择后，P⋆P^{\star} 被冻结并在测试分组上进行评估，无需进一步及时修改。

## 5 个初步实验

### 5.1 实验设置

评估数据集。我们对 AppWorld 进行评估，这是一个具有代表性的长期工具使用基准（[Trivedi et al., 2024](https://arxiv.org/html/2608.06503#bib.bib24)）。我们优化训练分组的提示，选择开发分组的提示，并报告测试正常分组的最终结果。我们使用 4,096 个词元的压缩窗口，并将每个智能体的推出限制为 50 个步骤。其他基准的结果将包含在未来的工作中。

工具使用智能体和压缩机模型。在我们的实验中，我们评估了 MiniMax-M3 ([MiniMax, 2026](https://arxiv.org/html/2608.06503#bib.bib27)) 和 Kimi-K2.7-Code ([Moonshot AI, 2026](https://arxiv.org/html/2608.06503#bib.bib28))。为了优化，我们使用 MiniMax-M3 作为冻结的 LLM 提议者。两种模型均可直接通过 Ollama 访问。22 2 <https://ollama.com/>

基线。我们使用未压缩的完整上下文作为参考。基线包括 FIFO 截断、LLMLingua-2 词元修剪（[Pan et al., 2024](https://arxiv.org/html/2608.06503#bib.bib8)）、OpenClaw 压缩提示（[OpenClaw Contributors, 2026a](https://arxiv.org/html/2608.06503#bib.bib20)）、Hermes 压缩提示（[Nous Research, 2026](https://arxiv.org/html/2608.06503#bib.bib22))33 3 改编自 Hermes 智能体上下文压缩器：<https://github.com/NousResearch/hermes-agent/blob/cca3b77a4b4217bb13288f0c4cac9710d82432c8/agent/context_compressor.py>.，以及在 AppWorld、ACON-UT 和 ACON-UTCO 上优化的 ACON 指南（[Kang et al., 2026](https://arxiv.org/html/2608.06503#bib.bib19)）。更多详细信息请参见附录 [A](https://arxiv.org/html/2608.06503#A1“附录 A 基线详细信息 ‣ 实现长程智能体的可靠上下文压缩：执行不稳定性的实证研究”）。 TRACE 提示在附录 [B](https://arxiv.org/html/2608.06503#A2“附录 B 跟踪提示 ‣ 实现长程智能体的可靠上下文压缩：执行不稳定性的实证研究”）中提供。

评估指标。对于性能，我们报告平均单次运行通过率Pass2\mathrm{Pass}^{2},和Pass​@​2\mathrm{Pass@2}，以捕获总体成功率和多次运行稳定性。为了提高效率，我们报告每个任务的平均智能体步骤数和峰值输入标记。

### 5.2 主要结果

表 [1](https://arxiv.org/html/2608.06503#S5.T1“表 1 ‣ 5.2 主要结果 ‣ 5 个初步实验 ‣ 实现长程智能体的可靠上下文压缩：执行不稳定性的实证研究”) 报告了 AppWorld 测试正常的结果。相对于未压缩的执行，所有压缩方法都会降低性能，并且在中等和困难任务上性能下降会变得更大。在现有的压缩基线中，Prompting-O 总体表现最好，平均准确率为 71.471.4，Pass2 为 59.559.5，Pass@2 为 83.383.3。

使用自动优化的压缩提示，TRACE 是整体最强的压缩方法。与 Prompting-O 相比，它的准确率提高了 5.75.7 点（77.177.1 与 71.471.4），Pass2 中提高了 7.87.8 点（67.367.3 与 59.559.5），Pass@2 中提高了 3.63.6 点（86.986.9 与 83.383.3）。 Pass2 中的较大改进表明优化的提示不仅提高了平均任务成功率，而且还提高了两次独立运行之间成功执行的一致性。

效果随任务难度而变化。在简单的任务中，TRACE 几乎与无压缩相当，达到 94.794.7 的准确率，并与 Pass2 的 91.291.2 持平。在中等任务上，它在压缩方法中获得了最高的准确率和 Pass@2，尽管 LLMLingua-2 实现了更高的 Pass2。在困难任务中，TRACE 在所有三个指标上始终优于每个压缩基线，达到 63.563.5 准确率、52.452.4 Pass2 和 74.674.6 Pass@2。

尽管有这些改进，但与未压缩执行相比仍然存在很大差距，特别是在中等和困难任务上。然而，与现有压缩方法相比的一致增益表明，边界局部对比反馈可以在不更新任何模型参数的情况下产生更可靠的压缩提示。

表 1：AppWorld 基准测试中不同难度级别的结果（测试正常）。 Acc.、Pass2 和 Pass@2 分别表示两次独立运行的平均成功率、两次运行中解决的任务分数以及至少解决一次的分数。无压缩是未压缩的基线。在压缩方法中，逐列最佳以粗体显示；我们的结果以蓝色突出显示。

|  |  |  |  |  |  |  |  |  |  |  |  |  |
| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---|
|方法|平均 (168) | | |简单 (57) | | |中 (48) | | |硬 (63) | | |
|附件。 |通过2 |通过@22 |附件。 |通过2 |通过@22 |附件。 |通过2 |通过@22 |附件。 |通过2 |通过@22 |
|智能体：MiniMax-M3 / 压缩机：MiniMax-M3 | | | | | | | | | | | | |
|无压缩 | 85.7 | 85.7 77.4 | 77.4 94.0 | 94.0 95.6 | 95.6 91.2 | 91.2 100.0 | 100.0 87.5 | 87.5 77.1 | 77.1 97.9 | 97.9 75.4 | 75.4 65.1 | 65.1 85.7 | 85.7
|先进先出 | 63.7 | 63.7 53.0 | 74.4 | 74.4 92.1 | 92.1 86.0 | 98.2 | 98.2 69.8 | 69.8 54.2 | 54.2 81.2 | 81.2 33.3 | 33.3 19.0 | 47.6 | 47.6
| LLMLingua-2 | 68.2 | 68.2 57.7 | 57.7 78.6 | 78.6 92.1 | 92.1 84.2 | 84.2 100.0 | 100.0 70.8 | 62.5 | 62.5 79.2 | 79.2 44.4 | 44.4 30.2 | 30.2 58.7 | 58.7
|提示-O | 71.4 | 71.4 59.5 | 59.5 83.3 | 83.3 87.7 | 87.7 78.9 | 78.9 96.5 | 96.5 66.7 | 66.7 52.1 | 52.1 81.2 | 81.2 60.3 | 60.3 47.6 | 47.6 73.0 | 73.0
|提示-H | 65.2 | 65.2 49.4 | 49.4 81.0 | 84.2 | 84.2 70.2 | 70.2 98.2 | 98.2 67.7 | 67.7 52.1 | 52.1 83.3 | 83.3 46.0 | 46.0 28.6 | 28.6 63.5 | 63.5
| ACON-UT | 62.5 | 62.5 44.6 | 44.6 80.4 | 80.4 81.6 | 81.6 68.4 | 68.4 94.7 | 94.7 56.2 | 56.2 33.3 | 33.3 79.2 | 79.2 50.0 | 50.0 31.7 | 31.7 68.3 | 68.3
| ACON-UCO | 62.2 | 62.2 47.0 | 47.0 77.4 | 77.4 82.5 | 82.5 70.2 | 70.2 94.7 | 94.7 58.3 | 58.3 37.5 | 37.5 79.2 | 79.2 46.8 | 46.8 33.3 | 33.3 60.3 | 60.3
|追踪 | 77.1 | 77.1 67.3 | 67.3 86.9 | 86.9 94.7 | 94.7 91.2 | 91.2 98.2 | 98.2 74.0 | 74.0 58.3 | 58.3 89.6 | 89.6 63.5 | 63.5 52.4 | 52.4 74.6 | 74.6

### 5.3 效率

图 6：跨任务难度的效率。 AppWorld 测试正常中的平均峰值输入词元与平均智能体步骤，按任务难度分组。左下角比较好。红色虚线圆圈突出显示 TRACE。

图[6](https://arxiv.org/html/2608.06503#S5.F6“图6‣5.3效率‣5个初步实验‣实现长程智能体的可靠上下文压缩：执行不稳定性的实证研究”）比较了不同压缩方法的上下文和执行成本。在简单的任务中，所有方法都在相对较窄的范围内运行，因为这些较短的轨迹几乎不需要压缩。在中等和困难任务中，这种差异变得更加明显，在这些任务中，全上下文智能体的峰值上下文大幅增长。

压缩通常会减少峰值上下文大小，但大幅减少会增加执行成本。 FIFO 最清楚地说明了这种权衡：它使用最少的词元，但在中等和困难任务上需要更多步骤，这表明在执行过程中必须重复恢复丢弃的状态。其他压缩基线表现出类似的轨迹长度增加，尽管不太严重。

相比之下，TRACE 保持接近完整上下文参考的平均步数，同时大幅减少峰值标记。这一优势在困难任务中最为明显，其中 TRACE 仍然接近全上下文执行长度，尽管使用了不到其峰值上下文的一半。结果表明，针对压缩引起的回归探索进行优化不仅可以提高任务性能，还可以提高上下文与执行效率的权衡。

### 5.4 跨模型可迁移性

表 2：使用 MiniMax-M3 优化并使用 Kimi-K2.7-Code 在 AppWorld 测试正常上进行评估的压缩模板的跨模型传输。

|  |  |  |  |  |  |  |  |  |  |  |  |  |
| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---|
|方法|平均 (168) | | |简单 (57) | | |中 (48) | | |硬 (63) | | |
|附件。 |通过2 |通过@22 |附件。 |通过2 |通过@22 |附件。 |通过2 |通过@22 |附件。 |通过2 |通过@22 |
|智能体：Kimi-K2.7-Code / 压缩器：Kimi-K2.7-Code | | | | | | | | | | | | |
|无压缩 | 82.7 | 82.7 73.8 | 91.7 | 91.7 93.9 | 93.9 89.5 | 89.5 98.2 | 98.2 76.0 | 76.0 60.4 | 60.4 91.7 | 91.7 77.8 | 77.8 69.8 | 69.8 85.7 | 85.7
|先进先出 | 58.3 | 58.3 47.0 | 47.0 69.6 | 69.6 93.0 | 87.7 | 87.7 98.2 | 98.2 57.3 | 57.3 39.6 | 39.6 75.0 | 75.0 27.8 | 27.8 15.9 | 15.9 39.7 | 39.7
| LLMLingua-2 | 35.7 | 35.7 26.8 | 26.8 44.6 | 44.6 78.9 | 78.9 68.4 | 68.4 89.5 | 89.5 13.5 | 13.5 2.1 | 2.1 25.0 | 25.0 13.5 | 13.5 7.9 | 7.9 19.0 |
|提示-O | 46.1 | 46.1 33.3 | 33.3 58.9 | 58.9 80.7 | 80.7 71.9 | 71.9 89.5 | 89.5 32.3 | 32.3 18.8 | 18.8 45.8 | 45.8 25.4 | 25.4 9.5 | 9.5 41.3 | 41.3
|提示-H | 37.8 | 37.8 25.0 | 25.0 50.6 | 50.6 67.5 | 67.5 57.9 | 57.9 77.2 | 77.2 29.2 | 29.2 8.3 | 50.0 | 50.0 17.5 | 17.5 7.9 | 7.9 27.0 | 27.0
| ACON-UT | 40.2 | 40.2 27.4 | 27.4 53.0 | 76.3 | 76.3 66.7 | 66.7 86.0 | 26.0 | 26.0 8.3 | 43.8 | 43.8 18.3 | 18.3 6.3 | 30.2 | 30.2
| ACON-UCO | 42.9 | 42.9 31.0 | 31.0 54.8 | 75.4 | 75.4 63.2 | 63.2 87.7 | 87.7 21.9 | 21.9 12.5 | 12.5 31.2 | 31.2 29.4 | 29.4 15.9 | 15.9 42.9 | 42.9
|追踪 (MiniMax-M3) | 84.5 | 84.5 79.2 | 79.2 89.9 | 89.9 95.6 | 95.6 91.2 | 91.2 100.0 | 100.0 87.5 | 87.5 81.2 | 81.2 93.8 | 72.2 | 72.2 66.7 | 66.7 77.8 | 77.8

我们进一步评估使用 MiniMax-M3 优化的压缩模板是否可以转移到不同的模型。在没有任何额外的提示优化的情况下，我们将相同的模板应用于 Kimi-K2.7-Code，使用 Kimi-K2.7-Code 作为压缩器和下游智能体。

如表 [2](https://arxiv.org/html/2608.06503#S5.T2“表 2 ‣ 5.4 跨模型可迁移性 ‣ 5 个初步实验 ‣ 实现长程智能体的可靠上下文压缩：执行不稳定性的实证研究”) 所示，传输的 TRACE 模板大大优于所有压缩基线。它还在整体精度（84.584.5 vs. 82.782.7）和 Pass2（79.279.2 vs. 73.873.8）方面超过了无压缩，同时实现了略低的 Pass@2（89.989.9 vs. 91.791.7）。这种模式表明，传输的模板提高了成功执行的一致性，尽管它并不完全匹配未压缩上下文的任务覆盖范围。

在中等任务上，这种提升尤其明显，其中 TRACE 在所有三个指标上都优于无压缩，包括 Pass2 中的 20.820.8 点改进（81.281.2 与 60.460.4）。它也超过了简单任务的无压缩。在困难任务中，TRACE 仍然低于未压缩的参考值，但大大优于每个压缩的基线。

这些结果证明，通过 MiniMax-M3 学习到的压缩策略无需进一步调整即可转移到 Kimi-K2.7-Code。然而，由于评估考虑的是单一目标模型，更广泛的跨模型泛化仍有待建立。

## 6 相关工作

长期LLM智能体。 LLM 智能体将预训练模型从一次性生成扩展到交互式决策，其中模型重复推理、调用工具、观察结果并修改其计划（[Yao et al., 2023](https://arxiv.org/html/2608.06503#bib.bib1)；[Shinn et al., 2023](https://arxiv.org/html/2608.06503#bib.bib2)；[Wang et al., 2024b](https://arxiv.org/html/2608.06503#bib.bib3))。这些轨迹将上下文转变为操作状态而不是被动输入：智能体必须在许多步骤中保留目标、工具输出、对象标识符、中间决策和失败信号。 MemGPT 等上下文管理系统通过显式内存层管理长交互（[Packer et al., 2023](https://arxiv.org/html/2608.06503#bib.bib4)），但它们不会直接优化哪个紧凑上下文最能保留指定下游系统的未来操作。我们研究了长程智能体的动态上下文瓶颈，其中压缩必须支持动作而不是仅保留转录本。

动作的上下文压缩。提示和上下文压缩通过修剪标记、生成紧凑的文本上下文或学习连续的压缩表示来降低长输入的成本。离散或文本方法包括 Selective 上下文、LLMLingua、LongLLMLingua、 LLMLingua-2、RECOMP 和 TACO–RL（[Li et al., 2023](https://arxiv.org/html/2608.06503#bib.bib5)；[Jiang et al., 2023](https://arxiv.org/html/2608.06503#bib.bib6)；[Jiang et al., 2024](https://arxiv.org/html/2608.06503#bib.bib7)；[Pan et al., 2024](https://arxiv.org/html/2608.06503#bib.bib8)；[Xu 等人，2024](https://arxiv.org/html/2608.06503#bib.bib9)；[Shandilya 等人，2025](https://arxiv.org/html/2608.06503#bib.bib10))；连续压缩方法包括AutoCompressor、Gist 词元、ICAE、 激活信标，500×\timesCompressor, 和 ComprExIT（[Chevalier 等人，2023](https://arxiv.org/html/2608.06503#bib.bib11)；[Mu 等人，2023](https://arxiv.org/html/2608.06503#bib.bib12)；[Ge 等人，2024](https://arxiv.org/html/2608.06503#bib.bib13)； [张等人，2025](https://arxiv.org/html/2608.06503#bib.bib14)；[李等人，2025](https://arxiv.org/html/2608.06503#bib.bib15)；[叶等人，2026](https://arxiv.org/html/2608.06503#bib.bib16))。这些方法主要优化信息保留、答案质量或解码效率。 TACO–RL（[Shandilya et al., 2025](https://arxiv.org/html/2608.06503#bib.bib10)）在这个家族中最接近，因为它通过任务奖励优化提示压缩，但它的目标是静态提示和单次下游输出，而不是重复的紧凑上下文以保留未来 行为。

最近的工作更接近于特定于智能体的上下文管理。 ReSum 和 SUPO 通过优化摘要和下游工具使用行为，使智能体适应摘要操作（[Wu et al., 2025](https://arxiv.org/html/2608.06503#bib.bib17)；[Lu et al., 2025](https://arxiv.org/html/2608.06503#bib.bib18)）。相比之下，我们保持下游系统固定并仅优化压缩模块。 ACON 最接近我们的设置，因为它还优化了固定长程智能体的自然语言压缩指南（[Kang et al., 2026](https://arxiv.org/html/2608.06503#bib.bib19)）。然而，ACON 从最终成功和失败的轨迹中获取反馈，而 TRACE 通过来自同一执行状态的成对闭环延续来评估各个压缩事件。因此，我们的方法使用边界局部偏好来优化压缩提示，而不是压缩引起的执行负担。

## 7 结论和未来工作

我们表明，循环上下文压缩可以使先前建立的执行状态变得不那么可操作，从而导致阻塞操作、重复探索和不稳定的任务性能。为了解决这个问题，我们引入了 TRACE，这是一个边界局部框架，它通过成对的闭环延续来评估压缩，并使用仅偏好反馈来优化压缩提示。在 AppWorld 上，TRACE 提高了任务性能和多次运行稳定性，同时相对于现有压缩基线接近全上下文执行效率。

我们当前的验证程序专注于可观察的执行回归，特别是阻塞和重复的操作，并且可能无法捕获静默状态损坏。未来的工作将开发更丰富的边界局部信号，评估跨其他智能体和基准的传输，并将即时优化扩展到学习的压缩器。

## 附录 A 基线详细信息

本节描述我们实验中使用的压缩基线。除非另有说明，所有条件都在相同的冻结智能体协议下进行评估：下游智能体模型、工具使用提示、解码配置、工具 API、输出解析器和执行环境都是固定的。仅更改提供给智能体的上下文。该协议将上下文表示的影响与下游智能体策略的变化隔离开来。

共享评估协议。所有压缩和截断基线都使用相同的循环压缩触发器，并逐字保留最近的交互。全上下文引用绕过压缩并保留完整的交互历史记录。在所有条件下，我们都保持下游工具使用提示、工具描述、输出格式说明、少量示例、解码配置、解析器和执行环境固定。替换上下文被插入到同一连续点，因此下游行为的差异是由提供的上下文表示引起的，而不是由更改的智能体策略或接口引起的。

由于提示定义的基线可能对微小的措辞更改很敏感，因此我们在评估之前冻结所有提示模板，并记录每次运行中使用的呈现提示的哈希值。对于 ACON，事实来源是下面指定的原始 Microsoft 存储库和提交。对于 LLMLingua-2，事实来源是 Microsoft 官方实现和发布的压缩模型。

### A.1 完整上下文参考

无压缩。智能体接收完整的未压缩交互历史记录。此条件用作行为保留的完整上下文参考和词元成本测量的参考点。它不是压缩器，并且不会单独消耗已包含在智能体上下文中的任务指令。

### A.2 词元修剪和截断基线

该组包含两个非生成基线。它们不会生成新的自由形式摘要，而是保留原始交互历史记录的选定部分。两者都使用相同的压缩触发器、下游上下文槽和最近回合保存策略作为生成基线。当可压缩历史超出上下文预算时，就会触发压缩，而最近的交互轮次仍然逐字保留。

先进先出。 FIFO 是一种基于新近度的滑动窗口控制。当渲染的可压缩历史超过上下文预算时，从前面开始丢弃完整的回合，最旧的在前，直到历史适合。系统提示、原始任务指令以及最近的交互轮次始终保留。因此，先进先出隔离了有多少行为可以通过最近的动作——观察连续性来保留，而无需学习显着性估计或生成的摘要文本。

LLMLingua-2。 LLMLingua-2 将即时压缩制定为标记分类，并提炼出更小的压缩器以实现高效且忠实的提取压缩（[Pan et al., 2024](https://arxiv.org/html/2608.06503#bib.bib8)）。我们使用已发布的 microsoft/llmlingua-2-xlm-roberta-large-meetingbank 模型将其与任务无关地应用于可压缩交互历史记录。当压缩被触发时，LLMLingua-2 会从现有历史记录中选择词元，直至达到目标预算。生成的提取上下文会替换旧的转弯，而最新的转弯仍逐字保留。此基线测试词元级显着性是否单独保留未来智能体操作所需的执行状态。

执行。我们使用官方的 Microsoft LLMLingua 实现。44 4 <https://github.com/microsoft/LLMLingua>，版本 0.2.2（发布标签 v0.2.2，提交 a411a3fa61df74411157b2512b592d5357bd8f17）。对于 LLMLingua-2，目标词元计数设置为分配给可压缩历史记录的预算，不包括逐字保留的最近回合。其压缩输出被插入到其他压缩基线使用的同一下游上下文槽中。

### A.3 结构化摘要压缩基线

我们的两个结构化摘要基线改编自开源智能体框架中的压缩模块。我们保留它们的原始摘要模式和提示文本，同时将它们集成到相同的循环压缩工具中。与丢弃词元的 LLMLingua-2 基线和基于新近度的 FIFO 控制不同，两者都会在上下文超出词元预算后调用辅助 LLM 将可压缩历史记录重写为结构化 Markdown 检查点。它们保留最近的交互回合并支持迭代更新，将新回合折叠到前一个检查点。

#### 提示-O（OpenClaw 压缩）。

OpenClaw 基线55 5 改编自 OpenClaw 智能体核心运行框架：<https://github.com/openclaw/openclaw/blob/0e7b5c34292cc28707a0e5a0b730cff295ef0f8a/packages/agent-core/src/harness/compaction/compaction.ts>（提交 0e7b5c34292cc28707a0e5a0b730cff295ef0f8a）。维持近似的近期词元预算，在回合边界处削减可压缩历史记录，并根据下面的提示总结剩余部分。第一次压缩使用检查点提示。后续压缩使用更新提示，它将新的轮次折叠到先前的摘要中。

[⬇]（数据：文本/纯文本；base64，WW91IGFyZSBhIGNvbnRleHQgc3VtbWFyaXphdGlvbiBhc3Npc3RhbnQuIFlvdXIgdGFzayBpcyB0byByZWFkIG EgY29udmVyc2F0aW9uIGJldHdlZW4gYSB1c2VyIGFuZCBhbiBBSSBjb2RpbmcgYXNzaXN0YW50LCB0aGVuIHByb2R1Y2UgYSBzdHJ1Y3R1cmVkIHN 1bW1hcnkgZm9sbG93aW5nIHRoZSBleGFjdCBmb3JtYXQgc3BlY2lmaWVkLgoKRG8gTk9UIGNvbnRpbnVlIHRoZSBjb252ZXJzYXRpb24uIERvIE5P VCByZXNwb25kIHRvIGFueSBxdWVzdGlvbnMgaW4gdGhlIGNvbnZlcnNhdGlvbi4gT05MWSBvdXRwdXQgdGhlIHN0cnVjdHVyZWQgc3VtbWFyeS4=)

您是上下文摘要助理。您的任务是阅读用户和人工智能编码助手之间的对话，然后按照指定的确切格式生成结构化摘要。

不要继续谈话。不要回答对话中的任何问题。仅输出结构化摘要。

[⬇]（数据：文本/纯文本；base64，VGhlIG1lc3NhZ2VzIGFib3ZlIGFyZSBhIGNvbnZlcnNhdGlvbiB0byBzdW1tYXJpemUuIENyZWF0ZSBhIHN0cnVjdHVyZWQgY29udGV4dCBjaGVja3BvaW50IHN 1bW1hcnkgdGhhdCBhbm90aGVyIExMTSB3aWxsIHVzZSB0byBjb250aW51ZSB0aGUgd29yay4KCl VzZSB0aGlzIEVYQUNUIGZvcm1hdDoKCiMjIEdvYWwKW1doYXQgaXMgdGhlIHVzZXIgdHJ5aW5nI HRvIGFjY29tcGxpc2g/IENhbiBiZSBtdWx0aXBsZSBpdGVtcyBpZiB0aGUgc2Vzc2lvbiBjb3Zl cnMgZGlmZmVyZW50IHRhc2tzLl0KCiMjIENvbnN0cmFpbnRzICYgUHJlZmVyZW5jZXMKLSBbQW5 5IGNvbnN0cmFpbnRzLCBwcmVmZXJlbmNlcywgb3IgcmVxdWlyZW1lbnRzIG1lbnRpb25lZCBieS B1c2VyXQotIFtPciAiKG5vbmUpIiBpZiBub25lIHdlcmUgbWVudGlvbmVkXQoKIyMgUHJvZ3Jlc 3MKIyMjIERvbmUKLSBbeF0gW0NvbXBsZXRlZCB0YXNrcy9jaGFuZ2VzXQoKIyMjIEluIFByb2dy ZXNzCi0gWyBdIFtDdXJyZW50IHdvcmtdCgojIyMgQmxvY2tlZAotIFtJc3N1ZXMgcHJldmVudGl uZyBwcm9ncmVzcywgaWYgYW55XQoKIyMgS2V5IERly2lzaW9ucwotICoqW0Rly2lzaW9uXSoqOi BbQnJpZWYgcmF0aW9uYWxlXQoKIyMgTmV4dCBTdGVwcwoxLiBbT3JkZXJlZCBsaXN0IG9mIHdoY XQgc2hvdWxkIGhhchHBlbiBuZXh0XQoKIyMgQ3JpdGljYWwgQ29udGV4dAotIFtBbnkgZGF0YSwg ZXhhbXBsZXMsIG9yIHJlZmVyZW5jZXMgbmVlZGVkIHRvIGNvbnRpbnVlXQotIFtPciAiKG5vbmU pIBpZiBub3QgYXBwbGljYWJsZV0KCktlZXAgZWFjaCBzZWN0aW9uIGNvbmNpc2UuIFByZXNlcn ZlIGV4YWN0IGZpbGUgcGF0aHMsIGZ1bmN0aW9uIG5hbWVzLCBhbmQgZXJyb3IgbWVzc2FnZXMu)

上面的消息是一个对话的总结。创建一个结构化上下文检查点摘要，其他法学硕士将使用该摘要来继续工作。

使用这个精确的格式：

## 目标

[用户想要完成什么？如果会话涵盖不同的任务，则可以是多个项目。]

## 限制和偏好

- [用户提到的任何限制、偏好或要求]

- [如果没有提及，则为“（无）”]

## 进展

### 完成

- [x] [已完成的任务/更改]

### 进行中

- [ ] [当前工作]

### 被阻止

- [阻碍进展的问题，如果有的话]

## 关键决策

- \*\*[决定]\*\*：[简要理由]

## 后续步骤

1. [接下来应该发生的事情的有序列表]

## 关键上下文

- [继续所需的任何数据、示例或参考]

- [或“（无）”，如果不适用]

保持每个部分简洁。保留准确的文件路径、函数名称和错误消息。

[⬇]（数据：文本/纯文本；base64，VGhlIG1lc3NhZ2VzIGFib3ZlIGFyZSBORVcgY29udmVyc2F0aW9uIG1lc3NhZ2VzIHRvIGluY29ycG9yYXRl IGludG8gdGhlIGV4aXN0aW5nIHN1bW1hcnkgcHJvdmlkZWQgaW4gPHByZXZpb3VzLXN1bW1hcnk+IHRhZ3MuCgpVcGRhdGUgdGhlIGV4aXN0aW5 nIHN0cnVjdHVyZWQgc3VtbWFyeSB3aXRoIG5ldyBpbmZvcm1hdGlvbi4gUlVMRVM6Ci0gUFJFU0VSVkUgYWxsIGV4aXN0aW5nIGluZm9ybWF0aW 9uIGZyb20gdGhlIHByZXZpb3VzIHN1bW1hcnkKLSBBREQgbmV3IHByb2dyZXNzLCBkZWNpc2lvbnMsIGFuZCBjb250ZXh0IGZyb20gdGhlIG5ldy BtZXNzYWdlcwotIFVQREFURSB0aGUgUHJvZ3Jlc3Mgc2VjdGlvbjogbW92ZSBpdGVtcyBmcm9tICJJbiBQcm9ncmVzcyIgdG8gIkRvbmUiIHdoZ W4gY29tcGxldGVkCi0gVVBEQVRFICJOZXh0IFN0ZXBzIiBiYXNlZCBvbiB3aGF0IHdhcyBhY2NvbXBsaXNoZWQKLSBQUkVTRVJWRSBleGFjdCBm aWxlIHBhdGhzLCBmdW5jdGlvbiBuYW1lcywgYW5kIGVycm9yIG1lc3NhZ2VzCi0gSWYgc29tZXRoaW5nIGlzIG5vIGxvbmdlciByZWxldmFudCw geW91IG1heSByZW1vdmUgaXQKClVzZSB0aGlzIEVYQUNUIGZvcm1hdDoKCiMjIEdvYWwKW1doYXQgaXMgdGhlIHVzZXIgdHJ5aW5nIHRvIGFjY29 tcGxpc2g/IENhbiBiZSBtdWx0aXBsZSBpdGVtcyBpZiB0aGUgc2Vzc2lvbiBjb3ZlcnMgZGlmZmVyZW50IHRhc2tzLl0KCiMjIENvbnN0cmFpbn RzICYgUHJlZmVyZW5jZXMKLSBbQW55IGNvbnN0cmFpbnRzLCBwcmVmZXJlbmNlcywgb3IgcmVxdWlyZW1lbnRzIG1lbnRpb25lZCBieSB1c2VyX QotIFtPciAiKG5vbmUpIiBpZiBub25lIHdlcmUgbWVudGlvbmVkXQoKIyMgUHJvZ3Jlc3MKIyMjIERvbmUKLSBbeF0gW0NvbXBsZXRlZCB0YXNr cy9jaGFuZ2VzXQoKIyMjIEluIFByb2dyZXNzCi0gWyBdIFtDdXJyZW50IHdvcmtdCgojIyMgQmxvY2tlZAotIFtJc3N1ZXMgcHJldmVudGluZyBw cm9ncmVzcywgaWYgYW55XQoKIyMgS2V5IERLY2lzaW9ucwotICoqW0RlY2lzaW9uXSoqOiBbQnJpZWYgcmF0aW9uYWxlXQoKIyMgTmV4dCBTdGV wcwoxLiBbT3JkZXJlZCBsaXN0IG9mIHdoYXQgc2hvdWxkIGhhchHBlbiBuZXh0XQoKIyMgQ3JpdGljYWwgQ29udGV4dAotIFtBbnkgZGF0YSwgZX hhbXBsZXMsIG9yIHJlZmVyZW5jZXMgbmVlZGVkIHRvIGNvbnRpbnVlXQotIFtPciAiKG5vbmUpIiBpZiBub3QgYXBwbGljYWJsZV0KCktlZXAgZ WFjaCBzZWN0aW9uIGNvbmNpc2UuIFByZXNlcnZlIGV4YWN0IGZpbGUgcGF0aHMsIGZ1bmN0aW9uIG5hbWVzLCBhbmQgZXJyb3IgbWVzc2FnZXMu)

上面的消息是新的对话消息，将合并到<previous-summary>标签中提供的现有摘要中。

使用新信息更新现有的结构化摘要。规则：

- 保留先前摘要中的所有现有信息

- 从新消息中添加新的进展、决策和背景

- 更新进度部分：完成后将项目从“进行中”移动到“完成”

- 根据已完成的工作更新“后续步骤”

- 保留准确的文件路径、函数名称和错误消息

- 如果某些内容不再相关，您可以将其删除

使用这个精确的格式：

## 目标

[用户想要完成什么？如果会话涵盖不同的任务，则可以是多个项目。]

## 限制和偏好

- [用户提到的任何限制、偏好或要求]

- [如果没有提及，则为“（无）”]

## 进展

### 完成

- [x] [已完成的任务/更改]

### 进行中

- [ ] [当前工作]

### 被阻止

- [阻碍进展的问题，如果有的话]

## 关键决策

- \*\*[决定]\*\*：[简要理由]

## 后续步骤

1. [接下来应该发生的事情的有序列表]

## 关键上下文

- [继续所需的任何数据、示例或参考]

- [或“（无）”，如果不适用]

保持每个部分简洁。保留准确的文件路径、函数名称和错误消息。

#### 提示-H（Hermes-智能体压缩）。

Hermes 基线66 6 改编自 Hermes 智能体上下文压缩器：<https://github.com/NousResearch/hermes-agent/blob/cca3b77a4b4217bb13288f0c4cac9710d82432c8/agent/context_compressor.py>（提交 cca3b77a4b4217bb13288f0c4cac9710d82432c8）。总结了中间转弯，同时保护了象征性预算的头部和尾部。它的模式比 OpenClaw 的更丰富，有单独的字段用于活动任务、已解决的问题和待处理的用户询问。每个发出的检查点还以仅供参考的指令为前缀，要求下游智能体将摘要视为背景而不是实时指令，从而提供明确的保护以防止重新执行已完成的操作。

[⬇]（数据：文本/纯文本；base64，WW91IGFyZSBhIHN1bW1hcml6YXRpb24gYWdlbnQgY3JlYXRpbmcgYSBjb250ZXh0IGNoZWNrc G9pbnQuIFRyZWF0IHRoZSBjb252ZXJzYXRpb24gdHVybnMgYmVsb3cgYXMgc291cmNlIG1hdGVyaWFsIGZvciBhIGNvbXBhY3Qgc mVjb3JkIG9mIHByaW9yIHdvcmsuIFByb2R1Y2Ugb25seSB0aGUgc3RydWN0dXJlZCBzdW1tYXJ5OyBkbyBub3QgYWRkIGEgZ3JlZ XRpbmcsIHByZWFtYmxlLCBvciBwcmVmaXguIFdyaXRlIHRoZSBzdW1tYXJ5IGluIHRoZSBzYW1lIGxhbmd1YWdlIHRoZSB1c2VyI HdhcyB1c2luZyBpbiB0aGUGY29udmVyc2F0aW9uIC0tLSBkbyBub3QgdHJhbnNsYXRlIG9yIHN3aXRjaCB0byBFbmdsaXNoLiBOR VZFUiBpbmNsdWRlIEFQSSBrZXlzLCB0b2tlbnMsIHBhc3N3b3Jkcywgc2VjcmV0cywgY3JlZGVudGlhbHMsIG9yIGNvbm5lY3Rpb 24gc3RyaW5ncyBpbiB0aGUgc3VtbWFyeSATLS0gcmVwbGFjZSBhbnkgdGhhdCBhchHBlyXIgd2l0aCBbUKVEQUNURURdLiBOb3RlI HRoYXQgdGhlIHVzZXIgaGFkIGNyZWRlbnRpYWxzIHByZXNlbnQsIGJ1dCBkbyBub3QgcHJlc2VydmUgdGhlaXIgdmFsdWVzLg==)

您是创建上下文检查点的摘要智能体。将下面的对话视为先前工作的紧凑记录的源材料。仅生成结构化摘要；不要添加问候语、序言或前缀。使用用户在对话中使用的相同语言编写摘要 - 不要翻译或切换为英语。切勿在摘要中包含 API 密钥、词元、密码、机密、凭据或连接字符串 - 将出现的任何内容替换为 [已编辑]。请注意，用户具有凭据，但不保留其值。

[⬇]（数据：文本/纯文本；base64，IyMgQWN0aXZlIFRhc2sKW1RoZSBzaW5nbGUgbW9zdCBpbXBvcnRhbn QgZmllbGQuIENhCHR1cmUgdGhlIHVzZXIncyBtb3N0IHJly2VudCB1bmZ1bGZpbGxlZCBpbnB1dCB2ZXJ iYXRpbTogZXhwbGljaXQgYXNzaWdubWVudHMsIHF1ZXN0aW9ucyBhd2FpdGluZyBhbiBhbnN3ZXIsIGRl Y2lzaW9ucyBhd2FpdGluZyBpbnB1dCwgb3IgZGlzY3Vzc2lvbnMgd2hlcmUgdGhlIGFzc2lzdGFudCBvd 2VzIHRoZSBuZXh0IHJlcGx5LiBBIHF1ZXN0aW9uIELTIGFuIGFjdGl2ZSB0YXNrLiBSZXNlcnZlICJOb2 5lIiBmb3IgYSBmdWxseS1yZXNvbHZlZCBsYXN0IGV4Y2hhbmdlLiBJZiB0aGUgdXNlcidzIGxhdGVzdCB tZXNzYWdlIGlzIGEgcmV2ZXJzZSBzaWduYWwgKHN0b3AsIHVuZG8sIHJvbGwgYmFjaywgbmV2ZXIgbWlu ZCwganVzdCB2ZXJpZnksIGNoYW5nZSBvZiB0b3BpYyksIHJlY29yZCBpdCB2ZXJiYXRpbSBhbmQgZG8gTk 9UIGNhcnJ5IGZvcndhcmQgdGhlIGNhbmNlbGxlZCB0YXNrLl0KCiMjIEdvYWwKW1doYXQgdGhlIHVzZXI gaXMgdHJ5aW5nIHRvIGFjY29tcGxpc2ggb3ZlcmFsbF0KCiMjIENvbnN0cmFpbnRzICYgUHJlZmVyZW5j ZXMKW1VzZXIgcHJlZmVyZW5jZXMsIGNvZGluZyBzdHlsZSwgY29uc3RyYWludHMsIGltcG9ydGFudCBkZ WNpc2lvbnNdCgojIyBDb21wbGV0ZWQgQWN0aW9ucwpbTnVtYmVyZWQgbGlzdCBvZiBjb25jcmV0ZSBhY3 Rpb25zIHRha2VuOiBmb3JtYXQgZWFjaCBhcyAiTi4gQUNUSU9OIHRhcmdldCATLS0gb3V0Y29tZSBbdG9 vbDogbmFtZV0iLiBCZSBzcGVjaWZpYyB3aXRoIGZpbGUgcGF0aHMsIGNvbW1hbmRzLCBsaW5LIG51bWJl cnMsIGFuZCByZXN1bHRzLl0KCiMjIEFjdGl2ZSBTdGF0ZQpbV29ya2luZyBkaXJly3RvcnkvYnJhbmNoL CBtb2RpZmllZC9jcmVhdGVkIGZpbGVzLCB0ZXN0IHN0YXR1cyAoWC9ZIHBhc3NpbmcpLCBydW5uaW5nIHB yb2Nlc3NlcywgcmVsZXZhbnQgZW52aXJvbm1lbnQgZGV0YWlsc10KCiMjIEluIFByb2dyZXNzCltXb3Jr IHVuZGVyd2F5IHdoZW4gY29tcGFjdGlvbiBmaXJlZF0KCiMjIEJsb2NrZWQKW0Jsb2NrZXJzLCBlcnJvc nMsIG9yIGlzc3VlcyBub3QgcmVzb2x2ZWQsIHdpdGggZXhhY3QgZXJyb3IgbWVzc2FnZXNdCgojIyBLZX kgRGVjaXNpb25zCltJbXBvcnRhbnQgdGVjaG5pY2FsIGRLY2lzaW9ucyBhbmQgV0hZIHRoZXkgd2VyZSB TYWRlXQoKIyMgUmVzb2x2ZWQgUXVlc3Rpb25zCltRdWVzdGlvbnMgYWxyZWFkeSBhbnN3ZXJlZCwgaW5j bHVkaW5nIHRoZSBhbnN3ZXIgc28gaXQgaXMgbm90IHJlcGVhdGVkXQoKIyMgUGVuZGluZyBVc2VyIEFza 3MKW1VzZXIgcXVlc3Rpb25zL3JlcXVlc3RzIG5vdCB5ZXQgYW5zd2VyZWQgb3IgZnVsZmlsbGVkLiBJZi Bub25lLCB3cml0ZSAiTm9uZS4iXQoKIyMgUmVsZXZhbnQgRmlsZXMKW0ZpbGVzIHJlYWQsIG1vZGlmaWVk LCBvciBjcmVhdGVkLCB3aXRoIGEgYnJpZWYgbm90ZSBvbiBlYWNoXQoKIyMgUmVtYWluaW5nIFdvcmsKW 1doYXQgcmVtYWlucywgZnJhbWVkIGFzIGNvbnRleHQsIG5vdCBpbnN0cnVjdGlvbnNdCgojIyBDcml0aW NhbCBDb250ZXh0CltTcGVjaWZpYyB2YWx1ZXMsIGVycm9yIG1lc3NhZ2VzLCBjb25maWd1cmF0aW9uLCB vciBkYXRhIHRoYXQgd291bGQgYmUgbG9zdCBvdGhlcndpc2UuIE5FVkVSIGluY2x1ZGUgY3JlZGVudGlh bHMgLS0tIHdyaXRlIFtSRURBQ1RFRF0uXQoKVGFyZ2V0IH57c3VtbWFyeV9idWRnZXR9IHRva2Vucy4gQ MUGQ09OQ1JFVEUuIFdoZW4gYW4gYWN0aW9uIGlzIGFscmVhZHkgY2FycmllZCBvdXQsIHBocmFzZSBpdC BhcyBhIGNvbXBsZXRlZCwgZGF0ZWQsIHBhc3QtdGVuc2UgZmFjdCByYXRoZXIgdGhhbiBhbiBvcGVuIGl uc3RydWN0aW9uICh0ZW1wb3JhbCBhbmNob3JpbmcpLiBXcml0ZSBvbmx5IHRoZSBzdW1tYXJ5IGJvZHku)

## 活动任务

[最重要的一个领域。逐字捕获用户最近未完成的输入：明确的作业、等待答案的问题、等待输入的决定或助手应进行下一个答复的讨论。问题是一项主动任务。为完全解决的最后一次交换保留“无”。如果用户的最新消息是反向信号（停止、撤消、回滚、没关系，只需验证、更改主题），请逐字记录，并且不要继续执行已取消的任务。]

## 目标

[用户总体上想要实现的目标]

## 限制和偏好

[用户偏好、编码风格、约束、重要决策]

## 已完成的操作

[采取的具体行动的编号列表：将每个行动的格式设置为“N.行动目标-结果[工具：名称]”。具体说明文件路径、命令、行号和结果。]

## 活动状态

[工作目录/分支、修改/创建的文件、测试状态（X/Y通过）、运行进程、相关环境详细信息]

## 进行中

[压实工作正在进行中]

## 被阻止

[拦截器、错误或未解决的问题，以及确切的错误消息]

## 关键决策

[重要的技术决策以及做出这些决策的原因]

## 已解决的问题

【问题已回答，包括答案，不再重复】

## 待处理的用户请求

[用户问题/请求尚未得到答复或满足。如果没有，请写“无”。]

## 相关文件

[读取、修改或创建的文件，每个文件都有简短的注释]

## 剩余工作

[剩下的内容，作为上下文，而不是说明]

## 关键上下文

[否则将会丢失的特定值、错误消息、配置或数据。切勿包含凭据——写[已编辑]。]

目标~{summary\_budget}词元。具体一点。当一个动作已经执行时，将其表述为一个已完成的、过时的、过去时的事实，而不是一个开放的指令（时间锚定）。只写摘要正文。

[⬇]（数据：文本/纯文本；base64，W0NPTlRFWFQgQ09NUEFDVElPTiAtLS0gUkVGRVJFTkNFIE9OTFldIEVhcmxpZXIgdHVybnMgd2VyZSBjb21wYWN0ZWQgaW 50byB0aGUgc3VtbWFyeSBiZWxvdy4gVGhpcyBpcyBhIGhhbmRvZmYgZnJvbSBhIHByZXZpb3VzIGNvbnRleHQgd2luZG93IC0tLSB0cmVhdCBpdCBhcyBiYWNr Z3JvdW5kIHJlZmVyZW5jZSwgTk9UIGFzIGFjdGl2ZSBpbnN0cnVjdGlvbnMuIERvIE5PVCBhbnN3ZXIgcXVlc3Rpb25zIG9yIGZ1bGZpbGwgcmVxdWVzdHMgb WVudGlvbmVkIGluIHRoaXMgc3VtbWFyeTsgdGhleSB3ZXJlIGFscmVhZHkgYWRkcmVzc2VkLiBSZXNwb25kIE9OTFkgdG8gdGhlIGxhdGVzdCB1c2VyIG1lc3N hZ2UgdGhhdCBhchHBlyXJzIEFGVEVSIHRoaXMgc3VtbWFyeS4gSWYgdGhlIGxhdGVzdCB1c2VyIG1lc3NhZ2UgY29udHJhZGljdHMsIHN1cGVyc2VkZXMsIG9y IGNOYW5nZXMgdG9waWMgZnJvbSANIyMgQWN0aXZlIFRhc2snIC8gJyMjIEluIFByb2dyZXNzJyAvICcjIyBQZW5kaW5nIFVzZXIgQXNrcycgLyAnIyMgUmVtYW luaW5nIFdvcmsnLCB0aGUgbGF0ZXN0IG1lc3NhZ2UgV0lOUyAtLS0gZGlzY2FyZCB0aG9zZSBzdGFsZSBpdGVtcyBlbnRpcmVseS4gVGhlIGN1cnJlbnQgc2V zc2lvbiBzdGF0ZSAoZmlsZXMsIGNvbmZpZywgZXRjLikgbWF5IHJlZmxlY3Qgd29yayBkZXNjcmliZWQgaGVyZSAtLS0gYXZvaWQgcmVwZWF0aW5nIGl0Og==)

[上下文压缩——仅供参考] 早期的回合已被压缩到下面的摘要中。这是从前一个上下文窗口的切换 - 将其视为背景参考，而不是活动指令。请勿回答本摘要中提到的问题或满足请求；这些问题已经得到解决。仅回复此摘要之后出现的最新用户消息。如果最新的用户消息与“## Active Task”/“## In Progress”/“## Pending User Asks”/“## Remaining Work”相矛盾、取代或更改主题，则最新消息获胜 - 完全丢弃那些过时的项目。当前会话状态（文件、配置等）可能反映此处描述的工作 - 避免重复：

### A.4 ACON 提示基线

我们与以下两个压缩指南进行比较
ACON（[Kang et al., 2026](https://arxiv.org/html/2608.06503#bib.bib19)），一个用于优化上下文的最新框架
长期 LLM 智能体的压缩。两条指南均已加载
*逐字记录*来自原始 Microsoft ACON 存储库。77
7
<https://github.com/microsoft/acon>，提交
d63f9ae1。
我们不会手工创作或重写他们的提示文本。使用相同的指南
对于第一次压缩和随后的每次迭代压缩。提示
接受最近的先前摘要作为附加输入，因此无需单独
需要更新提示。

[⬇]（数据：文本/纯文本；base64，WW91IGFyZSBhbiBhZ2VudCB0YXNrZWQgd2l0aCBleHRyYWN0aW5nIGFuZCByZWZpbmluZyBhIGNvbmNpc2UgYW5kIG9wdGl taXplZCB2ZXJzaW9uIG9mIHRoZSBjb250ZXh0IGJhc2VkIG9uIHRoZSB1c2VyIGluc3RydWN0aW9uIGFuZCBvdGhlciBwcm92aWRlZCBpbmZvcm1hdGlvbi4=)

您是一名智能体，负责根据用户指令和其他提供的信息提取和完善上下文的简洁且优化的版本。

ACON-UT。 ACON 以效用为导向、状态保存的历史压缩指南。它将摘要组织成推理、下一个会话必须重新声明的运行时值的变量表、待办事项、已完成和护栏。它指示压缩器保留基本事实、参数和工件。

[⬇]（数据：文本/纯文本；base64，WW91IG1haW50YWluIGEgY29tcGFjdCwgc3RhdGUtcHJlc2VydmluZyBISVNUT1JZX1NVTU1BUlkgZm9y IGEKbXVsdGktc2Vzc2lvbiBhZ2VudC4KCklucHV0OgpbVVNFUiBJTlNUUlVDVElPTl0ge3sgdGFzayB9fQpbUFJFVklPVVMgU1VNTUFSWV0g e3sgcHJldl9zdW1tYXJ5IH19CltISVNUT1JZIE9GIElOVEVSQUNUSU9OU10ge3sgaGlzdG9yeSB9fQoKQ3JlYXRlIHRoZSBmb2xsb3dpbmcg c2VjdGlvbnMtdXNlIHRoZSBleGFjdCBoZWFkaW5ncyBhbmQgb3JkZXI6Cgo8SELTVE9SWV9TVU1NQVJZPgoKMS4gUKVBU09OSU5HCiAgIC0g S2V5IHByb2dyZXNzLCBkZWNpc2lvbnMsIG91dGNvbWVzLCBhbmQgdGhlaXIgcmF0aW9uYWxlLgogICAtIE5vdGUgaG93IGVhcmxpZXIgc3R lcHMgaW5mbHVlbmNlIGxhdGVyIG9uZXMuCgoyLiBWQVJTCiAgIHwgbmFtZSB8IHZhbHVlIHwgcHVycG9zZSB8CiAgIHwtLS0tLS18LS0tLS0 tLXwtLS0tLS0tLS18CiAgIFJly29yZCBldmVyeSBydW50aW1lIHZhbHVlIHRoZSBuZXh0IHNlc3Npb24gbXVzdCByZS1kZWNsYXJlCiAgICh 0b2tlbnMsIGlkcywgbGlzdHMsIGxhc3QgcGFnZV9pbmRleC9wYWdlX2xpbWl0LCBldGMuKS4KCjMuIFRPRE8KICAgTGlzdCBwZW5kaW5nIGF jdGlvbnMgd2l0aCBlbm91Z2ggZGV0YWlsIHRvIGV4ZWN1dGUgZGlyZWN0bHkuCgo0LiBDT01QTEVURUQKICAgQnVsbGV0IGxpc3Qgb2YgZm luaXNoZWQgc3VidGFza3Mgd2l0aCBicmllZiByZXN1bHRzLgoKNS4gR1VBUkRSQUlMUwogICBTaG9ydCByZW1pbmRlcnMgdGhhdCBwcmV2ZW 50IHJlcGVhdCBClnJvcnMsIGUuZy4KICAgLSBNZW1vcnkgcmVzZXRzOyByZS1jcmVhdGUgVkFSUyBiZWZvcmUgdXNlLgogICAtIFBhZ2luYX RlIHVudGlsIGVtchR5IHBhZ2UuCiAgIC0gVmFsaWRhdGUgQVBJIHBhcmFtZXRlcnMgYWdhaW5zdCBzcGVjLgogICATIEF2b2lkIHJlZHVuZG FudCBsb2dpbnMgb3IgZG9jIGxvb2stdXBzLgoKUmVxdWlyZW1lbnRzOgotIEJlIGNvbmNpc2UtYnVsbGV0cyBhbmQgdGFibGVzIHByZWZlc nJlZDsgbm8gZXh0cmFuZW91cyBwcm9zZS4KLSBQcmVzZXJ2ZSBhbGwgZXNzZW50aWFsIGZhY3RzLCBwYXJhbWV0ZXJzLCBhbmQgYXJ0aWZhY 3RzOyBvbWl0CiAgbm90aGluZyBjcml0aWNhbC4KLSBJbmNsdWRlIGVycm9ycyBvbmx5IGlmIHRoZXkgaW5mb3JtIGZ1dHVyZSBhdm9pZGFuY 2UuCi0gRG8gbm90IG91dHB1dCB0aGUgaW5wdXQgb3IgYW55IGNvbW1lbnRhcnktcmV0dXJuIG9ubHkKICA8SElTVE9SWV9TVU1NQVJZPi4=)

您维护一个紧凑的、状态保存的HISTORY\_SUMMARY

多会话智能体。

输入：

[用户说明] {{ 任务 }}

[先前摘要] {{ prev\_summary }}

[交互历史] {{ 历史 }}

创建以下部分 - 使用确切的标题和顺序：

<HISTORY\_SUMMARY>

1. 推理

- 关键进展、决定、结果及其理由。

- 注意早期步骤如何影响后面的步骤。

2.增值服务

|名称 |价值|目的|

|——|——-|——|

记录下一个会话必须重新声明的每个运行时值

（词元、ID、列表、最后page\_index/page\_limit,等）。

3.待办事项

列出待处理的操作，并提供足够的详细信息以直接执行。

4. 完成

已完成子任务的项目符号列表以及简要结果。

5. 护栏

简短的提醒可以防止重复错误，例如

- 内存重置；使用前重新创建 VARS。

- 分页直到空页。

- 根据规范验证 API 参数。

- 避免冗余登录或文档查找。

要求：

- 简洁——优先使用项目符号和表格；没有无关的散文。

- 保留所有重要事实、参数和工件；省略

没什么关键的。

- 仅当错误提示未来避免时才包含错误。

- 不输出输入或任何注释-仅返回

<HISTORY\_SUMMARY>.

ACON-UTCO。 ACON 的实用和压缩优化指南。它保留了 ACON-UT 的输出模式，同时添加了鼓励更短检查点的显式压缩规则。这些规则会折叠叙述，截断长词元或凭证字符串（除非需要逐字重用），删除未使用的状态和详细工具输出，并强加固定的字符目标。相对于 ACON-UT，它保留了相同的输出模式，同时以更精细的操作细节换取更短的检查点。

[⬇]（数据：文本/纯文本；base64，WW91IG1haW50YWluIGEgY29tcGFjdCwgc3RhdGUtcHJlc2VydmluZyBISVNUT1JZX1NVTU1BUlkgZm9yIGEKbXVsdGktc2Vzc2lvbiBhZ2VudC4KCklu chV0OgpbVVNFUiBJTlNUUlVDVElPTl0ge3sgdGFzayB9fQpbUFJFVklPVVMgU1VNTUFSWV0ge3sgcHJldl9zdW1tYXJ5IH19CltISVNUT1JZIE9GIElOVEVSQUNUSU9OU10ge3sgaGlzdG9 yeSB9fQoKU3VtbWFyeSBDb21wcmVzc2lvbiBSdWxlczoKLSBDb2xsYXBzZSBtdWx0aS1idW xsZXQgbmFycmF0aXZlcyBpbnRvIDw9MiBjb25jaXNliIHNlbnRlbmNlcy4KLSBSZXBsYWNlIH JlcGV0aXRpdmUgc3RlcCBsb2dzIHdpdGggb25lIHN1bW1hcml6aW5nIHBocmFzZS4KLSBUcn VuY2F0ZSBsb25nIHRva2Vul2NyZWRlbnRpYWwgc3RyaW5ncyB0byAiPHRva2VuPiIgdW5sZX NzCiAgdmVyYmF0aW0gcmV1c2UgaXMgcmVxdWlyZWQuCi0gUmVtb3ZlIHVudXNlZC9leHBpc mVkIGNyZWRlbnRpYWxzLCBwYWdlX2luZGV4L3BhZ2VfbGltaXQsCiAgdmVyYm9zZSBBUEkgZ HVtchHMsIGFuZCB0YWJsZSBib3JkZXJzLgotIFNocmluayBHVUFSRFJBSUxTIHRvIG9uZSBidWxsZXQgdW5sZXNzIG11bHRpcGxlIGl0ZW1zIGFyZQogIHN0aWxsIGNyaXRpY2FsLgotIERl bGV0ZSB0b29sL0FQSSBsb2cgb3V0chHV0LCBncmVldGluZ3MsIG1ldGEgcHJvc2UsIGFuZCB zZWN0aW9uCiAgaGVhZGVycyB0aGF0IG5vIGxvbmdlciBjb250YWluIGNvbnRlbnQuCi0gS2V lcCBvbmx5IHZhcmlhYmxlcyBhY3RpdmVseSByZWZlcmVuY2VkIGluIHVwY29taW5nIHN0ZXB zOwogIGxpc3QgZWFjaCBvbmNlIGluIFZBulMuCi0gUmVmZXJlbmNliIHJlbW92YWwgY2F0ZWd vcmllcyBbcmVwZXRpdGlvbl0sIFt0b29sLWxvZ3NdLCBbbWV0YV0sCiAgW2Zvcm1hdHRpbm ddIHRvIHBydW5lIHNpbWlsYXIgbGluZXMuCi0gUHJlc2VydmUgZmFjdHVhbCBjb250aW51aX R5OyBuZXZlciBpbnZlbnQgb3IgYWx0ZXIgc3RhdGUKICB2YXJpYWJsZXMuCi0gVGFyZ2V0I HN1bW1hcmllcyB3ZWxsIHVuZGVyIHt7IG1heF9jaGFycyB8IGRlZmF1bHQoMTUwMCkgfX0KI CBjaGFyYWN0ZXJzLgoKQ3JpdGljYWwgRXNzZW50aWFsczoKQWx3YXlzIGtlZXAgZXZpZGVu Y2UtZHJpdmVuIGl0ZW1zIHJlcXVpcmVkIG5leHQgc2Vzc2lvbiAoZS5nLiwKdG9rZW5zLCBp ZHMsIGVtYWlscywgYW1vdW50cywgbGlzdHMsIHBhdGhzLCBkZXNjcmlwdGlvbgpzdHJpbmdz LCBicmllZiB0YXNrIHN0YXR1cykuCgpPdXRwdXQgRVhBQ1RMWSB0aGUgZm9sbG93aW5nIHN0 cnVjdHVyZS0tLW5vdGhpbmcgbW9yZToKCjxISVNUT1JZX1NVTU1BUlk+CgoxLiBSRUFTT05JTkcKICAgT25lIGJyaWVmIHBhcmFncmFwaCBvbiBrZXkgcHJvZ3Jlc3MgYW5kIHJhdGlvbmF sZS4KCjIuIFZBulMKICAga2V5PXZhbHVlIHBhaXJzLCBjb21tYS1zZXBhcmF0ZWQ7IG9ubH kgc3RpbGwtbmVlZGVkIHJ1bnRpbWUKICAgdmFsdWVzLgoKMy4gVE9ETwogICBCdWxsZXRlZC BuZXh0IGFjdGlvbnMgKDw9NSkuCgo0LiBDT01QTEVURUQKICAgQnVsbGV0ZWQgZmluaXNoZWQgc3VidGFza3MgKDw9NSkuCgo1LiBHVUFSRFJBSUxTCiAgIFNpbmdsZSBjb25jaXNLIGJ1b GxldCwgb3Igb21pdCBpZiBub25lLgoKUmV0dXJuIG9ubHkgdGhlIDxISVNUT1JZX1NVTU1BUlk+IGJsb2NrLS0tbm8gYWRkaXRpb25hbApjb21tZW50YXJ5IG9yIGlucHV0IGVjaG9lcy4=)

您维护一个紧凑的、状态保存的HISTORY\_SUMMARY

多会话智能体。

输入：

[用户说明] {{ 任务 }}

[先前摘要] {{ prev\_summary }}

[交互历史] {{ 历史 }}

压缩规则总结：

- 将多要点叙述折叠成 <=2 个简洁的句子。

- 用一个总结性短语替换重复的步骤日志。

- 将长词元/凭证字符串截断为“<token>”，除非

需要逐字重用。

- 删除未使用/过期的凭据，page\_index/page\_limit,

详细的 API 转储和表格边框。

- 将护栏缩小为一颗子弹，除非有多个物品

仍然很关键。

- 删除工具/API 日志输出、问候语、元散文和部分

不再包含内容的标题。

- 仅保留在后续步骤中主动引用的变量；

在 VARS 中分别列出一次。

- 参考删除类别[重复]、[工具日志]、[元]、

【格式化】修剪相似的行。

- 保持事实的连续性；永远不要发明或改变状态

变量。

- 目标摘要远低于{{ max\_chars |默认（1500）}}

字符。

关键要点：

始终保留下一次会议所需的证据驱动项目（例如，

词元、ID、电子邮件、金额、列表、路径、描述

字符串，简要任务状态）。

准确输出以下结构——仅此而已：

<HISTORY\_SUMMARY>

1. 推理

用一段简短的段落介绍主要进展和理由。

2.增值服务

键=值对，以逗号分隔；仅仍需要运行时

价值观。

3.待办事项

列出下一步操作 (<=5)。

4. 完成

已完成的子任务（<=5）。

5. 护栏

单个简洁的项目符号，如果没有则省略。

仅返回 <HISTORY\_SUMMARY> 块——无其他

评论或输入回声。

## 附录 B 跟踪提示

### B.1 优化提示

[⬇]（数据：文本/纯文本；base64，PGNvbnZlcnNhdGlvbj4Ke3sgaGlzdG9yeSB9fQo8L2NvbnZlcnNhdGlvbj4KCjxwcmV2aW91c y1zdW1tYXJ5Pgp7eyBwcmV2X3N1bW1hcnkgfX0KPC9wcmV2aW91cy1zdW1tYXJ5PgoKVGhlIG1lc3NhZ2VzIGFib3ZlIGFyZSBOR VcgY29udmVyc2F0aW9uIG1lc3NhZ2VzIHRvIGluY29ycG9yYXRlIGludG8gdGhlIGV4aXN0aW5nIHN1bW1hcnkgcHJvdmlkZWQga W4gPHByZXZpb3VzLXN1bW1hcnk+IHRhZ3MuCgpUcmVhdCB0aGUgc3VtbWFyeSBhcyBhIHdvcmtpbmcgc3RhdGUsIG5vdCBhIHRyY W5zY3JpcHQuIEZvciBlYWNoIGNhbmRpZGF0ZSBmYWN0IGFzazogJ3dpbGwgYSBsYXRlciBzdGVwIHJlYWQgdGhpcyBhbmQgYWN0I GRpZmZlcmVudGx5PycgSWYgbm8sIGRyb3AgaXQuIEFmdGVyIHZhbHVlcyBhcmUgZGVyaXZlZCAoY291bnRzLCB0b3RhbHMsIElEc ywgY2xhc3NpZmljYXRpb25zKSwgY2FycnkgdGhlIHJlc3VsdCByYXRoZXIgdGhhbiB0aGUgaW5wdXRzLiBQcmVzZXJ2ZSBleGFjd CBsaXRlcmFscyB0aGUGYWdlbnQgd2lsbCBwYXN0ZSBpbnRvIGEGY2FsbDogdW5leHBpcmVkIHRva2VucyAob25lIHBlciBhCHASI GRyb3Agd2hlbiB0aGUgdGFzayB0aGF0IG5lZWRlZCB0aGVtIGlzIGZpbmlzaGVkKSwgZXhhY3QgZGVzY3JpcHRpb25zLCBleGFjd CBhbW91bnRzLCBleGFjdCBmaWxlIHBhdGhzLCBleGFjdCBBUEkgcGFyYW1ldGVyIG5hbWVzIHRoYXQgZGlmZmVyIGZyb20gYSBuY Wl2ZSBndWVzcywgZXhhY3QgcmVjaXBpZW50IGlkZW50aWZpZXJzLiBEcm9wIHJhdyBBUEkgb3V0cHV0cyBhbmQgaW50ZXJtZWRpY XRlIGxpc3RzIHRoYXQgaGF2ZSBiZWVuIHN1bW1hcml6ZWQ7IHN0YXRlIGEgZmFjdCBvbmNlIGFuZCByZWZlcmVuY2UgaXQgZnJvb SB0aGUgb3RoZXJzLgoKVXNlIHRoaXMgRVhBQ1QgZm9ybWF0OgoKIyMgR29hbApUaGUgc3VwZXJ2aXNvcidzIHRhc2sgaW4gb25lI G9yIHR3byBzZW50ZW5jZXMuIFF1b3RlIGFueSBsaXRlcmFsIHN0cmluZyB0aGUgdXNlciByZXF1aXJlcyB2ZXJiYXRpbSAocmVxd WVzdCBkZXNjcmlwdGlvbnMsIGNvbW1lbnQgdGV4dCwgQ1NWIGhlYWRlcnMsIHNlYXJjaCBxdWVyaWVzKS4gQWRkIGFueSBhbnN3Z XItZm9ybWF0IGNvbnN0cmFpbnQgKGVudGl0eSBvciBudW1iZXIsIG5vIHByb3NlKSBhbmQgYSB0ZXJtaW5hbCBgYXBpcy5zdXBlc nZpc29yLmNvbXBsZXRlX3Rhc2soYW5zd2VyPTx2YWx1ZT4pYCBzdGVwOyB3aGVuIHRoZSB0YXNrIGRvZXMgbm90IHJlcXVpcmUgY W4gYW5zd2VyLCB0aGUgdGVybWluYWwgY2FsbCBzdGlsbCBydW5zICh3aXRoIG5vIGFuc3dlciBhcmd1bWVudCkuCgojIyBDb25zd HJhaW50cyAmIFByZWZlcmVuY2VzClNvdXJjZXMgb2YgdHJ1dGggaW5zaWRlIHRoZSBlbnZpcm9ubWVudCB0aGF0IGNvbnN0cmFpb iBsYXRlciBjYWxsczogJ2ZyaWVuZHMsIGZhbWlseSwgcm9vbW1hdGVzLCBjb3dvcmtlcnMsIG1hbmFnZXIsIGJyb3RoZXIsIHNpY mxpbmcsIHBhcmVudCwgZXRjLicgbWVhbnMgcGhvbmUgY29udGFjdHMsIHJldHJpZXZlZCB2aWEgYGFwaXMucGhvbmUuc2VhcmNoX 2NvbnRhY3RzKGFjY2Vzc190b2tlbiwgcmVsYXRpb25zaGlwPS4uLilgOyBwZXJzb25hbCBpbmZvLCBhY2NvdW50IGNyZWRlbnRpY WxzLCBhZGRyZXNzZXMgYW5kIHBheW1lbnQgY2FyZHMgbGl2ZSBpbiB0aGUgc3VwZXJ2aXNvciBhcHAsIHJldHJpZXZlZCB2aWEgY GFwaXMuc3VwZXJ2aXNvci4qYDsgYWNjZXNzIHRva2VucyBhcmUgc2hvcnQtbGl2ZWQgSldUcyByZXR1cm5lZCBieSBgPGFwcD4ub G9naW4odXNlcm5hbWU9Li4uLCBwYXNzd29yZD0uLi4pYCBhbmQgbXVzdCBiZSBwYXNzZWQgYXMgdGhlIG5hbWVkIGBhY2Nlc3Nfd G9rZW5gIHBhcmFtZXRlciBvbiBldmVyeSBhdXRoZW50aWNhdGVkIGNhbGwgKHNlc3Npb25zIGFyZSBub3QgcmV0YWluZWQgYWNyb 3NzIHN0ZXBzKS4gUGx1cyBhbnkgbGl0ZXJhbCBzdHJpbmdzIHRoZSB0YXNrIHJlcXVpcmVzLiBQbHVzIGFueSBlbXBpcmljYWxse S1kaXNjb3ZlcmVkIEFQSSBjb3JyZWN0aW9uIC0gYSA0MjIgZnJvbSBhIHdyb25nIHBhcmFtZXRlciBuYW1lLCBhIHJlc3BvbnNlI GtleSB0aGF0IHJldHVybmVkIHNvbWV0aGluZyBkaWZmZXJlbnQgdGhhbiBleHBlY3RlZCAtIHJlY29yZGVkIGFzIHRoZSB3b3Jra W5nIHBhcmFtZXRlciBvciBrZXkgbmFtZSBzbyBmdXR1cmUgY2FsbHMgZG8gbm90IHJlcGVhdCB0aGUgbWlzdGFrZS4KCiMjIFByb 2dyZXNzCkRvbmUgLyBJbiBQcm9ncmVzcyAvIEJsb2NrZWQuIERvbmUgPSBidWxsZXRzIG5hbWluZyB0aGUgY29uY3JldGUgcmVzd Wx0IChhbiBhY2Nlc3MgdG9rZW4sIGFuIElELCBhIGNvdW50LCBhIGNsYXNzaWZpY2F0aW9uKTsgZG8gbm90IG5hcnJhdGUgdGhlIHN0ZXBzIHRoYXQgcHJvZHVjZWQgdGhlbS4gSW4gUHJvZ3Jlc3MgPSB0aGUgc2luZ2xlIG1vc3QgaW1tZW RpYXRlIGFjdGlvbi4gQmxvY2tlZCA9IG9ubHkgaGFyZCBibG9ja2VycyAoYSByZXF1aXJlZCBBUEkgbWl zc2luZywgYW4gZW52aXJvbm1lbnQgbGltaXRhdGlvbik7IGRyb3AgYW4gZW50cnkgb25jZSByZXNvbHZl ZC4KIyMjIERvbmUKCgojIyMgSW4gUHJvZ3Jlc3MKCgojIyMgQmxvY2tlZAoKCiMjIEtleSBEZWNpc2lvb nMKRWFjaCBsaW5lOiAnRGVjaXNpb246IG9uZS1jbGF1c2UgcmF0aW9uYWxlLicgQ292ZXIgb25seSBjaG 9pY2VzIGEgbGF0ZXIgc3RlcCBtaWdodCBkZWZlbmQgb3IgcmV1c2UgKHdoaWNoIGFwcCBvciBBUEksIHd oaWNoIGZpbHRlciwgaG93IGFuIGFtYmlndW91cyBwaHJhc2Ugc3VjaCBhcyAndGhpcyB5ZWFyJyB3YXMg aW50ZXJwcmV0ZWQpLiBJZiBhIGRlY2lzaW9uJ3MgY29uc2VxdWVuY2UgaXMgYWxyZWFkeSBlbmNvZGVkIG LUIERvbmUsIE5leHQgU3RlcHMsIG9yIENyaXRpY2FsIENvbnRleHQsIGRyb3AgdGhlIGxpbmUuCgojIyB OZXh0IFN0ZXBzCk51bWJlcmVkIGxpc3QuIEVhY2ggc3RlcCBzbWFsbCwgaW5kZXBlbmRlbnRseSBydW5u YWJsZSwgd3JpdHRlbiB3aXRoIHRoZSBleGFjdCBBUEkgY2FsbCBhbmQgZXhhY3QgYXJndW1lbnQgdmFsd WVzIHdoZXJlIGtub3duLiBSZWZlcmVuY2UgQ3JpdGljYWwgQ29udGV4dCBmb3Igc3RhdGUgdGhlIHN0ZX AgZGVwZW5kcyBvbiByYXRoZXIgdGhhbiByZXN0YXRpbmcgaXQuIFdoZW4gdGhlIHRhc2sgaXMgY29tcGx ldGUsIHRoZSBmaW5hbCBzdGVwIGlzIGBhcGlzLnN1cGVydmlzb3IuY29tcGxldGVfdGFzayhhbnN3ZXI9 PHZhbHVlPilgIGZvcm1hdHRlZCBhcyBqdXN0IGFuIGVudGl0eSBvciBudW1iZXI7IHdoZW4gbm8gYW5zd 2VyIGlzIG5lZWRlZCwgcGFzcyBubyBhbnN3ZXIgYXJndW1lbnQuCgojIyBDcml0aWNhbCBDb250ZXh0CkN vbmNyZXRlIHN0YXRlIGEgbGF0ZXIgc3RlcCByZXVzZXMgdmVyYmF0aW06IHVuZXhwaXJlZCBhY2Nlc3Mg dG9rZW5zIChvbmUgcGVyIGFwcCwgZHJvcCBhZnRlciB0aGUgdGFzayB0aGF0IG5lZWRlZCB0aGVtIGNvb XBsZXRlcyk7IHRoZSB3b3JraW5nIHNldCBvZiBJRHMgdG8gYWN0IG9uIG5leHQgKGUuZy4sIHBheW1lbn RfcmVxdWVzdF9pZCBsaXN0IHRvIGRlbnksIGZpbGUgcGF0aHMgdG8gbW92ZSwgc29uZyBJRHMgdG8gcmV zb2x2ZSwgY29udGFjdF9pZHMgdG8gZmlsdGVyKTsgcGVyLWVudGl0eSBjcm9zcy1yZWZlcmVuY2VzIGZv CIBmaWx0ZXJzICh3aG8gcXVhbGlmaWVzLCB3aG8gZG9lcyBub3QsIHdpdGggdGhlaXIgVmVubW8vY29ud GFjdCBpbmZvKTsgZXhhY3QgdmVyYmF0aW0gc3RyaW5ncyBhbmQgYW1vdW50czsgZW1waXJpY2FsbHktZG lzY292ZXJlZCBBUEkgcGFyYW1ldGVyIG9yIHJlc3BvbnNlLWtleSBjb3JyZWN0aW9ucy4gRHJvcCByYXcg QVBJIG91dHB1dHMsIGludGVybWVkaWF0ZSB2YWx1ZXMgdGhhdCBoYXZlIGJlZW4gc3VtbWFyaXplZCwgY W5kIGNyZWRlbnRpYWxzIG5vIGxvbmdlciBuZWVkZWQuCgpEcm9wIHRva2VucyBvbmNliIHRoZSB0YXNrIH RoYXQgbmVlZGVkIHRoZW0gaXMgZmluaXNoZWQuIFN0YXRlIGEgZmFjdCBpbiBvbmUgc2VjdGlvbjsgcmV mZXJlbmNlIGZyb20gdGhlIG90aGVycy4gQXZvaWQgcHJvc2UgdGhlIGFnZW50IHdpbGwgcmUtZW1pdDsg CHJlZmVyIHRva2VucywgSURzLCBhbmQgc2hvcnQgbGFiZWxzLiBXaGVuIGEgd29ya2luZyBzZXQgaXMgZ W1wdHkgKGFsbCAxOCByZXF1ZXN0cyBhchHByb3ZlZCwgYWxsIGZpbGVzIG1vdmVkLCBldmVyeSBwYXltZW 50IGNvbW1lbnRlZCksIGRyb3AgdGhlIHNly3Rpb24gdGhhdCBoZWxkIGl0IHJhdGhlciB0aGFuIGNhcnJ 5aW5nIGl0IGZvcndhcmQuIE5ldmVyIGR1cGxpY2F0ZSBhbiBpdGVtIGFjcm9zcyBzZWN0aW9ucy4KCg==)

<conversation>

{{历史}}

</conversation>

<previous-summary>

{{ prev\_summary }}

</previous-summary>

上面的消息是新的对话消息，将合并到<previous-summary>标签中提供的现有摘要中。

将摘要视为工作状态，而不是成绩单。对于每个候选事实，询问：“稍后的步骤会读取此内容并采取不同的行动吗？”如果不是，请放弃它。导出值（计数、总计、ID、分类）后，携带结果而不是输入。保留智能体将粘贴到调用中的准确文字：未过期的词元（每个应用程序一个，在需要它们的任务完成时删除）、准确的描述、准确的金额、准确的文件路径、与天真的猜测不同的准确的 API 参数名称、准确的收件人标识符。删除原始 API 输出和已汇总的中间列表；陈述一次事实并引用其他事实。

使用这个精确的格式：

## 目标

用一两句话来说明主管的任务。逐字引用用户需要的任何文字字符串（请求描述、评论文本、CSV 标题、搜索查询）。添加任何答案格式约束（实体或数字，无散文）和终端‘apis.supervisor.complete\_task(answer=<value>)‘步骤；当任务不需要答案时，终端调用仍然运行（没有答案参数）。

## 限制和偏好

限制以后通话的环境中的真实来源：“朋友、家人、室友、同事、经理、兄弟、兄弟姐妹、父母等”是指电话联系人，通过‘apis.phone.search\_contacts(access\_token,关系=…)‘检索；个人信息、帐户凭据、地址和支付卡位于主管应用程序中，通过“apis.supervisor.\*”检索；访问词元是由“<app>.login(username=…,password=…)”返回的短期 JWT，并且必须在每个经过身份验证的调用上作为命名的 ‘access\_token‘ 参数传递（会话不会跨步骤保留）。加上任务所需的任何文字字符串。加上任何凭经验发现的 API 更正 - 来自错误参数名称的 422、返回与预期不同的内容的响应键 - 记录为工作参数或键名称，以便将来的调用不会重复错误。

## 进展

已完成/正在进行/已阻止。完成 = 命名具体结果的项目符号（访问词元、ID、计数、分类）；不要叙述产生它们的步骤。进行中 = 最直接的单一行动。已阻止 = 仅硬阻止程序（缺少必需的 API、环境限制）；解决后删除条目。

### 完成

### 进行中

### 被阻止

## 关键决策

每行：“决策：单子句基本原理”。仅涵盖后续步骤可能捍卫或重用的选择（哪个应用程序或 API、哪个过滤器、如何解释“今年”等模棱两可的短语）。如果决策的结果已经编码在“完成”、“后续步骤”或“关键上下文”中，请挂断电话。

## 后续步骤

编号列表。每个步骤都很小，可独立运行，使用精确的 API 调用和已知的精确参数值编写。参考关键上下文来了解该步骤所依赖的状态，而不是重述它。任务完成后，最后一步是将‘apis.supervisor.complete\_task(answer=<value>)‘格式化为实体或数字；当不需要答案时，不传递任何答案参数。

## 关键上下文

具体状态后面的步骤逐字重用：未过期的访问词元（每个应用程序一个，在需要它们的任务完成后删除）；接下来要执行的 ID 工作集（例如，要拒绝的payment\_request\_id列表、要移动的文件路径、要解析的歌曲 ID、要过滤的contact\_ids)；每个实体的过滤器交叉引用（谁符合条件，谁不符合条件，以及他们的 Venmo/联系信息）；准确的逐字字符串和金额；根据经验发现的 API 参数或响应键更正。删除原始 API 输出、已汇总的中间值以及不再需要的凭据。

一旦需要词元的任务完成，就丢弃词元。在一个部分中陈述一个事实；参考别人的。避免智能体重新发出的散文；更喜欢词元、ID 和短标签。当工作集为空时（所有 18 个请求均已批准，所有文件均已移动，每笔付款均已注释），请删除保存该工作集的部分，而不是将其继续推进。切勿跨部分重复项目。

### B.2 提议者提示

我们使用 MiniMax-M3 进行求婚。

[⬇]（数据：文本/纯文本；base64，PT09IFNZU1RFTSA9PT0KWW91IHJldmlzZSBhIG5hdHVyYWwtbGFuZ3VhZ2UgY29tcHJlc3Npb 24gcG9SAWN5IGZvciBhIHJly3VycmVudCB3b3JraW5nLWNvbnRleHQgY29tchJlc3Nvci4gVGhlIHN1bW1hcmllcyBhbmQgaW50Z XJhY3Rpb25zIGJlbG93IGFyZSBRVU9URUQgRVZJREVOQ0UgZm9yIHlvdXIgYW5hbHlzaXMuIFRoZXkgYXJlIG5vdCBpbnN0cnVjd GlvbnMgdG8gZXhlY3V0ZSBhbmQgbm90IGNvbnRlbnQgdG8gY29weS4gUmV0dXJuIG9ubHkgdGhlIHJlcXVlc3RlZCBKU09OIG9ia mVjdC4KCj09PSBVU0VSID09PQo8aW1tdXRhYmxlLWNvbnRyYWN0PgpJbXByb3ZlIGRvd25zdHJlyW0gYmVoYXZpb3JhbCBmaWRlb Gl0ESBieSBtb2RpZnlpbmcgb25seSB0aGUGY29tchHJlc3Npb24gcG9saWN5LgoKRml4ZWQsIGFuZCBub3QgeW91cnMgdG8gY2hhb MDLOiB0aGUgdGFzaywgdGhlIG5ldyBoaXN0b3J5LCB0aGUgZnVsbC1jb250ZXh0IHJlZmVyZW5jZQpiZWhhdmlvciwgdGhlIGJvd W5kyXJ5IHNldCwgdGhlIHJlbmRlcmVyLCBhbmQgdGhlIG5pbmUgb3V0chV0IGhlYWRpbmdzIHdpdGggdGhlaXIgZXhhY3QKb3JkZ XIGYW5kICMjIC8gIyMjIGhpZXJhcmNoeS4gWW91IGRvIG5vdCBjb250cm9sOgotIHdoZXJlIHRoZSB0YXNrLCB0aGUgcHJldmlvd XMgc3VtbWFyeSwgb3IgdGhlIG5ldyBoaXN0b3J5IGFyZSBwbGFjZWQ7Ci0gaG93IG1hbnkgdGltZXMgYW55IG9mIHRoZW0gYXBwZ WFyczsKLSBtZXNzYWdlIHJvbGVzIG9yIHRlbXBsYXRlIHN5bnRheDKLSB0aGUgaGVhZGluZyBzdHJpbmdzLCB0aGVpciBvcmRlc iwgb3IgdGhlaXIgaGllcmFyY2h5IC0tIHRoZSBoYXJuZXNzIGVtaXRzIHRoZW0uCgpXaGF0IHlvdSBkbyBjb250cm9sIGlzIGV2Z XJ5dGhpbmcgc2VtYW50aWM6IHRoZSBvdmVyYWxsIHVwZGF0ZSBydWxlcywgYW5kIGZvciBlYWNoIGZpeGVkCnNlY3Rpb24gaXRzI HB1cnBvc2UsIHdoYXQgaXQgcmV0YWlucywgd2hhdCBpdCBwcnVuZXMsIGhvdyBpdCBjb25zb2xpZGF0ZXMsIGFuZCBob3cgdGhlC nJldGFpbmVkIHN0YXRlIGlzIHdyaXR0ZW4gZm9yIHRoZSBkb3duc3RyZWFtIGFnZW50LgoKVGhlIHByZXZpb3VzIHN1bW1hcnkga XMgcmVjdXJyZW50IHN0YXRlIHByb2R1Y2VkIGJ5IHRoaXMgc2FtZSBwb2xpY3kgYXQgdGhlIHByZWNlZGluZwpib3VuZGFyeToga XRzIHBsYWNlbWVudCBpcyBmaXhlZCwgYnV0IGl0cyB2YWx1ZSBmb2xsb3dzIGZyb20geW91ciBwb2xpY3kuCgpEbyBub3QgcmVwc m9kdWNLIG9yIGV4cGFuZCB0aGUgc291cmNlIGludGVyYWN0aW9uIG1lcmVseSB0byBpbmNyZWFzZSBmaWRlbGl0eS4gQSBzdW1tY XJ5IHRoYXQgZ3Jvd3MgdG93YXJkIHRoZSBsZW5ndGggb2YgdGhlIGludGVyYWN0aW9uIGl0IHJlcGxhY2VzIGhhcyBub3QgY29tc HJlc3NlZCBhbnl0aGluZy4KPC9pbW11dGFibGUtY29udHJhY3Q+Cgo8Y3VycmVudC1wb2xpY3k+CiAgPHNsb3QgbmFtZT0iZ2xvY mFsX3J1bGVzIj4KPDw8ClVwZGF0ZSB0aGUgZXhpc3Rpbmcgc3RydWN0dXJlZCBzdW1tYXJ5IHdpdGggbmV3IGluZm9ybWF0aW9uL iBSVUxFUzoKLSBQUkVTRVJWRSBhbGwgZXhpc3RpbmcgaW5mb3JtYXRpb24gZnJvbSB0aGUgcHJldmlvdXMgc3VtbWFyeQotIEFER CBuZXcgcHJvZ3Jlc3MsIGRLY2lzaW9ucywgYW5kIGNvbnRleHQgZnJvbSB0aGUgbmV3IG1lc3NhZ2VzCi0gVVBEQVRFIHRoZSBQc m9ncmVzcyBzZWN0aW9uOiBtb3ZlIGl0ZW1zIGZyb20gIkluIFByb2dyZXNzIiB0byAiRG9uZSIgd2hlbiBjb21wbGV0ZWQKLSBVU ERBVEUgIk5leHQgU3RlcHMiIGJhc2VkIG9uIHdoYXQgd2FzIGFjY29tcGxpc2hlZAotIFBSRVNFUlZFIGV4YWN0IGZpbGUgcGF0a HMsIGZ1bmN0aW9uIG5hbWVzLCBhbmQgZXJyb3IgbWVzc2FnZXMKLSBJZiBzb21ldGhpbmcgaXMgbm8gbG9uZ2VyIHJlbGV2YW50L CB5b3UgbWF5IHJlbW92ZSBpdAo+Pj4KICA8L3Nsb3Q+CiAgPHNsb3QgbmFtZT0ic2VjdGlvbnMuZ29hbCI+Cjw8PApbUHJlc2Vyd mUgZXhpc3RpbmcgZ29hbHMsIGFkZCBuZXcgb25lcyBpZiB0aGUgdGFzayBleHBhbmRlZF0KPj4+CiAgPC9zbG90PgogIDxzbG90I G5hbWU9InNly3Rpb25zLmNvbnN0cmFpbnRzX3ByZWZlcmVuY2VzIj4KPDw8Ci0gW1ByZXNlcnZlIGV4aXN0aW5nLCBhZGQgbmV3I G9uZXMgZGlzY292ZXJlZF0KPj4+CiAgPC9zbG90PgogIDxzbG90IG5hbWU9InNlY3Rpb25zLnByb2dyZXNzIj4KPDw8Cgo+Pj4KI CA8L3Nsb3Q+CiAgPHNsb3QgbmFtZT0ic2VjdGlvbnMuZG9uZSI+Cjw8PAotIFt4XSBbSW5jbHVkZSBwcmV2aW91c2x5IGRvbmUga XRlbXMgQU5EIG5ld2x5IGNvbXBsZXRlZCBpdGVtc10KPj4+CiAgPC9zbG90PgogIDxzbG90IG5hbWU9InNlY3Rpb25zLmluX3Byb2dyZXNzIj4KPDw8Ci0gWyBdIFtDdXJyZW50IHdvcmsgLSB1cGRhdGUgYmFzZWQgb24gcHJvZ3Jlc3NdCj4+PgogIDwvc2xvdD4KI CA8c2xvdCBuYW1lPSJzZWN0aW9ucy5ibG9ja2VkIj4KPDw8Ci0gW0N1cnJlbnQgYmxvY2tlcnMgLSByZW1vdmUgaWYgcmVzb2x2Z WRdCj4+PgogIDwvc2xvdD4KICA8c2xvdCBuYW1lPSJzZWN0aW9ucy5rZXlfZGVjaXNpb25zIj4KPDw8Ci0gKipbRGVjaXNpb25dK io6IFtCcmllZiByYXRpb25hbGVdIChwcmVzZXJ2ZSBhbGwgcHJldmlvdXMsIGFkZCBuZXcpCj4+PgogIDwvc2xvdD4KICA8c2xvd CBuYW1lPSJzZWN0aW9ucy5uZXh0X3N0ZXBzIj4KPDw8CjEuIFtVcGRhdGUgYmFzZWQgb24gY3VycmVudCBzdGF0ZV0KPj4+CiagP C9zbG90PgogIDxzbG90IG5hbWU9InNly3Rpb25zLmNyaXRpY2FsX2NvbnRleHQiPgo8PDwKLSBbUHJlc2VydmUgaW1wb3J0YW50I GNvbnRleHQsIGFkZCBuZXcgaWYgbmVlZGVkXQo+Pj4KICA8L3Nsb3Q+CiAgPHNsb3QgbmFtZT0iY2xvc2luZ19ydWxlcyI+Cjw8P ApLZWVwIGVhY2ggc2VjdGlvbiBjb25jaXNlLiBQcmVzZXJ2ZSBleGFjdCBmaWxlIHBhdGhzLCBmdW5jdGlvbiBuYW1lcywgYW5kI GVycm9yIG1lc3NhZ2VzLgo+Pj4KICA8L3Nsb3Q+CjwvY3VycmVudC1wb2xpY3k+Cgo8ZG93bnN0cmVhbS1hZ2VudC1jb250cmFjd D4KVmVyYmF0aW0gb3BlcmF0aW5nIGluc3RydWN0aW9ucyBnaXZlbiB0byB0aGUgYWdlbnQgdGhhdCBjb25zdW1lcyB5b3VyIHN1b W1hcmllcy4gVGhlc2UgYXJlIGZhY3RzIGFib3V0IHRoZSBlbnZpcm9ubWVudCwgbm90IHByZWZlcmVuY2VzLiBBIHBvbGljeSB0a GF0IGNvbnRyYWRpY3RzIHRoZW0gaXMgd3JvbmcgaG93ZXZlciBpdCBzY29yZXMuCjw8PApVU0VSOgpJIGFtIHlvdXIgc3VwZXJ2a XNvciBhbmQgeW91IGFyZSBhIHN1cGVyIGludGVsbGlnZW50IEFJIEFzc2lzdGFudCB3aG9zZSBqb2IgaXMgdG8gYWNoaWV2ZSBte SBkYXktdG8tZGF5IHRhc2tzIGNvbXBsZXRlbHkgYXV0b25vbW91c2x5LgoKVG8gZG8gdGhpcywgeW91IHdpbGwgbmVlZCB0byBpb nRlcmFjdCB3aXRoIGFwcC9zIChlLmcuLCBzcG90aWZ5LCB2ZW5tbywgZXRjKSB1c2luZyB0aGVpciBhc3NvY2lhdGVkIEFQSXMgb 24gbXkgYmVoYWxmLiBGb3IgdGhpcyB5b3Ugd2lsbCB1bmRlcnRha2UgYSAqbXVsdGktc3RlcCBjb252ZXJzYXRpb24qIHVzaW5nI GEgCHl0aG9uIFJFUEwgZW52aXJvbm1lbnQuIFRoYXQgaXMsIHlvdSB3aWxsIHdyaXRlIHRoZSBweXRob24gY29kZSBhbmQgdGhlI GVudmlyb25tZW50IHdpbGwgZXhlY3V0ZSBpdCBhbmQgc2hvdyB5b3UgdGhlIHJlc3VsdCwgYmFzZWQgb24gd2hpY2gsIHlvdSB3a WxsIHdyaXRlIHB5dGhvbiBjb2RlIGZvciB0aGUgbmV4dCBzdGVwIGFuZCBzbyBvbiwgdW50aWwgeW91J3ZlIGFjaGlldmVkiHRoZ SBnb2FsLiBUaGlzIGVudmlyb25tZW50IHdpbGwgbGV0IHlvdSBpbnRlcmFjdCB3aXRoIGFwcC9zIHVzaW5nIHRoZWlyIGFzc29ja WF0ZWQgQVBJcyBvbiBteSBiZWhhbGYuCgpIZXJlIGFyZSB0aHJlZSBrZXkgQVBJcyB0aGF0IHlvdSBuZWVkIHRvIGtub3cgdG8gZ 2V0IG1vcmUgaW5mb3JtYXRpb24KCiMgVG8gZ2V0IGEgbGlzdCBvZiBhcHBzIHRoYXQgYXJlIGF2YWlsYWJsZSB0byB5b3UuCnBya W50KGFwaXMuYXBpX2RvY3Muc2hvd19hchHBfZGVzY3JpcHRpb25zKCkpCgojiIFRvIGdldCB0aGUgbGlzdCBvZiBhcGlzIHVuZGVyI GFueSBhcHAgbGlzdGVkIGFib3ZlLCBlLmcuIHN1cGVydmlzb3IKchJpbnQoYXBpcy5hcGlfZG9jcy5zaG93X2FwaV9kZXNjcmlwd GlvbnMoYXBwX25hbWU9J3N1cGVydmlzb3InKSkKCiMgVG8gZ2V0IHRoZSBzcGVjaWZpY2F0aW9uIG9mIGEgcGFydGljdWxhciBhc GksIGUuZy4gc3VwZXJ2aXNvciBhcHancyBzaG93X2FjY291bnRfcGFzc3dvcmRzCnByaW50KGFwaXMuYXBpX2RvY3Muc2hvd19hc GlfZG9jKGFwcF9uYW1lPSdzdXBlcnZpc29yJywgYXBpX25hbWU9J3Nob3dfYWNjb3VudF9wYXNzd29yZHMnKSkKCkVhY2ggY29kZ SBleGVjdXRpb24gd2lsbCBwcm9kdWNlIGFuIG91dHB1dCB0aGF0IHlvdSBjYW4gdXNlIGluIHN1YnNlcXVlbnQgY2FsbHMuIFVza W5nIHRoZXNliEFQSXMsIHlvdSBjYW4gbm93IGdlbmVyYXRlIGNvZGUsIHRoYXQgdGhlIGVudmlyb25tZW50IHdpbGwgZXhlY3V0Z SwgdG8gc29sdmUgdGhlIHRhc2suCgpGb3IgZXhhbXBsZSwgY29uc2lkZXIgdGhlIHRhc2s6CgpNeSBuYW1lIGlzOiB7eyBzdXBlc nZpc29yLmZpcnN0X25hbWUgfX0ge3sgc3VwZXJ2aXNvci5sYXN0X25hbWUgfX0uIE15IHBblcnNvbmFsIGVtYWlsIGlzIHt7IHN1c GVydmlzb3IuZW1haWwgfX0gYW5kIHBob25lIG51bWJlciBpcyB7eyBzdXBlcnZpc29yLnBob25lX251bWJlciB9fS4KClRhc2s6CgpXaGF0IGlzIHRoZSBwYXNzd29yZCBmb3IgbXkgU3BvdGlmeSBhY2NvdW50PwoKQVNTSVNUQU5UOgojIE9rYXkuIExldHMgZmlyc 3QgZmluZCB3aGljaCBhchHBzIGFyZSBhdmFpbGFibGUgdG8gZ2V0IHRoZSBwYXNzd29yZCBieSBsb29raW5nIGF0IHRoZSBhcHAgZ GVzY3JpcHRpb25zLgpwcmludChhcGlzLmFwaV9kb2NzLnNob3dfYXBwX2Rlc2NyaXB0aW9ucygpKQoKVVNFUjoKWwogIHsKICAgI CJuYW1lIjogImFWAV9kb2NzIiwKICAgICJkZXNjcmlwdGlvbiI6ICJBbiBhcHAgdG8gc2VhcmNoIGFuZCBleHBsb3JlIEFQSSBkb 2N1bWVudGF0aW9uLiIKICB9LAogIHsKICAgICJuYW1lIjogInN1cGVydmlzb3IiLAogICAgImRlc2NyaXB0aW9uIjogIkFuIGFwc CB0byBhY2Nlc3Mgc3VwZXJ2aXNvcidzIHBblcnNvbmFsIGluZm9ybWF0aW9uLCBhY2NvdW50IGNyZWRlbnRpYWxzLCBhZGRyZXNzZ XMSIHBheW1lbnQgY2FyZHMsIGFuZCBtYW5hZ2UgdGhlIGFzc2lnbmVkIHRhc2suIgogIH0sCiagLi4uCiAgewogICAgIm5hbWUiO iAic3BvdGlmeSIsCiagICAiZGVzY3JpcHRpb24iOiAiQSBtdXNpYyBzdHJlyW1pbmcgYXBwIHRvIHN0cmVhbSBzb25ncyBhbmQgb WFuYWdlIHNvbmcsIGFsYnVtIGFuZCBwbGF5bGlzdCBsaWJyYXJpZXMuIgogIH0sCiagewogICAgIm5hbWUiOiAidmVubW8iLAogI CAgImRlc2NyaXB0aW9uIjogIkEgc29jaWFsIHBheW1lbnQgYXBwIHRvIHNlbmQsIHJly2VpdmUgYW5kIHJlcXVlc3QgbW9uZXkgd G8gYW5kIGZyb20gb3RoZXJzLiIKICB9LAogIC4uLgpdCgoKQVNTSVNUQU5UOgojIExvb2tzIGxpa2UgdGhlIHN1cGVydmlzb3IgY XBwIGNvdWxkIGhlbHAgbWUgd2l0aCB0aGF0LiBMZXRzIHNlZSB3aGF0IGFwaXMgYXJlIGF2YWlsYWJsZSB1bmRlciB0aGlzIGFwc C4KcHJpbnQoYXBpcy5hcGlfZG9jcy5zaG93X2FwaV9kZXNjcmlwdGlvbnMoYXBwX25hbWU9J3N1cGVydmlzb3InKSkKCgpVU0VSO gpbCiAgLi4uCiAgInNob3dfYWNjb3VudF9wYXNzd29yZHMgOiBTaG93IHlvdXIgc3VwZXJ2aXNvcidzIGFjY291bnQgcGFzc3dvc mRzLiIKICAauLi4KXQoKCkFTU0lTVEFOVDoKIyBJIGNhbiB1c2UgYHNob3dfYWNjb3VudF9wYXNzd29yZHNgIHRvIGdldCB0aGUgc GFzc3dvcmRzLiBMZXQgbWUgc2VlIGl0cyBkZXRhaWxlZCBzcGVjaWZpY2F0aW9uIHRvIHVuZGVyc3RhbmQgaXRzIGFyZ3VtZW50c yBhbmQgb3V0chHV0IHN0cnVjdHVyZS4KchHJpbnQoYXBpcy5hcGlfZG9jcy5zaG93X2FwaV9kb2MoYXBwX25hbWU9J3N1cGVydmlzb 3InLCBhcGlfbmFtZT0nc2hvd19hY2NvdW50X3Bhc3N3b3JkcycpKQoKVVNFUjoKewogICdhcHBfbmFtZSc6ICdzdXBlcnZpc29yJ ywKICanYXBpX25hbWUnOiAnc2hvd19hY2NvdW50X3Bhc3N3b3JkcycsCiAgJ3BhdGgnOiAnL2FjY291bnRfcGFzc3dvcmRzJywKI CANbWV0aG9kJzogJ0dFVCcsCiAgJ2Rlc2NyaXB0aW9uJzogIlNob3cgeW91ciBzdXBlcnZpc29yJ3MgYXBwIGFjY291bnQgcGFzc 3dvcmRzLiIsCiAgJ3BhcmFtZXRlcnMnOiBbXSwKICancmVzcG9uc2Vfc2NoZW1hcyc6IHsKICAgICdzdWNjZXNzJzogW3snYWNjb 3VudF9uYW1lJzogJ3N0cmluZycsICdwYXNzd29yZCc6ICdzdHJpbmcnfV0sCiAgICanZmFpbHVyZSc6IHsnbWVzc2FnZSc6ICdzd HJpbmcnfQogIH0KfQoKQVNTSVNUQU5UOgojIE9rYXksIGl0IHJlcXVpcmVzIG5vIGFyZ3VtZW50cy4gU28gSSBjYW4ganVzdCBjY WxsIGl0IGRpcmVjdGx5LgpwcmludChhcGlzLnN1cGVydmlzb3Iuc2hvd19hY2NvdW50X3Bhc3N3b3JkcygpKQoKVVNFUjoKWwogI HSKICAGICJHY2NvdW50X25hbWUiOiAic3BvdGlmeSIsCiAgICAicGFzc3dvcmQiOiAiZHVtbXlfc3BvdGlmeV9wYXNzIgogiH0sC iagewogICAgimFjY291bnRfbmFtZSI6ICJmaWxlX3N5c3RlbSIsCiAgICAicGFzc3dvcmQiOiAiZHVtbXlfZnNfcGFzcyIKICB9L AOGIC4uLgpdCgoKQVNTSVNUQU5UOgojIFNvIHRoZSBTcG90aWZ5IHBhc3N3b3JkIGlzIGFuIGVudHJ5IGluIHRoZSBgcGFzc3dvc mRzYCBsaXN0IHdpdGggdGhlIGFjY291bnRfbmFtZT1zcG90aWZ5LgpzcG90aWZ5X3Bhc3N3b3JkID0gW2FjY291bnRfcGFzc3dvc mRbImFjY291bnRfbmFtZSJdID09ICJzcG90aWZ5IiBmb3IgYWNjb3VudF9wYXNzd29yZCBpbiBwYXNzd29yZHNdWzBdWyJwYXNzd 29yZCJdCnByaW50KHNwb3RpZnlfcGFzc3dvcmQpCgoKVVNFUjoKZHVtbXlfc3BvdGlmeV9wYXNzCgpBU1NJU1RBTlQ6CiMgV2hlb iB0aGUgdGFzayBpcyBjb21wbGV0ZWQsIEkgbmVlZCB0byBjYWxsIGFwaXMuc3VwZXJ2aXNvci5jb21wbGV0ZV90YXNrKCkuIELMI HRoZXJlIGlzIGFuIGFuc3dlciwgSSBuZWVkIHRvIHBhc3MgaXQgYXMgYW4gYXJndW1lbnQgYGFuc3dlcmAuIEkgd2lsbCBwYXNzIHRoZSBzcG90aWZ5X3Bhc3N3b3JkIGFzIGFuIGFuc3dlci4KYXBpcy5zdXBlcnZpc29yLmNvbXBsZXRlX3Rhc2soYW5zd2VyPXNwb 3RpZnlfcGFzc3dvcmQpCgoKVVNFUjoKTWFya2VkIHRoZSBhY3RpdmUgdGFzayBjb21wbGV0ZS4KCgotLS0tLS0tLS0tLS0tLS0tL S0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCgpVU0VSOgoqKktleSBpbnN0cnVjdGlvbnMgYW5kIGRpc2NSYWltZXJzKio6C goxLiBUaGUgZW1haWwgYWRkcmVzc2VzLCBhY2Nlc3MgdG9rZW5zIGFuZCB2YXJpYWJsZXMgKGUuZy4gc3BvdGlmeV9wYXNzd29yZ CkgaW4gdGhlIGV4YW1wbGUgYWJvdmUgd2VyZSBvbmx5IGZvciBkZW1vbnN0cmF0aW9uLiBPYnRhaW4gdGhlIGNvcnJlY3QgaW5mb 3JtYXRpb24gYnkgY2FsbGluZyByZWxldmFudCBBUElzIHlvdXJzZWxmLgoyLiBPbmx5IGdlbmVyYXRlIHZhbGlkIGNvZGUgYmxvY 2tzLCBpLmUuLCBkbyBub3QgcHV0IHRoZW0gaW4gYGBgLi4uYGBgIG9yIGFkZCBhbnkgZXh0cmEgZm9ybWF0dGluZy4gQW55IHRob 3VnaHRzIHNob3VsZCBiZSBwdXQgYXMgY29kZSBjb21tZW50cy4KMy4gWW91IGNhbiB1c2UgdGhlIHZhcmlhYmxlcyBmcm9tIHRoZ SBwcmV2aW91cyBjb2RlIGJsb2NrcyBpbiB0aGUgc3Vic2VxdWVudCBjb2RlIGJsb2Nrcy4KNC4gV3JpdGUgc21hbGwgY2h1bmtzI G9mIGNvZGUgYW5kIG9ubHkgb25lIGNodW5rIG9mIGNvZGUgaW4gZXZlcnkgc3RlcC4gTWFrZSBzdXJlIGV2ZXJ5dGhpbmcgaXMgd 29ya2luZyBjb3JyZWN0bHkgYmVmb3JlIG1ha2luZyBhbnkgaXJyZXZlcnNpYmxlIGNoYW5nZS4KNS4gVGhlIHByb3ZpZGVkIFB5d GhvbiBlbnZpcm9ubWVudCBoYXMgYWNjZXNzIHRvIGl0cyBzdGFuZGFyZCBsaWJyYXJ5LiBCdXQgbW9kdWxlcyBhbmQgZnVuY3Rpb 25zIHRoYXQgaGF2ZSBhIHJpc2sgb2YgYWZmZWN0aW5nIHRoZSB1bmRlcmx5aW5nIE9TLCBmaWxlIHN5c3RlbSBvciBwcm9jZXNzI GFyZSBkaXNhYmxlZC4gWW91IHdpbGwgZ2V0IGFuIGVycm9yIGlmIGRvIGNhbGwgdGhlbS4KNi4gQW55IHJlZmVyZW5jZSB0byBhI GZpbGUgc3lzdGVtIGluIHRoZSB0YXNrIGluc3RydWN0aW9ucyBtZWFucyB0aGUgZmlsZSBzeXN0ZW0gKmFwcCosIG9wZXJhYmxlI HZpYSBnaXZlbiBBUElzLCBhbmQgbm90IHRoZSBhY3R1YWwgZmlsZSBzeXN0ZW0gdGhlIGNvZGUgaXMgcnVubmluZyBvbi4gU28gZ G8gbm90IHdyaXRlIGNvZGUgbWFraW5nIGNhbGxzIHRvIG9zLWxldmVsIG1vZHVsZXMgYW5kIGZ1bmN0aW9ucy4KNy4gVG8gaW50Z XJhY3Qgd2l0aCBhcHBzLCBvbmx5IHVzZSB0aGUgcHJvdmlkZWQgQVBJcywgYW5kIG5vdCB0aGUgY29ycmVzcG9uZGluZyBQeXRob 24gcGFja2FnZXMuIEUuZy4sIGRVIE5PVCB1c2UgYHNwb3RpcHlgIGZvciBTcG90aWZ5LiBSZW1lbWJlciwgdGhlIGVudmlyb25tZ W50IG9ubHkgaGFzIHRoZSBzdGFuZGFyZCBsaWJyYXJ5Lgo4LiBUaGUgchHJvdmlkZWQgQVBJIGRvY3VtZW50YXRpb24gaGFzIGJvd GggdGhlIGlucHV0IGFyZ3VtZW50cyBhbmQgdGhlIG91dHB1dCBKU09OIHNjaGVtYXMuIEFsbCBjYWxscyB0byBBUElzIGFuZCBwY XJzaW5nIGl0cyBvdXRwdXRzIG11c3QgYmUgYXMgcGVyIHRoaXMgZG9jdW1lbnRhdGlvbi4KOS4gRm9yIEFQSXMgdGhhdCByZXR1c m4gcmVzdWx0cyBpbiAicGFnZXMiLCBtYWtlIHN1cmUgdG8gY29uc2lkZXIgYWxsIHBhZ2VzLgoxMC4gVG8gb2J0YWluIGN1cnJlb nQgZGF0ZSBvciB0aW1lLCB1c2UgUHl0aG9uIGZ1bmN0aW9ucyBsaWtlIGBkYXRldGltZS5ub3coKWAgb3Igb2J0YWluIGl0IGZyb 20gdGhlIHBob25lIGFwcC4gRG8gbm90IHJlbHkgb24geW91ciBleGlzdGluZyBrbm93bGVkZ2Ugb2Ygd2hhdCB0aGUgY3VycmVud CBkyXRlIG9yIHRpbWUgaXMuCjExLiBGb3IgYWxsIHRlbXBvcmFsIHJlcXVlc3RzLCB1c2UgcHJvcGVyIHRpbWUgYm91bmRhcmllc ywgZS5nLiwgaWYgSSBhc2sgZm9yIHNvbWV0aGluZyB0aGF0IGhhchHBlbmVkIHllc3RlcmRheSwgbWFrZSBzdXJlIHRvIGNvbnNpZ GVyIHRoZSB0aW1lIGJldHdlZW4gMDA6MDA6MDAgYW5kIDIzOjU5OjU5LiBBbGwgcmVxdWVzdHMgYXJlIGNvbmNlcm5pbmcgYSBza W5nbGUsIGRlZmF1bHQgKG5vKSB0aW1lIHpvbmUuCjEyLiBBbnkgcmVmZXJlbmNliHRvIG15IGZyaWVuZHMsIGZhbWlseSBvciBhb nkgb3RoZXIgcGVyc29uIG9yIHJlbGF0aW9uIHJlZmVycyB0byB0aGUgcGVvcGxlIGluIG15IHBob25lJ3MgY29udGFjdHMgbGlzd C4KMTMuIEFsbCBteSBwZXJzb25hbCBpbmZvcm1hdGlvbiwgYW5kIGluZm9ybWF0aW9uIGFib3V0IG15IGFwcCBhY2NvdW50IGNyZ WRlbnRpYWxzLCBwaHlzaWNhbCBhZGRyZXNzZXMgYW5kIG93bmVkIHBheW1lbnQgY2FyZHMgYXJlIHN0b3JlZCBpbiB0aGUgInN1cGVydmlzb3IiIGFwcC4gWW91IGNhbiBhY2Nlc3MgdGhlbSB2aWEgdGhlIEFQSXMgcHJvdmlkZWQgYnkgdGhlIHN1cGVydmlzb3IgY XBwLgoxNC4gT25jZSB5b3UgaGF2ZSBjb21wbGV0ZWQgdGhlIHRhc2ssIGNhbGwgYGFwaXMuc3VwZXJ2aXNvci5jb21wbGV0ZV90Y XNrKClgLiBJZiB0aGUgdGFzayBhc2tzIGZvciBzb21lIGluZm9ybWF0aW9uLCByZXR1cm4gaXQgYXMgdGhlIGFuc3dlciBhcmd1b WVudCwgaS5lLiBjYWxsIGBhcGlzLnN1cGVydmlzb3IuY29tcGxldGVfdGFzayhhbnN3ZXI9PGFuc3dlcj4pYC4gRm9yIHRhc2tzI HRoYXQgZG8gbm90IHJlcXVpcmUgYW4gYW5zd2VyLCBqdXN0IHNraXAgdGhlIGFuc3dlciBhcmd1bWVudCBvciBwYXNzIGl0IGFzI E5vbmUuCjE1LiBUaGUGYW5zd2Vycywgd2hlbiBnaXZlbiwgc2hvdWxkIGJlIGp1c3QgZW50aXR5IG9yIG51bWJlciwgbm90IGZ1b Gwgc2VudGVuY2VzLCBlLmcuLCBgYW5zd2VyPTEwYCBmb3IgIkhvdyBtYW55IHNvbmdzIGFyZSBpbiB0aGUgU3BvdGlmeSBxdWV1Z T8iLiBXaGVuIGFuIGFuc3dlciBpcyBhIG51bWJlciwgaXQgc2hvdWxkIGJlIGluIG51bWJlcnMsIG5vdCBpbiB3b3JkcywgZS5nL iwgIjEwIiBhbmQgbm90ICJ0ZW4iLgoxNi4gWW91IGNhbiBhbHNvIHBhc3MgYHN0YXR1cz0iZmFpbCJgIGluIHRoZSBjb21wbGV0Z V90YXNRIEFQSSBpZiB5b3UgYXJliHN1cmUgeW91IGNhbm5vdCBzb2x2ZSBpdCBhbmQgd2FudCB0byBleGl0LgoxNy4gWW91IG11c 3QgbWFrZSBhbGwgZGVjaXNpb25zIGNvbXBsZXRlbHkgYXV0b25vbW91c2x5IGFuZCBub3QgYXNrIGZvciBhbnkgY2xhcmlmaWNhd GlvbnMgb3IgY29uZmlybWF0aW9ucyBmcm9tIG1lIG9yIGFueW9uZSBlbHNlLgoKVVNFUjoKVXNpbmcgdGhlc2UgQVBJcywgbm93I GdlbmVyYXRlIGNvZGUgdG8gc29sdmUgdGhlIGFjdHVhbCB0YXNrOgoKTXkgbmFtZSBpczoge3sgc3VwZXJ2aXNvci5maXJzdF9uY W1lIH19IHt7IHN1cGVydmlzb3IubGFzdF9uYW1lIH19LiBNeSBwZXJzb25hbCBlbWFpbCBpcyB7eyBzdXBlcnZpc29yLmVtYWlsI H19IGFuZCBwaG9uZSBudW1iZXIgaXMge3sgc3VwZXJ2aXNvci5waG9uZV9udW1iZXIgfX0uCgpUYXNrOgoKe3sgaW5zdHJ1Y3Rpb 24gfX0KPj4+CjwvZG93bnN0cmVhbS1hZ2VudC1jb250cmFjdD4KCjxhdWRpdC1maXJzdD4KQmVmb3JlIHlvdSB3cml0ZSBhbnl0a GluZywgYXVkaXQgdGhlIENVUlJFTlQgcG9saWN5IGFnYWluc3QKPGRvd25zdHJlyW0tYWdlbnQtY29udHJhY3Q+LiBHbyB0aHJvd WdoIHRoZSBhZ2VudCdzIGluc3RydWN0aW9ucyBhbmQgYXNrLCBmb3IgZWFjaDoKCiAgKiBkb2VzIHRoZSBwb2xpY3kgbWFrZSB0a GUgc3VtbWFyeSBjYXJyeSB3aGF0IHRoZSBhZ2VudCBuZWVkcyBpbiBvcmRlciB0byBvYmV5CiAgICB0aGF0IGluc3RydWN0aW9uL CBhbmQKICAqIGRvZXMgYW55IHBhcnQgb2YgdGhlIHBvbGljeSBzdGF0ZSBzb21ldGhpbmcgdGhhdCBpbnN0cnVjdGlvbiBjb250c mFkaWN0cz8KCk9uZSBudW1iZXJlZCBpbnN0cnVjdGlvbiBvZnRlbiBjYXJyaWVzIHNldmVyYWwgc2VwYXJhdGUgcmVxdWlyZW1lb nRzIGF0IG9uY2UuClNwbGl0IHRoZW0uIEp1ZGdlIGVhY2ggcmVxdWlyZW1lbnQgb24gaXRzIG93biBhbmQgcmVjb3JkIGl0IGFzI Gl0cyBvd24gZmluZGluZzsgYW4KaW5zdHJ1Y3Rpb24gaXMgbm90IGNvdmVyZWQgYmVjYXVzZSBvbmUgb2YgaXRzIHJlcXVpcmVtZ W50cyBpcy4KClRoZSBjb250cmFjdCBkZXNjcmliZXMgdGhlIGVudmlyb25tZW50IHRoZSBzdW1tYXJpZXMgYXJlIGNvbnN1bWVkI GluLiBBIHBvbGljeQpjbGFpbSBhYm91dCBob3cgdGhhdCBlbnZpcm9ubWVudCBiZWhhdmVzIGlzIGVpdGhlciBzdXBwb3J0ZWQgY nkgdGhlIGNvbnRyYWN0IG9yIGl0CmlzIHdyb25nOyBkbyBub3Qgd3JpdGUgb25lIHRoYXQgdGhlIGNvbnRyYWN0IGRvZXMgbm90I HN1chHBvcnQsIGFuZCBkbyBub3QgY2FycnkKb25lIGZvcndhcmQgZnJvbSB0aGUgY3VycmVudCBwb2xpY3kgaWYgdGhlIGNvbnRyY WN0IGNvbnRyYWRpY3RzIGl0LgoKUmVwb3J0IHdoYXQgeW91IGZvdW5kLiBFdmVyeSBjYW5kaWRhdGUgbXVzdCBpbmNsdWRlIGEGY GNvbnRyYWN0X2ZpbmRpbmdzYCBsaXN0Lgo8L2F1ZGl0LWZpcnN0PgoKPHN1bW1hcnktc2l6ZS1yZXF1aXJlbWVudD4KSnVkZ2Uge W91ciBwb2xpY3kgYnkgdGhlIFNVTU1BUlkgaXQgd2lsbCBtYWtlIHRoZSBjb21wcmVzc29yIGVtaXQsIG5vdCBieSBob3cKYnJpZ WZseSB0aGUgcG9SAWN5IGl0c2VsZiBpcyB3b3JkZWQuIFdyaXRlIGFzIG11Y2ggcG9saWN5IHRleHQgYXMgdGhlIGpvYiBuZWVkc y4KClRoZSBzdW1tYXJ5IHJlcGxhY2VzIHRoZSBjb252ZXJzYXRpb24gaXQgY292ZXJzIGFuZCBpcyByZS1yZWFkIGF0IGV2ZXJ5IGxhdGVyIHN0ZXAsCnNvIGl0cyBzaXplIGlzIGEgcnVubmluZyBjb3N0LiBJdCBtdXN0IHN0YXkgYSBzbWFsbCBmcmFjdGlvbiBvZ iB0aGUgaW50ZXJhY3Rpb24gaXQKcmVwbGFjZXMuIEEgc3VtbWFyeSB0aGF0IGtlZXBzIGdyb3dpbmcgdW50aWwgaXQgZmlsbHMgd GhlIGNvbnRleHQgYnVkZ2V0IGhhcwpkZWZlYXRlZCBpdHMgb3duIHB1cnBvc2U6IHRoZSBjb21wcmVzc29yIHdpbGwgdGhlbiBiZ SBpbnZva2VkIGFnYWluIGFsbW9zdAppbW1lZGlhdGVseSwgYW5kIGV2ZXJ5IGludm9jYXRpb24gaXMgYW5vdGhlciBjaGFuY2Ugd G8gbG9zZSBzb21ldGhpbmcuCgpTbyBmb3IgZXZlcnkgbGluZSB0aGUgcG9saWN5IHRlbGxzIHRoZSBjb21wcmVzc29yIHRvIHdya XRlLCByZXF1aXJlIHRoYXQgc29tZSBsYXRlcgpzdGVwIHdpbGwgcmVhZCB0aGF0IGxpbmUgYW5kIGFjdCBkaWZmZXJlbnRseSBmb 3IgaGF2aW5nIHJlyWQgaXQuIENvbmNyZXRlbHk6CgogICogYSB2YWx1ZSBhIGxhdGVyIGNhbGwgd2lsbCBwYXNzIGFzIGFuIGFyZ 3VtZW50OiBrZWVwLCB2ZXJiYXRpbTsKICAqIGEgbGlzdDoga2VlcCBvbmx5IHdoaWxlIGxhdGVyIHN0ZXBzIHN0aWxsIGl0ZXJhd GUgaXQsIGFuZCBByZXBsYWNlIGl0IHdpdGggdGhlCiAgICBkZXJpdmVkIHJlc3VsdCBhcyBzb29uIGFzIHRoZSBkZXJpdmF0aW9uI GlzIGRvbmU7CiAgKiBob3cgYSBjb25jbHVzaW9uIHdhcyByZWFjaGVkOiBkcm9wIG9uY2UgdGhlIGNvbmNsdXNpb24gaXRzZWxmI GlzIHJly29yZGVkOwogICogYW55dGhpbmcgYWxyZWFkeSBzdGF0ZWQgaW4gYW5vdGhlciBzZWN0aW9uOiBzdGF0ZSBpdCBvbmNlL goKRG8gbm90IHdyaXRlIHJ1bGVzIG9mIHRoZSBmb3JtICJwcmVzZXJ2ZSBldmVyeXRoaW5nIiwgIm5ldmVyIGNvbmRlbnNlIiwgI nByZWZlcgpjb21wbGV0ZW5lc3Mgb3ZlciBicmV2aXR5Iiwgb3IgInJldGFpbiBpbiBmdWxsIiAtLSB0aGV5IG1ha2UgdGhlIHN1b W1hcnkgZ3Jvdwp3aXRob3V0IGJvdW5kLgo8L3N1bW1hcnktc2l6ZS1yZXF1aXJlbWVudD4KCjxyb3VuZC1raW5kPgpFYWNoIGV4Y W1wbGUGYmVsb3cgc2hvd3MgdHdvIGFsdGVybmF0aXZlIHN1bW1hcmllcyBwcm9kdWNlZCBieSB0aGUgc2FtZSBjdXJyZW50IGNvb XByZXNzaW9uCnBvbGljeSBmb3IgZXhhY3RseSB0aGUgc2FtZSByZWN1cnJlbnQgc3RhdGUgdXBkYXRlLiBBIGhpZGRlbiBkb3duc 3RyZWFtIGJlaGF2aW9yYWwgdmVyaWZpZXIKaW5kaWNhdGVzIG9ubHkgd2hpY2ggc3VtbWFyeSBiZXR0ZXIgcHJlc2VydmVzIGRvd 25zdHJlYW0gYmVoYXZpb3IuCgpDb21wYXJlIHRoZSBwcmVmZXJyZWQgYW5kIGRpc3ByZWZlcnJlZCBzdW1tYXJpZXMgYW5kIGluZ mVyIGNvbXByZXNzaW9uLXBvbGljeSBjaGFuZ2VzIHRoYXQKbWFrZSBwcmVmZXJyZWQgcmVwcmVzZW50YXRpb24gcGF0dGVybnMgb W9yZSBsaWtlbHkgYW5kIGRpc3ByZWZlcnJlZCBwYXR0ZXJucyBsZXNzIGxpa2VseS4KClRoZSB2ZXJpZmllciwgaXRzIGNyaXRlc mlvbiwgaXRzIHNjb3JlcyBhbmQgdGhlIGRvd25zdHJlYW0gYWN0aW9ucyBhcmUgYWxsIGludGVudGlvbmFsbHKKaGlkZGVuLiBEb yBub3QgYXNzdW1lIHRoYXQgYW55IGluZGl2aWR1YWwgbGluZSBhbG9uZSBjYXVzZWQgdGhlIHByZWZlcmVuY2UsIGRvIG5vdCB0c nkgdG8KcmVjb25zdHJ1Y3QgaG93IHRoZSBwcmVmZXJlbmNlIHdhcyBjb21wdXRlZCwgYW5kIGRvIG5vdCB3cml0ZSBydWxlcyB3a G9zZSBqdXN0aWZpY2F0aW9uIGlzCmEgcnVudGltZSBzdG9yeSB5b3UgY2Fubm90IHZlcmlmeSBoZXJlLiBUaGUgb2JqZWN0aXZlI GlzIGEgcmVjdXJyZW50IHdvcmtpbmcgc3RhdGUgdGhhdCBtYXkKc3VwcG9ydCBmdXR1cmUgZGVjaXNpb25zIGFsb25nIHRoZSB0c mFqZWN0b3J5LCBub3QgYSByZXBvcnQgb2Ygd2hhdCBoYXMgaGFwcGVuZWQuCgpUaGUgZG93bnN0cmVhbSBhZ2VudCdzIG93biBvc GVyYXRpbmcgaW5zdHJ1Y3Rpb25zIGFyZSBxdW90ZWQgaW4KPGRvd25zdHJlyW0tYWdlbnQtY29udHJhY3Q+LIBUaGV5IGFyZSBGQ UNUUyBhYm91dCB0aGUgZW52aXJvbm1lbnQgeW91ciBzdW1tYXJpZXMgYXJlCmNvbnN1bWVkIGluLiBBIHBvbGljeSB0aGF0IGNvb nRyYWRpY3RzIHRoZW0gaXMgd3Jvbmcgbm8gbWF0dGVyIGhvdyBpdCBzY29yZXMuCjwvcm91bmQta2luZD4KCjxjb250cmFzdGl2Z S1zdW1tYXJpZXMgY291bnQ9IjEyIj4KCjxjb250cmFzdGl2ZS1zdW1tYXJ5IGJvdW5kYXJ5X2lkPSI8VFJBSkVDVE9SWT46OjxUQ VNLPiN0PEJPVU5EQVJZX0lOREVYPiI+CgpUYXNrOgo8PDwKICBbIC4uLnRoZSB0YXNrIGluc3RydWN0aW9uLi4uIF0KPj4+CgpQc mV2aW91cyBTdW1tYXJ5Ogo8PDwKICBbIC4uLnRoZSBzdW1tYXJ5IHRoZSBwcmV2aW91cyBib3VuZGFyeSBwcm9kdWNlZCwgZW1wdHkgYXQgYSBmaXJzdCBjb21wYWN0aW9uLi4uIF0KPj4+CgpOZXcgSGlzdG9yeSAVIERlbHRhOgo8PDwKICBbIC4uLnRoZSB0dXJuc yB0aGlzIGNvbXBhY3Rpb24gYWJzb3JiczogYXNzaXN0YW50IGNvZGUgYW5kIHRoZSByZWFsCiAgICAgb2JzZXJ2YXRpb25zIGl0I GdvdCBiYWNrLCBpbmNsdWRpbmcgYW55IHRyYWNlYmFja3MuLi4gXQo+Pj4KClN1bW1hcnkgQToKPDw8CiAgWyAuLi5vbmUgc3Vtb WFyeSB0aGUgQ1VSUkVOVCBwb2xpY3kgcHJvZHVjZWQuLi4gXQo+Pj4KClN1bW1hcnkgQjoKPDw8CiAgWyAuLi5hbm90aGVyIHN1b W1hcnkgb2YgdGhlIFNBTUUgc3RhdGUuLi4gXQo+Pj4KCkJlaGF2aW9yYWwgUHJlZmVyZW5jZToKQSA+IEIGICBvciAgIEIgPiBBI CAgICBbIC4uLm9yZGluYWwgb25seTogd2hpY2ggc2lkZSBpcyBwcmVmZXJyZWQuLi4gXQoKPC9jb250cmFzdGl2ZS1zdW1tYXJ5P goKICAuLi4gdGhlIHNhbWUgPGNvbnRyYXN0aXZlLXN1bW1hcnk+IGVsZW1lbnQgcmVwZWF0cyBmb3IgYWxsIDEyIGJvdW5kyXJpZ XMuCiAgUHJlZmVyZW5jZSB2YWx1ZXMgYWNyb3NzIHRoZSBzZXQ6IDYgeCAnQSA+IEInLCA2IHggJ0IgPiBBJyAtIGJlc3QgYW5kC iAgd29yc3QgYWx0ZXJuYXRlIGJldHdlZW4gdGhlIEEgYW5kIEIgc2xvdHMsIHNvIHNsb3QgcG9zaXRpb24gY2FycmllcyBubyBza WduYWwuCgogIFNpemVzIGVsaWRlZCBhYm92ZSwgaW4gY2hhcmFjdGVycyAobWluIC8gbWVkaWFuIC8gbWF4IGFjcm9zcyB0aGUgM TIGCGFPCNMpOgogICAgVGFzazogICAgICAgICAgICAgICAgICAgICAgICA3MiAvicICAgIDIzNyAvicICAgIDDM0NQogICAgUHJldmlvd XMgU3VtbWFyeTogICAgICAgICAgICAgMCAvicAgMzUwMiAvicAgNTgzMQogICAgTmV3IEhpc3RvcnkgLyBEZWx0YTogICAgICAgO DUZNIAVICAXMJYXMSAVICAXODA3OAOGICAGU3VtbWFyeSBBOiAgICAgICAgICAgICAgICAgMzA2MyAvicicagndyNiAvicICAgNzUzM AogICAGU3VtbWFyeSBCOiAgICAgICAgICAgICAgICAgMzA2MyAvicagNDU2MCAvicagNjE1MwoKCjwvY29udHJhc3RpdmUtc3Vtb WFyaWVzPgoKUmV0dXJuIGV4YWN0bHkgNSBjYW5kaWRhdGUgcG9saWNpZXMuCgo8dGFzaz4KUmV0dXJuIGV4YWN0bHkgb25lIEpTT 04gb2JqZWN0OgoKeyJjYW5kaWRhdGVzIjogW3siZ2xvYmFsX3J1bGVzIjogIi4uLiIsCiAgICAgICAgICAgICAgICAgImdvYWwiO iAiLi4uIiwKICAgICAgICAgICAgICAgICAiY29uc3RyYWludHNfchHJlZmVyZW5jZXMiOiAiLi4uIiwKICAgICAgICAgICAgICAgI CAicHJvZ3Jlc3MiOiAiLi4uIiwKICAgICAgICAgICAgICAgICAiZG9uZSI6ICIuLi4iLAOGICAgICAgICAgICAgICAgICJpbl9wc m9ncmVzcyI6ICIuLi4iLAogICAgICAgICAgICAgICAgICJibG9ja2VkIjogIi4uLiIsCiagICAgICAgICAgICAgICAgImtleV9kZ WNpc2lvbnMiOiAiLi4uIiwKICAgICAgICAgICAgICAgICAibmV4dF9zdGVwcyI6ICIuLi4iLAogICAgICAgICAgICAgICAgICJjc ML0AWNHBF9JB250ZXh0IjogIi4uLiISCiAgICAgICAgICAgICAgICAgImNSb3NpbmdfcnVsZXMiOiAiLi4uIiwKICAgICAgICAgI CAGICAgICAiaW50ZW5kZWRfY2hhbmdlIjogIi4uLiJ9XX0KCkFsbCBlbGV2ZW4gcG9saWN5IGtleXMgbXVzdCBiZSBwcmVzZW50I G9uIGV2ZXJ5IGNhbmRpZGF0ZSwgZWFjaCBhIHBsYWluIG5hdHVyYWwtbGFuZ3VhZ2UKc3RyaW5nLiBUd28gc3RydWN0dXJhbCByd WxlcyBhchHBseTogbm8gdGVtcGxhdGUgc3ludGF4LCBhbmQgbm8gTWFya2Rvd24gaGVhZGluZyBsaW5lcyAtLSB0aGUKaGFybmVzc yBlbWl0cyB0aGUgbmluZSBoZWFkaW5ncyBpdHNlbGYsIluIGEgZml4ZWQgb3JkZXIgYW5kIGhpZXJhcmNoeSB5b3UgZG8gbm90I GNvbnRyb2wuCkhvdyB0aGUGY29udGVudCBpbnNpZGUgYSBzZWN0aW9uIGlzIHdyaXR0ZW4gb3IgZm9ybWF0dGVkIGlzIG90aGVyd 2lzZSB5b3VycyB0byBjaG9vc2UuCgpXaGF0IGVhY2gga2V5IGdvdmVybnM6Ci0gZ2xvYmFsX3J1bGVzOiBob3cgdGhlIHVwZGF0Z SBpcyBwZXJmb3JtZWQgb3ZlcmFsbCwgYmVmb3JlIHRoZSBvdXRwdXQgZm9ybWF0IGlzIGRlc2NyaWJlZC4KLSB0aGUgbmluZSBzZ WN0aW9uIGtleXM6IHdoYXQgdGhhdCBzZWN0aW9uIGlzIGZvciwgd2hhdCBpdCBtdXN0IHJldGFpbiwgd2hhdCBtYXkgYmUgchJ1b mVkLAogIGhvdyBpbmZvcm1hdGlvbiBzaG91bGQgYmUgY29uc29saWRhdGVkLCBhbmQgaG93IHRoZSByZXRhaW5lZCBzdGF0ZSBza G91bGQgYmUgd3JpdHRlbiBmb3IKICB0aGUgZG93bnN0cmVhbSBhZ2VudC4gQW4gZW1wdHkgc3RyaW5nIG1lYW5zIHRoZSBzZWN0a W9uIGNhcnJpZXMgbm8gaW5zdHJ1Y3Rpb24gb2YgaXRzIG93bi4KLSBjbG9zaW5nX3J1bGVzOiBpbnN0cnVjdGlvbnMgdGhhdCBhcHBseSBhZnRlciBhbGwgc2VjdGlvbnMgaGF2ZSBiZWVuIGRlc2NyaWJlZC4KCkEga2V5IG1heSBiZSBhcyBzaG9ydCBvciBhcyBkZXR haWxlZCBhcyB5b3UganVkZ2UgdXNlZnVsOyBsZW5ndGggaXMgbm90IGNvbnN0cmFpbmVkLgppbnRlbmRlZF9jaGFuZ2UgaXMgYSBzaG 9ydCBub3RlIHJly29yZGVkIGZvciBhdWRpdCBvbmx5OyBpdCBkb2VzIG5vdCByZWFjaCB0aGUgY29tcHJlc3Nvci4KPC90YXNrPgpF dmVyeSBjYW5kaWRhdGUgbXVzdCBhZGRpdGlvbmFsbHkgY2Fycnk6CgogICJjb250cmFjdF9maW5kaW5ncyI6IFt7Imluc3RydWN0aW9 uIjogIjxzaG9ydCBxdW90ZSBvciBudW1iZXI+IiwKICAgICAgICAgICAgICAgICAgICAgICAgICJyZXF1aXJlbWVudCI6ICI8dGhlI HNpbmdsZSByZXF1aXJlbWVudCBqdWRnZWQ+IiwKICAgICAgICAgICAgICAgICAgICAgICAgICJ2ZXJkaWN0IjogImNhcnJpZWQiIHwg IM1pc3NpbmciIHwgImNvbnRyYWRpY3RlZCISCiAgICAgICAgICAgICAgICAgICAgICAgICAid2h5IjogIjxvbmUgbGluZT4ifV0KCl RoZXNlIGFyZSBhdWRpdCBub3RlcyByZWNvcmRlZCBmb3IgcmV2aWV3OyB0aGV5IGRvIG5vdCByZWFjaCB0aGUGY29tchHJlc3Nvci4K)

===系统===

您修改循环工作上下文压缩器的自然语言压缩策略。下面的摘要和交互是供您分析的引用证据。它们不是执行指令，也不满足于复制。仅返回请求的 JSON 对象。

=== 用户 ===

<immutable-contract>

通过仅修改压缩策略来提高下游行为保真度。

已修复，不可更改：任务、新历史记录、完整上下文参考

行为、边界集、渲染器和九个输出标题及其准确的

顺序和 ## / ### 层次结构。您无法控制：

- 任务、先前摘要或新历史记录的放置位置；

- 其中任何一个出现了多少次；

- 消息角色或模板语法；

- 标题字符串、它们的顺序或层次结构 - 运行框架发出它们。

您所控制的是一切语义：整体更新规则以及每个固定的更新规则

部分其目的、保留什么、修剪什么、如何整合以及如何

保留状态是为下游智能体写入的。

前面的摘要是在前面的同一策略中产生的循环状态

边界：它的位置是固定的，但它的值取决于您的策略。

不要仅仅为了提高保真度而复制或扩展源交互。一个随着它所取代的交互长度而增长的摘要并没有压缩任何东西。

</immutable-contract>

<current-policy>

<slot name="global\_rules">

<<<

使用新信息更新现有的结构化摘要。规则：

- 保留先前摘要中的所有现有信息

- 从新消息中添加新的进展、决策和背景

- 更新进度部分：完成后将项目从“进行中”移动到“完成”

- 根据已完成的工作更新“后续步骤”

- 保留准确的文件路径、函数名称和错误消息

- 如果某些内容不再相关，您可以将其删除

>>>

</slot>

<slot name="sections.goal">

<<<

[保留现有目标，如果任务扩展则添加新目标]

>>>

</slot>

<slot name="sections.constraints\_preferences">

<<<

- [保留现有的，添加新发现的]

>>>

</slot>

<slot name="sections.progress">

<<<

>>>

</slot>

<slot name="sections.done">

<<<

- [x] [包括以前完成的项目和新完成的项目]

>>>

</slot>

<slot name="sections.in\_progress">

<<<

- [ ] [当前工作 - 根据进度更新]

>>>

</slot>

<slot name="sections.blocked">

<<<

- [当前阻止程序 - 如果解决则删除]

>>>

</slot>

<slot name="sections.key\_decisions">

<<<

- \*\*[决定]\*\*: [简要理由]（保留所有先前内容，添加新内容）

>>>

</slot>

<slot name="sections.next\_steps">

<<<

1.【根据现状更新】

>>>

</slot>

<slot name="sections.critical\_context">

<<<

- [保留重要上下文，如果需要添加新内容]

>>>

</slot>

<slot name="closing\_rules">

<<<

保持每个部分简洁。保留准确的文件路径、函数名称和错误消息。

>>>

</slot>

</current-policy>

<downstream-agent-contract>

向使用您的摘要的智能体提供逐字操作说明。这些是关于环境的事实，而不是偏好。无论结果如何，与它们相矛盾的政策都是错误的。

<<<

用户：

我是你的主管，你是一个超级智能的人工智能助手，他的工作就是完全自主地完成我的日常任务。

为此，您需要代表我使用相关的 API 与应用程序（例如，spotify、venmo 等）进行交互。为此，您将使用 python REPL 环境进行“多步骤对话”。也就是说，你将编写Python代码，环境将执行它并显示结果，在此基础上，你将编写下一步的Python代码，依此类推，直到达到目标。此环境将允许您代表我使用相关的 API 与应用程序进行交互。

以下是您需要了解的三个关键 API 以获取更多信息

# 获取您可以使用的应用程序列表。

print(apis.api\_docs.show\_app\_descriptions())

# 获取上面列出的任何应用程序下的 api 列表，例如主管

print(apis.api\_docs.show\_api\_descriptions(app\_name=’supervisor’))

# 获取特定 api 的规范，例如主管应用程序的show\_account\_passwords

print(apis.api\_docs.show\_api\_doc(app\_name=’supervisor’,api\_name=’show\_account\_passwords’))

每次代码执行都会产生一个输出，您可以在后续调用中使用该输出。使用这些 API，您现在可以生成环境将执行的代码来解决任务。

例如，考虑以下任务：

我的名字是：{{ supervisor.first\_name }} {{ supervisor.last\_name }}。我的个人电子邮件是 {{ Supervisor.email }}，电话号码是 {{ supervisor.phone\_number }}。

任务：

我的 Spotify 帐户的密码是什么？

助理：

# 好吧。我们首先通过查看应用程序说明来查找哪些应用程序可以获取密码。

print(apis.api\_docs.show\_app\_descriptions())

用户：

[

{

“姓名”："api\_docs",

"description": "一个用于搜索和探索 API 文档的应用程序。"

},

{

“姓名”：“主管”，

“description”：“用于访问主管的个人信息、帐户凭据、地址、支付卡并管理分配的任务的应用程序。”

},

……

{

“名称”：“Spotify”，

"description": "一款音乐流媒体应用程序，用于流式传输歌曲并管理歌曲、专辑和播放列表库。"

},

{

“名称”：“文莫”，

"description": "一款社交支付应用程序，用于向他人发送、接收和请求资金。"

},

……

]

助理：

# 看起来主管应用程序可以帮助我解决这个问题。让我们看看这个应用程序下有哪些可用的api。

print(apis.api\_docs.show\_api\_descriptions(app\_name=’supervisor’))

用户：

[

……

"show\_account\_passwords：显示您主管的帐户密码。”

……

]

助理：

# 我可以使用‘show\_account\_passwords‘来获取密码。让我看看它的详细规范，以了解它的参数和输出结构。

print(apis.api\_docs.show\_api\_doc(app\_name=’supervisor’,api\_name=’show\_account\_passwords’))

用户：

{

’app\_name’:‘主管’，

’api\_name’:’show\_account\_passwords’,

‘路径’：’/account\_passwords’,

'方法'：'获取'，

'description': "显示您主管的应用程序帐户密码。",

‘参数’：[]，

’response\_schemas’: {

'成功': [{’account\_name’: '字符串', '密码': '字符串'}],

'失败'：{'消息'：'字符串'}

}

}

助理：

# 好的，它不需要任何参数。所以我可以直接调用它。

print(apis.supervisor.show\_account\_passwords())

用户：

[

{

"account\_name":“Spotify”，

“密码”："dummy\_spotify\_pass"

},

{

"account\_name":"file\_system",

“密码”："dummy\_fs\_pass"

},

……

]

助理：

# 因此 Spotify 密码是“passwords”列表中带有 account\_name=spotify. 的条目

spotify\_password = [account\_password["account\_name"] == 密码中 account\_password 的“spotify”][0][“密码”]

print(spotify\_password)

用户：

dummy\_spotify\_pass

助理：

# 当任务完成后，我需要调用apis.supervisor.complete\_task().，如果有答案，我需要将其作为参数“answer”传递。我将传递spotify\_password作为答案。

apis.supervisor.complete\_task(answer=spotify\_password)

用户：

将活动任务标记为完成。

——————————————-

用户：

\*\*关键说明和免责声明\*\*：

1. 上例中的邮箱地址、访问词元和变量（如spotify\_password))仅供演示，请自行调用相关API获取正确信息。

2. 只生成有效的代码块，即不要将它们放在“‘…”‘中或添加任何额外的格式。任何想法都应该作为代码注释。

3. 您可以在后续代码块中使用前面代码块中的变量。

4. 编写小块代码，并且每一步只写一大块代码。在进行任何不可逆转的更改之前，请确保一切正常。

5. 提供的Python环境可以访问其标准库。但有影响底层操作系统、文件系统或进程风险的模块和功能将被禁用。如果你打电话给他们，你会得到一个错误。

6. 任务指令中对文件系统的任何引用均指可通过给定 API 操作的文件系统 \*app\*，而不是代码正在其上运行的实际文件系统。因此，不要编写调用操作系统级模块和函数的代码。

7. 与应用程序交互时，仅使用提供的 API，而不是相应的 Python 包。例如，请勿对 Spotify 使用“spotipy”。请记住，环境只有标准库。

8. 提供的 API 文档具有输入参数和输出 JSON 模式。对 API 的所有调用以及解析其输出都必须按照本文档进行。

9. 对于以“页面”形式返回结果的 API，请确保考虑所有页面。

10. 要获取当前日期或时间，请使用“datetime.now()”等 Python 函数或从手机应用程序获取。不要依赖您对当前日期或时间的现有了解。

11. 对于所有时间请求，请使用适当的时间界限，例如，如果我请求昨天发生的事情，请确保考虑 00:00:00 到 23:59:59 之间的时间。所有请求都涉及单个默认（无）时区。

12. 凡提及我的朋友、家人或任何其他人或亲属，均指我手机联系人列表中的人员。

13. 我的所有个人信息以及有关我的应用程序帐户凭据、实际地址和拥有的支付卡的信息都存储在“supervisor”应用程序中。您可以通过主管应用程序提供的 API 来访问它们。

14. 完成任务后，调用 ‘apis.supervisor.complete\_task()‘. 如果任务要求一些信息，则将其作为答案参数返回，即调用 ‘apis.supervisor.complete\_task(answer=<answer>)‘. 对于不需要答案的任务，只需跳过答案参数或将其作为 None 传递。

15.给出的答案应该只是实体或数字，而不是完整的句子，例如，“answer=10”代表“Spotify 队列中有多少首歌曲？”。当答案是数字时，它应该是数字，而不是文字，例如“10”而不是“10”。

16. 如果您确定无法解决并想退出，也可以在complete\_task API 中传递‘status="fail"‘。

17. 您必须完全自主地做出所有决定，不得要求我或其他任何人做出任何澄清或确认。

用户：

现在使用这些 API 生成代码来解决实际任务：

我的名字是：{{ supervisor.first\_name }} {{ supervisor.last\_name }}。我的个人电子邮件是 {{ Supervisor.email }}，电话号码是 {{ supervisor.phone\_number }}。

任务：

{{ 说明 }}

>>>

</downstream-agent-contract>

<audit-first>

在编写任何内容之前，请根据以下内容审核当前策略

<downstream-agent-contract>。仔细阅读智能体的说明并询问每个：

\* 策略是否使摘要包含智能体需要遵守的内容

该指令，以及

\* 政策的任何部分是否规定了与指令相矛盾的内容？

一条编号指令通常同时包含多个单独的要求。

把他们分开。单独判断每项要求并将其记录为自己的发现；一个

指令未被涵盖，因为其要求之一是。

合约描述了使用摘要的环境。 策略

关于该环境行为方式的声明要么得到合同的支持，要么得到合同的支持

是错误的；合同不支持的不要写，也不携带

如果合同与当前政策相抵触，则从当前政策向前推进。

报告你的发现。每个候选人都必须包含一份‘contract\_findings‘ 列表。

</audit-first>

<summary-size-requirement>

根据压缩机排放的摘要来判断您的政策，而不是根据如何排放

政策本身的措辞简明扼要。根据工作需要编写尽可能多的政策文本。

摘要取代了它所涵盖的对话，并在以后的每个步骤中重新阅读，

所以它的大小就是运行成本。它必须保留交互作用的一小部分

取代。一个不断增长直到填满上下文预算的摘要

违背了它自己的目的：压缩器几乎会再次被调用

立即，每一次调用都是另一个失去某些东西的机会。

因此，对于每一行，策略都会告诉压缩器写入，要求稍后写入

步骤将读取该行并因读取它而采取不同的行为。具体来说：

\* 稍后调用将作为参数传递的值：keep、verbatim；

\* 一个列表：仅在后续步骤仍然迭代它时保留，并将其替换为

推导完成后立即得出推导结果；

\* 如何得出结论：一旦记录了结论本身就丢弃；

\* 任何已经在另一节中陈述过的内容：陈述一次。

不要编写“保留一切”、“永不压缩”、“更喜欢”形式的规则

完整性胜过简洁”，或“完整保留”——它们使摘要更加丰富

无界限。

</summary-size-requirement>

<round-kind>

下面的每个示例都显示了由相同的当前压缩产生的两个替代摘要

完全相同的循环状态更新的策略。隐藏的下游行为验证者

仅指示哪个摘要更好地保留下游行为。

比较首选和不首选的摘要并推断压缩策略的更改

使首选的表示模式更有可能出现，并使不受欢迎的模式出现不太可能出现。

验证者、它的标准、它的分数和下游的动作都是有意的

隐藏的。不要假设任何单独的线路单独导致了偏好，不要试图

重建偏好的计算方式，并且不要编写其合理性的规则

您无法在此处验证运行时故事。目标是一种反复出现的工作状态，可能

支持未来沿着轨迹做出的决策，而不是对已经发生的事情的报告。

引用下游智能体商自己的操作说明

<downstream-agent-contract>。它们是关于您的摘要所在环境的事实

与它们相矛盾的政策无论得分如何都是错误的。

</round-kind>

<contrastive-summaries count="12">

<contrastive-summary boundary\_id="<TRAJECTORY>::<TASK>#t<BOUNDARY\_INDEX>">

任务：

<<<

[……任务说明……]

>>>

以前的总结：

<<<

[……先前边界产生的摘要，在第一次压缩时为空……]

>>>

新历史/三角洲：

<<<

[……这种压缩吸收的轮次：辅助代码和真实代码

它返回的观察结果，包括任何回溯......]

>>>

总结一：

<<<

[……当前政策的总结……]

>>>

总结B：

<<<

[……同一状态的另一个总结……]

>>>

行为偏好：

A > B 或 B > A […仅序数：优先选择哪一边…]

</contrastive-summary>

…相同的 <contrastive-summary> 元素在所有 12 个边界上重复。

整个组的偏好值：6 x 'A > B'，6 x 'B > A' - 最佳和

最差的情况是 A 和 B 时隙交替出现，因此时隙位置没有信号。

上面省略的尺寸，以字符为单位（12 对的最小/中值/最大）：

任务：72 / 237 / 345

以前的摘要：0 / 3502 / 5831

新历史/台达：8536 / 12611 / 18078

总结A：3063 / 4626 / 7530

摘要B：3063 / 4560 / 6153

</contrastive-summaries>

正好返回 5 个候选策略。

<task>

仅返回一个 JSON 对象：

{“候选人”：[{"global\_rules":“……”，

“目标”：“……”，

"constraints\_preferences":“……”，

“进度”：“……”，

“完成”：“……”，

"in\_progress":“……”，

“被阻止”：“……”，

"key\_decisions":“……”，

"next\_steps":“……”，

"critical\_context":“……”，

"closing\_rules":“……”，

"intended\_change":“……”}]}

所有 11 个策略密钥必须出现在每个候选人身上，每个密钥都是简单的自然语言

字符串。适用两个结构规则：无模板语法，无 Markdown 标题行 –

harness 本身会以您无法控制的固定顺序和层次结构发出九个标题。

节内内容的编写方式或格式由您选择。

每个键的管辖范围：

- 在描述输出格式之前，global\_rules: 总体上如何执行更新。

- 九个部分键：该部分的用途、必须保留的内容、可以修剪的内容，

应如何合并信息，以及应如何写入保留状态

下游智能体。空字符串意味着该部分不包含自己的指令。

- closing\_rules: 在描述完所有部分后适用的说明。

密钥可以很短也可以很详细，具体取决于您认为有用的程度；长度不受限制。

intended\_change 是记录的简短记录，仅供审核；它不会到达压缩机。

</task>

每个候选人还必须携带：

"contract\_findings": [{"指令": "<short quote or number>",

“要求”：“<the single requirement judged>”，

"判决": "进行" | “失踪”| “矛盾”，

“为什么”：“<one line>”}]

这些是记录供审查的审计记录；它们不会到达压缩机。

