# MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent

- 来源: https://arxiv.org/abs/2507.02259
- 发布日期: 2025-07-03
- 日期依据: page metadata: citation_date
- 类型: paper
- 主题: MemAgent、强化学习、压缩记忆
- 抓取状态: full_text_html
- 正文来源: https://arxiv.org/html/2507.02259
- 抓取时间 UTC: 2026-10-26T09:38:09.586112+00:00
- 作者: Yu, Hongli, Chen, Tinghong, Feng, Jiangtao, Chen, Jiangjie, Dai, Weinan, Yu, Qiying, Zhang, Ya-Qin, Ma, Wei-Ying, Liu, Jingjing, Wang, Mingxuan, Zhou, Hao

## 来源摘要 / 页面简介

Abstract: Despite improvements by length extrapolation, efficient attention and memory modules, handling infinitely long documents with linear complexity without performance degradation during extrapolation remains the ultimate challenge in long-text processing. We directly optimize for long-text tasks in an end-to-end fashion and introduce a novel agent workflow, MemAgent, which reads text in segments and updates the memory using an overwrite strategy. We extend the DAPO algorithm to facilitate training via independent-context multi-conversation generation. MemAgent has demonstrated superb long-context capabilities, being able to extrapolate from an 8K context trained on 32K text to a 3.5M QA task with performance loss < 5% and achieves 95%+ in 512K RULER test.

## 抓取正文

# MEMAGENTMEMAGENT: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent

Hongli Yu
Affiliation:  Institute for AI Industry Research (AIR), Tsinghua University
Affiliation:  ByteDance Seed
Affiliation:  SIA-Lab of Tsinghua AIR and ByteDance Seed
  
Tinghong Chen
Affiliation:  Institute for AI Industry Research (AIR), Tsinghua University
  
Jiangtao Feng
Affiliation:  Institute for AI Industry Research (AIR), Tsinghua University
  
Jiangjie Chen
Affiliation:  ByteDance Seed
Affiliation:  SIA-Lab of Tsinghua AIR and ByteDance Seed
  
Weinan Dai
Affiliation:  Institute for AI Industry Research (AIR), Tsinghua University
Affiliation:  ByteDance Seed
Affiliation:  SIA-Lab of Tsinghua AIR and ByteDance Seed
  
Qiying Yu
Affiliation:  Institute for AI Industry Research (AIR), Tsinghua University
Affiliation:  ByteDance Seed
Affiliation:  SIA-Lab of Tsinghua AIR and ByteDance Seed
  
Ya-Qin Zhang
Affiliation:  Institute for AI Industry Research (AIR), Tsinghua University
Affiliation:  SIA-Lab of Tsinghua AIR and ByteDance Seed
  
Wei-Ying Ma
Affiliation:  Institute for AI Industry Research (AIR), Tsinghua University
Affiliation:  SIA-Lab of Tsinghua AIR and ByteDance Seed
  
Jingjing Liu
Affiliation:  Institute for AI Industry Research (AIR), Tsinghua University
Affiliation:  SIA-Lab of Tsinghua AIR and ByteDance Seed
  
Mingxuan Wang
Affiliation:  ByteDance Seed
  
Hao Zhou
††thanks: \*Corresponding author.
Affiliation:  Institute for AI Industry Research (AIR), Tsinghua University
Affiliation:  SIA-Lab of Tsinghua AIR and ByteDance Seed

###### Abstract

Despite improvements by length extrapolation, efficient attention and memory modules, handling infinitely long documents without performance degradation during extrapolation remains the ultimate challenge in long-text processing. To solve this problem, we introduce a novel agent workflow, MemAgent, which processes text in segments and updates memory through an overwrite strategy, addressing the challenge of long-context task through enhanced memory management. We further extend the DAPO algorithm to directly optimize memory ability in an end-to-end fashion, facilitating training via independent-context multi-conversation generation. Experimental results demonstrate that MemAgent has superb long-context capabilities, being able to extrapolate from an 8K context to a 3.5M QA task with a performance loss of less than 10% and achieving over 95% on the 512K NIAH test.

|  |
| --- |
|  |

