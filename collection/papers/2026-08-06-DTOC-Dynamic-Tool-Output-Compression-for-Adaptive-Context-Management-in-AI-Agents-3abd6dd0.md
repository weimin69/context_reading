# DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents

- 来源: https://arxiv.org/abs/2609.26121
- 发布日期: 2026-08-06
- 日期依据: page metadata: citation_date
- 类型: paper
- 主题: 工具输出压缩、可恢复上下文
- 抓取状态: full_text_html
- 正文来源: https://arxiv.org/html/2609.26121
- 抓取时间 UTC: 2026-10-26T09:34:14.635273+00:00
- 作者: Chaturvedi, Abhay, Bhattacharya, Shreya, Gopalkrishnan, Rashmika, van der Putten, Peter

## 来源摘要 / 页面简介

Abstract: As agent capabilities have grown, practical limitations increasingly stem from constrained context windows rather than model capacity. Common strategies, such as truncation, heuristic aging, and lossy summarization, may discard useful information or introduce hallucination risk. To address these challenges, we propose Dynamic Tool Output Compression (DTOC), a framework for scalable context management in LLM-based agents that models context updates as explicit and reversible operations within the agent reasoning loop. DTOC retains full tool outputs in external memory while inserting compact placeholders into the active context, enabling selective reconstruction when needed. We formalize the DTOC mechanism, integrate it into a ReAct-style agent architecture, and provide a production-oriented implementation supporting on-demand restoration of compressed outputs. Experiments on DeepSWE reveal model-dependent effects: for responsive models (Sonnet 4.6, GPT-5.4), DTOC reduces input tokens (10.3 and 12.7%) and agent steps (2.4 and 32.3%), while increasing solve rates (2.5 and 1.5 times higher) and lowering cost per solved task (3 and 3.5 times lower cost per solved task). For the other models results are more mixed, with GPT-5.5 doubling solve rate and halving cost, but no impact on solve rate and negative impact on cost for the other models. Ablation results show reversibility is critical: disable-only compression variants degraded performance, while full DTOC recovered baseline accuracy at substantially lower context cost. These findings indicate that explicit, reversible context management can improve the efficiency of long-horizon agent reasoning without degrading task performance.

## 抓取正文

11institutetext: Product R&D, Pegasystems, Bangalore, India
  
11email: {abhay.chaturvedi,shreya.Bhattacharya,rashmika.gopalakrishnan}@pega.com
22institutetext: AI Lab, Pegasystems, Amsterdam, the Netherlands
  
22email: peter.vanderputten@pega.com
  
33institutetext: LIACS, Leiden University, Leiden, the Netherlands
  
33email: p.w.h.van.der.putten@liacs.leidenuniv.nl

# DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents

Abhay Chaturvedi
  
Shreya Bhattacharya
  
Rashmika Gopalkrishnan
  
Peter van der Putten

###### Abstract

As agent capabilities have grown, practical limitations increasingly stem from constrained context windows rather than model capacity. Common strategies, such as truncation, heuristic aging, and lossy summarization, may discard useful information or introduce hallucination risk. To address these challenges, we propose Dynamic Tool Output Compression (DTOC), a framework for scalable context management in LLM-based agents that models context updates as explicit and reversible operations within the agent reasoning loop. DTOC retains full tool outputs in external memory while inserting compact placeholders into the active context, enabling selective reconstruction when needed.
We formalize the DTOC mechanism, integrate it into a ReAct-style agent architecture, and provide a production-oriented implementation supporting on-demand restoration of compressed outputs.
Experiments on DeepSWE reveal model-dependent effects: for responsive models (Sonnet 4.6, GPT-5.4), DTOC reduces input tokens (10.3 and 12.7%) and agent steps (2.4 and 32.3%), while increasing solve rates (2.5 and 1.5 times higher) and lowering cost per solved task (3 and 3.5 times lower cost per solved task). For the other models results are more mixed, with GPT-5.5 doubling solve rate and halving cost, but no impact on solve rate and negative impact on cost for the other models.
Ablation results show reversibility is critical: disable-only compression variants degraded performance, while full DTOC recovered baseline accuracy at substantially lower context cost.
These findings indicate that explicit, reversible context management can improve the efficiency of long-horizon agent reasoning without degrading task performance.

## 1 Introduction

