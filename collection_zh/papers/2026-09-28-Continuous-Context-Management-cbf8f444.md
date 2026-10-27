> 本文为简体中文机器翻译，使用 Google Translate 公开接口并统一技术术语，尚未经逐句人工校对。代码、链接和公式按原文保留；实验数字及技术结论请对照原文。
> [查看本地英文原文](../../collection/papers/2026-09-28-Continuous-Context-Management-cbf8f444.md) · [原始来源](https://arxiv.org/abs/2609.35540)

# 持续上下文管理

- 来源: https://arxiv.org/abs/2609.35540- 发布日期: 2026-09-28- 日期依据: page metadata: citation_date- 类型: paper- 主题: 持续上下文管理、强化学习- 抓取状态: full_text_html- 正文来源: https://arxiv.org/html/2609.35540- 抓取时间 UTC: 2026-10-26T09:33:42.159450+00:00 - 作者: Hoy, William, Fan, Jingxuan, Celik, Nurcin, Pan, Xu

## 来源摘要/页面简介

摘要：长程大语言模型（LLM）智能体通常会保留其完整的交互历史记录，直到在预定义阈值触发压缩为止。我们研究了连续上下文管理（CCM），它每次都会执行压缩，以防止交互历史记录在活动提示中累积。在每一回合，CCM 智能体都会发出更新的记忆以及环境操作；它的下一个提示包含原始任务、保留的记忆和最新的观察结果，而不是完整的记录。我们首先使用Claude Sonnet 4.6、Claude Opus 4.6、GLM-5和Kimi K3评估CCM，无需对TerminalBench-2进行微调。 CCM 大大减少了累积输入使用量和活动提示大小，尽管它会降低大多数模型的任务成功率，同时保留Kimi K3的性能。我们使用具有特权全历史蒸馏的 GRPO 来改进开放权重模型中的 CCM。学生初始模型的冻结副本根据学生的推出重建的完整历史记录对每个采样的学生动作进行评分，从而提供密集的动作词元监督，而无需单独的教师推出或参考解决方案。在 WebShop 上，该目标在两个评估模型尺度上都显着提高了 CCM 相对于 GRPO 的性能，并且超过了 Qwen3-4B-Instruct 的全历史 GRPO，但对于 Qwen3-8B 则不然。在 Endless Terminals 上，增强方法比 GRPO 有了一定的改进，两种 CCM 策略都优于未经训练的全历史基线。这些结果表明，对于在保留上下文大幅减少的情况下运行的智能体来说，CCM 是一种可行的推理范式，并且可以通过具有特权的全历史蒸馏的强化学习来提高其性能。

## 抓取正文（中文翻译）

# 持续上下文管理

威廉·霍伊

迈阿密大学

wjh58@miami.edu

范景轩

哈佛大学

jfan@g.harvard.edu

努尔钦·塞利克

迈阿密大学

celik@miami.edu

徐攀

哈佛大学

xupan@fas.harvard.edu

###### 摘要

长程大语言模型 (LLM) 智能体通常会保留其完整的交互历史记录，直到在预定义阈值触发压缩为止。我们研究了连续上下文管理（CCM），它每次都会执行压缩，以防止交互历史记录在活动提示中累积。在每一回合，CCM 智能体都会发出更新的记忆以及环境操作；它的下一个提示包含原始任务、保留的记忆和最新的观察结果，而不是完整的记录。我们首先使用Claude Sonnet 4.6、Claude Opus 4.6、GLM-5和Kimi K3评估CCM，无需对TerminalBench-2进行微调。 CCM 大大减少了累积输入使用量和活动提示大小，尽管它会降低大多数模型的任务成功率，同时保留Kimi K3的性能。我们使用具有特权全历史蒸馏的 GRPO 来改进开放权重模型中的 CCM。学生初始模型的冻结副本根据学生的首次展示重建的完整历史记录对每个采样的学生动作进行评分，从而提供密集的动作词元监督，而无需单独的教师首次展示或参考解决方案。在 WebShop 上，该目标在两个评估模型尺度上都显着改善了 GRPO 上的 CCM，并且超过了Qwen3-4B-Instruct 的全历史 GRPO，但对于 Qwen3-8B 则不然。在 Endless Terminals 上，增强方法比 GRPO 提供了适度的改进，两种 CCM 策略都优于未经训练的全历史基线。这些结果表明，对于在保留上下文大幅减少的情况下运行的智能体来说，CCM 是一种可行的推理范式，并且可以通过具有特权的全历史蒸馏的强化学习来提高其性能。

|  |
| ---|
|  |

## 1 简介

长程语言智能体必须在与环境的重复交互中保留有用的信息。购物智能体可能需要记住之前遇到的几个页面的产品属性，而终端智能体可能需要保留先前命令的结果。保留完整的交互历史记录可以直接访问这些信息，但会导致活动上下文随着任务的进行而增长。累积的历史受到模型上下文窗口的限制，即使在此限制内，随着输入的增长，模型性能也会下降（[Liu et al., 2024](https://arxiv.org/html/2609.35540#bib.bib31); [Du et al., 2025](https://arxiv.org/html/2609.35540#bib.bib3); [Hong et al., 2025](https://arxiv.org/html/2609.35540#bib.bib32))或包括不相关信息（[Shi et al., 2023](https://arxiv.org/html/2609.35540#bib.bib30)）。

常见的解决方案是当上下文达到预定义的词元阈值时压缩交互历史记录，用较短的摘要替换较早的内容（[Wu et al., 2025](https://arxiv.org/html/2609.35540#bib.bib5); [Li et al., 2026c](https://arxiv.org/html/2609.35540#bib.bib15)）。重复压缩允许会话继续超出单个上下文窗口的长度。然而，上下文仍然在压缩事件之间累积，并且在再次压缩之前可能占据可用窗口的很大一部分。这种累积紧凑范式的最终形式是内存管理成为每个操作步骤的一部分，并且智能体不断更新它所携带的信息。我们研究了这种称为连续上下文管理（CCM）的设置，其中智能体在每个动作旁边生成更新的记忆，其下一个上下文是根据更新的记忆和最新的观察构建的。 “连续”是指以最精细步长分辨率进行内存管理，而不是其数学含义。当 GPU 内存成为主要限制时，例如在消费级 GPU 上本地部署 LLM，保持活动上下文紧凑可以减少词元缓存内存，从而允许更大的模型在相同的 GPU 内存预算内运行，这尤其有用。

我们首先使用Claude Sonnet 4.6、Claude Opus 4.6、GLM-5和Kimi K3将CCM评估为TerminalBench-2上的开箱即用推理范例。在这些模型中，CCM 大大减少了累积输入使用量和典型的活动提示大小。 Sonnet、Opus 和 GLM-5 ​​的成功率有所下降，但 Kimi K3 的成功率略有上升。由此产生的资金节省在很大程度上取决于提供商特定的提示缓存策略和词元价格：前缀缓存可以大大降低完整历史提示的成本，尽管其词元使用量更大。这些结果证明了 CCM 具有减少上下文使用的潜力，同时揭示了四个模型中三个模型的性能差距，从而激发了我们对 CCM 智能体训练方法的研究。

先前的工作已经确立了学习此类内存管理行为的可行性，例如 MEM1、MemAgent、MMENTO 和 压缩整合 RL（[Zhou et al., 2025](https://arxiv.org/html/2609.35540#bib.bib11)；[Yu et al., 2025](https://arxiv.org/html/2609.35540#bib.bib12)；[Kotonis et al., 2026](https://arxiv.org/html/2609.35540#bib.bib9)；[李等人，2026c](https://arxiv.org/html/2609.35540#bib.bib15))。基于这些方法，特别是 MEM1 中使用的每回合整合，我们结合了两个训练信号来训练智能体管理记忆并使用它们来生成动作。这两种能力紧密结合。智能体可能保留相关事实，但在选择行动时不使用它们；相反，有效的行动政策无法可靠地弥补其记忆中遗漏的重要信息。强化学习可以通过任务奖励来优化这两种能力，但情节级别的结果对单个任务操作提供的指导有限。为了对紧凑内存生成的动作提供额外的监督，我们使用基于策略上下文蒸馏的额外蒸馏目标（[Ye et al., 2026](https://arxiv.org/html/2609.35540#bib.bib20)）和 SDAR 的门控自蒸馏方法（[Lu et al., 2026](https://arxiv.org/html/2609.35540#bib.bib27)），其中教师将完整的交互历史视为特权信息。教师在训练前使用与学生相同的权重进行初始化，并在整个训练过程中保持冻结状态。在每一步中，它都会接收当前操作之前的完整历史记录，并对学生采样的操作标记进行自回归评分。词元级教师-学生置信差距门对动作词元上的策略梯度进行加权。该过程提供了动作词元监督，无需单独训练的教师、额外的教师部署或成功的参考轨迹。

我们在 WebShop 和 Endless Terminals 上评估了这个训练方法，专注于提高智能体性能，同时仅使用完整历史基线所需的提示上下文的一小部分。在 WebShop 上，与单独使用 GRPO 训练的 CCM 相比，添加全历史蒸馏大大提高了两个模型的任务成功率。在 Endless Terminals 上，两种经过训练的 CCM 策略都优于未经训练的全历史基线，同时保持紧凑的模型写入记忆。与 CCM + GRPO 相比，蒸馏提供了适度的改进。总之，这些结果表明，我们的训练方案提高了 CCM 的任务绩效，同时保留了显着的即时长度节省。

我们的主要贡献是：

*•

  我们研究连续上下文管理（CCM），其中智能体在每个操作步骤更新紧凑的内存。我们对 TerminalBench-2 的评估表明，无需额外培训即可大幅减少输入词元的使用，并描述了任务性能和 API 成本权衡的特征。
*•

  我们引入了一种将 GRPO 与特权全历史蒸馏相结合的训练方法。对WebShop和Endless Terminals的实验表明，训练提高了CCM的任务性能，同时大大减少了上下文长度。

## 2 相关作品

##### 长程智能体的上下文管理。

ReAct 风格的智能体在后续提示中保留推理、动作和观察的完整序列（[Yao et al., 2022b](https://arxiv.org/html/2609.35540#bib.bib1)），因此上下文会随着时间的推移而增长，并且长时间输入时性能可能会下降（[Du et al., 2025](https://arxiv.org/html/2609.35540#bib.bib3)）。推理时间方法通过外部记忆、周期性总结、结构化压缩和不断发展的上下文表示来扩展视野（[Packer et al., 2023](https://arxiv.org/html/2609.35540#bib.bib4); [Wu et al., 2025](https://arxiv.org/html/2609.35540#bib.bib5); [Kang et al., 2025](https://arxiv.org/html/2609.35540#bib.bib6); [Wan et al., 2025](https://arxiv.org/html/2609.35540#bib.bib7)；[Zhang et al., 2026a](https://arxiv.org/html/2609.35540#bib.bib8)；[Li et al., 2026a](https://arxiv.org/html/2609.35540#bib.bib16))，以及一些工作训练模型来生成摘要或决定何时压缩（[Lu et al., 2025](https://arxiv.org/html/2609.35540#bib.bib10)；[Li 等人，2026b](https://arxiv.org/html/2609.35540#bib.bib13)；[Zhang 等人，2026c](https://arxiv.org/html/2609.35540#bib.bib14)；[Yu 等人，2025](https://arxiv.org/html/2609.35540#bib.bib12)；等，2026](https://arxiv.org/html/2609.35540#bib.bib9))。 MEM1（[Zhou et al., 2025](https://arxiv.org/html/2609.35540#bib.bib11)）在表述上与我们的方法最接近。在每个回合，智能体都会发出一个内部状态，将其先前的状态与最新的观察结果相结合，并且较早的回合会被修剪。 MEM1 从 PPO 的结果奖励中学习这种行为，通过注意掩模对串联轨迹进行训练，该注意掩模将每个标记限制在生成时可用的上下文中。我们的研究在几个方面与 MEM1 不同。首先，我们表明前沿模型可以在无需额外训练的情况下使用开箱即用的 CCM，从而大大减少上下文使用，尽管大多数评估的模型都会导致任务性能下降。其次，我们不是仅仅依靠结果奖励来训练模型来管理其状态，而是将情节级 GRPO 与设计的词元级蒸馏目标结合起来。

##### 强化学习和同策略蒸馏。

GRPO 等强化学习方法提供来自环境或验证者奖励的轨迹级监督（[Shao et al., 2024](https://arxiv.org/html/2609.35540#bib.bib17)；[Dong et al., 2025](https://arxiv.org/html/2609.35540#bib.bib18)；[Feng et al., 2025](https://arxiv.org/html/2609.35540#bib.bib19)）。在政策蒸馏（包括在政策自我蒸馏）中，通过来自更强大的老师或来自以特权信息为条件的相同政策的密集词元级指导来补充这种反馈（[Ye et al., 2026](https://arxiv.org/html/2609.35540#bib.bib20); [Yang et al., 2026](https://arxiv.org/html/2609.35540#bib.bib21); [MiMo Team, 2026](https://arxiv.org/html/2609.35540#bib.bib22);[GLM-5团队,2026](https://arxiv.org/html/2609.35540#bib.bib23);[赵等人,2026](https://arxiv.org/html/2609.35540#bib.bib24);[何等人,2026](https://arxiv.org/html/2609.35540#bib.bib25); [Zhang 等人，2026b](https://arxiv.org/html/2609.35540#bib.bib26))。 [卢等人。 (2026)](https://arxiv.org/html/2609.35540#bib.bib27)提出了自蒸馏智能体强化学习（SDAR），它结合了强化学习和策略自蒸馏，使用基于学生不确定性或师生信心差距的词元级门。我们将其置信间隙门控调整为多轮 CCM 智能体。对于每个采样的动作标记，我们将其在当前策略的紧凑 CCM 上下文下的概率与在学生初始模型的冻结副本下的概率进行比较，以重建的完整历史记录为条件。在整个训练过程中，教师的权重保持固定。这提供了辅助动作词元蒸馏信号，而不需要单独训练的教师、额外的教师部署或成功的参考轨迹。

## 3 持续上下文管理

### 3.1 方法说明

对于任务 xx，令 o0o\_{0} 表示初始环境观测值 m0m\_{0} 最初是空的记忆。轮到时 n≥1n\geq 1、连续上下文管理（CCM）智能体接收观察 on−1o\_{n-1} 和保留的记忆 mn−1m\_{n-1}, 并生成更新的记忆 mnm\_{n} 和行动 ana\_{n} 根据

|  |  |  |  |
| ---| ---| ---| ---|
|  | (mn,an)∼πθ(⋅∣x,mn−1,on−1),(m\_{n},a\_{n})\sim\pi\_{\theta}\!\left(\cdot\mid x,\,m\_{n-1},\,o\_{n-1}\right), |  | (1) |

生成的响应由更新的记忆和环境操作组成，yn=[mn;an]y\_{n}=[\,m\_{n}\,;\,a\_{n}\,].执行ana\_{n}产生下一个观察ono\_{n}.智能体然后从xx、mnm\_{n},和ono\_{n}.构建第n+1n+1轮的提示。不直接包含在内。因此，只有当智能体决定将其保存在mnm\_{n}.时，早期轮次的信息才仍然可用

图 1：持续上下文管理。在每一轮，智能体都会接收原始任务、上一轮的记忆以及当前的观察结果。它发出更新的记忆，然后执行环境操作。下一个提示是根据更新的记忆和最新的观察而不是完整的交互记录构建的。

### 3.2 TerminalBench-2 结果

Terminal-Bench 2.0 （[Merrill et al., 2026](https://arxiv.org/html/2609.35540#bib.bib2)）包含 89 个具有挑战性的人工任务，需要智能体通过终端交互来完成现实的工作流程。我们使用 Claude Sonnet 4.6、Claude Opus 4.6、GLM-5 和 Kimi K3 评估所有 89 项任务的 CCM。对于每个模型，我们使用 pass@1 将 CCM 与标准全历史基线进行比较。

表 [1](https://arxiv.org/html/2609.35540#S3.T1“表 1 ‣ 3.2 TerminalBench-2 结果 ‣ 3 连续上下文管理 ‣ 连续上下文管理”) 报告任务成功、词元使用情况以及每个任务的估计 API 成本；表 [5](https://arxiv.org/html/2609.35540#A1.T5“表 5 ‣ 附录 A Terminal-Bench 2.0 推理配置 ‣ 连续上下文管理”）还报告了交互长度和详细的词元统计。 Claude Sonnet 4.6、Claude Opus 4.6 和 Kimi K3 帐户用于提供商端提示缓存的成本估算。报告GLM-5，但没有提示缓存，因为 Amazon Bedrock 对此模型不支持。附录 [A](https://arxiv.org/html/2609.35540#A1“附录 A Terminal-Bench 2.0 推理配置 ‣ 连续上下文管理”) 中提供了推理和词元记账配置。

表 1：89 项任务中Terminal-Bench 2.0 pass@1 结果。成本是根据每个任务的估算方法，包括可用的即时缓存；无法通过 Amazon Bedrock 对 GLM-5 进行提示缓存。

|  |  |  |  |  |  |  |
| ---| ---| ---| ---| ---| ---| ---|
|  |  |  |峰值提示词元 | |  |  |
|型号|模式|成功，nn (%) |中位数|最大|最大保留内存|每项任务的预计成本|
| Claude Sonnet 4.6 |基线| 38 (42.7) | 38 (42.7) 16,673 | 16,673 131,157 | 131,157 – | 0.468 美元 |
|  | CCM| 28（31.5）| 3,568 | 3,568 50,614 | 1,219 | 1,219 0.472 美元 |
| Claude Opus 4.6 |基线| 52（58.4）| 15,405 | 15,405 103,512 | 103,512 – | 0.831 美元 |
|  | CCM| 36（40.4）| 4,280 | 4,280 51,457 | 51,457 1,403 | 1,403 1.087 美元 |
| GLM-5 |基线| 31 (34.8) | 17,560 | 17,560 116,407 | 116,407 – | 0.515 美元 |
|  | CCM| 26 (29.2) | 26 (29.2) | 4,279 | 4,279 47,287 | 47,287 561 | 561 0.124 美元 |
| Kimi K3 |基线| 56（62.9）| 9,472 | 9,472 74,313 | – | 0.302 美元 |
|  | CCM| 57（64.0）| 3,243 | 3,243 27,645 | 27,645 1,058 | 1,058 0.622 美元 |

如表 [1](https://arxiv.org/html/2609.35540#S3.T1“表 1 ‣ 3.2 TerminalBench-2 结果 ‣ 3 连续上下文管理 ‣ 连续上下文管理”) 所示，CCM 显着降低了所有四种模型的峰值提示大小。中位情节级别峰值从完整历史提示下的 9,472–17,560 个词元减少到 CCM 下的 3,243–4,280 个词元。最大的保留 CCM 内存仅包含 561-1,403 个词元。不过，最大 CCM 提示可能会大得多，因为每个提示还包括最新的终端观察结果，最多可能包含 60,000 个字符。 CCM 限制累积的交互历史，但不压缩当前的观察。

CCM 还将 Claude Sonnet 4.6 每个任务的平均累积输入标记减少了 83.1%，Claude Opus 4.6 减少了 81.5%，GLM-5 减少了 84.3%，Kimi K3 减少了 75.8%。这种压缩伴随着 Sonnet、Opus 和 GLM-5 的 pass@1 成功率降低，分别下降了 11.2、18.0 和 5.6 个百分点。相比之下，Kimi K3在 CCM 下略有改善，从 62.9% 提高到 64.0%。

货币效果在很大程度上取决于提供商端的即时缓存。对于 Sonnet，这两种方法的估计成本几乎相同：完整历史提示每个任务 0.468 美元，CCM 0.472 美元。对于 Opus 和 Kimi，缓存使得完整历史提示的成本更低，尽管它的累积输入使用量要大得多：Opus 的$0.831 versus $1.087，Kimi 的 0.302 美元和 0.622 美元。由于我们的 GLM-5 端点不支持提示缓存，因此输入减少将每个任务的估计成本从 $0.515 to $0.124 降低。总体而言，CCM 持续减少峰值和累积上下文使用，但其对任务成功和货币成本的影响取决于模型以及提供商的缓存和定价策略。

## 4 通过强化学习改进持续上下文管理

### 4.1 自蒸馏 GRPO

我们通过结合 GRPO 和基于蒸馏的目标来改进 CCM 政策。我们将第[3]节（https://arxiv.org/html/2609.35540#S3“3连续上下文管理‣连续上下文管理”）中定义的CCM策略称为*学生*，并用ynS:=yn=[mn;an]y^{S}\_{n}:=y\_{n}=[\,m\_{n}\,;\,a\_{n}\,].表示其在第nn轮的响应。学生推出遵循图[1](https://arxiv.org/html/2609.35540#S3.F1“图1‣”中所示的CCM交互过程） 3.1方法说明‣3连续上下文管理‣连续上下文管理》）。 GRPO 优化学生回答中的所有有效标记，包括记忆和动作标记（详细信息参见附录 [B](https://arxiv.org/html/2609.35540#A2“附录 B GRPO 目标 ‣ 连续上下文管理”)）。

除了 GRPO 之外，我们还使用基于蒸馏的目标。 *教师*策略是训练前学生模型的冻结副本。它的权重在整个训练过程中保持固定，而学生则更新。在每个回合中，教师都会使用完整的环境历史记录来为学生根据紧凑的记忆进行操作提供动作标记监督。

具体来说，我们将当前操作ana\_{n}之前的学生环境历史重建为特权信息，hnS=(o0,a1,o1,…,an−1,on−1)h^{S}\_{n}=\bigl(o\_{0},a\_{1},o\_{1},\ldots,a\_{n-1},o\_{n-1}\bigr),，其中o0o\_{0}是初始观察结果。此历史记录仅包括先前的操作和观察，不包括当前操作 ana\_{n}. 对于当前操作 ana\_{n}, 内的标记位置 tt，学生以 sn,tC=PC​(x,mn−1,on−1,mn,an,<t)s^{C}\_{n,t}=P\_{C}\bigl(x,m\_{n-1},o\_{n-1},m\_{n},a\_{n,<t}\bigr), 为条件，其中 PCP\_{C} 是 CCM 提示渲染器，mnm\_{n} 已作为第一部分生成当前响应的，an,<ta\_{n,<t}表示前面的操作词元前缀。特权教师以sn,t+=PF​(x,hnS,an,<t)s^{+}\_{n,t}=P\_{F}\bigl(x,h^{S}\_{n},a\_{n,<t}\bigr),为条件，其中PFP\_{F}是完整历史提示渲染器。当评分an,ta\_{n,t},时，除了任务xx之外，教师仅收到hnSh^{S}\_{n}和前面的动作词元前缀an,<ta\_{n,<t}；目标标记和后续操作标记都不包含在其调节上下文中。学生和老师从相同的轨迹中获得相同的采样动作词元。学生使用当前权重和紧凑的内存，而教师使用固定的初始权重和完整的动作前环境历史记录。

图 2：使用 GRPO 和全历史自蒸馏训练 CCM 智能体。上图：学生 πθ\pi\_{\theta} 在 CCM 下推出。具有情节任务奖励的 GRPO 优化了所有响应标记，包括记忆和动作。底部：教师πθ0\pi\_{\theta\_{0}}是学生初始模型的副本，权重在整个训练过程中保持固定。它接收从学生的展示中重建的行动前环境历史，并对学生采样的行动进行自回归评分。对于每个动作标记，教师对数概率 ℓT\ell^{T} 和学生对数概率 ℓS\ell^{S} 给出置信间隙 Δ\Delta. 该间隙设置门 gg，仅对有效动作标记的蒸馏损失 ℒdistill=−mean⁡(g​ℓS)\mathcal{L}\_{\text{distill}}=-\,\mathrm{mean}(g\,\ell^{S}) 进行加权。总训练损失由GRPO损失和蒸馏损失组成。

对于学生采样的动作标记an,ta\_{n,t},，我们将教师学生信心差距定义为

|  |  |  |  |
| ---| ---| ---| ---|
|  | Δn,t=stopgrad⁡[log⁡πθ0​(an,t∣sn,t+)−log⁡πθ​(an,t∣sn,tC)],\Delta\_{n,t}=\operatorname{stopgrad}\!\left[\log\pi\_{\theta\_{0}}\bigl(a\_{n,t}\mid s^{+}\_{n,t}\bigr)-\log\pi\_{\theta}\bigl(a\_{n,t}\mid s^{C}\_{n,t}\bigr)\right], |  | (2) |

其中θ0\theta\_{0}表示学生在任何训练更新之前的初始参数。教师πθ0\pi\_{\theta\_{0}}在整个训练过程中保持冻结状态，并且永远不会因更新的学生而刷新。运算符stopgrad⁡[⋅]\operatorname{stopgrad}[\cdot]在反向传播期间将其参数视为常数。

遵循 SDAR 的间隙门控公式（[Lu et al., 2026](https://arxiv.org/html/2609.35540#bib.bib27)），我们将置信间隙转换为词元级门，gn,t=stopgrad⁡[σ⁡(β​Δn,t)]g\_{n,t}=\operatorname{stopgrad}\!\left[\sigma\bigl(\beta\Delta\_{n,t}\bigr)\right],，其中σ\sigma是逻辑 sigmoid，β>0\beta>0控制门锐度。获得特权老师更大信任的词元具有Δn,t>0\Delta\_{n,t}>0，并且获得更大的门控权重。已经获得学生更大信心的词元具有Δn,t<0\Delta\_{n,t}<0并且被削弱，但保留了较小的正权重。

令 Mi,n,t∈{0,1}M\_{i,n,t}\in\{0,1\} 表示词元 tt 属于 rollout ii 的第 nn 次有效操作块，并且具有有效的学生和教师分数。蒸馏损失是所有符合条件的操作词元的平均值：

|  |  |  |  |
| ---| ---| ---| ---|
|  | Ldistill=−∑i,n,tMi,n,tgi,n,tlogπθ(ai,n,t∣si,n,tC)/∑i,n,tMi,n,t.L\_{\mathrm{distill}}={-\displaystyle\sum\_{i,n,t}M\_{i,n,t}g\_{i,n,t}\log\pi\_{\theta}\bigl(a\_{i,n,t}\mid s^{C}\_{i,n,t}\bigr)}/{\displaystyle\sum\_{i,n,t}M\_{i,n,t}}. |  | (3) |

蒸馏损失适用于所有有效的学生生成的操作标记（仅适用于任务操作，与同时适用于内存和任务操作的 GRPO 不同）。它根据师生对数概率差距对每个标记的梯度进行加权。当全历史教师分配一个比紧凑上下文学生更高的概率时，该词元会收到更大的门控权重变化，从而鼓励学生重现附加上下文支持的词元。负间隙词元接收较小的门控权重，从而缩小梯度的大小。在附录 [C](https://arxiv.org/html/2609.35540#A3“附录 C 有关蒸馏目标的详细信息‣连续上下文管理”）中，我们展示了在策略采样下的固定上下文中，预期更新相当于使用 OPD 有符号对数概率间隙的有界、中心 sigmoid 变换，在局部恢复小间隙的缩放 OPD 梯度。

组合训练损失为Ltotal=LGRPO+λdistill​LdistillL\_{\mathrm{total}}=L\_{\mathrm{GRPO}}+\lambda\_{\mathrm{distill}}L\_{\mathrm{distill}}.，我们设置λdistill=0.01\lambda\_{\mathrm{distill}}=0.01和β=5\beta=5.其他训练配置详细信息请参见附录[E](https://arxiv.org/html/2609.35540#A5“附录E实验细节‣连续上下文管理”）。

### 4.2 WebShop 结果

WebShop （[Yao et al., 2022a](https://arxiv.org/html/2609.35540#bib.bib29)）是一个模拟购物基准，用于测试客服人员浏览网页、选择产品选项和完成购买的能力。图[3](https://arxiv.org/html/2609.35540#S4.F3“图3‣4.2WebShop结果‣4通过强化学习改进连续上下文管理‣连续上下文管理”）比较了Qwen3-4B-Instruct的训练检查点的CCM + GRPO与CCM + GRPO +蒸馏Qwen3-8B。未经训练的 CCM 和完整历史条件提供了固定的参考点。表 [2](https://arxiv.org/html/2609.35540#S4.T2“表 2 ‣ 4.2 WebShop 结果 ‣ 4 通过强化学习改进连续上下文管理‣连续上下文管理”）还报告了完整历史 GRPO 并总结了每个训练方法的最佳观察检查点的任务性能、记忆行为和提示大小。

图 3：在固定的 128 任务 pass@1 评估中，对 Qwen3-4B-Instruct（上）和 Qwen3-8B（下）进行WebShop 检查点评估，温度为 0.4，种子为 42，轮数限制为 15。列报告确切的任务成功情况、部分WebShop分数和平均情节长度。实线显示跨检查点 10-100 的 CCM + GRPO 和 CCM + GRPO + 蒸馏。虚线表示相应的未经训练的 CCM 和完整历史表现。

在步骤100，在两个模型尺度上，添加特权蒸馏显着改进了CCM，而CCM+GRPO则优于CCM+GRPO。对于Qwen3-4B-Instruct，添加特权蒸馏将精确成功率提高了 62.50 个百分点，从 24.22% 提高到 86.72%，而部分得分从 0.817 提高到 0.948。蒸馏增强的 CCM 策略也超过了全历史 GRPO，其准确率达到 75.78%，部分得分为 0.839。它平均完成任务 5.36 回合，而全历史 GRPO 为 5.85 回合，CCM + GRPO 为 15.00 回合。

对于第 100 步的Qwen3-8B，添加特权蒸馏比 CCM + GRPO 提高了精确成功率 46.09 个百分点，从 11.72% 提高到 57.81%。其部分得分略低，分别为 0.728 和 0.744。全历史 GRPO 仍然是该模型的最强条件，准确率达到 80.47%，部分得分为 0.907。 CCM + GRPO + 蒸馏的平均剧集长度为 6.63 回合，CCM + GRPO 的平均剧集长度为 9.13 回合，全历史 GRPO 的平均剧集长度为 5.55 回合。

压缩匹配轨迹在附录 [F.1](https://arxiv.org/html/2609.35540#A6.SS1“F.1 WebShop⟧‣附录 F 定性轨迹分析‣连续上下文管理”)中报告。在所选任务中，未经训练的策略在搜索或导航过程中失败，而 CCM + GRPO 到达正确的产品，但重复选择已选择的选项。 CCM + GRPO + 蒸馏遵循所需的产品-颜色-尺寸-购买顺序。

表 2：固定 128 项任务WebShop 评估中观察到的最佳任务成功情况和情境行为。提示在 4,096 个词元模型输入限制时被截断。

|  |  |  |  |  |  |  |  |  |
| ---| ---| ---| ---| ---| ---| ---| ---| ---|
|  |最佳表现 | |记忆行为| |内存大小 | |峰值提示词元 | |
|状况 |确切成功率 (%) |步骤|更新率(%)|前缀保留率 (%) |平均 |最大|中位数|最大|
| *Qwen3-4B-Instruct* | | | | | | | | |
|未经训练的完整历史 | 3.91 | 3.91 – | – | – | – | – | 4,096 | 4,096 4,096 | 4,096
| GRPO 完整历史 | 81.25 | 81.25 70 | 70 – | – | – | – | 1,721 | 1,721 3,076 | 3,076
|未经培训的 CCM | 0.78 | 0.78 – | 57.6 | 57.6 69.6 | 69.6 225.7 | 225.7 861 | 861 1,232 | 1,232 1,908 | 1,908
| CCM + GRPO | 32.81 | 32.81 60| 12.9 | 12.9 98.5 | 98.5 95.6 | 95.6 147 | 147 1,045 | 1,045 1,327 | 1,327
| CCM + GRPO + 蒸馏 | 86.72 | 100 | 100 100.0 | 100.0 77.2 | 77.2 60.1 | 60.1 89 | 89 1,041 | 1,041 1,279 | 1,279
| *Qwen3-8B* | | | | | | | | |
|未经训练的完整历史 | 16.41 | 16.41 – | – | – | – | – | 2,258 | 2,258 4,096 | 4,096
| GRPO 完整历史 | 82.81 | 70 | 70 – | – | – | – | 1,738 | 1,738 4,096 | 4,096
|未经培训的 CCM | 0.00 | 0.00 – | 15.0 | 15.0 96.7 | 96.7 511.8 | 511.8 1,013 | 1,013 1,582 | 1,582 2,127 | 2,127
| CCM + GRPO | 32.81 | 32.81 60| 9.1 | 99.4 | 99.4 510.6 | 510.6 994 | 994 1,200 | 1,200 1,954 | 1,954
| CCM + GRPO + 蒸馏 | 77.34 | 77.34 80| 96.9 | 96.9 82.3 | 82.3 185.3 | 185.3 421 | 421 1,149 | 1,149 1,435 | 1,435

表 [2](https://arxiv.org/html/2609.35540#S4.T2“表 2 ‣ 4.2 WebShop 结果 ‣ 4 通过强化学习改进连续上下文管理 ‣ 连续上下文管理”) 报告了每个训练方法的最佳观察检查点的内存更新行为和前缀重用。 CCM + GRPO 策略很少修改其内存。 Qwen3-4B-Instruct 和 Qwen3-8B 的内存更新率分别为 12.9% 和 9.1%，同时几乎保留了它们之前的全部内存前缀。添加蒸馏会产生更主动的内存管理。 Qwen3-4B-Instruct 在每个连续回合中都会改变其记忆，同时保留前面前缀的 77.2%； Qwen3-8B 在 96.9% 的回合中改变它，同时保留 82.3%。蒸馏的目标是改善内存使用而不是直接内存管理。然而，改善内存使用有助于 GRPO 更加有效，从而改善内存操作和任务操作。

相对于CCM + GRPO，添加特权蒸馏后，Qwen3-4B-Instruct的累计投入从10,636个减少到3,720个，Qwen3-8B的累计投入从9,929个减少到5,578个，分别减少了65.0%和43.8%。这些差异部分反映了较早的任务完成，而不仅仅是上下文压缩。 CCM 也不会自动减少总输入，未经训练的Qwen3-8B CCM 策略比其完整历史对应策略需要更多轮次，因此会处理更多词元。

### 4.3 Endless Terminals 结果

我们还使用 Qwen3-8B 在Endless Terminals（[Gandhi et al., 2026](https://arxiv.org/html/2609.35540#bib.bib28)）上比较了 CCM + GRPO 与 CCM + GRPO + 蒸馏，其中智能体执行终端命令来管理文件、处理数据、分析日志、编写脚本和操作数据库。图 [4](https://arxiv.org/html/2609.35540#S4.F4“图 4 ‣ 4.3 Endless Terminals 结果 ‣ 4 通过强化学习改进连续上下文管理 ‣ 连续上下文管理”）报告任务成功情况和平均片段长度。虚线显示了同一评估协议下未经训练的 CCM 和完整历史策略。

图 4：在 16 轮限制的固定 300 任务测试集上对 Qwen3-8B 进行Endless Terminals 检查点评估。曲线报告 CCM + GRPO 和 CCM + GRPO + 蒸馏的任务成功率（左）和平均情节长度（右）。虚线表示相应的未经训练的 CCM 和完整历史策略。

未经训练的全历史策略和 CCM 策略表现相似，分别解决了 20.33% 和 21.00% 的任务。这种差异只对应于 300 个任务中的两个。这两个条件共同解决了 43 个任务，而 18 个任务仅通过完整历史记录解决，20 个任务仅通过 CCM 解决。与其他基准相比，对如此小的差距的一种可能的解释是，Endless Terminals将其持久沙箱中的部分相关状态外部化为文件，并且 shell 状态跨轮保存，允许通过额外的检查命令恢复上下文中遗漏的信息。

观察到的最佳成功率是 CCM + GRPO + 蒸馏高出 3.00 个百分点：第 50 步为 32.00%，而 CCM + GRPO 在第 30 步为 29.00%。在第 60 步，两种方法分别达到 22.67% 和 28.33%。两项选定的 CCM 保单几乎使用全部 16 圈津贴。全历史 GRPO 取得了最强的性能，在第 30 步达到了 35.33%。尽管两种经过训练的 CCM 方法都优于未经训练的全历史和 CCM 策略，但两者都不匹配全历史 GRPO。压缩匹配轨迹的示例出现在附录[F.2](https://arxiv.org/html/2609.35540#A6.SS2“F.2Endless Terminals‣附录F定性轨迹分析‣连续上下文管理”)中。我们报告了两种经过训练的 CCM 策略中一项​​仅通过 CCM + GRPO + 蒸馏解决的任务，以及一项仅通过 CCM + GRPO 解决的任务。

表 3：通过使用 Qwen3-8B 对固定 300 个任务 Endless Terminals 进行训练步骤 60 进行训练，观察到的最佳任务成功率和记忆行为。对于每种经过训练的方法，我们都会报告评估的检查点的成功率最高，从而打破平局，支持较早的检查点。

|  |  |  |  |  |  |  |
| ---| ---| ---| ---| ---| ---| ---|
|  |最佳表现 | |记忆行为| |内存大小（词元）| |
|状况 |成功 (%) |步骤|更新率(%)|前缀保留率 (%) |平均 |最大|
|未经训练的完整历史 | 20.33 | – | – | – | – | – |
| GRPO 完整历史 | 35.33 | 30| – | – | – | – |
|未经培训的 CCM | 21:00 | – | 34.8 | 81.2 | 81.2 63.9 | 63.9 346 | 346
| CCM + GRPO | 29:00 | 30| 16.9 | 16.9 94.6 | 94.6 77.1 | 77.1 720 | 720
| CCM + GRPO + 蒸馏 | 32.00 | 50 | 50 36.9 | 36.9 72.9 | 72.9 144.0 | 144.0 906 | 906

表 [3](https://arxiv.org/html/2609.35540#S4.T3“表 3 ‣ 4.3 Endless Terminals 结果 ‣ 4 通过强化学习改进连续情境管理 ‣ 连续情境管理”) 报告了通过训练完成的任务成功情况和记忆行为。 CCM + GRPO + 蒸馏比 CCM + GRPO 更频繁地更新其内存，分别为 36.9% 和 16.9%，并且保留了较小的前一个内存前缀（分别为 72.9% 和 94.6%）。蒸馏增强策略还保持了更大的内存，平均为 144.0 个词元，最多为 906 个词元，而 CCM + GRPO 的平均为 77.1 个词元，最多为 720 个词元。我们省略了峰值提示统计数据，因为在此基准中终端观察本身可能非常大，我们为所有条件设置了上下文长度的截止限制，并且每个条件至少在一个情节中达到此限制。由于 CCM 管理保留的交互历史记录，但不压缩最新的观察，因此这些提示大小的统计数据并不能清楚地测量智能体保留的记忆量，而是由长观察和我们对其长度的硬截止限制主导。

### 4.4 一般能力保留

先前的工作表明，同政策蒸馏可以提高任务性能，同时减少对现有功能的遗忘（[Shenfeld et al., 2026](https://arxiv.org/html/2609.35540#bib.bib33); [Ye et al., 2026](https://arxiv.org/html/2609.35540#bib.bib20)）。我们研究了在 CCM 下的智能体训练过程中，特权全历史蒸馏是否能提供比单独使用 GRPO 类似的好处。为了衡量保留率，我们评估了 MMLU-Pro、HellaSwag 和 IFEval 上的预训练基础模型和检查点 100/60 (WebShop/Endless Terminal) 策略。表 [4](https://arxiv.org/html/2609.35540#S4.T4“表 4 ‣ 4.4 通用能力保留 ‣ 4 通过强化学习改进连续上下文管理 ‣ 连续上下文管理”）报告了三个解码种子的平均分数。

表 4：智能体培训后的一般能力保留情况。值是三个解码种子的平均百分比分数，带有样本标准差。括号报告相对于相应预训练基础模型的绝对百分比变化，在舍入之前计算。

|  |  |  |  |
| ---| ---| ---| ---|
|方法| MMLU-专业版 |海拉斯瓦格 | IFEval 严格 |
| *WebShop，Qwen3-4B-Instruct* | | | |
| Pretrained base | 65.25±0.6665.25\pm 0.66 | 80.14±0.0780.14\pm 0.07 | 83.30±0.5683.30\pm 0.56 |
| Full-history GRPO | 62.48±0.49​(−2.77)62.48\pm 0.49\;(-2.77) | 67.92±0.42​(−12.22)67.92\pm 0.42\;(-12.22) | 80.35±0.65​(−2.96)80.35\pm 0.65\;(-2.96) |
| CCM + GRPO | 55.16±0.60​(−10.09)55.16\pm 0.60\;(-10.09) | 66.68±0.71​(−13.46)66.68\pm 0.71\;(-13.46) | 82.32±0.47​(−0.99)82.32\pm 0.47\;(-0.99) |
| CCM + GRPO + distillation | 64.23±0.25​(−1.03)64.23\pm 0.25\;(-1.03) | 74.53±0.20​(−5.62)74.53\pm 0.20\;(-5.62) | 83.18±0.49​(−0.12)83.18\pm 0.49\;(-0.12) |
| *WebShop，Qwen3-8B* | | | |
| Pretrained base | 56.88±0.6556.88\pm 0.65 | 79.54±0.3979.54\pm 0.39 | 81.95±1.2381.95\pm 1.23 |
| Full-history GRPO | 54.28±1.00​(−2.60)54.28\pm 1.00\;(-2.60) | 76.68±0.80​(−2.86)76.68\pm 0.80\;(-2.86) | 79.48±1.40​(−2.46)79.48\pm 1.40\;(-2.46) |
| CCM + GRPO | 58.25±0.40​(+1.37)58.25\pm 0.40\;(+1.37) | 73.94±0.44​(−5.60)73.94\pm 0.44\;(-5.60) | 81.33±0.67​(−0.62)81.33\pm 0.67\;(-0.62) |
| CCM + GRPO + distillation | 56.95±0.25​(+0.07)56.95\pm 0.25\;(+0.07) | 76.71±0.17​(−2.83)76.71\pm 0.17\;(-2.83) | 81.58±1.17​(−0.37)81.58\pm 1.17\;(-0.37) |
| *Endless Terminals，Qwen3-8B* | | | |
| Pretrained base | 56.88±0.6556.88\pm 0.65 | 79.54±0.3979.54\pm 0.39 | 81.95±1.2381.95\pm 1.23 |
| Full-history GRPO | 58.63±0.80​(+1.74)58.63\pm 0.80\;(+1.74) | 79.31±0.42​(−0.23)79.31\pm 0.42\;(-0.23) | 82.44±0.67​(+0.49)82.44\pm 0.67\;(+0.49) |
| CCM + GRPO | 60.61±0.92​(+3.73)60.61\pm 0.92\;(+3.73) | 77.38±0.12​(−2.16)77.38\pm 0.12\;(-2.16) | 82.44±1.33​(+0.49)82.44\pm 1.33\;(+0.49) |
| CCM + GRPO + distillation | 61.75±0.37​(+4.87)61.75\pm 0.37\;(+4.87) | 78.48±0.79​(−1.06)78.48\pm 0.79\;(-1.06) | 82.38±0.56​(+0.43)82.38\pm 0.56\;(+0.43) |

在 WebShop 和 Qwen3-4B-Instruct 上，特权蒸馏大大减少了与 CCM + GRPO 相关的降解。相对于预训练模型，MMLU-Pro、HellaSwag 和 IFEval 上的蒸馏增强策略变化了 -1.03-1.03、-5.62-5.62 和 -0.12-0.12 个百分点。对于WebShop和Qwen3-8B，方法之间的差异较小。相对于 CCM + GRPO，蒸馏提高了 HellaSwag 和 IFEval 保留率，而 CCM + GRPO 获得了最高的 MMLU-Pro 分数。

在Endless Terminals，所有三个训练后策略都比
在 MMLU-Pro 上预训练模型并在 IFEval 上保持接近。 CCM + GRPO
+ 蒸馏获得最高的MMLU-Pro分数并保留更多
HellaSwag 性能优于 CCM + GRPO，而完整历史记录的 GRPO 仍然存在
最接近预训练的 HellaSwag 分数。总体来说，有特权
蒸馏为 4B WebShop 提供了最明显的保留优势
模型。它的效果在模型尺度、训练中并不统一
环境或评估任务。

## 5 讨论与结论

CCM 证明智能体可以使用紧凑、不断更新的记忆进行操作，从而大大减少保留的上下文。特权全历史蒸馏提高了任务准确性，同时减少了一般能力的遗忘，在WebShop和Qwen3-4B-Instruct上具有最明显的联合优势。当模型权重和 KV 缓存争夺有限的 GPU 内存时，例如在消费者 GPU 或支持许多并发智能体会话的服务器上运行的本地智能体，这种方法尤其重要。较小的活动上下文可以在相同的内存预算内容纳更大的模型或更多的并发任务。然而，不同模型和环境的好处各不相同，较短的提示并不一定意味着较低的 API 成本，这取决于前缀缓存和定价策略。

### AI使用声明

生成式人工智能工具协助手稿措辞、LaTeX 格式化以及根据主要来源检查书目元数据。

### 道德声明

这项工作研究了在购物和终端环境中执行操作的智能体的上下文管理。保留记忆中的错误或遗漏可能会影响以后的行动，并且保留记忆可能包含观察中的敏感信息。因此，超出这些基准的应用程序应使用适当的访问控制、数据处理保护措施以及对后续行动的人工监督。报告的基准测试结果并不能证明 CCM 智能体对于不受限制的部署是安全或可靠的。

### 再现性声明

第[3]节(https://arxiv.org/html/2609.35540#S3“3连续上下文管理‣连续上下文管理”)定义了CCM交互协议，第[4]节(https://arxiv.org/html/2609.35540#S4“4通过强化学习改进连续上下文管理‣连续上下文管理”)描述了培训目标。附录[A](https://arxiv.org/html/2609.35540#A1“附录ATerminal-Bench 2.0推理配置‣连续上下文管理”)提供了Terminal-Bench 2.0推理设置、提示模板和词元计费。附录[B](https://arxiv.org/html/2609.35540#A2“附录B GRPO目标‣连续上下文管理”）和[C](https://arxiv.org/html/2609.35540#A3“附录C有关蒸馏目标的详细信息‣连续上下文管理”）指定优化设置和蒸馏目标。附录[E](https://arxiv.org/html/2609.35540#A5“附录E实验细节‣连续上下文管理”)记录了训练和评估分割、奖励、解码设置、推出限制、模型变体和训练框架；附录[E.5](https://arxiv.org/html/2609.35540#A5.SS5“E.5 CCM 提示模板 ‣ 附录 E 实验详细信息 ‣ 连续上下文管理”) 提供了 CCM 提示模板。这些详细信息支持所报告协议的复制，尽管通过托管模型 API 获得的结果可能会因提供商更新而有所不同。

## 附录内容

## 附录A Terminal-Bench 2.0 推理配置

我们在固定的 89 个任务Terminal-Bench 2.0 集上评估 pass@1。基线使用标准 Terminus-2 智能体并每次接收完整的交互历史记录。在 CCM 下，每个提示都包含原始任务、模型在前一回合写入的内存以及最新的终端观察结果。对于所有四个模型，我们使用温度 0.60.6，每轮最多允许生成 8,192 个词元，并将每个任务限制为 50 轮。 CCM 系统提示和每轮输入模板如清单 [1](https://arxiv.org/html/2609.35540#LST1“清单 1 ‣ 附录 A Terminal-Bench 2.0 推理配置 ‣ 连续上下文管理”) 和 [2](https://arxiv.org/html/2609.35540#LST2“清单 2 ‣ 附录 A”) Terminal-Bench 2.0 推理配置 ‣ 连续上下文管理”）。正式任务指令被逐字插入到 {instruction} 字段中。

表 [5](https://arxiv.org/html/2609.35540#A1.T5“表 5 ‣ 附录 A Terminal-Bench 2.0 推理配置 ‣ 连续上下文管理”) 报告 pass@1 性能和累积词元使用情况。词元计数是提供者报告的每个任务的平均值，并对一个情节中的所有模型调用进行求和。 Claude Sonnet 4.6、Claude Opus 4.6 和 Kimi K3 使用提供程序端提示缓存。 GLM-5 在没有提示缓存的情况下进行评估，因为 Amazon Bedrock 不支持此模型。

表 5：详细的 Terminal-Bench 2.0 pass@1 和 89 个任务的平均累积词元使用情况。基线表示完整历史提示。

|  |  |  |  |  |  |  |  |  |
| ---| ---| ---| ---| ---| ---| ---| ---| ---|
|  | Claude Sonnet 4.6 | | Claude Opus 4.6 | | GLM-5 | | Kimi K3 | |
|公制|基线| CCM|基线| CCM|基线| CCM|基线| CCM|
| *评价* | | | | | | | | |
|成功，nn (%) | 38 (42.7) | 38 (42.7) 28（31.5）| 52（58.4）| 36（40.4）| 31 (34.8) | 26 (29.2) | 26 (29.2) | 56（62.9）| 57（64.0）|
|平均匝数| 20.88 | 30.33 | 21.60 | 21.60 26:00 | 25.90 | 25.90 32.50 | 32.50 14.49 | 14.49 19.02 |
| *每个任务的词元* | | | | | | | | |
|未缓存的输入 | 14,955 | 14,955 48,056 | 23,914 | 23,914 86,052 | 86,052 480,325 | 75,481 | 75,481 102 | 102 27,039 | 27,039
|缓存读取输入| 408,900 | 27,135 | 27,135 410,180 | 410,180 0 | – | – | 186,969 | 186,969 20,685 | 20,685
|缓存写入输入| 27,151 | 27,151 936 | 936 30,440 | 30,440 0 | – | – | 14,776 | 1,128 | 1,128
|总投入| 451,006 | 76,126 | 464,533 | 464,533 86,052 | 86,052 480,325 | 75,481 | 75,481 201,846 | 48,852 |
|总产量| 13,265 | 13,265 21,084 | 21,084 12,662 | 12,662 26,286 | 26,286 10,808 | 15,184 | 15,184 12,659 | 12,659 35,354 | 35,354
|缓存读取份额 (%) | 90.7 | 90.7 35.6 | 35.6 88.3 | 88.3 0.0 | 0.0 – | – | 92.6 | 92.6 42.3 | 42.3

[⬇]（数据：文本/纯文本；base64，ICBZb3UgYXJlIGFuIEFJIGFzc2lzdGFudCB0YXNrZWQgd2l0aCBzb2x2aW5nIGNvbW1hbmQtb GluZSB0YXNrcyBpbiBhIExpbnV4IGVudmlyb25tZW50LiBZb3Ugd2lsbCBiZSBnaXZlbiBhIHRhc2sgZGVzY3JpcHRpb24gYW5kC iAgdGhlIG91dHB1dCBmcm9tIHByZXZpb3VzbHkgZXhlY3V0ZWQgY29tbWFuZHMuIFlvdXIgZ29hbCBpcyB0byBzb2x2ZSB0aGUgd GFzayBieSBwcm92aWRpbmcgYmF0Y2hlcyBvZiBzaGVsbCBjb21tYW5kcy4KCiAgSU1QT1JUQU5UIE1FTU9SWSBCRUhBVklPUjogW W91IGhhdmUgYSBzZWxmLW1hbmFnZWQgY29udGV4dCB3aW5kb3cuIFlvdSB3aWxsIG5vdCBzZWUgdGhlIGZ1bGwgcHJldmlvdXMgd HJhamVjdG9yeS4gT24gZWFjaCB0dXJuLAogIHlvdSB3aWxsIHJly2VpdmUgdGhlIHRhc2sgZGVzY3JpcHRpb24sIHlvdXIgcHJld MLVdXMgY29udGV4dF93aW5kb3csIGFuZCB0aGUgbGF0ZXN0IHRlcm1pbmFsIG91dHB1dC4gVXNlIGNvbnRleHRfd2luZG93IHRvc iAgcHJlc2VydmUgZHVyYWJsZSBzdGF0ZSBuZWVkZWQgZm9yIGZ1dHVyZSB0dXJucy4KCiAgRm9ybWF0IHlvdXIgcmVzcG9uc2UgY XMgSlNPTiB3aXRoIHRoZSBmb2xsb3dpbmcgc3RydWN0dXJlOgoKICB7CiAgICAiY29udGV4dF93aW5kb3ciOiAiQ29tcGFjdCBkd XJhYmxlIG1lbW9yeSB0byBjYXJyeSBpbnRvIHRoZSBuZXh0IHR1cm4uIEluY2x1ZGUgdGFzayBnb2FsLCB3b3JraW5nIGRpcmVjd G9yeSwga2V5IGZpbGVzCiAgICBpbnNwZWN0ZWQsIGltcG9ydGFudCBjb21tYW5kIHJlc3VsdHMsIGVkaXRzIG1hZGUsIHRlc3RzI HJ1biwgdW5yZXNvbHZlZCBibG9ja2VycywgYW5kIHZlcmlmaWNhdGlvbiBzdGF0dXMuIERvIG5vdCBpbmNsdWRlIGxvbmcKICAgI HRlcm1pbmFsIHRyYW5zY3JpcHRzIG9yIHByaXZhdGUgcmVhc29uaW5nLiISCiAgICAiYW5hbHlzaXMiOiAiQW5hbHl6ZSB0aGUGY 3VycmVudCBzdGF0ZSBiYXNlZCBvbiB0aGUgdGVybWluYWwgb3V0cHV0IHByb3ZpZGVkLiBXaGF0IGRvIHlvdSBzZWU/IFdoYXQga GFzIGJlZW4gYWNjb21wbGlzaGVkPyBXaGF0CiAgICBzdGlsbCBuZWVkcyB0byBiZSBkb25lPyIsCiAgICAicGxhbiI6ICJEZXNjc mliZSB5b3VyIHBsYW4gZm9yIHRoZSBuZXh0IHN0ZXBzLiBXaGF0IGNvbW1hbmRzIHdpbGwgeW91IHJ1biBhbmQgd2h5PyBCZSBzc GVjaWZpYyBhYm91dCB3aGF0IHlvdSBleHBLY3QgZWFjaAogICAgY29tbWFuZCB0byBhY2NvbXBsaXNoLiIsCiAgICAiY29tbWFuZ HMiOiBbCiAgICAgIHSKICAgICAgICAia2V5c3Ryb2tlcyI6ICJscyAtbGFcbiIsCiAgICAgICAgImR1cmF0aW9uIjogMC4xCiagI CAgIH0sCiagICAgIHSKICAgICAgICAia2V5c3Ryb2tlcyI6ICJjZCBwcm9qZWN0XG4iLAOGICAgICAgICJkdXJhdGlvbiI6IDAuM QogICAgICB9CiAgICBdLAogICAgInRhc2tfY29tcGxldGUIOiB0cnVlCiAgfQoKICBSZXF1aXJlZCBmaWVsZHM6CiagLSAiY29ud GV4dF93aW5kb3ciOiBDb21wYWN0IGR1cmFibGUgbWVtb3J5IHRvIGNhcnJ5IGludG8gdGhlIG5leHQgdHVybi4gSW5jbHVkZSB0Y XNrIGdvYWwsIHdvcmtpbmcgZGlyZWN0b3J5LCBrZXkgZmlsZXMKICBpbnNwZWN0ZWQsIGltcG9ydGFudCBjb21tYW5kIHJlc3Vsd HMsIGVkaXRzIG1hZGUsIHRlc3RzIHJ1biwgdW5yZXNvbHZlZCBibG9ja2VycywgYW5kIHZlcmlmaWNhdGlvbiBzdGF0dXMuIERvI G5vdCBpbmNsdWRlIGxvbmcKICB0ZXJtaW5hbCB0cmFuc2NyaXB0cywgcHJpdmF0ZSByZWFzb25pbmcsIG9yIHNwZWN1bGF0aXZlI HBsYW5zLgogIC0gImFuYWx5c2lzIjogWW91ciBhbmFseXNpcyBvZiB0aGUgY3VycmVudCBzaXR1YXRpb24KICAtICJwbGFuIjogW W91ciBwbGFuIGZvciB0aGUgbmV4dCBzdGVwcwogIC0gImNvbW1hbmRzIjogQXJyYXkgb2YgY29tbWFuZCBvYmplY3RzIHRvIGV4Z WN1dGUKCiAgT3B0aW9uYWwgZmllbGRzOgogIC0gInRhc2tfY29tcGxldGUIOiBCb29sZWFuIGluZGljYXRpbmcgaWYgdGhlIHRhc 2sgaXMgY29tcGxldGUKCiAgQ29tbWFuZCBvYmplY3Qgc3RydWN0dXJlOgogIC0gImtleXN0cm9rZXMiOiBTdHJpbmcgY29udGFpb mluZyB0aGUgZXhhY3Qga2V5c3Ryb2tlcyB0byBzZW5kIHRvIHRoZSB0ZXJtaW5hbCAocmVxdWlyZWQpCiAgLSAiZHVyYXRpb24iO iBOdW1iZXIgb2Ygc2Vjb25kcyB0byB3YWl0IGZvciB0aGUGY29tbWFuZCB0byBjb21wbGV0ZSBiZWZvcmUgdGhlIG5leHQgY29tb WFuZCB3aWxsIGJlIGV4ZWN1dGVkIChkZWZhdWx0cyB0byAxLjAgaWYKICBub3QgcHJlc2VudCkKCiAgSU1QT1JUQU5UOiBUaGUgd GV4dCBpbnNpZGUgImtleXN0cm9rZXMiIHdpbGwgYmUgdXNlZCBjb21wbGV0ZWx5IHZlcmJhdGltIGFzIGtleXN0cm9rZXMuIFdyaXRlIGNvbW1hbmRzIGV4YWN0bHkgYXMgeW91IHdhbnQgdGhlbQogIHNlbnQgdG8gdGhlIHRlcm1pbmFsOgogIC0gWW91IG11c3QgZW5kIGV2ZXJ5IGNvbW 1hbmQgd2l0aCBhIG5ld2xpbmUgKFxuKSBvciBpdCB3aWxsIG5vdCBleGVjdXRlLgogIC0gRm9yIHNwZWNpYWwga2V5IHNlcXVlbmNlcywgdXNlIHRtdXgt c3R5bGUgZXNjYXBlIHNlcXVlbmNlczoKICAgIC0gQy1jIGZvciBDdHJsK0MKICAgIC0gQy1kIGZvciBDdHJsK0QKCiAgVGhlICJkdXJhdGlvbiIgYXR0c mlidXRlIHNwZWNpZmllcyB0aGUgbnVtYmVyIG9mIHNly29uZHMgdG8gd2FpdCBmb3IgdGhlIGNvbW1hbmQgdG8gY29tcGxldGUgKGRlZmF1bHQ6IDEuMCk gYmVmb3JlIHRoZSBuZXh0CiAgY29tbWFuZCB3aWxsIGJlIGV4ZWN1dGVkLiBPbiBpbW1lZGlhdGUgdGFza3MgKGUuZy4signkLCBscywgZWNobywgY2F0 KSBzZXQgYSBkdXJhdGlvbiBvZiAwLjEgc2Vjb25kcy4gT24gY29tbWFuZHMgKGUuZy4sIGdjYywKICBmaW5kLCBydXN0Yykgc2V0IGEgZHVyYXRpb24gb2 YGMS4wIHNly29uZHMuIE9uIHNsb3cgY29tbWFuZHMgKGUuZy4sIG1ha2UsIHB5dGhvbjMgW2xvbmcgcnVubmluZyBzY3JpcHRdLCB3Z2V0IFtmaWxlXSk gc2V0IGFuCiAgYXBwcm9wcmlhdGUgZHVyYXRpb24gYXMgeW91IGRldGVybWluZSBuZWNlc3NhcnkuCgogIEl0IGlzIGJldHRlciB0byBzZXQgYSBzbWFsb GVyIGR1cmF0aW9uIHRoYW4gYSBsb25nZXIgZHVyYXRpb24uIEl0IGlzIGFsd2F5cyBwb3NzaWJsZSB0byB3YWl0IGFnYWluIGlmIHRoZSBwcmlvciBvdX RwdXQgaGFzIG5vdAogIGZpbmlzaGVkLCBieSBydW5uaW5nIHsia2V5c3Ryb2tlcyI6ICIiLCAiZHVyYXRpb24iOiAxMC4wfSBvbiBzdWJzZXF1ZW50IHJl CXVlc3RzIHRvIHDhaXQgbG9uZ2VyLiBOZXZlciB3YWl0IGxvbmdlciB0aGFuIDYwCiAgc2Vjb25kczsgcHJlZmVyIHRvIHBvbGwgdG8gc2VlIGludGVyb WVkaWF0ZSByZXN1bHQgc3RhdHVzLgoKICBJbXBvcnRhbnQgbm90ZXM6CiAgLSBFYWNoIGNvbW1hbmQncyBrZXlzdHJva2VzIGFyZSBzZW50IGV4YWN0bHk gYXMgd3JpdHRlbi4KICATIERvIG5vdCBpbmNsdWRlIGV4dHJhIHdoaXRlc3BhY2UgYmVmb3JlIG9yIGFmdGVyIHRoZSBrZXlzdHJva2VzIHVubGVzcyBp DCBpcyBwYXJ0IG9mIHRoZSBpbnRlbmRlZCBjb21tYW5kLgogIC0gRXh0cmEgdGV4dCBiZWZvcmUgb3IgYWZ0ZXIgdGhlIEpTT04gd2lsbCBnZW5lcmF0ZS B3YXJuaW5ncyBidXQgYmUgdG9sZXJhdGVkLgogIC0gVGhlIEpTT04gbXVzdCBiZSB2YWxpZDsgdXNlIHByb3BlciBlc2NhcGluZyBmb3IgcXVvdGVzIGF uZCBzcGVjaWFsIGNOYXJhY3RlcnMgd2l0aGluIHN0cmluZ3MuCiAgLSBUaGUGY29tbWFuZHMgYXJyYXkgY2FuIGJlIGVtcHR5IHdoZW4gd2FpdGluZy4=)

您是一名 AI 助手，负责在 Linux 环境中解决命令行任务。您将获得任务描述和

先前执行的命令的输出。您的目标是通过提供批量 shell 命令来解决任务。

重要的内存行为：您有一个自我管理的上下文窗口。您将看不到之前的完整轨迹。每回合，

您将收到任务描述、之前的context\_window,以及最新的终端输出。使用 context\_window 来

保留未来回合所需的持久状态。

将您的响应格式化为具有以下结构的 JSON：

{

"context\_window":“紧凑型持久存储器，可带入下一回合。包括任务目标、工作目录、关键文件

检查、重要的命令结果、所做的编辑、运行的测试、未解决的阻止程序以及验证状态。不包括长

最终记录或私人推理。",

"analysis": "根据提供的终端输出分析当前状态。你看到了什么？已经完成了什么？什么

还需要做吗？”,

"plan": "描述您接下来的步骤的计划。您将运行哪些命令以及为什么？具体说明您对每个命令的期望

命令来完成。",

“命令”：[

{

“击键”：“ls -la\n",

“持续时间”：0.1

},

{

“击键”：“cd project\n",

“持续时间”：0.1

}

],

"task\_complete": 正确

}

必填字段：

- "context\_window": 紧凑耐用的内存可带入下一回合。包括任务目标、工作目录、关键文件

检查、重要的命令结果、所做的编辑、运行的测试、未解决的阻止程序以及验证状态。不包括长

最终记录、私人推理或推测性计划。

- “分析”：您对当前情况的分析

- “计划”：您下一步的计划

- “commands”：要执行的命令对象数组

可选字段：

- "task\_complete": 指示任务是否完成的布尔值

命令对象结构：

- “按键”：包含发送到终端的确切按键的字符串（必需）

- “duration”：在执行下一个命令之前等待命令完成的秒数（默认为 1.0，如果

不存在）

重要提示：“按键”内的文本将完全逐字用作按键。完全按照您想要的方式编写命令

发送到终端：

- 您必须以换行符(\n)结束每个命令，否则它将不会执行。

- 对于特殊的按键序列，请使用 tmux 样式的转义序列：

- C-c 表示 Ctrl+C

- C-d 代表 Ctrl+D

“duration”属性指定在下一个命令之前等待命令完成的秒数（默认值：1.0）

命令将被执行。对于即时任务（例如 cd、ls、echo、cat），将持续时间设置为 0.1 秒。关于命令（例如，gcc、

find, rustc) 设置 1.0 秒的持续时间。对于慢速命令（例如 make、python3 [长时间运行的脚本]、wget [文件]），设置

根据您的需要确定适当的持续时间。

设置较小的持续时间比设置较长的持续时间更好。如果先前的输出尚未输出，则始终可以再次等待

完成后，通过对后续请求运行 {"key Strikes": "", "duration": 10.0} 来等待更长时间。切勿等待超过 60

秒；更喜欢轮询以查看中间结果状态。

重要提示：

- 每个命令的击键均完全按照书面形式发送。

- 不要在击键之前或之后包含额外的空格，除非它是预期命令的一部分。

- JSON 之前或之后的额外文本将生成警告，但可以容忍。

- JSON必须有效；对字符串中的引号和特殊字符使用正确的转义。

- 等待时命令数组可以为空。

列表 1：用于所有四个 TerminalBench-2 型号的 CCM 系统提示。

[⬇]（数据：文本/纯文本；base64，ICBUYXNrIERlc2NyaXB0aW9uOgogIHtpbnN0cnVjdGlvbn0KCiAgUHJldmlvdX MgY29udGV4dF93aW5kb3c6CiAge2NvbnRleHRfd2luZG93IG9yICIoZW1wdHKpIn0KCiAgQ3VycmVudCB0ZXJtaW5 hbCBzdGF0ZToKICBMYXRlc3QgVGVybWluYWwgT3V0chHV0OgogIHtsYXRlc3RfdGVybWluYWxfb3V0cHV0IG9yICIo bm9uZSB5ZXQpIn0KCiAgUmV0dXJuIHRoZSByZXF1aXJlZCBKU09OIG9iamVjdCBmb3IgdGhlIG5leHQgdHVybi4=)

任务描述：

{说明}

上一页context\_window:

{context\_window 或“（空）”}

当前终端状态：

最新终端输出：

{latest\_terminal\_output 或“（还没有）”}

返回下一回合所需的 JSON 对象。

清单 2：CCM 每回合输入模板。大括号字段由当前任务状态填充。

## 附录 B GRPO 目标

对于每项任务，GRPO 对一组 GG 学生轨迹进行采样并计算组归一化环境优势，

|  |  |  |  |
| --- | --- | --- | --- |
|  | A(i)=R(i)−μRσR+εstd.A^{(i)}=\frac{R^{(i)}-\mu\_{R}}{\sigma\_{R}+\varepsilon\_{\mathrm{std}}}. |  | (4) |

使用重要性比

|  |  |  |  |
| --- | --- | --- | --- |
|  | rt(i)=πθ​(yt(i)∣st(i))πθold​(yt(i)∣st(i)),r^{(i)}\_{t}=\frac{\pi\_{\theta}\bigl(y^{(i)}\_{t}\mid s^{(i)}\_{t}\bigr)}{\pi\_{\theta\_{\mathrm{old}}}\bigl(y^{(i)}\_{t}\mid s^{(i)}\_{t}\bigr)}, |  | (5) |

修剪后的政策目标是

|  |  |  |  |
| --- | --- | --- | --- |
|  | LPG=−Agg⁡[min⁡(rt(i)​A(i),clip⁡(rt(i),1−ϵ,1+ϵ)​A(i))],L\_{\mathrm{PG}}=-\operatorname{Agg}\Bigl[\min\bigl(r^{(i)}\_{t}A^{(i)},\,\operatorname{clip}(r^{(i)}\_{t},1-\epsilon,1+\epsilon)\,A^{(i)}\bigr)\Bigr], |  | (6) |

其中 Agg\operatorname{Agg} 表示有效学生生成标记的屏蔽标记平均值。我们的实现还使用双重裁剪来获得足够的负面优势。参考策略正则化器应用为

|  |  |  |  |
| --- | --- | --- | --- |
|  | LrefKL=Agg[DKL(πθ(⋅∣st)∥πref(⋅∣st))],L\_{\mathrm{refKL}}=\operatorname{Agg}\Bigl[D\_{\mathrm{KL}}\bigl(\pi\_{\theta}(\cdot\mid s\_{t})\,\|\,\pi\_{\mathrm{ref}}(\cdot\mid s\_{t})\bigr)\Bigr], |  | (7) |

使用采样 KL 估计器实现。

### B.1 优化超参数

表 [6](https://arxiv.org/html/2609.35540#A2.T6“表 6 ‣ B.1 优化超参数 ‣ 附录 B GRPO 目标 ‣ 连续上下文管理”) 报告共享优化配置。 CCM + GRPO 和 CCM + GRPO + Distillation 使用相同的 GRPO 超参数。后者还执行特权全历史教师评分并应用蒸馏损失。其蒸馏特定的超参数是λdistill=0.01\lambda\_{\mathrm{distill}}=0.01和β=5\beta=5.

表 6：用于WebShop 和 Endless Terminals 的优化超参数。

|  |  |  |
| --- | --- | --- |
|超参数| WebShop | Endless Terminals |
|训练步骤| 100 | 100 60|
|每步任务 | 32 | 32 32 | 32
|每个任务的推出 | 8 | 8 |
|每步轨迹 | 256 | 256 256 | 256
| PPO 小批量尺寸 | 32 | 32 32 | 32
|每个 GPU 的微批量大小 | 1 | 1 |
| PPO 时代 | 1 | 1 |
| Learning rate | 1×10−61\times 10^{-6} | 1×10−61\times 10^{-6} |
| LR时间表|恒定|恒定|
|热身步骤| 0 | 0 |
|亚当·贝塔斯 | (0.9,0.999)(0.9,0.999) | (0.9,0.999) (0.9,0.999)(0.9,0.999) | (0.9,0.999)
|体重衰减| 0.01 | 0.01 0.01 | 0.01
|渐变裁剪| 1.0 | 1.0 |
| PPO 剪辑比率 | 0.2 | 0.2 0.2 | 0.2
|双削波系数| 3.0 | 3.0 |
|熵系数| 0.001 | 0.001 0.0 | 0.0
|参考-KL系数| 0.01 | 0.01 0.01 | 0.01
| KL 估计器 |低方差 |低方差 |
| Context-SDAR coefficient λ\lambda | 0.01 | 0.01 |
| Gate sharpness β\beta | 5.0 | 5.0 |

## 附录 C 有关蒸馏目标的详细信息

本节解释了我们对 SDAR（[Lu et al., 2026](https://arxiv.org/html/2609.35540#bib.bib27)）目标的选择，推导其梯度，并建立其与策略蒸馏 (OPD) 的联系。自始至终，教师概率都是使用特权全历史条件根据学生生成的动作标记进行评估的。蒸馏目标监督动作词元，而 GRPO 为内存和动作生成提供任务级监督。

＃＃＃＃＃ 动机。

完整的交互历史记录提供了学生紧凑记忆中可能缺失的信息。因此，比较这两种情况下相同动作标记的概率为全历史条件下偏好的行为提供了训练信号。教师是学生初始模型的冻结副本，在整个训练过程中权重保持固定；不保证比更新后的学生更强。获得完整的历史记录并不能保证每个教师的判断都是正确的，师生概率差距大并不一定表明监督的比例可靠。

因此，我们采用 SDAR 的间隙门控蒸馏目标（[Lu et al., 2026](https://arxiv.org/html/2609.35540#bib.bib27)）。它将教师与学生的对数概率差距转换为有界门控权重，允许全历史指导来调节词元级似然梯度，同时保留 GRPO 作为任务级目标。该门赋予在全历史条件下分配更高概率的词元更大的权重，并限制与极端概率不一致相关的梯度乘数。这个选择并没有直接最小化反向KL；它与 OPD 的关系如下所示。

##### 目标和实现的梯度。

让

|  |  |  |
| --- | --- | --- |
|  | ℓi,n,tS​(θ)=log⁡πθ​(ai,n,t∣si,n,tC),ℓi,n,tT=log⁡πθ0​(ai,n,t∣si,n,t+),\ell^{S}\_{i,n,t}(\theta)=\log\pi\_{\theta}(a\_{i,n,t}\mid s^{C}\_{i,n,t}),\qquad\ell^{T}\_{i,n,t}=\log\pi\_{\theta\_{0}}(a\_{i,n,t}\mid s^{+}\_{i,n,t}), |  |

其中θ0\theta\_{0}表示学生训练前的初始参数。在整个训练过程中，教师权重固定为θ0\theta\_{0}。学生和教师的概率在相同的采样动作标记上进行评估，分别以紧凑上下文和特权全历史上下文为条件。教师分数与梯度计算无关。

我们将独立对数概率间隙和门控权重定义为

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Δi,n,t\displaystyle\Delta\_{i,n,t} | =sg⁡[ℓi,n,tT−ℓi,n,tS​(θ)],\displaystyle=\operatorname{sg}\!\left[\ell^{T}\_{i,n,t}-\ell^{S}\_{i,n,t}(\theta)\right], |  | (8) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | gi,n,t\displaystyle g\_{i,n,t} | =sg⁡[σ⁡(β​Δi,n,t)],\displaystyle=\operatorname{sg}\!\left[\sigma(\beta\Delta\_{i,n,t})\right], |  | (9) |

其中sg\operatorname{sg}表示停止梯度，σ\sigma是逻辑S形，β>0\beta>0控制门锐度。让 Mi,n,tM\_{i,n,t} 指示具有可用学生和教师分数的有效操作标记，并让 Z=∑i,n,tMi,n,tZ=\sum\_{i,n,t}M\_{i,n,t}. 对于 Z>0Z>0 的采样批次，蒸馏损失为

|  |  |  |  |
| --- | --- | --- | --- |
|  | Ldistill(θ)=−1Z∑i,n,tMi,n,tgi,n,tℓi,n,tS(θ).L\_{\mathrm{distill}}(\theta)=-\frac{1}{Z}\sum\_{i,n,t}M\_{i,n,t}g\_{i,n,t}\ell^{S}\_{i,n,t}(\theta). |  | (10) |

没有合格行动词元的批次不会造成蒸馏损失。

采样的标记、上下文和掩码在反向传播期间是固定的。因为门权重是分离的，

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∇θLdistill=−1Z∑i,n,tMi,n,tgi,n,t∇θℓi,n,tS(θ).\nabla\_{\theta}L\_{\mathrm{distill}}=-\frac{1}{Z}\sum\_{i,n,t}M\_{i,n,t}g\_{i,n,t}\nabla\_{\theta}\ell^{S}\_{i,n,t}(\theta). |  | (11) |

因此，教师通过门权重影响蒸馏梯度，而不需要通过教师模型提供梯度。正间隙词元具有 gi,n,t>1/2g\_{i,n,t}>1/2,，而负间隙词元具有 gi,n,t<1/2g\_{i,n,t}<1/2. 负间隙词元保留正门控权重，缩小其各自蒸馏梯度的大小，而不是反转其似然梯度方向。这些陈述涉及单个词元梯度；净概率变化还取决于其他词元以及通过共享模型参数进行的 GRPO 更新。

##### 相当于 SDAR 损失。

SDAR 使用加权师生对数概率差来表达其采样词元目标：

|  |  |  |  |
| --- | --- | --- | --- |
|  | L~distill=1Z​∑i,n,tMi,n,t​gi,n,t​[ℓi,n,tT−ℓi,n,tS​(θ)].\widetilde{L}\_{\mathrm{distill}}=\frac{1}{Z}\sum\_{i,n,t}M\_{i,n,t}g\_{i,n,t}\left[\ell^{T}\_{i,n,t}-\ell^{S}\_{i,n,t}(\theta)\right]. |  | (12) |

该表达式与等式不同。 ([10](https://arxiv.org/html/2609.35540#A3.E10“在目标中并实现梯度。‣附录C有关蒸馏目标的详细信息‣连续上下文管理”))

|  |  |  |
| --- | --- | --- |
|  | C=1Z​∑i,n,tMi,n,t​gi,n,t​ℓi,n,tT.C=\frac{1}{Z}\sum\_{i,n,t}M\_{i,n,t}g\_{i,n,t}\ell^{T}\_{i,n,t}. |  |

由于教师分数和门控权重都是分离的，因此 CC 的反向传播梯度为零。因此，这两个表达式在同一批次上产生相同的蒸馏梯度。我们从显示的目标中省略 CC，以使加权似然更新更加明确。这是关于给定更新时反向传播的声明：当重新计算分数或门时，CC 的数值可能会发生变化。

##### OPD 中的反向 KL 梯度。

要将本地词元更新与 OPD 进行比较，请修复学生上下文 ss 及其相应的特权上下文 s+s^{+}。写

|  |  |  |
| ---| ---| ---|
|  | pθ​(a)=πθ​(a∣s),q⁡(a)=πθ0​(a∣s+),δθ​(a)=log⁡q⁡(a)−log⁡pθ​(a).p\_{\theta}(a)=\pi\_{\theta}(a\mid s),\qquad q(a)=\pi\_{\theta\_{0}}(a\mid s^{+}),\qquad\delta\_{\theta}(a)=\log q(a)-\log p\_{\theta}(a). |  |

这里 qq 是固定的，并且假设两个分布都对所考虑的词元支持为正。

在这些固定的背景下，反向 KL 目标是

|  |  |  |  |
| ---| ---| ---| ---|
|  | JRKL(θ)=DKL(pθ∥q)=∑apθ(a)[logpθ(a)−logq(a)].J\_{\mathrm{RKL}}(\theta)=D\_{\mathrm{KL}}(p\_{\theta}\|q)=\sum\_{a}p\_{\theta}(a)\left[\log p\_{\theta}(a)-\log q(a)\right]. |  | (13) |

对概率权重和对数概率求微分可以得出

|  |  |  |  |  |
| ---| ---| ---| ---| ---|
|  | ∇θJRKL\displaystyle\nabla\_{\theta}J\_{\mathrm{RKL}} | =∑a∇θpθ​(a)​[log⁡pθ​(a)−log⁡q⁡(a)+1]\displaystyle=\sum\_{a}\nabla\_{\theta}p\_{\theta}(a)\left[\log p\_{\theta}(a)-\log q(a)+1\right] |  | (14) |
|  |  |  |  |  |
| ---| ---| ---| ---| ---|
|  |  | =−𝔼a∼pθ​[δθ​(a)​∇θ​log⁡pθ​(a)].\displaystyle=-\mathbb{E}\_{a\sim p\_{\theta}}\left[\delta\_{\theta}(a)\nabla\_{\theta}\log p\_{\theta}(a)\right]. |  | (15) |

常数项消失是因为

|  |  |  |  |
| ---| ---| ---| ---|
|  | 𝔼a∼pθ[∇θlogpθ(a)]=∇θ∑apθ(a)=0.\mathbb{E}\_{a\sim p\_{\theta}}\left[\nabla\_{\theta}\log p\_{\theta}(a)\right]=\nabla\_{\theta}\sum\_{a}p\_{\theta}(a)=0. |  | (16) |

因此，OPD 使用带符号的对数概率间隙作为负似然梯度的系数。

##### 预期 SDAR 更新及其与 OPD 的连接。

对于在固定上下文中从当前学生采样的标记 aa，反向传播的 SDAR 梯度为

|  |  |  |
| ---| ---| ---|
|  | G^SDAR​(θ,a)=−σ⁡(β​δθ​(a))​∇θ​log⁡pθ​(a).\widehat{G}\_{\mathrm{SDAR}}(\theta;a)=-\sigma(\beta\delta\_{\theta}(a))\nabla\_{\theta}\log p\_{\theta}(a). |  |

将其期望定义为

|  |  |  |  |
| ---| ---| ---| ---|
|  | GSDAR​(θ)=𝔼a∼pθ​[G^SDAR​(θ,a)].G\_{\mathrm{SDAR}}(\theta)=\mathbb{E}\_{a\sim p\_{\theta}}\left[\widehat{G}\_{\mathrm{SDAR}}(\theta;a)\right]. |  | (17) |

这是所实现的采样词元梯度的期望。不应将其与完全区分采样词元损失的当前策略期望相混淆，这将引入额外的采样分布项。

使用方程式 （[16](https://arxiv.org/html/2609.35540#A3.E16“在OPD中的反向KL梯度中。‣附录C有关蒸馏目标的详细信息‣连续上下文管理”）），我们可以从门权重中减去1/21/2而不改变预期梯度：

|  |  |  |  |  |
| ---| ---| ---| ---| ---|
|  | GSDAR\displaystyle G\_{\mathrm{SDAR}} | =−𝔼a∼pθ​[(σ⁡(β​δθ​(a))−12)​∇θ​log⁡pθ​(a)]\displaystyle=-\mathbb{E}\_{a\sim p\_{\theta}}\left[\left(\sigma(\beta\delta\_{\theta}(a))-\frac{1}{2}\right)\nabla\_{\theta}\log p\_{\theta}(a)\right] |  | (18) |
|  |  |  |  |  |
| ---| ---| ---| ---| ---|
|  |  | =−12​𝔼a∼pθ​[tanh⁡(β​δθ​(a)2)​∇θ​log⁡pθ​(a)].\displaystyle=-\frac{1}{2}\mathbb{E}\_{a\sim p\_{\theta}}\left[\tanh\!\left(\frac{\beta\delta\_{\theta}(a)}{2}\right)\nabla\_{\theta}\log p\_{\theta}(a)\right]. |  | (19) |

因此，预期 OPD 和 SDAR 梯度中的有效词元权重为

|  |  |  |  |
| ---| ---| ---| ---|
|  | wOPD​(δ)=δ,wSDAR​(δ)=σ⁡(β​δ)−12=12​tanh⁡(β​δ/2).w\_{\mathrm{OPD}}(\delta)=\delta,\qquad w\_{\mathrm{SDAR}}(\delta)=\sigma(\beta\delta)-\frac{1}{2}=\frac{1}{2}\tanh(\beta\delta/2). |  | (20) |

居中的 SDAR 权重是单调的，与 δ\delta, 具有相同的符号，并且范围在 -1/2-1/2 和 1/21/2 之间。因此，它保留了标记级教师偏好的符号和顺序，同时压缩了它们的大小。尽管实现的门是正的，但其预期的策略梯度承认这种等效的有符号表示。

对于 |β​δ|≪1|\beta\delta|\ll 1，泰勒展开式给出

|  |  |  |  |
| ---| ---| ---| ---|
|  | wSDAR​(δ)=β4​δ+O⁡((β​δ)3).w\_{\mathrm{SDAR}}(\delta)=\frac{\beta}{4}\delta+O\!\left((\beta\delta)^{3}\right). |  | (21) |

当这种近似适用于对期望有贡献的词元时，

|  |  |  |  |
| ---| ---| ---| ---|
|  | GSDAR(θ)≈β4∇θDKL(pθ∥q).G\_{\mathrm{SDAR}}(\theta)\approx\frac{\beta}{4}\nabla\_{\theta}D\_{\mathrm{KL}}(p\_{\theta}\|q). |  | (22) |

因此，预期的 SDAR 更新在局部接近缩放的 OPD 梯度，以获得足够小的对数概率间隙。对于大间隙，有效权重会饱和而不是线性增长。由于这种变换非线性地重新加权标记，因此合计 SDAR 和 OPD 梯度不需要具有远离小间隙状态的相同方向。

##### 连接的范围。

中心恒等式和局部近似表征了从当前学生分布中采样的固定上下文中的词元更新。它们不通过记忆的生成、先前的动作标记或访问的环境历史的分布来区分。他们也没有为完整的训练过程建立精确的反向 KL 最小化。

实际上，推出是由行为策略快照生成的，并且可以在参数更新后重用。如果没有适当的采样校正，则精确的策略同一性不需要保持。通过随机数量的合格词元进行依赖于词元的过滤和标准化也可以改变预期的批次梯度。因此，推导表征了局部蒸馏更新；它没有为完全屏蔽轨迹损失建立确切的身份。

最后，减去 1/21/2 可以保留指定假设下的预期梯度，但通常会更改有限批量梯度。我们的实现保留了正 sigmoid 门；居中仅用于分析。有界门限制了每个 词元 的梯度乘数，而不是底层模型梯度的范数，并且不能保证单调 KL 减少或任务改进。

## 附录 D 其他消融结果

### D.1 不使用 GRPO 的蒸馏

我们评估辅助特权蒸馏是否可以在没有伴随的 GRPO 目标的情况下训练 CCM 策略。这些运行保留了学生动作标记的相同轨迹特权全历史评分，但将 GRPO 损失权重设置为零。由于蒸馏目标仅对动作标记进行操作，因此在这种情况下，记忆标记不会接收直接的训练信号。

表 7：固定 128 项任务WebShop 评估的纯蒸馏消融。两个模型均在 CCM 下的检查点 100 处进行评估。部分分数是满足WebShop约束的平均百分比。

|  |  |  |  |  |
| ---| ---| ---| ---| ---|
|型号|成功 (%) |已解决 |部分分数 (%) |转 |
| Qwen3-4B-Instruct | 0.00 | 0.00 0/128 | 0/128 0.59 | 0.59 14.97 | 14.97
| Qwen3-8B | 0.78 | 0.78 1/128 | 1/128 5.27 | 5.27 14.11 | 14.11

如表[7](https://arxiv.org/html/2609.35540#A4.T7“表7‣D.1无GRPO的蒸馏‣附录D附加消融结果‣连续上下文管理”），两者
仅蒸馏策略在检查点的精确成功率几乎为零
100：Qwen3-4B-Instruct 未解决任何任务，而 Qwen3-8B 仅解决其中一项
128. 在这些WebShop实验中，特权动作词元蒸馏
因此不会取代验证者驱动的 GRPO。 GRPO提供
对记忆和动作标记的轨迹级监督，同时
特权蒸馏仅作为辅助目标有效
在主要实验中与 GRPO 一起使用。

## 附录 E 实验细节

### E.1 基准和数据分割

##### WebShop。

我们使用WebShop文本环境和小型产品配置。训练任务是从所有大于或等于 500 的 WebShop 任务 ID 中采样的。评估使用固定的任务 ID 集 0–127。我们训练 100 个策略更新，并使用 pass@1、温度 0.40.4、种子 4242 和 15 轮情节限制分别评估保存的检查点。

我们使用一种形状奖励，将WebShop的部分任务得分与准确完成任务的更大奖励相结合。让rpartial∈[0,1]r\_{\mathrm{partial}}\in[0,1]表示本机WebShop任务分数，让s∈{0,1}s\in\{0,1\}表示完全成功。训练奖励为

|  |  |  |  |
| ---| ---| ---| ---|
|  | RWebShop=2​rpartial+8​s.R\_{\mathrm{WebShop}}=2r\_{\mathrm{partial}}+8s. |  | (23) |

因此，不成功的轨迹根据其部分进度获得 00 到 22 之间的奖励，而完全成功的轨迹则获得 1010 的奖励。

##### Endless Terminals。

我们使用固定的 Endless Terminals 拆分，其中包含 2,083 个训练任务、100 个验证任务和 300 个保留测试任务。培训持续 60 次策略更新。最终结果是通过评估固定 300 任务测试集上保存的检查点（pass@1、种子 4242、温度 0.60.6 和 16 轮情节限制）获得的。环境奖励是二元任务成功。无效动作将受到系数 0.10.1 的辅助惩罚。

### E.2 推出配置

表 [8](https://arxiv.org/html/2609.35540#A5.T8“表 8 ‣ E.2 Rollout 配置 ‣ 附录 E 实验详细信息 ‣ 连续上下文管理”) 总结了 rollout 和序列限制。所有报告的实验都禁用思考。自我管理的学生每次都会发出一个内存块，然后发出一个环境操作块。

表 8：推出和序列长度配置。 WebShop 使用 1,024 个生成词元用于 Qwen3-4B-Instruct，使用 2,048 个生成词元用于Qwen3-8B。

|  |  |  |
| ---| ---| ---|
|超参数| WebShop | Endless Terminals |
|最大转数| 15 | 15 16 | 16
|取样温度| 1.0 | 0.6 | 0.6
|顶页 | 1.0 | 1.0 |
|顶级kk |无限制|无限制|
|学生提示限额| 4,096 | 4,096 16,384 | 16,384
|老师提示限制| 32,768 | 16,384 | 16,384
|每回合生成词元| 1,024 / 2,048 | 4,096 | 4,096
|最大模型长度| 32,768 | 20,480 | 20,480
|思维启用 |没有 |没有 |

### E.3 模型和系统

WebShop实验使用Qwen3-4B-Instruct-2507和Qwen3-8B。 Endless Terminals 实验使用Qwen3-8B。培训是在 verl 中通过 FSDP 策略更新和并置 vLLM 部署生成来实施的。每次运行都使用一个带有四个 H100 或 H200 GPU 的节点。

### E.4 评估

WebShop 检查点评估使用温度 0.40.4、种子 4242 和固定 128 个任务集。 Endless Terminals 使用温度 0.60.6、种子 4242 和固定 300 任务保留测试集。

### E.5 CCM 提示模板

以下列表重现了用于连续上下文管理的提示。 WebShop 使用单个每回合提示，其中包含任务、保留记忆、当前观察和可接受的操作。无尽终端使用固定的系统提示，后面是作为单独用户消息的原始任务和包含保留内存和最新终端观察的每轮用户消息。大括号字段在运行时填充。

清单 3：WebShop CCM 每回合提示模板。

[⬇]（数据：文本/纯文本；base64，ICBZb3UgYXJlIGFuIGV4cGVydCBhdXRvbm9tb3VzIGFnZW50IG9wZXJhdGluZyB pbiB0aGUgV2ViU2hvcCBlLWNvbW1lcmNlIGVudmlyb25tZW50LgogIFlvdXIgdGFzayBpcyB0bzoge3Rhc2tfZGVzY 3JpcHRpb259LgoKICBNRU1PUlk6CiAgLSBNZW1vcnkgaXMgdGhlIHBblcnNpc3RlbnQgcmVjb3JkIG9mIHVzZWZ1bCB pbmZvcm1hdGlvbiBmcm9tIGVhcmxpZXIgc2hvcHBpbmcKICAgIHR1cm5zLiBUaGUgb3JpZ2luYWwgdGFzayBpcyBhbH dheXMgc2hvd24gc2VwYXJhdGVseS4KICAtIFlvdXIgcHJldmlvdXMgYWNjZXB0ZWQgbWVtb3J5IGFwcGVhcnMgYmVs b3cuIEl0IGlzIGVtchR5IG9uIHRoZSBmaXJzdCB0dXJuLgogIC0gRXZlcnkgcmVzcG9uc2UgbXVzdCBjb250YWluIG V4YWN0bHkgb25lIDxtZW1vcnk+IDwvbWVtb3J5PiBibG9jay4KICAtIEluc2lkZSB0aGF0IGJsb2NrLCByZXRhaW4g Y29uY3JldGUgdGFzayBjb25zdHJhaW50cywgcHJvZHVjdCBldmlkZW5jZSwKICAgIHNlbGVjdGVkIG9wdGlvbnMsIGF uZCB1bnJlc29sdmVkIHJlcXVpcmVtZW50cyB0aGF0IGNvdWxkIGJLIG5lZWRlZCBsYXRlci4KICAtIElmIG5vIHVzZ WZ1bCBpbmZvcm1hdGlvbiBjaGFuZ2VkLCByZXBlYXQgdGhlIHByZXZpb3VzIG1lbW9yeSB1bmNoYW5nZWQuCiAgLSB OZXZlciB3cml0ZSBpbnN0cnVjdGlvbnMsIGxhYmVscywgb3IgZ2VuZXJpYyBmaWxsZXIgaW4gbWVtb3J5LgoKICBQc mV2aW91cyBtZW1vcnk6CiAgPG1lbW9yeT57Y29udGV4dF93aW5kb3d9PC9tZW1vcnk+CgogIFlvdSBhcmUgbm93IGF0 IHN0ZXAge2N1cnJlbnRfc3RlcH0uCiAgWW91ciBjdXJyZW50IG9ic2VydmF0aW9uIGlzOiB7Y3VycmVudF9vYnNlcn ZhdGlvbn0uCiAgWW91ciBhZG1pc3NpYmxlIGFjdGlvbnMgYXJlOgogIFsKICB7YXZhaWxhYmxlX2FjdGlvbnN9CiAg XS4KCiAgV3JpdGUgdGhlIHVwZGF0ZWQgPG1lbW9yeT4gPC9tZW1vcnk+IGJsb2NrLiBUaGVuIGNob29zZSBleGFjdG x5IG9uZSBhZG1pc3NpYmxlCiAgYWN0aW9uIGFuZCB3cml0ZSBpdCBpbnNpZGUgPGFjdGlvbj4gPC9hY3Rpb24+Lg==)

您是在 WebShop 电子商务环境中运营的专家自主智能体。

您的任务是：{task\_description}.

内存：

- 记忆是早期购物中有用信息的持久记录

轮流。原始任务始终单独显示。

- 您之前接受的记忆出现在下面。第一回合时它是空的。

- 每个响应必须恰好包含一个 <memory> </memory> 块。

- 在该块内，保留具体的任务约束、产品证据，

选定的选项以及稍后可能需要的未解决的需求。

- 如果有用的信息没有改变，则重复先前的记忆不变。

- 切勿在内存中写入指令、标签或通用填充符。

以前的记忆：

<memory>{context\_window}</memory>

您现在处于步骤{current\_step}.

您当前的观察结果是：{current\_observation}.

您可接受的行为是：

[

{available\_actions}

]。

写入更新后的 <memory> </memory> 块。然后准确选择一项可接受的

动作并将其写入<action></action>。

清单 4：Endless Terminals CCM 系统提示。

[⬇]（数据：文本/纯文本；base64，ICBZb3UgYXJlIGEgaGlnaGx5IGNhcGFibGUgTGludXggdGVybWluYWwgYWdlbnQg b3BlcmF0aW5nIHN0cmljdGx5IHZpYSBhIHNpbmdsZS1zaGVsbC1jb21tYW5kIGludGVyZmFjZS4KICBHb2FsOiBjb21 wbGV0ZSB0aGUgdXNlcidzIHRhc2suCgogIENSSVRJQ0FMIE1FTU9SWSBSRVFVSVJFTUVOVDoKICATIEVWRVJZIFJFU1 BPTlNFIE1VU1QgQkVHSU4gV0lUSCA8bWVtb3J5PiBBTkQgSU5DTFVERSBFWEFDVExZIE9ORSA8L21lbW9yeT4gQ0xPU0 LORyBUQUCuCiagLSBUSElTiElOQ0xVREVTIFRIRSBGSVJTVCBUVVJOLCBFVkVSWSBJTlRFUk1FRElBVEUgVFVSTiwgQ U5EIFRIRSBGSU5BTCBUVVJOLgogIC0gQSBSRVNQT05TRSBDT05UQUlOSU5HIDxjb21tYW5kPiBPUiA8YWN0aW9uPmRvb MU8L2FjdGlvbj4gV0lUSE9VVCA8bWVtb3J5Pi4uLjwvbWVtb3J5PiBJUyBJTlZBTElEIEFORCBXSUxMIE5PVCBFWEVD VVRFLgogIC0gTkVWRVIgT1VUUFVUIEEgQkFSRSBDT01NQU5ELiBZT1VSIEZJULNUIE9VVFBVVCBDSEFSQUNURVJTIE1V U1QgQkU6IDxtZW1vcnk+CgogIFJ1bGVzOgogIC0gRXZlcnkgcmVzcG9uc2UgbXVzdCB1c2UgZXhhY3RseSBvbmUgb2Y gdGhlc2UgdHdvIGZvcm1zOgoKICAgIDxtZW1vcnk+RkFDVFNfVE9fUKVNRU1CRVI8L21lbW9yeT4KICAgIDxjb21tYW 5kPlRIRV9TSU5HTEVfU0hFTExfQ09NTUFORDwvY29tbWFuZD4KCiAgICBPUgoKICAgIDxtZW1vcnk+RkFDVFNfVE9fU kVNRU1CRVI8L21lbW9yeT4KICAgIDxhY3Rpb24+ZG9uZTwvYWN0aW9uPgoKICAtIERvIG5vdCBvdXRwdXQgYSBiYXJlI Dxjb21tYW5kPiBvciA8YWN0aW9uPiBibG9jay4KICATIERvIG5vdCB1c2UgPGNvbW1hbmRfd2luZG93PiBvciBhbnkg b3RoZXIgd3JhchHBlciBuYW1lcy4KICAtIERvbid0IHVzZSBpbnRlcmFjdGl2ZSBjb21tYW5kcyBhbmQgY29uZmlybWF0 AW9uczsgdXNLIG5vbi1pbnRlcmFjdGl2ZSBmbGFncy4KICAtIFByZWZlciBzaW1wbGUsIHJvYnVzdCBDTEkgdG9vbHM 7IHdyaXRlIGZpbGVzIGV4cGxpY2l0bHkgd2hlbiBuZWVkZWQuCiAgLSBJZiB5b3UgYmVsaWV2ZSB0aGUgdGFzayBpcyB zb2x2ZWQsIHVzZSB0aGUgc2Vjb25kIGZvcm0gd2l0aCA8YWN0aW9uPmRvbmU8L2FjdGlvbj4uCiAgLSBIaW50OiB5b3 UgbWlnaHQgd2FudCB0byBydW4gY29tbWFuZHMgaW50ZXJhY3RpdmVseSB0byBzZWUgdGhlIG91dHB1dCBhbmQgdGhlb iB3cml0ZSB0aGUGY29tbWFuZC4gRG9uJ3QganVzdCBwaXBlIHRoZSBjb21tYW5kcy4KICAtIE9ubHkgeW91ciBmaXJz DCBjb21tYW5kIGluIGNvbW1hbmQgdGFncyB3aWxsIGJlIGV4ZWN1dGVkLiBTbyBkb24ndCByZXNwb25kIHdpdGggbXVs dGlwbGUGY29tbWFuZHMuCiAgLSBIaW50OiBWZXJpZnkgeW91ciBzb2x1dGlvbiBvbmNlIHlvdSBhcmUgZG9uZS4gRWc 6IHlvdSBjYW4gdXNlIGNhdCB0byBzZWUgdGhlIGlucHV0IGFuZCB0aGUgb3V0cHV0LgogIC0gRG8gbm90IGp1c3Qgd3J pdGUgbG9uZyBiYXNoIHNjcmlwdHMuIFdyaXRlIHRoZSBjb21tYW5kcyB0aGF0IHlvdSB3b3VsZCB3cml0ZSBpbiBhIH Rlcm1pbmFsLgoKICBJTVBPUlRBTlQgTUVNT1JZIEJFSEFWSU9SOgogIC0gV3JpdGUgaW4gPG1lbW9yeT4gdGhlIGZhY3 RzIGZyb20gdGhlIHRhc2sgYW5kIHRlcm1pbmFsIHdvcmsgdGhhdCBzaG91bGQgYmUgYXZhaWxhYmxlIG9uIHRoZSBuZ Xh0IHR1cm4uCiAgLSBUaGUgbmV4dCB0dXJuIHdpbGwgbm90IHJly2VpdmUgdGhlIGVhcmxpZXIgY29udmVyc2F0aW9u LiBJdCByZWNlaXZlcyBvbmx5IHRoZSBvcmlnaW5hbCB0YXNrLCB5b3VyIGxhdGVzdCBtZW1vcnksIGFuZCB0aGUgbmV 3ZXN0IHRlcm1pbmFsCiAgb2JzZXJ2YXRpb24uCiAgLSBVcGRhdGUgdGhlIG1lbW9yeSBhcyB3b3JrIHByb2dyZXNzZXM gc28gaXQgcmVmbGVjdHMgdGhlIGN1cnJlbnQgZHVyYWJsZSBzdGF0ZS4KICAtIE1lbW9yeSBkZXNjcmliZXMgdGhlIH N0YXRlIGJlZm9yZSB0aGUGY29tbWFuZCBpbiB0aGUgc2FtZSByZXNwb25zZSBleGVjdXRlcy4KICAtIFJly29yZCBjb2 1wbGV0ZWQgd29yayBvbmx5IHdoZW4gY29uZmlybWVkIGJ5IGFuIGVhcmxpZXIgdGVybWluYWwgb2JzZXJ2YXRpb24uC iAgLSBEbyBub3QgZGVzY3JpYmUgdGhlIGFjY29tcGFueWluZyBjb21tYW5kIGFzIGFscmVhZHkgY29tcGxldGVkLg==)

您是一个功能强大的 Linux 终端智能体，严格通过单 shell 命令界面进行操作。

目标：完成用户的任务。

关键内存要求：

- 每条回复都必须以 <memory> 开头，并包含一个 </memory> 结束标签。

- 这包括第一个转弯、每个中间转弯和最后一个转弯。

- 包含 <command> 或 <action>done</action> 而没有 <memory>...</memory> 的响应无效且不会执行。

- 切勿输出裸命令。您的第一个输出字符必须是：<memory>

规则：

- 每个响应都必须使用以下两种形式之一：

<memory>FACTS\_TO\_REMEMBER</memory>

<command>THE\_SINGLE\_SHELL\_COMMAND</command>

或

<memory>FACTS\_TO\_REMEMBER</memory>

<action>完成</action>

- 不要输出裸露的<command>或<action>块。

- 不要使用 <command\_window> 或任何其他包装名称。

- 不要使用交互式命令和确认；使用非交互式标志。

- 喜欢简单、强大的 CLI 工具；需要时显式写入文件。

- 如果您认为任务已解决，请使用第二种形式<action>done</action>。

- 提示：您可能希望以交互方式运行命令以查看输出，然后编写命令。不要只是通过管道传输命令。

- 仅执行命令标签中的第一个命令。所以不要用多个命令来响应。

- 提示：完成后验证您的解决方案。例如：您可以使用 cat 查看输入和输出。

- 不要只编写长的 bash 脚本。编写您将在终端中编写的命令。

重要的记忆行为：

- 在<memory>中写入下一轮应该可用的任务和终端工作的事实。

- 下一个回合将不会收到之前的对话。它只接收原始任务、您的最新内存和最新的终端

观察。

- 随着工作的进展更新内存，使其反映当前的持久状态。

- 内存描述了同一响应中的命令执行之前的状态。

- 仅在通过早期终端观察确认时才记录已完成的工作。

- 不要将随附的命令描述为已完成。

在Endless Terminals中，原始任务指令作为单独的用户消息逐字提供。然后每次都会重建以下附加用户消息：

清单 5：Endless Terminals CCM 每回合用户消息模板。

[⬇]（数据：文本/纯文本；base64，ICBQcmV2aW91cyBtZW1vcnk6CiAgPG1lbW9yeT57bWVtb3J5fTwvbWVtb3J5PgoKICBDdXJyZW50IG9i c2VydmF0aW9uOgogIHtvYnNlcnZhdGlvbn0KCiAgUkVTUE9OU0UgUkVRVUlSRU1FTlQ6IEJlZ2luIHlvdXIgcmVzcG9uc2Ugd2l0aCA8bWV tb3J5Pi4gV3JpdGUgdGhlIGNvbXBsZXRlIHVwZGF0ZWQgPG1lbW9yeT4uLi48L21lbW9yeT4gYmxvY2ssIHRoZW4gZXhhY3RseSBvbmUgPG NvbW1hbmQ+Li4uPC8KICBjb21tYW5kPiBvciA8YWN0aW9uPmRvbmU8L2FjdGlvbj4uIE5ldmVyIHJldHVybiBhIGJhcmUgY29tbWFuZC4=)

以前的记忆：

<memory>{内存}</memory>

目前观察：

{观察}

回复要求：以<memory>开始您的回复。写入完整更新的<memory>...</memory>块，然后恰好是一个<command>...</

命令>或<action>完成</action>。切勿返回裸命令。

## 附录 F 定性轨迹分析

我们提出了简洁的匹配轨迹来说明评估条件之间的行为差​​异。对于每个轨迹，我们保留初始转弯、实质上改变保留记忆或环境状态的转弯、每个重复故障模式的第一个实例、最终有效操作以及验证者结果。明确总结具有相同行为的连续转弯。摘录内括号内的省略是编辑性的，仅删除不相关或重复的输出。

### F.1 WebShop

##### 任务。

智能体商必须购买一件价格低于 50 美元的男式衬衫，且满足所要求的材质、版型、袖子、颜色和尺寸限制。配套任务需要棉质氨纶、经典版型、短袖、木炭石南色（浅色）和尺寸 1x。

表 9：匹配的 WebShop 轨迹的结果。 Exact表示任务完全成功；部分是WebShop约束匹配分数。

|  |  |  |  |  |
| ---| ---| ---| ---| ---|
|型号|状况 |准确|部分|转 |
| Qwen3-4B-Instruct |未经训练的完整历史 |没有 | 0.000 | 0.000 15 | 15
|  |未经培训的 CCM |没有 | 0.000 | 0.000 15 | 15
|  | CCM + GRPO |没有 | 0.857 | 0.857 15 | 15
|  | CCM + GRPO + 蒸馏 |是的 | 1.000 | 1.000 5 |
| Qwen3-8B |未经训练的完整历史 |没有 | 0.000 | 0.000 12 | 12
|  |未经培训的 CCM |没有 | 0.000 | 0.000 15 | 15
|  | CCM + GRPO |没有 | 0.857 | 0.857 10 | 10
|  | CCM + GRPO + 蒸馏 |是的 | 1.000 | 1.000 5 |

##### 未经训练的政策。

未经训练的全历史策略反复发出广泛的搜索，但没有达成有效的购买。未经训练的 CCM 策略将任务约束保留在内存中，但继续对不相关的结果进行分页。这两种情况都不会购买满足所请求选项的产品。

##### CCM + GRPO 失败。

对于Qwen3-4B-Instruct，CCM + GRPO 找到目标产品并打开其产品页面。然而，在初始搜索之后，它的内存实际上保持不变：

<memory>

任务：找到可机洗的棉氨纶男士正装衬衫，

经典版型，短袖，颜色：木炭石南色（浅色），

尺寸：1x，价格低于 50.00 美元。

未解决：尚未生成任何搜索或产品选项。

</memory>

<action>点击[b07hrfsnl4]</action>

生成的产品页面公开了两个必需的选项：

大小：[..., 1x, ...]

颜色：[...、木炭石南色（浅色）、...]

Nautica 男式纯色圆领短袖口袋 T 恤

价格：$16.05 to $40.98

立即购买

该策略选择颜色，然后在剩余的中间回合中重复相同的颜色选择操作，而不是选择大小 1x：

<action>点击[木炭石南花（浅色）]</action>

在最后一轮，它购买仅选择颜色的产品。环境分配部分分数 0.8570.857，而不是完全成功：

已购买

阿信：B07HRFSNL4

选项：{“color”：“木炭石南花（浅色）”}

奖励：0.8571428571428571

Qwen3-8B CCM + GRPO 轨迹表现出相同的高级失败：它达到了目标产品，但在没有满足每个所需选项的情况下进行了购买，获得部分分数 0.8570.857。

##### CCM + GRPO + 蒸馏成功。

蒸馏增强的Qwen3-4B-Instruct策略记录了任务约束和交互的当前阶段。它的五个动作形成了所需的搜索-产品-颜色-尺码-购买序列：

第1转：<action>搜索[纯棉男士正装衬衫 纯棉氨纶

 经典版型短袖 炭灰色（浅色）

 尺寸 1x 价格低于 50.00]</action>

第2回合：<action>点击[b07hrfsnl4]</action>

第三回合：<action>点击【木炭石南花（浅）】</action>

第4回合：<action>点击[1x]</action>

第5回合：<action>点击【立即购买】</action>

内存随着选项选择状态而变化。例如，在它记录的 size 操作之前：

<memory>

任务：找到可机洗的棉氨纶男士正装衬衫，

经典版型，短袖，颜色：木炭石南色（浅色），

尺寸：1x，价格低于 50.00 美元。

当前步骤：4（选择尺寸）。

操作：选择尺寸 1x。

选择的尺寸：1x。

满足尺寸限制：是。

</memory>

<action>点击[1x]</action>

最终观察结果证实选择了两个必需的选项：

已购买

阿信：B07HRFSNL4

选项：{“color”：“木炭石南花（浅色）”，“size”：“1x”}

奖励：1.0

Qwen3-8B 遵循相同的五动作顺序。它的内存使用结构化表示来保留约束和选定的操作：

<memory>

{

 “约束”：{

 "type": "男士正装衬衫",

 “材质”：“棉氨纶”，

 "fit": "经典版型",

 "sleeve": "短袖",

 "color": "木炭石南色（浅色）",

 “尺寸”：“1x”，

 "price\_limit": 50.00

 },

 "actions\_taken": [

 “点击[木炭石南花（浅色）]”，

 “点击[1x]”

 ]

}

</memory>

同样，它会购买选择了两个选项的目标产品，并获得确切的奖励 1.0。

### F.2 Endless Terminals

两个Endless Terminals示例揭示了互补的结果：一个仅通过匹配条件中的CCM + GRPO + Distillation来解决，而另一个通过CCM + GRPO来解决，但不通过蒸馏增强策略来解决。他们还将干净的提前终止与创建验证者有效状态后的持续操作进行了对比。

表 10：两条匹配的 Endless Terminals 轨迹的结果。

|  |  |  |  |
| ---| ---| ---| ---|
|任务|状况 |成功|转 |
| 4d41da7b | 4d41da7b未经训练的完整历史 |没有 | 2 |
|  |未经培训的 CCM |没有 | 2 |
|  | CCM + GRPO |没有 | 16 | 16
|  | CCM + GRPO + 蒸馏 |是的 | 2 |
|贝夫73f4 |未经训练的完整历史 |是的 | 4 |
|  |未经培训的 CCM |没有 | 16 | 16
|  | CCM + GRPO |是的 | 16 | 16
|  | CCM + GRPO + 蒸馏 |没有 | 16 | 16

#### F.2.1 权限审核设置：蒸馏增强 CCM 成功

##### 任务。

智能体必须创建一个 shell 脚本存根，将目录和文件模式分别设置为 750 和 740，并写入包含准确内容的三行权限验证日志。

##### 故障模式。

未经训练的完整历史策略执行几乎所有必需的操作，但从 ls -l 构造第三条日志行。生成的权限字符串包含尾随 SELinux 标记 -rwxr-----.，而不是所需的 -rwxr-----。未经训练的 CCM 策略仅创建目录，然后在内存中记录未执行的文件和日志操作已完成并终止。 CCM + GRPO 最初创建一个有效状态，但其内存保持不变：

<memory>初始状态：尚未执行任何命令。</memory>

它继续发出命令直到第 16 回合，并最终仅用第三行覆盖验证日志。因此，验证者报告该文件包含一行而不是三行。

##### CCM + GRPO + 蒸馏。

蒸馏增强策略通过一个命令执行完整的设置：

<memory>需要创建特定的目录结构和文件

具有特定权限和内容。</memory>

<command>mkdir -p /home/user/project\_utils/secure\_scripts &&

chmod 750 /home/user/project\_utils/secure\_scripts &&

echo -e ’#!/bin/bash\necho "备份脚本存根"’ >

/home/user/project\_utils/secure\_scripts/backup.sh &&

chmod 740 /home/user/project\_utils/secure\_scripts/backup.sh &&

echo -e "$(stat -c "%a %n" /home/user/project\_utils/secure\_scripts)\n\

$(stat -c "%a %n" /home/user/project\_utils/secure\_scripts/backup.sh)\n\

-rwxr----- /home/user/project\_utils/secure\_scripts/backup.sh" >

/home/user/perm\_check.log</command>

观察到零退出代码后，它请求在第 2 回合完成：

<memory>需要创建特定的目录结构和文件

具有特定权限和内容。</memory>

<action>完成</action>

... [100%]

0.01秒内3次通过

该轨迹提供了一个干净的提前终止示例：策略通过一个环境操作达到验证者有效状态，并且不发出任何冗余命令。

#### F.2.2 Git 跟踪文件导出：CCM + GRPO 成功

##### 任务。

智能体必须在/home/user/demo\_repo内查询Git，并按照Git返回的顺序和最后的换行符将所有跟踪路径写入/home/user/git\_files.log.

##### 未经训练的完整历史基线。

在两个命令因在存储库之外运行而失败后，基线更改目录并成功：

<command>cd /home/user/demo\_repo && git ls 文件 |

T 恤/home/user/git\_files.log</command>

自述文件.md

脚本/run.sh

src/main.py

它请求在第 4 回合完成，并且所有五个验证者测试都通过。

##### CCM + GRPO。

第一个 CCM + GRPO 命令也在错误的目录中运行并失败。第二轮更正工作目录并查询Git：

<memory>

初始状态：尚未执行任何命令。

任务：列出/home/user/demo\_repo中跟踪的文件并保存到

/home/user/git\_files.log.

</memory>

<command>cd /home/user/demo\_repo && git ls 文件</command>

命令成功。输出：

自述文件.md

脚本/run.sh

src/main.py

以下内存保存命令结果，策略将三个路径写入请求的文件：

<memory>

任务：列出/home/user/demo\_repo中跟踪的文件并保存到

/home/user/git\_files.log.

git ls-files 的输出：README.md 脚本/run.sh src/main.py

</memory>

<command>echo -e "README.md\nscripts/run.sh\nsrc/main.py" >

/home/user/git\_files.log</command>

第4-16次重复重写相同的有效内容而不是终止。最终状态通过了所有验证者测试：

...... [100%]

0.02秒内5次通过

##### CCM + GRPO + 蒸馏失败。

蒸馏增强策略最初将错误的工作目录误认为是不存在的存储库，并不必要地重新初始化 Git。然后它会重复使用无效的 -n 选项和 git ls-files。尽管第 15 回合最终获得了正确的跟踪路径，但第 16 回合再次使用了无效选项并留下了错误的输出文件。验证程序报告三个失败的测试，包括不正确的内容和缺少尾随换行符。

＃＃＃＃＃ 解释。

这两个例子表明，训练有素的 CCM 目标在每项任务上都不占主导地位。他们还表明，终止行为在不同条件下有很大差异：蒸馏增强策略在权限任务中成功执行操作后立即终止，而 CCM + GRPO 在 Git 任务早期建立正确的状态，但继续发出冗余命令，直到轮数限制。