Figure 1: Accuracy scores of RULER-HQA ([Hsieh et al., 2024](https://arxiv.org/html/2507.02259#bib.bib15); [Yang et al., 2018](https://arxiv.org/html/2507.02259#bib.bib69)) . Even models that employ long-context continual pretraining and extrapolation techniques fail to maintain consistent performance. In contrast, MemAgent with RL only demonstrates marginal performance dropping.

## 1 Introduction

While having demonstrated impressive capabilities ([OpenAI, 2024](https://arxiv.org/html/2507.02259#bib.bib18); [DeepMind, 2024](https://arxiv.org/html/2507.02259#bib.bib21); [XAI, 2024](https://arxiv.org/html/2507.02259#bib.bib20); [Anthropic, 2024](https://arxiv.org/html/2507.02259#bib.bib19); [OpenAI, 2023](https://arxiv.org/html/2507.02259#bib.bib17)), industry-level Large Language Model (LLM) systems ([Anthropic, 2025](https://arxiv.org/html/2507.02259#bib.bib26); [Li et al., 2025a](https://arxiv.org/html/2507.02259#bib.bib25); [Liu et al., 2024](https://arxiv.org/html/2507.02259#bib.bib24); [Yen et al., 2024](https://arxiv.org/html/2507.02259#bib.bib14)) still face a critical challenge: how to handle long contexts effectively - processing an entire book, executing a complex chain of reasoning over many steps, or managing the long-term memory of an agent system - all these complex tasks can generate overflowing text that quickly explodes the typical-size context window of current LLMs.

![Refer to caption](https://arxiv.org/html/2507.02259v2/method.png)

Figure 2: MemAgent is inspired by the way humans process long documents. It divides the document into multiple chunks and allows LLMs to process them iteratively, recording relevant information in memory. Finally, LLMs generate answers based on the information stored in the memory.

Existing approaches to long-context tasks are three-pronged. The first involves length extrapolation methods by shifting the positional embeddings in order to extend the context window of the model ([Su et al., 2024](https://arxiv.org/html/2507.02259#bib.bib44); [bloc97, 2023](https://arxiv.org/html/2507.02259#bib.bib45); [Chen et al., 2023](https://arxiv.org/html/2507.02259#bib.bib46); [Peng et al., 2023b](https://arxiv.org/html/2507.02259#bib.bib16); [An et al., 2024](https://arxiv.org/html/2507.02259#bib.bib47)), plus continued pre-training ([Liu et al., 2023](https://arxiv.org/html/2507.02259#bib.bib61); [Xiong et al., 2023](https://arxiv.org/html/2507.02259#bib.bib60); [Gao et al., 2025](https://arxiv.org/html/2507.02259#bib.bib62)). Despite promising potential, these methods often suffer from performance degradation and slow processing speed due to O⁡(n2)O(n^{2}) computational complexity when applied to extremely long text. The second school of methods leverages sparse attention ([Beltagy et al., 2020](https://arxiv.org/html/2507.02259#bib.bib58); [Zhao et al., 2019](https://arxiv.org/html/2507.02259#bib.bib56); [Xiao et al., 2023](https://arxiv.org/html/2507.02259#bib.bib57)) and linear attention mechanisms ([Child et al., 2019](https://arxiv.org/html/2507.02259#bib.bib55); [Katharopoulos et al., 2020](https://arxiv.org/html/2507.02259#bib.bib59)) to reduce the complexity of attention for more efficient processing of longer sequences. However, this typically requires training from scratch, with inherent adversities such as linear attention facing difficulties in parallel training or sparse attention depending on human-defined patterns. The last line of inquiry investigates context compression ([Jiang et al., 2023](https://arxiv.org/html/2507.02259#bib.bib64); [Li et al., 2023](https://arxiv.org/html/2507.02259#bib.bib63); [Behrouz et al., 2024](https://arxiv.org/html/2507.02259#bib.bib53); [Zhang et al., 2024](https://arxiv.org/html/2507.02259#bib.bib54)), which aims to condense information in token-level or external-memory-plugin modules. Such approaches often struggle with extrapolation, and require the integration of additional modules or context operations, which ineluctably disrupts the standard generation process and hinders compatibility as well as parallelization.

Hence, a successful LLM with strong long-context capabilities requires the trinity of:
OPEN1)1) processing infinite length of text;
OPEN2)2) scaling without significant performance drop; and OPEN3)3) efficient decoding with linear complexity. To pursue this quest, we return to the basic intuition behind long-context modeling ([Miller and others, 1956](https://arxiv.org/html/2507.02259#bib.bib65); [Hochreiter and Schmidhuber, 1997](https://arxiv.org/html/2507.02259#bib.bib66); [Graves et al., 2014](https://arxiv.org/html/2507.02259#bib.bib67); [Weston et al., 2014](https://arxiv.org/html/2507.02259#bib.bib68)). When humans process long-context information, we tend to abstract out the main revealing conceptions to capture the essence of the whole text, often by making notes of critical details or using short-handed stenograph to record the key points, while discarding redundant and irrelevant data. We do not attempt to memorize every single fact or each small piece of information; instead, we focus our intellectual energy on more important aspects of the task at hand. This selective attention not only simplifies the process but also aids in tackling complex problems more efficiently.

Following this anthropocentric intuition, we propose a novel use of Reinforcement Learning (RL) to equip LLMs with a dynamically updated fixed-length ‘memory’, as illustrated in [Figure 2](https://arxiv.org/html/2507.02259#S1.F2 "Figure 2 ‣ 1 Introduction ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"). During inference, the LLM processes the input text segment-by-segment. As it reads each segment, the model proactively and selectively updates the memory, which then contributes to the generation of the final output after all relevant messages are aggregated and synergized in the memory. This clever mechanism allows the LLM to flexibly handle arbitrary text lengths while maintaining a linear time complexity during processing, since the length of the memory is fixed, which leads to a fixed context window size for the model. This segment-based approach generates multiple outputs from a single long-text input, requiring multiple rounds of memory updates and a final round for the generation of the final response. Training this type of agent workflow, which enables dialogues across multiple independent contexts, is still an unexplored territory in current LLM study. Existing systems typically handle workflow trajectories via alternating tool calls or environment feedback by either simply concatenating ([Ouyang et al., 2025](https://arxiv.org/html/2507.02259#bib.bib41); [Jin et al., 2025](https://arxiv.org/html/2507.02259#bib.bib39)) them or using a sliding window ([Feng et al., 2025](https://arxiv.org/html/2507.02259#bib.bib40)) approach, which lacks flexibility and scalability in practice.
Our MemAgent approach, instead, proposes that treats each context-independent conversation as an optimization objective. Based on the DAPO ([Yu et al., 2025](https://arxiv.org/html/2507.02259#bib.bib32)) algorithm, we implement the Multi-Conv DAPO to optimize an arbitrary agent workflow by verifiable outcome reward.

In our experiments, an RL-trained model with a modest 8K context window (with a 1024-token memory and a 5000-token document chunk) trained on 60K length documents exhibits consistently superb capabilities for Question Answering (QA) tasks on documents of up to 3.5 million tokens, without performance drop and with linear computation cost. This demonstratively showcases the efficiency and scalability of our long-context memory approach.

Our major contributions are threefold:

* •

  We introduce a novel approach that enables LLMs to process arbitrarily long inputs within limited context window under linear time complexity during inference, overcoming a significant bottleneck in long-context processing.
* •

  We design an agent workflow to implement this mechanism and propose an end-to-end training approach using the multi-conversation DAPO algorithm.
* •

  We empirically demonstrate that our RL-trained method allows models to extrapolate to vastly long documents with minimal performance degradation, pushing the boundaries of what is currently achievable in long-context LLM systems.

![Refer to caption](https://arxiv.org/html/2507.02259v2/algo.png)

Figure 3: Comparison between vanilla GRPO and Multi-Conv DAPO. During the rollout phase of Multi-conv DAPO, each sample generates multiple conversations. The answer contained in the final conversation is used to compute the reward and advantage, which are then employed to optimize all preceding conversations.

## 2 Methodology

In this section, we describe the details of MemAgent approach for solving long-context tasks, including the overall workflow (§\mathsection [2.1](https://arxiv.org/html/2507.02259#S2.SS1 "2.1 The MemAgent Workflow: RL-shaped Memory for Unbounded Contexts ‣ 2 Methodology ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent")), Multi-conv RL algorithm for training MemAgent (§\mathsection [2.2](https://arxiv.org/html/2507.02259#S2.SS2 "2.2 Training MemAgent with Multi-conv RL ‣ 2 Methodology ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent")) and the formal modeling of our architecture(§\mathsection [2.3](https://arxiv.org/html/2507.02259#S2.SS3 "2.3 Rethinking MemAgent from Autoregressive Modeling Perspectives ‣ 2 Methodology ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent")).

### 2.1 The MemAgent Workflow: RL-shaped Memory for Unbounded Contexts

As illustrated in [Figure 2](https://arxiv.org/html/2507.02259#S1.F2 "Figure 2 ‣ 1 Introduction ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"), MemAgent views an arbitrarily long document not as a monolithic block but as a controlled stream of evidence.
At every step, the model sees exactly two things: the next chunk of text and a compact, fixed-length memory that summarizes everything deemed important so far.
Crucially, the memory is just a sequence of ordinary tokens inside the context window, so the core generation process of the base LLM remains unchanged.

After reading a new chunk, the model overwrites the previous memory with an updated one.
This overwrite strategy seems almost too simple, yet it is precisely what enables the system to scale:
because memory length never grows, the total compute per chunk stays O⁡(1)O(1) and end-to-end complexity is strictly linear to the number of chunks.
We formulate the overwrite decision as a reinforcement learning problem: the agent is rewarded for retaining information that will later prove useful and for discarding distractors that would waste precious tokens.
By optimizing this objective with our newly introduced multi-conversation DAPO algorithm (detailed in §\mathsection [2.2](https://arxiv.org/html/2507.02259#S2.SS2 "2.2 Training MemAgent with Multi-conv RL ‣ 2 Methodology ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent")), the model learns to compress aggressively while preserving answer-critical facts.

The workflow naturally decomposes inference into two modules.
Within the Context-Processing module the model iterates over chunks, updating memory with a prompt template (Table [5](https://arxiv.org/html/2507.02259#A1.T5 "Table 5 ‣ A.1 Prompt Template ‣ Appendix A Implementation Details ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"), top).
Once the stream is exhausted, a final Answer-Generation module is invoked (Table [5](https://arxiv.org/html/2507.02259#A1.T5 "Table 5 ‣ A.1 Prompt Template ‣ Appendix A Implementation Details ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"), bottom) where the model consults only the problem statement and the memory to produce its boxed answer.
Because positional embeddings are never re-scaled or patched, the same tokenization and attention layout apply in both modules, unlocking the model’s latent length-extrapolation capability without any architectural modifications.

MemAgent therefore enjoys three benefits from this design:
(1) Unlimited length: the document can be millions of tokens because it is processed as a stream;
(2) No performance cliff: RL encourages the memory to retain exactly the information needed, yielding near-lossless extrapolation (Figure [1](https://arxiv.org/html/2507.02259#S0.F1 "Figure 1 ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"));
(3) Linear cost: a constant window size implies decoding time and memory consumption grow linearly with input length (O⁡(N)O(N)) (detailed in §\mathsection [B](https://arxiv.org/html/2507.02259#A2 "Appendix B Computation Complexity ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent").)
This renders a practical recipe for turning any moderately context-sized LLM into an efficient long-context reasoner with minimal engineering overhead.

Figure 4: The architecture and graphic model of MemAgent. The memory is modeled as a latent memory variable, thereby enabling the decomposition of the autoregressive language model into multiple steps of reading from and writing to the memory.

### 2.2 Training MemAgent with Multi-conv RL

By viewing memory update in context processing for answer-generation tasks as part of the policy to be optimized by RL, we adopt the RLVR recipe ([OpenAI, 2024](https://arxiv.org/html/2507.02259#bib.bib18); [Guo et al., 2025](https://arxiv.org/html/2507.02259#bib.bib35); [Seed et al., 2025](https://arxiv.org/html/2507.02259#bib.bib23)) to train MemAgent.
We adopt DAPO ([Yu et al., 2025](https://arxiv.org/html/2507.02259#bib.bib32)), an efficient and effective algorithm refined from Group Relative Policy Optimization (GRPO) ([Shao et al., 2024](https://arxiv.org/html/2507.02259#bib.bib34)), as our training algorithm. Due to the nature of our MemAgent approach, which generates multiple context-independent conversations for a single query as illustrated in Figure [2](https://arxiv.org/html/2507.02259#S1.F2 "Figure 2 ‣ 1 Introduction ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"), we treat each conversation as an independent optimization target. This approach necessitates an extension of the loss computation from the conventional (group, token) structure to a new (group, conversation, token) dimensionality, as shown in Figure [3](https://arxiv.org/html/2507.02259#S1.F3 "Figure 3 ‣ 1 Introduction ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent").

Formally, the policy model πθold\pi\_{\theta\_{\text{old}}} samples a group of GG individual responses {oi,j}i=1G\{o\_{i,j}\}\_{i=1}^{G} for an input xx. Let nin\_{i} denote the number of generated conversations (oi,1,oi,2,…,oi,ni)(o\_{i,1},o\_{i,2},...,o\_{i,n\_{i}}) for a given sample (qi,ai)(q\_{i},a\_{i}). oi,jo\_{i,j} further decomposes into token-level outputs (oi,j,1,oi,j,2,…,oi,j,|oi,j|)(o\_{i,j,1},o\_{i,j,2},...,o\_{i,j,|o\_{i,j}|}). The advantage value is derived from the conversation that contains the final answer, then uniformly applied to all conversations originating from the same sample, as shown in Eq [1](https://arxiv.org/html/2507.02259#S2.E1 "Equation 1 ‣ 2.2 Training MemAgent with Multi-conv RL ‣ 2 Methodology ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"). Following Dr. GRPO ([Liu et al., 2025](https://arxiv.org/html/2507.02259#bib.bib33)), we do not devide the advantage by the standard deviation. Eq [2](https://arxiv.org/html/2507.02259#S2.E2 "Equation 2 ‣ 2.2 Training MemAgent with Multi-conv RL ‣ 2 Methodology ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent") describes our loss function.

|  |  |  |  |
| --- | --- | --- | --- |
|  | A^i,j,t=Ri−mean​({Ri}i=1G)\hat{A}\_{i,j,t}=R\_{i}-\text{mean}(\{R\_{i}\}\_{i=1}^{G}) |  | (1) |

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | 𝒥DAPO​(θ)=\displaystyle\mathcal{J}\_{\text{DAPO}}(\theta)= | 𝔼(q,a)∼𝒟,{oi,j}i=1G∼πθold(⋅∣q,oi,j−1)\displaystyle\mathbb{E}\_{(q,a)\sim\mathcal{D},\{o\_{i,j}\}\_{i=1}^{G}\sim\pi\_{\theta\_{\text{old}}}(\cdot\mid q,~o\_{i,j-1})} |  | (2) |
|  |  | [1∑i=1G∑j=1ni|oi,j|∑i=1G∑j=1ni∑t=1|oi,j|(𝒞i,j,t−βDKL(πθ||πref)]\displaystyle\Bigg[\frac{1}{\sum\_{i=1}^{G}\sum\_{j=1}^{n\_{i}}|o\_{i,j}|}\sum\_{i=1}^{G}\sum\_{j=1}^{n\_{i}}\sum\_{t=1}^{|o\_{i,j}|}\Big(\mathcal{C}\_{i,j,t}-\beta D\_{\text{KL}}(\pi\_{\theta}||\pi\_{\text{ref}}\Big)\Bigg] |  |
|  | where ​𝒞i,j,t=\displaystyle\text{where\quad}\mathcal{C}\_{i,j,t}= | min⁡(ri,j,t​(θ)​A^i,j,t,clip​(ri,j,t​(θ),1−εl​o​w,1+εh​i​g​h)​A^i,j,t)\displaystyle\min\Big(r\_{i,j,t}(\theta)\hat{A}\_{i,j,t},\ \text{clip}\Big(r\_{i,j,t}(\theta),1-\varepsilon\_{low},1+\varepsilon\_{high}\Big)\hat{A}\_{i,j,t}\Big) |  |
|  | ri,j,t​(θ)=\displaystyle r\_{i,j,t}(\theta)= | πθ​(oi,j,t∣q,oi,j,<t)πθold​(oi,j,t∣q,oi,j,<t).\displaystyle\frac{\pi\_{\theta}(o\_{i,j,t}\mid q,o\_{i,j,<t})}{\pi\_{\theta\_{\text{old}}}(o\_{i,j,t}\mid q,o\_{i,j,<t})}. |  |

Following the RLVR recipe ([Guo et al., 2025](https://arxiv.org/html/2507.02259#bib.bib35); [Jin et al., 2025](https://arxiv.org/html/2507.02259#bib.bib39); [Yu et al., 2025](https://arxiv.org/html/2507.02259#bib.bib32)),
we train the model with a final outcome reward computed by a rule-based verifier:

|  |  |  |  |
| --- | --- | --- | --- |
|  | R⁡(y^,y)=𝟏is\_equiv​(y,y^)R(\hat{y},y)=\displaystyle\bm{1}\_{\mathrm{\texttt{is\\_equiv}(y,\hat{y})}} |  | (3) |

where y^\hat{y} is the predicted answer while yy refers to the ground truth.

Table 1: Main experimental results comparing model performance across various context lengths. All values represent accuracy (%).

Model
Length

7K
14K
28K
56K
112K
224K
448K
896K
1.75M
3.5M

QwenLong-L1-32B
72.66
75.00
72.66
60.94
31.25
17.19
13.28
11.72
N/A
N/A

Qwen2.5-Instruct-14B-1M
60.16
60.94
50.00
57.03
50.00
37.50
8.59
0.00
N/A
N/A

Qwen2.5-Instruct-7B-1M
61.72
56.25
53.91
55.47
51.56
33.59
12.50
0.00
N/A
N/A

DS-Distill-Qwen-32B
70.31
66.41
65.62
46.88
23.44
13.28
7.81
7.03
N/A
N/A

DS-Distill-Qwen-14B
64.06
64.84
57.03
40.62
14.84
8.59
3.12
6.25
N/A
N/A

DS-Distill-Qwen-7B
30.47
12.50
3.12
0.00
0.00
0.78
0.00
0.00
N/A
N/A

Qwen2.5-Instruct-32B
69.53
64.84
60.16
51.56
44.53
21.88
14.06
7.03
N/A
N/A

Qwen2.5-Instruct-14B
75.00
67.19
57.03
54.69
44.53
21.88
10.94
2.34
N/A
N/A

Qwen2.5-Instruct-7B
52.34
57.03
51.56
44.53
32.81
13.28
6.25
1.56
N/A
N/A

RL-MemAgent-14B
80.47
82.03
82.03
83.59
81.25
77.34
79.69
75.78
78.91
71.09

RL-MemAgent-7B
81.25
81.25
82.03
80.47
79.69
75.78
76.56
74.22
77.34
71.88

### 2.3 Rethinking MemAgent from Autoregressive Modeling Perspectives

Tto get a deeper sense of the MemAgent design, we propose to re-think language-model factorization in the following fashion.
A standard autoregressive LLM factorizes the joint likelihood of a sequence 𝐱1:N\mathbf{x}\_{1:N} as
p(𝐱1:N)=∏n=1Np(xn∣𝐱1:n−1),p(\mathbf{x}\_{1:N})=\prod\_{n=1}^{N}p(x\_{n}\mid\mathbf{x}\_{1:n-1}),
implicitly assuming that every past token (or at least its hidden state) must stay in the active context.
This is what turns quadratic attention into the long-context bottleneck.

MemAgent replaces the unbounded history with a fixed-length memory 𝐦∈𝕍M\mathbf{m}\!\in\!\mathbb{V}^{M}, as shown in Figure [4](https://arxiv.org/html/2507.02259#S2.F4 "Figure 4 ‣ 2.1 The MemAgent Workflow: RL-shaped Memory for Unbounded Contexts ‣ 2 Methodology ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent").
The input text is streamed through the model in KK contiguous chunks
𝐜1,…,𝐜K\mathbf{c}^{1},\dots,\mathbf{c}^{K} (each of length ≤C\leq C).
After chunk kk is read, the model overwrites the panel with a new vector 𝐦k\mathbf{m}^{k} that summarizes all evidence seen so far.
Because |𝐦k|=M|\mathbf{m}^{k}|=M is constant, both compute and memory per step are O⁡(C+M)O(C+M), yielding an overall linear complexity O⁡(N)O(N).

Introducing the latent sequence 𝐦1:K−1\mathbf{m}^{1:K-1} decomposes the original likelihood as

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | p(𝐱1:N)\displaystyle p(\mathbf{x}\_{1:N}) | =∑𝐦1:K−1∏k=1Kp⁡(𝐜k∣𝐦k−1)⏟readp⁡(𝐦k∣𝐜k,𝐦k−1)⏟write,\displaystyle=\!\!\!\!\sum\_{\mathbf{m}^{1:K-1}}\prod\_{k=1}^{K}\underbrace{p(\mathbf{c}^{k}\mid\mathbf{m}^{k-1})}\_{\text{read}}\;\underbrace{p(\mathbf{m}^{k}\mid\mathbf{c}^{k},\mathbf{m}^{k-1})}\_{\text{write}}, |  | (4) |

with base case 𝐦0=∅\mathbf{m}^{0}=\varnothing.
Inside each chunk, we still run an ordinary transformer decoder, but conditioned on a constant context window
(𝐜k,𝐦k−1)(\mathbf{c}^{k},\mathbf{m}^{k-1}).
The read path factorizes token-by-token,
p(𝐜k∣𝐦k−1)=∏i=(k−1)​C+1k​Cp(xi∣𝐱1:i−1,𝐦k−1),p(\mathbf{c}^{k}\mid\mathbf{m}^{k-1})=\!\!\!\prod\_{i=(k-1)C+1}^{kC}\!p(x\_{i}\mid\mathbf{x}\_{1:i-1},\mathbf{m}^{k-1}),
while the write path generates the next memory in the same autoregressive fashion.

In our formulation, the model’s reading and writing operations over the context constitute an Markov Decision Process(MDP) and the objective of RL is to optimize the final reward obtained by this MDP. Therefore, MemAgent’s learning objective is to generate a read–write memory trajectory that maximizes the reward, which corresponds to learning an optimal distribution over memory states conditioned on the input context. This further theoretically illustrates the intrinsic unity between our RL formulation and long-text modeling.

Table 2: Model performance on LongBench-SUM. All values represent recall rates (%). Bold marks the highest value and Underline marks the second highest value in each column.

|  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Model | GOV REPORT | | | | QMSUM | | | |
| ROUGE-1 | ROUGE-2 | ROUGE-L | AVG | ROUGE-1 | ROUGE-2 | ROUGE-L | AVG |
| Qwen2.5-Instruct-32B | 23.67 | 8.46 | 12.57 | 14.90 | 47.77 | 11.29 | 28.17 | 29.08 |
| Qwen2.5-Instruct-14B | 31.19 | 10.96 | 14.96 | 19.04 | 47.53 | 11.46 | 28.28 | 29.09 |
| Qwen2.5-Instruct-7B | 30.91 | 11.68 | 15.20 | 19.26 | 46.64 | 12.01 | 28.33 | 28.99 |
| QwenLong-L1 | 27.60 | 8.20 | 13.07 | 16.29 | 39.44 | 8.24 | 23.56 | 23.74 |
| Qwen2.5-Instruct-14B-1M | 30.58 | 11.93 | 15.51 | 19.34 | 47.31 | 13.13 | 29.07 | 29.84 |
| Qwen2.5-Instruct-7B-1M | 31.02 | 11.47 | 15.30 | 19.26 | 46.72 | 12.33 | 28.66 | 29.24 |
| DS-Distill-Qwen-32B | 26.13 | 8.86 | 12.98 | 15.99 | 39.09 | 8.75 | 23.96 | 23.93 |
| DS-Distill-Qwen-14B | 28.24 | 9.72 | 13.78 | 17.25 | 41.25 | 8.95 | 25.00 | 25.07 |
| DS-Distill-Qwen-7B | 33.30 | 9.39 | 14.59 | 19.10 | 34.33 | 5.97 | 21.57 | 20.62 |
| RL-MemAgent-14B | 37.16 | 12.03 | 16.23 | 21.80 | 50.21 | 12.70 | 31.27 | 31.39 |
| RL-MemAgent-7B | 30.28 | 12.37 | 15.37 | 19.34 | 48.49 | 14.41 | 30.91 | 31.27 |

## 3 Experiments

### 3.1 Experimental Setup

Training Details. To maintain comparability with previous work, we choose Qwen2.5-7B-Instruct and Qwen2.5-14B-Instruct ([Yang et al., 2024](https://arxiv.org/html/2507.02259#bib.bib36)) as backbone models. We implement the framework for multi-conversation with independent contexts based on verl ([Sheng et al., 2024](https://arxiv.org/html/2507.02259#bib.bib43)).

We employ a two-stage curriculum RL strategy:

Table 3: Model performance on LongBench-QA.

Method
2Wiki
HQA
MuSiQue
NQA
Qasper
AVG

QwenLong-L1-32B
83.0
69.5
51.0
26.0
24.0
50.7

Qwen2.5-Instruct-14B-1M
70.5
65.5
35.0
22.0
22.0
43.0

Qwen2.5-Instruct-7B-1M
67.5
58.5
26.0
21.5
24.0
39.5

DS-Distill-Qwen-32B
83.5
69.0
47.5
24.0
21.0
49.0

DS-Distill-Qwen-14B
83.5
67.0
42.0
22.0
22.0
47.3

DS-Distill-Qwen-7B
47.0
31.5
7.5
4.0
17.5
21.5

Qwen2.5-Instruct-32B
68.5
66.0
37.0
24.5
22.5
43.7

Qwen2.5-Instruct-14B
67.0
63.5
39.0
20.0
20.5
42.0

Qwen2.5-Instruct-7B
52.5
59.0
24.0
19.0
19.0
34.7

MemAgent-14B
79.0
73.0
52.0
25.0
26.0
51.0

MemAgent-7B
74.0
69.5
47.0
21.5
29.0
48.2

OPEN1)1) stage I focuses on enabling the model to acquire fundamental memory capabilities; OPEN2)2) stage II trains the model to transfer these capabilities to more diverse contexts and challenging tasks. Specific hyperparameters for training are detailed in §\mathsection [A.3](https://arxiv.org/html/2507.02259#A1.SS3 "A.3 Training ‣ Appendix A Implementation Details ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent").

During training, we intentionally limit the model to an 8K context window to demonstrate its extrapolation capabilities. This 8K window is allocated as follows: 1024 tokens for the query, 5000 tokens for the context chunk, 1024 tokens for the memory, and 1024 tokens for the output, with the remaining tokens reserved for the chat template.

Benchmarks.
We conduct comprehensive evaluations on several long-text benchmarks to assess the model’s capabilities across various text types and tasks.

1. 1.

   RULER-HQA. This benchmark is created using the same synthetic method as in the first-stage training data. It consists of tasks with a moderate information density and controllable length, where the context distribution is close to natural language, serving as a quantitative evaluation of extrapolation performance.
2. 2.

   LongBench-QA. This benchmark is composed of NarrativeQA ([Kočiskỳ et al., 2018](https://arxiv.org/html/2507.02259#bib.bib8)), Qasper ([Dasigi et al., 2021](https://arxiv.org/html/2507.02259#bib.bib9)), HotpotQA ([Yang et al., 2018](https://arxiv.org/html/2507.02259#bib.bib69)), 2WikiMultihopQA [Ho et al. (2020)](https://arxiv.org/html/2507.02259#bib.bib7), and MuSiQue ([Trivedi et al., 2022](https://arxiv.org/html/2507.02259#bib.bib6)). The tasks are relatively short but have a high information density, which severely tests the model’s flexible memory management. It also evaluates the model’s ability to generalize its memory capabilities to various materials, such as novels, news articles, and Wiki items.
3. 3.

   NIAH. Needle in a haystack (NIAH) ([Kamradt, 2023](https://arxiv.org/html/2507.02259#bib.bib13)) is a series of extremely long synthetic tasks with very low information density. To succeed, the model must identify key information and maintain its integrity throughout a long process, thereby testing the robustness of memory.
4. 4.

   LongBench-SUM. We also adopt two long-context summay tasks, GovReport([Huang et al., 2021](https://arxiv.org/html/2507.02259#bib.bib4)) and QMSum([Zhong et al., 2021](https://arxiv.org/html/2507.02259#bib.bib5)) from LongBench([Bai et al., 2024](https://arxiv.org/html/2507.02259#bib.bib3)) to evaluate the performance in different task category that is different from retrieval QA.

Baselines. We use DeepSeek-R1-Distill-Qwen ([Guo et al., 2025](https://arxiv.org/html/2507.02259#bib.bib35)), Qwen-2.5-Instruct-1M ([Yang et al., 2025](https://arxiv.org/html/2507.02259#bib.bib38)) , Qwen-2.5-Instruct ([Yang et al., 2024](https://arxiv.org/html/2507.02259#bib.bib36))and QwenLong-L1 ([Wan et al., 2025](https://arxiv.org/html/2507.02259#bib.bib37)) as baselines. Their generation configurations are shown in Table [6](https://arxiv.org/html/2507.02259#A1.T6 "Table 6 ‣ A.4 Evaluation ‣ Appendix A Implementation Details ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"), while MemAgent uses the same context management as described previously in Training Details.
We also compare MemAgent with other agent method, detailed in §\mathsection .

![Refer to caption](https://arxiv.org/html/2507.02259v2/niah_single_combined_multi_2x2.png)

Figure 5: Performance heatmaps on NIAH benchmark across different context lengths.

### 3.2 Main Results

RULER-HQA. The results are reported in Table [1](https://arxiv.org/html/2507.02259#S2.T1 "Table 1 ‣ 2.2 Training MemAgent with Multi-conv RL ‣ 2 Methodology ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"). We conduct a comparative analysis of all model performances with context lengths ranging from 7K to 896K. For MemAgent, we extend the evaluation to ultra-long contexts of 1.75M and 3.5M to assess its extrapolation capabilities.

MemAgent exhibits remarkable length extrapolation capabilities with only marginal performance decay as the input context-length increases. In contrast, baseline models show distinct failure patterns. DS-Distill-Qwen series show rapid performance degradation. QwenLong-L1 maintains reasonable performance within its training length but experiences substantial degradation afterward. The Qwen2.5-Instruct-1M series maintains acceptable performance up to 112K tokens, but the performance deteriorates to zero at 896K tokens, well before reaching their theoretical 1M token capacity. This suggests that despite extended context windows, these models struggle with effective information utilization in ultra-long contexts.

LongBench-QA. The results on the LongBench-QA benchmark are presented in Table [3](https://arxiv.org/html/2507.02259#S3.T3 "Table 3 ‣ 3.1 Experimental Setup ‣ 3 Experiments ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"). MemAgent demonstrates superior overall performance, outperforming larger long-context or reasoning models. Reasoning models such as the DS-Distill families and the QwenLong model which are trained on a complex dataset, exhibit strong performance. In contrast, the Qwen2.5-Instruct-1M series shows limited improvement over its backbone model. This suggests that LongBench-QA emphasize a deeper understanding of text rather than simple retrieval ability. The performance of MemAgent demonstrates that the memory capabilities acquired through reinforcement learning are generalizable.

NIAH.
We adopt three variants of NIAH from the RULER benchmark [Hsieh et al. (2024)](https://arxiv.org/html/2507.02259#bib.bib15) with increasing difficulty across three levels.
As depicted in Figure [5](https://arxiv.org/html/2507.02259#S3.F5 "Figure 5 ‣ 3.1 Experimental Setup ‣ 3 Experiments ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"), the majority of baselines struggle to maintain consistent performance even within a 128K context window, even Qwen2.5-Instruct-1M also experience a performance drop at 512K. RL-MemAgent, despite suffering some performance fluctuations, shows only a minimal performance loss of less than 5% at 512K. This robust performance is particularly noteworthy given that the evaluation at 512K involves more than 100 turns of dialogue.

LongBench-SUM. We evaluate summary quality by the recall scores of ROUGE-{1,2,L}. RL-MemAgent achieves SOTA on almost all metrics, demonstrating that the model has learned general memory and context management capabilities, rather than abilities specific to the QA task.

### 3.3 Ablation Study

Figure 6: Ablation result of RL training on RULER-HQA.

Figure 7: Ablation result of RL training on Longbench-QA.

#### 3.3.1 RL Training

To investigate the impact of reinforcement learning, we conduct ablation experiments. The results of RULER-HQA and NIAH are presented in Figure [7](https://arxiv.org/html/2507.02259#S3.F7 "Figure 7 ‣ 3.3 Ablation Study ‣ 3 Experiments ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent") and Figure [5](https://arxiv.org/html/2507.02259#S3.F5 "Figure 5 ‣ 3.1 Experimental Setup ‣ 3 Experiments ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"), respectively. MemAgent without reinforcement learning training outperforms the backbone models; however, it still exhibits a substantial decline in performance as the input length increases. The results of Longbench-QA, shown in Figure [7](https://arxiv.org/html/2507.02259#S3.F7 "Figure 7 ‣ 3.3 Ablation Study ‣ 3 Experiments ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"), demonstrate that directly applying MemAgent leads to only marginal or even negative improvements. In contrast, RL-MemAgent achieves significant improvements in both evaluation scenarios, indicating reinforcement learning training is essential to develop generalizable and robust memory abilities.

#### 3.3.2 Memory Length

Selecting an appropriate MemAgent setting involves certain trade-offs. A larger memory size allows the model to store more useful information, but it also introduces challenges in memory management and increases the likelihood of redundancy. Conversely situation may lead to insufficient storage capacity, leaving the model without the necessary references.

To achieve a reasonable compression ratio while keeping the total context length within 8,192 tokens, we set the default configuration of MemAgent to use a 1,024-token memory and context chunks of 5,000 tokens, based on preliminary validation results.

To investigate the effect of hyperparameter choices, we conduct an ablation study on memory length ranging from 256 to 4096. The results presented in Figure [8](https://arxiv.org/html/2507.02259#S3.F8 "Figure 8 ‣ 3.3.3 Context Distribution ‣ 3.3 Ablation Study ‣ 3 Experiments ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent") and Figure [9](https://arxiv.org/html/2507.02259#S3.F9 "Figure 9 ‣ 3.3.3 Context Distribution ‣ 3.3 Ablation Study ‣ 3 Experiments ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"), showing that our chosen configuration constitutes a reasonable sweet spot, and that MemAgent ’s performance is robust over different memory size. We further examine the impact of varying the context size in §\mathsection  and observe similar trends.

#### 3.3.3 Context Distribution

Although our experiments show that MemAgent can effectively extrapolate to a length of 3.5M tokens, we still wish to examine whether MemAgent is affected by issues such as information-overwritten and the lost-in-the-middle phenomenon. Our hypothesis is that overcoming such problem is a natural result of end-to-end optimization. During training, the model learns to preserve and track critical information in order to maximize the final reward.

To validate this hypothesis, we carefully design a set of probing experiments based on RULER-HQA, where the context is consist of some key information and many distractors. We divided the key information into two groups and placed them at different positions within the context. We constructed five settings: (0%, 100%), (20%, 80%), (40%, 60%), (0%, 20%), and (80%, 100%), where 0% indicates the beginning of the context and 100% means the end of the context.

For example, in the (0%, 100%) case, the model sees one piece of key information at the very beginning and the other only at the final memory update step. This represents one of the most challenging scenarios for the information-overwritten problem. While (40%, 60%) may serve as a challenging lost-in-the-middle setting.

The results shown in table [4](https://arxiv.org/html/2507.02259#S3.T4 "Table 4 ‣ 3.3.3 Context Distribution ‣ 3.3 Ablation Study ‣ 3 Experiments ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent") indicates that MemAgent remains consistently robust across all patterns without exhibiting any catastrophic performance degradation. This strongly supports our hypothesis that the general memory abilities acquired through trial and error are not tied to any particular context pattern.

![Refer to caption](https://arxiv.org/html/2507.02259v2/niah_single_abl_combined_multi_2x2.png)

Figure 8: Ablation result of memory-length on NIAH

Figure 9: Ablation result of memory-length on Longbench

Table 4: Probe experiment results. Ctx. Dist. denotes the context distribution, where the two numbers correspond to the relative positions of the two key-information groups within the entire context. 0% means the beginning and 100% means the end. random indicates randomly shuffling all context items, consistent with the setup in the main experiment. The other rows show the performance difference relative to random. All values represent accuracy (%).

|  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Model | Ctx. Dist. | Length | | | | | | | |
| 7K | 14K | 28K | 56K | 112K | 224K | 448K | AVG |
| 14B | random | 80.47 | 82.03 | 82.03 | 83.59 | 81.25 | 77.34 | 79.69 | 75.78 |
|  | 0% 20% | +3.91 | -3.91 | +3.13 | +1.57 | 0.00 | +4.69 | +3.90 | +1.90 |
|  | 0% 100% | +3.12 | +0.78 | +3.13 | -3.12 | +1.56 | +7.82 | +6.25 | +2.79 |
|  | 20% 80% | +0.78 | -3.12 | +2.35 | +0.79 | -3.13 | +5.47 | -3.13 | 0.00 |
|  | 40% 60% | +1.56 | +2.35 | -2.34 | -3.12 | -1.56 | +3.13 | -0.78 | -0.11 |
|  | 80% 100% | -2.35 | 0.00 | +1.56 | +0.79 | +3.13 | 0.00 | +1.56 | +0.67 |
| 7B | random | 81.25 | 81.25 | 82.03 | 80.47 | 79.69 | 75.78 | 76.56 | 79.58 |
|  | 0% 20% | -1.56 | -0.78 | +3.13 | +3.91 | +3.12 | +5.47 | +3.13 | +2.35 |
|  | 0% 100% | +0.78 | 0.00 | +2.35 | +1.56 | +3.90 | +4.69 | +2.35 | +2.23 |
|  | 20% 80% | -0.78 | -0.78 | +2.35 | 0.00 | 0.00 | 0.00 | +3.13 | +0.56 |
|  | 40% 60% | 0.00 | +1.56 | +3.13 | +0.78 | -3.91 | +3.13 | +5.47 | +1.45 |
|  | 80% 100% | +1.56 | 0.00 | +0.78 | -0.78 | +0.78 | +4.69 | 0.00 | +1.00 |

## 4 Related Work

Long Context LLMs. Extrapolation methods for RoPE-based LLMs ([Su et al., 2024](https://arxiv.org/html/2507.02259#bib.bib44)), such as NTK ([bloc97, 2023](https://arxiv.org/html/2507.02259#bib.bib45)), PI ([Chen et al., 2023](https://arxiv.org/html/2507.02259#bib.bib46)), YaRN ([Peng et al., 2023b](https://arxiv.org/html/2507.02259#bib.bib16)) and DCA ([An et al., 2024](https://arxiv.org/html/2507.02259#bib.bib47)), modify the components of positional embeddings, enabling the model to capture long-range semantic dependencies. On the other hand, Linear attention mechanisms ([Child et al., 2019](https://arxiv.org/html/2507.02259#bib.bib55); [Katharopoulos et al., 2020](https://arxiv.org/html/2507.02259#bib.bib59)), Recurrent Neural Networks (RNNs) and State Space Models (SSMs) ([Gu et al., 2021](https://arxiv.org/html/2507.02259#bib.bib48); [Gu and Dao, 2023](https://arxiv.org/html/2507.02259#bib.bib49); [Peng et al., 2023a](https://arxiv.org/html/2507.02259#bib.bib50); [De et al., 2024](https://arxiv.org/html/2507.02259#bib.bib51); [Feng et al., 2024](https://arxiv.org/html/2507.02259#bib.bib52)), sparse attention  ([Beltagy et al., 2020](https://arxiv.org/html/2507.02259#bib.bib58); [Zhao et al., 2019](https://arxiv.org/html/2507.02259#bib.bib56); [Xiao et al., 2023](https://arxiv.org/html/2507.02259#bib.bib57); [Yuan et al., 2025](https://arxiv.org/html/2507.02259#bib.bib70); [Lu et al., 2025](https://arxiv.org/html/2507.02259#bib.bib71)) focus on architecture improvements. Chunk strategy have also been explored in long-context modeling  ([Li et al., 2025b](https://arxiv.org/html/2507.02259#bib.bib2); [Liao et al., 2025](https://arxiv.org/html/2507.02259#bib.bib1)), while MemAgent aims to equip memory ability to any backbone model via post-training with standard RL frameworks without heavily changing on architecture.

Memory Mechanism. The Long Short-Term Memory (LSTM) mechanism  ([Hochreiter and Schmidhuber, 1997](https://arxiv.org/html/2507.02259#bib.bib66)) achieved significant success in early NLP tasks, while Neural Turing Machines  ([Graves et al., 2014](https://arxiv.org/html/2507.02259#bib.bib67)) and Memory Networks ([Weston et al., 2014](https://arxiv.org/html/2507.02259#bib.bib68)) demonstrated how to equip neural networks with memory. Existing memory mechanisms integrated to Transformer models are typically realized by adding external memory modules ([Martins et al., 2021](https://arxiv.org/html/2507.02259#bib.bib73); [Wu et al., 2020](https://arxiv.org/html/2507.02259#bib.bib72); [Behrouz et al., 2024](https://arxiv.org/html/2507.02259#bib.bib53); [Bulatov et al., 2023](https://arxiv.org/html/2507.02259#bib.bib75)) or external database ([Zhong et al., 2024](https://arxiv.org/html/2507.02259#bib.bib78); [Lu et al., 2023](https://arxiv.org/html/2507.02259#bib.bib76); [Modarressi et al., 2023](https://arxiv.org/html/2507.02259#bib.bib77)). Recently, retrieval-augmented memory agent ([Fang et al., 2025](https://arxiv.org/html/2507.02259#bib.bib11); [Chhikara et al., 2025](https://arxiv.org/html/2507.02259#bib.bib10); [Zhou et al., 2025](https://arxiv.org/html/2507.02259#bib.bib12)) workflows have attracted the community’s attention. The diffrence between MemAgent and other agent is that we use reinforcement learning to enable LLM itself the ability to memorize.

Reinforcement Learning for LLMs. In recent RL studies, the reward signals have gradually shifted from human preferences  ([Ouyang et al., 2022](https://arxiv.org/html/2507.02259#bib.bib28)) or reward models distilled from them ([Bai et al., 2022](https://arxiv.org/html/2507.02259#bib.bib74)) to rule-based feedback, which has demonstrated great potential in enhancing model reasoning capabilities ([OpenAI, 2024](https://arxiv.org/html/2507.02259#bib.bib18); [Guo et al., 2025](https://arxiv.org/html/2507.02259#bib.bib35); [Qwen, 2024](https://arxiv.org/html/2507.02259#bib.bib22); [DeepMind, 2024](https://arxiv.org/html/2507.02259#bib.bib21); [Team et al., 2025](https://arxiv.org/html/2507.02259#bib.bib27)) with GAE ([Schulman et al., 2018](https://arxiv.org/html/2507.02259#bib.bib30)) based PPO  ([Schulman et al., 2017](https://arxiv.org/html/2507.02259#bib.bib29)) or GRPO ([Shao et al., 2024](https://arxiv.org/html/2507.02259#bib.bib34)) training. Algorithmic enhancements ([Hu, 2025](https://arxiv.org/html/2507.02259#bib.bib31); [Yu et al., 2025](https://arxiv.org/html/2507.02259#bib.bib32); [Liu et al., 2025](https://arxiv.org/html/2507.02259#bib.bib33)) have mostly focused on improving sustainability and efficiency of these algorithms. To further release the potential of RL, recent works such as Search-R1 ([Jin et al., 2025](https://arxiv.org/html/2507.02259#bib.bib39)), Agent-R1 ([Ouyang et al., 2025](https://arxiv.org/html/2507.02259#bib.bib41)) and RAGEN ([Wang et al., 2025](https://arxiv.org/html/2507.02259#bib.bib42)) have explored the training of tool-using agents based on multi-turn chat. GiGPO ([Feng et al., 2025](https://arxiv.org/html/2507.02259#bib.bib40)) further investigates the use of multiple independent contexts in agent training.

## 5 Conclusion

In this paper, we introduce MemAgent, a novel long-context method that employs an RL-trained memory module, which enables large language models (LLMs) to selectively record relevant information while disregarding extraneous details. Our experiments demonstrate that when trained on 60K-length sequences, MemAgent exhibits remarkable extrapolation, extending its effective context to 3.5M tokens with only 8K context. The model achieves state-of-the-art performance across a diverse range of long-context tasks. Our ablation studies reveal the critical role of RL-based training in achieving these results and how memory capacity influences performance across different task types, providing key insights into the proposed memory mechanism. We hope that this work may lay a strong foundation for developing more advanced memory architectures and training strategies, thereby paving the way for significantly enhancing the long-context capabilities of LLMs.

## Reproducibility statement

For reproducibility, we have provided the inplementation details in (§\mathsection [A](https://arxiv.org/html/2507.02259#A1 "Appendix A Implementation Details ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent")), including the prompt template (§\mathsection [A.1](https://arxiv.org/html/2507.02259#A1.SS1 "A.1 Prompt Template ‣ Appendix A Implementation Details ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent")), pseudocode (§\mathsection [A.2](https://arxiv.org/html/2507.02259#A1.SS2 "A.2 Algorithm ‣ Appendix A Implementation Details ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent")) and training recipe and algorithm hyperparameter (§\mathsection [A.3](https://arxiv.org/html/2507.02259#A1.SS3 "A.3 Training ‣ Appendix A Implementation Details ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent")) and evaluation settings (§\mathsection [A.4](https://arxiv.org/html/2507.02259#A1.SS4 "A.4 Evaluation ‣ Appendix A Implementation Details ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent")). The training and evaluation code, as well as the dataset and model weights, will be available in open-source platforms.

## Appendix A Implementation Details

### A.1 Prompt Template

|  |
| --- |
| You are presented with a problem, a section of an article that may contain the answer, and a previous memory. Please read the section carefully and *update the memory* with new information that helps to answer the problem, while retaining all relevant details from the previous memory. |
| <problem> {prompt} </problem> |
| <memory> {memory} </memory> |
| <section> {chunk} </section> |
| Updated memory: |
| You are presented with a problem and a previous memory. Please answer the problem based on the previous memory and put the answer in `\boxed{}`. |
| <problem> {prompt} </problem> |
| <memory> {memory} </memory> |
| Your answer: |

Table 5: Template of MemAgent for context processing (top part) and final
answer generation (bottom). Curly-brace placeholders {} will be replaced
with actual content.

### A.2 Algorithm

Algorithm 1  Multi-conv DAPO

1:
Policy model πθ\pi\_{\theta}, reference model πref\pi\_{\mathrm{ref}} (frozen),
rule-based verifier VV, dataset 𝒟\mathcal{D}, group size GG

2:
while not converged do

3:
  Sample a prompt q∼𝒟q\sim\mathcal{D}

4:
  for g=1g=1 to GG do ⊳\triangleright Group of conversations for the same qq

5:
   Initialize hg,0←[q]h\_{g,0}\leftarrow[q]

6:
   for t=1t=1 to cgc\_{g} do ⊳\triangleright Context-independent conversation

7:
     Sample og,t∼πθ(⋅∣hg,t−1)o\_{g,t}\sim\pi\_{\theta}(\cdot\mid h\_{g,t-1})

8:
     hg,t←hg,t−1∥og,th\_{g,t}\leftarrow h\_{g,t-1}\mathbin{\|}o\_{g,t}

9:
   end for

10:
   yg←og,cgy\_{g}\leftarrow o\_{g,c\_{g}} ⊳\triangleright Final response used for scoring

11:
   r^g←V⁡(q,yg)\hat{r}\_{g}\leftarrow V(q,y\_{g}) ⊳\triangleright Rule-based reward

12:
   dg←KL(πθ(⋅∣hg,cg)∥πref(⋅∣hg,cg))d\_{g}\leftarrow\mathrm{KL}\big(\pi\_{\theta}(\cdot\mid h\_{g,c\_{g}})\,\|\,\pi\_{\mathrm{ref}}(\cdot\mid h\_{g,c\_{g}})\big)

13:
   rg←r^g−β​dgr\_{g}\leftarrow\hat{r}\_{g}-\beta d\_{g}

14:
  end for

15:
  {Ag}g=1G←GroupNorm⁡({rg}g=1G)\{A\_{g}\}\_{g=1}^{G}\leftarrow\mathrm{GroupNorm}(\{r\_{g}\}\_{g=1}^{G})

16:
  for g=1g=1 to GG do

17:
   ρg←πθ​(yg∣hg,cg)πθold​(yg∣hg,cg)\rho\_{g}\leftarrow\dfrac{\pi\_{\theta}(y\_{g}\mid h\_{g,c\_{g}})}{\pi\_{\theta\_{\text{old}}}(y\_{g}\mid h\_{g,c\_{g}})}

18:
   𝒥g←min⁡(ρg​Ag,clip⁡(ρg,1−ϵl​o​w,1+ϵh​i​g​h)​Ag)\mathcal{J}\_{g}\leftarrow\min\big(\rho\_{g}A\_{g},\,\mathrm{clip}(\rho\_{g},1-\epsilon\_{low},1+\epsilon\_{high})A\_{g}\big)

19:
  end for

20:
  𝒥clip←1G​∑g=1G𝒥g\mathcal{J}\_{\mathrm{clip}}\leftarrow\frac{1}{G}\sum\_{g=1}^{G}\mathcal{J}\_{g}

21:
  θ←θ+η​∇θ𝒥clip\theta\leftarrow\theta+\eta\nabla\_{\theta}\mathcal{J}\_{\mathrm{clip}}

22:
end while

### A.3 Training

We use the DAPO algorithm for training, applying a KL factor of 1×10−31\times 10^{-3} and disabling the entropy loss. The AdamW optimizer is employed with a constant learning rate of 1×10−61\times 10^{-6} and a linear warm-up scheduler, with the wram-up step set to 20. We use a rollout batchsize of 256, with a group size of 16. Note that due to the multi-conversation feature of MemAgent, the actual mini-batchsize is not equal to rollout batchsize/16. We utilize off-policy training by fixing the ratio of the sample batch size to the backpropagation batch size is set to 16.

We shift to stage II when stage I are fully converged, which takes about 400 steps. Here is the training data recipe of each stage.

* •

  Stage I We use 32,768 synthetic QA data instances, each approximately 32K tokens in length. These are based on the HotpotQA ([Yang et al., 2018](https://arxiv.org/html/2507.02259#bib.bib69)) dataset and follow the RULER ([Hsieh et al., 2024](https://arxiv.org/html/2507.02259#bib.bib15)) methodology, which involves embedding golden paragraphs (containing correct answers) within extensive distractor content sampled from the same dataset.
* •

  Stage II We use 2,560 training instances with a maximum length of 60K tokens. This set consists of difficult, high-quality long-text QA data from DocQA-RL-1.6K ([Wan et al., 2025](https://arxiv.org/html/2507.02259#bib.bib37)), mixed with data from the first stage.

Each training sample used in stage I is of 200 articles in HotpotQA, with an approximate total token length of 28K. We thoroughly clean the dataset by filtering out questions where Qwen2.5-7B-Base or Qwen2.5-7B-Instruct achieves 100 % Best-Of-2 score without given any context. These questions likely represent common knowledge already internalized within the models’ memories. 80,000 samples from the HotpotQA training split are processed through this pipeline and approximately 50% of the data are filtered out. We chose the frist 32,768 samples of processed data as our training set.

We then apply a similar approach to synthesize 128 samples from the HotpotQA validation set. For extrapolation performance testing, we synthesize test sets with different context lengths using the same pipeline. The number of wiki items ranges from 50 up to 6400, corresponding to context lengths of approximately 7K to 3.5M tokens.

### A.4 Evaluation

We extract answers from the model outputs using regular expressions, and we prompt the model to respond in the specified format. The chosen format is ’the answer is ANSWER.’

We employ the sub\_em score for all benchmarks. This means that an answer is considered correct if it contains all the elements of the ground truth. When an answer consists of multiple parts and the expected response should include all of them, the score corresponds to the proportion of correct parts provided.

Before evaluating the answers, we normalize both the ground truth and the extracted responses. For example, we remove definite articles, ignore case distinctions, and apply similar standard normalization steps following previous work ([Wan et al., 2025](https://arxiv.org/html/2507.02259#bib.bib37); [Hsieh et al., 2024](https://arxiv.org/html/2507.02259#bib.bib15); [Yen et al., 2024](https://arxiv.org/html/2507.02259#bib.bib14)).

Table [6](https://arxiv.org/html/2507.02259#A1.T6 "Table 6 ‣ A.4 Evaluation ‣ Appendix A Implementation Details ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent") shows the generation configurations of baseline models.

Table 6: Generation configurations of baseline models.

Model
Context Length
Input/Output Tokens

QwenLong-L1 ([Wan et al., 2025](https://arxiv.org/html/2507.02259#bib.bib37))
128K
120,000 / 10,000

Qwen2.5-Instruct-1M Series ([Yang et al., 2025](https://arxiv.org/html/2507.02259#bib.bib38))
1M
990,000 / 10,000

DeepSeek-R1-Distill-Qwen Series ([Guo et al., 2025](https://arxiv.org/html/2507.02259#bib.bib35))
128K
120,000 / 10,000

Qwen2.5-Instruct Series([Yang et al., 2024](https://arxiv.org/html/2507.02259#bib.bib36))
128K
120,000 / 10,000

NIAH niah\_single\_{1,2,3} in RULER ([Hsieh et al., 2024](https://arxiv.org/html/2507.02259#bib.bib15)) benchmark are used in our test. The yaml configuration of RULER are presented in [7](https://arxiv.org/html/2507.02259#A1.T7 "Table 7 ‣ A.4 Evaluation ‣ Appendix A Implementation Details ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"). In level 1, the ”haystack” consists of repetitive sentences, and the ”needle” is a seven-digit number associated with a magic word. For level 2, the ”haystack” is composed of longer essays. Level 3 goes a step further than Level 2 where the ”needle” is a 36-character UUID string. Question and context are concated as the input of LLMs. We omit the answer\_prefix provided in original RULER benchmark since it is not compatible with MemAgent workflow.

|  |
| --- |
| niah\_single\_1: |
| task: niah |
| args: |
| type\_haystack: repeat |
| type\_needle\_k: words |
| type\_needle\_v: numbers |
| num\_needle\_k: 1 |
| num\_needle\_v: 1 |
| num\_needle\_q: 1 |
| niah\_single\_2: |
| task: niah |
| args: |
| type\_haystack: essay |
| type\_needle\_k: words |
| type\_needle\_v: numbers |
| num\_needle\_k: 1 |
| num\_needle\_v: 1 |
| num\_needle\_q: 1 |
| niah\_single\_3: |
| task: niah |
| args: |
| type\_haystack: essay |
| type\_needle\_k: words |
| type\_needle\_v: uuids |
| num\_needle\_k: 1 |
| num\_needle\_v: 1 |
| num\_needle\_q: 1 |

Table 7: Synthetic Configuration used for NIAH task.

## Appendix B Computation Complexity

We adopt the floating-point operations (FLOP) estimator for the Qwen2Model from verl [Sheng et al. (2024)](https://arxiv.org/html/2507.02259#bib.bib43) to compute the FLOP cost of both the baseline model and our proposed method. The results are shown in Figure [10](https://arxiv.org/html/2507.02259#A2.F10 "Figure 10 ‣ Appendix B Computation Complexity ‣ MEMAGENT MEMAGENT : Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent"). The baseline model exhibits an O(n2n^{2}) complexity, while MemAgent achieves an O⁡(n)O(n) complexity.

Figure 10: Floating point operations across context lengths from 8K to 4M

For the baseline model, the number of tokens required to process is q+c+oq+c+o, where qq represents the length for the problem, cc is the context length and oo represents the output length.

For MemAgent, total FLOP cost is the sum of the FLOPs from all stages. The detailed stages involved are as follows:

* •

  Initializing: In the first stage, the model processes an input consisting of q+200+oq+200+o, where 200200 represents a constant added to prompt the model to follow the MemAgent workflow.
* •

  Memory Updating: The number of repetitions is determined by k=⌈cN⌉k=\lceil\frac{c}{N}\rceil, where cc is the variable component of the input. Each repetition requires an input of length q+200+N+oq+200+N+o.
* •

  Final Answering: The final stage processes an input of length q+100+oq+100+o, which includes the accumulated output from the previous steps.

We set q=1024,o=1024,N=5000q=1024,o=1024,N=5000 and cc is ranging from 8K to 4M to calculate the final result.

## Appendix C Case Study

To further illustrate the proposed memory mechanism in detail, we conduct a case study on a generation trajectory of MemAgent-14B. The input question is: The director of the romantic comedy ‘Big Stone Gap’ is based in what New York city? This a 2-hop question with the following relevant Wikipedia entries:

1) Big Stone Gap is a 2014 American drama romantic comedy film written and directed by Adriana Trigiani.

2) Adriana Trigiani is an Italian American best-selling author of sixteen books, television writer, film director, and entrepreneur based in Greenwich Village, New York City.

In the first round, the model is presented with the entry Ghost, which refers to a production team also based in New York. The model chooses to retain this potentially useful information for future use. In the second round, no relevant context is provided; nevertheless, the model maintains its agent state, demonstrating robustness against distraction. In the third round, both relevant entries are presented. The model correctly identifies critical information and updates its memory accordingly, leading to the correct answer: Greenwich Village, New York City. At this point, the reasoning process is complete. In the remaining rounds, the model’s memory remains unchanged and is used to produce the final response.

### Chunk1

…

Document 20:
Ghost (production team)

Ghost is a Swedish record producing and songwriting team, composed of Ulf Lindström and Johan Ekhé, based in New York City.

…

### Memory1

The provided section does not contain any information about the director of the romantic comedy ”Big Stone Gap” or their base in New York City. However, it does mention a production team called ”Ghost” which is based in New York City. Since the problem is specifically asking about the director of ”Big Stone Gap,” and there is no direct information about the director in the given section, we cannot infer anything directly related to the problem from the provided text.

Updated memory:

•

Ghost is a Swedish record producing and songwriting team, composed of Ulf Lindström and Johan Ekhé, based in New York City. They are perhaps best known for writing and producing Swedish singer Robyn’s three first studio albums.

The problem remains unanswered based on the provided section. Additional information would be needed to determine the director of ”Big Stone Gap” and their base in New York City.

### Chunk2

…(No relevant document)

### Memory2

The provided section does not contain any information about the director of the romantic comedy ”Big Stone Gap” or their base in New York City. 2
Therefore, the updated memory remains unchanged with respect to the problem at hand. The memory still notes that the Ghost record producing and songwriting team is based in New York City, but it does not provide any information about the director of ”Big Stone Gap.”

Updated memory:

•

Ghost is a Swedish record producing and songwriting team, composed of Ulf Lindström and Johan Ekhé, based in New York City. They are perhaps best known for writing and producing Swedish singer Robyn’s three first studio albums.
•

The problem remains unanswered based on the provided section. Additional information would be needed to determine the director of ”Big Stone Gap” and their base in New York City.
