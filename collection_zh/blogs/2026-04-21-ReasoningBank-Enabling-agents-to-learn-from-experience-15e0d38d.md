> 本文为简体中文机器翻译，使用 Google Translate 公开接口并统一技术术语，尚未经逐句人工校对。代码、链接和公式按原文保留；实验数字及技术结论请对照原文。
> [查看本地英文原文](../../collection/blogs/2026-04-21-ReasoningBank-Enabling-agents-to-learn-from-experience-15e0d38d.md) · [原始来源](https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/)

# ReasoningBank：让智能体从经验中学习

- 来源: https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/- 发布日期: 2026-04-21- 日期依据: curated source date (verified from source/search)- 类型: blog- 主题: ReasoningBank、经验记忆- 抓取状态: article_html- 正文来源: https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/- 抓取时间 UTC: 2026-10-26T09:41:28.752844+00:00

## 抓取正文（中文翻译）

![ReasoningBank：让智能体能够从经验中学习](https://storage.googleapis.com/gweb-research2023-media/original_images/ReasoningBank-2.png)

# ReasoningBank：使智能体能够从经验中学习

2026 年 4 月 21 日

Jun Yan 和 Chen-Yu Lee，Google Cloud 研究科学家

ReasoningBank 是一种新颖的智能体记忆框架，它使用成功和失败的经验来提炼可推广的推理策略，使智能体能够在部署后不断从经验中学习。

## 快速链接

* [论文](https://arxiv.org/abs/2509.25140)
* [推理库代码](https://github.com/google-research/reasoning-bank)
* + ×

智能体在处理复杂的现实任务中变得越来越重要，从一般的网络导航到协助广泛的软件工程代码库。然而，当这些智能体在现实世界中转变为持久的、长期运行的角色时，他们面临着一个关键的限制：他们很难在部署后分析成功和失败的经验并从中学习。

如果智能体在没有记忆机制的情况下处理每项新任务，就会反复犯同样的策略错误，并放弃有价值的见解。为了解决这个问题，引入了各种形式的智能体记忆来存储有关过去交互的信息以供重用。然而，现有方法通常侧重于保存所采取的每个操作的详尽记录 - 例如 [Synapse](https://arxiv.org/abs/2306.07863) 中使用的轨迹内存 - 或者仅记录从成功尝试中总结的工作流程，如 [智能体工作流程内存](https://arxiv.org/abs/2409.07429)）。这些方法有两个根本缺点：首先，通过记录详细的行动而不是战术预见，它们无法提炼出更高层次的、可转移的推理模式；其次，由于过分强调成功的经验，他们错过了学习的主要来源——自己的失败。

为了弥补这一差距，在我们的 ICLR 论文“[ReasoningBank: Scaling 智能体 Self-Evolving with Reasoning Memory](https://arxiv.org/abs/2509.25140)”中，我们引入了一种新颖的智能体记忆框架 ([github](https://github.com/google-research/reasoning-bank))，该框架从成功和失败的经验中提炼出有用的见解，用于测试时的自我进化。当根据网页浏览和软件工程基准进行评估时，与基线方法相比，ReasoningBank 提高了智能体有效性（更高的成功率）和效率（更少的任务步骤）。

![ReasoningBank-1](https://storage.googleapis.com/gweb-research2023-media/images/ReasoningBank-1.width-1250.png)

*内存内容比较：现有策略和 ReasoningBank。*

## 使用 ReasoningBank 提炼见解

ReasoningBank 将全局推理模式提炼为高级结构化记忆。每个结构化内存项包含以下内容：

* *标题*：总结核心策略的简洁标识符。
* *描述*：内存项目的简短摘要。
* *内容*：从过去的经验中提取的精炼推理步骤、决策理由或操作见解。

记忆工作流程在检索、提取和巩固的连续、闭环中运行。在采取行动之前，智能体利用 ReasoningBank 将相关记忆收集到其上下文中。然后，它与环境进行交互，并使用[LLM作为法官](https://arxiv.org/abs/2306.05685)来自我评估结果轨迹并提取成功见解或失败反思。值得注意的是，这种自我判断不需要完全准确，因为我们发现 ReasoningBank 对于判断噪声非常稳健。在提取过程中，智能体将工作流程和可概括的见解从轨迹中提取到新的记忆中。为简单起见，我们直接将它们附加到 ReasoningBank，为未来的工作留下更复杂的整合策略。

至关重要的是，与现有的仅关注成功运行的[工作流程记忆策略](https://arxiv.org/abs/2409.07429)不同，ReasoningBank 主动分析失败的经验以寻找反事实信号和陷阱。通过将这些错误提炼为预防性教训，ReasoningBank 建立了强大的战略护栏。例如，智能体不仅仅学习“单击‘加载更多’按钮”之类的程序规则，还可以从过去的失败中学习“在尝试加载更多结果之前始终首先验证当前页面标识符，以避免无限滚动陷阱”。

![ReasoningBank-2](https://storage.googleapis.com/gweb-research2023-media/images/ReasoningBank-2.width-1250.png)

*在测试期间 ReasoningBank 的工作流程与智能体集成。*

## 内存感知测试时间缩放 (MaTTS)

[测试时缩放](https://arxiv.org/abs/2408.03314) (TTS)——在推理时缩放计算——在[数学](https://arxiv.org/abs/2501.19393)和[竞争性编程](https://arxiv.org/abs/2502.14382)等推理领域显示出巨大的有效性。然而，在智能体环境中，现有的 TTS 方法通常会放弃探索轨迹，并将最终答案视为唯一有用的结果。这种被忽视的探索实际上是一个丰富的数据源，可以随着时间的推移加速智能体从经验中学习的能力。

我们通过内存感知测试时间缩放（MaTTS）显式地将内存与缩放联系起来，从而弥补了这一差距。通过使用 ReasoningBank 作为强大的经验学习器，MaTTS 通过对比和细化信号将广泛的探索提炼成高质量的记忆。我们通过两种不同形式的缩放来展示 MaTTS 函数的强大功能：

* *并行缩放*：智能体在内存的指导下为同一查询生成多个不同的轨迹。通过自我对比，ReasoningBank 可以比较成功的推理轨迹和虚假的推理轨迹，以提炼出更稳健的策略并合成更高质量的记忆。
* *顺序缩放*：智能体在单个轨迹内迭代地完善推理，以产生强大的中间原理。 ReasoningBank 将这些关于智能体试错和逐步改进的中间见解捕获为高质量的记忆项目。

MaTTS 建立了强大的协同作用：来自 ReasoningBank 的高质量记忆引导规模化探索转向更有前景的策略，而作为回报，规模化交互会产生更丰富的学习信号，这些信号反馈到更智能的 ReasoningBank 中以帮助智能体。

![ReasoningBank-3](https://storage.googleapis.com/gweb-research2023-media/images/ReasoningBank-3.width-1250.png)

*内存感知测试时间缩放 (MaTTS) 与 ReasoningBank 的比较。*

## 性能和紧急能力

我们通过涵盖动态环境的具有挑战性的基准对 ReasoningBank 进行了评估。使用 [ReAct](https://arxiv.org/abs/2210.03629) 提示策略作为所有智能体的基础，我们将 ReasoningBank 与三种内存配置进行比较：无内存基线 (Vanilla ReAct)、[Synapse](https://arxiv.org/abs/2306.07863)（轨迹内存）和 [AWM](https://arxiv.org/abs/2409.07429)（工作流内存）。从我们在 [WebArena](https://arxiv.org/abs/2307.13854) 和 [SWE-Bench-Verified](https://openai.com/index/introducing-swe-bench-verified/) 上对 [Gemini-2.5-Flash](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash) 的主要评估结果来看，我们有以下主要观察结果：

* *卓越的成功率*：不进行扩展的 ReasoningBank 在 WebArena 上的性能优于无内存智能体 8.3%，在 SWE-Bench-Verified 上优于无内存智能体 4.6%。
* *效率增益*：由于智能体主动访问过去的决策理由，因此它执行命令时会大大减少漫无目的的探索。在 SWE-Bench-Verified 上，ReasoningBank 在无内存基准上每个任务节省了近 3 个总执行步骤。
* *MaTTS 协同*：当添加 MaTTS（缩放因子 k=5 的并行缩放）时，成功率进一步提高。 ReasoningBank w/ MaTTS 比 ReasoningBank 提高了 3% 的成功率，并且在 WebArena 上减少了 0.4 步。

![ReasoningBank-4](https://storage.googleapis.com/gweb-research2023-media/images/ReasoningBank-4.width-1250.png)

*WebArena 和 SWE-Bench-Verified 上不同智能体记忆策略的性能比较（任务成功率和每个任务的平均步数）。*

重要的是，在评估过程中，我们观察到了战略成熟度的出现。在网络浏览示例中，智能体的初始策划规则类似于简单的程序清单（例如，“查找页面链接”）。随着智能体坚持解决更多的问题集，这些记忆在执行过程中被合并。在现有知识的基础上，智能体将新的轨迹提炼成更高级的记忆。随着时间的推移，简单的清单演变成了具有组合性、预防性逻辑结构的记忆（例如，“使用活动页面过滤器不断交叉引用任务，以确保检索到的数据集不会过早分页”）。更多详情请参阅[论文](https://arxiv.org/abs/2509.25140)。

## 结论

ReasoningBank 提供了一个强大的框架，使法学硕士能够在测试期间从经验中学习并发展成为持续学习者。我们相信内存驱动的体验扩展代表了智能体扩展的一个重要新领域。

我们很高兴与更广泛的研究界分享这一点。

## 致谢

*这项研究由 Siru Ouyang、Jun Yan、I-Hung Hsu、Yanfei Chen、Ke Jiang、Zifeng Wang、Rujun Han、Long T. Le、Samira Daruki、Xiangru Tang、Vishy Tirumalashetty、George Lee、Mahsan Rofouei、Hangfei Lin、Jiawei Han、Chen-Yu Lee 和 Tomas Pfister 进行。*

* 标签：
* [生成式人工智能](https://research.google/blog/label/generative-ai)
* [机器智能](https://research.google/blog/label/machine-intelligence)
* [自然语言处理](https://research.google/blog/label/natural-language-processing)

## 快速链接

* [论文](https://arxiv.org/abs/2509.25140)
* [推理库代码](https://github.com/google-research/reasoning-bank)
* + ×

## 其他感兴趣的帖子

* [![Nexus AI 软件界面显示胸部 X 光片，其中三个圆圈肺部区域标记为“TB 提示”和“FIR”。](https://storage.googleapis.com/gweb-research2023-media/original_images/AIforTBScreening2_Xray.png)

  2026 年 10 月 23 日

  将基础模型带到结核病筛查的第一线

  + 生成式人工智能
    ·
  + 健康与生物科学](https://research.google/blog/bringing-foundational-models-to-the-front-lines-of-tb-screening/)
* [![USS0291-Google 研究圣歌电影_缩略图4 (1)](https://storage.googleapis.com/gweb-research2023-media/original_images/USS0291-Google_Research_Anthem_Film_Thumbnail4_1.jpg)

  2026 年 10 月 14 日

  Research@2026：我们增强人类创造力的 10 种方法

  + 普通科学
    ·
  + 生成式人工智能
    ·
  + 健康与生物科学](https://research.google/blog/research-2026-10-ways-were-amplifying-human-ingenuity/)
* [![深度评论2](https://storage.googleapis.com/gweb-research2023-media/original_images/DeepReview2.jpg)

  2026 年 10 月 14 日

  通过 Deep Review 分析技术文档

  + 普通科学
    ·
  + 机器智能
    ·
  + 自然语言处理](https://research.google/blog/analyzing-technical-documents-with-deep-review/)

× ❮ ❯

![ReasoningBank-2](https://storage.googleapis.com/gweb-research2023-media/original_images/ReasoningBank-2.png)

![ReasoningBank-1](https://storage.googleapis.com/gweb-research2023-media/original_images/ReasoningBank-1.png)

![ReasoningBank-4](https://storage.googleapis.com/gweb-research2023-media/original_images/ReasoningBank-4.png)

![ReasoningBank-3](https://storage.googleapis.com/gweb-research2023-media/original_images/ReasoningBank-3.png)