The primary challenge in maintaining long-horizon agentic trajectories is the inherent attention scarcity within the transformer architecture [[20](https://arxiv.org/html/2609.26121#bib.bib1 "Memory as action: autonomous context curation for long-horizon agentic tasks"), [15](https://arxiv.org/html/2609.26121#bib.bib2 "COMPASS: enhancing agent long-horizon reasoning with evolving context"), [12](https://arxiv.org/html/2609.26121#bib.bib3 "Longcat-flash-thinking-2601 technical report"), [1](https://arxiv.org/html/2609.26121#bib.bib4 "Effective context engineering for AI agents"), [18](https://arxiv.org/html/2609.26121#bib.bib5 "Trams: training-free memory selection for long-range language modeling")]. Modern large language models (LLMs) rely on self-attention, where every token attends to every other token, resulting in O​(n2)O(n^{2}) pairwise interactions as the context length
nn grows [[14](https://arxiv.org/html/2609.26121#bib.bib6 "Attention is all you need")]. As nn expands, the model’s ability to retrieve specific ‘needles’ from an increasingly dense informational ‘haystack’ degrades, reducing its capacity to surface earlier but task-critical details [[8](https://arxiv.org/html/2609.26121#bib.bib9 "Lost in the middle: how language models use long contexts")].
This limitation manifests empirically as ‘context rot’, a degradation in the model’s effective reasoning horizon: although models may support large nominal context windows (e.g., 128k tokens), performance often declines well before these limits are reached [[8](https://arxiv.org/html/2609.26121#bib.bib9 "Lost in the middle: how language models use long contexts")].

These constraints become particularly acute in long horizon tasks, such as scientific and software engineering workflows, where (semi-)autonomous agents must integrate heterogeneous tool outputs over many steps [[18](https://arxiv.org/html/2609.26121#bib.bib5 "Trams: training-free memory selection for long-range language modeling"), [13](https://arxiv.org/html/2609.26121#bib.bib11 "Autonomous task planning for heterogeneous multi-agent systems"), [11](https://arxiv.org/html/2609.26121#bib.bib12 "From autonomous agents to integrated systems, a new paradigm: orchestrated distributed intelligence"), [10](https://arxiv.org/html/2609.26121#bib.bib31 "Agentic large language models, a survey")]. Over long trajectories, the accumulation of prompts, tool outputs, and intermediate reasoning saturates the available context, forcing truncation of earlier turns. Critically, the earliest messages often encode the user’s primary objectives, safety constraints, or key assumptions, leading subsequent reasoning to proceed on a progressively distorted representation of the original task [[7](https://arxiv.org/html/2609.26121#bib.bib14 "GitGoodBench: a novel benchmark for evaluating agentic performance on git")].

Existing context-management strategies often prove insufficient in agentic settings [[20](https://arxiv.org/html/2609.26121#bib.bib1 "Memory as action: autonomous context curation for long-horizon agentic tasks")].
Hard truncation, in which older segments are removed once a token budget is exceeded, results in irreversible information loss and effectively forces planning under partial observability [[2](https://arxiv.org/html/2609.26121#bib.bib15 "You know, for context - part II: agentic AI and context engineering"), [1](https://arxiv.org/html/2609.26121#bib.bib4 "Effective context engineering for AI agents")].
LLM-based summarization, used in systems such as OpenHands [[16](https://arxiv.org/html/2609.26121#bib.bib26 "OpenHands: an open platform for AI software developers as generalist agents")] and Cursor 111<https://www.openhands.dev/>, <https://cursor.com/>, mitigates token growth but can introduce abstraction errors, hallucinations, and trajectory elongation, causing agents to overlook failure signals and repeat unproductive actions [[7](https://arxiv.org/html/2609.26121#bib.bib14 "GitGoodBench: a novel benchmark for evaluating agentic performance on git"), [5](https://arxiv.org/html/2609.26121#bib.bib16 "Smarter context management for LLM-powered agents")].
Other lossy approaches, such as Caveman-style compression222<https://github.com/juliusbrussee/caveman>, face similar fidelity trade-offs, while static observation masking relies on recency or size heuristics and cannot easily recover relevant information from earlier reasoning steps [[7](https://arxiv.org/html/2609.26121#bib.bib14 "GitGoodBench: a novel benchmark for evaluating agentic performance on git")].

To address these limitations, we introduce Dynamic Tool-Output Compression (DTOC), a framework that treats context management as an explicit agent action rather than a fixed system-level mechanism. Tool outputs are stored in an external memory and replaced in the active context with lightweight references, allowing agents to selectively hide and later restore information as needed. DTOC therefore provides reversible, low-risk context compression that preserves recoverability while reducing active-context growth during long-horizon reasoning.
A reference implementation built on OpenCode and used for the main experiments is available at <https://github.com/chaturvediabhay24/opencode>.

## 2 Related Work

The conceptual lineage of DTOC traces back to the ReAct framework
[[17](https://arxiv.org/html/2609.26121#bib.bib30 "ReAct: synergizing reasoning and acting in language models")], which showed that interleaving explicit reasoning traces (‘thoughts’) with actions and observations enables more robust problem solving than reasoning alone [[17](https://arxiv.org/html/2609.26121#bib.bib30 "ReAct: synergizing reasoning and acting in language models")]. In ReAct, reasoning traces function as a form of inner speech that allows the model to induce, track, and revise action plans while integrating new evidence from the environment. However, ReAct was developed under the assumption of relatively short interaction histories and does not explicitly address the constraints imposed by finite context windows in long-horizon trajectories [[17](https://arxiv.org/html/2609.26121#bib.bib30 "ReAct: synergizing reasoning and acting in language models")].

Subsequent work on prompt compression, notably LLMLingua [[6](https://arxiv.org/html/2609.26121#bib.bib18 "LLMLingua: compressing prompts for accelerated inference of large language models")], sought to address context limitations by using smaller language models to identify and remove low-importance tokens based on perplexity. LLMLingua reports substantial compression (up to 20× in some settings) for static prompts while maintaining task performance across multiple benchmarks [[6](https://arxiv.org/html/2609.26121#bib.bib18 "LLMLingua: compressing prompts for accelerated inference of large language models")].
In agentic settings, however, perplexity-based compression can be overly aggressive: tokens that appear linguistically predictable may carry high task-specific semantic value, such as unique identifiers, numeric parameters, or error codes in execution logs. Moreover, LLMLingua operates as a fundamentally lossy, one-way transformation, discarding information that cannot be fully reconstructed from the compressed prompt [[6](https://arxiv.org/html/2609.26121#bib.bib18 "LLMLingua: compressing prompts for accelerated inference of large language models")]. DTOC instead targets the dominant source of context growth, tool outputs, and controls their visibility through a non-destructive mechanism that hides or reveals content without irreversible deletion.

In parallel, a broader shift toward ‘context engineering’ has emerged as a formal discipline concerned with the systematic optimization of information payloads presented to LLMs [[9](https://arxiv.org/html/2609.26121#bib.bib19 "A survey of context engineering for large language models"), [3](https://arxiv.org/html/2609.26121#bib.bib20 "Context engineering 2.0: the context of context engineering"), [19](https://arxiv.org/html/2609.26121#bib.bib21 "Agentic context engineering: evolving contexts for self-improving language models")].
Anthropic’s [[1](https://arxiv.org/html/2609.26121#bib.bib4 "Effective context engineering for AI agents")] work on ‘Agent Skills’ and ‘Progressive Disclosure’ exemplifies this direction: agents maintain lightweight references or handles to external resources and selectively load full content only when necessary, rather than streaming all information into the live context at once [[1](https://arxiv.org/html/2609.26121#bib.bib4 "Effective context engineering for AI agents")]. DTOC generalizes this principle from individual files or queries to the entire conversational state, treating the evolving interaction history as a dynamic repository that the agent can explicitly load or unload as its reasoning unfolds, enabling agent control over system heuristics.

Closely related is Stanford’s ACE (Agentic Context Engineering)framework [[19](https://arxiv.org/html/2609.26121#bib.bib21 "Agentic context engineering: evolving contexts for self-improving language models")], which conceptualizes contexts as ‘evolving playbooks’ that accumulate, refine, and organize strategies through a generator–reflector–curator cycle [[19](https://arxiv.org/html/2609.26121#bib.bib21 "Agentic context engineering: evolving contexts for self-improving language models")]. ACE focuses on high-level adaptation of strategy representations and demonstrates how naive, end-to-end rewriting of long contexts can induce ‘context collapse’, where crucial details are inadvertently erased during iterative summarization [[19](https://arxiv.org/html/2609.26121#bib.bib21 "Agentic context engineering: evolving contexts for self-improving language models")]. DTOC is complementary to ACE: whereas ACE manages the structure and evolution of strategic playbooks, DTOC supplies the low-level token management and tool-output governance needed to keep these playbooks, and the evidentiary traces they depend on, within the model’s effective attention span.

## 3 Methodology: Dynamic Tool Output Compression

This section formalizes Dynamic Tool Output Compression (DTOC) as a structured, non-destructive context management framework. We describe the general mechanism (Section [3.1](https://arxiv.org/html/2609.26121#S3.SS1 "3.1 General Mechanism Overview ‣ 3 Methodology: Dynamic Tool Output Compression ‣ DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents")), detail the implementation via an explicit tool-based interface (Section [3.2](https://arxiv.org/html/2609.26121#S3.SS2 "3.2 Implementation via Explicit Tool-Based Control ‣ 3 Methodology: Dynamic Tool Output Compression ‣ DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents")), specify the underlying data structures (Section [3.3](https://arxiv.org/html/2609.26121#S3.SS3 "3.3 DTOC Data Structures and Tool Interface ‣ 3 Methodology: Dynamic Tool Output Compression ‣ DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents")), and finally situate DTOC within the broader context engineering landscape (Sections [3.4](https://arxiv.org/html/2609.26121#S3.SS4 "3.4 Context Engineering Perspective ‣ 3 Methodology: Dynamic Tool Output Compression ‣ DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents"), [3.5](https://arxiv.org/html/2609.26121#S3.SS5 "3.5 Relation to ACE and Playbook Evolution ‣ 3 Methodology: Dynamic Tool Output Compression ‣ DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents")).

### 3.1 General Mechanism Overview

DTOC formulates context management as an explicit agent-level operation over a persistent external memory of tool outputs. At each step, the agent maintains a minimal active context comprising the current user query, its reasoning trace, and a curated subset of prior tool outputs. All outputs are stored in a structured repository indexed by lightweight identifiers, aligning with ‘Agent Skills’ and ‘Progressive Disclosure’ paradigms where agents reference resources via handles rather than raw content [[1](https://arxiv.org/html/2609.26121#bib.bib4 "Effective context engineering for AI agents")].

Instead of compressing or discarding information, DTOC enables explicit retrieval and unloading actions, allowing the agent to dynamically manage context under token constraints. This yields a non-destructive visibility layer in which outputs remain persistently stored and recoverable, with access governed by the agent’s learned retrieval policy rather than irreversible truncation. Consequently, DTOC shifts the bottleneck from storage capacity to efficient access and retrieval.

### 3.2 Implementation via Explicit Tool-Based Control

In practice, DTOC is realized through a dedicated context management tool that exposes visibility control as an explicit agent action (Figure [1](https://arxiv.org/html/2609.26121#S3.F1 "Figure 1 ‣ 3.2 Implementation via Explicit Tool-Based Control ‣ 3 Methodology: Dynamic Tool Output Compression ‣ DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents")). Rather than relying on provider-specific tool identifiers (e.g., OpenAI or Anthropic tool IDs), the orchestration layer assigns custom identifiers at execution time and wraps each tool response in a structured JSON object containing three fields: tool\_key, a unique identifier; tool\_result, the output content; and estimated\_tokens, an approximate token count used for context budgeting.

![Refer to caption](https://arxiv.org/html/2609.26121v1/x1.png)

Figure 1: Architecture of DTOC. The figure shows reversible, agent-controlled context compression. Initially, all tool outputs are included in the active context (left). The agent selectively disables irrelevant tool outputs to reduce token usage while retaining their metadata (middle). When needed, previously disabled outputs can be re-enabled without loss of information (right), enabling progressive disclosure and fine-grained context engineering under orchestrator-level control.

The agent interacts with a manage\_context tool parameterized by two lists, enable and disable, each specifying a set of tool keys. Invoking this tool updates output visibility within the active context. Disabled outputs are replaced with compact metadata-only placeholders containing the tool key, timestamp, and token estimate, while enabled outputs restore their full tool\_result from the orchestrator. This mechanism decouples visibility management from provider APIs, yielding a model-agnostic and unified representation of visible, hidden, and recoverable outputs.

Trigger conditions for context compression are conveyed through a natural language tool description (e.g., invoking the tool when the context nears its limit and certain outputs become irrelevant). This design delegates compression policy to the agent rather than fixed heuristics, aligning with DTOC’s agent-centric philosophy. By exposing token estimates for each output, the agent can make informed trade-offs between retaining useful information and maintaining a compact context.

### 3.3 DTOC Data Structures and Tool Interface

To make the DTOC mechanism concrete, we formally specify the key data structures and tool interfaces used in our implementation. Algorithm [1](https://arxiv.org/html/2609.26121#alg1 "Algorithm 1 ‣ 3.3 DTOC Data Structures and Tool Interface ‣ 3 Methodology: Dynamic Tool Output Compression ‣ DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents") presents the core orchestrator logic, including the ToolOutput record structure, the persistent store, the context assembly procedure, and the manage\_context interface.

Algorithm 1  DTOC Orchestrator: Data Structures and Context Management

Record ToolOutput:

tool\_key: String ⊳\triangleright Orchestrator-generated unique ID, e.g. "tool\_001"

tool\_result: String ⊳\triangleright Raw content returned by external tool

estimated\_tokens: Integer ⊳\triangleright Heuristic token-count approximation

timestamp: DateTime ⊳\triangleright Invocation time

visible: Boolean ⊳\triangleright Indicates inclusion in the active context

State: Persistent store 𝒮\mathcal{S}: ToolKey →\rightarrow ToolOutput

procedure AssembleContext(𝒮\mathcal{S})

𝒞←∅\mathcal{C}\leftarrow\emptyset

for each (k,o)∈𝒮(k,o)\in\mathcal{S} do

if o.visible=trueo.\texttt{visible}=\textbf{true} then

𝒞←𝒞∪{o}\mathcal{C}\leftarrow\mathcal{C}\cup\{o\} ⊳\triangleright Include full tool output

else

𝒞←𝒞∪{Placeholder(k,o.estimated\_tokens,o.timestamp)}\mathcal{C}\leftarrow\mathcal{C}\cup\{\textsc{Placeholder}(k,o.\texttt{estimated\\_tokens},o.\texttt{timestamp})\}

end if

end for

return 𝒞\mathcal{C}

end procedure

procedure ManageContext(enable: List[ToolKey], disable: List[ToolKey])

for each k∈disablek\in\texttt{disable} do

𝒮​[k].visible←false\mathcal{S}[k].\texttt{visible}\leftarrow\textbf{false}

end for

for each k∈enablek\in\texttt{enable} do

𝒮​[k].visible←true\mathcal{S}[k].\texttt{visible}\leftarrow\textbf{true}

end for

return StatusReport(modified keys, Δ\Delta active tokens)

end procedure

Each ToolOutput record associates a unique orchestrator-assigned identifier (tool\_key) with the raw content returned by an external tool (tool\_result), along with a heuristic estimate of its token footprint (estimated\_tokens), an invocation timestamp, and a visible flag that determines whether the content is included in the active context. The orchestrator maintains a persistent store 𝒮\mathcal{S} mapping each ToolKey to its corresponding record.

At each reasoning step, the AssembleContext procedure constructs the active context 𝒞\mathcal{C}. Outputs marked as visible are incorporated in full, whereas hidden outputs are replaced by compact placeholders that retain only essential metadata, namely the ToolKey, estimated token count, timestamp, and an implicit hidden-status indicator. This design preserves referential integrity while minimizing token consumption.

Interaction with the context management mechanism is mediated through the ManageContext procedure, which accepts two sets of ToolKey values corresponding to enable and disable operations, respectively. The procedure updates the visibility flags in 𝒮\mathcal{S} and returns a StatusReport summarizing the modified entries and the resulting change in active token count. This immediate feedback enables the agent to reason explicitly about the trade-off between context breadth and token efficiency.

The interface design satisfies three key properties. First, all compression operations are reversible, as the complete tool\_result is persisted in 𝒮\mathcal{S} irrespective of its visibility status. Second, the agent has explicit access to metadata such as token estimates and timestamps, supporting informed and adaptive context selection. Third, the mechanism is provider-agnostic, relying solely on orchestrator-level abstractions rather than vendor-specific tool-calling semantics.

We estimate token counts with a character-count heuristic (len(content)/4) applied when the orchestrator wraps each tool output. The manage\_context tool description provided verbatim to all models reads: *“Use this tool when you feel the context limit is increasing and there are some tool outputs whose content is no longer relevant to the current reasoning step. One can disable such outputs to free up context space, and re-enable them later if needed.”* No explicit trigger threshold is imposed; compression timing is delegated entirely to the agent. Placeholders for disabled outputs consume approximately 30–50 tokens regardless of original output size. When the active context approaches the model’s native limit, the underlying provider applies its own truncation; DTOC aims to prevent reaching this threshold through proactive agent-driven compression but does not override provider-level behavior.

### 3.4 Context Engineering Perspective

Our methodology adopts the emerging lens of context engineering, formalizing the interaction history and tool-output store as an information payload to be actively optimized rather than passively accumulated [[9](https://arxiv.org/html/2609.26121#bib.bib19 "A survey of context engineering for large language models")]. Concretely, DTOC operationalizes context engineering [[9](https://arxiv.org/html/2609.26121#bib.bib19 "A survey of context engineering for large language models"), [3](https://arxiv.org/html/2609.26121#bib.bib20 "Context engineering 2.0: the context of context engineering"), [19](https://arxiv.org/html/2609.26121#bib.bib21 "Agentic context engineering: evolving contexts for self-improving language models")] at two levels.
First, it generalizes the ‘Progressive Disclosure’ principle from individual resources (e.g., files or queries) to the full conversational trajectory: past messages and tool outputs remain available for selective re-instantiation into the live context, but are not maintained there by default [[1](https://arxiv.org/html/2609.26121#bib.bib4 "Effective context engineering for AI agents")]. This shifts context management from static inclusion to dynamic, demand-driven access.
Second, DTOC introduces a compact action vocabulary, conceptually including operations such as select, enable, disable, and retrieve, that the agent can invoke to manage its memory footprint. This elevates context selection into a learnable component of the policy, rather than a fixed system heuristic.

### 3.5 Relation to ACE and Playbook Evolution

Finally, we situate DTOC within the Agentic Context Engineering (ACE) framework [[19](https://arxiv.org/html/2609.26121#bib.bib21 "Agentic context engineering: evolving contexts for self-improving language models")], which views contexts as ‘evolving playbooks’ that accumulate and refine strategies via a generator–reflector–curator cycle. In our experimental setup, high-level strategy adaptation (e.g., switching debugging tactics or adjusting research plans) corresponds to ACE’s notion of playbook evolution, while DTOC provides the low-level token and tool-output management required to keep these playbooks within the model’s effective attention span.

This separation of concerns enables us to disentangle whether strategic failures arise from genuine reasoning errors or from context pathologies such as context collapse, where critical details are lost due to repeated summarization or truncation [[19](https://arxiv.org/html/2609.26121#bib.bib21 "Agentic context engineering: evolving contexts for self-improving language models")]. By instrumenting both high-level decision traces and the underlying DTOC operations, our methodology quantifies the extent to which dynamic, non-destructive control over tool-output visibility improves success rates and sample efficiency in long-horizon agentic tasks.

## 4 Experimental Setup

We evaluate DTOC on six tasks from DeepSWE [[4](https://arxiv.org/html/2609.26121#bib.bib34 "DeepSWE: measuring frontier coding agents on original, long-horizon engineering tasks")], a benchmark of real-world open-source software engineering tasks, using five frontier models under two conditions: DTOC ON and DTOC OFF (Table [1](https://arxiv.org/html/2609.26121#S4.T1 "Table 1 ‣ 4 Experimental Setup ‣ DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents")). We use DeepSWE [[4](https://arxiv.org/html/2609.26121#bib.bib34 "DeepSWE: measuring frontier coding agents on original, long-horizon engineering tasks")] because all tasks require implementing complete, non-trivial features that produce extended agent trajectories (30–285 steps), providing a naturalistic stress test for context management under realistic token accumulation.
The five models were selected to span three axes of variation that are directly relevant to context management. First, provider diversity: we include Anthropic (Sonnet, Opus), OpenAI (GPT‑5.4, GPT‑5.5), and Google (Gemini) to ensure our findings are not idiosyncratic to a single architecture or training methodology. Second, context window size: the selected models cover native capacities of 128K (GPT‑5.4/GPT‑5.5), 200K (Sonnet/Opus), and 1M tokens (Gemini Flash), allowing us to test whether DTOC’s benefit attenuates as native context capacity grows. Third, capability tier and reasoning style: by pairing a mid‑tier and a high‑end model from each provider (Sonnet vs. Opus; GPT‑5.4 vs. GPT‑5.5) we evaluate whether DTOC benefits scale with model capability, while Gemini Flash exemplifies a “large‑context, fast‑inference” design point. Together, these choices let us isolate effects of provider, native context size, and model capability on DTOC’s effectiveness.

Table 1: Experimental Grid

| Component | Setting |
| --- | --- |
| Benchmark | DeepSWE (6 real-world open-source SWE tasks; Python and TypeScript) |
| Models | Claude Sonnet 4.6 (200K); Claude Opus 4.8 (200K); GPT-5.4 (128K); GPT-5.5 (128K); Gemini 3.5 Flash (1M) |
| Conditions | DTOC ON (agent has manage\_context tool); DTOC OFF (no compression, full context retained) |
| Metrics | Task solve rate (reward), input tokens, agent steps, wall-clock duration, cost per solved task |
| Agent | opencode v0.0.0-dtoc-implementation (ReAct-style, shared prompts, identical tool configurations) |

### 4.1 Tasks and Environments

DeepSWE requires implementing complete features capable of passing each project’s full test suite. The tasks span Python projects (Narwhals, FastAPI, sqlite-utils, and Mashumaro) and TypeScript projects (drizzle-orm and ts-pattern), ranging from the implementation of a single combinator (matchEach) to multi-file rolling-window features. These tasks generate long agent trajectories (30–285 steps) with substantial tool-output accumulation, making DeepSWE a natural stress test for context management.

Agents are executed using OpenCode, a ReAct-style coding agent that interleaves reasoning and tool invocation. The available toolset includes file operations (read, write, edit, and apply\_patch), code-intelligence tools (glob, grep, and lsp), and shell execution via bash.
Each model–condition pair was run on all assigned tasks using identical agent configurations, with tool outputs wrapped in structured JSON envelopes containing orchestrator-assigned identifiers, raw results, and token estimates. In the DTOC-ON condition, the agent is additionally provided with the manage\_context tool, which enables dynamic visibility control over previously generated tool outputs (Section [3.2](https://arxiv.org/html/2609.26121#S3.SS2 "3.2 Implementation via Explicit Tool-Based Control ‣ 3 Methodology: Dynamic Tool Output Compression ‣ DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents")). All other tools, prompts, and configuration settings are held constant across experimental conditions.
Task success is measured as a binary outcome. A task receives a reward of 1.01.0 if all project tests pass successfully and 0.00.0 otherwise.

## 5 Results

We evaluate DTOC on the DeepSWE [[4](https://arxiv.org/html/2609.26121#bib.bib34 "DeepSWE: measuring frontier coding agents on original, long-horizon engineering tasks")] benchmark as per the set up described in the previous section, along with a small-scale ablation study on proprietary data.

### 5.1 DeepSWE Benchmark

Table [4](https://arxiv.org/html/2609.26121#footnote4 "footnote 4 ‣ Table 2 ‣ 5.1 DeepSWE Benchmark ‣ 5 Results ‣ DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents") summarizes the aggregate DeepSWE results per model and Table [3](https://arxiv.org/html/2609.26121#S5.T3 "Table 3 ‣ 5.1 DeepSWE Benchmark ‣ 5 Results ‣ DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents") shows the solve matrix by task and model, under DTOC ON and OFF conditions. These results reveal model-family-dependent compression behaviors. DTOC’s effectiveness depends on each model’s native reasoning style, verbosity, and implicit context-management strategies.

Table 2: DeepSWE benchmark: aggregate results per model (6 real-world SWE tasks). Δ\Delta columns show relative change with DTOC ON vs. OFF; negative values indicate improvement. SR is Solve Rate, CS is Cost Solved. Denominators below 6 reflect tasks excluded due to infrastructure timeouts.444Mashumaro was not evaluated for Sonnet OFF and Gemini (both conditions) due to infrastructure timeouts; denominators reflect completed runs only.

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| Model | SR | SR | Input | Steps Δ\Delta | CS | CS |
|  | ON | OFF | Tokens Δ\Delta |  | ON | OFF |
| Claude Sonnet 4.6 | 3/6 | 1/5 | −10.3%-10.3\% | −2.4%-2.4\% | $8.65 | $26.27 |
| GPT-5.4 | 3/6 | 2/6 | −12.7%-12.7\% | −32.3%-32.3\% | $2.64 | $9.30 |
| GPT-5.5 | 2/6 | 1/6 | −0.6%-0.6\% | +14.3%+14.3\% | $49.93 | $100.49 |
| Claude Opus 4.8 | 3/6 | 3/6 | +18.4%+18.4\% | +8.2%+8.2\% | $21.50 | $19.64 |
| Gemini 3.5 Flash | 1/5 | 1/5 | +48.7%+48.7\% | +30.2%+30.2\% | $18.11 | $13.28 |

DTOC has a strongly positive effect on Claude Sonnet 4.6. The solve rate increases from 1/51/5 (20%20\%) to 3/63/6 (50%50\%). Average input tokens decrease from 369,666369{,}666 to 331,615331{,}615 (−10.3%-10.3\%), output tokens decrease from 104,442104{,}442 to 93,80493{,}804 (−10.2%-10.2\%), and mean task duration decreases by 106​s106\,\mathrm{s} (from 2,318​s2{,}318\,\mathrm{s} to 2,212​s2{,}212\,\mathrm{s}). At the task level, ts-pattern exhibits a 3.6×3.6\times speedup (3232 versus 117117 steps), sqlite-utils succeeds with DTOC but fails almost immediately without it (22 steps), and drizzle-orm is fully solved only in the DTOC condition. Cost per solved task decreases by approximately 67%67\%, from $​26.27\mathdollar 26.27 to $​8.65\mathdollar 8.65.

GPT-5.4 is highly compression-responsive and achieves the best overall efficiency. DTOC reduces input tokens by 12.7%12.7\% (from 129,824129{,}824 to 113,374113{,}374), cache-read tokens by 26.8%26.8\%, and agent steps by 32.3%32.3\% (from 54.254.2 to 36.736.7). The solve rate improves from 33%33\% to 50%50\%, while average duration decreases by 59​s59\,\mathrm{s}. Notably, mashumaro is solved with DTOC (72/7272/72 tests passing in 3333 steps) but fails without DTOC (67/7267/72 tests passing in 7373 steps), suggesting that DTOC preserves critical information during long trajectories. GPT-5.4 combined with DTOC achieves the lowest cost per solved task, reducing cost from $9.30 to $2.64.

GPT-5.5 exhibits a modest but positive response to DTOC. The solve rate doubles from 1/61/6 to 2/62/6, and mean duration decreases from 790​s790\,\mathrm{s} to 740​s740\,\mathrm{s}, making GPT-5.5 the fastest model overall at approximately 12.312.3 minutes per task. Input token savings are negligible (−0.6%-0.6\%), while agent steps increase by 14.3%14.3\%, suggesting that frequent manage\_context invocations generate overhead without substantially reducing context size. DTOC enables a complete solution for ts-pattern and yields substantially greater partial progress on fastapi (519519 tests passed versus 4343 without DTOC). Cost per solved task decreases from $100.49 to $49.93.

Claude Opus 4.8 exhibits task-dependent trade-offs with no aggregate improvement in solve rate, remaining at 3/63/6 in both conditions. Under DTOC, input tokens increase by 18.4%18.4\%, agent steps increase by 8.2%8.2\%, and execution time increases by 5.7%5.7\%. However, outcomes vary across tasks. For example, mashumaro succeeds only with DTOC, whereas sqlite-utils succeeds only without DTOC. These results suggest that certain compression decisions may occasionally remove context that remains relevant. Because Opus generates substantially more output tokens than the other models, the relative benefits of DTOC are reduced and partially offset by the overhead of context-management operations.

DTOC has a negative effect on Gemini 3.5 Flash. Input tokens increase by 48.7%48.7\%, agent steps increase by 30.2%30.2\%, and execution time increases by 35.8%35.8\%, while the solve rate remains unchanged at 1/51/5. Cost per solved task increases by approximately 36%36\%. Inspection of execution traces suggests that Gemini frequently performs small compression operations that introduce overhead without producing meaningful reductions in active context size. Its incremental action style generates many short outputs and tool interactions, causing management overhead to outpace compression gains. These findings suggest that model-specific compression policies may be necessary to fully realize DTOC’s benefits.

Table 3: DeepSWE per-task solve matrix (✓\checkmark = solved, ×\times = not solved, — = not evaluated).

|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | Sonnet 4.6 | | GPT-5.4 | | GPT-5.5 | | Opus 4.8 | | Gemini 3.5 | |
| Task | ON | OFF | ON | OFF | ON | OFF | ON | OFF | ON | OFF |
| narwhals (Python) | ×\times | ×\times | ×\times | ×\times | ×\times | ×\times | ×\times | ×\times | ×\times | ×\times |
| drizzle-orm (TS) | ✓\checkmark | ×\times | ×\times | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ×\times | ×\times |
| fastapi (Python) | ×\times | ×\times | ×\times | ×\times | ×\times | ×\times | ×\times | ×\times | ×\times | ×\times |
| sqlite-utils (Python) | ✓\checkmark | ×\times | ✓\checkmark | ×\times | ×\times | ×\times | ×\times | ✓\checkmark | ×\times | ×\times |
| ts-pattern (TS) | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark | ×\times | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark |
| mashumaro (Python) | ×\times | — | ✓\checkmark | ×\times | ×\times | ×\times | ✓\checkmark | ×\times | — | — |
| Total | 3/6 | 1/5 | 3/6 | 2/6 | 2/6 | 1/6 | 3/6 | 3/6 | 1/5 | 1/5 |

Task difficulty as shown in per-task solve matrix Table [3](https://arxiv.org/html/2609.26121#S5.T3 "Table 3 ‣ 5.1 DeepSWE Benchmark ‣ 5 Results ‣ DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents") also moderates DTOC’s effectiveness. Two tasks, narwhals and fastapi, remain unsolved by all evaluated models, indicating intrinsic difficulty beyond context-management considerations. In contrast, ts-pattern is solved in 99 of 1010 model-condition pairs and serves as a near-ceiling baseline. DTOC’s largest effects appear on medium-difficulty tasks. For example, sqlite-utils and mashumaro are solved only under DTOC for specific models, implying that context curation can be the decisive factor separating success from failure when tasks are challenging but still tractable.

### 5.2 Ablation Study

We did carry out a small-scale explorative ablation study on real-world proprietary data and code.
To isolate the contribution of individual DTOC components, we compare four configurations: no compression, tool tracking only, disable-only, and full enable+disable (Table [4](https://arxiv.org/html/2609.26121#S5.T4 "Table 4 ‣ 5.2 Ablation Study ‣ 5 Results ‣ DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents")).

The results reveal that implementing tool tracking without the ability to disable context (‘+ Tool tracking, no disable’) resulted in a slight performance degradation to 77.8% success rate while maintaining high context usage (87K tokens). The high frequency of file re-reads (4.2 average) suggests that tracking alone introduces significant overhead and necessitates a recovery mechanism to be effective.
Interestingly, the ‘Disable only’ configuration significantly outperformed the uncompressed baseline, achieving an 81.4% success rate with only 57K tokens. This indicates that aggressive context pruning can improve model focus by removing "noise," though the non-zero re-read average (0.1) highlights a persistent risk of irreversible information loss. The Full DTOC configuration achieved the optimal balance, reaching the highest overall success rate of 83.6% using 61K tokens. By integrating both disabling and dynamic re-enabling capabilities, the framework eliminated file re-reads entirely (0.0). This confirms that the ability to recover previously compressed context is essential for achieving peak reliability, allowing the model to surpass the baseline performance while maintaining a significantly leaner context footprint.

Table 4: Ablation of DTOC components

| Configuration | Success rate (%) | Context (tokens) | Notes | File re-reads (avg) |
| --- | --- | --- | --- | --- |
| No compression (baseline) | 78.2 | 89K | — | 0.0 |
| + Tool tracking, no disable | 77.8 | 87K | Overhead only | 4.2 |
| + Disable only (no re-enable) | 81.4 | 57K | Information loss risk | 0.1 |
| + Full DTOC (enable + disable) | 83.6 | 61K | Best result | 0.0 |

## 6 Discussion

### 6.1 Reflection on Results

DeepSWE reveals clear model-family differences in DTOC effectiveness. Sonnet 4.6, GPT-5.4 and GPT-5.5 achieve higher solve rates and lower costs, while Opus 4.8 and Gemini 3.5 Flash show little or no aggregate benefit. For Opus, this neutrality masks complementary task-level effects: DTOC enables solving mashumaro, whereas DTOC OFF solves sqlite-utils, suggesting that DTOC reshapes rather than consistently expands the model’s capability frontier.

Three model-level factors may explain the observed variation. First, native context-management behavior appears important: models that already avoid redundant tool interactions (e.g., GPT-5.4) amplify DTOC’s benefits, whereas models that employ many small reasoning steps (e.g., Gemini) generate management overhead faster than DTOC can reduce context size. Second, output verbosity influences effectiveness; Opus produces substantially larger outputs (131K avg), reducing the relative savings achievable through compression. Third, instruction-following fidelity may play a role. Models that interpret the generic manage\_context prompt as a signal to perform frequent shallow compressions appear to perform worse than models that apply compression selectively. These findings suggest that DTOC should be adapted to individual model families or guided by learned, model-specific policies.

For medium-difficulty tasks such as sqlite-utils and mashumaro, DTOC is often the factor that separates success from failure. In contrast, easier tasks such as ts-pattern are solved consistently regardless of compression, while more difficult tasks such as narwhals and fastapi remain unsolved across all evaluated conditions. Sonnet’s failure on sqlite-utils without DTOC, where execution stalled after only two steps, illustrates how context saturation can contribute to premature task abandonment. DTOC mitigates such failures by preserving a manageable active context throughout long-horizon trajectories.

For compression-responsive models, DTOC yields substantial economic benefits, reducing cost per solved task by approximately 67–72% for Sonnet 4.6 (67%) and GPT-5.4 (72%). These gains arise from both direct token savings and improved solve rates, which amortize execution overhead across a larger number of successful outcomes. In contrast, models exhibiting increased token consumption under DTOC, such as Opus and Gemini, incur corresponding cost penalties, highlighting the need for model-specific deployment.

### 6.2 Limitations

Several limitations qualify these findings.
First, the current DeepSWE task selection contains only six feature-request tasks, limiting statistical power and domain coverage; refactoring and software architecture tasks were not evaluated. Expanding DeepSWE coverage to include additional task types and programming languages, such as Go, JavaScript, and Rust, would improve the breadth of the evaluation.
Second, all experiments used a single generic manage\_context prompt, which may not align equally well with the instruction-following behavior of all models.
Third, the binary success metric, defined as whether all tests pass, obscures meaningful differences in partial progress.
Finally, only a single trial was performed for each model–task–condition combination, leaving the influence of stochastic variability unmeasured. Additionally, the DeepSWE evaluation compares only DTOC ON versus OFF, without direct comparison against alternative context-management approaches such as LLMLingua [[6](https://arxiv.org/html/2609.26121#bib.bib18 "LLMLingua: compressing prompts for accelerated inference of large language models")], prompt truncation, or extractive summarization. Direct comparison is non-trivial because these methods target static prompts rather than dynamic multi-turn agent trajectories, but establishing relative performance remains an important direction. We note that DTOC is complementary to token-level compression: methods like LLMLingua could be applied *within* individual tool outputs before DTOC manages their inter-output visibility.

### 6.3 Future Work

This paper should be seen as an introduction to the method and a proof of principle. Several directions merit further investigation to more robustly investigate its behavior in different contexts and expand into new feature sets and directions.
First, larger benchmark suites, multiple independent runs and additional baseline comparisons would enable statistical testing of observed effects. We experimented with other benchmarks as well, such as HotPotQA and proprietary company data and tasks, but we do recommend to expand DeepSWE coverage first, to keep the focus on long horizon tasks where context management matters most.
Second, replicating ablation studies on DeepSWE could further isolate the impact of specific DTOC capabilities under different contexts. Initial experiments on proprietary use cases indicate that full DTOC outperforms DTOC that just turns context off versus no DTOC.
Third, budget-aware prompting could expose real-time token counts and context-budget thresholds, helping agents make more informed compression decisions. Also, hybrid compression mechanisms that retain machine-generated summaries within placeholders may preserve useful preview information while still reducing context size, potentially benefiting models that prefer frequent incremental compression.
Finally, model-adaptive compression policies could be made visible through adjacent AI methods such as process mining, learned from trajectories or selected dynamically by the orchestrator to better align compression behavior with model-specific reasoning patterns.

## 7 Conclusion

Dynamic Tool Output Compression (DTOC) addresses context management as a first-class problem in agentic systems, rather than a secondary implementation detail.
By allowing agents to explicitly control the visibility of past tool outputs, DTOC reframes compression from an irreversible, lossy operation into a reversible decision embedded in the agent’s reasoning loop.

Empirically, DTOC yields model-dependent effects. For compression-responsive models (Sonnet 4.6, GPT-5.4, GPT-5.5), observed solve rates improve (e.g., from 20% to 50% for Sonnet, 33% to 50% for GPT-5.4) and cost per solved task decrease by 67–72%. For Claude Opus 4.8 and Gemini 3.5 Flash, solve rates remain unchanged while token consumption increases by 18–49%, indicating that DTOC should not be deployed without model-specific tuning. These findings are based on single runs per condition and require validation through repeated trials.

Qualitative analysis of agent trajectories reveals that agents spontaneously adopt a repertoire of compression strategies, such as breadth-then-depth exploration, iterative refinement, and chunking that are sensitive to task structure and uncertainty. This diversity supports the central hypothesis that compression decisions are best made by the agent itself, conditioned on its evolving beliefs and plan, rather than imposed via fixed external rules. DTOC thus forms a bridge between low-level context-window mechanics and high-level planning, allowing compression to be optimized in situ as part of the reasoning process.

Taken together, these results suggest that context engineering should be treated as a core dimension of agent design, on par with planning, tool use, and memory. DTOC provides a practical, model-agnostic framework for doing the same. It is simple to implement, requiring only orchestrator-level tracking of tool outputs and a single additional tool in the agent’s action space, compatible with existing ReAct-style agents and tool ecosystems, and effective for models whose reasoning style aligns with selective, deliberate compression. The explicit tool-based interface, with orchestrator-assigned identifiers and structured JSON envelopes, ensures that DTOC can be deployed on any LLM platform without relying on provider-specific APIs or tool-call mechanisms. Looking forward, combining DTOC with learned compression policies, hierarchical summaries, and multi-agent coordination mechanisms offers a rich research agenda. As models continue to grow and tasks become more complex, we expect DTOC-like mechanisms to become a foundational component of scalable, production-grade agentic systems, which are lossless, agent-driven, and reversible.

{credits}

#### 7.0.1 \discintname

The authors have no competing interests to declare that are relevant to the content of this article.
