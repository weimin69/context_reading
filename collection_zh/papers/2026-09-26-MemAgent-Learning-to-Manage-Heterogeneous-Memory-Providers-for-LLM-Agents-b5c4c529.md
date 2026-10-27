> 本文为简体中文机器翻译，使用 Google Translate 公开接口并统一技术术语，尚未经逐句人工校对。代码、链接和公式按原文保留；实验数字及技术结论请对照原文。
> [查看本地英文原文](../../collection/papers/2026-09-26-MemAgent-Learning-to-Manage-Heterogeneous-Memory-Providers-for-LLM-Agents-b5c4c529.md) · [原始来源](https://arxiv.org/abs/2609.32521)

# MemAgent：学习为大语言模型智能体管理异构记忆系统

- 来源: https://arxiv.org/abs/2609.32521- 发布日期: 2026-09-26- 日期依据: page metadata: citation_date- 类型: paper- 主题: MemAgent、记忆路由- 抓取状态: full_text_html- 正文来源: https://arxiv.org/html/2609.32521- 抓取时间 UTC: 2026-10-26T09:38:54.442849+00:00 - 作者: Wei, Yongxian, Zhao, Yilin, Cheng, Runxi, Chen, Xinrui, Yuan, Chun, Wang, Yaoru, Yan, Jiahong, Li, Dian

## 来源摘要/页面简介

摘要：当前的智能体在任务之间基本上保持无状态，限制了他们从先前的交互中不断改进的能力，并使记忆对于长期智能体行为至关重要。现有的记忆方法试图重用过去的经验，但大多数依赖于单一的记忆表示（例如，轨迹、反思、技能、结构化知识），其有效性因任务分布而异。重新思考这个设计空间，我们评估了 13 种内存方法，发现没有一种方法可以跨基准泛化，从而揭示了管理异构内存提供程序的潜力。我们将智能体记忆制定为路由问题，其中记忆智能体决定从哪个记忆提供者检索、是否注入短期记忆以及哪个提供者应存储生成的体验。基于这个角度，我们提出了 MemAgent，具有内容感知路由架构和训练数据合成管道。路由架构结合了检索前的内容感知探测、执行期间的短期记忆门控以及选择性多提供者存储，而训练管道则综合了针对路由决策的阶段特定监督。在 GAIA、WebWalkerQA 和 xBench-DS 中，MemAgent 将平均准确度提高了 10.0%，并且在所有三个基准测试中均优于每种单独的内存方法。这些收益伴随着不到 0.3% 的路由开销和 12% 的平均任务步骤减少。

## 抓取正文（中文翻译）

# MemAgent：学习管理 LLM 智能体的异构内存提供程序

魏永贤1 赵依林2 程润熙1 陈新锐1

春园1 王耀如2 严嘉宏2 李典2

1清华大学  2腾讯

###### 摘要

目前的智能体在跨任务时基本上保持无状态，限制了它们从先前的交互中不断改进的能力，并使记忆对于长期智能体行为至关重要。现有的记忆方法试图重用过去的经验，但大多数依赖于单一的记忆表示（*例如*、轨迹、反思、技能、结构化知识），其有效性因任务分布而异。重新思考这个设计空间，我们评估了 13 种内存方法，发现没有一种方法可以跨基准泛化，从而揭示了“管理”异构内存提供程序的潜力。我们将智能体记忆表述为“路由”问题，其中内存智能体决定从哪个内存提供者检索、是否注入短期记忆以及哪个提供者应存储结果体验。基于这个角度，我们提出了 MemAgent，具有内容感知路由架构和训练数据合成管道。路由架构结合了检索前的内容感知探测、执行期间的短期记忆门控以及选择性多提供者存储，而训练管道则综合了针对路由决策的阶段特定监督。在 GAIA、WebWalkerQA 和 xBench-DS 中，MemAgent 将平均准确度提高了 10.0%，并且在所有三个基准测试中均优于每种单独的内存方法。这些收益伴随着不到 0.3% 的路由开销和 12% 的平均任务步骤减少。我们的代码可以在[此处](https://github.com/WalkerWorldPeace/MemAgent)获得。

|  |
| ---|
|  |

## 1 简介

![参考说明](https://arxiv.org/html/2609.32521v1/example_repaired_v15.png)

图 1：任务智能体与工具交互来解决任务，而过去任务的经验存储在异构内存提供程序中。通过将检索路由到适当的提供者，记忆智能体可以帮助任务智能体以更少的步骤正确地解决新任务。

LLM 智能体已迅速从单轮问答扩展到长期任务，例如网络研究、多模态推理和工具增强问题解决（[Yao et al., 2023](https://arxiv.org/html/2609.32521#bib.bib38)；[Xu et al., 2025](https://arxiv.org/html/2609.32521#bib.bib46)；[Shi et al., 2026b](https://arxiv.org/html/2609.32521#bib.bib50)；[李等人，2025b](https://arxiv.org/html/2609.32521#bib.bib45))。尽管在日益复杂的环境中运行，大多数智能体在很大程度上仍然是“跨任务无状态”：每次调用都是从头开始，没有机制可以重用先前的经验或随着时间的推移积累的学习策略。这种无状态性是持续改进的根本障碍，并限制了智能体在相关任务之间摊销精力的能力（[Xu et al., 2026](https://arxiv.org/html/2609.32521#bib.bib52); [Ouyang et al., 2026](https://arxiv.org/html/2609.32521#bib.bib54)）。因此，记忆已成为持续智能体行为的重要机制，促进了关于如何捕获、表示和重用过去的交互的丰富工作（[Du et al., 2026](https://arxiv.org/html/2609.32521#bib.bib48); [Long et al., 2026](https://arxiv.org/html/2609.32521#bib.bib49); [Li et al., 2025a](https://arxiv.org/html/2609.32521#bib.bib47);[舒等人，2026](https://arxiv.org/html/2609.32521#bib.bib51))。

现有的记忆增强智能体的主要区别在于它们如何代表过去的经验：总结轨迹（[Wang et al., 2024](https://arxiv.org/html/2609.32521#bib.bib1)）、反映的见解（[Shinn et al., 2023](https://arxiv.org/html/2609.32521#bib.bib39)）、结构化知识（[Tang et al., 2025](https://arxiv.org/html/2609.32521#bib.bib10))、工作流程模板([Wang et al., 2025c](https://arxiv.org/html/2609.32521#bib.bib6))、程序脚本([Fang et al., 2026](https://arxiv.org/html/2609.32521#bib.bib11))或可执行技能([Zheng et al., 2025](https://arxiv.org/html/2609.32521#bib.bib8))。尽管每种方法都会报告其目标基准的性能增益，但这些设计通常是单独提出和评估的。因为每种方法都致力于单一的内存表示，所以一个核心问题仍然悬而未决：*是否有任何单一的表示在不同的任务分布中保持一致有效？*

为了回答这个问题，我们将 13 种具有代表性的内存方法统一在一个通用接口下，并在三个基准测试中将每种方法作为不同的“内存提供者”进行评估：GAIA、WebWalkerQA 和 xBench DeepSearch。我们的结果显示出很强的跨基准异质性（请参阅[第 3 节](https://arxiv.org/html/2609.32521#S3“3 重新思考智能体记忆 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”中的重新思考)；没有一种方法能够普遍适用，并且在一个基准测试中表现最好的方法常常在其他基准测试中表现不佳。至关重要的是，“事后预言机”（如果任何提供商成功，则认为任务已解决）的表现比最佳个体提供商高出 18%18\% 以上。这种未开发的潜力表明，智能体记忆更多的是解决异构内存提供者的路由问题，而不是寻找单一的最佳格式。提供者不仅在存储的内容上有所不同，而且在索引和检索内容的方式上也有所不同，*例如*通过表面相似性、结构抽象或可组合的见解。因此，提供者的选择应该考虑实际检索的内容和每个提供者的传输偏差，而不是仅仅依赖于表面级别的任务相似性。

受此观察的启发，我们将智能体记忆表述为异构提供程序池上的“路由问题”（参见[图 1](https://arxiv.org/html/2609.32521#S1.F1“第 1 简介 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”））。对于每个任务，专用内存智能体𝒜M\mathcal{A}\_{M}在整个内存生命周期中做出三个决定：在执行之前从哪个长期提供者检索（开始），是否在执行期间注入短期工作内存（输入），以及哪些提供者应在之后存储结果轨迹（结束）。与静态工具路由不同，这些决策不仅取决于提供者描述，还取决于做出每个决策的执行上下文。

为了实现这个概念，我们提出了 MemAgent，一个包含两个核心组件的框架。第一个是跨越整个内存生命周期的内容感知路由架构。在开始阶段，轻量级的“探测”会在路由之前预览每个提供者。在“进入”阶段，“短期记忆门控”仅在工作记忆摘要可能有助于下一步行动时才注入工作记忆摘要。在结束阶段，“选择性多提供者存储”专门将轨迹写入可能有用的提供者，从而增强未来的检索并防止内存污染。第二个组件是训练数据合成管道。该管道通过强制探索和特定阶段的奖励信号生成对路由决策的监督，从而实现对记忆智能体的奖励过滤监督微调𝒜M\mathcal{A}\_{M}.

在 GAIA、WebWalkerQA 和 xBench-DS 中，MemAgent 的平均准确度比基线提高了 10.0%10.0%，并在所有三个基准测试中击败了所有单一提供商方法。它还提高了效率，将平均任务步骤减少了 12%12\%，同时增加了不到 0.3%0.3\% 的路由开销。

总之，我们的主要贡献有三个：

*•

  我们通过对异构内存提供者的跨基准研究来重新思考智能体记忆，结果表明没有一个提供者能够始终主导跨任务。此外，我们提出了一个图结构的长期记忆提供者和一个短期工作记忆提供者。
*•

  我们将内存表述为一个三阶段路由问题（开始/结束/结束），并提出了 MemAgent，一个由内容感知路由架构和训练数据合成管道组成的框架，用于在没有真实标签的情况下监督路由决策。
*•

  在 GAIA、WebWalkerQA 和 xBench-DS 中，MemAgent 的平均准确度比基线提高了 10.0%，并且优于所有单一提供商方法。同时，它将平均任务步骤减少了 12%12\%，同时增加了不到 0.3%0.3\% 的路由开销。

## 2 相关工作

记忆已成为实现长程智能体行为的核心机制，但最近的工作跨越了广泛且分散的设计空间（[Yu et al., 2026a](https://arxiv.org/html/2609.32521#bib.bib53); [Xiang et al., 2026](https://arxiv.org/html/2609.32521#bib.bib55)）。先前的调查按照功能角色（*例如*，工作、事实和经验记忆）和生命周期（形成、检索和精炼）等维度组织智能体记忆（[Hu et al., 2026b](https://arxiv.org/html/2609.32521#bib.bib31); [Zhang et al., 2025b](https://arxiv.org/html/2609.32521#bib.bib33)）。我们将之前的工作分为三个方向。

##### 工作记忆和情境管理。

为了主动管理上下文窗口，MEM1 ([Zhou et al., 2026b](https://arxiv.org/html/2609.32521#bib.bib24)) 在固定预算下维持紧凑的内部状态，而 AgeMem ([Yu et al., 2026b](https://arxiv.org/html/2609.32521#bib.bib25)) 将内存操作制定为 RL 训练的动作。对于长期网络和深入研究任务，智能体要么反思 重新组织步骤之间的工作空间（ARC（[Yao et al., 2026](https://arxiv.org/html/2609.32521#bib.bib20)）、IterResearch（[Chen et al., 2026](https://arxiv.org/html/2609.32521#bib.bib21)））或定期将轨迹提炼为紧凑的推理状态（ReSum（[Wu et al., 2025c](https://arxiv.org/html/2609.32521#bib.bib34))，AgentFold ([Ye et al., 2026](https://arxiv.org/html/2609.32521#bib.bib35)))。

##### 长期且可重复使用的内存。

先前的工作以多种形式研究跨任务记忆，包括总结轨迹（[Wang et al., 2024](https://arxiv.org/html/2609.32521#bib.bib1)）、反映成功和失败（[Zhao et al., 2024](https://arxiv.org/html/2609.32521#bib.bib2)）、重要性加权记忆池（[Park et al., 2023](https://arxiv.org/html/2609.32521#bib.bib3))、语义索引检索([Zhong et al., 2024](https://arxiv.org/html/2609.32521#bib.bib4))、结构化外部存储器([Wang et al., 2025a](https://arxiv.org/html/2609.32521#bib.bib26))和效用感知检索([Zhang et al., 2026c](https://arxiv.org/html/2609.32521#bib.bib27)); MemoryAgentBench（[Hu et al., 2026a](https://arxiv.org/html/2609.32521#bib.bib22)）进一步拓宽了此类系统的评估方式。相关行存储可重用的过程或技能，而不是原始轨迹，如 ReMe ([Cao et al., 2026](https://arxiv.org/html/2609.32521#bib.bib30))、Memento-Skills ([Zhou et al., 2026a](https://arxiv.org/html/2609.32521#bib.bib29)) 和 MemSkill ([Zhang et al., 2026b](https://arxiv.org/html/2609.32521#bib.bib28))。这些作品展示了长期重用的价值，但通常保留一种固定的表示形式。

##### 学习或改进内存设计本身。

除了改进固定内存系统之外，最近的工作还尝试自动化内存设计。例如，ALMA（[Xiong et al., 2026](https://arxiv.org/html/2609.32521#bib.bib23)）将内存设计作为可执行程序进行元学习，而 MemEvolve（[Zhang et al., 2026a](https://arxiv.org/html/2609.32521#bib.bib13)）则跨多个提供者池演化内存架构。自动化智能体设计框架（[Hu et al., 2025](https://arxiv.org/html/2609.32521#bib.bib36)；[Shang et al., 2025](https://arxiv.org/html/2609.32521#bib.bib37)）将内存组件视为智能体架构更广泛的搜索空间中的一个轴。这些方法与我们的观察相一致，即不同的内存设计表现出互补的行为，尽管它们寻求为整个系统提供更好的统一设计。

大多数先前的工作改进了单个内存系统或统一的内存控制器。相比之下，MemAgent 将内存异构性视为一个机会：它没有提出另一种内存格式或全局优化设计，而是学习针对异构长期提供者的推理时间路由策略，以及短期记忆门控和选择性多提供者存储。

## 3 重新思考智能体记忆

最近的记忆增强智能体的主要区别在于它们如何表示过去的经验，利用诸如经验库（[Zhao et al., 2024](https://arxiv.org/html/2609.32521#bib.bib2)）、工作流模板（[Wang et al., 2025c](https://arxiv.org/html/2609.32521#bib.bib6)）、程序脚本（[Fang et al., 2026](https://arxiv.org/html/2609.32521#bib.bib11))、知识图谱([Zhang et al., 2025a](https://arxiv.org/html/2609.32521#bib.bib32))和智能体技能([Zheng et al., 2025](https://arxiv.org/html/2609.32521#bib.bib8))。尽管每种方法都在其目标基准上取得了进步，但仍不清楚是否有任何单一内存范例在不同任务中表现一致。

##### 通用记忆的幻觉。

为了测试这个假设，我们在三个不同的基准上评估了 13 种代表性记忆方法，每种方法都用作智能体的唯一记忆系统：GAIA（一般推理）、WebWalkerQA（网络导航）和 xBench-DS（深度搜索）。

![参考说明](https://arxiv.org/html/2609.32521v1/rethink.png)

图 2：13 种内存方法相对于无内存基准的交叉基准增益。没有任何一种方法能够在所有三个基准测试中占据主导地位。星星标记每个基准测试中的最佳方法。

[如图。 2](https://arxiv.org/html/2609.32521#S3.F2“在通用内存的幻觉中。‣ 3 重新思考智能体记忆‣ MemAgent：学习管理 LLM 智能体的异构内存提供者”）显示出很强的跨基准异质性。 AWM 在 GAIA 上领先（+6.1%+6.1\%），但稍微损害了 WebWalkerQA（-0.6%-0.6\%），而 ExpeL 在 WebWalkerQA 上领先（+7.6%+7.6\%），但在 GAIA 上仅处于中等水平。没有一种方法在多个基准上是最好的。不同的任务有不同的记忆表示，因此简单地设计一个“更好”的单一记忆不太可能缩小差距。

##### 路由机会。

鉴于观察到的跨基准互补性，路由成为一种有前途的解决方案。事后预言机认为，如果 13 个单一提供程序系统中的任何一个成功，任务就已解决，其平均准确率达到 89.6%89.6\%（[表 1](https://arxiv.org/html/2609.32521#S5.T1“在 5.2 主要结果 ‣ 5 个实验 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”)）。这远远超过了最好的个体提供者 (71.0%71.0\%)，13 个提供者中有 10 个唯一地解决了至少一项任务这一事实进一步证明了这一点。这些结果揭示了基于每个任务在现有内存结构中进行选择的大量机会。如附录 [D](https://arxiv.org/html/2609.32521#A4“附录 D 为什么内存提供者表现出互补行为？‣ MemAgent：学习管理 LLM 智能体的异构内存提供者”) 中所示，提供者公开了不同的表示和检索契约；因此，选择应考虑实际检索的内容和每个提供者的传输偏差，而不仅仅是任务表面。然而，这种转变引入了信用分配挑战：任务级结果无法表明哪个提供者或阶段负责，因为存储机制仅收到延迟的反馈。

## 4 方法论

我们引入 MemAgent，这是一个内存智能体为任务智能体管理不同内存提供程序的框架。它包含两个组件：(1) 内容感知路由架构（[第 4.2 节](https://arxiv.org/html/2609.32521#S4.SS2“4.2 内容感知路由 ‣ 4 方法论 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”)），以及 (2) 数据合成管道，无需真实标签即可提供路由监督（[第 4.3 节](https://arxiv.org/html/2609.32521#S4.SS3“4.3 训练数据合成 ‣ 4 方法论 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）。 MemAgent 学习每个决策的策略，以便在整个任务执行过程中通过适当的提供者路由、注入和存储内存。 [如图。 3](https://arxiv.org/html/2609.32521#S4.F3“在 4 方法论中‣ MemAgent：学习管理 LLM 智能体 的异构内存提供程序”) 说明了整体架构。

![参考说明](https://arxiv.org/html/2609.32521v1/inference.png)

图3： 
对于每个任务，内存智能体𝒜M\mathcal{A}\_{M}做出三个路由决策。 (I) 开始：预览𝒫\mathcal{P},中的所有提供者，选择一个，并将检索到的长期记忆注入到任务智能体𝒜T\mathcal{A}\_{T}’s提示符中。 (II) 在：在每个步骤中，短期记忆提供者都会从工具交互(at,ot)(a\_{t},o\_{t}),中总结跨步骤状态，并由𝒜M\mathcal{A}\_{M}决定是否注入摘要或跳过。 （三）结束：任务完成后，𝒜M\mathcal{A}\_{M}选择子集𝒮⊆𝒫\mathcal{S}\subseteq\mathcal{P}来存储轨迹ξτ\xi\_{\tau}以备将来复用。

### 4.1 问题表述

考虑一个解决多步骤智能体任务的任务智能体𝒜T\mathcal{A}\_{T}。在每个任务τ\tau,，智能体执行状态、动作和观察的轨迹ξτ=(s0,a0,o0,…,sT,aT)\xi\_{\tau}=(s\_{0},a\_{0},o\_{0},\ldots,s\_{T},a\_{T})，产生二进制结果yτ∈{0,1}y\_{\tau}\in\{0,1\}（正确与否）。我们用内存智能体𝒜M\mathcal{A}\_{M}来增强𝒜T\mathcal{A}\_{T}，它在ξτ\xi\_{\tau}:的生命周期中做出三种类型的内存决策（i）在执行开始之前开始(dbegind\_{\text{begin}}):，𝒜M\mathcal{A}\_{M}选择长期记忆提供者p∈𝒫p\in\mathcal{P}检索注入的相关跨任务经验 在s0s\_{0};之前进入𝒜T\mathcal{A}\_{T}’s系统提示符 (ii) 在(din(t)d\_{\text{in}}^{(t)}):中，在ξτ\xi\_{\tau},𝒜M\mathcal{A}\_{M}期间的每个步骤tt中决定是注入结构化短期记忆还是跳过注入； (iii) 在ξτ\xi\_{\tau}完成后结束(dendd\_{\text{end}}):，𝒜M\mathcal{A}\_{M}选择提供者的子集𝒮⊆𝒫\mathcal{S}\subseteq\mathcal{P}来存储ξτ\xi\_{\tau}以供其他任务将来检索。

我们将记忆智能体制定为决策空间𝒟\mathcal{D}给定上下文c∈𝒞c\in\mathcal{C}（*例如*，任务状态）上的策略𝒜M​(d∣c)\mathcal{A}\_{M}(d\midc），经过训练以最大化预期成功率max𝒜M⁡𝔼τ​[yτ]\max\_{\mathcal{A}\_{M}}\;\mathbb{E}\_{\tau}[y\_{\tau}].

为了在不同的任务中利用内存多样性，MemAgent 维护了一个 KK 异构内存提供程序池。这些提供程序共享一个具有两个标准操作的统一接口：检索相关记忆并将任务轨迹存储为可重用的体验。这种抽象将路由策略与提供者内部解耦，允许𝒜M\mathcal{A}\_{M}与不同的内存范例交互，同时保持对其底层实现的不可知性。此外，我们还为任务内工作记忆提供了一个短期记忆提供程序，以及一个图结构记忆提供程序 InsightGraph。 [表 6](https://arxiv.org/html/2609.32521#A1.T6“在 A.1 内存提供程序池 ‣ 附录 A 实现细节 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”)（附录 [A.1](https://arxiv.org/html/2609.32521#A1.SS1“A.1 内存提供程序池 ‣ 附录 A 实现细节 ‣ MemAgent：学习管理LLM 智能体的异构内存提供程序”））。

### 4.2 内容感知路由

内存智能体𝒜M\mathcal{A}\_{M}将特定于阶段的决策上下文cc映射到路由操作。

开始阶段：内容感知探测。仅基于任务描述 qq 和静态提供者配置文件的路由是不可靠的（[Fioresi et al., 2026](https://arxiv.org/html/2609.32521#bib.bib56)）；重要的是提供商是否“真正拥有”相关内容。因此，我们用 *probe results* 来增强 Begin 上下文 cc。 Prior to the routing decision, 𝒜M\mathcal{A}\_{M} issues a lightweight parallel retrieval against all providers, obtaining a short snippet preview of each provider’s most relevant memory.这些预览是在没有检索分数的情况下注入的。 Since providers use incompatible scoring scales, exposing scores would teach the model a spurious “pick the highest-scored provider” shortcut rather than forcing it to reason about semantic relevance.为了减轻位置偏差，候选提供者被随机洗牌。

同相：短期记忆门控。 To determine whether to inject 短期记忆 at step tt, the 上下文 cc includes qq, the step index tt, a compact summary of the current 短期记忆 state, and the task 智能体’s recent actions (*i.e.*, recent 工具调用 and observations from ξτ\xi\_{\tau}). This allows 𝒜M\mathcal{A}\_{M} to judge whether the recalled state would materially aid the next step.

结束阶段：多提供商存储。 To facilitate the selection of providers for storing the completed trajectory, the 上下文 cc comprises a trajectory summary, the binary task outcome, and provider-specific descriptions detailing what each would extract and retain.

### 4.3 训练数据合成

![参考说明](https://arxiv.org/html/2609.32521v1/training.png)

图 4：记忆智能体的训练数据合成管道。 Forced exploration enumerates provider-action combinations for each task, producing trajectories Ξ\Xi with binary outcomes {yτ(p,a)}\{y\_{\tau}^{(p,a)}\}. Supervision signals are derived from task correctness (for Begin), LLM-as-Judge attribution (for Begin and In), and downstream reuse (for End).最后，奖励过滤保留了高质量的上下文决策对 (c,d)(c,d)，用于 𝒜M\mathcal{A}\_{M}. 的监督微调

训练𝒜M\mathcal{A}\_{M}的核心挑战是缺乏真实的路由标签。 We address this by synthesizing supervision through three stages: forced exploration, per-decision reward scoring, and reward-filtered data construction.

强制探索。 For each training task τ\tau, we systematically iterate through all providers by forcing 𝒜M\mathcal{A}\_{M} to route to each pi∈𝒫p\_{i}\in\mathcal{P} in turn, while additionally varying the In-phase action (Query or NoOp).任务智能体𝒜T\mathcal{A}\_{T}每次运行都正常执行；仅覆盖内存路由。 This process yields a trajectory set Ξ={ξτ(p,a):τ∈𝒯train,p∈𝒫,a∈𝒜}\Xi=\{\xi\_{\tau}^{(p,a)}:\tau\in\mathcal{T}\_{\mathrm{train}},\;p\in\mathcal{P},\;a\in\mathcal{A}\} with corresponding recorded outcomes {yτ(p,a)}\{y\_{\tau}^{(p,a)}\}. By observing how the *same* task performs under *every* provider, we better control for task difficulty and obtain comparisons across providers.

每个决策的奖励。 We derive fine-grained per-decision rewards from three complementary sources: current-task correctness, LLM-judge attribution, and downstream reuse.

*信号 1：任务正确性*（开始）。对于任务τ\tau,，让𝒫τ+={p:yτ(p,⋅)=1}\mathcal{P}\_{\tau}^{+}=\{p:y\_{\tau}^{(p,\cdot)}=1\}表示导致正确结果的提供者集。路由到p∈𝒫τ+p\in\mathcal{P}\_{\tau}^{+}的开始决策会收到积极的奖励。我们进一步通过可区分性进行加权：当𝒫τ+\mathcal{P}\_{\tau}^{+}是𝒫\mathcal{P},的真非空子集时，任务正确性携带最强的信号*即*，该任务将有效的提供者与无效的提供者区分开来。

*信号 2：法学硕士作为因果归因的法官*（开始/结束）。任务正确性提供了二进制信号，但无法量化特定检索或注入对 yτy\_{\tau}. 的贡献*多少*。我们采用 LLM 法官（[Zheng et al., 2023](https://arxiv.org/html/2609.32521#bib.bib40)）来检查每个决策的上下文（检索或注入的内容）以及任务智能体的后续操作（是否实际利用了内存）。法官对多个归因维度进行评分（附录 [B.2](https://arxiv.org/html/2609.32521#A2.SS2“B.2 LLM 作为法官奖励设计 ‣ 附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供者”)），我们将其汇总为标量奖励：

|  |  |  |  |
| --- | --- | --- | --- |
|  | rd=⟨𝐰(ϕ),𝐬^⟩=∑i=1Kϕwi(ϕ)​s^i,s^i={si/smax,dim. ​i↑1−si/smax,dim. ​i↓,𝐰(ϕ)∈ΔKϕ−1r\_{d}\;=\;\big\langle\mathbf{w}^{(\phi)},\,\hat{\mathbf{s}}\big\rangle\;=\;\sum\_{i=1}^{K\_{\phi}}w\_{i}^{(\phi)}\,\hat{s}\_{i},\quad\hat{s}\_{i}=\begin{cases}s\_{i}/s\_{\max},&\text{dim.\ }i\uparrow\\[-2.0pt] 1-s\_{i}/s\_{\max},&\text{dim.\ }i\downarrow\end{cases},\quad\mathbf{w}^{(\phi)}\in\Delta^{K\_{\phi}-1} |  | (1) |

其中ϕ∈{Begin,In}\phi\in\{\textsc{Begin},\textsc{In}\}表示决策阶段，KϕK\_{\phi}判断维度，si∈{0,…,smax}s\_{i}\in\{0,\dots,s\_{\max}\}是原始判断分数，↑/↓\uparrow/\downarrow表示正/负维度（*例如*，利用率与噪声）。特定阶段权重向量𝐰(ϕ)∈ΔKϕ−1\mathbf{w}^{(\phi)}\in\Delta^{K\_{\phi}-1}满足wi(ϕ)≥0w\_{i}^{(\phi)}\geq0和∑iwi(ϕ)=1\sum\_{i}w\_{i}^{(\phi)}=1.

*信号3：下游奖励*（完）。对于存储决策，我们根据实际的下游重用来定义奖励，因为只有当重用的内存“也”有助于检索任务的成功时，存储选择才有价值。令 ξτ\xi\_{\tau} 为存储在提供者 pp 中的轨迹，并令 𝒯>τ(p)={τ′>τ:Retrieved​(τ′,p)∩Stored​(ξτ,p)≠∅}\mathcal{T}\_{>\tau}^{(p)}=\{\tau^{\prime}>\tau:\textsc{Retrieved}(\tau^{\prime},p)\cap\textsc{Stored}(\xi\_{\tau},p)\neq\emptyset\} 表示后续任务集，其中从 pp 开始检索包含源自ξτ\xi\_{\tau}. 的项目。我们将*命中覆盖率*和*下游成功率*组合成单个标量奖励：

|  |  |  |  |
| --- | --- | --- | --- |
|  | rend(ξτ,p)=12min(1,|𝒯>τ(p)|H)+12⋅|{τ′∈𝒯>τ(p):yτ′=1}|max⁡(|𝒯>τ(p)|, 1)r\_{\mathrm{end}}(\xi\_{\tau},p)=\tfrac{1}{2}\min\!\Big(1,\;\frac{|\mathcal{T}\_{>\tau}^{(p)}|}{H}\Big)+\tfrac{1}{2}\cdot\frac{\big|\{\tau^{\prime}\in\mathcal{T}\_{>\tau}^{(p)}:y\_{\tau^{\prime}}=1\}\big|}{\max(|\mathcal{T}\_{>\tau}^{(p)}|,\,1)} |  | (2) |

其中Stored​(ξτ,p)\textsc{Stored}(\xi\_{\tau},p)表示由轨迹ξτ\xi\_{\tau}写入到pp的记忆项目，Retrieved​(τ′,p)\textsc{Retrieved}(\tau^{\prime},p)由任务τ′\tau^{\prime}从pp检索的项目，HH是一个饱和常数，可防止单个重度重用的轨迹主导奖励。

这三个信号是互补的：任务正确性定义了“搜索空间边界”（只有yτ=1y\_{\tau}{=}1决策进入训练池），LLM-as-Judge提供了该空间内的“质量等级”，下游奖励提供了“真实存储标签”。

奖励过滤的 SFT 数据构建。我们使用特定阶段的过滤从评分决策中构建 SFT 数据。在开始阶段，任务级正确性通过𝒫τ+\mathcal{P}\_{\tau}^{+}:充当主要过滤器（i）如果𝒫τ+\mathcal{P}\_{\tau}^{+}是𝒫\mathcal{P},的真非空子集，我们将所有决策路由到p∈𝒫τ+p\in\mathcal{P}\_{\tau}^{+};（ii）如果所有提供者都成功(𝒫τ+=𝒫\mathcal{P}\_{\tau}^{+}=\mathcal{P}),，我们保留根据法官奖励rdr\_{d};排名的top-kk决策，并且（iii）如果全部失败(𝒫τ+=∅\mathcal{P}\_{\tau}^{+}=\emptyset),，我们放弃任务。带有 rd=0r\_{d}=0, 指示空或不相关检索的决策也会被丢弃。对于 In 阶段，阈值rd≥ϵinr\_{d}\geq\epsilon\_{\textsc{in}} 保留高质量的 Query 和 NoOp 决策。类似地，结束阶段保留决策，其中 rend≥ϵendr\_{\mathrm{end}}\geq\epsilon\_{\textsc{end}}. 每个训练示例都是一个（提示，完成）对，包括决策上下文 cc 和相应的结构化路由决策，与[Sec. 2]中定义的空间相匹配。 4.2](https://arxiv.org/html/2609.32521#S4.SS2“4.2 内容感知路由 ‣ 4 方法论 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）。

SFT 培训。我们通过 LoRA 微调𝒜M\mathcal{A}\_{M}（[Hu et al., 2022](https://arxiv.org/html/2609.32521#bib.bib42)），通过屏蔽提示标记来最大限度地减少结构化决策标记上的交叉熵损失（[Ouyang et al., 2022](https://arxiv.org/html/2609.32521#bib.bib41)）。为了防止共享上下文中的数据泄漏，我们执行任务级训练验证拆分，确保同一任务的所有开始/结束/结束决策保持分组。算法 [1](https://arxiv.org/html/2609.32521#alg1“算法 1 ‣ B.1 推理管道 ‣ 附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）中总结了端到端推理管道。

## 5 个实验

在本节中，我们首先描述我们的实验设置。然后，我们展示我们的主要结果。我们还提供消融研究和讨论以进行彻底分析。

### 5.1 实验设置

基准。我们评估了需要多步骤工具使用和推理的三个智能体基准：GAIA（[Mialon et al., 2024](https://arxiv.org/html/2609.32521#bib.bib14)）（跨越三个难度级别）、WebWalkerQA（[Wu et al., 2025b](https://arxiv.org/html/2609.32521#bib.bib15)）（多轮网络导航查询）和 xBench-DS （[Chen et al., 2025](https://arxiv.org/html/2609.32521#bib.bib16)）（规划和工具使用任务）。数据集详细信息参见附录 [A.2](https://arxiv.org/html/2609.32521#A1.SS2“A.2 数据集详细信息 ‣ 附录 A 实现详细信息 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）。

智能体框架。我们使用单智能体深度研究框架Flash-Searcher（[Qin et al., 2026](https://arxiv.org/html/2609.32521#bib.bib18)）作为任务智能体，配备四个工具：WebSearch（搜索引擎查询）、CrawlPage（URL内容提取）、VisualInspector（图像分析）和AudioInspector（音频转录）。任务智能体由 GPT-5-mini 通过 API 提供支持。记忆智能体通过 LoRA 进行了 Qwen3.5-4B ([Team, 2026](https://arxiv.org/html/2609.32521#bib.bib17)) 微调（r=16r{=}16，α=32\alpha{=}32, dropout=0.05=0.05；0.84% 可训练）。

训练配置。继 MemEvolve（[Zhang et al., 2026a](https://arxiv.org/html/2609.32521#bib.bib13)）之后，训练使用 53 个 GAIA Level-1 任务和 120 个从 TaskCraft 综合生成的多跳任务（[Shi et al., 2026a](https://arxiv.org/html/2609.32521#bib.bib19)）。每个决策奖励评分使用GPT-5-mini作为LLM-as-Judge。 SFT 训练使用学习率2×10−52{\times}10^{-5},余弦计划，预热比率 0.1，有效批量大小 64，最大序列长度 4,096。

评估协议。强制探索期间积累的存储被植入到评估运行中，确保内存智能体在推理时可以访问内存池。评估遵循在线协议，当智能体系统处理连续的任务流时，经验记忆库会实时更新。任务智能体在 GAIA 上每个任务的上限为 15 个步骤，在 WebWalkerQA 和 xBench-DS 上的上限为 40 个步骤，在所有方法中统一应用。

基线。我们将 MemAgent 与不同的内存方法进行比较。 (i) No Memory 运行任务智能体而不增加任何内存。 (ii) 随机路由用随机路由决策取代记忆智能体。 (iii) MemAgent w/o 训练直接采用Qwen3.5-4B模型。 (iv) 单独记忆方法单独评估 13 个长期记忆提供者中的每一个。 (v) PromptRoute 用 GPT-5-mini 取代了 SFT 训练的记忆智能体，利用提示，其中包括每个提供者的统计数据、路由规则和从强制探索轨迹中挖掘的代表性案例（参见附录 [C.2](https://arxiv.org/html/2609.32521#A3.SS2 “C.2 PromptRoute：决策知识库 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序"))。 (vi) MemAgent（5 个提供商）将我们的智能体限制为为跨基准互补性而选择的精选子集（ExpeL、AWM、SkillWeaver、Voyager 和 InsightGraph），从而隔离了提供商池大小的影响。 (vii) Oracle 在可用时为每个任务选择成功的提供者，定义路由的上限。 (viii) All-Concat 在开始阶段从所有内存提供者检索并连接它们的输出。 (ix) All-Fuse 执行相同的记忆检索，但使用 LLM 将检索到的内容合并到单个记忆笔记中。

### 5.2 主要结果

表 1：GAIA、WebWalkerQA 和 xBench-DS 的准确度 (%)。灰色增量显示相对于无内存基线的百分比变化。 GAIA 结果按难度级别详细列出（L​1L1–L​3L3）。粗体和下划线表示最好和第二好的记忆方法。

|  |  |  |  |  |  |  |  |
| ---| ---| ---| ---| ---| ---| ---| ---|
|方法|盖亚 | | | | WebWalkerQA | xBench-DS |平均。 |
|总体 | 1 级 | 2 级 | 3 级 |
|没有记忆| 58.8 | 73.6 | 73.6 54.7 | 54.7 42.3 | 42.3 69.4 | 69.4 69.0 | 69.0 65.7 | 65.7
|个人记忆方法| | | | | | | |
| 智能体-KB ([Tang et al., 2025](https://arxiv.org/html/2609.32521#bib.bib10)) | 60.0 +1.2 | 73.6 | 73.6 54.7 | 54.7 50.0 | 50.0 70.0 +0.6 | 71.0 +2.0 | 67.0 +1.3 |
|轻量级 ([Zhang et al., 2026a](https://arxiv.org/html/2609.32521#bib.bib13)) | 59.4 +0.6 | 67.9 | 67.9 61.6 | 61.6 34.6 | 34.6 73.5 +4.1 | 73.0 +4.0 | 68.6 +2.9 |
| ExpeL ([Zhao et al., 2024](https://arxiv.org/html/2609.32521#bib.bib2)) | 61.8 +3.0 | 73.6 | 73.6 61.6 | 61.6 38.5 | 38.5 77.1 +7.6 | 74.0 +5.0 | 71.0 +5.2 |
| SkillWeaver ([Zheng et al., 2025](https://arxiv.org/html/2609.32521#bib.bib8)) | 63.6 +4.8 | 71.7 | 71.7 66.3 | 66.3 38.5 | 38.5 70.0 +0.6 | 77.0 +8.0 | 70.2 +4.5 |
| Voyager ([Wang et al., 2024](https://arxiv.org/html/2609.32521#bib.bib1)) | 64.2 +5.5 | 77.4 | 77.4 64.0 | 64.0 38.5 | 38.5 70.6 +1.2 | 68.0--1.0| 67.6 +1.9 |
| InsightGraph（我们的）| 61.8 +3.0 | 69.8 | 69.8 59.3 | 59.3 53.8 | 53.8 72.4 +2.9 | 75.0 +6.0 | 69.7 +4.0 |
| DILU ([Wen et al., 2024](https://arxiv.org/html/2609.32521#bib.bib5)) | 59.4 +0.6 | 69.8 | 69.8 61.6 | 61.6 30.8 | 30.8 71.8 +2.4 | 75.0 +6.0 | 68.7 +3.0 |
|生成（[Park et al., 2023](https://arxiv.org/html/2609.32521#bib.bib3)）| 60.6 +1.8 | 75.5 | 75.5 58.1 | 58.1 38.5 | 38.5 72.4 +2.9 | 72.0 +3.0 | 68.3 +2.6 |
| Memp ([Fang et al., 2026](https://arxiv.org/html/2609.32521#bib.bib11)) | 61.8 +3.0 | 73.6 | 73.6 61.6 | 61.6 38.5 | 38.5 72.4 +2.9 | 70.0 +1.0 | 68.1 +2.3 |
|备忘单（[Suzgun 等人，2026](https://arxiv.org/html/2609.32521#bib.bib7)）| 60.6 +1.8 | 69.8 | 69.8 59.3 | 59.3 46.2 | 46.2 70.6 +1.2 | 70.0 +1.0 | 67.1 +1.4 |
| AWM ([Wang et al., 2025c](https://arxiv.org/html/2609.32521#bib.bib6)) | 64.8 +6.1 | 75.5 | 75.5 64.0 | 64.0 46.2 | 46.2 68.8 --0.6 | 68.8 --0.6 69.0 +0.0 | 67.5 +1.8 |
| EvolveR ([Wu et al., 2026](https://arxiv.org/html/2609.32521#bib.bib12)) | 60.6 +1.8 | 66.0 | 65.1 | 65.1 34.6 | 34.6 71.8 +2.4 | 71.0 +2.0 | 67.8 +2.1 |
| Mobile-E ([Wang et al., 2025b](https://arxiv.org/html/2609.32521#bib.bib9)) | 63.6 +4.8 | 81.1 | 81.1 62.8 | 62.8 30.8 | 30.8 74.1 +4.7 | 71.0 +2.0 | 69.6 +3.9 |
|路由方式| | | | | | | |
|随机路由| 58.2−-0.6 | 58.2−-0.6 67.9 | 67.9 58.1 | 58.1 38.5 | 38.5 72.4 +3.0 | 71.0 +2.0 | 67.2 +1.5 |
| MemAgent 无需培训 | 63.6 +4.8 | 71.7 | 71.7 67.4 | 67.4 34.6 | 34.6 70.6 +1.2 | 70.0 +1.0 | 68.1 +2.4 |
| MemAgent（5 个提供商）| 63.6 +4.8 | 77.4 | 77.4 61.6 | 61.6 42.3 | 42.3 72.9 +3.5 | 73.0 +4.0 | 69.8 +4.1 |
|提示路线 | 65.5 +6.7 | 77.4 | 77.4 64.0 | 64.0 46.2 | 46.2 71.2 +1.8 | 76.0 +7.0 | 70.9 +5.2 |
|全连 | 62.4 +3.6 | 79.2 | 79.2 61.6 | 61.6 30.8 | 30.8 74.1 +4.7 | 73.0 +4.0 | 69.8 +4.1 |
|全保险丝 | 63.6 +4.8 | 83.0 | 60.5 | 60.5 34.6 | 34.6 75.3 +5.9 | 74.0 +5.0 | 71.0 +5.3 |
| MemAgent（我们的）| 69.7 +10.9 | 83.0 | 67.4 | 67.4 50.0 | 50.0 79.4 +10.0 | 78.0 +9.0 | 75.7 +10.0 |
|上限 | | | | | | | |
|甲骨文（13 家提供商）| 87.3 +28.5 | 94.3 | 94.3 87.2 | 87.2 73.1 | 73.1 89.4 +20.0 | 92.0 +23.0 | 89.6 +23.8 |

[表 1](https://arxiv.org/html/2609.32521#S5.T1“在 5.2 主要结果 ‣ 5 个实验 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）显示了所有三个基准测试的结果。 MemAgent 与无内存基准相比取得了一致的收益，总体平均提高了 10.0%。至关重要的是，MemAgent 在所有基准测试中都超越了每个单一提供商的基准：GAIA 上 +4.9%（相对于 AWM），WebWalkerQA 上 +2.3%（相对于 ExpeL），xBench 上 +1.0%（相对于 SkillWeaver）。虽然不同的单独方法在特定基准测试中占据主导地位，但 MemAgent 始终优于所有方法。这验证了学习路由有效地捕获了整个提供商池的互补优势。在 GAIA 上，这些改进在所有难度级别上都保持一致。为了进一步理清这些收益的来源，我们研究了两种受控变体，它们隔离了路由和训练的作用。用随机策略（随机路由）替换内存智能体无法恢复 MemAgent 的性能，这表明改进来自“学习”而不是任意路由。未经训练的 MemAgent 同样不及 MemAgent，这表明仅靠模型的指令跟踪能力是不够的，而训练对于有效路由至关重要。

提示路线。我们研究路由知识是否可以提炼成提示，而不是通过 SFT 学习。 PromptRoute 用冻结的 LLM 取代了经过 SFT 训练的智能体，并使用决策知识库 (DKB) 优化了其提示。该 DKB 从强制探索轨迹中提取性能统计数据、路由规则和代表性示例，以进行推理时注入。 PromptRoute 在基准测试中的平均成绩为 70.9%（比无记忆基线高出 5.2%），证明了 LLM 挖掘知识的有效性。然而，MemAgent 的性能仍然优于它，这证实了 SFT 比单独基于提示的检索捕获了更细粒度的路由区别。我们认为法学硕士挖掘的即时优化是未来工作的一个有希望的方向。

提供商池大小。 MemAgent（5 个提供商）将路由限制为五个互补提供商的精选子集。该变体总体达到 69.8%，落后于完整的 13 提供商系统。尽管它的性能优于无内存基线并可与大多数单一提供商方法相媲美，但这种差距强调了提供商多样性的重要性。排除的提供商（*例如*、LightWeight、Memp、DILU 和 Mobile-E）显然提供了完整路由模型成功利用的互补优势。

表 2：GAIA 上的训练管道消融。准确性 （％）; Δ\Delta = 相对于完整模型的下降。

| Configuration | Accuracy (%) | | | | Δ\Delta |
| ---| ---| ---| ---| ---| ---|
|  |奥夫。 | L1 | L2 | L3 |
|基础（全部判断，不探测，不过滤） | 60.6 | 60.6 75.5 | 75.5 61.6 | 61.6 26.9 | 26.9 – |
|不开始正确性过滤 | 62.4 | 62.4 79.2 | 79.2 60.5 | 60.5 34.6 | 34.6 +7.3 |
|无需去除探针分数 | 63.0 | 77.4 | 77.4 64.0 | 64.0 30.8 | 30.8 +6.7 |
|没有阈值过滤 | 63.6 | 79.2 | 79.2 61.6 | 61.6 38.5 | 38.5 +6.1 |
|没有最终下游奖励 | 66.7 | 66.7 75.5 | 75.5 68.6 | 42.3 | 42.3 +3.0 |
| MemAgent（完整）| 69.7 | 69.7 83.0 | 67.4 | 67.4 50.0 | 50.0 – |

表 3：GAIA 上的推理架构消融。准确性 （％）;选择性商店针对选定的提供商，全商店针对所有 13 家提供商。

|开始|在 |结束 |准确度 (%) | | | |
| ---| ---| ---| ---| ---| ---| ---|
|奥夫。 | L1 | L2 | L3 |
| ✗ | ✗ | ✗ | 58.8 | 73.6 | 73.6 54.7 | 54.7 42.3 | 42.3
| ✗ | ✓ | ✗ | 63.0 | 77.4 | 77.4 64.0 | 64.0 30.8 | 30.8
| ✓ | ✓ |全店 | 65.5 | 65.5 81.1 | 81.1 64.0 | 64.0 38.5 | 38.5
| ✓ | ✓ |选择性| 69.7 | 69.7 83.0 | 67.4 | 67.4 50.0 | 50.0

从所有提供者检索。检索和组合来自每个提供者的记忆可能会引入冗余、不相关或冲突的上下文。 [表 1](https://arxiv.org/html/2609.32521#S5.T1“在 5.2 主要结果 ‣ 5 个实验 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供者”）中的所有提供者基线测试了仅广泛的覆盖范围是否可以取代选择性路由，并支持选择特定于提供者的内容而不是不加区别的聚合。

### 5.3 分析与讨论

##### 消融研究。

我们进行了两项系统的消融研究，以隔离训练数据合成管道和三相推理架构的贡献。 [表 3](https://arxiv.org/html/2609.32521#S5.T3“在 5.2 主要结果 ‣ 5 个实验 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供者”）提出了 GAIA 的留一消融。与使用启发式 LLM 作为法官奖励（无需探测或过滤）的基本配置相比，我们的四个组件的综合性能提升了 +9.1%。开始正确性过滤影响最大 (+7.3%)；使用真实结果而不是智能体分数对于更困难的任务至关重要（将 L3 从 34.6% 提升到 50.0%）。删除探测分数 (+6.7%) 可防止智能体利用不兼容的度量标准（*例如*，原始计数与余弦相似度）来天真地选择得分最高的提供商。同相阈值过滤可以抑制短期记忆过度查询，否则会降低长期性能。最后，下游最终奖励 (+3.0%) 通过测量实际内存重用来优化存储决策。

[表 3](https://arxiv.org/html/2609.32521#S5.T3“在 5.2 主要结果 ‣ 5 个实验 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供者”）通过改变是否检索长期记忆、是否注入短期记忆以及存储是选择性的还是不加区别的来消除三阶段推理。 In-only 配置（基于规则的短期记忆注入，无需长期检索或存储）比基线提高了 4.2%，证实了任务内工作记忆的价值。强制全存储消融（存储所有提供商的每个轨迹）仅实现了 65.5%。发生这种情况是因为不加区别的存储用低相关性内存污染了检索池。这凸显了选择性结束阶段路由的必要性；如果没有它，存储的低质量记忆的噪音就会抵消长期记忆的好处。

##### 任务智能体传输。

我们用 GPT-5.6 Luna 替换 GPT-5-mini 并转移记忆智能体而无需重新训练。 [表 4](https://arxiv.org/html/2609.32521#S5.T4“消融研究中。‣ 5.3 分析和讨论 ‣ 5 个实验 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）表明，MemAgent 总体上在每个难度级别上都优于无内存设置和最佳固定提供程序，这表明学习的路由在任务智能体主干中仍然有效。附录 [C.1](https://arxiv.org/html/2609.32521#A3.SS1“C.1 路由器容量 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 智能体 的异构内存提供程序”) 进一步检查路由器容量的影响。

表 4：零样本传输到 GAIA 上的GPT-5.6 Luna。

|方法|总体 | L1 | L2 | L3 |
| ---| ---| ---| ---| ---|
|没有记忆| 67.9 | 67.9 77.4 | 77.4 68.6 | 46.2 | 46.2
| AWM（最佳提供商）| 69.7 | 69.7 77.4 | 77.4 68.6 | 57.7 | 57.7
| MemAgent（零射击）| 71.5 | 71.5 79.2 | 79.2 69.8 | 69.8 61.5 | 61.5

##### 推理开销。

一个自然的担忧是内存增强推理的计算成本； [表 5](https://arxiv.org/html/2609.32521#S5.T5“推理开销。‣ 5.3 分析和讨论 ‣ 5 个实验 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）详细介绍了 GAIA 上的每个任务开销。注入到任务智能体上下文中的内存文本量非常小，每个任务总计 ∼\sim1.2K 词元（少于任务智能体每个任务平均词元的 0.5%）。虽然注入开销是所有内存增强方法所固有的，但与其他 13 个提供程序相比，MemAgent 的注入大小仍然适中，例如 ∼\sim970 词元的 ExpeL（请参阅附录 [C.4](https://arxiv.org/html/2609.32521#A3.SS4“C.4 注入开销 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 的异构内存提供程序）智能体”））。 MemAgent 独特的路由成本涉及通过 4B 参数模型进行并行探测和推理。此步骤仅增加每个任务 1.2 秒的时间，或不到平均延迟的 0.3%。至关重要的是，记忆增强实际上“减少”了任务步骤的总数。 MemAgent 平均需要 8.0 步，而无内存基线则需要 9.1 步（减少了 12%）。这种效率提升在较困难的任务中最为明显，L3 步数从 12.3 下降到 10.7，因为检索到的记忆有助于智能体避免无效的探索。

表 5：MemAgent 在 GAIA 上的推理开销。注入大小计算添加到每个任务智能体提示的内存词元。路由延迟是 MemAgent 每个任务的额外挂钟成本。

|  |  |  |
| ---| ---| ---|
|组件|每任务成本 |笔记|
|内存注入（将词元插入上下文）： | | |
| Begin (long-term retrieval) | ∼\sim370 tokens | median 268, max 2.2K |
| In (short-term, per step) | ∼\sim210 tokens | 3.8 steps/task triggered |
| Total injected per task | ∼\sim1.2K tokens | <<0.5% of task tokens |
|路由成本（特定于 MemAgent）： | | |
| Probe (13 providers, parallel) | ∼\sim75 ms | one-time at Begin |
| Memory agent inference (4B) | ∼\sim80 ms/decision | ∼\sim9 decisions/task |
| Total routing latency | ∼\sim1.2 s/task | <<0.3% of task time |
|任务效率：| | |
| Avg. steps (No Memory →\to MemAgent) | 9.1 →\to 8.0 steps | −-12% |

## 6 结论

在本文中，我们从异构性的角度重新审视智能体记忆，并介绍了 MemAgent，一个三阶段路由框架。其内容感知架构和数据合成管道可监督跨提供商的长期检索、短期记忆使用和选择性存储。在三个基准测试中，MemAgent 将平均准确度提高了 10.0%，优于单一提供商基准，同时以最小的路由开销减少了任务步骤。总的来说，我们的结果支持整个内存生命周期的自适应、内容感知编排。

## 附录内容

|  |  |  |
| ---| ---| ---|
|一个 | [实现细节](https://arxiv.org/html/2609.32521#A1“附录A实现细节‣MemAgent：学习管理LLM智能体的异构内存提供者”）| [A](https://arxiv.org/html/2609.32521#A1“附录 A 实现细节 ‣ MemAgent：学习管理 LLM 智能体 的异构内存提供程序”) |
|  | [A.1 内存提供程序池](https://arxiv.org/html/2609.32521#A1.SS1“A.1 内存提供程序池 ‣ 附录 A 实现细节 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) | [A.1](https://arxiv.org/html/2609.32521#A1.SS1“A.1 内存提供程序池 ‣ 附录 A 实现细节 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) |
|  | [A.2 数据集详细信息](https://arxiv.org/html/2609.32521#A1.SS2“A.2 数据集详细信息 ‣ 附录 A 实现细节 ‣ MemAgent：学习管理 LLM 智能体 的异构内存提供程序”) | [A.2](https://arxiv.org/html/2609.32521#A1.SS2“A.2 数据集详细信息 ‣ 附录 A 实现详细信息 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) |
|  | [A.3 培训详情](https://arxiv.org/html/2609.32521#A1.SS3“A.3 培训详情 ‣ 附录 A 实施细节 ‣ MemAgent：学习管理 LLM 智能体 的异构内存提供者”) | [A.3](https://arxiv.org/html/2609.32521#A1.SS3“A.3 培训详细信息 ‣ 附录 A 实施详细信息 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) |
|  | [A.4 评估详细信息](https://arxiv.org/html/2609.32521#A1.SS4“A.4 评估详细信息 ‣ 附录 A 实现细节 ‣ MemAgent：学习管理 LLM 智能体 的异构内存提供程序”) | [A.4](https://arxiv.org/html/2609.32521#A1.SS4“A.4 评估详细信息 ‣ 附录 A 实现详细信息 ‣ MemAgent：学习管理 LLM 智能体 的异构内存提供程序”) |
|  | [A.5 提供程序实现参数](https://arxiv.org/html/2609.32521#A1.SS5“A.5 提供程序实现参数 ‣ 附录 A 实现细节 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) | [A.5](https://arxiv.org/html/2609.32521#A1.SS5“A.5 提供程序实现参数 ‣ 附录 A 实现细节 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) |
|乙| [方法详细信息](https://arxiv.org/html/2609.32521#A2“附录B方法详细信息‣MemAgent：学习管理LLM智能体的异构内存提供程序”）| [B](https://arxiv.org/html/2609.32521#A2“附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体 的异构内存提供程序”) |
|  | [B.1 推理管道](https://arxiv.org/html/2609.32521#A2.SS1“B.1 推理管道 ‣ 附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体 的异构内存提供程序”) | [B.1](https://arxiv.org/html/2609.32521#A2.SS1“B.1 推理管道 ‣ 附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) |
|  | [B.2 LLM-as-Judge 奖励设计](https://arxiv.org/html/2609.32521#A2.SS2 "B.2 LLM-as-Judge 奖励设计 ‣ 附录 B 方法细节 ‣ MemAgent: 学习管理 LLM 智能体 的异构内存提供者") | [B.2](https://arxiv.org/html/2609.32521#A2.SS2“B.2 LLM 作为评委奖励设计 ‣ 附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) |
|  | [B.3 InsightGraph](https://arxiv.org/html/2609.32521#A2.SS3“B.3 InsightGraph：自适应图内存‣附录 B 方法详细信息‣MemAgent：学习管理 LLM 智能体的异构内存提供程序”) | [B.3](https://arxiv.org/html/2609.32521#A2.SS3 "B.3 InsightGraph: 自适应图内存 ‣ 附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序") |
|  | [B.4 短期记忆提供程序](https://arxiv.org/html/2609.32521#A2.SS4“B.4 短期记忆提供程序 ‣ 附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) | [B.4](https://arxiv.org/html/2609.32521#A2.SS4“B.4 短期记忆提供程序 ‣ 附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) |
|  | [B.5 决策提示格式和输出模式](https://arxiv.org/html/2609.32521#A2.SS5“B.5 决策提示格式和输出模式 ‣ 附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体 的异构内存提供程序”) | [B.5](https://arxiv.org/html/2609.32521#A2.SS5“B.5 决策提示格式和输出模式 ‣ 附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) |
| C | [进一步分析](https://arxiv.org/html/2609.32521#A3“附录C进一步分析‣MemAgent：学习管理LLM智能体的异构内存提供者”)| [C](https://arxiv.org/html/2609.32521#A3“附录C进一步分析‣MemAgent：学习管理LLM智能体的异构内存提供者”)|
|  | [C.1 路由器容量](https://arxiv.org/html/2609.32521#A3.SS1“C.1 路由器容量 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 智能体 的异构内存提供程序”) | [C.1](https://arxiv.org/html/2609.32521#A3.SS1“C.1 路由器容量 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 智能体 的异构内存提供程序”) |
|  | [C.2 PromptRoute：决策知识库](https://arxiv.org/html/2609.32521#A3.SS2“C.2 PromptRoute：决策知识库‣附录C进一步分析‣MemAgent：学习管理LLM智能体的异构内存提供程序”）| [C.2](https://arxiv.org/html/2609.32521#A3.SS2“C.2 PromptRoute：决策知识库 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) |
|  | [C.3 路由行为](https://arxiv.org/html/2609.32521#A3.SS3“C.3 路由行为 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) | [C.3](https://arxiv.org/html/2609.32521#A3.SS3“C.3 路由行为 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) |
|  | [C.4 注入开销](https://arxiv.org/html/2609.32521#A3.SS4“C.4 注入开销 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) | [C.4](https://arxiv.org/html/2609.32521#A3.SS4“C.4 注入开销 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) |
| d | [为什么内存提供者表现出互补行为？](https://arxiv.org/html/2609.32521#A4“附录D为什么内存提供者表现出互补行为？‣MemAgent：学习管理LLM智能体的异构内存提供者”）| [D](https://arxiv.org/html/2609.32521#A4“附录 D 为什么内存提供者表现出互补行为？‣ MemAgent：学习管理 LLM 智能体的异构内存提供者”) |
|  | [D.1 三个代表性系列及其失败模式](https://arxiv.org/html/2609.32521#A4.SS1“D.1 三个代表性系列及其失败模式 ‣ 附录 D 为什么内存提供者表现出互补行为？ ‣ MemAgent：学习管理 LLM 智能体的异构内存提供者”) | [D.1](https://arxiv.org/html/2609.32521#A4.SS1“D.1 三个代表性 系列及其失败模式 ‣ 附录 D 为什么内存提供者表现出互补行为？ ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序") |
|  | [D.2 定性视角：任务表面和转移要求](https://arxiv.org/html/2609.32521#A4.SS2“D.2 定性视角：任务表面和转移要求 ‣ 附录 D 为什么内存提供者表现出互补行为？ ‣ MemAgent：学习管理 LLM 智能体的异构内存提供者”) | [D.2](https://arxiv.org/html/2609.32521#A4.SS2“D.2 定性视角：任务表面和传输要求‣附录 D 为什么内存提供者表现出互补行为？‣MemAgent：学习管理 LLM 智能体的异构内存提供者”) |
|  | [D.3 案例研究：存储中的互补传输模式](https://arxiv.org/html/2609.32521#A4.SS3“D.3 案例研究：存储中的互补传输模式 ‣ 附录 D 为什么内存提供者表现出互补行为？ ‣ MemAgent：学习管理 LLM 智能体的异构内存提供者”) | [D.3](https://arxiv.org/html/2609.32521#A4.SS3“D.3 案例研究：存储中的互补传输模式 ‣ 附录 D 为什么内存提供程序表现出互补行为？ ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) |
|  | [D.4 影响](https://arxiv.org/html/2609.32521#A4.SS4“D.4 影响 ‣ 附录 D 为什么内存提供程序表现出互补行为？ ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) | [D.4](https://arxiv.org/html/2609.32521#A4.SS4“D.4 含义 ‣ 附录 D 为什么内存提供程序表现出互补行为？ ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) |

## Appendix A Implementation Details

本节概述了我们实验的内存提供程序池、数据集、训练和评估详细信息，然后是每个提供程序的实现参数。

### A.1 Memory Provider Pool

表 [6](https://arxiv.org/html/2609.32521#A1.T6“表 6 ‣ A.1 内存提供程序池 ‣ 附录 A 实现细节 ‣ MemAgent：学习管理 LLM 智能体 的异构内存提供程序”）总结了 MemAgent 使用的综合提供程序池。该池由 13 个异构长期提供者组成，涵盖探索记忆、经验学习、工作流归纳、程序记忆、原理演化和图结构记忆，以及一个专为任务内状态聚合而设计的短期记忆提供者。值得注意的是，我们向该框架引入了两个自定义提供程序：InsightGraph（图形结构的长期提供程序）和基于规则的短期记忆提供程序。这些新颖组件的全面实现细节可在附录 [B.3](https://arxiv.org/html/2609.32521#A2.SS3“B.3 InsightGraph：自适应图形内存‣附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体 的异构内存提供程序”)和附录 [B.4](https://arxiv.org/html/2609.32521#A2.SS4“B.4 短期记忆提供程序 ‣附录 B 方法详细信息”中找到‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）。

表 6：MemAgent 中的内存提供程序。该池包含 13 个跨越不同内存范式的异构长期提供程序，以及一个用于任务内状态聚合的短期记忆提供程序。存储策略：从过去的轨迹中提取并保存的具体信息；检索机制：用于查询新任务的相关记忆的方法。

|  |  |  |  |
| ---| ---| ---| ---|
|供应商|记忆范式|存储策略|检索机制 |
| Voyager ([Wang et al., 2024](https://arxiv.org/html/2609.32521#bib.bib1)) |探索记忆|通过嵌入精炼轨迹摘要 |任务相似度的语义搜索 |
| ExpeL ([Zhao et al., 2024](https://arxiv.org/html/2609.32521#bib.bib2)) |体验学习|双路径：所有结果的洞察+成功的精细轨迹|混合洞察+轨迹检索|
|生成（[Park et al., 2023](https://arxiv.org/html/2609.32521#bib.bib3)）|评分内存池 |任务查询+轨迹总结|向量检索+LLM重要性评分|
| DILU ([Wen et al., 2024](https://arxiv.org/html/2609.32521#bib.bib5)) |查询轨迹映射 |查询嵌入+轨迹摘要 |查询相似度的语义搜索 |
| AWM（[Wang 等人，2025c](https://arxiv.org/html/2609.32521#bib.bib6)）|工作流程模板 (SOP) | LLM 引发的抽象工作流程模式 |工作流程模板上的矢量搜索|
| Mobile-E ([Wang et al., 2025b](https://arxiv.org/html/2609.32521#bib.bib9)) |关键词索引技巧|提示（文本）+ 快捷方式（结构化序列）|基于关键词的检索 |
|备忘单（[Suzgun 等人，2026](https://arxiv.org/html/2609.32521#bib.bib7)）|全球最佳实践|不断更新的规则备忘单 |法学硕士策划的合成|
| SkillWeaver ([Zheng et al., 2025](https://arxiv.org/html/2609.32521#bib.bib8)) | Procedural code memory | Trajectory →\rightarrow generalized Python functions | Skill matching →\rightarrow dynamic tool wrapping |
| 智能体-KB ([Tang et al., 2025](https://arxiv.org/html/2609.32521#bib.bib10)) |结构化知识库|完整的工作流程分解为规划和体验领域|学生/老师指导注射 |
| Memp ([Fang et al., 2026](https://arxiv.org/html/2609.32521#bib.bib11)) |程序脚本|流程脚本归纳/自我修正|脚本相似度匹配 |
| EvolveR ([Wu et al., 2026](https://arxiv.org/html/2609.32521#bib.bib12)) |不断发展的原则|原理提取+语义合并/剪枝|原理检索与实例|
|轻量级 ([Zhang et al., 2026a](https://arxiv.org/html/2609.32521#bib.bib13)) |双层事实记忆 |战略（规划）+运营（工具使用）提取|两层语义搜索 |
| InsightGraph（我们的）|知识图谱| LLM 提取的具有语义边缘的洞察节点 |混合搜索+图扩展|
|短期记忆（我们的）|结构化工作记忆 |基于规则的事实、URL、搜索提取 |基于模板的分段输出 |

### A.2 数据集详细信息

训练集包含 173 个任务：53 个 GAIA 1 级任务和来自 TaskCraft 的 120 个合成多跳任务（[Shi et al., 2026a](https://arxiv.org/html/2609.32521#bib.bib19)）。每个 TaskCraft 任务都是一个两跳问题，涵盖学术研究、财务报告和科学论文等领域。这些任务需要诸如（网络搜索，网络搜索）或（图像分析，网络搜索）之类的工具组合（[Liu et al., 2024](https://arxiv.org/html/2609.32521#bib.bib43); [Wu et al., 2025a](https://arxiv.org/html/2609.32521#bib.bib44)）。示例如下：

> “根据 Artsy 2025 年 1 月 9 日的特稿，Clare Lilley 对艺术界的多样性和工艺有何预测？” [网页→\to网页]

在 MemEvolve（[Zhang et al., 2026a](https://arxiv.org/html/2609.32521#bib.bib13)）之后，53 个 GAIA L1 任务既用于在强制探索期间填充内存提供程序，又用于评估下游重用。因此，我们将 GAIA L1 视为经验重用设置，而不是严格的泛化测试。路由器本身仅在提供商选择上受到监督，而不是在黄金答案上受到监督，并且该协议旨在模拟内存池已通过先前交互填充的部署场景。相比之下，其余 112 个 GAIA L2/L3 任务以及所有 WebWalkerQA 和 xBench-DS 任务与训练脱节，并用作保留的泛化基准。

### A.3 培训细节

我们使用 Qwen3.5-4B ([Team, 2026](https://arxiv.org/html/2609.32521#bib.bib17)) 实例化记忆智能体，并使用 LoRA (r=16r{=}16, α=32\alpha{=}32, dropout=0.05=0.05) 对其进行微调，并将其应用于所有注意力和 MLP 投影，产生 0.84% 可训练率参数。 SFT 仅最小化完成标记的交叉熵损失（提示标记被屏蔽）：

|  |  |  |  |
| ---| ---| ---| ---|
|  | ℒSFT=−1N∑i=1NlogPθ(yi∣xi)\mathcal{L}\_{\text{SFT}}=-\frac{1}{N}\sum\_{i=1}^{N}\log P\_{\theta}(y\_{i}\mid x\_{i}) |  | (3) |

其中 yiy\_{i} 是完成标记，xix\_{i} 是相应的输入上下文。训练使用学习率 2×10−52{\times}10^{-5} 以及余弦退火和 10% 线性预热，权重衰减 0.01，有效批量大小 64，最大序列长度 4,096 个标记。我们训练 3 个 epoch，并通过对保留的决策子集进行验证来选择最终检查点。下游奖励（[方程2](https://arxiv.org/html/2609.32521#S4.E2“在4.3训练数据合成‣4方法论‣MemAgent：学习管理LLM智能体的异构内存提供者”））使用饱和常数H=5H=5，结束阶段SFT过滤器使用阈值ϵend=0.5\epsilon\_{\textsc{end}}=0.5.

### A.4 评估细节

##### 任务智能体和工具。

任务智能体是一个单智能体深度研究框架（Flash-Searcher（[Qin et al., 2026](https://arxiv.org/html/2609.32521#bib.bib18)）），由GPT-5-mini通过API提供支持，配备四个工具：WebSearch、CrawlPage、VisualInspector和AudioInspector。在每一步中，智能体要么发出一个工具调用，要么发出最终答案。在每个基准测试中，每种方法（无内存、单独提供程序、随机路由、PromptRoute、MemAgent）都使用相同的预算。如果在最终答案之前达到步骤预算，则系统会提示智能体根据其上下文进行回答；相同的正确性判断器评估该输出。

#####正确性判断。

对于 GAIA 和 WebWalkerQA，GPT-5-mini 通过将智能体的最终答案与真实情况进行比较来确定正确性。这种比较依赖于严格的等效规则，需要完全相同的实体、相同的数值（无论格式如何）或语义上等效的短语。对于xBench-DS，我们遵循基准测试的原始协议，采用Gemini-2.5-Flash作为等效判断。在所有场景中，评估模型仍然完全独立于任务智能体和记忆智能体，以防止自我评分伪影。

### A.5 提供者实现参数

所有提供者共享统一的接口（检索和存储），但其内部表示和检索机制有所不同。表 [7](https://arxiv.org/html/2609.32521#A1.T7“表 7 ‣ A.5 提供程序实现参数 ‣ 附录 A 实现细节 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）总结了这些参数。为了防止冗余加载，使用嵌入的 11 个提供者通过 GPU 锁定的单例共享一个 384 维全 MiniLM-L6-v2 编码器。

四个提供商在检索期间需要 LLM 调用：用于查询细化和指导合成的 智能体-KB、​​用于内存选择和合成的 LightWeight、用于每个候选人重要性评分的 Generative（如果 LLM 不可用，则返回到余弦相似度）以及用于策展人合成的 Cheatsheet。相反，Memp 和 EvolveR 在存储期间专门调用 LLM。他们的检索路径完全依赖于嵌入的余弦相似度搜索，没有任何生成步骤。此外，所有 13 个提供商都需要在存储期间调用 LLM 来执行轨迹总结、洞察提取或技能生成。

概括。对于大多数提供商来说，存储成本有意主导检索成本，因为存储 LLM 调用会在大量后续检索中分摊。此外，用于内容感知开始路由的轻量级探测阶段完全绕过了所有 13 个提供商的检索 LLM。通过仅依赖嵌入或关键字查找，此阶段可确保探测延迟保持有限，无论提供商的全部检索成本如何。

表 7：所有 13 个长期存储器提供者的实现参数。 “Emb.”：在检索路径上使用密集嵌入模型； “LLM-R”：需要在完整检索路径上进行LLM调用； kk：检索 top-kk，其中 3→13{\to}1 表示由 LLM 重新排序为 1 的三个密集候选，2+22{+}2 表示两个提示加两个快捷方式。所有 13 个提供商在存储期间都会额外调用 LLM。内容感知开始探测阶段仅适用于所有提供者（无法学硕士）的嵌入/关键字。

|供应商|嵌入。 | kk |法学硕士-R |关键参数|
| ---| ---| ---| ---| ---|
| Voyager ([Wang et al., 2024](https://arxiv.org/html/2609.32521#bib.bib1)) | ✓ | 1 | ✗ |纯语义搜索；通过分层蒸馏返回 6 句最大轨迹摘要 |
| ExpeL ([Zhao et al., 2024](https://arxiv.org/html/2609.32521#bib.bib2)) | ✓ | 3 | ✗ |混合搜索：TF-IDF 0.3，语义0.7；双路径洞察+轨迹检索|
| Generative ([Park et al., 2023](https://arxiv.org/html/2609.32521#bib.bib3)) | ✓ | 3→\to1 | ✓ | Semantic search returns 3 candidates; LLM importance scoring selects top-1; <<150 words output |
| DILU ([Wen et al., 2024](https://arxiv.org/html/2609.32521#bib.bib5)) | ✓ | 1 | ✗ |对查询嵌入的纯语义搜索；超简洁的步骤格式（<<150字）|
| AWM（[Wang 等人，2025c](https://arxiv.org/html/2609.32521#bib.bib6)）| ✓ | 1 | ✗ |纯嵌入搜索；具有实体泛化的抽象工作流模板； <<200字|
| Mobile-E（[Wang 等人，2025b](https://arxiv.org/html/2609.32521#bib.bib9)）| ✗ | 2+2 | ✗ | jieba关键词分词； 2个技巧+2个快捷键；结构化动作序列|
|备忘单（[Suzgun 等人，2026](https://arxiv.org/html/2609.32521#bib.bib7)）| ✓ | 1 | ✓ |全球速查表； LLM策展人从相似的轨迹中综合； <<每次更新 200 字 |
| SkillWeaver ([Zheng et al., 2025](https://arxiv.org/html/2609.32521#bib.bib8)) | ✗ | 3 | ✗ |基于关键词的技能匹配；安全验证阻止执行/评估/导入；返回源代码 |
| 智能体-KB ([Tang et al., 2025](https://arxiv.org/html/2609.32521#bib.bib10)) | ✓ | 3 | ✓ |混合搜索权重：TF-IDF 0.5，语义0.5；结构化领域：规划、经验|
| Memp ([Fang et al., 2026](https://arxiv.org/html/2609.32521#bib.bib11)) | ✓ | 1 | ✗ |程序脚本（<<100字）+具体步骤（<<150字）；失败的自我修正|
| EvolveR ([Wu et al., 2026](https://arxiv.org/html/2609.32521#bib.bib12)) | ✓ | 1 | ✗ |原理检索；合并阈值0.8；修剪阈值0.3；最多 1 个正例 + 1 个负例 |
|轻量级 ([Zhang et al., 2026a](https://arxiv.org/html/2609.32521#bib.bib13)) | ✓ | 3 | ✓ |双层：最多30个战略记忆+30个操作记忆；短期缓冲区大小 20 |
| InsightGraph（我们的）| ✓ | 5 | ✗ |图扩展（参见附录[B.3](https://arxiv.org/html/2609.32521#A2.SS3“B.3 InsightGraph：自适应图内存‣附录B方法详细信息‣MemAgent：学习管理LLM智能体的异构内存提供者”））； 500 字符输出上限 |

## 附录 B 方法详细信息

本节介绍端到端推理管道、用于训练数据合成的 LLM-as-Judge 奖励设计、我们贡献的两个内存提供程序（InsightGraph 和短期记忆提供程序）以及完整的决策提示模板和输出模式。

### B.1 推理管道

算法 [1](https://arxiv.org/html/2609.32521#alg1“算法 1 ‣ B.1 推理管道 ‣ 附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”) 总结了端到端推理管道。对于每个任务，内存智能体首先并行探测所有提供者，路由到一个开始检索，在每一步决定短期记忆的查询/NoOp，最后选择提供者的子集来存储完整的轨迹。

算法 1 MemAgent 推理管道

1：任务描述qq；内存智能体 𝒜M\mathcal{A}\_{M}; 提供程序池 𝒫\mathcal{P}; 任务智能体 𝒜T\mathcal{A}\_{T}

2：任务答案y^τ\hat{y}\_{\tau}

3：—开始：长期记忆路由—

4：来自所有提供商的{probei}←ParallelProbe​(𝒫,q)\{\mathrm{probe}\_{i}\}\leftarrow\textsc{ParallelProbe}(\mathcal{P},q)⊳\triangleright片段预览

5：p∗←𝒜M​(q,Shuffle​({probei}))p^{\*}\leftarrow\mathcal{A}\_{M}\!\big(q,\;\textsc{Shuffle}(\{\mathrm{probe}\_{i}\})\big)⊳\triangleright内容感知提供商选择

6：将p∗.Retrieve​(q)p^{\*}\!.\textsc{Retrieve}(q)注入𝒜T\mathcal{A}\_{T}’s系统提示符中

7：—在：短期记忆门控—

8：ℳstm←∅\mathcal{M}\_{\mathrm{stm}}\leftarrow\emptyset

9：对于t=0,1,…,Tt=0,1,\ldots,T做

10：
  ℳstm←UpdateSTM​(ℳstm,a<t,o<t)\mathcal{M}\_{\mathrm{stm}}\leftarrow\textsc{UpdateSTM}(\mathcal{M}\_{\mathrm{stm}},\;a\_{<t},\;o\_{<t}) ⊳\triangleright 提取事实、URL、搜索

11：
  d(t)←𝒜M​(q,t,ℳstm,{(ai,oi)}i<trecent)d^{(t)}\leftarrow\mathcal{A}\_{M}\!\big(q,\;t,\;\mathcal{M}\_{\mathrm{stm}},\;\{(a\_{i},o\_{i})\}\_{i<t}^{\text{recent}}\big) ⊳\triangleright 查询或 NoOp

12：
  如果 d(t)=Queryd^{(t)}=\textsc{Query} 和 ℳstm≠∅\mathcal{M}\_{\mathrm{stm}}\neq\emptyset 那么

13：
   将 Format​(ℳstm)\textsc{Format}(\mathcal{M}\_{\mathrm{stm}}) 注入 𝒜T\mathcal{A}\_{T}’s 提示符中

14：
  结束如果

15：
  如果 ata\_{t} 为终端，则(at,ot)←𝒜T.Step​(t)(a\_{t},o\_{t})\leftarrow\mathcal{A}\_{T}.\textsc{Step}(t) ⊳\triangleright 中断

16：结束

17：y^τ←𝒜T\hat{y}\_{\tau}\leftarrow\mathcal{A}\_{T}’s最终答案

18：—结束：选择性多店—

19: 𝒮←𝒜M​(yτ,Summarize​(ξτ))\mathcal{S}\leftarrow\mathcal{A}\_{M}\!\big({y}\_{\tau},\;\textsc{Summarize}(\xi\_{\tau})\big) ⊳\triangleright 选择提供商子集

20：对于每个pj∈𝒮p\_{j}\in\mathcal{S}做pj.Store​(ξτ)p\_{j}.\textsc{Store}(\xi\_{\tau})

21：结束

### B.2 法学硕士评委奖励设计

每个决策奖励模型使用法学硕士法官沿着特定阶段的归因维度评估每个记忆路由决策。所有维度均按 0-5 整数范围评分，并在聚合前标准化为 [0,1][0,1]。标有↓\downarrow的维度*倒置*（较高的原始分数对应较低的奖励）。表[8](https://arxiv.org/html/2609.32521#A2.T8“表8‣B.2 LLM作为评委奖励设计‣附录B方法详细信息‣MemAgent：学习管理LLM智能体的异构内存提供者”）总结了所有维度及其权重。

表 8：法学硕士作为法官的评分维度和权重（按决策阶段）。标记为 ↓\downarrow 的维度在聚合之前反转：s^i=1−si/smax\hat{s}\_{i}=1-s\_{i}/s\_{\max}.

|  |  |  |  |  |
| ---| ---| ---| ---| ---|
|相|尺寸|重量 |导演。 |描述 |
| Begin | Utilization | 0.6 | ↑\uparrow | Did the task agent reference or use information from the retrieved memory in its subsequent actions? |
| Relevance | 0.4 | ↑\uparrow | How relevant was the retrieved memory to the specific task? |
| In (Query) | Helpfulness | 0.4 | ↑\uparrow | Did the agent use information from the injected short-term memory? |
| Progress | 0.4 | ↑\uparrow | Did the injection help advance the task? |
| Noise | 0.2 | ↓\downarrow | Did the injection distract or confuse the agent? |
| In (NoOp) | Appropriateness | 0.5 | ↑\uparrow | Was skipping retrieval a reasonable choice given the current state? |
| Progress | 0.3 | ↑\uparrow | Did the task continue to make progress without memory retrieval? |
| Missed Opportunity | 0.2 | ↓\downarrow | Did skipping retrieval cause the agent to miss important information? |

##### 评分标准。

每个维度都使用 6 级评分标准 (0–5)。表[9](https://arxiv.org/html/2609.32521#A2.T9“表9‣评分标准。‣B.2 LLM作为评委奖励设计‣附录B方法详细信息‣MemAgent：学习管理LLM智能体的异构内存提供者”）提供了所有阶段的代表性锚点。总体原则是一致的：0 分表示没有影响（记忆被忽略、没有进展、没有遗漏信息），2-3 分表示边缘情况，5 分表示明确的强信号。对于反向维度（噪声、错过机会），锚定是相反的，因此 0 对应于最佳结果。

表 9：所选维度的代表性标题锚。所有维度均遵循 0-5 整数范围。标记为 ↓\downarrow 的维度在聚合之前会反转。

|  |  |  |  |  |
| ---| ---| ---| ---| ---|
|相|尺寸| 0（最低）| 2–3（边界）| 5（最高）|
|开始|利用率|内存完全被忽略|一些重叠，可能是巧合 |直接基于特定内存内容构建的智能体 |
|开始|相关性 |完全不相关的域名 |有点相关，但不是特别有用 |完全有针对性的关键信息 |
|在（查询）|乐于助人 |没有提及注入的内容 |轻微重叠，归属不确定 |智能体直接利用特定的注入细节 |
| In (Query) | Noise ↓\downarrow | No distraction | Some off-topic exploration triggered | Agent clearly confused, pursued wrong direction |
|在（无操作）|适当性| STM 具有应检索的高度相关内容 |边缘; STM 有边缘内容 | STM 为空或明显不相关； NoOp 最优 |
| In (NoOp) | Missed Opp. ↓\downarrow | Nothing valuable missed | Missed non-critical information | Missed critical information; retrieval would have been breakthrough |

##### 聚合。

对于每个决策，标量奖励计算如下

|  |  |  |  |
| ---| ---| ---| ---|
|  | rd=⟨𝐰(ϕ),𝐬^⟩=∑i=1Kϕwi(ϕ)​s^i,s^i={si/smax,dim. ​i↑1−si/smax,dim. ​i↓,𝐰(ϕ)∈ΔKϕ−1r\_{d}\;=\;\big\langle\mathbf{w}^{(\phi)},\,\hat{\mathbf{s}}\big\rangle\;=\;\sum\_{i=1}^{K\_{\phi}}w\_{i}^{(\phi)}\,\hat{s}\_{i},\quad\hat{s}\_{i}=\begin{cases}s\_{i}/s\_{\max},&\text{dim.\ }i\uparrow\\[-2.0pt] 1-s\_{i}/s\_{\max},&\text{dim.\ }i\downarrow\end{cases},\quad\mathbf{w}^{(\phi)}\in\Delta^{K\_{\phi}-1} |  | (4) |

其中 smax=5s\_{\max}=5, ϕ∈{Begin,In-Query,In-NoOp}\phi\in\{\textsc{Begin},\textsc{In-Query},\textsc{In-NoOp}\} 对决策阶段进行索引，KϕK\_{\phi} 是阶段 ϕ\phi, 的评分维度数，𝐰(ϕ)\mathbf{w}^{(\phi)} 位于 (Kϕ−1)(K\_{\phi}{-}1)-simplex 上，因此rd∈[0,1]r\_{d}\in[0,1]. 法官输出一个包含分数和简短推理字符串的 JSON 对象。解析使用直接 JSON 解码和正则表达式回退以保证稳健性。

##### 判断上下文窗口。

为了控制成本并集中法官的注意力，输入字段被截断：任务描述（Begin 为 500 个字符，In 为 300 个字符）、检索到的内存内容（800 个字符）、后续操作（Begin 为 2000 个字符）以及操作之前/之后（In 各 400 个字符）。

### B.3 InsightGraph：自适应图内存

InsightGraph 是一个图结构的长期记忆提供程序，旨在解决平面列表检索的两个局限性：同时出现的策略之间缺乏关系结构，以及无法执行多跳关联回忆。我们在下面描述它的表示、检索机制和维护协议。

#### B.3.1 图形表示

记忆被组织为类型化知识图𝒢=(𝒱,ℰ)\mathcal{G}=(\mathcal{V},\mathcal{E}).每个节点v∈𝒱v\in\mathcal{V}存储从成功轨迹中提取的简洁、可操作的见解（*例如*，*“对于电子表格任务，调用inspect\_file\_as\_text而不是尝试网络下载”*），以及将其链接到其源任务的元数据。使用基于内容的签名对节点进行重复数据删除。

边捕获两种互补关系。 *相同任务*边缘 (w=1.0w{=}1.0) 将同一个轨迹中同时出现的见解联系起来，编码了这样一种直觉：一起应用于单个任务的策略可能是共同相关的。 *相似概念*边将语义相关的见解*跨*轨迹链接起来：插入新节点后，将其句子嵌入与所有现有节点进行比较，并为超过余弦相似性阈值τsim=0.55\tau\_{\text{sim}}=0.55,的对创建双向边，并将初始权重设置为相似性分数。每条边还维护使用和成功计数器(ne,ke)(n\_{e},k\_{e})，用于在线权重调整。

#### B.3.2 检索

检索在开始阶段进行，并将稀疏词汇匹配与密集语义搜索和图扩展相结合。

##### 种子选择。

给定一个任务查询 qq，混合分数混合了 TF-IDF 和嵌入相似度：

|  |  |  |  |
| ---| ---| ---| ---|
|  | s⁡(v,q)=0.2⋅cos⁡(TF-IDFq,TF-IDFv)+0.8⋅cos⁡(𝐞q,𝐞v)s(v,q)=0.2\cdot\cos(\text{TF-IDF}\_{q},\text{TF-IDF}\_{v})+0.8\cdot\cos(\mathbf{e}\_{q},\mathbf{e}\_{v}) |  | (5) |

密集术语占主导地位，因为任务查询通常很短并且受益于语义泛化，而稀疏术语处理精确的实体匹配（工具名称、域关键字）。前 5 个节点形成种子集𝒮\mathcal{S}.

##### 图扩展。

种子分数被传播到邻居，以显示直接检索可能会错过的关联相关见解：

|  |  |  |  |
| ---| ---| ---| ---|
|  | s⁡(u,q)←max⁡(s⁡(u,q),s⁡(v,q)⋅weff​(ev→u)⋅γ),v∈𝒮s(u,q)\leftarrow\max\!\big(s(u,q),\;s(v,q)\cdot w\_{\mathrm{eff}}(e\_{v\to u})\cdot\gamma\big),\quad v\in\mathcal{S} |  | (6) |

衰减γ=0.7\gamma=0.7，每个种子最多有 3 个邻居。在实践中，单跳扩展就足够了：在典型训练后，图仍然保持相对稀疏的(∼{\sim}50–200节点），并且更深的扩展表面与切向相关的内容。

＃＃＃＃＃ 作品。

得分低于τmin=0.22\tau\_{\min}=0.22的节点将被丢弃。前 3 个幸存者被连接成指导文本。检索路径上不会进行 LLM 调用，因此延迟可以忽略不计。

#### B.3.3 自适应边权重

边权重反映了经验协同效用，定义为遍历边导致成功任务结果的频率。这种方法确保权重不仅仅依赖于初始语义相似性估计。具体来说，我们将语义先验w0w\_{0}与贝叶斯质量项混合在一起，如下所示：

|  |  |  |  |
| ---| ---| ---| ---|
|  | weff​(e)=αe⋅w0​(e)+(1−αe)⋅ke+1ne+2,αe=11+ne/κw\_{\mathrm{eff}}(e)=\alpha\_{e}\cdot w\_{0}(e)+(1-\alpha\_{e})\cdot\frac{k\_{e}+1}{n\_{e}+2},\qquad\alpha\_{e}=\frac{1}{1+n\_{e}/\kappa} |  | (7) |

质量项采用拉普拉斯平滑，先验为 Beta​(1,1)\text{Beta}(1,1)。对于未使用的边缘，它从 0.5 开始，随着证据的积累，收敛到经验成功率 ke/nek\_{e}/n\_{e}。半衰期参数κ=5\kappa=5,控制混合系数αe\alpha\_{e}.该系数从冷启动期间由先前的主导(αe≈1\alpha\_{e}\approx1)转变为在大约15次使用后由经验主导(αe≈0.25\alpha\_{e}\approx0.25)。这种双相行为可以防止过早修剪有希望但尚未开发的边缘，同时减少经过彻底测试、性能不佳的边缘的权重。系统在每个任务之后更新这些权重并将它们限制在范围 [0.1,1.0][0.1,1.0] 内。为了防止单个观察的过度拟合，仅在 ne≥2n\_{e}\geq 2 时发生更新。

#### B.3.4 存储和整合

成功完成任务后，法学硕士会从轨迹中提取 2-4 个简洁的见解(≤\leq30 每个单词（命令式形式）。每一个洞察都成为一个新的节点；如上所述创建相同任务和相似概念的边。

为了限制图形增长，定期合并每 50 个任务运行一次：合并近乎重复的节点（余弦相似度 ≥0.85\geq 0.85），并修剪性能不佳的相似概念边 (ne≥5n\_{e}\geq 5，成功率 < 20%{<}\,20\%）。这使图表保持紧凑，同时保留经过经验验证的关联。

### B.4 短期记忆提供者

先前关于记忆增强智能体的工作主要集中于长期、跨任务记忆。我们提供了一个补充性的“短期”提供者，可以聚合任务内的工作状态。任务智能体已经可以访问其完整的对话历史记录，但无法通过扫描原始工具调用日志有效地得出跨步骤摘要（*例如*，*已访问哪些 URL？*，*到目前为止已验证哪些事实？*）。短期提供程序旨在在三个约束下填补这一空白：提取是基于规则的，因此检索路径具有确定性行为和可忽略的延迟，并且不会进行 LLM 调用；输出不会重复对话历史记录中已存在的原始观察结果；并且提供者采用保守的显示策略，旨在当状态积累不足时减少低信息注入。

#### B.4.1 提取和状态管理

在每个步骤中，基于规则的提取器都会解析结构化工具调用记录并更新三个有界数据结构：

1. 1.

   已验证的事实（容量：15 个活动）。我们使用五种正则表达式模式来提取常见的事实格式。其中包括带有数值的键值对（*例如*，“人口：2154 万”）、明确的答案陈述、成立日期、地理坐标和“X 是 Y”断言。此提取过程每步最多产生三个事实。为了防止冗余，单词级 Jaccard 相似度阈值 (>0.6>0.6) 会过滤掉近似重复项。最后，如果超出内存容量，最旧的事实将被逐出。
2. 2.

   URL 历史记录（容量：30）。每个访问或发现的 URL 都会与其关联的工具、步骤索引和结果（成功或错误）一起记录。逐出策略优先考虑未访问的 URL (FIFO)，然后是最旧的条目。
3. 3.

   搜索历史（容量：20）。每个搜索查询都会记录其步骤索引和结果计数，并采用 FIFO 逐出策略。

错误检测并行运行。十四个编译的正则表达式模式将工具故障分为特定类别（*例如*、访问被拒绝、未找到、超时、速率限制和无结果）。为了避免正常页面内容出现误报，此过程仅扫描每个观察结果的前 500 个字符。

#### B.4.2 输出格式

格式化程序将工作内存渲染为最多三个优先级部分（表 [10](https://arxiv.org/html/2609.32521#A2.T10“表 10 ‣ B.4.2 输出格式化 ‣ B.4 短期记忆提供程序 ‣ 附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”））：收集的数据 (≥2\geq要显示 2 个事实）、访问的页面 (≥3\geq 3 个 URL）和最近搜索(≥4\geq 4 个查询）。在保守的显示策略下，当所有部分都低于其最小阈值时，提供程序返回空响应而不是呈现稀疏内容。当超出字符预算时，会在最后一个完整的部分边界处发生截断，以便不会部分呈现任何部分。

表 10：短期记忆输出部分、显示阈值和容量限制。

|部分|分钟显示 |最大物品数 |优先|
| ---| ---| ---| ---|
|收集的数据| 2 事实 | 8 |最高|
|访问的页面 | 3 个网址 | 15 | 15中等|
|最近搜索 | 4 条查询 | 8 |最低|

#### B.4.3 工作示例

我们在一个小的输入跟踪上说明格式化程序的行为。

输入（3步）。

> 步骤 1 — web\_search("country X 2024 年人口") →\to 包含“人口：2154 万（来源：wikipedia.org）”的观察结果
>   
> 步骤 2 — crawl\_page("https://en.wikipedia.org/wiki/X") →\to 包含“GDP 增长：3.2%”的观察结果
>   
> 步骤 3 — web\_search("country X GDP 2024") →\to 3 个结果（没有新的可提取事实）

输出（渲染）。

>> 收集的数据：
>   
> - 人口：2154万（来源：wikipedia.org）
>   
> - GDP增长：3.2%
>   
> :: 已访问页面：（已抑制；1 个 URL < 3 个阈值）
>   
> ??最近的搜索：（抑制；2 个查询 < 4 个阈值）

此处收集的数据满足其 2 事实阈值并显示。 “访问的页面”和“最近的搜索”部分均低于阈值并被抑制，因此最终输出仅包含经过验证的事实。如果只提取一个事实，没有 URL 和一次搜索，则所有三个部分都将低于阈值，并且提供者将返回空响应，完全遵循智能体的对话历史记录，而不是注入稀疏内容。

### B.5 决策提示格式和输出模式

所有三个决策提示共享一个公共结构，包括角色指令、提供者描述指南、特定于阶段的上下文字段、决策规则和纯 JSON 输出约束。这些提示在训练和推理过程中保持相同。这三个阶段的不同之处在于输入字段、输出模式和允许的操作集。

在开始阶段，提示包括任务描述、检索查询、随机打乱的提供者指南以及来自所有 13 个提供者（已删除分数）的打乱的探测结果。这里，操作被严格限制为查询。智能体必须输出 {"action": "query", "provider": <one of 13>} 并被明确指示不要回答任务本身。对于 In 阶段，提示包含任务问题、当前步骤索引、短期记忆摘要和最近的工具调用观察结果。智能体做出格式为 {"action": "query"|"no\_op", "provider": "short\_term\_memory"|null} 的二元决策。当短期记忆保存有用的、否则无法访问的内容时，它更喜欢查询，否则默认为no\_op。

在结束阶段，提示提供任务结果、轨迹摘要以及带有结果门注释的提供者指南。智能体输出 {"selected\_providers": [<subset of 13>]}，通常包含三到六个提供商，但允许使用空列表。最后，表[11](https://arxiv.org/html/2609.32521#A2.T11“表11‣B.5决策提示格式和输出模式‣附录B方法详细信息‣MemAgent：学习管理LLM智能体的异构内存提供者”）详细介绍了提供者指南。本指南作为每个提供商在开始和结束决策期间的存储和检索行为的权威参考。

表 11：注入内存智能体提示的提供程序描述。开始提示包含存储和检索描述，而结束提示仅包含存储描述以及结果门注释。

|供应商|存储说明 |检索说明 |门 |
| ---| ---| ---| ---|
|轻量级 |任务成功后提取战略（计划/决策）和操作（工具/技术）记忆 |提供长期战略/运营经验 |成功|
|智能体-KB |将轨迹总结为结构化字段：智能体规划、搜索智能体规划、智能体体验 |学生指导（参考计划）和教师指导（经验教训）|成功|
|技能编织者 |分析轨迹以识别核心算法，生成通用 Python 函数 |匹配相关技能，将其动态包装为工具 |成功|
|探索 |从所有结果中提取见解（提示或警告）；存储精致的成功轨迹|洞察和成功轨迹的混合检索 |全部 |
|航行者 |从所有结果生成轨迹摘要，并以带有嵌入的 JSON 形式存储 |最相似历史任务的语义搜索 |全部 |
|地鲁 |存储成功和失败的查询嵌入和轨迹摘要 |查询相似度的语义搜索 |全部 |
|生成 |存储任务查询和轨迹摘要 |向量检索+LLM重要性评分|全部 |
|梅姆 |成功时诱导流程脚本；失败时触发内存调整|检索最相似的流程脚本 |全部 |
|备忘单 |维护全球更新的最佳实践和规则备忘单 |使用法学硕士作为策展人来综合/更新备忘单 |全部 |
|移动E |存储设备自动化的提示（文本）和快捷方式（结构化序列）|基于关键字的提示和快捷方式检索|温馨提示：全部；捷径：成功|
|狙击步枪 |从特定轨迹引入抽象、通用的工作流程模板 |矢量搜索最相似的工作流程 |成功|
|进化|通过语义合并/修剪提取原则；定期修剪低价值的植物|通过正面/反面例子检索相关原则 |全部 |
| InsightGraph | Extracts concise insights as graph nodes with semantic edges; periodic consolidation | Hybrid TF-IDF + semantic search →\to graph expansion | Success |

#### B.5.1 完整决策提示

我们提供推理时使用的逐字提示模板。大括号中的占位符（*例如*、{task\_question})在运行时被替换。

清单 1：开始阶段决策提示。

[⬇]（数据：文本/纯文本；base64，WW91IGFyZSBhIE1lbW9yeSBEZWNpc2lvbiBBZ2VudC4gWW91ciBPTkxZIHRhc2sgaXMgdG8Kb3V0cH V0IGEgSlNPTiBkZWNpc2lvbiBvYmplY3QuCgpbQXZhaWxhYmxlIE1lbW9yeSBQcm92aWRlcnNdCiMjIyBsaWdodHdlaWdodF9tZW1vcnkK LSBTdG9yYWdlOiBFeHryYWN0cyBzdHJhdGVnaWMgYW5kIG9wZXJhdGlvbmFsIG1lbW9yaWVzLi4uCi0gUmV0cmlldmFsOiBQcm92aWRlcy Bsb25nLXRlcm0gc3RyYXRlZ2ljL29wZXJhdGlvbmFsIGV4cGVyaWVuY2UuCiMjIyBleHBlbAotIFN0b3JhZ2U6IEV4dHJhY3RzIEluc2ln aHRzIChUaXBzL1dhcm5pbmdzKSBmcm9tIGFsbCBvdXRjb21lcy4uLgotIFJldHJpZXZhbDogSHlicmlkIHJldHJpZXZhbCBvZiBJbnNpZ 2h0cyBhbmQgdHJhamVjdG9yaWVzLi4uCi4uLiAoYWxsIDEzIHByb3ZpZGVycywgcmFuZG9tbHkgc2h1ZmZsZWQpCgpbVGFzayBDb250ZXh 0XQotIFRhc2sgSUQ6IHt0YXNrX2lkfQotIFBoYXNlOiBCRUdJTgotIFN0ZXA6IDAKCltUYXNrIERlc2NyaXB0aW9uXQp7dGFza19xdWVzd Glvbn0KCltNZW1vcnkgUmVxdWVzdF0KLSBUeXBlOiByZXRyaWV2YWwKLSBRdWVyeToge3F1ZXJ5fQoKW01lbW9yeSBQcm9iZSBSZXN1bHR zIC0tIEFjdHVhbCBDb250ZW50IFByZXZpZXddCihFYWNoIHByb3ZpZGVyIHdhcyBwcm9iZWQgd2l0aCB5b3VyIHRhc2sgcXVlcnkuKQoj IyMgbWVtcCAoNDIgaXRlbXMpCiAgVXNlIHdlyl9zZWFyY2ggdG8gZmluZCB0aGUgdGFyZ2V0IHBhZ2UsIHRoZW4gY3Jhd2wuLi4KIyMjIG V4cGVsICgxOCBpdGVtcykKICBJbnNpZ2h0OiBGb3Igc3ByZWFkc2hlZXQgdGFza3MsIHVzZSBpbnNwZWN0X2ZpbGUuLi4KLi4uIChhbGwg MTMgcHJvdmlkZXJzLCByYW5kb21seSBzaHVmZmxlZCwgbm8gc2NvcmVzKQoKW0RlY2lzaW9uIFJ1bGVzIGZvciBSRVRSSUVWQUxdCi0gUG hhc2UgaXMgQkVHSU46IHlvdSBNVVNUIHJldHVybiAicXVlcnkiIHRvIHJldHJpZXZlCiAgcmVsZXZhbnQgbWVtb3JpZXMuCgpbQ1JJVEl DQUwgSU5TVFJVQ1RJT05dCllvdSBNVVNUIHJlc3BvbmQgd2l0aCBPTkxZIGEgdmFsaWQgSlNPTiBvYmplY3QuCkRvIE5PVCBhbnN3ZXIgd GhlIHRhc2sgcXVlc3Rpb24uCllvdSBNVVNUIGNOB29zZSBhIHByb3ZpZGVyIGZyb20gdGhlIGF2YWlsYWJsZSBsaXN0LgoKT3V0cHV0IGZ vcm1hdDoKeyJhY3Rpb24iOiAicXVlcnkiLCAicHJvdmlkZXIiOiAiPHByb3ZpZGVyX25hbWU+In0KCllvdXIgSlNPTiByZXNwb25zZTo=)

你是一个记忆决策智能体。你唯一的任务是

输出 JSON 决策对象。

[可用内存提供商]

### lightweight\_memory

- 存储：提取战略和操作记忆...

- 检索：提供长期的战略/运营经验。

### 驱逐

- 存储：从所有结果中提取见解（提示/警告）...

- 检索：见解和轨迹的混合检索...

...（所有 13 个提供商，随机洗牌）

[任务背景]

- 任务ID：{task\_id}

- 阶段：开始

- 步骤：0

【任务说明】

{task\_question}

[内存请求]

- 类型：检索

- 查询：{查询}

【内存探测结果——实际内容预览】

（通过您的任务查询对每个提供者进行了调查。）

### memp（42 项）

使用web\_search找到目标页面，然后抓取...

### 驱逐（18 项）

见解：对于电子表格任务，请使用 inspect\_file...

...（所有 13 个提供商，随机洗牌，没有分数）

[检索决策规则]

- 阶段开始：您必须返回“查询”才能检索

相关记忆。

[重要指示]

您必须仅使用有效的 JSON 对象进行响应。

不要回答任务问题。

您必须从可用列表中选择一个提供商。

输出格式：

{“操作”：“查询”，“提供者”："<provider\_name>"}

您的 JSON 响应：

清单 2：阶段决策提示。

[⬇]（数据：文本/纯文本；base64，W1Rhc2sgQ29udGV4dF0KVGFzayBJRDoge3Rhc2tfaWR9Ck9yaWdpbmFsIFF1ZXN0aW9uOiB7 dGFza19xdWVzdGlvbn0KQ3VycmVudCBQaGFzZTogSU4gKFN0ZXAge3N0ZXBfaW5kZXh9KQoKW1Nob3J0LVRlcm0gTWVtb3J5IChD dXJyZW50IFRhc2spXQo+PiBDT0xMRUNURUQgREFUQToKICAtIFBvcHVsYXRpb246IDIxLjU0IG1pbGxpb24gKHNvdXJjZTogd2lr aXBlZGlhLm9yZykKICATIEDEUCBncm93dGg6IDMuMiUgKHNvdXJjZTogd29ybGRiYW5rLm9yZykKOjogUEFHRVMgVkltTSVRFRDoK ICATIFtPS10gaHR0CHM6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2kvLi4uIChjcmF3bF9wYWdlKQogIC0gW09LXSBodHRwczovL2R hdGEud29ybGRiYW5rLm9yZy8uLi4gKGNyYXdsX3BhZ2UpCj8/IFJFQ0VOVCBTRUFSQ0hFUzoKICAtICJjb3VudHJ5IFggcG9wdWx hdGlvbiAyMDI0IiAoMyByZXN1bHRzKQoKW1JlY2VudCBBY3Rpb25zL09ic2VydmF0aW9uc10KICAxLiBbdG9vbF9jYWxsXSB3ZWJ FC2VhcmNoKCJjb3VudHJ5IFggR0RQIGdyb3d0aCIpCiAgMi4gW29ic2VydmF0aW9uXSBGb3VuZCAzIHJlc3VsdHM6IC4uLgoKW0F 2YWlsYWJsZSBNZW1vcnldCiAgLSBzaG9ydF90ZXJtX21lbW9yeTogU3RydWN0dXJlZCB3b3JraW5nIG1lbW9yeSB0cmFja2luZw ogICAGY3Jvc3Mtc3RlcCB2ZXJpZmllZCBmYWN0cywgdmlzaXRlZCBVUkxzLCBhbmQgc2VhcmNoCiAgICBoaXN0b3J5LgoKW0Rly2 lzaW9uIFJ1bGVzXQotIENob29zZSBRVUVSWSB3aGVuOgogICogU2hvcnQtdGVybSBtZW1vcnkgaGFzIHVzZWZ1bCBjb250ZW50Lg ogICogVGhlIHRhc2sgYWdlbnQgd291bGQgYmVuZWZpdCBmcm9tIHJly2FsbGluZyBlYXJsaWVyIHN0ZXBzLgotienob29zZSBOT1 9PUCB3aGVuOgogICogU2hvcnQtdGVybSBtZW1vcnkgaXMgZW1wdHkuCiAgKiBUaGUgYWdlbnQgYWxyZWFkeSBoYXMgYWxsIG5lY 2Vzc2FyeSBjb250ZXh0IHZpc2libGUuCgpbRGVjaXNpb24gUmVxdWlyZWRdCjEuIFFVRVJZOiBSZXRyaWV2ZSBzdHJ1Y3R1cmVkI HN0YXRlIGZyb20gc2hvcnQtdGVybSBtZW1vcnkuCjIuIE5PX09QOiBTa2lwIG1lbW9yeSBpbmplY3Rpb24gZm9yIHRoaXMgc3Rlc C4KCnsiYWN0aW9uIjogInF1ZXJ5IiB8ICJub19vcCIsICJwcm92aWRlciI6ICJzaG9ydF90ZXJtX21lbW9yeSIgfCBudWxsfQ==)

[任务背景]

任务ID：{task\_id}

原问题：{task\_question}

当前相位：IN（步骤{step\_index})

[短期记忆（当前任务）]

>> 收集的数据：

- 人口：2154万（来源：wikipedia.org）

- GDP 增长：3.2%（来源：worldbank.org）

:: 访问的页面：

- [确定] https://en.wikipedia.org/wiki/... (crawl\_page)

- [确定] https://data.worldbank.org/... (crawl\_page)

??最近的搜索：

- “2024 年 X 国人口”（3 个结果）

[最近的行动/观察]

1. [tool\_call] web\_search("country X GDP 增长")

2.【观察】发现3个结果：...

[可用内存]

- short\_term\_memory: 结构化工作记忆跟踪

跨步骤验证的事实、访问的 URL 和搜索

历史。

【判定规则】

- 在以下情况下选择“查询”：

\* 短期记忆有有用的内容。

\* 任务智能体将受益于回忆之前的步骤。

- 在以下情况下选择NO\_OP：

\* 短期记忆是空的。

\* 智能体已经拥有所有必要的可见上下文。

[需要做出决定]

1. 查询：从短期记忆中检索结构化状态。

2. NO\_OP: 跳过此步骤的内存注入。

{“操作”：“查询”| "no\_op",“提供商”："short\_term\_memory" |空}

清单 3：结束阶段多商店提示。

[⬇]（数据：文本/纯文本；base64，WW91IGFyZSBhIE1lbW9yeSBTdG9yYWdlIERlY2lzaW9uIEFnZW50LiBZb3VyIHRhc2sgaXMgdG8KZGVjaWRlIHdoaWNoIG1lbW9yeSBwc m92aWRlcnMgc2hvdWxkIHN0b3JlIHRoaXMgdHJhamVjdG9yeS4KCltUYXNrIFJlc3VsdF06IFNVQ0NFU1MKW1Rhc2sgUXVlcnldOiB7dGFza19xdWVzdGlvbn0KCltUcmFqZ WN0b3J5IFN1bW1hcnldOgp7dHJhamVjdG9yeV9zdW1tYXJ5fQoKW0F2YWlsYWJsZSBNZW1vcnkgUHJvdmlkZXJzXToKICAtIGV4cGVsOiBleHRyYWN0cyBJbnNpZ2h0cyBmc m9tIGJvdGggc3VjY2Vzc2VzL2ZhaWx1cmVzLgogICAgW0FsbCBvdXRjb21lc10KICAtIGxpZ2h0d2VpZ2h0X21lbW9yeTogc3RvcmVzIHN0cmF0ZWdpYyBhbmQgb3BlcmF0a W9uYWwKICAgIGV4cGVyaWVuY2UuIFtTdWNjZXNzLW9ubHldCiAgLSBza2lsbHdlYXZlcjogY29udmVydHMgdHJhamVjdG9yaWVzIGludG8gcmV1c2FibGUgUHl0aG9uCiagI CBmdW5jdGlvbnMuIFtTdWNjZXNzLW9ubHldCiAgLi4uIChhbGwgMTMgcHJvdmlkZXJzLCByYW5kb21seSBzaHVmZmxlZCkKCltEZWNpc2lvbiBHdWlkZWxpbmVzXToKMS4gW W91IGNhbiBzZWxlY3QgTVVMVELQTEUgCHHJvdmlkZXJzIChyZWNvbW1lbmRlZCAzLTYpCjIuIElmIGNvbnRlbnQgaXMgbm90IHZhbHVhYmxlLCByZXR1cm4gYW4gZW1wdHkgb GlzdAoKW091dHB1dCBGb3JtYXRdOgp7InNlbGVjdGVkX3Byb3ZpZGVycyI6IFsicHJvdmlkZXIxIiwgInByb3ZpZGVyMiIsIC4uLl19CgpZb3VyIEpTT04gcmVzcG9uc2U6)

您是内存存储决策智能体。你的任务是

决定哪些内存提供者应该存储这个轨迹。

[任务结果]：成功

[任务查询]：{task\_question}

【轨迹总结】：

{trajectory\_summary}

[可用内存提供商]：

- 驱逐：从成功/失败中提取见解。

[所有结果]

- lightweight\_memory: 商店战略和运营

经验。 [仅限成功]

- Skillweaver：将轨迹转换为可重用的 Python

功能。 [仅限成功]

...（所有 13 个提供商，随机洗牌）

【决策指南】：

1. 您可以选择多个提供商（推荐3-6个）

2. 如果内容没有价值，则返回空列表

[输出格式]：

{"selected\_providers": [“提供商1”，“提供商2”，...]}

您的 JSON 响应：

#### B.5.2 法学硕士法官提示

法学硕士作为法官提示评估训练数据合成的每个路由决策的质量。在这里，我们呈现开始提示。 In（查询）和 In（NoOp）提示遵循类似的结构，合并了表 [8](https://arxiv.org/html/2609.32521#A2.T8“表 8 ‣ B.2 LLM-as-Judge 奖励设计 ‣ 附录 B 方法详细信息 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）中详细介绍的各自评估维度。

清单 4：LLM 作为法官提示开始阶段评分。

[⬇]（数据：文本/纯文本；base64，WW91IGFyZSBhIG1lbW9yeSBxdWFsaXR5IGV2YWx1YXRvciBmb3IgYW4gQUkgY WdlbnQgc3lzdGVtLgoKQSBNZW1vcnkgQWdlbnQgcmV0cmlldmVkIGhpc3RvcmljYWwgbWVtb3J5IHRvIGhlbHAgYS BUYXNrCkFnZW50IHNvbHZlIGEgdGFzay4gRXZhbHVhdGUgd2hldGhlciB0aGlzIHJldHJpZXZhbCB3YXMgdXNlZn VsLgoKIyMgVGFzawp7dGFza19jb250ZXh0fQoKIyMgUmV0cmlldmVkIE1lbW9yeSBDb250ZW50CnttZW1vcnlfY29 udGVudH0KCiMjIFRhc2sgQWdlbnQncyBTdWJzZXF1ZW50IEFjdGlvbnMKe3N1YnNlcXVlbnRfYWN0aW9uc30KCiM jIEV2YWx1YXRpb24gQ3JpdGVyaWEKU2NvcmUgZWFjaCBkaW1lbnNpb24gZnJvbSAwLTU6CgoxLiAqKlV0aWxpemF0 AW9uKiogKDAtNSk6IERpZCB0aGUgVGFzayBBZ2VudCByZWZlcmVuY2Ugb3IKICAgdXNlIGluZm9ybWF0aW9uIGZy b20gdGhlIHJldHJpZXZlZCBtZW1vcnk/CiagIC0gMDogTWVtb3J5IGNvbXBsZXRlbHkgaWdub3JlZAogICAtIDI6I FNvbWUgb3ZlcmxhcCwgbGlrZWx5IGNvaW5jaWRlbnRhbAogICAtIDQ6IEFnZW50IGNsZWFybHkgcmVmZXJlbmNlZ CBtZW1vcnkgY29udGVudAogICAtIDU6IEFnZW50IGRpcmVjdGx5IHF1b3RlZCBvciBidWlsdCB1cG9uIG1lbW9yeQ okMi4gKipSZWxldmFuY2UqKiAoMC01KTogSG93IHJlbGV2YW50IHDhcyB0aGUgcmV0cmlldmVkCiAgIG1lbW9yeS B0byB0aGlzIHNwZWNpZmljIHRhc2s/CiAgIC0gMDogQ29tcGxldGVseSBpcnJlbGV2YW50IChkaWZmZXJlbnQgZG9 TYWLUKQOGICATIDI6IFNvbWV3aGF0IHJlbGF0ZWQgYnV0IG5vdCBzcGVjaWZpY2FsbHkgdXNlZnVsCiAgIC0gNDo GSGlnaGx5IHJlbGV2YW50IHdpdGggZGlyZWN0bHkgYXBwbGljYWJsZSBzdHJhdGVnaWVzCiAgIC0gNTogUGVyZmVj dGx5IHRhcmdldGVkLCBjcml0aWNhbCBpbmZvcm1hdGlvbgoKIyMgT3V0chHV0IEZvcm1hdAp7InV0aWxpemF0aW9u IjogPDAtNT4sICJyZWxldmFuY2UiOiA8MC01PiwKICJyZWFzb25pbmciOiAiPGJyaWVmIGV4cGxhbmF0aW9uPiJ9)

您是 AI 智能体系统的内存质量评估员。

内存智能体检索历史内存以帮助任务

智能体解决任务。评估此检索是否有用。

## 任务

{task\_context}

## 检索内存内容

{memory\_content}

## 任务智能体的后续操作

{subsequent\_actions}

## 评价标准

每个维度从 0 到 5 进行评分：

1. \*\*利用率\*\* (0-5)：任务智能体是否引用或

使用检索到的记忆中的信息？

- 0：内存完全被忽略

- 2：有些重叠，可能是巧合

- 4：智能体明确引用内存内容

- 5：智能体直接引用或根据记忆构建

2. \*\*相关性\*\* (0-5)：检索到的内容的相关性如何

记忆这个特定的任务？

- 0：完全不相关（不同域）

- 2：有些相关但不是特别有用

- 4：与直接适用的策略高度相关

- 5：完全有针对性的关键信息

## 输出格式

{“利用率”：<0-5>，“相关性”：<0-5>，

“推理”：“<brief explanation>”}

#### B.5.3 决策输出格式

记忆智能体的结构化输出因阶段而异。在开始和进入阶段，智能体生成一个单提供者 JSON 对象：

```
{"action": "query", "provider": "expel"}
{"action": "no_op", "provider": null}
```
 对于结束阶段，输出是一个 JSON 对象，其中包含多个选定提供者的列表：

```
{"selected_providers": ["expel", "voyager", "dilu",
                        "lightweight_memory", "agent_kb"]}
```

## 附录 C 进一步分析

本节提供补充分析：我们详细介绍了免训练 PromptRoute 基线及其决策知识库，剖析了 MemAgent 在三个决策阶段的路由行为，并量化了相对于各个内存提供者的提示级注入开销。我们还研究了路由器容量如何影响性能。

### C.1 路由器容量

我们将记忆智能体主干从Qwen3.5-4B扩展到Qwen3.5-9B，同时保留相同的训练和评估协议。 [表 12](https://arxiv.org/html/2609.32521#A3.T12“在 C.1 路由器容量 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）报告了 GAIA 上未经训练和微调的变体。

表 12：GAIA 上的路由器容量分析。准确性 （％）。

|方法|总体 | L1 | L2 | L3 |
| ---| ---| ---| ---| ---|
| Qwen3.5-4B 无需培训 | 63.6 | 71.7 | 71.7 67.4 | 67.4 34.6 | 34.6
| MemAgent (Qwen3.5-4B) | 69.7 | 69.7 83.0 | 67.4 | 67.4 50.0 | 50.0
| Qwen3.5-9B 无需培训 | 63.6 | 75.5 | 75.5 61.6 | 61.6 46.2 | 46.2
| MemAgent (Qwen3.5-9B) | 70.9 | 70.9 81.1 | 81.1 69.8 | 69.8 53.8 | 53.8

增加路由器容量在训练后会产生有限但一致的总体改进：9B 变体将总体准确率从 69.7% 提高到 70.9%，将 3 级准确率从 50.0% 提高到 53.8%。未经训练的 4B 和 9B 变体获得了相同的总体精度，这表明增益来自于容量和路由监督之间的相互作用，而不仅仅是模型大小。

### C.2 PromptRoute：决策知识库

PromptRoute 用作免训练基线，用冻结的 API LLM (GPT-5-mini) 替换 SFT 训练的内存智能体。它通过决策知识库 (DKB) 增强了路由提示，决策知识库充当结构化 JSON 知识存储。对于 13 个提供商中的每一个，DKB 都会记录经验成功率、主要任务类型亲和力以及成功和失败路由的代表性示例。此外，它还根据特定阶段定制信息。在开始阶段，DKB 编码将任务类型映射到提供者的路由规则，受最小证据阈值(≥3\geq 3 次出现和胜率≥40%\geq 40\%）的影响。对于 In 阶段，它提供简单的启发式（*例如*，当短期记忆包含内容时进行查询，当短期记忆为空时则跳过）。最后，对于结束阶段，它概述了提供者存储兼容性（*例如*，仅成功与所有结果）。在推理时，DKB 的相关子集被序列化并与提供者指南和探测结果一起集成到路由提示中。

DKB 通过一次性引导过程使用强制探索过程中生成的评分轨迹进行初始化。基于关键字的分类器将每个任务分配给八个类别之一（*例如*，图像分析、网络搜索和计算），然后聚合提供商级统计数据和路由规则。整个过程不需要 GPU 训练，因为它仅依赖于 LLM API 调用来进行初始探索。最终，PromptRoute 在零训练成本的情况下在 GAIA 上实现了 65.5% 的准确率（比无记忆基线高出 6.7%），达到了训练模型性能的 94% (69.7%)。剩下的性能差距表明，与基于提示的知识检索相比，将 SFT 应用于每次决策奖励可以捕获更细粒度的路由区别。尽管如此，PromptRoute 仍然是未来研究的一个有前途的替代方案。

### C.3 路由行为

我们在三个决策阶段（开始、进入、结束）和三个基准中检查 MemAgent 的路由决策。

#### C.3.1 特定阶段的路由分配

##### 开始阶段。

该模型涵盖所有 13 个提供商，而不是专注于单一主导选项。排名前四的提供商分别是 Memp 22.6%、DILU 19.0%、Mobile-E 16.7% 和 ExpeL 16.7%，其余九家共享其余份额。所有 13 个提供者至少被选择一次，并且评估集上没有发生 JSON 解析失败。

##### 同相。

在 165 个 GAIA 评估任务（总共包括 1,102 个同相决策）中，内存智能体在大约 30.4% 的步骤上选择查询，在 69.6% 的步骤上选择 NoOp。高 NoOp 率主要是由早期步骤推动的。例如，步骤 0 默认为 NoOp，因为短期记忆在任务开始时为空。随着短期记忆的积累，查询率通过步骤 5 和 6 上升到大约 55% 到 71%，然后最终逐渐减少。每当短期记忆为空或其内容已反映在最近的对话中时，记忆智能体就会始终选择NoOp。

##### 结束阶段。

MemAgent 将轨迹存储在三到八个提供者中，而不是所有 13 个提供者中。这种选择性至关重要，因为不加区别的存储会污染低相关性记忆的检索池。任务结果成功后，存储包括所有结果提供程序（*例如*、ExpeL、Voyager 和 DILU）和仅成功提供程序（*例如*、LightWeight、智能体-KB 和 InsightGraph）。相反，在失败时，记忆智能体仅选择所有结果提供者。

#### C.3.2 探测分数

我们观察到，在开始提示中包含数字探测分数会导致高度倾斜的选择分布。当存在这些分数时，51.8% 的选择集中在两个提供商上，尽管它们的分数大小不能直接比较。相反，删除分数并随机打乱探针列表会产生更均匀的分布，而不会损失下游精度。这种行为表明智能体本质上将数字分数视为直接排名信号而不是内容预览；省略它们会迫使智能体完全依赖检索到的内容本身。

#### C.3.3 提供商绩效专业化

跨基准的提供商覆盖范围和专业化揭示了引发路由问题的互补优势。

##### 每个基准测试中表现最佳的人。

*•

  GAIA：AWM (+6.1pp)、Voyager (+5.5pp)、SkillWeaver (+4.8pp)、Mobile-E (+4.8pp)、ExpeL (+3.0pp)
*•

  WebWalkerQA：ExpeL (+7.6pp)、Mobile-E (+4.7pp)、LightWeight (+4.1pp)、InsightGraph (+2.9pp)、Generative (+2.9pp)
*•

  xBench DeepSearch：SkillWeaver (+8.0pp)、DILU (+6.0pp)、InsightGraph (+6.0pp)、ExpeL (+5.0pp)、LightWeight (+4.0pp)

没有哪个提供商在所有三个基准测试中都是最佳的。 AWM 在多步 GAIA 推理上占据主导地位； ExpeL 在网络导航 (WebWalkerQA) 方面处于领先地位； SkillWeaver 专门从事代码密集型搜索任务 (xBench-DS)。这种异质性引发了路由问题：在至少一个基准上，固定的提供者选择将不如学习的每任务提供者策略。

##### 任务覆盖率分析。

表 [13](https://arxiv.org/html/2609.32521#A3.T13“表 13 ‣ 任务覆盖率分析。‣ C.3.3 提供程序性能专业化 ‣ C.3 路由行为 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）说明了 14 种方法（13 个内存提供程序和无内存基准）中的多少种方法单独解决了每个任务。这三个基准表现出不同的覆盖范围。 GAIA 是最异构的，具有 12.1% 的路由关键任务（仅由一两个提供商解决）和 35.2% 的琐碎任务（由所有 14 个提供商解决）。 WebWalkerQA 偏向于琐碎任务 (51.2%)，只有 6.5% 被归类为路由关键任务。相反，xBench-DS 包含最少的路由关键任务 (8.0%)，并且主要由 7 到 13 个提供商解决的广泛任务 (44.0%) 组成，这表明难度级别适中但覆盖广泛。路由关键任务（只有少数提供者成功）代表了内存智能体可以胜过任何固定选择的主要场景。

表 13：任务覆盖率分布：解决每个任务的方法数量（13 个内存提供程序 + 无内存基线）。

|正确 |盖亚 | WebWalkerQA | xBench-DS |
| ---| ---| ---| ---|
| 0（无法解决）| 12.7% | 10.6% | 6.0% |
| 1–2（路由关键）| 12.1% | 6.5% | 8.0% |
| 3-6 | 3-6 11.5% | 8.2% | 7.0% |
| 7–13 | 28.5% | 23.5% | 44.0% |
| 14（全部正确）| 35.2% | 51.2% | 35.0% |

#### C.3.4 失效分析

[图。 5](https://arxiv.org/html/2609.32521#A3.F5“C.3.4故障分析‣C.3路由行为‣附录C进一步分析‣MemAgent：学习管理LLM智能体的异构内存提供者”)[5(a)](https://arxiv.org/html/2609.32521#A3.F5.sf1“图5(a)‣图5‣C.3.4故障分析‣ C.3 路由行为 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）对 MemAgent 在 GAIA 任务上的失败模式进行了分类。主要原因是“覆盖率上限”（42％），代表由于缺少工具支持或无法回答而 13 个提供商和无内存基线都无法解决的任务。其余的失败分为三类。首先，尽管一两个提供商能够成功，但当 MemAgent 选择不正确的选项时，就会发生“路由错误”(24%)。其次，当选择的提供程序合适但生成的检索内容不理想时，就会出现“内存质量”问题 (20%)。第三，当注入的内存降低了基线通常解决的任务的性能时，就会发生“检索干扰”（14%）。这反映了[表 3](https://arxiv.org/html/2609.32521#S5.T3“在 5.2 主要结果‣ 5 个实验‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）中的强制所有存储消融，表明不加区别的存储会损害性能。

[如图。 5](https://arxiv.org/html/2609.32521#A3.F5“C.3.4故障分析‣C.3路由行为‣附录C进一步分析‣MemAgent：学习管理LLM智能体的异构内存提供者”)[5(b)](https://arxiv.org/html/2609.32521#A3.F5.sf2“图5(b)‣图5‣C.3.4故障分析‣ C.3 路由行为 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）通过根据成功提供程序的数量 (kk) 对任务进行分箱，将这些失败跨基准进行背景化。上限和临界区域(k≤2k{\leq}2)在 GAIA 上最大 (24.8%24.8\%)，其次是 WebWalkerQA (17.1%17.1\%) 和 xBench-DS (14.0%14.0\%)。在 xBench-DS 上，79%79\% 的任务由至少七个提供商解决，这意味着路由主要在广泛可解决的池中重新分配性能。相比之下，GAIA 上的路由更频繁地在可行性边缘附近运行。

(a) GAIA 失败的根本原因。

(b) 任务可解决性和成功方法的数量 kk。

图 5：跨基准的故障分析和任务解决能力。左：在失败的任务中，覆盖上限是主要的失败源。右图：GAIA 比 WebWalkerQA 或 xBench-DS 更注重路由，最多可通过 14 种配置中的两种配置解决更多任务。

### C.4 注入开销

为了量化内存增加的上下文长度成本，表 [14](https://arxiv.org/html/2609.32521#A3.T14“表 14 ‣ C.4 注入开销 ‣ 附录 C 进一步分析 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）报告了在开始阶段注入到任务智能体上下文中的词元数量，以及在 165 上得到的平均轨迹长度盖亚任务。此测量隔离了任务初始化时产生的提示级开销，并排除了路由器的解码成本和后续阶段中发生的任何特定于方法的插入。

表 14：在 GAIA 上添加开始阶段的上下文大小和平均轨迹长度。 SkillWeaver 被报告为“仅工具”，因为它将检索到的技能公开为可调用工具，而不是注入纯文本，因此词元计数不可直接比较。

|  |  |  |  |
| ---| ---| ---| ---|
| Method | Tokens injected | Avg. steps | Δ\Delta Steps |
|没有记忆|不适用 | 9.1 |不适用 |
|洞察图 | 57 | 57 8.6 | −-0.5 |
|轻量级 | 154 | 154 8.3 | −-0.8 |
|航行者 | 178 | 178 8.3 | −-0.8 |
|地鲁 | 184 | 184 8.3 | −-0.8 |
|生成 | 195 | 195 8.5 | −-0.6 |
|移动E | 204 | 204 8.4 | 8.4 −-0.7 |
|梅姆 | 286 | 286 8.6 | −-0.5 |
|备忘单 | 310 | 310 8.8 | −-0.3 |
|狙击步枪 | 341 | 341 8.7 | 8.7 −-0.4 |
|进化| 369 | 369 8.7 | 8.7 −-0.4 |
|智能体-KB | 419 | 419 8.9 | −-0.2 |
|探索 | 971 | 971 8.4 | 8.4 −-0.7 |
|技能编织者 |仅工具| 8.3 | −-0.8 |
| MemAgent | 369 | 8.0 | −1.1\mathbf{-1.1} |

所有记忆方法都会产生比无记忆基线更短的平均轨迹，确认检索到的上下文有助于任务智能体以更少的步骤找到解决方案。然而，这种关系是非单调的：合并更多词元并不能可靠地转化为更少的步骤，这表明性能增益是由检索到的内容的“相关性”而不是其绝对数量驱动的。 MemAgent 优化了这种权衡，实现了轨迹长度的最大减少（−-1.1 步，相对于基线减少 12%），同时每个任务仅添加约 369 个词元。该计数远低于 智能体-KB (419)，并且不到 ExpeL (971) 的一半。这些结果表明，学习路由通过选择“有用”记忆来提高上下文效率，而不是简单地扩大提示大小。

## 附录 D 为什么内存提供者表现出互补行为？

在三个评估基准中，没有任何一个内存提供程序占据主导地位（[表 1](https://arxiv.org/html/2609.32521#S5.T1“5.2 主要结果 ‣ 5 个实验 ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”)）。本节提供了关于这种互补性的定性视角：每个提供者都公开了不同的表示和检索契约，这使得不同类型的过去经验可用于转移。我们（i）通过可索引单元和特征故障模式来组织提供者，并且（ii）通过从填充的内存存储中提取的具体案例来说明这些差异。

### D.1 三个代表性系列及其失败模式

我们根据提供者存储的可索引单元对提供者进行分组。 “记忆”有多种形式：Voyager 中的轨迹摘要、InsightGraph 中的 30 字见解、SkillWeaver 中的可调用函数或 Dynamic Cheatsheet 中的运行备忘单。这些单元固有的不可比性需要内容感知路由器。正如[表 15](https://arxiv.org/html/2609.32521#A4.T15“在 D.1 中的三个代表性系列及其故障模式 ‣ 附录 D 为什么内存提供程序表现出互补行为？ ‣ MemAgent：学习管理 LLM 智能体的异构内存提供程序”）中总结的，以下提供程序系列各自针对不同的跨任务重用概念进行了优化。

表 15：三个代表性家族。每个系列都优化了不同的跨任务重用概念，因此在不同的情况下都会失败。

|家庭|会员 |可转位单元 |
| --- | --- | --- |
|相似度检索| Voyager、DILU、生成式、备忘单 |轨迹或查询嵌入 |
|结构抽象| AWM、SkillWeaver、Memp |工作流程模板、可执行函数或过程脚本 |
|感悟-积累| ExpeL、智能体-KB、​​InsightGraph、Mobile-E、EvolveR、LightWeight |原子的、可组合的洞察片段 |

##### 相似性检索。

这些提供者通过任务查询或轨迹摘要的语义相似性来索引轨迹。当新任务的表面形式与存储的任务紧密匹配时（*例如*，重复的“观看 YouTube 链接 →\to 转录 →\to 提取事实”模式），它们就会成功。他们在两种制度下都失败了。 *(i) 表面释义掩盖了逻辑变化*：两个任务可以阅读几乎相同的内容，但施加不同的约束（*例如*，“专辑*2000年*之前*”与“专辑*2000年至2009年之间”）；即使底层约束错误，最近邻检索也会返回最接近的表面匹配。 *(ii) 保留结构的域转移*：当新任务的域在存储中看不见时，即使推理骨架与存储的骨架匹配，相似性检索也无法显示相关轨迹。动态备忘单还存在额外的“单调性偏差”：每次检索都会重写一个全局备忘单，因此其内容以最近出现的任务类型为主，并且早期领域的信息会被隐式遗忘。

##### 结构抽象。

这些提供者故意丢弃特定于任务的内容，仅保留解决方案的形状：AWM 使用变量名称参数化工作流程 (target\_subject\_page, revision\_year); SkillWeaver 编译通用 Python 函数； Memp 引入了一个剥离了特定实体的“心理模型”脚本。当两个任务尽管表面不相关但共享抽象计算逻辑时，它们会表现出色。它们的故障模式是互补的。 *过度概括* – Memp 的实体剥离脚本丢失了某些任务所依赖的细节。 *覆盖不足* – SkillWeaver 保留的技能非常少，因此如果传入任务与现有技能签名不匹配，则检索不会返回任何内容。 *缺少警告* – AWM 仅摄取成功的轨迹；对于智能体的自然倾向是已知陷阱的任务，AWM 没有机制来显示警告。

##### 洞察力积累。

这些提供者将每个轨迹分解为许多小的、可重复使用的单元；每个单元都可以独立检索并与其他单元组合。对于那些成功取决于“组装”几个原子最佳实践（例如，站点限制搜索+对照参考列表交叉检查+引用确切部分）的任务来说，这是最强的。失效模式由检索几何驱动。 *词汇泛滥*：拥有数千个存储的见解，许多共享通用名词（“维基百科”、“搜索”），因此 top-kk 退化为通用建议，而特定任务的课程则降至截止值以下。 *关键字脆弱性*：Mobile-E 使用纯关键字匹配，因此不与存储的提示共享表面词汇的查询不会检索到任何内容。 *修剪删除负面证据*：EvolveR 放弃了低分原则，但罕见的警告原则正是那些可以在其应用的罕见任务中拯救智能体的原则。 *图污染*：InsightGraph 积极创建SIMILAR\_CONCEPT 边缘，并且一些通用见解（*例如*，“使用站点限制搜索”）成为主导图扩展的中心，无论查询如何。

### D.2 定性透镜：任务表面和传输要求

上述故障模式的出现是因为每个提供商公开了不同的传输单元。相似性检索提供者青睐任务描述与当前查询接近的记忆；结构抽象提供者公开可重用的过程，并删除了特定于任务的细节；洞察力积累提供者检索可以组合的较小碎片。这些合约都不是一律优选的：它们的效用取决于当前任务需要什么以及填充的商店实际上可以返回的内容。

这种观点激发了内容感知探测，而不假设路由器显式地恢复了潜在的逻辑形式。探测片段揭示了每个提供者可用于当前任务的具体内存，允许路由器比较提供者输出，而不是仅依赖于静态提供者描述或任务级表面相似性。

### D.3 案例研究：存储中的互补传输模式

我们用从填充的内存存储中抽取的五个案例来说明这些互补的传输模式。这些案例展示了特定于提供者的表示如何暴露其他提供者错过的有用内容；案例 5 呈现了相反的情况，其中表面接近度误导了相似性检索器。

##### 案例 1：权威 PDF 检索（InsightGraph 桥接不相关的表面）。

*•

  任务 A：*“艾米丽·米德基夫 2014 年 6 月在一本以赫里德玛儿子的名字命名的期刊上发表的文章中……，两位不同的作者引用了哪个词来表达对龙描绘本质的厌恶？”*
*•

  任务 B：*“莱斯特大学论文‘Hiccup 能供应足够的鱼来维持……’中计算出的鱼袋体积是多少立方米？”*

由于任务本质上不共享表面词汇，因此密集的任务到任务检索不会产生有用的跨任务信号。然而，InsightGraph 通过 SIMILAR\_CONCEPT 边将它们连接起来
*“使用有针对性的站点和文件类型限制搜索，结合作者、日期和期刊名称变体来查找权威 PDF”*（来自任务 A）和
*“使用精确标题和站点限制的搜索查询（引用和站点：）快速定位权威 PDF”*（来自任务 B）。
尽管这两个任务具有不同的表面词汇，但都可以重用相同的操作模式：*识别唯一标题→\to按站点/文件类型限制搜索→\to从PDF中提取一个字段*。任务级相似性检索不会暴露这种联系，因为它的比较单位是完整的任务描述。 InsightGraph 可以公开它，因为它的可索引单元是原子洞察力，并且图形扩展将该洞察力从一个任务传播到另一个任务的检索上下文中。

##### 案例 2：跨异构域重用工作流（AWM 成功；Voyager 失败）。

来自“Mercedes Sosa studio albums”训练任务的存储 AWM 工作流程将解决方案抽象为通用框架：*定义变量 {\{artist\_name, wiki\_url, start\_year, end\_year}\} →\to 检索页面→\to 解析结构化列表→\to 按年份范围过滤*。在评估过程中，来自完全不同领域的两个 GAIA 任务（一个维基百科页数问题和一个五人魔兽世界小组组成问题）都受益于这个工作流程，因为它们可以重用相同的操作模式：*打开目标页面→\to解析结构化列表→\to通过谓词过滤→\to计数*。相比之下，Voyager 存储了 Mercedes Sosa 轨迹的文字叙述（“我搜索并爬行……计划了 MediaWiki API 查询……”），它仍然与音乐领域相关；因此，它对 WoW 任务的 top-1 检索会产生不相关的轨迹。当新任务需要工作流程的“形状”而不是特定执行的叙述时，这种性能差距就会出现。

##### 情况 3：反模式警告（ExpeL 成功；AWM 保持沉默）。

GAIA 任务询问：*“维基百科关于反分裂主义的页面进行了多少次编辑……？”*。智能体的自然行为是从页面的历史 UI 复制修订计数器，由于分页和软恢复，该计数器会过度计数。这种故障模式出现在训练轨迹中。 ExpeL 采集了成功和失败信息，并存储了一条警告：

> “当维基百科任务要求‘编辑’或‘修订’的数量时，验证页面历史记录 UI 中的计数器是否已分页；不要直接依赖历史页面计数器。”

AWM 在设计上丢弃了这种警告注释（仅成功摄取），因此它对此任务的检索无法防止陷阱。该任务由 ExpeL、InsightGraph 和 智能体-KB 解决，但不能由 AWM、Voyager、DILU 或无内存基线解决。

##### 案例 4：可执行技能泛化（SkillWeaver 的全有或全无的回报）。

SkillWeaver 存储了一个 Python 函数 find\_adjacent\_players(team, as\_of\_date)，该函数返回在给定日期的目标球员之前和之后具有球衣号码的球员。要求“截至 2023 年 7 月，Taishō Tamai 号码前后号码的投手”的评估任务与此函数签名*完全匹配*；该技能确定性地运行并返回答案。要求相邻单元格的同级 Excel 地图导航任务没有匹配的技能，并且 SkillWeaver 不提供有用的内存。该案例揭示了可执行技能内存的权衡：当抽象算法匹配时，该技能严格优于任何工作流程描述，因为它“执行”；如果没有，该技能就没有任何好处。

##### 案例 5：相似性陷阱（DILU 在近似释义上产生误导）。

当两个任务共享表面形式但它们施加的约束不同时，就会出现相反的失败：

*•

  存储轨迹：*“Mercedes Sosa 在 2000 年至 2009 年间发行了多少张录音室专辑？”*
*•

  评估任务：*“Mercedes Sosa 在 2000 年之前发行了多少张录音室专辑？”*

这两个查询是余弦空间中的近似释义。 DILU 以高置信度返回存储的轨迹，并且智能体将其年份范围过滤器 [2000, 2009] 复制到新查询中，从而产生十年内的答案。 AWM 将 {start\_year, end\_year} 公开为占位符，避免了陷阱，因为在执行之前必须从当前查询重新绑定占位符。这个案例是案例 1-2 的镜像：当表面“太”接近结构时，相似性检索就会过度拟合；结构抽象总是重新绑定变量。

### D.4 影响

这些案例说明了提供商池的三个经验属性。 *(i)* 提供者的表示和检索合同决定了过去经验的哪些部分可以公开以供重用。 *(ii)* 表面相似性可能很有用，但它也可能会错过可转移的过程或检索具有不兼容约束的近似释义；结构抽象和较小的洞察单元提供了互补的替代方案。 *(iii)* 内容感知探测让 MemAgent 检查每个填充的提供程序可以为当前任务返回什么，并在这些补充输出中进行选择。该分析在不假设显式潜在结构恢复的情况下解释了提供者的异质性。

[36](https://arxiv.org/html/2609.32521#bib.bib61), [34](https://arxiv.org/html/2609.32521#bib.bib59), [35](https://arxiv.org/html/2609.32521#bib.bib57), [32](https://arxiv.org/html/2609.32521#bib.bib58), [33](https://arxiv.org/html/2609.32521#bib.bib60)

