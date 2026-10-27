> 本文为简体中文机器翻译，使用 Google Translate 公开接口并统一技术术语，尚未经逐句人工校对。代码、链接和公式按原文保留；实验数字及技术结论请对照原文。
> [查看本地英文原文](../../collection/papers/2025-07-03-MemAgent-Reshaping-Long-Context-LLM-with-Multi-Conv-RL-based-Memory-Agent-a3184b5b.md) · [原始来源](https://arxiv.org/abs/2507.02259)

# MemAgent：通过基于多轮对话强化学习的记忆智能体重塑长上下文大语言模型

- 来源: https://arxiv.org/abs/2507.02259- 发布日期: 2025-07-03- 日期依据: page metadata: citation_date- 类型: paper- 主题: MemAgent、强化学习、压缩记忆- 抓取状态: full_text_html- 正文来源: https://arxiv.org/html/2507.02259- 抓取时间 UTC: 2026-10-26T09:38:09.586112+00:00 - 作者: Yu, Hongli, Chen, Tinghong, Feng, Jiangtao, Chen, Jiangjie, Dai, Weinan, Yu, Qiying, Zhang, Ya-Qin, Ma, Wei-Ying, Liu, Jingjing, Wang, Mingxuan, Zhou, Hao

## 来源摘要/页面简介

摘要：尽管通过长度外推、高效注意力和记忆模块进行了改进，但在外推期间不降低性能的情况下以线性复杂度处理无限长文档仍然是长文本处理的最终挑战。我们以端到端的方式直接优化长文本任务，并引入一种新颖的智能体工作流程 MemAgent，它分段读取文本并使用覆盖策略更新内存。我们扩展了 DAPO 算法，以通过独立上下文多对话生成来促进训练。 MemAgent 展示了卓越的长上下文能力，能够从 32K 文本训练的 8K 上下文推断到 3.5M QA 任务，性能损失 < 5%，并在 512K RULER 测试中达到 95%+。

## 抓取正文（中文翻译）

# MEMAGENTMEMAGENT：使用基于 Multi-Conv RL 的内存智能体重塑长上下文 LLM

于红利 所属单位：清华大学人工智能产业研究院 (AIR) 所属单位：字节跳动种子 所属单位：清华 AIR 和字节跳动种子 SIA 实验室
  
陈廷红 所属单位：清华大学人工智能产业研究院 (AIR)
  
冯江涛 单位：清华大学人工智能产业研究院 (AIR)
  
陈江杰 所属机构：字节跳动种子 所属机构：清华大学 AIR 的 SIA-Lab 和字节跳动种子
  
戴伟南 所属单位：清华大学人工智能产业研究院 (AIR) 所属单位：字节跳动种子 所属单位：清华 AIR 和字节跳动种子 SIA 实验室
  
余启英 所属单位：清华大学人工智能产业研究院 (AIR) 所属单位：字节跳动种子 所属单位：清华 AIR 和字节跳动种子 SIA 实验室
  
张亚勤 单位：清华大学人工智能产业研究院 (AIR) 单位：清华 AIR 和字节跳动种子 SIA 实验室
  
马伟英 单位：清华大学人工智能产业研究院 (AIR) 单位：清华 AIR 和字节跳动种子 SIA 实验室
  
刘晶晶 所属单位：清华大学人工智能产业研究院 (AIR) 所属单位：清华 AIR 和字节跳动种子 SIA 实验室
  
王明轩隶属关系：字节跳动种子
  
周浩††感谢：\*通讯作者。隶属关系：清华大学人工智能产业研究院 (AIR) 隶属关系：清华 AIR 和字节跳动种子 SIA 实验室

###### 摘要

尽管通过长度外推、高效注意力和内存模块进行了改进，但在外推过程中处理无限长文档而不降低性能仍然是长文本处理的最终挑战。为了解决这个问题，我们引入了一种新颖的智能体工作流程MemAgent，它分段处理文本并通过覆盖策略更新内存，通过增强的内存管理解决长上下文任务的挑战。我们进一步扩展 DAPO 算法，以端到端的方式直接优化记忆能力，通过独立上下文多对话生成促进训练。实验结果表明，MemAgent 具有出色的长上下文能力，能够从 8K 上下文推断到 3.5M QA 任务，性能损失不到 10%，在 512K NIAH 测试中达到超过 95%。

|  |
| --- |
|  |

图 1：RULER-HQA 的准确度得分（[Hsieh et al., 2024](https://arxiv.org/html/2507.02259#bib.bib15)；[Yang et al., 2018](https://arxiv.org/html/2507.02259#bib.bib69))。即使采用长上下文连续预训练和外推技术的模型也无法保持一致的性能。相比之下，带有 RL 的 MemAgent 仅表现出边际性能下降。

## 1 简介

同时展示了令人印象深刻的能力（[OpenAI，2024](https://arxiv.org/html/2507.02259#bib.bib18)；[DeepMind，2024](https://arxiv.org/html/2507.02259#bib.bib21)；[XAI，2024](https://arxiv.org/html/2507.02259#bib.bib20)；[Anthropic，2024](https://arxiv.org/html/2507.02259#bib.bib19)； [OpenAI, 2023](https://arxiv.org/html/2507.02259#bib.bib17))，行业级大型语言模型 (LLM) 系统（[Anthropic, 2025](https://arxiv.org/html/2507.02259#bib.bib26)；[Li et al., 2025a](https://arxiv.org/html/2507.02259#bib.bib25)；[Liu et al., 2024](https://arxiv.org/html/2507.02259#bib.bib24); [Yen et al., 2024](https://arxiv.org/html/2507.02259#bib.bib14)) 仍然面临着一个严峻的挑战：如何有效地处理长上下文 - 处理整本书，执行多个步骤的复杂推理链，或管理智能体系统的长期记忆 - 所有这些复杂的任务都会生成溢出的文本，从而快速爆炸当前 LLM 的典型大小上下文窗口。

![参考说明](https://arxiv.org/html/2507.02259v2/method.png)

图 2：MemAgent 的灵感来自于人类处理长文档的方式。它将文档分为多个块，并允许法学硕士迭代处理它们，将相关信息记录在内存中。最后，法学硕士根据记忆中存储的信息生成答案。

现有的长上下文任务方法有三管齐下。第一种涉及通过移动位置嵌入来扩展模型的上下文窗口的长度外推方法（[Su et al., 2024](https://arxiv.org/html/2507.02259#bib.bib44); [bloc97, 2023](https://arxiv.org/html/2507.02259#bib.bib45); [Chen et al., 2023](https://arxiv.org/html/2507.02259#bib.bib46); [Peng et al., 2023b](https://arxiv.org/html/2507.02259#bib.bib16)；[An et al., 2024](https://arxiv.org/html/2507.02259#bib.bib47))，加上持续的预训练（[Liu et al., 2023](https://arxiv.org/html/2507.02259#bib.bib61)；[Xiong et al., 2023](https://arxiv.org/html/2507.02259#bib.bib60);[高等人，2025](https://arxiv.org/html/2507.02259#bib.bib62))。尽管潜力巨大，但这些方法在应用于极长文本时，由于 O⁡(n2)O(n^{2}) 计算复杂性，常常会出现性能下降和处理速度缓慢的问题。第二类方法利用稀疏注意力（[Beltagy et al., 2020](https://arxiv.org/html/2507.02259#bib.bib58)；[Zhao et al., 2019](https://arxiv.org/html/2507.02259#bib.bib56)；[Xiao et al., 2023](https://arxiv.org/html/2507.02259#bib.bib57)）和线性注意力机制（[Child et al., 2019](https://arxiv.org/html/2507.02259#bib.bib55)；[Katharopoulos et al., 2020](https://arxiv.org/html/2507.02259#bib.bib59))，以降低注意力的复杂性，从而更有效地处理较长的序列。然而，这通常需要从头开始训练，并存在固有的不利因素，例如线性注意力在并行训练中面临困难，或者稀疏注意力取决于人类定义的模式。最后一行调查研究了上下文压缩（[Jiang et al., 2023](https://arxiv.org/html/2507.02259#bib.bib64); [Li et al., 2023](https://arxiv.org/html/2507.02259#bib.bib63); [Behrouz et al., 2024](https://arxiv.org/html/2507.02259#bib.bib53); [Zhang et al., 2024](https://arxiv.org/html/2507.02259#bib.bib54))，旨在压缩词元级或外部内存插件模块中的信息。此类方法通常难以进行外推，并且需要集成额外的模块或上下文操作，这不可避免地会破坏标准生成过程并阻碍兼容性和并行化。

因此，具有强大长上下文能力的成功法学硕士需要三位一体： OPEN1)1) 处理无限长度的文本； OPEN2)2) 扩展时性能不会显着下降； OPEN3)3) 具有线性复杂度的高效解码。为了追求这一追求，我们回到长上下文建模背后的基本直觉（[Miller 等人，1956](https://arxiv.org/html/2507.02259#bib.bib65)；[Hochreiter 和 Schmidhuber，1997](https://arxiv.org/html/2507.02259#bib.bib66)；[Graves 等人，2014](https://arxiv.org/html/2507.02259#bib.bib67)；[Weston等人，2014](https://arxiv.org/html/2507.02259#bib.bib68))。当人类处理长上下文信息时，我们倾向于抽象出主要的揭示性概念，以捕捉整个文本的本质，通常是通过记下关键细节或使用人手不足的速记机来记录关键点，同时丢弃冗余和不相关的数据。我们并不试图记住每一个事实或每一个小信息；相反，我们将智力精力集中在手头任务的更重要方面。这种选择性关注不仅简化了过程，而且有助于更有效地解决复杂问题。

遵循这种以人类为中心的直觉，我们提出了一种强化学习 (RL) 的新颖用途，为法学硕士配备动态更新的固定长度“记忆”，如图 2 所示（https://arxiv.org/html/2507.02259#S1.F2“图 2 ‣ 1 简介 ‣ MEMAGENT MEMAGENT：使用基于多卷积 RL 的记忆智能体重塑长上下文法学硕士”）。在推理过程中，LLM 逐段处理输入文本。当它读取每个片段时，模型会主动、有选择地更新内存，然后在所有相关消息在内存中聚合和协同后，有助于生成最终输出。这种巧妙的机制允许LLM灵活地处理任意文本长度，同时在处理过程中保持线性时间复杂度，因为内存的长度是固定的，这导致模型的上下文窗口大小是固定的。这种基于分段的方法从单个长文本输入生成多个输出，需要多轮内存更新和最后一轮以生成最终响应。训练这种类型的智能体工作流程可以实现跨多个独立上下文的对话，这在当前的法学硕士研究中仍然是一个尚未探索的领域。现有系统通常通过交替工具调用或环境反馈来处理工作流程轨迹，方法是简单地连接（[Ouyang et al., 2025](https://arxiv.org/html/2507.02259#bib.bib41); [Jin et al., 2025](https://arxiv.org/html/2507.02259#bib.bib39)）或使用滑动窗口（[Feng et al., 2025](https://arxiv.org/html/2507.02259#bib.bib40)) 方法，在实践中缺乏灵活性和可扩展性。相反，我们的 MemAgent 方法建议将每个与上下文无关的对话视为优化目标。基于 DAPO（[Yu et al., 2025](https://arxiv.org/html/2507.02259#bib.bib32)）算法，我们实现了 Multi-Conv DAPO，通过可验证的结果奖励来优化任意智能体工作流程。

在我们的实验中，在 60K 长度的文档上训练的具有适度 8K 上下文窗口（具有 1024 个词元内存和 5000 个词元文档块）的 RL 训练模型在针对多达 350 万个词元的文档的问答 (QA) 任务中表现出始终如一的卓越能力，而没有性能下降和线性计算成本。这清楚地展示了我们的长上下文记忆方法的效率和可扩展性。

我们的主要贡献有三个：

*•

  我们引入了一种新颖的方法，使法学硕士能够在推理过程中以线性时间复杂度在有限的上下文窗口内处理任意长的输入，克服了长上下文处理中的一个重大瓶颈。
*•

  我们设计了一个智能体工作流程来实现该机制，并提出了一种使用多对话 DAPO 算法的端到端训练方法。
*•

  我们凭经验证明，我们的 RL 训练方法允许模型在性能下降最小的情况下推断出很长的文档，从而突破了长上下文 LLM 系统目前可实现的界限。

![参考说明](https://arxiv.org/html/2507.02259v2/algo.png)

图 3：普通 GRPO 和 Multi-Conv DAPO 之间的比较。在 Multi-conv DAPO 的推出阶段，每个样本都会生成多个对话。最终对话中包含的答案用于计算奖励和优势，然后用于优化所有先前的对话。

## 2 方法论

在本节中，我们将详细介绍用于解决长上下文任务的 MemAgent 方法，包括整体工作流程 (§\mathsection [2.1](https://arxiv.org/html/2507.02259#S2.SS1 "2.1 MemAgent 工作流程：用于无界上下文的 RL 形记忆 ‣ 2 方法论 ‣ MEMAGENT MEMAGENT : Reshaping Long-上下文 LLM with Multi-Conv基于 RL 的记忆智能体"))，用于训练 MemAgent 的多卷积 RL 算法(§\mathsection [2.2](https://arxiv.org/html/2507.02259#S2.SS2 "2.2 使用多卷积 RL 训练 MemAgent ‣ 2 方法论 ‣ MEMAGENT MEMAGENT : Reshaping Long-上下文 LLM with Multi-Conv RL-based Memory 智能体")) 和正式建模我们的architecture(§\mathsection [2.3](https://arxiv.org/html/2507.02259#S2.SS3“2.3 从自回归建模角度重新思考 MemAgent ‣ 2 方法论 ‣ MEMAGENT MEMAGENT：使用基于多卷积 RL 的记忆智能体重塑长上下文 LLM”））。

### 2.1 MemAgent 工作流程：无界上下文的 RL 型内存

如[图 2](https://arxiv.org/html/2507.02259#S1.F2“图 2 ‣ 1 简介 ‣ MEMAGENT MEMAGENT：使用基于多卷积强化学习的内存智能体重塑长上下文 LLM”) 所示，MemAgent 将任意长的文档视为受控的证据流，而不是单一的块。在每一步，模型都会看到两件事：下一个文本块和一个紧凑的、固定长度的内存，它总结了迄今为止认为重要的所有内容。至关重要的是，内存只是上下文窗口内的一系列普通标记，因此基础 LLM 的核心生成过程保持不变。

读取新块后，模型会用更新的记忆覆盖以前的内存。这种覆盖策略看起来几乎太简单了，但它正是使系统能够扩展的原因：因为内存长度永远不会增长，所以每个块的总计算量保持为 O⁡(1)O(1) 并且端到端复杂性与块的数量严格呈线性关系。我们将覆盖决策制定为强化学习问题：智能体因保留稍后证明有用的信息以及丢弃会浪费宝贵词元的干扰因素而获得奖励。通过使用我们新引入的多对话 DAPO 算法优化此目标（详细信息请参见§\mathsection [2.2](https://arxiv.org/html/2507.02259#S2.SS2“2.2 使用多卷积 RL 训练 MemAgent ‣ 2 方法论 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的内存智能体重塑长上下文 LLM”），模型学会积极压缩，同时保留答案关键事实。

工作流程自然地将推理分解为两个模块。在上下文处理模块中，模型迭代块，使用提示模板更新内存（表 [5](https://arxiv.org/html/2507.02259#A1.T5“表 5 ‣ A.1 提示模板 ‣ 附录 A 实现细节 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的内存智能体重塑长上下文 LLM”)，顶部）。一旦流耗尽，就会调用最终的答案生成模块（表 [5](https://arxiv.org/html/2507.02259#A1.T5“表 5 ‣ A.1 提示模板 ‣ 附录 A 实现细节 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的内存智能体重塑长上下文 LLM”)，底部），其中模型仅查阅问题陈述和内存以生成其盒装答案。由于位置嵌入永远不会重新缩放或修补，因此两个模块中都适用相同的标记化和注意力布局，从而无需进行任何架构修改即可解锁模型的潜在长度外推能力。

因此，MemAgent 从这种设计中获得了三个好处：（1）无限长度：文档可以是数百万个词元，因为它是作为流处理的； (2) 无性能悬崖：RL 鼓励内存准确保留所需的信息，从而产生近乎无损的外推（图 [1](https://arxiv.org/html/2507.02259#S0.F1“图 1 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的内存智能体重塑长上下文 LLM”)； (3) 线性成本：恒定的窗口大小意味着解码时间和内存消耗随输入长度线性增长 (O⁡(N)O(N))（详细信息请参见§\mathsection [B](https://arxiv.org/html/2507.02259#A2“附录 B 计算复杂度 ‣ MEMAGENT MEMAGENT : Reshaping Long-上下文 LLM with Multi-Conv RL-based Memory）智能体”）。）这提供了一个实用的方法，可以将任何中等上下文大小的 LLM 转变为具有最小工程开销的高效长上下文推理器。

图 4：MemAgent 的架构和图形模型。内存被建模为潜在内存变量，从而能够将自回归语言模型分解为读取和写入内存的多个步骤。

### 2.2 使用多卷积强化学习训练 MemAgent

通过将答案生成任务的上下文处理中的记忆更新视为 RL 优化策略的一部分，我们采用 RLVR 配方（[OpenAI, 2024](https://arxiv.org/html/2507.02259#bib.bib18); [Guo et al., 2025](https://arxiv.org/html/2507.02259#bib.bib35); [Seed et al., 2025](https://arxiv.org/html/2507.02259#bib.bib23))训练MemAgent。我们采用 DAPO（[Yu et al., 2025](https://arxiv.org/html/2507.02259#bib.bib32)）作为我们的训练算法，这是一种从组相对策略优化（GRPO）（[Shao et al., 2024](https://arxiv.org/html/2507.02259#bib.bib34)）提炼出来的高效算法。由于我们的 MemAgent 方法的性质，它会为单个查询生成多个上下文无关的对话，如图 [2](https://arxiv.org/html/2507.02259#S1.F2“图 2 ‣ 1 简介 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的内存智能体重塑长上下文 LLM”），我们将每个对话视为独立的优化目标。这种方法需要将损失计算从传统的（组，词元）结构扩展到新的（组，对话，词元）维度，如图[3](https://arxiv.org/html/2507.02259#S1.F3“图3‣1简介‣MEMAGENT MEMAGENT：使用基于多卷积RL的记忆智能体重塑长上下文LLM”）所示。

形式上，策略模型πθold\pi\_{\theta\_{\text{old}}}对输入xx的一组GG个体响应{oi,j}i=1G\{o\_{i,j}\}\_{i=1}^{G}进行采样。让nin\_{i}表示给定样本(qi,ai)(q\_{i},a\_{i}).oi,jo\_{i,j}生成的对话数量(oi,1,oi,2,…,oi,ni)(o\_{i,1},o\_{i,2},...,o\_{i,n\_{i}})进一步分解为词元级输出(oi,j,1,oi,j,2,…,oi,j,|oi,j|)(o\_{i,j,1},o\_{i,j,2},...,o\_{i,j,|o\_{i,j}|})。优势值源自包含最终答案的对话，然后统一应用于源自同一样本的所有对话，如公式[1](https://arxiv.org/html/2507.02259#S2.E1“公式 1 ‣ 2.2 使用多卷积 RL 训练 MemAgent ‣ 2 方法论 ‣ MEMAGENT MEMAGENT : Reshaping Long-上下文 LLM with Multi-Conv RL-based Memory智能体”）。遵循 GRPO 博士（[Liu et al., 2025](https://arxiv.org/html/2507.02259#bib.bib33)），我们不通过标准差来划分优势。方程 [2](https://arxiv.org/html/2507.02259#S2.E2“方程 2 ‣ 2.2 使用多卷积 RL 训练 MemAgent ‣ 2 方法论 ‣ MEMAGENT MEMAGENT：使用基于多卷积 RL 的记忆智能体重塑长上下文 LLM”) 描述了我们的损失函数。

|  |  |  |  |
| --- | --- | --- | --- |
|  | A^i,j,t=Ri−mean​({Ri}i=1G)\hat{A}\_{i,j,t}=R\_{i}-\text{mean}(\{R\_{i}\}\_{i=1}^{G}) |  | (1) |

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | 𝒥DAPO​(θ)=\displaystyle\mathcal{J}\_{\text{DAPO}}(\theta)= | 𝔼(q,a)∼𝒟,{oi,j}i=1G∼πθold(⋅∣q,oi,j−1)\displaystyle\mathbb{E}\_{(q,a)\sim\mathcal{D},\{o\_{i,j}\}\_{i=1}^{G}\sim\pi\_{\theta\_{\text{old}}}(\cdot\mid q,~o\_{i,j-1})} |  | (2) |
|  |  | [1∑i=1G∑j=1ni|oi,j|∑i=1G∑j=1ni∑t=1|oi,j|(𝒞i,j,t−βDKL(πθ||πref)]\displaystyle\Bigg[\frac{1}{\sum\_{i=1}^{G}\sum\_{j=1}^{n\_{i}}|o\_{i,j}|}\sum\_{i=1}^{G}\sum\_{j=1}^{n\_{i}}\sum\_{t=1}^{|o\_{i,j}|}\Big(\mathcal{C}\_{i,j,t}-\beta D\_{\text{KL}}(\pi\_{\theta}||\pi\_{\text{ref}}\Big)\Bigg] |  |
|  | where ​𝒞i,j,t=\displaystyle\text{where\quad}\mathcal{C}\_{i,j,t}= | min⁡(ri,j,t​(θ)​A^i,j,t,clip​(ri,j,t​(θ),1−εl​o​w,1+εh​i​g​h)​A^i,j,t)\displaystyle\min\Big(r\_{i,j,t}(\theta)\hat{A}\_{i,j,t},\ \text{clip}\Big(r\_{i,j,t}(\theta),1-\varepsilon\_{low},1+\varepsilon\_{high}\Big)\hat{A}\_{i,j,t}\Big) |  |
|  | ri,j,t​(θ)=\displaystyle r\_{i,j,t}(\theta)= | πθ​(oi,j,t∣q,oi,j,<t)πθold​(oi,j,t∣q,oi,j,<t).\displaystyle\frac{\pi\_{\theta}(o\_{i,j,t}\mid q,o\_{i,j,<t})}{\pi\_{\theta\_{\text{old}}}(o\_{i,j,t}\mid q,o\_{i,j,<t})}. |  |

遵循 RLVR 配方（[Guo et al., 2025](https://arxiv.org/html/2507.02259#bib.bib35)；[Jin et al., 2025](https://arxiv.org/html/2507.02259#bib.bib39)；[Yu et al., 2025](https://arxiv.org/html/2507.02259#bib.bib32)），我们使用基于规则的验证器计算的最终结果奖励来训练模型：

|  |  |  |  |
| --- | --- | --- | --- |
|  | R⁡(y^,y)=𝟏is\_equiv​(y,y^)R(\hat{y},y)=\displaystyle\bm{1}\_{\mathrm{\texttt{is\\_equiv}(y,\hat{y})}} |  | (3) |

其中 y^\hat{y} 是预测答案，而 yy 是指真实值。

表 1：比较不同上下文长度的模型性能的主要实验结果。所有值均代表准确度 (%)。

型号长度

7K 14K 28K 56K 112K 224K 448K 896K 1.75M 3.5M

QwenLong-L1-32B 72.66 75.00 72.66 60.94 31.25 17.19 13.28 11.72 不适用 不适用

Qwen2.5-Instruct-14B-1M 60.16 60.94 50.00 57.03 50.00 37.50 8.59 0.00 不适用 不适用

Qwen2.5-Instruct-7B-1M 61.72 56.25 53.91 55.47 51.56 33.59 12.50 0.00 不适用 不适用

DS-蒸馏-Qwen-32B 70.31 66.41 65.62 46.88 23.44 13.28 7.81 7.03 不适用 不适用

DS-蒸馏-Qwen-14B 64.06 64.84 57.03 40.62 14.84 8.59 3.12 6.25 不适用 不适用

DS-蒸馏-Qwen-7B 30.47 12.50 3.12 0.00 0.00 0.78 0.00 0.00 不适用 不适用

Qwen2.5-Instruct-32B 69.53 64.84 60.16 51.56 44.53 21.88 14.06 7.03 不适用 不适用

Qwen2.5-Instruct-14B 75.00 67.19 57.03 54.69 44.53 21.88 10.94 2.34 不适用 不适用

Qwen2.5-Instruct-7B 52.34 57.03 51.56 44.53 32.81 13.28 6.25 1.56 不适用 不适用

RL-MemAgent-14B 80.47 82.03 82.03 83.59 81.25 77.34 79.69 75.78 78.91 71.09

RL-MemAgent-7B 81.25 81.25 82.03 80.47 79.69 75.78 76.56 74.22 77.34 71.88

### 2.3 从自回归建模角度重新思考 MemAgent

为了更深入地了解 MemAgent 设计，我们建议按照以下方式重新思考语言模型分解。标准自回归 LLM 将序列 𝐱1:N\mathbf{x}\_{1:N} 的联合似然因式分解为 p(𝐱1:N)=∏n=1Np(xn∣𝐱1:n−1),p(\mathbf{x}\_{1:N})=\prod\_{n=1}^{N}p(x\_{n}\mid\mathbf{x}\_{1:n-1}),，隐式假设每个过去的标记（或至少其隐藏状态）必须保留在活动上下文中。这就是将二次注意力变成长上下文瓶颈的原因。

MemAgent 将无界历史记录替换为固定长度内存𝐦∈𝕍M\mathbf{m}\!\in\!\mathbb{V}^{M},，如图 [4](https://arxiv.org/html/2507.02259#S2.F4 "图 4 ‣ 2.1 MemAgent 工作流程：用于无界上下文的 RL 型内存 ‣ 2 方法论 ‣ MEMAGENT MEMAGENT : Reshaping Long-上下文 LLM with基于多卷积强化学习的记忆智能体”）。输入文本以 KK 连续块𝐜1,…,𝐜K\mathbf{c}^{1},\dots,\mathbf{c}^{K}（每个长度≤C\leqC）的形式流式传输通过模型。读取块 kk 后，模型会用新向量 𝐦k\mathbf{m}^{k} 覆盖面板，该向量总结了迄今为止看到的所有证据。因为 |𝐦k|=M|\mathbf{m}^{k}|=M 是常数，所以每步的计算和内存都是 O⁡(C+M)O(C+M)，从而产生整体线性复杂度 O⁡(N)O(N)。

引入潜在序列𝐦1:K−1\mathbf{m}^{1:K-1}将原始似然分解为

|  |  |  |  |  |
| ---| ---| ---| ---| ---|
|  | p(𝐱1:N)\displaystyle p(\mathbf{x}\_{1:N}) | =∑𝐦1:K−1∏k=1Kp⁡(𝐜k∣𝐦k−1)⏟readp⁡(𝐦k∣𝐜k,𝐦k−1)⏟write,\displaystyle=\!\!\!\!\sum\_{\mathbf{m}^{1:K-1}}\prod\_{k=1}^{K}\underbrace{p(\mathbf{c}^{k}\mid\mathbf{m}^{k-1})}\_{\text{read}}\;\underbrace{p(\mathbf{m}^{k}\mid\mathbf{c}^{k},\mathbf{m}^{k-1})}\_{\text{write}}, |  | (4) |

在基本情况𝐦0=∅\mathbf{m}^{0}=\varnothing.的情况下，在每个块内，我们仍然运行普通的转换器解码器，但以恒定的上下文窗口(𝐜k,𝐦k−1)(\mathbf{c}^{k},\mathbf{m}^{k-1}).为条件。读取路径逐个词元分解，p(𝐜k∣𝐦k−1)=∏i=(k−1)​C+1k​Cp(xi∣𝐱1:i−1,𝐦k−1),p(\mathbf{c}^{k}\mid\mathbf{m}^{k-1})=\!\!\!\prod\_{i=(k-1)C+1}^{kC}\!p(x\_{i}\mid\mathbf{x}\_{1:i-1},\mathbf{m}^{k-1}),，而写入路径以相同的自回归方式生成下一个内存。

在我们的公式中，模型在上下文中的读写操作构成了马尔可夫决策过程（MDP），强化学习的目标是优化该 MDP 获得的最终奖励。因此，MemAgent 的学习目标是生成最大化奖励的读写记忆轨迹，这对应于学习以输入上下文为条件的记忆状态的最佳分布。这进一步从理论上说明了我们的强化学习公式和长文本建模之间的内在统一性。

表 2：LongBench-SUM 上的模型性能。所有值均代表召回率 (%)。粗体标记最高值，下划线标记每列中的第二高值。

|  |  |  |  |  |  |  |  |  |
| ---| ---| ---| ---| ---| ---| ---| ---| ---|
|型号|政府报告| | | |质量总和 | | | |
|胭脂-1 |胭脂-2 |胭脂-L |平均 |胭脂-1 |胭脂-2 |胭脂-L |平均 |
| Qwen2.5-Instruct-32B | 23.67 | 23.67 8.46 | 8.46 12.57 | 12.57 14.90 | 14.90 47.77 | 47.77 11.29 | 11.29 28.17 | 28.17 29.08 | 29.08
| Qwen2.5-Instruct-14B | 31.19 | 31.19 10.96 | 10.96 14.96 | 14.96 19.04 | 19.04 47.53 | 47.53 11.46 | 11.46 28.28 | 28.28 29.09 | 29.09
| Qwen2.5-Instruct-7B | 30.91 | 30.91 11.68 | 11.68 15.20 | 15.20 19.26 | 19.26 46.64 | 46.64 12.01 | 12.01 28.33 | 28.33 28.99 | 28.99
| QwenLong-L1 | 27.60 | 27.60 8.20 | 13.07 | 13.07 16.29 | 16.29 39.44 | 39.44 8.24 | 8.24 23.56 | 23.56 23.74 | 23.74
| Qwen2.5-Instruct-14B-1M | 30.58 | 11.93 | 11.93 15.51 | 15.51 19.34 | 19.34 47.31 | 47.31 13.13 | 13.13 29.07 | 29.07 29.84 | 29.84
| Qwen2.5-Instruct-7B-1M | 31.02 | 11.47 | 11.47 15.30 | 19.26 | 19.26 46.72 | 46.72 12.33 | 12.33 28.66 | 28.66 29.24 | 29.24
| DS-蒸馏-Qwen-32B | 26.13 | 26.13 8.86 | 12.98 | 12.98 15.99 | 15.99 39.09 | 39.09 8.75 | 23.96 | 23.96 23.93 | 23.93
| DS-蒸馏-Qwen-14B | 28.24 | 28.24 9.72 | 9.72 13.78 | 13.78 17.25 | 17.25 41.25 | 41.25 8.95 | 8.95 25:00 | 25.07 | 25.07
| DS-蒸馏-Qwen-7B | 33.30 | 9.39 | 9.39 14.59 | 14.59 19.10 | 19.10 34.33 | 5.97 | 5.97 21.57 | 21.57 20.62 | 20.62
| RL-MemAgent-14B | 37.16 | 37.16 12.03 | 12.03 16.23 | 16.23 21.80 | 21.80 50.21 | 12.70 | 12.70 31.27 | 31.27 31.39 |
| RL-MemAgent-7B | 30.28 | 12.37 | 12.37 15.37 | 15.37 19.34 | 19.34 48.49 | 48.49 14.41 | 14.41 30.91 | 30.91 31.27 | 31.27

## 3 个实验

### 3.1 实验设置

培训细节。为了保持与之前工作的可比性，我们选择 Qwen2.5-7B-Instruct 和 Qwen2.5-14B-Instruct （[Yang et al., 2024](https://arxiv.org/html/2507.02259#bib.bib36)）作为骨干模型。我们基于 verl 实现了具有独立上下文的多对话框架（[Sheng et al., 2024](https://arxiv.org/html/2507.02259#bib.bib43)）。

我们采用两阶段课程强化学习策略：

表 3：LongBench-QA 上的模型性能。

方法2Wiki HQA MuSiQue NQA Qasper AVG

QwenLong-L1-32B 83.0 69.5 51.0 26.0 24.0 50.7

Qwen2.5-Instruct-14B-1M 70.5 65.5 35.0 22.0 22.0 43.0

Qwen2.5-Instruct-7B-1M 67.5 58.5 26.0 21.5 24.0 39.5

DS-蒸馏-Qwen-32B 83.5 69.0 47.5 24.0 21.0 49.0

DS-蒸馏-Qwen-14B 83.5 67.0 42.0 22.0 22.0 47.3

DS-蒸馏-Qwen-7B 47.0 31.5 7.5 4.0 17.5 21.5

Qwen2.5-Instruct-32B 68.5 66.0 37.0 24.5 22.5 43.7

Qwen2.5-Instruct-14B 67.0 63.5 39.0 20.0 20.5 42.0

Qwen2.5-Instruct-7B 52.5 59.0 24.0 19.0 19.0 34.7

MemAgent-14B 79.0 73.0 52.0 25.0 26.0 51.0

MemAgent-7B 74.0 69.5 47.0 21.5 29.0 48.2

OPEN1)1) 第一阶段重点关注使模型获得基本的记忆能力； OPEN2)2) 第二阶段训练模型将这些能力转移到更多样化的环境和具有挑战性的任务中。训练的具体超参数详见 §\mathsection [A.3](https://arxiv.org/html/2507.02259#A1.SS3“A.3 训练 ‣ 附录 A 实现细节 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的记忆智能体重塑长上下文 LLM”)。

在训练过程中，我们有意将模型限制在 8K 上下文窗口内，以展示其外推能力。这个 8K 窗口的分配如下：1024 个词元用于查询，5000 个词元用于上下文块，1024 个词元用于内存，1024 个词元用于输出，其余词元保留用于聊天模板。

基准。我们对多个长文本基准进行综合评估，以评估模型在各种文本类型和任务中的能力。

1. 1.

   统治者总部。该基准是使用与第一阶段训练数据相同的合成方法创建的。它由信息密度适中、长度可控的任务组成，上下文分布接近自然语言，作为外推性能的定量评估。
2. 2.

   LongBench-QA。该基准测试由 NarrativeQA ([Kočiskỳ et al., 2018](https://arxiv.org/html/2507.02259#bib.bib8))、Qasper ([Dasigi et al., 2021](https://arxiv.org/html/2507.02259#bib.bib9))、HotpotQA ([Yang et al., 2018](https://arxiv.org/html/2507.02259#bib.bib69))、 2WikiMultihopQA [Ho 等人。 (2020)](https://arxiv.org/html/2507.02259#bib.bib7) 和 MuSiQue ([Trivedi et al., 2022](https://arxiv.org/html/2507.02259#bib.bib6))。任务相对较短，但信息密度较高，这严重考验了模型灵活的内存管理能力。它还评估模型将其记忆能力推广到各种材料（例如小说、新闻文章和维基条目）的能力。
3. 3.

   尼亚赫。大海捞针（NIAH）（[Kamradt，2023](https://arxiv.org/html/2507.02259#bib.bib13)）是一系列信息密度极低、极长的合成任务。为了成功，模型必须识别关键信息并在整个过程中保持其完整性，从而测试记忆的稳健性。
4. 4.

   长凳-SUM。我们还采用了两个长上下文summay任务，来自LongBench([Bai et al., 2024](https://arxiv.org/html/2507.02259#bib.bib3))的GovReport([Huang et al., 2021](https://arxiv.org/html/2507.02259#bib.bib4))和QMSum([Zhong et al., 2021](https://arxiv.org/html/2507.02259#bib.bib5))来评估与检索 QA 不同的任务类别中的性能。

基线。我们使用 DeepSeek-R1-Distill-Qwen（[Guo et al., 2025](https://arxiv.org/html/2507.02259#bib.bib35)）、Qwen-2.5-Instruct-1M（[Yang et al., 2025](https://arxiv.org/html/2507.02259#bib.bib38)）、Qwen-2.5-Instruct（[Yang et al., 2024](https://arxiv.org/html/2507.02259#bib.bib36))和QwenLong-L1 ([Wan et al., 2025](https://arxiv.org/html/2507.02259#bib.bib37))作为基线。它们的生成配置如表 [6](https://arxiv.org/html/2507.02259#A1.T6“表 6 ‣ A.4 评估 ‣ 附录 A 实现细节 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的内存智能体重塑长上下文 LLM”），而 MemAgent 使用与之前在训练详细信息中描述的相同的上下文管理。我们还将 MemAgent 与其他智能体方法进行了比较，详细信息请参见§\mathsection 。

![参考说明](https://arxiv.org/html/2507.02259v2/niah_single_combined_multi_2x2.png)

图 5：不同上下文长度下 NIAH 基准的性能热图。

### 3.2 主要结果

统治者总部。结果报告在表 [1](https://arxiv.org/html/2507.02259#S2.T1“表 1 ‣ 2.2 使用多卷积 RL 训练 MemAgent ‣ 2 方法论 ‣ MEMAGENT MEMAGENT：使用基于多卷积 RL 的记忆智能体重塑长上下文 LLM”）。我们对上下文长度从 7K 到 896K 的所有模型性能进行了比较分析。对于MemAgent，我们将评估扩展到1.75M和3.5M的超长上下文，以评估其外推能力。

MemAgent 表现出卓越的长度外推能力，随着输入上下文长度的增加，性能仅略有下降。相比之下，基线模型显示出不同的故障模式。 DS-Distill-Qwen 系列表现出快速的性能下降。 QwenLong-L1 在训练期间保持合理的性能，但之后会经历大幅下降。 Qwen2.5-Instruct-1M 系列在高达 112K 词元时仍保持可接受的性能，但在达到 896K 词元时性能会下降至零，远远低于其理论 1M 词元容量。这表明，尽管有扩展的上下文窗口，这些模型仍难以在超长上下文中有效利用信息。

LongBench-QA。 LongBench-QA 基准测试的结果如表 [3](https://arxiv.org/html/2507.02259#S3.T3“表 3 ‣ 3.1 实验设置 ‣ 3 个实验 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的记忆智能体重塑长上下文 LLM”）。 MemAgent 表现出卓越的整体性能，优于较大的长上下文或推理模型。 DS-Distill 系列和QwenLong 模型等推理模型在复杂数据集上进行训练，表现出强大的性能。相比之下，Qwen2.5-Instruct-1M系列对其骨干模型的改进有限。这表明 LongBench-QA 强调对文本的更深入理解，而不是简单的检索能力。 MemAgent 的性能表明，通过强化学习获得的记忆能力是可推广的。

尼亚赫。我们采用 RULER 基准中的 NIAH 的三个变体 [Hsieh 等人。 (2024)](https://arxiv.org/html/2507.02259#bib.bib15)，三个级别的难度不断增加。如图 [5](https://arxiv.org/html/2507.02259#S3.F5“图 5 ‣ 3.1 实验设置 ‣ 3 个实验 ‣ MEMAGENT MEMAGENT：使用基于多卷积 RL 的记忆智能体重塑长上下文 LLM”），即使在 128K 上下文窗口内，大多数基线也难以保持一致的性能，甚至Qwen2.5-Instruct-1M 512K 时性能也会下降。 RL-MemAgent 尽管存在一些性能波动，但在 512K 时仅表现出小于 5% 的最小性能损失。鉴于 512K 的评估涉及超过 100 轮对话，这种强劲的性能尤其值得注意。

长凳-SUM。我们通过 ROUGE-{1,2,L} 的召回分数来评估摘要质量。 RL-MemAgent 在几乎所有指标上都实现了 SOTA，这表明该模型已经学习了一般内存和上下文管理功能，而不是特定于 QA 任务的能力。

### 3.3 消融研究

图 6：RULER-HQA 上 RL 训练的消融结果。

图 7：Longbench-QA 上 RL 训练的消融结果。

#### 3.3.1 强化学习训练

为了研究强化学习的影响，我们进行了消融实验。 RULER-HQA 和 NIAH 的结果如图[7](https://arxiv.org/html/2507.02259#S3.F7“图 7 ‣ 3.3 Ablation Study ‣ 3 Experiments ‣ MEMAGENT MEMAGENT : Reshaping Long-上下文 LLM with Multi-Conv RL-based Memory 智能体”)和图[5](https://arxiv.org/html/2507.02259#S3.F5“图 5 ‣ 3.1 实验设置 ‣ 3 个实验 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的记忆智能体重塑长上下文 LLM”）。未经强化学习训练的MemAgent优于骨干模型；然而，随着输入长度的增加，它的性能仍然表现出大幅下降。 Longbench-QA 的结果如图 [7](https://arxiv.org/html/2507.02259#S3.F7“图 7 ‣ 3.3 消融研究 ‣ 3 个实验 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的记忆智能体重塑长上下文 LLM”），表明直接应用 MemAgent 只会带来边际甚至负面的改进。相比之下，RL-MemAgent 在两种评估场景中都取得了显着的改进，这表明强化学习训练对于开发通用且强大的记忆能力至关重要。

#### 3.3.2 内存长度

选择适当的 MemAgent 设置涉及某些权衡。更大的内存大小允许模型存储更多有用的信息，但它也带来了内存管理的挑战并增加了冗余的可能性。反之，情况可能会导致存储容量不足，使模型没有必要的参考。

为了实现合理的压缩比，同时将上下文总长度保持在 8,192 个词元以内，根据初步验证结果，我们将 MemAgent 的默认配置设置为使用 1,024 个词元内存和 5,000 个词元的上下文块。

为了研究超参数选择的影响，我们对从 256 到 4096 的内存长度进行了消融研究。结果如图[8]所示（https://arxiv.org/html/2507.02259#S3.F8“图 8 ‣ 3.3.3 上下文分布 ‣ 3.3 消融研究 ‣ 3 个实验 ‣ MEMAGENT MEMAGENT : Reshaping Long-上下文 LLM with基于 Multi-Conv RL 的记忆智能体”）和图[9](https://arxiv.org/html/2507.02259#S3.F9“图 9 ‣ 3.3.3 上下文分布 ‣ 3.3 消融研究 ‣ 3 个实验 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的记忆智能体重塑长上下文 LLM”），表明我们选择的配置构成了合理的最佳点，并且MemAgent 的性能在不同的内存大小上都很稳健。我们进一步研究了§\mathsection 中不同上下文大小的影响，并观察到类似的趋势。

#### 3.3.3 上下文分布

尽管我们的实验表明 MemAgent 可以有效地推断到 3.5M 词元的长度，但我们仍然希望检查 MemAgent 是否受到信息覆盖和中间丢失现象等问题的影响。我们的假设是，克服此类问题是端到端优化的自然结果。在训练过程中，模型学习保存和跟踪关键信息，以最大化最终奖励。

为了验证这个假设，我们仔细设计了一组基于 RULER-HQA 的探测实验，其中上下文由一些关键信息和许多干扰因素组成。我们将关键信息分为两组，并将它们放置在上下文中的不同位置。我们构建了五个设置：(0%, 100%)、(20%, 80%)、(40%, 60%)、(0%, 20%) 和 (80%, 100%)，其中 0% 表示上下文的开始，100% 表示上下文的结束。

例如，在 (0%, 100%) 情况下，模型在一开始就看到一条关键信息，而另一条仅在最后的内存更新步骤中看到。这代表了信息覆盖问题最具挑战性的场景之一。而 (40%, 60%) 可能是一个具有挑战性的迷失在中间的设置。

表 [4](https://arxiv.org/html/2507.02259#S3.T4“表 4 ‣ 3.3.3 上下文分布 ‣ 3.3 消融研究 ‣ 3 个实验 ‣ MEMAGENT MEMAGENT：使用基于多卷积 RL 的记忆智能体重塑长上下文 LLM”）表明 MemAgent 在所有模式中保持一致的稳健性，而没有表现出任何灾难性的性能下降。这有力地支持了我们的假设，即通过反复试验获得的一般记忆能力与任何特定的上下文模式无关。

![参考说明](https://arxiv.org/html/2507.02259v2/niah_single_abl_combined_multi_2x2.png)

图8：NIAH上记忆长度的消融结果

图9：Longbench上记忆长度的消融结果

表 4：探针实验结果。 Ctx。区。表示上下文分布，其中两个数字对应于整个上下文中两个关键信息组的相对位置。 0%表示开始，100%表示结束。 random 表示随机打乱所有上下文项，与主实验中的设置一致。其他行显示相对于随机的性能差异。所有值均代表准确度 (%)。

|  |  |  |  |  |  |  |  |  |  |
| ---| ---| ---| ---| ---| ---| ---| ---| ---| ---|
|型号| Ctx。区。 |长度 | | | | | | | |
| 7K | 14K | 28K | 56K | 112K | 224K | 448K |平均 |
| 14B | 14B随机| 80.47 | 82.03 | 82.03 | 83.59 | 81.25 | 81.25 77.34 | 77.34 79.69 | 79.69 75.78 |
|  | 0% 20% | +3.91 | -3.91 | -3.91 +3.13 | +1.57 | 0.00 | 0.00 +4.69 | +3.90 | +1.90 |
|  | 0% 100% | +3.12 | +0.78 | +3.13 | -3.12 | +1.56 | +7.82 | +6.25 | +2.79 |
|  | 20% 80% | +0.78 | -3.12 | +2.35 | +0.79 | -3.13 | +5.47 | -3.13 | 0.00 | 0.00
|  | 40% 60% | +1.56 | +2.35 | -2.34 | -2.34 -3.12 | -1.56 | -1.56 +3.13 | -0.78 | -0.78 -0.11 | -0.11
|  | 80% 100% | -2.35 | -2.35 0.00 | 0.00 +1.56 | +0.79 | +3.13 | 0.00 | 0.00 +1.56 | +0.67 |
| 7B|随机| 81.25 | 81.25 81.25 | 81.25 82.03 | 80.47 | 79.69 | 79.69 75.78 | 76.56 | 79.58 |
|  | 0% 20% | -1.56 | -1.56 -0.78 | -0.78 +3.13 | +3.91 | +3.12 | +5.47 | +3.13 | +2.35 |
|  | 0% 100% | +0.78 | 0.00 | 0.00 +2.35 | +1.56 | +3.90 | +4.69 | +2.35 | +2.23 |
|  | 20% 80% | -0.78 | -0.78 -0.78 | -0.78 +2.35 | 0.00 | 0.00 0.00 | 0.00 0.00 | 0.00 +3.13 | +0.56 |
|  | 40% 60% | 0.00 | 0.00 +1.56 | +3.13 | +0.78 | -3.91 | -3.91 +3.13 | +5.47 | +1.45 |
|  | 80% 100% | +1.56 | 0.00 | 0.00 +0.78 | -0.78 | -0.78 +0.78 | +4.69 | 0.00 | 0.00 +1.00 |

## 4 相关工作

长上下文法学硕士。基于 RoPE 的 LLM 的外推方法（[Su et al., 2024](https://arxiv.org/html/2507.02259#bib.bib44)），例如 NTK（[bloc97, 2023](https://arxiv.org/html/2507.02259#bib.bib45)）、PI（[Chen et al., 2023](https://arxiv.org/html/2507.02259#bib.bib46)）、 YaRN（[Peng et al., 2023b](https://arxiv.org/html/2507.02259#bib.bib16)）和 DCA（[An et al., 2024](https://arxiv.org/html/2507.02259#bib.bib47)）修改位置嵌入的组件，使模型能够捕获远程语义依赖关系。另一方面，线性注意力机制（[Child et al., 2019](https://arxiv.org/html/2507.02259#bib.bib55)；[Katharopoulos et al., 2020](https://arxiv.org/html/2507.02259#bib.bib59)）、循环神经网络（RNN）和状态空间模型（SSM）（[Gu et al., 2021](https://arxiv.org/html/2507.02259#bib.bib48)；[Gu 和 Dao，2023](https://arxiv.org/html/2507.02259#bib.bib49)；[Peng 等人，2023a](https://arxiv.org/html/2507.02259#bib.bib50)；[De 等人，2024](https://arxiv.org/html/2507.02259#bib.bib51)； 2024](https://arxiv.org/html/2507.02259#bib.bib52))，稀疏注意力([Beltagy et al., 2020](https://arxiv.org/html/2507.02259#bib.bib58); [Zhao et al., 2019](https://arxiv.org/html/2507.02259#bib.bib56); [Xiao et al., 2023](https://arxiv.org/html/2507.02259#bib.bib57); [Yuan et al., 2025](https://arxiv.org/html/2507.02259#bib.bib70)；[Lu et al., 2025](https://arxiv.org/html/2507.02259#bib.bib71)) 专注于架构改进。块策略也在长上下文建模中得到了探索（[Li et al., 2025b](https://arxiv.org/html/2507.02259#bib.bib2); [Liao et al., 2025](https://arxiv.org/html/2507.02259#bib.bib1)），而 MemAgent 的目标是通过标准 RL 框架的后训练为任何骨干模型配备记忆能力，而无需对架构进行重大改变。

记忆机制。长短期记忆 (LSTM) 机制（[Hochreiter 和 Schmidhuber，1997](https://arxiv.org/html/2507.02259#bib.bib66)）在早期 NLP 任务中取得了巨大成功，而神经图灵机（[Graves 等人，2014](https://arxiv.org/html/2507.02259#bib.bib67)）和记忆网络（[Weston 等人， 2014](https://arxiv.org/html/2507.02259#bib.bib68)) 演示了如何为神经网络配备记忆。集成到 Transformer 模型中的现有内存机制通常通过添加外部内存模块来实现（[Martins et al., 2021](https://arxiv.org/html/2507.02259#bib.bib73)；[Wu et al., 2020](https://arxiv.org/html/2507.02259#bib.bib72)； [Behrouz 等人，2024](https://arxiv.org/html/2507.02259#bib.bib53)； [Bulatov 等人，2023](https://arxiv.org/html/2507.02259#bib.bib75)) 或外部数据库（[Zhong 等人，2024](https://arxiv.org/html/2507.02259#bib.bib78)；[Lu 等人，2023](https://arxiv.org/html/2507.02259#bib.bib76)；[Modarressi 等人， 2023](https://arxiv.org/html/2507.02259#bib.bib77))。最近，检索增强记忆智能体（[Fang et al., 2025](https://arxiv.org/html/2507.02259#bib.bib11); [Chhikara et al., 2025](https://arxiv.org/html/2507.02259#bib.bib10); [Zhou et al., 2025](https://arxiv.org/html/2507.02259#bib.bib12)）工作流程引起了社区的关注。 MemAgent 与其他智能体的区别在于，我们使用强化学习来使 LLM 本身能够 记住。

法学硕士的强化学习。在最近的强化学习研究中，奖励信号已逐渐从人类偏好（[Ouyang et al., 2022](https://arxiv.org/html/2507.02259#bib.bib28)）或从中提取的奖励模型（[Bai et al., 2022](https://arxiv.org/html/2507.02259#bib.bib74)）转向基于规则的反馈，这在增强模型推理能力方面表现出了巨大的潜力（[OpenAI, 2024](https://arxiv.org/html/2507.02259#bib.bib18);[郭等人，2025](https://arxiv.org/html/2507.02259#bib.bib35)；[Qwen，2024](https://arxiv.org/html/2507.02259#bib.bib22)；[DeepMind，2024](https://arxiv.org/html/2507.02259#bib.bib21)； 2025](https://arxiv.org/html/2507.02259#bib.bib27)) 与基于 GAE ([Schulman et al., 2018](https://arxiv.org/html/2507.02259#bib.bib30)) 的 PPO ([Schulman et al., 2017](https://arxiv.org/html/2507.02259#bib.bib29)) 或 GRPO ([Shao et al., 2024](https://arxiv.org/html/2507.02259#bib.bib34)) 培训。算法增强（[Hu, 2025](https://arxiv.org/html/2507.02259#bib.bib31)；[Yu et al., 2025](https://arxiv.org/html/2507.02259#bib.bib32)；[Liu et al., 2025](https://arxiv.org/html/2507.02259#bib.bib33)）主要集中在提高这些算法的可持续性和效率上。为了进一步释放强化学习的潜力，最近的研究成果包括 Search-R1（[Jin et al., 2025](https://arxiv.org/html/2507.02259#bib.bib39)）、智能体-R1（[Ouyang et al., 2025](https://arxiv.org/html/2507.02259#bib.bib41)）和 RAGEN（[Wang et al., 2025](https://arxiv.org/html/2507.02259#bib.bib42))探索了基于多轮聊天的工具使用智能体的训练。 GiGPO（[Feng et al., 2025](https://arxiv.org/html/2507.02259#bib.bib40)）进一步 研究在智能体训练中使用多个独立上下文。

## 5 结论

在本文中，我们介绍了 MemAgent，这是一种新颖的长上下文方法，采用强化学习训练的记忆模块，使大型语言模型 (LLM) 能够有选择地记录相关信息，同时忽略无关细节。我们的实验表明，当对 60K 长度的序列进行训练时，MemAgent 表现出显着的外推能力，将其有效上下文扩展到仅 8K 上下文的 350 万个标记。该模型在各种长上下文任务中实现了最先进的性能。我们的消融研究揭示了基于强化学习的训练在实现这些结果方面的关键作用，以及记忆容量如何影响不同任务类型的表现，为所提出的记忆机制提供了重要的见解。我们希望这项工作可以为开发更先进的记忆架构和训练策略奠定坚实的基础，从而为显着增强法学硕士的长上下文能力铺平道路。

## 再现性声明

为了可重复性，我们在(§\mathsection [A](https://arxiv.org/html/2507.02259#A1“附录 A 实现细节 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的内存智能体重塑长上下文 LLM”)) 中提供了实现详细信息，包括提示模板(§\mathsection [A.1](https://arxiv.org/html/2507.02259#A1.SS1“A.1 提示模板 ‣ 附录 A 实现细节 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的内存智能体重塑长上下文 LLM”))，伪代码(§\mathsection [A.2](https://arxiv.org/html/2507.02259#A1.SS2“A.2 算法 ‣ 附录 A 实现细节 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的内存智能体重塑长上下文 LLM”)) 以及训练配方和算法超参数(§\mathsection [A.3](https://arxiv.org/html/2507.02259#A1.SS3“A.3 训练 ‣ 附录 A 实现细节 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的内存智能体重塑长上下文 LLM”)) 和评估设置(§\mathsection [A.4](https://arxiv.org/html/2507.02259#A1.SS4“A.4 评估 ‣ 附录 A 实现细节 ‣ MEMAGENT MEMAGENT：使用基于多卷积 RL 的内存智能体重塑长上下文 LLM”))。训练和评估代码以及数据集和模型权重将在开源平台上提供。

## 附录 A 实施细节

### A.1 提示模板

|  |
| ---|
|您会看到一个问题、文章中可能包含答案的部分以及以前的记忆。请仔细阅读本节，并使用有助于回答问题的新信息“更新记忆”，同时保留先前记忆中的所有相关细节。 |
| <problem> {提示} </problem> |
| <memory> {内存} </memory> |
| <section> {块} </section> |
|更新内存： |
| You are presented with a problem and a previous memory. Please answer the problem based on the previous memory and put the answer in `\boxed{}`. |
| <problem> {提示} </problem> |
| <memory> {内存} </memory> |
|您的回答： |

表 5：用于上下文处理（顶部）和最终答案生成（底部）的 MemAgent 模板。大括号占位符 {} 将替换为实际内容。

### A.2 算法

算法1 多变换DAPO

1：策略模型πθ\pi\_{\theta},参考模型πref\pi\_{\mathrm{ref}}（冻结），基于规则的验证器VV，数据集𝒟\mathcal{D},组大小GG

2：虽然没有收敛

3：
  提示示例 q∼𝒟q\sim\mathcal{D}

4：
  for g=1g=1 to GG do ⊳\triangleright 同一 qq 的对话组

5：
   初始化hg,0←[q]h\_{g,0}\leftarrow[q]

6：
   对于 t=1t=1 到 cgc\_{g} 执行⊳\triangleright 上下文无关的对话

7：
     样品og,t∼πθ(⋅∣hg,t−1)o\_{g,t}\sim\pi\_{\theta}(\cdot\midh\_{g,t-1})

8：
     hg,t←hg,t−1∥og,th\_{g,t}\leftarrow h\_{g,t-1}\mathbin{\|}o\_{g,t}

9：
   结束于

10：
   yg←og,cgy\_{g}\leftarrow o\_{g,c\_{g}} ⊳\triangleright 用于评分的最终响应

11：
   r^g←V⁡(q,yg)\hat{r}\_{g}\leftarrow V(q,y\_{g}) ⊳\triangleright 基于规则的奖励

12：
   dg←KL(πθ(⋅∣hg,cg)∥πref(⋅∣hg,cg))d\_{g}\leftarrow\mathrm{KL}\big(\pi\_{\theta}(\cdot\midh\_{g,c\_{g}})\,\|\,\pi\_{\mathrm{ref}}(\cdot\midh\_{g,c\_{g}})\big)

13：
   rg←r^g−β​dgr\_{g}\leftarrow\hat{r}\_{g}-\betad\_{g}

14：
  结束于

15：
  {Ag}g=1G←GroupNorm⁡({rg}g=1G)\{A\_{g}\}\_{g=1}^{G}\leftarrow\mathrm{GroupNorm}(\{r\_{g}\}\_{g=1}^{G})

16：
  对于 g=1g=1 到 GG 做

17：
   ρg←πθ​(yg∣hg,cg)πθold​(yg∣hg,cg)\rho\_{g}\leftarrow\dfrac{\pi\_{\theta}(y\_{g}\midh\_{g,c\_{g}})}{\pi\_{\theta\_{\text{old}}}(y\_{g}\midh\_{g,c\_{g}})}

18：
   𝒥g←min⁡(ρg​Ag,clip⁡(ρg,1−ϵl​o​w,1+ϵh​i​g​h)​Ag)\mathcal{J}\_{g}\leftarrow\min\big(\rho\_{g}A\_{g},\,\mathrm{clip}(\rho\_{g},1-\epsilon\_{low},1+\epsilon\_{high})A\_{g}\big)

19：
  结束于

20：
  𝒥clip←1G​∑g=1G𝒥g\mathcal{J}\_{\mathrm{clip}}\leftarrow\frac{1}{G}\sum\_{g=1}^{G}\mathcal{J}\_{g}

21：
  θ←θ+η​∇θ𝒥clip\theta\leftarrow\theta+\eta\nabla\_{\theta}\mathcal{J}\_{\mathrm{clip}}

22：结束时

### A.3 培训

我们使用 DAPO 算法进行训练，应用 KL 因子 1×10−31\times 10^{-3} 并禁用熵损失。 AdamW 优化器采用恒定学习率 1×10−61\times 10^{-6} 和线性预热调度器，wram-up 步骤设置为 20。我们使用 rollout 批量大小为 256，组大小为 16。请注意，由于 MemAgent 的多对话功能，实际的小批量大小不等于 rollout 批量大小/16。我们通过将样本批量大小与反向传播批量大小的比率固定为 16 来利用离策略训练。

当第一阶段完全收敛时，我们转向第二阶段，这需要大约 400 个步骤。这是每个阶段的训练数据配方。

*•

  第一阶段我们使用 32,768 个合成 QA 数据实例，每个实例长度约为 32K 个词元。这些基于 HotpotQA（[Yang 等人，2018](https://arxiv.org/html/2507.02259#bib.bib69)）数据集，并遵循 RULER（[Hsieh 等人，2024](https://arxiv.org/html/2507.02259#bib.bib15)）方法，其中涉及将黄金段落（包含正确答案）嵌入从同一数据集采样的大量干扰内容中。
*•

  第二阶段我们使用 2,560 个训练实例，最大长度为 60K 词元。该集合由来自 DocQA-RL-1.6K（[Wan et al., 2025](https://arxiv.org/html/2507.02259#bib.bib37)）的困难、高质量长文本 QA 数据组成，并与第一阶段的数据混合。

第一阶段使用的每个训练样本都是 HotpotQA 中的 200 篇文章，总 词元 长度约为 28K。我们通过过滤掉 Qwen2.5-7B-Base 或 Qwen2.5-7B-Instruct 在没有给出任何上下文的情况下达到 100% Best-Of-2 分数的问题来彻底清理数据集。这些问题可能代表了模型记忆中已经内化的常识。来自 HotpotQA 训练分割的 80,000 个样本通过此管道进行处理，大约 50% 的数据被过滤掉。我们选择了前 32,768 个处理数据样本作为我们的训练集。

然后，我们应用类似的方法从 HotpotQA 验证集中合成 128 个样本。对于外推性能测试，我们使用相同的管道合成具有不同上下文长度的测试集。 wiki 项目的数量范围从 50 到 6400，对应于大约 7K 到 350 万个词元的上下文长度。

### A.4 评估

我们使用正则表达式从模型输出中提取答案，并提示模型以指定的格式进行响应。选择的格式是“答案就是答案”。

我们对所有基准测试都采用 sub\_em 分数。这意味着如果答案包含基本事实的所有元素，则该答案被认为是正确的。当答案由多个部分组成并且预期响应应包括所有部分时，分数对应于所提供的正确部分的比例。

在评估答案之前，我们对基本事实和提取的响应进行标准化。例如，我们删除定冠词，忽略大小写区别，并按照之前的工作应用类似的标准标准化步骤（[Wan et al., 2025](https://arxiv.org/html/2507.02259#bib.bib37); [Hsieh et al., 2024](https://arxiv.org/html/2507.02259#bib.bib15); [Yen et al., 2024](https://arxiv.org/html/2507.02259#bib.bib14))。

表 [6](https://arxiv.org/html/2507.02259#A1.T6“表 6 ‣ A.4 评估 ‣ 附录 A 实现细节 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的内存智能体重塑长上下文 LLM”) 显示了基线模型的生成配置。

表 6：基线模型的生成配置。

模型上下文长度输入/输出标记

QwenLong-L1（[Wan 等人，2025](https://arxiv.org/html/2507.02259#bib.bib37)）128K 120,000 / 10,000

Qwen2.5-Instruct-1M 系列 ([Yang et al., 2025](https://arxiv.org/html/2507.02259#bib.bib38)) 1M 990,000 / 10,000

DeepSeek-R1-Distill-Qwen 系列（[Guo et al., 2025](https://arxiv.org/html/2507.02259#bib.bib35)）128K 120,000 / 10,000

Qwen2.5-Instruct 系列([Yang et al., 2024](https://arxiv.org/html/2507.02259#bib.bib36)) 128K 120,000 / 10,000

我们的测试中使用了 RULER 中的 NIAH niah\_single\_{1,2,3}（[Hsieh et al., 2024](https://arxiv.org/html/2507.02259#bib.bib15)）基准。 RULER 的 yaml 配置在 [7](https://arxiv.org/html/2507.02259#A1.T7“表 7 ‣ A.4 评估 ‣ 附录 A 实现细节 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的内存智能体重塑长上下文 LLM”）中介绍。在第一级中，“干草堆”由重复的句子组成，“针”是一个与魔法词相关的七位数字。对于第 2 级，“干草堆”由较长的论文组成。第 3 级比第 2 级更进一步，其中“needle”是 36 个字符的 UUID 字符串。问题和上下文连接起来作为法学硕士的输入。我们省略了原始 RULER 基准测试中提供的answer\_prefix，因为它与 MemAgent 工作流程不兼容。

|  |
| ---|
| niah\_single\_1: |
|任务：尼亚|
|参数： |
| type\_haystack: repeat |
| type\_needle\_k: words |
| type\_needle\_v: numbers |
| num\_needle\_k: 1 |
| num\_needle\_v: 1 |
| num\_needle\_q: 1 |
| niah\_single\_2: |
|任务：尼亚|
|参数： |
| type\_haystack: essay |
| type\_needle\_k: words |
| type\_needle\_v: numbers |
| num\_needle\_k: 1 |
| num\_needle\_v: 1 |
| num\_needle\_q: 1 |
| niah\_single\_3: |
|任务：尼亚|
|参数： |
| type\_haystack: essay |
| type\_needle\_k: words |
| type\_needle\_v: uuids |
| num\_needle\_k: 1 |
| num\_needle\_v: 1 |
| num\_needle\_q: 1 |

表 7：用于 NIAH 任务的综合配置。

## 附录 B 计算复杂度

我们采用来自 verl [Sheng et al. 2017] 的 Qwen2Model 浮点运算 (FLOP) 估计器。 (2024)](https://arxiv.org/html/2507.02259#bib.bib43) 来计算基线模型和我们提出的方法的 FLOP 成本。结果如图 [10](https://arxiv.org/html/2507.02259#A2.F10“图 10 ‣ 附录 B 计算复杂性 ‣ MEMAGENT MEMAGENT：使用基于 Multi-Conv RL 的内存智能体重塑长上下文 LLM”）。基线模型的复杂度为 O(n2n^{2})，而 MemAgent 的复杂度为 O⁡(n)O(n)。

图 10：从 8K 到 4M 上下文长度的浮点运算

对于基线模型，处理所需的词元数量为 q+c+oq+c+o，其中 qq 表示问题的长度，cc 是上下文长度，oo 表示输出长度。

对于 MemAgent，总 FLOP 成本是所有阶段 FLOP 的总和。涉及的具体阶段如下：

*•

  初始化：在第一阶段，模型处理由 q+200+oq+200+o 组成的输入，其中 200200 表示添加的常量，用于提示模型遵循 MemAgent 工作流程。
*•

  内存更新：重复次数由k=⌈cN⌉k=\lceil\frac{c}{N}\rceil,决定，其中cc是输入的可变分量。每次重复都需要长度为 q+200+N+oq+200+N+o 的输入。
*•

  最终答案：最后阶段处理长度为 q+100+oq+100+o 的输入，其中包括前面步骤的累积输出。

我们设置q=1024,o=1024,N=5000q=1024,o=1024,N=5000，cc的范围是8K到4M来计算最终结果。

## 附录 C 案例研究

为了进一步详细说明所提出的记忆机制，我们对 MemAgent-14B 的生成轨迹进行了案例研究。输入问题是：浪漫喜剧《巨石峡》的导演居住在纽约哪个城市？这是一个包含以下相关维基百科条目的 2 跳问题：

1) 《巨石峡》是一部 2014 年美国剧情浪漫喜剧电影，由阿德里亚娜·特里贾尼编剧并执导。

2) 阿德里安娜·特里贾尼 (Adriana Trigiani) 是一位意大利裔美国人，出版了 16 本书，同时也是电视作家、电影导演和企业家，居住在纽约市格林威治村。

在第一轮中，该模型出现了条目“Ghost”，它指的是同样位于纽约的生产团队。该模型选择保留这些可能有用的信息以供将来使用。在第二轮中，没有提供相关上下文；尽管如此，该模型仍保持其智能体状态，表现出抗干扰的鲁棒性。在第三轮中，将展示两个相关条目。该模型正确识别关键信息并相应更新其内存，从而得出正确答案：纽约市格林威治村。至此，推理过程就完成了。在剩余的回合中，模型的记忆保持不变并用于产生最终响应。

### 块1

……

文档20：幽灵（制作组）

Ghost 是一支瑞典唱片制作和歌曲创作团队，由 Ulf Lindström 和 Johan Ekhé 组成，总部位于纽约。

……

### 内存1

提供的部分不包含有关浪漫喜剧“Big Stone Gap”的导演或其在纽约市的基地的任何信息。不过，它确实提到了一个位于纽约市的名为“Ghost”的制作团队。由于问题专门询问《巨石峡》的导演，并且给定部分中没有有关导演的直接信息，因此我们无法从提供的文本中推断出与问题直接相关的任何内容。

更新内存：

•

Ghost 是一支瑞典唱片制作和歌曲创作团队，由 Ulf Lindström 和 Johan Ekhé 组成，总部位于纽约。他们最出名的也许是创作和制作瑞典歌手罗宾的前三张录音室专辑。

根据提供的部分，该问题仍未得到解答。需要更多信息来确定“Big Stone Gap”的导演及其在纽约市的基地。

### 块2

…（无相关文件）

### 内存2

提供的部分不包含有关浪漫喜剧“Big Stone Gap”的导演或其在纽约市的基地的任何信息。 2 因此，更新后的内存对于当前的问题保持不变。记忆仍然指出，Ghost 唱片制作和歌曲创作团队位于纽约市，但没有提供有关《Big Stone Gap》导演的任何信息。

更新内存：

•

Ghost 是一支瑞典唱片制作和歌曲创作团队，由 Ulf Lindström 和 Johan Ekhé 组成，总部位于纽约。他们最出名的也许是创作和制作瑞典歌手罗宾的前三张录音室专辑。 •

根据提供的部分，该问题仍未得到解答。需要更多信息来确定“Big Stone Gap”的导演及其在纽约市的基地。

