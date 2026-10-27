# Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability

- 来源: https://arxiv.org/abs/2608.06503
- 发布日期: 2026-08-06
- 日期依据: page metadata: citation_date
- 类型: paper
- 主题: 压缩可靠性、长程Agent
- 抓取状态: full_text_html
- 正文来源: https://arxiv.org/html/2608.06503
- 抓取时间 UTC: 2026-10-26T09:35:23.034501+00:00
- 作者: Min, Guanghui, Wu, Liang, Darbari, Mayank, Chen, Chen, Hong, Liangjie

## 来源摘要 / 页面简介

Abstract: Recurrent context compression controls context growth in long-horizon agents, but its behavioral effects remain poorly understood. In this preliminary empirical study, we show that compression can weaken the influence of recent interactions, increasing blocked actions, repeated exploration, and instability across runs. Motivated by these observations, we introduce TRACE, a verifier-guided framework that evaluates individual compaction events through paired closed-loop continuations from the same environment state and uses summary preferences to optimize a natural-language compression prompt while keeping all models frozen. Initial results on AppWorld show improvements over existing compression baselines in task performance, multi-run reliability, and context--execution efficiency. These findings provide early evidence for boundary-local evaluation as a promising direction for reliable agent context compression.

## 抓取正文

# Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability

Guanghui Min
Affiliation: Department of Computer Science, University of Virginia,
Charlottesville, VA, USA
Affiliation: Nokia, Sunnyvale, CA, USA
Email: [jjm8vr@virginia.edu](mailto:)
  
Liang Wu
Affiliation: Nokia, Sunnyvale, CA, USA
Email: [zrh6du@virginia.edu](mailto:)
  
Mayank Darbari
Affiliation: Nokia, Sunnyvale, CA, USA
Email: [liang.wu@nokia.com](mailto:)
  
Chen Chen
Affiliation: Department of Computer Science, University of Virginia,
Charlottesville, VA, USA
Email: [mayank.darbari@nokia.com](mailto:)
  
Liangjie Hong
Affiliation: Nokia, Sunnyvale, CA, USA
Email: [liangjie.hong@nokia.com](mailto:)

###### Abstract

Recurrent context compression controls context growth in long-horizon agents, but its behavioral effects remain poorly understood. In this preliminary empirical study, we show that compression can weaken the influence of recent interactions, increasing blocked actions, repeated exploration, and instability across runs. Motivated by these observations, we introduce TRACE, a verifier-guided framework that evaluates individual compaction events through paired closed-loop continuations from the same environment state and uses summary preferences to optimize a natural-language compression prompt while keeping all models frozen. Initial results on AppWorld show improvements over existing compression baselines in task performance, multi-run reliability, and context–execution efficiency. These findings provide early evidence for boundary-local evaluation as a promising direction for reliable agent context compression. Our code is in <https://github.com/nokia-applied-research/Trace>.

|  |
| --- |
|  |

## 1 Introduction

Large language models increasingly operate over long, evolving contexts rather than isolated prompts. Such settings include interactive agents that interleave reasoning, actions, observations, and plan revision ([Yao et al., 2023](https://arxiv.org/html/2608.06503#bib.bib1); [Shinn et al., 2023](https://arxiv.org/html/2608.06503#bib.bib2); [Wang et al., 2024b](https://arxiv.org/html/2608.06503#bib.bib3)); browser, application, API, and office environments that require extended interaction with external systems ([Zhou et al., 2024](https://arxiv.org/html/2608.06503#bib.bib23); [Trivedi et al., 2024](https://arxiv.org/html/2608.06503#bib.bib24); [Wang et al., 2024c](https://arxiv.org/html/2608.06503#bib.bib25)); policy-constrained conversational workflows; and retrieval-intensive research tasks that accumulate evidence over multiple steps. In all of these settings, the context grows with every tool output, retrieved source, intermediate decision, user clarification, and partial result. Repeatedly supplying the full history increases inference cost and peak-context pressure, while making the information needed for the next decision increasingly difficult to locate. Context compression is therefore essential for scalable long-horizon LLM systems.

Prior work has progressively moved from document-level prompt compression to trajectory-aware context management. General prompt-compression methods prune, rewrite, or distill input tokens to reduce inference cost while preserving semantic content or downstream task quality ([Li et al., 2023](https://arxiv.org/html/2608.06503#bib.bib5); [Jiang et al., 2023](https://arxiv.org/html/2608.06503#bib.bib6); [Jiang et al., 2024](https://arxiv.org/html/2608.06503#bib.bib7); [Pan et al., 2024](https://arxiv.org/html/2608.06503#bib.bib8); [Xu et al., 2024](https://arxiv.org/html/2608.06503#bib.bib9); [Shandilya et al., 2025](https://arxiv.org/html/2608.06503#bib.bib10)). For long-horizon agents, recent methods recognize that context contains more than ordinary prose: it records action–observation histories, intermediate plans, and evolving interaction state. ReSum and SUPO therefore co-optimize summarization with downstream agent behavior ([Wu et al., 2025](https://arxiv.org/html/2608.06503#bib.bib17); [Lu et al., 2025](https://arxiv.org/html/2608.06503#bib.bib18)); ACON improves compression guidelines by contrasting successful full-context trajectories with failed compressed ones ([Kang et al., 2026](https://arxiv.org/html/2608.06503#bib.bib19)); and practical systems compact long sessions into structured natural-language checkpoints ([OpenClaw Contributors, 2026a](https://arxiv.org/html/2608.06503#bib.bib20); [OpenClaw Contributors, 2026b](https://arxiv.org/html/2608.06503#bib.bib21); [Nous Research, 2026](https://arxiv.org/html/2608.06503#bib.bib22)). These advances establish that agent context should be treated differently from a static document.

Nevertheless, these approaches share an implicit substitution assumption: once a shorter checkpoint retains the task-relevant content, it can stand in for the original interaction history. This assumption overlooks the directional role of history in long-horizon execution. A raw trajectory does not merely record facts; its ordered action–observation sequence anchors what has already been completed, where execution currently stands, and whether the task is ready to terminate. Summarization can flatten this directed process into a declarative account of past progress and future plans. As a result, even when salient entities and progress labels are retained, a frozen agent may lose its local position in the trajectory, replay completed actions, or continue acting beyond the terminal frontier. The central challenge is therefore to compress history while preserving a representation from which the frozen agent can reliably recognize its current execution state.

We propose TRACE
(Trajectory-Relative
Agent
Context ComprEssion), a
verifier-guided framework for optimizing recurrent context compression for
frozen long-horizon agents. Rather than inferring compression quality from
terminal task outcomes, TRACE evaluates each compaction boundary
directly. From the same environment state, it compares paired closed-loop
continuations before and after compression and measures the additional blocked
or repeated exploration induced by the summary. These boundary-local scores
produce preferences between candidate summaries. A frozen proposer observes
only which summary is preferred—not the subsequent actions, observations, or
error signals—and uses these preferences to revise the natural-language
compression template. The compressor model, downstream agent, tools, and
decoding configuration remain fixed throughout.

Our contributions are threefold:

* •

  Behavioral diagnosis.
  We show that recurrent compression can attenuate the effect of recent
  interactions, increasing blocked execution and repeated exploration while
  reducing multi-run reliability.
* •

  Boundary-local compression optimization.
  We introduce a paired closed-loop verifier that separates
  compression-induced execution regressions from the frozen agent’s intrinsic
  behavioral variability, and use its summary preferences to optimize the
  compression template without exposing rollout details to the proposer.
* •

  Empirical evaluation.
  On AppWorld, TRACE consistently outperforms existing compression
  baselines across task difficulty levels, improves repeated-run reliability, and
  keeps average execution steps close to full context while substantially reducing
  peak context usage. Moreover, the template optimized with MiniMax-M3 transfers
  to Kimi-K2.7-Code without further optimization, outperforming all compressed
  baselines and even exceeding full context in overall accuracy and Pass2.

## 2 Preliminaries

### 2.1 Context Compression for Frozen Long-Horizon Agents

Notations.
We study context compression for a fixed downstream agent ℳ\mathcal{M} interacting with an external environment ℰ\mathcal{E}.
The agent is fixed in the sense that its language model, system prompt, action interface, output parser, and decoding procedure are not modified.
Let 𝒟={ui}i=1|𝒟|\mathcal{D}=\{u\_{i}\}\_{i=1}^{|\mathcal{D}|} denote a distribution of long-horizon tasks, where each task begins with an instruction uu.
A rollout is denoted by τ=(u,a1,o1,…,aT,oT)\tau=(u,a\_{1},o\_{1},\ldots,a\_{T},o\_{T}).
Before decision step tt, the complete interaction history is ht=(u,a1,o1,…,at−1,ot−1)h\_{t}=(u,a\_{1},o\_{1},\ldots,a\_{t-1},o\_{t-1}), where aia\_{i} is an agent action and oi=ℰ⁡(ai)o\_{i}=\mathcal{E}(a\_{i}) is the corresponding environment observation.
We distinguish the complete interaction history hth\_{t} from the agent-visible context ztz\_{t} supplied to the frozen agent.
Given ztz\_{t}, the agent generates at∼ℳ(⋅∣zt)a\_{t}\sim\mathcal{M}(\cdot\mid z\_{t}) and receives ot=ℰ⁡(at)o\_{t}=\mathcal{E}(a\_{t}).
Full-context execution uses zt=htz\_{t}=h\_{t}.
Since |ht||h\_{t}| generally grows with tt, the complete history can eventually exceed the practical context budget of long-horizon execution.

### 2.2 Problem Definition

Long-horizon agents must periodically replace their growing working context with a bounded textual representation ([Kang et al., 2026](https://arxiv.org/html/2608.06503#bib.bib19); [Lu et al., 2025](https://arxiv.org/html/2608.06503#bib.bib18); [Wang et al., 2024a](https://arxiv.org/html/2608.06503#bib.bib26); [Nous Research, 2026](https://arxiv.org/html/2608.06503#bib.bib22); [OpenClaw Contributors, 2026a](https://arxiv.org/html/2608.06503#bib.bib20)).
Let 𝒞\mathcal{C} denote a compressor and BB denote the context budget.
Given the current agent-visible context ztz\_{t}, action ata\_{t}, and observation oto\_{t}, define the pre-compaction context as z¯t+1=zt⊕(at,ot)\bar{z}\_{t+1}=z\_{t}\oplus(a\_{t},o\_{t}), where ⊕\oplus denotes textual concatenation.
The context supplied at the next decision step is recursively updated as

|  |  |  |  |
| --- | --- | --- | --- |
|  | zt+1={z¯t+1,|z¯t+1|≤B,𝒞⁡(z¯t+1,B),|z¯t+1|>B.z\_{t+1}=\begin{cases}\bar{z}\_{t+1},&|\bar{z}\_{t+1}|\leq B,\\ \mathcal{C}(\bar{z}\_{t+1};B),&|\bar{z}\_{t+1}|>B.\end{cases} |  | (1) |

Thus, after a compaction event, the replacement context zt+1z\_{t+1} becomes the only historical record available to the frozen agent and to subsequent compaction steps.
For a compressor 𝒞\mathcal{C}, let p𝒞,B​(τ∣u)p\_{\mathcal{C},B}(\tau\mid u) denote the rollout distribution induced by the frozen agent ℳ\mathcal{M}, environment ℰ\mathcal{E}, and the recursive context transition in Equation [1](https://arxiv.org/html/2608.06503#S2.E1 "Equation 1 ‣ 2.2 Problem Definition ‣ 2 Preliminaries ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability").
Let R⁡(τ)R(\tau) denote the environment-defined terminal reward.

## 3 Empirical Study: Behavioral Effects of Context Compression

In this section, we first show that recurrent compression degrades task success and reliability, especially over longer trajectories. We then trace this degradation to execution-state mislocalization and examine how it manifests as blocked execution and repeated exploration after compaction.

### 3.1 Repeated Compression Degrades Agent Behavior

(a) Compression performance.

(b) Cross-run behavioral instability.

(c) Long-horizon degradation.

Figure 1: Repeated context replacement degrades agent behavior despite refetchable information.
AppWorld allows agents to re-query persistent application state, so previously observed information remains recoverable after compaction.
(a) Mean pass rate declines as the context budget shrinks.
(b) The widening gap between P​@​2P@2 and P2P^{2} indicates reduced reliability across repeated runs.
(c) Even with summary-based compaction, degradation is substantially sharper for tasks with longer full-context reference horizons.

Equation ([1](https://arxiv.org/html/2608.06503#S2.E1 "Equation 1 ‣ 2.2 Problem Definition ‣ 2 Preliminaries ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability")) makes context compression a recurrent intervention: once the working context exceeds the budget, the replacement context becomes the input to both subsequent decisions and later compaction events. Its quality therefore cannot be assessed from a single replacement in isolation. A locally plausible summary may still alter the downstream rollout once it is repeatedly reused as the agent’s working context.

We evaluate this effect on the 147-task AppWorld train–development split ([Trivedi et al., 2024](https://arxiv.org/html/2608.06503#bib.bib24)). AppWorld is a stateful API-use benchmark: agents interact with persistent simulated applications through API calls, and earlier observations can be recovered by re-querying the underlying application state. This setting differs from knowledge-intensive tasks, where summary-based compaction is expected to outperform FIFO truncation because it preserves facts that would otherwise be permanently discarded. In AppWorld, removing an observation from the working context does not necessarily make its content permanently inaccessible. We use MiniMax-M3 as both compressor and downstream agent ([MiniMax, 2026](https://arxiv.org/html/2608.06503#bib.bib27)). Our evaluation harness adapts OpenClaw’s recurrent compaction loop11
1
Adapted from the OpenClaw agent-core harness,
<https://github.com/openclaw/openclaw/blob/0e7b5c34292cc28707a0e5a0b730cff295ef0f8a/packages/agent-core/src/harness/compaction/compaction.ts>
(commit 0e7b5c34292cc28707a0e5a0b730cff295ef0f8a). ([OpenClaw Contributors, 2026a](https://arxiv.org/html/2608.06503#bib.bib20)) . This common runtime pattern is also used in other agentic frameworks such as AG2 and Hermes Agent ([Wang et al., 2024a](https://arxiv.org/html/2608.06503#bib.bib26); [Nous Research, 2026](https://arxiv.org/html/2608.06503#bib.bib22)).

Figure [1](https://arxiv.org/html/2608.06503#S3.F1 "Figure 1 ‣ 3.1 Repeated Compression Degrades Agent Behavior ‣ 3 Empirical Study: Behavioral Effects of Context Compression ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability") reveals a surprising budget-dependent pattern. Summary-based compaction does not uniformly outperform FIFO truncation: at 1616K, 88K, and 44K, FIFO matches or slightly exceeds summary-based execution. Their difference emerges only under the tightest budget, where summary-based compaction reaches 72.8%72.8\% while FIFO drops to 42.2%42.2\%. Thus, in this information-refetchable setting, the advantage of summarization over recency-only truncation appears only under severe compression. Both policies nevertheless remain below full-context performance.

Mean pass rate alone does not fully characterize this degradation. Following the repeated-run reliability metrics used in τ\tau-bench and τ2\tau^{2}-bench ([Yao et al., 2025](https://arxiv.org/html/2608.06503#bib.bib30); [Barres et al., 2025](https://arxiv.org/html/2608.06503#bib.bib29)), PkP^{k} denotes the fraction of tasks solved in all kk independent runs, whereas P​@​kP@k denotes the fraction solved in at least one of the kk runs. We use k=2k=2 throughout. Under stronger compression, the gap between P​@​2P@2 and P2P^{2} widens substantially. Compression therefore does not merely remove a subset of tasks from the agent’s reach: it converts some tasks that were reliably solved into tasks that are only intermittently solved under the same runtime condition.

This instability is more pronounced on tasks with longer full-context execution horizons, measured by the median number of steps in successful full-context runs. Even under summary-based compaction, longer-horizon tasks degrade more sharply as the budget shrinks, consistent with an accumulating effect of repeated context replacement.

Together, these results suggest that successful compression depends not only on preserving globally relevant information, but also on maintaining the local continuity that anchors the agent’s current execution position. FIFO preserves recent action–observation continuity despite discarding most earlier history, whereas repeated summary replacement can progressively weaken this local anchor over longer trajectories. We next isolate this effect at matched decision points.

Takeaway: Compressor quality is better reflected by multi-run stability than by single-run performance alone.

### 3.2 Beyond Information Loss: Execution-State Mislocalization

Figure 2: Terminal completion.
Total height denotes the termination rate; dark segments denote
termination in the required form.

The degradation in Section [3.1](https://arxiv.org/html/2608.06503#S3.SS1 "3.1 Repeated Compression Degrades Agent Behavior ‣ 3 Empirical Study: Behavioral Effects of Context Compression ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability") is often attributed
to the loss of facts, variables, or task progress during summarization. This account is incomplete in our setting: earlier
observations remain re-queryable in AppWorld, while FIFO truncation remains
competitive at moderate budgets despite discarding most earlier history.
We therefore ask whether compression also weakens the agent’s ability to
recover its current execution state—what has been completed, what remains
actionable, and whether execution should continue or terminate.

Summary Replacement Disrupts Terminal Completion.
We first probe the final decision before termination. For each trajectory with
at least one compaction, we hold the task, environment, agent header, and
decision point fixed, and compare the actual summary context, FIFO truncation
at the same budget, and the full pre-terminal history. All turns are
reconstructed in their native interaction format, and we sample 1010 next
actions under each rendering.

Figure [2](https://arxiv.org/html/2608.06503#S3.F2 "Figure 2 ‣ 3.2 Beyond Information Loss: Execution-State Mislocalization ‣ 3 Empirical Study: Behavioral Effects of Context Compression ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability") shows that, at 22K, the summary condition
terminates in only 44.6%44.6\% of samples, with 37.3%37.3\% using the required form,
compared with 77.2%77.2\%/68.1%68.1\% for FIFO and 66.6%66.6\%/60.6%60.6\% for full
history. The deficit persists at 44K and 88K. It is most pronounced when
correct completion requires no substantive response: the summary-conditioned
agent more often continues acting or supplies unnecessary content instead of
terminating directly. Summary replacement therefore impairs both completion
recognition and compliance with the required output form.

Takeaway: Compression can weaken action commitment and adherence to the required output form.

Compression Attenuates Recent Interaction Updates.
We next examine whether this effect persists throughout a summary’s lifetime.
For each compaction, let St−1S\_{t-1} denote the previous summary, Δt\Delta\_{t} the
new raw interaction history, and
St=C⁡(St−1,Δt)S\_{t}=C(S\_{t-1},\Delta\_{t}) the updated summary. At every recorded decision
boundary before the next compaction, we construct four matched contexts: the
full raw prefix; St−1S\_{t-1} followed by the uncompressed Δt\Delta\_{t}; the updated
summary StS\_{t}; and St−1S\_{t-1} with Δt\Delta\_{t} omitted. Each condition is then
followed by the same recorded suffix and ends at the same decision point.

Figure 3: Effect of recent interactions.
Divergence from full-history behavior when the new interaction history is
retained verbatim, compressed, or omitted. Error bars denote task-level
95%95\% bootstrap confidence intervals.

We independently sample 2424 next actions under each context. Sampled actions
are neither executed nor fed back to the agent. We canonicalize the primary API
call and compute its noise-corrected total-variation divergence from the
full-history distribution, averaging first over all decision points in the
summary’s lifetime and then over tasks.
Figure [3](https://arxiv.org/html/2608.06503#S3.F3 "Figure 3 ‣ 3.2 Beyond Information Loss: Execution-State Mislocalization ‣ 3 Empirical Study: Behavioral Effects of Context Compression ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability") reveals a clear gradient. Retaining the
raw update yields the smallest divergence (0.1490.149); compressing it into the
updated summary increases divergence to 0.2330.233; and omitting it entirely
produces the largest shift (0.2890.289). OpenClaw therefore preserves part of the
behavioral effect of recent interactions, but systematically attenuates it
relative to retaining them verbatim.

Together, these probes identify a common functional failure of recurrent
compression: recent interactions that should revise execution exert a weaker
or distorted effect on subsequent decisions after being absorbed into the
summary. This may arise from omitted information, distorted progress, or
ineffective use of retained information; our experiments do not fully separate
these causes. Goal revisions, tool failures, unexpected outcomes, and
completion events are consequential precisely because they should change how
the agent continues. This motivates evaluating compression at the boundary where it occurs, using
its downstream execution consequences rather than terminal outcomes or static
textual fidelity.

### 3.3 Compression Induces Regressive Exploration

The preceding intervention shows that compression preserves part of the
behavioral effect of recent interactions, but attenuates it relative to
retaining them verbatim. We next examine how this attenuation manifests during
closed-loop execution.

At each compaction boundary, we restore the same AppWorld execution state and
independently roll out the frozen agent under two context renderings. PRE
retains the raw interaction update available before compaction, whereas POST
uses the updated summary together with OpenClaw’s retained raw turn. These are
free-running closed-loop rollouts using the original AppWorld tools: each
generated action is executed, and its actual observation is returned before
the next decision. We evaluate 590590 boundaries and 4,6404{,}640 rollouts, using
five samples per rendering for first compactions and three for later
compactions, each capped at five actions.

Figure 4: Blocked execution and regressive exploration.
Marginal POST-minus-PRE effects at each of the first five actions after
compaction. Blocked/error actions follow AppWorld’s native error contract;
refetch/replay denotes an exact action signature previously observed before
the boundary or earlier in the same rollout. Error bars denote
boundary-level 95%95\% bootstrap confidence intervals.

Figure [4](https://arxiv.org/html/2608.06503#S3.F4 "Figure 4 ‣ 3.3 Compression Induces Regressive Exploration ‣ 3 Empirical Study: Behavioral Effects of Context Compression ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability") reports the marginal effect of each action
step, rather than the cumulative effect through that step. Compression
immediately increases blocked execution: POST produces 0.1080.108 more
blocked/error actions than PRE at the first action, and the effect remains
positive throughout the continuation. Refetching is initially weaker
(0.0310.031), but rises at the second action and remains positive thereafter.

This temporal pattern is consistent with two complementary consequences of
attenuating recent interaction updates. Compression can first make previously
established execution state less directly accessible, producing explicit
blocks, and subsequently induce additional work to recover or reconstruct that
state. Thus, retained information may remain recoverable while becoming less
actionable for continued execution.

Takeaway: Compression increases regressive exploration, weakening the influence of interactions retained within the context window.

## 4 Trace: Optimizing the Compression Prompt

Section [3](https://arxiv.org/html/2608.06503#S3 "3 Empirical Study: Behavioral Effects of Context Compression ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability") shows that compression can make recently
established execution state less actionable, leading to blocked actions and
repeated exploration. TRACE, illustrated in
Figure [5](https://arxiv.org/html/2608.06503#S4.F5 "Figure 5 ‣ 4.1 Boundary-Local Execution Verifier ‣ 4 Trace: Optimizing the Compression Prompt ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability"), converts this observation into a
boundary-local optimization signal. All model parameters remain frozen: we
optimize only the natural-language compression template used by the compressor.

Prior prompt-optimization methods such as ACON construct feedback from
trajectories where the agent succeeds with full context but fails with
compressed context ([Kang et al., 2026](https://arxiv.org/html/2608.06503#bib.bib19)). Such trajectory-level supervision,
however, cannot isolate compression-induced errors from the agent’s intrinsic
behavioral variation and downstream contingencies. A successful trajectory
does not imply that every intermediate compression was faithful, since a
compression defect may never be exercised or may be recovered through
subsequent environment interactions. Conversely, a failed trajectory does not
imply that its summaries were poor, since failure may arise independently of
compression. We therefore construct supervision directly at individual
compaction boundaries using paired closed-loop continuations from the same
execution state.

### 4.1 Boundary-Local Execution Verifier

Our verifier measures whether a compression event introduces additional
observable execution regressions, operationalized as actions that are blocked
by the environment or repeat tool calls that have already been executed.
Rather than attributing the eventual task outcome to every summary along the
trajectory, we evaluate each summary locally at the boundary where it replaces
the raw interaction history.

Consider a compaction boundary bb. Let xb−x\_{b}^{-} denote the context immediately
before replacement, consisting of the previous recurrent summary, if any,
followed by the newly accumulated raw interactions. Given a candidate summary
ss, let xb+​(s)x\_{b}^{+}(s) denote the corresponding post-compaction context,
including the recent raw turn retained by the compaction policy.

Starting from the same environment state, we independently roll out the frozen
agent under xb−x\_{b}^{-} and xb+​(s)x\_{b}^{+}(s). Both PRE and POST continuations are
fully closed-loop: generated actions are executed through the original tools,
and the resulting observations are returned to the agent. PRE therefore serves
as a paired local control for the frozen agent’s intrinsic execution behavior,
whereas POST captures any additional burden induced by replacing the history
with summary ss.

![Refer to caption](https://arxiv.org/html/2608.06503v2/trace_pipeline.png)

Figure 5: Overview of TRACE.
At each compaction boundary, paired closed-loop continuations are evaluated
from the same environment state. PRE retains the context available before
compaction, whereas POST replaces the compressible history with a candidate
summary. The verifier measures the resulting increase in blocked or
repeated actions and ranks candidate summaries. The frozen proposer receives
the downstream system prompt, the incumbent compression prompt, and the
resulting summary preferences, but not the rollout actions, observations,
errors, or verifier decomposition. It then produces candidate compression
templates, which are selected through end-to-end evaluation on the
development split.

Let zj​(τ)z\_{j}(\tau) indicate whether the jj-th action in continuation τ\tau
constitutes an observable execution regression. We define the short-horizon
execution burden as

|  |  |  |  |
| --- | --- | --- | --- |
|  | G⁡(τ)=∑j=1Kzj​(τ),G(\tau)=\sum\_{j=1}^{K}z\_{j}(\tau), |  | (2) |

where KK is a fixed rollout horizon. The compression-induced burden of
candidate summary ss is

|  |  |  |  |
| --- | --- | --- | --- |
|  | Δ​Gb​(s)=𝔼⁡[G⁡(τb+​(s))]−𝔼⁡[G⁡(τb−)],\Delta G\_{b}(s)=\mathbb{E}\!\left[G\!\left(\tau\_{b}^{+}(s)\right)\right]-\mathbb{E}\!\left[G\!\left(\tau\_{b}^{-}\right)\right], |  | (3) |

and the verifier score is

|  |  |  |  |
| --- | --- | --- | --- |
|  | Qb​(s)=−Δ​Gb​(s).Q\_{b}(s)=-\Delta G\_{b}(s). |  | (4) |

A higher score indicates that the summary introduces fewer additional execution
regressions relative to retaining the pre-compaction context.

In AppWorld, we instantiate zjz\_{j} as the union of two observable events. An
action is *blocked* when it triggers AppWorld’s native execution-error
contract. An action is *repeated* when its canonicalized tool-call
signature matches one executed before the boundary or earlier in the same
continuation. Their union is counted once, including when an action satisfies
both conditions. These signals capture immediate execution failures and
redundant attempts to recover information or repeat operations already explored
before compression.

Importantly, PRE is not treated as an optimal trajectory. It serves only as a
paired control from the same execution state, allowing the verifier to control
for the frozen agent’s intrinsic stochasticity and execution errors when
estimating the local effect of compression.

### 4.2 Verifier-Guided Prompt Optimization

Following ACON ([Kang et al., 2026](https://arxiv.org/html/2608.06503#bib.bib19)), we optimize the compressor in
natural-language prompt space rather than updating model parameters. The
difference lies in how supervision is constructed. Instead of contrasting
terminally successful and failed trajectories, TRACE constructs
preferences between summaries evaluated at the same compaction boundary.

#### Training-boundary selection.

We first collect PRE and POST continuations for compaction boundaries in the
AppWorld training split using the frozen base compressor. From these
continuations, we identify boundaries exhibiting blocked actions and group them
according to AppWorld’s native execution-error type. We then select 12
boundaries through stratified sampling across these error categories. This
provides optimization examples covering multiple forms of execution blockage
rather than concentrating on the most frequent error type.

#### Candidate generation and boundary-local scoring.

Let P0P\_{0} denote the base compression template and IbI\_{b} the compressor input
at boundary bb, including the previous summary, newly accumulated interaction
history, retained recent turn, and compression budget. The frozen base
compressor independently generates three candidate summaries:

|  |  |  |  |
| --- | --- | --- | --- |
|  | sb,n=S⁡(Ib,P0),n∈{1,2,3}.s\_{b,n}=S(I\_{b};P\_{0}),\qquad n\in\{1,2,3\}. |  | (5) |

For each candidate, we generate a candidate-specific POST continuation under
xb+​(sb,n)x\_{b}^{+}(s\_{b,n}). The PRE continuations collected for boundary bb remain
frozen and are reused across all three candidates. Each summary is scored using
Equation [4](https://arxiv.org/html/2608.06503#S4.E4 "Equation 4 ‣ 4.1 Boundary-Local Execution Verifier ‣ 4 Trace: Optimizing the Compression Prompt ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability"), so differences among candidates arise only
from their POST behavior rather than from variation in the PRE control.

For each boundary, we retain the highest- and lowest-scoring candidates,

|  |  |  |  |
| --- | --- | --- | --- |
|  | sb+=arg⁡maxsb,n​Qb​(sb,n),sb−=arg⁡minsb,n​Qb​(sb,n),s\_{b}^{+}=\arg\max\_{s\_{b,n}}Q\_{b}(s\_{b,n}),\qquad s\_{b}^{-}=\arg\min\_{s\_{b,n}}Q\_{b}(s\_{b,n}), |  | (6) |

forming 12 boundary-matched contrastive examples:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒟pref={(Ib,sb+,sb−)}b=112.\mathcal{D}\_{\mathrm{pref}}=\left\{\bigl(I\_{b},s\_{b}^{+},s\_{b}^{-}\bigr)\right\}\_{b=1}^{12}. |  | (7) |

#### System-aware prompt proposal.

During preliminary experiments, we found that guidelines inferred solely from
contrastive summaries could contradict the frozen downstream system prompt.
For example, when an incorrect variable name in a summary caused an execution
error, the proposer often added a rule such as
“variables from previous sessions are not preserved,” even though
the system prompt explicitly states, “You can use the variables from
the previous code blocks in the subsequent code blocks.”

We therefore provide the proposer with the downstream
system prompt in addition to the incumbent compression template and preference
examples. The proposer is instructed to first examine whether either summary
in a pair introduces information or directives inconsistent with the system
prompt, and then use the contrastive pairs to infer revisions to the
compression policy.

The proposer observes only the compressor inputs and the better–worse summary
pairs. It does not observe the subsequent rollout actions, environment
observations, blocked-action errors, repeated-call indicators, or verifier
decomposition. This prevents it from directly encoding individual rollout
failures into the template.

A frozen proposer generates five complete candidate templates:

|  |  |  |  |
| --- | --- | --- | --- |
|  | {P1,…,P5}=G⁡(P0,Hsys,𝒟pref),\{P\_{1},\ldots,P\_{5}\}=G\!\left(P\_{0},H\_{\mathrm{sys}},\mathcal{D}\_{\mathrm{pref}}\right), |  | (8) |

where HsysH\_{\mathrm{sys}} is the frozen downstream system prompt. Each candidate
preserves the original summary schema, section structure, placeholders,
renderer, compression budget, and downstream interface. Only the
natural-language instructions governing what the compressor retains, updates,
and removes are revised.

#### End-to-end development selection.

Boundary-local verifier scores are used to construct the contrastive
supervision, but the final template is selected by end-to-end agent performance.
For each proposed template PmP\_{m}, we run the complete recurrent compression and
execution pipeline twice on every task in the AppWorld development split. Let
Yt,r​(Pm)∈{0,1}Y\_{t,r}(P\_{m})\in\{0,1\} indicate whether run r∈{1,2}r\in\{1,2\} succeeds on task
tt. We compute

|  |  |  |  |
| --- | --- | --- | --- |
|  | Pass2​(Pm)=1|𝒟dev|​∑t∈𝒟devYt,1​(Pm)​Yt,2​(Pm),\mathrm{Pass}^{2}(P\_{m})=\frac{1}{|\mathcal{D}\_{\mathrm{dev}}|}\sum\_{t\in\mathcal{D}\_{\mathrm{dev}}}Y\_{t,1}(P\_{m})Y\_{t,2}(P\_{m}), |  | (9) |

which measures the fraction of development tasks completed successfully in
both runs. The selected template is

|  |  |  |  |
| --- | --- | --- | --- |
|  | P⋆=arg⁡maxPm,m∈{1,…,5}​Pass2​(Pm).P^{\star}=\arg\max\_{P\_{m},\;m\in\{1,\ldots,5\}}\mathrm{Pass}^{2}(P\_{m}). |  | (10) |

Thus, terminal outcomes are not used to construct individual summary
preferences: those preferences are determined exclusively by the
boundary-local execution verifier. Terminal performance is used only at the
final model-selection stage on the development split. After selection,
P⋆P^{\star} is frozen and evaluated on the test split without further prompt
revision.

## 5 Preliminary Experiments

### 5.1 Experimental Setup

Evaluation Datasets.
We evaluate on AppWorld, a representative long-horizon tool-use benchmark ([Trivedi et al., 2024](https://arxiv.org/html/2608.06503#bib.bib24)). We optimize prompts on the training split, select the prompt on the development split, and report final results on the test-normal split. We use a compression window of 4,096 tokens and cap each agent rollout at 50 steps. Results on additional benchmarks will be included in future work.

Tool-use Agent and Compressor Models. In our experiments, we evaluate MiniMax-M3 ([MiniMax, 2026](https://arxiv.org/html/2608.06503#bib.bib27)) and Kimi-K2.7-Code ([Moonshot AI, 2026](https://arxiv.org/html/2608.06503#bib.bib28)). For optimization, we use MiniMax-M3 as the frozen LLM proposer. Both models are accessed directly through Ollama.22
2
<https://ollama.com/>

Baselines.
We use the uncompressed full context as the reference. Baselines include FIFO
truncation, LLMLingua-2 token pruning ([Pan et al., 2024](https://arxiv.org/html/2608.06503#bib.bib8)), the OpenClaw
compaction prompt ([OpenClaw Contributors, 2026a](https://arxiv.org/html/2608.06503#bib.bib20)),
the Hermes compaction prompt ([Nous Research, 2026](https://arxiv.org/html/2608.06503#bib.bib22))33
3
Adapted
from the Hermes agent context compressor:
<https://github.com/NousResearch/hermes-agent/blob/cca3b77a4b4217bb13288f0c4cac9710d82432c8/agent/context_compressor.py>.,
and the ACON guidelines optimized on AppWorld, ACON-UT and ACON-UTCO ([Kang et al., 2026](https://arxiv.org/html/2608.06503#bib.bib19)).
More details are in Appendix [A](https://arxiv.org/html/2608.06503#A1 "Appendix A Details of Baselines ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability"). The TRACE prompt is provided in Appendix [B](https://arxiv.org/html/2608.06503#A2 "Appendix B Trace Prompts ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability").

Evaluation Metrics.
For performance, we report the average single-run pass rate, Pass2\mathrm{Pass}^{2},
and Pass​@​2\mathrm{Pass@2} to capture both overall success and multi-run stability.
For efficiency, we report the average number of agent steps and peak input
tokens per task.

### 5.2 Main Results

Table [1](https://arxiv.org/html/2608.06503#S5.T1 "Table 1 ‣ 5.2 Main Results ‣ 5 Preliminary Experiments ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability") reports results on AppWorld
test-normal. All compression methods reduce performance relative to
uncompressed execution, with the degradation becoming substantially larger on
medium and hard tasks. Among the existing compressed baselines,
Prompting-O performs best overall, achieving an average accuracy of 71.471.4,
Pass2 of 59.559.5, and Pass@2 of 83.383.3.

Using the automatically optimized compression prompt, TRACE is the
strongest compressed method overall. It improves over Prompting-O by 5.75.7
points in accuracy (77.177.1 vs. 71.471.4), 7.87.8 points in Pass2
(67.367.3 vs. 59.559.5), and 3.63.6 points in Pass@2
(86.986.9 vs. 83.383.3). The larger improvement in Pass2 indicates that the
optimized prompt improves not only average task success, but also the
consistency of successful execution across the two independent runs.

The effect varies with task difficulty. On easy tasks, TRACE nearly
matches no compression, reaching 94.794.7 accuracy and tying its Pass2 of
91.291.2. On medium tasks, it obtains the highest accuracy and Pass@2 among
compressed methods, although LLMLingua-2 achieves a higher Pass2. On hard
tasks, TRACE consistently outperforms every compressed baseline across
all three metrics, reaching 63.563.5 accuracy, 52.452.4 Pass2, and 74.674.6
Pass@2.

Despite these improvements, a substantial gap from uncompressed execution
remains, particularly on medium and hard tasks. Nevertheless, the consistent
gains over existing compression methods show that boundary-local contrastive
feedback can produce a more reliable compression prompt without updating any
model parameters.

Table 1: Results across different difficulty levels on the AppWorld benchmark (test-normal). Acc., Pass2, and Pass@2 denote mean success over two independent runs, the fraction of tasks solved in both runs, and the fraction solved at least once, respectively. No compression is the uncompressed baseline. Among compressed methods, column-wise best is in bold; our results are highlighted in blue.

|  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Method | Average (168) | | | Easy (57) | | | Medium (48) | | | Hard (63) | | |
| Acc. | Pass2 | Pass@22 | Acc. | Pass2 | Pass@22 | Acc. | Pass2 | Pass@22 | Acc. | Pass2 | Pass@22 |
| Agent: MiniMax-M3 / Compressor: MiniMax-M3 | | | | | | | | | | | | |
| No compression | 85.7 | 77.4 | 94.0 | 95.6 | 91.2 | 100.0 | 87.5 | 77.1 | 97.9 | 75.4 | 65.1 | 85.7 |
| FIFO | 63.7 | 53.0 | 74.4 | 92.1 | 86.0 | 98.2 | 69.8 | 54.2 | 81.2 | 33.3 | 19.0 | 47.6 |
| LLMLingua-2 | 68.2 | 57.7 | 78.6 | 92.1 | 84.2 | 100.0 | 70.8 | 62.5 | 79.2 | 44.4 | 30.2 | 58.7 |
| Prompting-O | 71.4 | 59.5 | 83.3 | 87.7 | 78.9 | 96.5 | 66.7 | 52.1 | 81.2 | 60.3 | 47.6 | 73.0 |
| Prompting-H | 65.2 | 49.4 | 81.0 | 84.2 | 70.2 | 98.2 | 67.7 | 52.1 | 83.3 | 46.0 | 28.6 | 63.5 |
| ACON-UT | 62.5 | 44.6 | 80.4 | 81.6 | 68.4 | 94.7 | 56.2 | 33.3 | 79.2 | 50.0 | 31.7 | 68.3 |
| ACON-UTCO | 62.2 | 47.0 | 77.4 | 82.5 | 70.2 | 94.7 | 58.3 | 37.5 | 79.2 | 46.8 | 33.3 | 60.3 |
| TRACE | 77.1 | 67.3 | 86.9 | 94.7 | 91.2 | 98.2 | 74.0 | 58.3 | 89.6 | 63.5 | 52.4 | 74.6 |

### 5.3 Efficiency

Figure 6: Efficiency across task difficulty.
Average peak input tokens versus average agent steps on AppWorld
test-normal, grouped by task difficulty. Lower-left is better. Red dashed
circles highlight TRACE.

Figure [6](https://arxiv.org/html/2608.06503#S5.F6 "Figure 6 ‣ 5.3 Efficiency ‣ 5 Preliminary Experiments ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability") compares the context and execution
costs of different compression methods. On easy tasks, all methods operate
within a relatively narrow range, as these shorter trajectories require little
compression. The differences become more pronounced on medium and hard tasks,
where the peak context of the full-context agent grows substantially.

Compression generally reduces peak context size, but aggressive reduction can
increase execution cost. FIFO illustrates this trade-off most clearly: it uses
the fewest tokens, yet requires substantially more steps on medium and hard
tasks, suggesting that discarded state must be repeatedly recovered during
execution. Other compression baselines exhibit similar, though less severe,
increases in trajectory length.

In contrast, TRACE maintains an average step count close to the
full-context reference while substantially reducing peak tokens. This advantage
is most visible on hard tasks, where TRACE remains near the
full-context execution length despite using less than half of its peak context.
The results indicate that optimizing against compression-induced regressive
exploration improves not only task performance but also the
context–execution efficiency trade-off.

### 5.4 Cross-Model Transferability

Table 2: Cross-model transfer of the compression template optimized with
MiniMax-M3 and evaluated with Kimi-K2.7-Code on AppWorld test-normal.

|  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Method | Average (168) | | | Easy (57) | | | Medium (48) | | | Hard (63) | | |
| Acc. | Pass2 | Pass@22 | Acc. | Pass2 | Pass@22 | Acc. | Pass2 | Pass@22 | Acc. | Pass2 | Pass@22 |
| Agent: Kimi-K2.7-Code / Compressor: Kimi-K2.7-Code | | | | | | | | | | | | |
| No compression | 82.7 | 73.8 | 91.7 | 93.9 | 89.5 | 98.2 | 76.0 | 60.4 | 91.7 | 77.8 | 69.8 | 85.7 |
| FIFO | 58.3 | 47.0 | 69.6 | 93.0 | 87.7 | 98.2 | 57.3 | 39.6 | 75.0 | 27.8 | 15.9 | 39.7 |
| LLMLingua-2 | 35.7 | 26.8 | 44.6 | 78.9 | 68.4 | 89.5 | 13.5 | 2.1 | 25.0 | 13.5 | 7.9 | 19.0 |
| Prompting-O | 46.1 | 33.3 | 58.9 | 80.7 | 71.9 | 89.5 | 32.3 | 18.8 | 45.8 | 25.4 | 9.5 | 41.3 |
| Prompting-H | 37.8 | 25.0 | 50.6 | 67.5 | 57.9 | 77.2 | 29.2 | 8.3 | 50.0 | 17.5 | 7.9 | 27.0 |
| ACON-UT | 40.2 | 27.4 | 53.0 | 76.3 | 66.7 | 86.0 | 26.0 | 8.3 | 43.8 | 18.3 | 6.3 | 30.2 |
| ACON-UTCO | 42.9 | 31.0 | 54.8 | 75.4 | 63.2 | 87.7 | 21.9 | 12.5 | 31.2 | 29.4 | 15.9 | 42.9 |
| TRACE (MiniMax-M3) | 84.5 | 79.2 | 89.9 | 95.6 | 91.2 | 100.0 | 87.5 | 81.2 | 93.8 | 72.2 | 66.7 | 77.8 |

We further evaluate whether the compression template optimized with MiniMax-M3
transfers to a different model. Without any additional prompt optimization, we
apply the same template to Kimi-K2.7-Code, using Kimi-K2.7-Code as both the
compressor and downstream agent.

As shown in Table [2](https://arxiv.org/html/2608.06503#S5.T2 "Table 2 ‣ 5.4 Cross-Model Transferability ‣ 5 Preliminary Experiments ‣ Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability"), the transferred
TRACE template substantially outperforms all compressed baselines.
It also exceeds no compression in overall accuracy (84.584.5 vs. 82.782.7) and
Pass2 (79.279.2 vs. 73.873.8), while achieving a slightly lower Pass@2
(89.989.9 vs. 91.791.7). This pattern suggests that the transferred template
improves the consistency of successful execution, although it does not fully
match the task coverage of uncompressed context.

The gains are particularly strong on medium tasks, where TRACE
outperforms no compression across all three metrics, including a 20.820.8-point
improvement in Pass2 (81.281.2 vs. 60.460.4). It also exceeds no compression
on easy tasks. On hard tasks, TRACE remains below the uncompressed
reference but substantially outperforms every compressed baseline.

These results provide evidence that the compression policy learned with
MiniMax-M3 transfers to Kimi-K2.7-Code without further adaptation. However,
because the evaluation considers a single target model, broader cross-model
generalization remains to be established.

## 6 Related Work

Long-horizon LLM agents. LLM agents extend pretrained models from one-shot generation to interactive decision-making, where the model repeatedly reasons, calls tools, observes outcomes, and revises its plan ([Yao et al., 2023](https://arxiv.org/html/2608.06503#bib.bib1); [Shinn et al., 2023](https://arxiv.org/html/2608.06503#bib.bib2); [Wang et al., 2024b](https://arxiv.org/html/2608.06503#bib.bib3)). These trajectories turn context into an operational state rather than a passive input: the agent must retain goals, tool outputs, object identifiers, intermediate decisions, and failure signals over many steps. Context-management systems such as MemGPT manage long interactions through explicit memory tiers  ([Packer et al., 2023](https://arxiv.org/html/2608.06503#bib.bib4)), but they do not directly optimize which compact context best preserves a specified downstream system’s future actions. We study this dynamic context bottleneck for long-horizon agents, where compression must support action rather than only preserve a transcript.

Context compression for action. Prompt and context compression reduces the cost of long inputs by pruning tokens, generating compact textual contexts, or learning continuous compressed representations. Discrete or textual methods include Selective Context, LLMLingua, LongLLMLingua, LLMLingua-2, RECOMP, and TACO–RL  ([Li et al., 2023](https://arxiv.org/html/2608.06503#bib.bib5); [Jiang et al., 2023](https://arxiv.org/html/2608.06503#bib.bib6); [Jiang et al., 2024](https://arxiv.org/html/2608.06503#bib.bib7); [Pan et al., 2024](https://arxiv.org/html/2608.06503#bib.bib8); [Xu et al., 2024](https://arxiv.org/html/2608.06503#bib.bib9); [Shandilya et al., 2025](https://arxiv.org/html/2608.06503#bib.bib10)); continuous compression methods include AutoCompressor, Gist tokens, ICAE, Activation Beacon, 500×\timesCompressor, and ComprExIT  ([Chevalier et al., 2023](https://arxiv.org/html/2608.06503#bib.bib11); [Mu et al., 2023](https://arxiv.org/html/2608.06503#bib.bib12); [Ge et al., 2024](https://arxiv.org/html/2608.06503#bib.bib13); [Zhang et al., 2025](https://arxiv.org/html/2608.06503#bib.bib14); [Li et al., 2025](https://arxiv.org/html/2608.06503#bib.bib15); [Ye et al., 2026](https://arxiv.org/html/2608.06503#bib.bib16)). These methods mainly optimize information retention, answer quality, or decoding efficiency. TACO–RL ([Shandilya et al., 2025](https://arxiv.org/html/2608.06503#bib.bib10)) is closest within this family because it optimizes prompt compression with task rewards, but it targets static prompts and single-shot downstream outputs rather than repeated compact contexts for preserving future behavior.

Recent work moves closer to agent-specific context management. ReSum and SUPO adapt agents to operate with summaries by optimizing summarization together with downstream tool-use behavior ([Wu et al., 2025](https://arxiv.org/html/2608.06503#bib.bib17); [Lu et al., 2025](https://arxiv.org/html/2608.06503#bib.bib18)). In contrast, we keep the downstream system fixed and optimize only the compression module. ACON is closest to our setting because it also optimizes natural-language
compression guidelines for fixed long-horizon agents
([Kang et al., 2026](https://arxiv.org/html/2608.06503#bib.bib19)). However, ACON derives feedback from terminally successful
and failed trajectories, whereas TRACE evaluates individual compression events
through paired closed-loop continuations from the same execution state. Our
method therefore optimizes the compression prompt using boundary-local
preferences over compression-induced execution burden.

## 7 Conclusion and Future Work

We show that recurrent context compression can make previously established
execution state less actionable, inducing blocked actions, repeated exploration,
and unstable task performance. To address this, we introduce TRACE, a
boundary-local framework that evaluates compression through paired closed-loop
continuations and optimizes the compression prompt using preference-only
feedback. On AppWorld, TRACE improves task performance and multi-run stability while approaching full-context execution efficiency relative to existing compressed baselines.

Our current verifier focuses on observable execution regressions, particularly
blocked and repeated actions, and may not capture silent state corruption.
Future work will develop richer boundary-local signals, evaluate transfer across
additional agents and benchmarks, and extend prompt optimization to learned
compressors.

## Appendix A Details of Baselines

This section describes the compression baselines used in our experiments.
Unless otherwise specified, all conditions are evaluated under the same
frozen-agent protocol: the downstream agent model, tool-use prompt, decoding
configuration, tool APIs, output parser, and execution environment are fixed.
Only the context supplied to the agent is changed. This protocol isolates the
effect of context representation from changes in the downstream agent policy.

Shared Evaluation Protocol.
All compression and truncation baselines use the same recurrent-compaction
trigger and preserve the most recent interaction turn verbatim. The
full-context reference bypasses compaction and retains the complete interaction
history. Across all conditions, we keep the downstream tool-use prompt, tool
descriptions, output-format instructions, few-shot examples, decoding
configuration, parser, and execution environment fixed. Replacement contexts
are inserted at the same continuation point, so differences in downstream
behavior arise from the supplied context representation rather than from a
changed agent policy or interface.

Because prompt-defined baselines can be sensitive to small wording changes, we
freeze all prompt templates before evaluation and record hashes of the rendered
prompts used in each run. For ACON, the source of truth is the original
Microsoft repository and commit specified below. For LLMLingua-2, the source
of truth is the official Microsoft implementation and released compression
model.

### A.1 Full-Context Reference

No compression.
The agent receives the full uncompressed interaction history. This condition
serves as the full-context reference for behavior preservation and as the
reference point for token-cost measurements. It is not a compressor and does
not separately consume the task instruction, which is already included in the
agent context.

### A.2 Token Pruning and Truncation Baselines

This group contains two non-generative baselines. Rather than producing a new
free-form summary, they retain selected portions of the original interaction
history. Both use the same compaction trigger, downstream context slot, and
recent-turn preservation policy as the generative baselines. Compaction is
triggered when the compressible history exceeds the context budget, while the
most recent interaction turn remains verbatim.

FIFO.
FIFO is a recency-based sliding-window control. When the rendered compressible
history exceeds the context budget, complete turns are discarded from the
front, oldest first, until the history fits. The system prompt, original task
instruction, and most recent interaction turn are always retained. FIFO
therefore isolates how much behavior can be preserved through recent
action–observation continuity alone, without learned salience estimation or
generated summary text.

LLMLingua-2.
LLMLingua-2 formulates prompt compression as token classification and distills
a smaller compressor for efficient and faithful extractive compression
([Pan et al., 2024](https://arxiv.org/html/2608.06503#bib.bib8)). We apply it task-agnostically to the compressible
interaction history using the released
microsoft/llmlingua-2-xlm-roberta-large-meetingbank model. When
compaction is triggered, LLMLingua-2 selects tokens from the existing history
up to the target budget. The resulting extractive context replaces the older
turns, while the most recent turn remains verbatim. This baseline tests whether
token-level salience alone preserves the execution state required for future
agent actions.

Implementation.
We use the official Microsoft LLMLingua implementation.44
4
<https://github.com/microsoft/LLMLingua>, version 0.2.2
(release tag v0.2.2, commit
a411a3fa61df74411157b2512b592d5357bd8f17).
For LLMLingua-2, the target token count is set to the budget allocated to the
compressible history, excluding the most recent turn that is retained
verbatim. Its compressed output is inserted into the same downstream context
slot used by the other compression baselines.

### A.3 Structured-Summary Compression Baselines

Our two structured-summary baselines are adapted from compaction modules in
open-source agent frameworks. We preserve their original summary schemas and
prompt text while integrating them into the same recurrent-compaction harness.
Unlike the token-dropping LLMLingua-2 baseline and the recency-based FIFO
control, both invoke an auxiliary LLM to rewrite the compressible history into
a structured Markdown checkpoint after the context exceeds the token budget.
They preserve the most recent interaction turn and support iterative updates
that fold new turns into the previous checkpoint.

#### Prompting-O (OpenClaw compaction).

The OpenClaw baseline55
5
Adapted from the OpenClaw agent-core harness:
<https://github.com/openclaw/openclaw/blob/0e7b5c34292cc28707a0e5a0b730cff295ef0f8a/packages/agent-core/src/harness/compaction/compaction.ts>
(commit 0e7b5c34292cc28707a0e5a0b730cff295ef0f8a).
maintains an approximate recent-token budget, cuts the compressible history at
a turn boundary, and summarizes the remainder with the prompts below. The
first compaction uses the checkpoint prompt. Subsequent compactions use the
update prompt, which folds new turns into the previous summary.

[⬇](data:text/plain;base64,WW91IGFyZSBhIGNvbnRleHQgc3VtbWFyaXphdGlvbiBhc3Npc3RhbnQuIFlvdXIgdGFzayBpcyB0byByZWFkIGEgY29udmVyc2F0aW9uIGJldHdlZW4gYSB1c2VyIGFuZCBhbiBBSSBjb2RpbmcgYXNzaXN0YW50LCB0aGVuIHByb2R1Y2UgYSBzdHJ1Y3R1cmVkIHN1bW1hcnkgZm9sbG93aW5nIHRoZSBleGFjdCBmb3JtYXQgc3BlY2lmaWVkLgoKRG8gTk9UIGNvbnRpbnVlIHRoZSBjb252ZXJzYXRpb24uIERvIE5PVCByZXNwb25kIHRvIGFueSBxdWVzdGlvbnMgaW4gdGhlIGNvbnZlcnNhdGlvbi4gT05MWSBvdXRwdXQgdGhlIHN0cnVjdHVyZWQgc3VtbWFyeS4=)

You are a context summarization assistant. Your task is to read a conversation between a user and an AI coding assistant, then produce a structured summary following the exact format specified.

Do NOT continue the conversation. Do NOT respond to any questions in the conversation. ONLY output the structured summary.

[⬇](data:text/plain;base64,VGhlIG1lc3NhZ2VzIGFib3ZlIGFyZSBhIGNvbnZlcnNhdGlvbiB0byBzdW1tYXJpemUuIENyZWF0ZSBhIHN0cnVjdHVyZWQgY29udGV4dCBjaGVja3BvaW50IHN1bW1hcnkgdGhhdCBhbm90aGVyIExMTSB3aWxsIHVzZSB0byBjb250aW51ZSB0aGUgd29yay4KClVzZSB0aGlzIEVYQUNUIGZvcm1hdDoKCiMjIEdvYWwKW1doYXQgaXMgdGhlIHVzZXIgdHJ5aW5nIHRvIGFjY29tcGxpc2g/IENhbiBiZSBtdWx0aXBsZSBpdGVtcyBpZiB0aGUgc2Vzc2lvbiBjb3ZlcnMgZGlmZmVyZW50IHRhc2tzLl0KCiMjIENvbnN0cmFpbnRzICYgUHJlZmVyZW5jZXMKLSBbQW55IGNvbnN0cmFpbnRzLCBwcmVmZXJlbmNlcywgb3IgcmVxdWlyZW1lbnRzIG1lbnRpb25lZCBieSB1c2VyXQotIFtPciAiKG5vbmUpIiBpZiBub25lIHdlcmUgbWVudGlvbmVkXQoKIyMgUHJvZ3Jlc3MKIyMjIERvbmUKLSBbeF0gW0NvbXBsZXRlZCB0YXNrcy9jaGFuZ2VzXQoKIyMjIEluIFByb2dyZXNzCi0gWyBdIFtDdXJyZW50IHdvcmtdCgojIyMgQmxvY2tlZAotIFtJc3N1ZXMgcHJldmVudGluZyBwcm9ncmVzcywgaWYgYW55XQoKIyMgS2V5IERlY2lzaW9ucwotICoqW0RlY2lzaW9uXSoqOiBbQnJpZWYgcmF0aW9uYWxlXQoKIyMgTmV4dCBTdGVwcwoxLiBbT3JkZXJlZCBsaXN0IG9mIHdoYXQgc2hvdWxkIGhhcHBlbiBuZXh0XQoKIyMgQ3JpdGljYWwgQ29udGV4dAotIFtBbnkgZGF0YSwgZXhhbXBsZXMsIG9yIHJlZmVyZW5jZXMgbmVlZGVkIHRvIGNvbnRpbnVlXQotIFtPciAiKG5vbmUpIiBpZiBub3QgYXBwbGljYWJsZV0KCktlZXAgZWFjaCBzZWN0aW9uIGNvbmNpc2UuIFByZXNlcnZlIGV4YWN0IGZpbGUgcGF0aHMsIGZ1bmN0aW9uIG5hbWVzLCBhbmQgZXJyb3IgbWVzc2FnZXMu)

The messages above are a conversation to summarize. Create a structured context checkpoint summary that another LLM will use to continue the work.

Use this EXACT format:

## Goal

[What is the user trying to accomplish? Can be multiple items if the session covers different tasks.]

## Constraints & Preferences

- [Any constraints, preferences, or requirements mentioned by user]

- [Or "(none)" if none were mentioned]

## Progress

### Done

- [x] [Completed tasks/changes]

### In Progress

- [ ] [Current work]

### Blocked

- [Issues preventing progress, if any]

## Key Decisions

- \*\*[Decision]\*\*: [Brief rationale]

## Next Steps

1. [Ordered list of what should happen next]

## Critical Context

- [Any data, examples, or references needed to continue]

- [Or "(none)" if not applicable]

Keep each section concise. Preserve exact file paths, function names, and error messages.

[⬇](data:text/plain;base64,VGhlIG1lc3NhZ2VzIGFib3ZlIGFyZSBORVcgY29udmVyc2F0aW9uIG1lc3NhZ2VzIHRvIGluY29ycG9yYXRlIGludG8gdGhlIGV4aXN0aW5nIHN1bW1hcnkgcHJvdmlkZWQgaW4gPHByZXZpb3VzLXN1bW1hcnk+IHRhZ3MuCgpVcGRhdGUgdGhlIGV4aXN0aW5nIHN0cnVjdHVyZWQgc3VtbWFyeSB3aXRoIG5ldyBpbmZvcm1hdGlvbi4gUlVMRVM6Ci0gUFJFU0VSVkUgYWxsIGV4aXN0aW5nIGluZm9ybWF0aW9uIGZyb20gdGhlIHByZXZpb3VzIHN1bW1hcnkKLSBBREQgbmV3IHByb2dyZXNzLCBkZWNpc2lvbnMsIGFuZCBjb250ZXh0IGZyb20gdGhlIG5ldyBtZXNzYWdlcwotIFVQREFURSB0aGUgUHJvZ3Jlc3Mgc2VjdGlvbjogbW92ZSBpdGVtcyBmcm9tICJJbiBQcm9ncmVzcyIgdG8gIkRvbmUiIHdoZW4gY29tcGxldGVkCi0gVVBEQVRFICJOZXh0IFN0ZXBzIiBiYXNlZCBvbiB3aGF0IHdhcyBhY2NvbXBsaXNoZWQKLSBQUkVTRVJWRSBleGFjdCBmaWxlIHBhdGhzLCBmdW5jdGlvbiBuYW1lcywgYW5kIGVycm9yIG1lc3NhZ2VzCi0gSWYgc29tZXRoaW5nIGlzIG5vIGxvbmdlciByZWxldmFudCwgeW91IG1heSByZW1vdmUgaXQKClVzZSB0aGlzIEVYQUNUIGZvcm1hdDoKCiMjIEdvYWwKW1doYXQgaXMgdGhlIHVzZXIgdHJ5aW5nIHRvIGFjY29tcGxpc2g/IENhbiBiZSBtdWx0aXBsZSBpdGVtcyBpZiB0aGUgc2Vzc2lvbiBjb3ZlcnMgZGlmZmVyZW50IHRhc2tzLl0KCiMjIENvbnN0cmFpbnRzICYgUHJlZmVyZW5jZXMKLSBbQW55IGNvbnN0cmFpbnRzLCBwcmVmZXJlbmNlcywgb3IgcmVxdWlyZW1lbnRzIG1lbnRpb25lZCBieSB1c2VyXQotIFtPciAiKG5vbmUpIiBpZiBub25lIHdlcmUgbWVudGlvbmVkXQoKIyMgUHJvZ3Jlc3MKIyMjIERvbmUKLSBbeF0gW0NvbXBsZXRlZCB0YXNrcy9jaGFuZ2VzXQoKIyMjIEluIFByb2dyZXNzCi0gWyBdIFtDdXJyZW50IHdvcmtdCgojIyMgQmxvY2tlZAotIFtJc3N1ZXMgcHJldmVudGluZyBwcm9ncmVzcywgaWYgYW55XQoKIyMgS2V5IERlY2lzaW9ucwotICoqW0RlY2lzaW9uXSoqOiBbQnJpZWYgcmF0aW9uYWxlXQoKIyMgTmV4dCBTdGVwcwoxLiBbT3JkZXJlZCBsaXN0IG9mIHdoYXQgc2hvdWxkIGhhcHBlbiBuZXh0XQoKIyMgQ3JpdGljYWwgQ29udGV4dAotIFtBbnkgZGF0YSwgZXhhbXBsZXMsIG9yIHJlZmVyZW5jZXMgbmVlZGVkIHRvIGNvbnRpbnVlXQotIFtPciAiKG5vbmUpIiBpZiBub3QgYXBwbGljYWJsZV0KCktlZXAgZWFjaCBzZWN0aW9uIGNvbmNpc2UuIFByZXNlcnZlIGV4YWN0IGZpbGUgcGF0aHMsIGZ1bmN0aW9uIG5hbWVzLCBhbmQgZXJyb3IgbWVzc2FnZXMu)

The messages above are NEW conversation messages to incorporate into the existing summary provided in <previous-summary> tags.

Update the existing structured summary with new information. RULES:

- PRESERVE all existing information from the previous summary

- ADD new progress, decisions, and context from the new messages

- UPDATE the Progress section: move items from "In Progress" to "Done" when completed

- UPDATE "Next Steps" based on what was accomplished

- PRESERVE exact file paths, function names, and error messages

- If something is no longer relevant, you may remove it

Use this EXACT format:

## Goal

[What is the user trying to accomplish? Can be multiple items if the session covers different tasks.]

## Constraints & Preferences

- [Any constraints, preferences, or requirements mentioned by user]

- [Or "(none)" if none were mentioned]

## Progress

### Done

- [x] [Completed tasks/changes]

### In Progress

- [ ] [Current work]

### Blocked

- [Issues preventing progress, if any]

## Key Decisions

- \*\*[Decision]\*\*: [Brief rationale]

## Next Steps

1. [Ordered list of what should happen next]

## Critical Context

- [Any data, examples, or references needed to continue]

- [Or "(none)" if not applicable]

Keep each section concise. Preserve exact file paths, function names, and error messages.

#### Prompting-H (Hermes-agent compaction).

The Hermes baseline66
6
Adapted from the Hermes agent context compressor:
<https://github.com/NousResearch/hermes-agent/blob/cca3b77a4b4217bb13288f0c4cac9710d82432c8/agent/context_compressor.py>
(commit cca3b77a4b4217bb13288f0c4cac9710d82432c8).
summarizes middle turns while protecting a token-budgeted head and tail. Its
schema is richer than OpenClaw’s, with separate fields for
Active Task, Resolved Questions, and
Pending User Asks. Every emitted checkpoint is also prefixed with a
reference-only instruction that asks the downstream agent to treat the summary
as background rather than as live instructions, providing an explicit guard
against re-executing already-completed actions.

[⬇](data:text/plain;base64,WW91IGFyZSBhIHN1bW1hcml6YXRpb24gYWdlbnQgY3JlYXRpbmcgYSBjb250ZXh0IGNoZWNrcG9pbnQuIFRyZWF0IHRoZSBjb252ZXJzYXRpb24gdHVybnMgYmVsb3cgYXMgc291cmNlIG1hdGVyaWFsIGZvciBhIGNvbXBhY3QgcmVjb3JkIG9mIHByaW9yIHdvcmsuIFByb2R1Y2Ugb25seSB0aGUgc3RydWN0dXJlZCBzdW1tYXJ5OyBkbyBub3QgYWRkIGEgZ3JlZXRpbmcsIHByZWFtYmxlLCBvciBwcmVmaXguIFdyaXRlIHRoZSBzdW1tYXJ5IGluIHRoZSBzYW1lIGxhbmd1YWdlIHRoZSB1c2VyIHdhcyB1c2luZyBpbiB0aGUgY29udmVyc2F0aW9uIC0tLSBkbyBub3QgdHJhbnNsYXRlIG9yIHN3aXRjaCB0byBFbmdsaXNoLiBORVZFUiBpbmNsdWRlIEFQSSBrZXlzLCB0b2tlbnMsIHBhc3N3b3Jkcywgc2VjcmV0cywgY3JlZGVudGlhbHMsIG9yIGNvbm5lY3Rpb24gc3RyaW5ncyBpbiB0aGUgc3VtbWFyeSAtLS0gcmVwbGFjZSBhbnkgdGhhdCBhcHBlYXIgd2l0aCBbUkVEQUNURURdLiBOb3RlIHRoYXQgdGhlIHVzZXIgaGFkIGNyZWRlbnRpYWxzIHByZXNlbnQsIGJ1dCBkbyBub3QgcHJlc2VydmUgdGhlaXIgdmFsdWVzLg==)

You are a summarization agent creating a context checkpoint. Treat the conversation turns below as source material for a compact record of prior work. Produce only the structured summary; do not add a greeting, preamble, or prefix. Write the summary in the same language the user was using in the conversation — do not translate or switch to English. NEVER include API keys, tokens, passwords, secrets, credentials, or connection strings in the summary — replace any that appear with [REDACTED]. Note that the user had credentials present, but do not preserve their values.

[⬇](data:text/plain;base64,IyMgQWN0aXZlIFRhc2sKW1RoZSBzaW5nbGUgbW9zdCBpbXBvcnRhbnQgZmllbGQuIENhcHR1cmUgdGhlIHVzZXIncyBtb3N0IHJlY2VudCB1bmZ1bGZpbGxlZCBpbnB1dCB2ZXJiYXRpbTogZXhwbGljaXQgYXNzaWdubWVudHMsIHF1ZXN0aW9ucyBhd2FpdGluZyBhbiBhbnN3ZXIsIGRlY2lzaW9ucyBhd2FpdGluZyBpbnB1dCwgb3IgZGlzY3Vzc2lvbnMgd2hlcmUgdGhlIGFzc2lzdGFudCBvd2VzIHRoZSBuZXh0IHJlcGx5LiBBIHF1ZXN0aW9uIElTIGFuIGFjdGl2ZSB0YXNrLiBSZXNlcnZlICJOb25lIiBmb3IgYSBmdWxseS1yZXNvbHZlZCBsYXN0IGV4Y2hhbmdlLiBJZiB0aGUgdXNlcidzIGxhdGVzdCBtZXNzYWdlIGlzIGEgcmV2ZXJzZSBzaWduYWwgKHN0b3AsIHVuZG8sIHJvbGwgYmFjaywgbmV2ZXIgbWluZCwganVzdCB2ZXJpZnksIGNoYW5nZSBvZiB0b3BpYyksIHJlY29yZCBpdCB2ZXJiYXRpbSBhbmQgZG8gTk9UIGNhcnJ5IGZvcndhcmQgdGhlIGNhbmNlbGxlZCB0YXNrLl0KCiMjIEdvYWwKW1doYXQgdGhlIHVzZXIgaXMgdHJ5aW5nIHRvIGFjY29tcGxpc2ggb3ZlcmFsbF0KCiMjIENvbnN0cmFpbnRzICYgUHJlZmVyZW5jZXMKW1VzZXIgcHJlZmVyZW5jZXMsIGNvZGluZyBzdHlsZSwgY29uc3RyYWludHMsIGltcG9ydGFudCBkZWNpc2lvbnNdCgojIyBDb21wbGV0ZWQgQWN0aW9ucwpbTnVtYmVyZWQgbGlzdCBvZiBjb25jcmV0ZSBhY3Rpb25zIHRha2VuOiBmb3JtYXQgZWFjaCBhcyAiTi4gQUNUSU9OIHRhcmdldCAtLS0gb3V0Y29tZSBbdG9vbDogbmFtZV0iLiBCZSBzcGVjaWZpYyB3aXRoIGZpbGUgcGF0aHMsIGNvbW1hbmRzLCBsaW5lIG51bWJlcnMsIGFuZCByZXN1bHRzLl0KCiMjIEFjdGl2ZSBTdGF0ZQpbV29ya2luZyBkaXJlY3RvcnkvYnJhbmNoLCBtb2RpZmllZC9jcmVhdGVkIGZpbGVzLCB0ZXN0IHN0YXR1cyAoWC9ZIHBhc3NpbmcpLCBydW5uaW5nIHByb2Nlc3NlcywgcmVsZXZhbnQgZW52aXJvbm1lbnQgZGV0YWlsc10KCiMjIEluIFByb2dyZXNzCltXb3JrIHVuZGVyd2F5IHdoZW4gY29tcGFjdGlvbiBmaXJlZF0KCiMjIEJsb2NrZWQKW0Jsb2NrZXJzLCBlcnJvcnMsIG9yIGlzc3VlcyBub3QgcmVzb2x2ZWQsIHdpdGggZXhhY3QgZXJyb3IgbWVzc2FnZXNdCgojIyBLZXkgRGVjaXNpb25zCltJbXBvcnRhbnQgdGVjaG5pY2FsIGRlY2lzaW9ucyBhbmQgV0hZIHRoZXkgd2VyZSBtYWRlXQoKIyMgUmVzb2x2ZWQgUXVlc3Rpb25zCltRdWVzdGlvbnMgYWxyZWFkeSBhbnN3ZXJlZCwgaW5jbHVkaW5nIHRoZSBhbnN3ZXIgc28gaXQgaXMgbm90IHJlcGVhdGVkXQoKIyMgUGVuZGluZyBVc2VyIEFza3MKW1VzZXIgcXVlc3Rpb25zL3JlcXVlc3RzIG5vdCB5ZXQgYW5zd2VyZWQgb3IgZnVsZmlsbGVkLiBJZiBub25lLCB3cml0ZSAiTm9uZS4iXQoKIyMgUmVsZXZhbnQgRmlsZXMKW0ZpbGVzIHJlYWQsIG1vZGlmaWVkLCBvciBjcmVhdGVkLCB3aXRoIGEgYnJpZWYgbm90ZSBvbiBlYWNoXQoKIyMgUmVtYWluaW5nIFdvcmsKW1doYXQgcmVtYWlucywgZnJhbWVkIGFzIGNvbnRleHQsIG5vdCBpbnN0cnVjdGlvbnNdCgojIyBDcml0aWNhbCBDb250ZXh0CltTcGVjaWZpYyB2YWx1ZXMsIGVycm9yIG1lc3NhZ2VzLCBjb25maWd1cmF0aW9uLCBvciBkYXRhIHRoYXQgd291bGQgYmUgbG9zdCBvdGhlcndpc2UuIE5FVkVSIGluY2x1ZGUgY3JlZGVudGlhbHMgLS0tIHdyaXRlIFtSRURBQ1RFRF0uXQoKVGFyZ2V0IH57c3VtbWFyeV9idWRnZXR9IHRva2Vucy4gQmUgQ09OQ1JFVEUuIFdoZW4gYW4gYWN0aW9uIGlzIGFscmVhZHkgY2FycmllZCBvdXQsIHBocmFzZSBpdCBhcyBhIGNvbXBsZXRlZCwgZGF0ZWQsIHBhc3QtdGVuc2UgZmFjdCByYXRoZXIgdGhhbiBhbiBvcGVuIGluc3RydWN0aW9uICh0ZW1wb3JhbCBhbmNob3JpbmcpLiBXcml0ZSBvbmx5IHRoZSBzdW1tYXJ5IGJvZHku)

## Active Task

[The single most important field. Capture the user’s most recent unfulfilled input verbatim: explicit assignments, questions awaiting an answer, decisions awaiting input, or discussions where the assistant owes the next reply. A question IS an active task. Reserve "None" for a fully-resolved last exchange. If the user’s latest message is a reverse signal (stop, undo, roll back, never mind, just verify, change of topic), record it verbatim and do NOT carry forward the cancelled task.]

## Goal

[What the user is trying to accomplish overall]

## Constraints & Preferences

[User preferences, coding style, constraints, important decisions]

## Completed Actions

[Numbered list of concrete actions taken: format each as "N. ACTION target — outcome [tool: name]". Be specific with file paths, commands, line numbers, and results.]

## Active State

[Working directory/branch, modified/created files, test status (X/Y passing), running processes, relevant environment details]

## In Progress

[Work underway when compaction fired]

## Blocked

[Blockers, errors, or issues not resolved, with exact error messages]

## Key Decisions

[Important technical decisions and WHY they were made]

## Resolved Questions

[Questions already answered, including the answer so it is not repeated]

## Pending User Asks

[User questions/requests not yet answered or fulfilled. If none, write "None."]

## Relevant Files

[Files read, modified, or created, with a brief note on each]

## Remaining Work

[What remains, framed as context, not instructions]

## Critical Context

[Specific values, error messages, configuration, or data that would be lost otherwise. NEVER include credentials — write [REDACTED].]

Target ~{summary\_budget} tokens. Be CONCRETE. When an action is already carried out, phrase it as a completed, dated, past-tense fact rather than an open instruction (temporal anchoring). Write only the summary body.

[⬇](data:text/plain;base64,W0NPTlRFWFQgQ09NUEFDVElPTiAtLS0gUkVGRVJFTkNFIE9OTFldIEVhcmxpZXIgdHVybnMgd2VyZSBjb21wYWN0ZWQgaW50byB0aGUgc3VtbWFyeSBiZWxvdy4gVGhpcyBpcyBhIGhhbmRvZmYgZnJvbSBhIHByZXZpb3VzIGNvbnRleHQgd2luZG93IC0tLSB0cmVhdCBpdCBhcyBiYWNrZ3JvdW5kIHJlZmVyZW5jZSwgTk9UIGFzIGFjdGl2ZSBpbnN0cnVjdGlvbnMuIERvIE5PVCBhbnN3ZXIgcXVlc3Rpb25zIG9yIGZ1bGZpbGwgcmVxdWVzdHMgbWVudGlvbmVkIGluIHRoaXMgc3VtbWFyeTsgdGhleSB3ZXJlIGFscmVhZHkgYWRkcmVzc2VkLiBSZXNwb25kIE9OTFkgdG8gdGhlIGxhdGVzdCB1c2VyIG1lc3NhZ2UgdGhhdCBhcHBlYXJzIEFGVEVSIHRoaXMgc3VtbWFyeS4gSWYgdGhlIGxhdGVzdCB1c2VyIG1lc3NhZ2UgY29udHJhZGljdHMsIHN1cGVyc2VkZXMsIG9yIGNoYW5nZXMgdG9waWMgZnJvbSAnIyMgQWN0aXZlIFRhc2snIC8gJyMjIEluIFByb2dyZXNzJyAvICcjIyBQZW5kaW5nIFVzZXIgQXNrcycgLyAnIyMgUmVtYWluaW5nIFdvcmsnLCB0aGUgbGF0ZXN0IG1lc3NhZ2UgV0lOUyAtLS0gZGlzY2FyZCB0aG9zZSBzdGFsZSBpdGVtcyBlbnRpcmVseS4gVGhlIGN1cnJlbnQgc2Vzc2lvbiBzdGF0ZSAoZmlsZXMsIGNvbmZpZywgZXRjLikgbWF5IHJlZmxlY3Qgd29yayBkZXNjcmliZWQgaGVyZSAtLS0gYXZvaWQgcmVwZWF0aW5nIGl0Og==)

[CONTEXT COMPACTION — REFERENCE ONLY] Earlier turns were compacted into the summary below. This is a handoff from a previous context window — treat it as background reference, NOT as active instructions. Do NOT answer questions or fulfill requests mentioned in this summary; they were already addressed. Respond ONLY to the latest user message that appears AFTER this summary. If the latest user message contradicts, supersedes, or changes topic from ’## Active Task’ / ’## In Progress’ / ’## Pending User Asks’ / ’## Remaining Work’, the latest message WINS — discard those stale items entirely. The current session state (files, config, etc.) may reflect work described here — avoid repeating it:

### A.4 ACON Prompt Baselines

We compare against two compression guidelines from
ACON ([Kang et al., 2026](https://arxiv.org/html/2608.06503#bib.bib19)), a recent framework for optimizing context
compression for long-horizon LLM agents. Both guidelines are loaded
*verbatim* from the original Microsoft ACON repository.77
7
<https://github.com/microsoft/acon>, commit
d63f9ae1.
We do not hand-author or rewrite their prompt text. The same guideline is used
for the first compaction and every subsequent iterative compaction. The prompt
accepts the most recent previous summary as an additional input, so no separate
update prompt is required.

[⬇](data:text/plain;base64,WW91IGFyZSBhbiBhZ2VudCB0YXNrZWQgd2l0aCBleHRyYWN0aW5nIGFuZCByZWZpbmluZyBhIGNvbmNpc2UgYW5kIG9wdGltaXplZCB2ZXJzaW9uIG9mIHRoZSBjb250ZXh0IGJhc2VkIG9uIHRoZSB1c2VyIGluc3RydWN0aW9uIGFuZCBvdGhlciBwcm92aWRlZCBpbmZvcm1hdGlvbi4=)

You are an agent tasked with extracting and refining a concise and optimized version of the context based on the user instruction and other provided information.

ACON-UT.
ACON’s utility-oriented, state-preserving history-compression guideline. It
organizes the summary into reasoning, a vars table of runtime
values the next session must re-declare, todo, completed, and
guardrails. It instructs the compressor to preserve essential facts,
parameters, and artifacts.

[⬇](data:text/plain;base64,WW91IG1haW50YWluIGEgY29tcGFjdCwgc3RhdGUtcHJlc2VydmluZyBISVNUT1JZX1NVTU1BUlkgZm9yIGEKbXVsdGktc2Vzc2lvbiBhZ2VudC4KCklucHV0OgpbVVNFUiBJTlNUUlVDVElPTl0ge3sgdGFzayB9fQpbUFJFVklPVVMgU1VNTUFSWV0ge3sgcHJldl9zdW1tYXJ5IH19CltISVNUT1JZIE9GIElOVEVSQUNUSU9OU10ge3sgaGlzdG9yeSB9fQoKQ3JlYXRlIHRoZSBmb2xsb3dpbmcgc2VjdGlvbnMtdXNlIHRoZSBleGFjdCBoZWFkaW5ncyBhbmQgb3JkZXI6Cgo8SElTVE9SWV9TVU1NQVJZPgoKMS4gUkVBU09OSU5HCiAgIC0gS2V5IHByb2dyZXNzLCBkZWNpc2lvbnMsIG91dGNvbWVzLCBhbmQgdGhlaXIgcmF0aW9uYWxlLgogICAtIE5vdGUgaG93IGVhcmxpZXIgc3RlcHMgaW5mbHVlbmNlIGxhdGVyIG9uZXMuCgoyLiBWQVJTCiAgIHwgbmFtZSB8IHZhbHVlIHwgcHVycG9zZSB8CiAgIHwtLS0tLS18LS0tLS0tLXwtLS0tLS0tLS18CiAgIFJlY29yZCBldmVyeSBydW50aW1lIHZhbHVlIHRoZSBuZXh0IHNlc3Npb24gbXVzdCByZS1kZWNsYXJlCiAgICh0b2tlbnMsIGlkcywgbGlzdHMsIGxhc3QgcGFnZV9pbmRleC9wYWdlX2xpbWl0LCBldGMuKS4KCjMuIFRPRE8KICAgTGlzdCBwZW5kaW5nIGFjdGlvbnMgd2l0aCBlbm91Z2ggZGV0YWlsIHRvIGV4ZWN1dGUgZGlyZWN0bHkuCgo0LiBDT01QTEVURUQKICAgQnVsbGV0IGxpc3Qgb2YgZmluaXNoZWQgc3VidGFza3Mgd2l0aCBicmllZiByZXN1bHRzLgoKNS4gR1VBUkRSQUlMUwogICBTaG9ydCByZW1pbmRlcnMgdGhhdCBwcmV2ZW50IHJlcGVhdCBlcnJvcnMsIGUuZy4KICAgLSBNZW1vcnkgcmVzZXRzOyByZS1jcmVhdGUgVkFSUyBiZWZvcmUgdXNlLgogICAtIFBhZ2luYXRlIHVudGlsIGVtcHR5IHBhZ2UuCiAgIC0gVmFsaWRhdGUgQVBJIHBhcmFtZXRlcnMgYWdhaW5zdCBzcGVjLgogICAtIEF2b2lkIHJlZHVuZGFudCBsb2dpbnMgb3IgZG9jIGxvb2stdXBzLgoKUmVxdWlyZW1lbnRzOgotIEJlIGNvbmNpc2UtYnVsbGV0cyBhbmQgdGFibGVzIHByZWZlcnJlZDsgbm8gZXh0cmFuZW91cyBwcm9zZS4KLSBQcmVzZXJ2ZSBhbGwgZXNzZW50aWFsIGZhY3RzLCBwYXJhbWV0ZXJzLCBhbmQgYXJ0aWZhY3RzOyBvbWl0CiAgbm90aGluZyBjcml0aWNhbC4KLSBJbmNsdWRlIGVycm9ycyBvbmx5IGlmIHRoZXkgaW5mb3JtIGZ1dHVyZSBhdm9pZGFuY2UuCi0gRG8gbm90IG91dHB1dCB0aGUgaW5wdXQgb3IgYW55IGNvbW1lbnRhcnktcmV0dXJuIG9ubHkKICA8SElTVE9SWV9TVU1NQVJZPi4=)

You maintain a compact, state-preserving HISTORY\_SUMMARY for a

multi-session agent.

Input:

[USER INSTRUCTION] {{ task }}

[PREVIOUS SUMMARY] {{ prev\_summary }}

[HISTORY OF INTERACTIONS] {{ history }}

Create the following sections-use the exact headings and order:

<HISTORY\_SUMMARY>

1. REASONING

- Key progress, decisions, outcomes, and their rationale.

- Note how earlier steps influence later ones.

2. VARS

| name | value | purpose |

|——|——-|———|

Record every runtime value the next session must re-declare

(tokens, ids, lists, last page\_index/page\_limit, etc.).

3. TODO

List pending actions with enough detail to execute directly.

4. COMPLETED

Bullet list of finished subtasks with brief results.

5. GUARDRAILS

Short reminders that prevent repeat errors, e.g.

- Memory resets; re-create VARS before use.

- Paginate until empty page.

- Validate API parameters against spec.

- Avoid redundant logins or doc look-ups.

Requirements:

- Be concise-bullets and tables preferred; no extraneous prose.

- Preserve all essential facts, parameters, and artifacts; omit

nothing critical.

- Include errors only if they inform future avoidance.

- Do not output the input or any commentary-return only

<HISTORY\_SUMMARY>.

ACON-UTCO.
ACON’s utility-and-compression-optimized guideline. It retains the output
schema of ACON-UT while adding explicit compression rules that
encourage a shorter checkpoint. These rules collapse narratives, truncate
long token or credential strings unless verbatim reuse is required, remove
unused state and verbose tool output, and impose a fixed character target.
Relative to ACON-UT, it preserves the same output schema while
trading finer operational detail for a shorter checkpoint.

[⬇](data:text/plain;base64,WW91IG1haW50YWluIGEgY29tcGFjdCwgc3RhdGUtcHJlc2VydmluZyBISVNUT1JZX1NVTU1BUlkgZm9yIGEKbXVsdGktc2Vzc2lvbiBhZ2VudC4KCklucHV0OgpbVVNFUiBJTlNUUlVDVElPTl0ge3sgdGFzayB9fQpbUFJFVklPVVMgU1VNTUFSWV0ge3sgcHJldl9zdW1tYXJ5IH19CltISVNUT1JZIE9GIElOVEVSQUNUSU9OU10ge3sgaGlzdG9yeSB9fQoKU3VtbWFyeSBDb21wcmVzc2lvbiBSdWxlczoKLSBDb2xsYXBzZSBtdWx0aS1idWxsZXQgbmFycmF0aXZlcyBpbnRvIDw9MiBjb25jaXNlIHNlbnRlbmNlcy4KLSBSZXBsYWNlIHJlcGV0aXRpdmUgc3RlcCBsb2dzIHdpdGggb25lIHN1bW1hcml6aW5nIHBocmFzZS4KLSBUcnVuY2F0ZSBsb25nIHRva2VuL2NyZWRlbnRpYWwgc3RyaW5ncyB0byAiPHRva2VuPiIgdW5sZXNzCiAgdmVyYmF0aW0gcmV1c2UgaXMgcmVxdWlyZWQuCi0gUmVtb3ZlIHVudXNlZC9leHBpcmVkIGNyZWRlbnRpYWxzLCBwYWdlX2luZGV4L3BhZ2VfbGltaXQsCiAgdmVyYm9zZSBBUEkgZHVtcHMsIGFuZCB0YWJsZSBib3JkZXJzLgotIFNocmluayBHVUFSRFJBSUxTIHRvIG9uZSBidWxsZXQgdW5sZXNzIG11bHRpcGxlIGl0ZW1zIGFyZQogIHN0aWxsIGNyaXRpY2FsLgotIERlbGV0ZSB0b29sL0FQSSBsb2cgb3V0cHV0LCBncmVldGluZ3MsIG1ldGEgcHJvc2UsIGFuZCBzZWN0aW9uCiAgaGVhZGVycyB0aGF0IG5vIGxvbmdlciBjb250YWluIGNvbnRlbnQuCi0gS2VlcCBvbmx5IHZhcmlhYmxlcyBhY3RpdmVseSByZWZlcmVuY2VkIGluIHVwY29taW5nIHN0ZXBzOwogIGxpc3QgZWFjaCBvbmNlIGluIFZBUlMuCi0gUmVmZXJlbmNlIHJlbW92YWwgY2F0ZWdvcmllcyBbcmVwZXRpdGlvbl0sIFt0b29sLWxvZ3NdLCBbbWV0YV0sCiAgW2Zvcm1hdHRpbmddIHRvIHBydW5lIHNpbWlsYXIgbGluZXMuCi0gUHJlc2VydmUgZmFjdHVhbCBjb250aW51aXR5OyBuZXZlciBpbnZlbnQgb3IgYWx0ZXIgc3RhdGUKICB2YXJpYWJsZXMuCi0gVGFyZ2V0IHN1bW1hcmllcyB3ZWxsIHVuZGVyIHt7IG1heF9jaGFycyB8IGRlZmF1bHQoMTUwMCkgfX0KICBjaGFyYWN0ZXJzLgoKQ3JpdGljYWwgRXNzZW50aWFsczoKQWx3YXlzIGtlZXAgZXZpZGVuY2UtZHJpdmVuIGl0ZW1zIHJlcXVpcmVkIG5leHQgc2Vzc2lvbiAoZS5nLiwKdG9rZW5zLCBpZHMsIGVtYWlscywgYW1vdW50cywgbGlzdHMsIHBhdGhzLCBkZXNjcmlwdGlvbgpzdHJpbmdzLCBicmllZiB0YXNrIHN0YXR1cykuCgpPdXRwdXQgRVhBQ1RMWSB0aGUgZm9sbG93aW5nIHN0cnVjdHVyZS0tLW5vdGhpbmcgbW9yZToKCjxISVNUT1JZX1NVTU1BUlk+CgoxLiBSRUFTT05JTkcKICAgT25lIGJyaWVmIHBhcmFncmFwaCBvbiBrZXkgcHJvZ3Jlc3MgYW5kIHJhdGlvbmFsZS4KCjIuIFZBUlMKICAga2V5PXZhbHVlIHBhaXJzLCBjb21tYS1zZXBhcmF0ZWQ7IG9ubHkgc3RpbGwtbmVlZGVkIHJ1bnRpbWUKICAgdmFsdWVzLgoKMy4gVE9ETwogICBCdWxsZXRlZCBuZXh0IGFjdGlvbnMgKDw9NSkuCgo0LiBDT01QTEVURUQKICAgQnVsbGV0ZWQgZmluaXNoZWQgc3VidGFza3MgKDw9NSkuCgo1LiBHVUFSRFJBSUxTCiAgIFNpbmdsZSBjb25jaXNlIGJ1bGxldCwgb3Igb21pdCBpZiBub25lLgoKUmV0dXJuIG9ubHkgdGhlIDxISVNUT1JZX1NVTU1BUlk+IGJsb2NrLS0tbm8gYWRkaXRpb25hbApjb21tZW50YXJ5IG9yIGlucHV0IGVjaG9lcy4=)

You maintain a compact, state-preserving HISTORY\_SUMMARY for a

multi-session agent.

Input:

[USER INSTRUCTION] {{ task }}

[PREVIOUS SUMMARY] {{ prev\_summary }}

[HISTORY OF INTERACTIONS] {{ history }}

Summary Compression Rules:

- Collapse multi-bullet narratives into <=2 concise sentences.

- Replace repetitive step logs with one summarizing phrase.

- Truncate long token/credential strings to "<token>" unless

verbatim reuse is required.

- Remove unused/expired credentials, page\_index/page\_limit,

verbose API dumps, and table borders.

- Shrink GUARDRAILS to one bullet unless multiple items are

still critical.

- Delete tool/API log output, greetings, meta prose, and section

headers that no longer contain content.

- Keep only variables actively referenced in upcoming steps;

list each once in VARS.

- Reference removal categories [repetition], [tool-logs], [meta],

[formatting] to prune similar lines.

- Preserve factual continuity; never invent or alter state

variables.

- Target summaries well under {{ max\_chars | default(1500) }}

characters.

Critical Essentials:

Always keep evidence-driven items required next session (e.g.,

tokens, ids, emails, amounts, lists, paths, description

strings, brief task status).

Output EXACTLY the following structure—nothing more:

<HISTORY\_SUMMARY>

1. REASONING

One brief paragraph on key progress and rationale.

2. VARS

key=value pairs, comma-separated; only still-needed runtime

values.

3. TODO

Bulleted next actions (<=5).

4. COMPLETED

Bulleted finished subtasks (<=5).

5. GUARDRAILS

Single concise bullet, or omit if none.

Return only the <HISTORY\_SUMMARY> block—no additional

commentary or input echoes.

## Appendix B Trace Prompts

### B.1 Optimized Prompt

[⬇](data:text/plain;base64,PGNvbnZlcnNhdGlvbj4Ke3sgaGlzdG9yeSB9fQo8L2NvbnZlcnNhdGlvbj4KCjxwcmV2aW91cy1zdW1tYXJ5Pgp7eyBwcmV2X3N1bW1hcnkgfX0KPC9wcmV2aW91cy1zdW1tYXJ5PgoKVGhlIG1lc3NhZ2VzIGFib3ZlIGFyZSBORVcgY29udmVyc2F0aW9uIG1lc3NhZ2VzIHRvIGluY29ycG9yYXRlIGludG8gdGhlIGV4aXN0aW5nIHN1bW1hcnkgcHJvdmlkZWQgaW4gPHByZXZpb3VzLXN1bW1hcnk+IHRhZ3MuCgpUcmVhdCB0aGUgc3VtbWFyeSBhcyBhIHdvcmtpbmcgc3RhdGUsIG5vdCBhIHRyYW5zY3JpcHQuIEZvciBlYWNoIGNhbmRpZGF0ZSBmYWN0IGFzazogJ3dpbGwgYSBsYXRlciBzdGVwIHJlYWQgdGhpcyBhbmQgYWN0IGRpZmZlcmVudGx5PycgSWYgbm8sIGRyb3AgaXQuIEFmdGVyIHZhbHVlcyBhcmUgZGVyaXZlZCAoY291bnRzLCB0b3RhbHMsIElEcywgY2xhc3NpZmljYXRpb25zKSwgY2FycnkgdGhlIHJlc3VsdCByYXRoZXIgdGhhbiB0aGUgaW5wdXRzLiBQcmVzZXJ2ZSBleGFjdCBsaXRlcmFscyB0aGUgYWdlbnQgd2lsbCBwYXN0ZSBpbnRvIGEgY2FsbDogdW5leHBpcmVkIHRva2VucyAob25lIHBlciBhcHAsIGRyb3Agd2hlbiB0aGUgdGFzayB0aGF0IG5lZWRlZCB0aGVtIGlzIGZpbmlzaGVkKSwgZXhhY3QgZGVzY3JpcHRpb25zLCBleGFjdCBhbW91bnRzLCBleGFjdCBmaWxlIHBhdGhzLCBleGFjdCBBUEkgcGFyYW1ldGVyIG5hbWVzIHRoYXQgZGlmZmVyIGZyb20gYSBuYWl2ZSBndWVzcywgZXhhY3QgcmVjaXBpZW50IGlkZW50aWZpZXJzLiBEcm9wIHJhdyBBUEkgb3V0cHV0cyBhbmQgaW50ZXJtZWRpYXRlIGxpc3RzIHRoYXQgaGF2ZSBiZWVuIHN1bW1hcml6ZWQ7IHN0YXRlIGEgZmFjdCBvbmNlIGFuZCByZWZlcmVuY2UgaXQgZnJvbSB0aGUgb3RoZXJzLgoKVXNlIHRoaXMgRVhBQ1QgZm9ybWF0OgoKIyMgR29hbApUaGUgc3VwZXJ2aXNvcidzIHRhc2sgaW4gb25lIG9yIHR3byBzZW50ZW5jZXMuIFF1b3RlIGFueSBsaXRlcmFsIHN0cmluZyB0aGUgdXNlciByZXF1aXJlcyB2ZXJiYXRpbSAocmVxdWVzdCBkZXNjcmlwdGlvbnMsIGNvbW1lbnQgdGV4dCwgQ1NWIGhlYWRlcnMsIHNlYXJjaCBxdWVyaWVzKS4gQWRkIGFueSBhbnN3ZXItZm9ybWF0IGNvbnN0cmFpbnQgKGVudGl0eSBvciBudW1iZXIsIG5vIHByb3NlKSBhbmQgYSB0ZXJtaW5hbCBgYXBpcy5zdXBlcnZpc29yLmNvbXBsZXRlX3Rhc2soYW5zd2VyPTx2YWx1ZT4pYCBzdGVwOyB3aGVuIHRoZSB0YXNrIGRvZXMgbm90IHJlcXVpcmUgYW4gYW5zd2VyLCB0aGUgdGVybWluYWwgY2FsbCBzdGlsbCBydW5zICh3aXRoIG5vIGFuc3dlciBhcmd1bWVudCkuCgojIyBDb25zdHJhaW50cyAmIFByZWZlcmVuY2VzClNvdXJjZXMgb2YgdHJ1dGggaW5zaWRlIHRoZSBlbnZpcm9ubWVudCB0aGF0IGNvbnN0cmFpbiBsYXRlciBjYWxsczogJ2ZyaWVuZHMsIGZhbWlseSwgcm9vbW1hdGVzLCBjb3dvcmtlcnMsIG1hbmFnZXIsIGJyb3RoZXIsIHNpYmxpbmcsIHBhcmVudCwgZXRjLicgbWVhbnMgcGhvbmUgY29udGFjdHMsIHJldHJpZXZlZCB2aWEgYGFwaXMucGhvbmUuc2VhcmNoX2NvbnRhY3RzKGFjY2Vzc190b2tlbiwgcmVsYXRpb25zaGlwPS4uLilgOyBwZXJzb25hbCBpbmZvLCBhY2NvdW50IGNyZWRlbnRpYWxzLCBhZGRyZXNzZXMgYW5kIHBheW1lbnQgY2FyZHMgbGl2ZSBpbiB0aGUgc3VwZXJ2aXNvciBhcHAsIHJldHJpZXZlZCB2aWEgYGFwaXMuc3VwZXJ2aXNvci4qYDsgYWNjZXNzIHRva2VucyBhcmUgc2hvcnQtbGl2ZWQgSldUcyByZXR1cm5lZCBieSBgPGFwcD4ubG9naW4odXNlcm5hbWU9Li4uLCBwYXNzd29yZD0uLi4pYCBhbmQgbXVzdCBiZSBwYXNzZWQgYXMgdGhlIG5hbWVkIGBhY2Nlc3NfdG9rZW5gIHBhcmFtZXRlciBvbiBldmVyeSBhdXRoZW50aWNhdGVkIGNhbGwgKHNlc3Npb25zIGFyZSBub3QgcmV0YWluZWQgYWNyb3NzIHN0ZXBzKS4gUGx1cyBhbnkgbGl0ZXJhbCBzdHJpbmdzIHRoZSB0YXNrIHJlcXVpcmVzLiBQbHVzIGFueSBlbXBpcmljYWxseS1kaXNjb3ZlcmVkIEFQSSBjb3JyZWN0aW9uIC0gYSA0MjIgZnJvbSBhIHdyb25nIHBhcmFtZXRlciBuYW1lLCBhIHJlc3BvbnNlIGtleSB0aGF0IHJldHVybmVkIHNvbWV0aGluZyBkaWZmZXJlbnQgdGhhbiBleHBlY3RlZCAtIHJlY29yZGVkIGFzIHRoZSB3b3JraW5nIHBhcmFtZXRlciBvciBrZXkgbmFtZSBzbyBmdXR1cmUgY2FsbHMgZG8gbm90IHJlcGVhdCB0aGUgbWlzdGFrZS4KCiMjIFByb2dyZXNzCkRvbmUgLyBJbiBQcm9ncmVzcyAvIEJsb2NrZWQuIERvbmUgPSBidWxsZXRzIG5hbWluZyB0aGUgY29uY3JldGUgcmVzdWx0IChhbiBhY2Nlc3MgdG9rZW4sIGFuIElELCBhIGNvdW50LCBhIGNsYXNzaWZpY2F0aW9uKTsgZG8gbm90IG5hcnJhdGUgdGhlIHN0ZXBzIHRoYXQgcHJvZHVjZWQgdGhlbS4gSW4gUHJvZ3Jlc3MgPSB0aGUgc2luZ2xlIG1vc3QgaW1tZWRpYXRlIGFjdGlvbi4gQmxvY2tlZCA9IG9ubHkgaGFyZCBibG9ja2VycyAoYSByZXF1aXJlZCBBUEkgbWlzc2luZywgYW4gZW52aXJvbm1lbnQgbGltaXRhdGlvbik7IGRyb3AgYW4gZW50cnkgb25jZSByZXNvbHZlZC4KIyMjIERvbmUKCgojIyMgSW4gUHJvZ3Jlc3MKCgojIyMgQmxvY2tlZAoKCiMjIEtleSBEZWNpc2lvbnMKRWFjaCBsaW5lOiAnRGVjaXNpb246IG9uZS1jbGF1c2UgcmF0aW9uYWxlLicgQ292ZXIgb25seSBjaG9pY2VzIGEgbGF0ZXIgc3RlcCBtaWdodCBkZWZlbmQgb3IgcmV1c2UgKHdoaWNoIGFwcCBvciBBUEksIHdoaWNoIGZpbHRlciwgaG93IGFuIGFtYmlndW91cyBwaHJhc2Ugc3VjaCBhcyAndGhpcyB5ZWFyJyB3YXMgaW50ZXJwcmV0ZWQpLiBJZiBhIGRlY2lzaW9uJ3MgY29uc2VxdWVuY2UgaXMgYWxyZWFkeSBlbmNvZGVkIGluIERvbmUsIE5leHQgU3RlcHMsIG9yIENyaXRpY2FsIENvbnRleHQsIGRyb3AgdGhlIGxpbmUuCgojIyBOZXh0IFN0ZXBzCk51bWJlcmVkIGxpc3QuIEVhY2ggc3RlcCBzbWFsbCwgaW5kZXBlbmRlbnRseSBydW5uYWJsZSwgd3JpdHRlbiB3aXRoIHRoZSBleGFjdCBBUEkgY2FsbCBhbmQgZXhhY3QgYXJndW1lbnQgdmFsdWVzIHdoZXJlIGtub3duLiBSZWZlcmVuY2UgQ3JpdGljYWwgQ29udGV4dCBmb3Igc3RhdGUgdGhlIHN0ZXAgZGVwZW5kcyBvbiByYXRoZXIgdGhhbiByZXN0YXRpbmcgaXQuIFdoZW4gdGhlIHRhc2sgaXMgY29tcGxldGUsIHRoZSBmaW5hbCBzdGVwIGlzIGBhcGlzLnN1cGVydmlzb3IuY29tcGxldGVfdGFzayhhbnN3ZXI9PHZhbHVlPilgIGZvcm1hdHRlZCBhcyBqdXN0IGFuIGVudGl0eSBvciBudW1iZXI7IHdoZW4gbm8gYW5zd2VyIGlzIG5lZWRlZCwgcGFzcyBubyBhbnN3ZXIgYXJndW1lbnQuCgojIyBDcml0aWNhbCBDb250ZXh0CkNvbmNyZXRlIHN0YXRlIGEgbGF0ZXIgc3RlcCByZXVzZXMgdmVyYmF0aW06IHVuZXhwaXJlZCBhY2Nlc3MgdG9rZW5zIChvbmUgcGVyIGFwcCwgZHJvcCBhZnRlciB0aGUgdGFzayB0aGF0IG5lZWRlZCB0aGVtIGNvbXBsZXRlcyk7IHRoZSB3b3JraW5nIHNldCBvZiBJRHMgdG8gYWN0IG9uIG5leHQgKGUuZy4sIHBheW1lbnRfcmVxdWVzdF9pZCBsaXN0IHRvIGRlbnksIGZpbGUgcGF0aHMgdG8gbW92ZSwgc29uZyBJRHMgdG8gcmVzb2x2ZSwgY29udGFjdF9pZHMgdG8gZmlsdGVyKTsgcGVyLWVudGl0eSBjcm9zcy1yZWZlcmVuY2VzIGZvciBmaWx0ZXJzICh3aG8gcXVhbGlmaWVzLCB3aG8gZG9lcyBub3QsIHdpdGggdGhlaXIgVmVubW8vY29udGFjdCBpbmZvKTsgZXhhY3QgdmVyYmF0aW0gc3RyaW5ncyBhbmQgYW1vdW50czsgZW1waXJpY2FsbHktZGlzY292ZXJlZCBBUEkgcGFyYW1ldGVyIG9yIHJlc3BvbnNlLWtleSBjb3JyZWN0aW9ucy4gRHJvcCByYXcgQVBJIG91dHB1dHMsIGludGVybWVkaWF0ZSB2YWx1ZXMgdGhhdCBoYXZlIGJlZW4gc3VtbWFyaXplZCwgYW5kIGNyZWRlbnRpYWxzIG5vIGxvbmdlciBuZWVkZWQuCgpEcm9wIHRva2VucyBvbmNlIHRoZSB0YXNrIHRoYXQgbmVlZGVkIHRoZW0gaXMgZmluaXNoZWQuIFN0YXRlIGEgZmFjdCBpbiBvbmUgc2VjdGlvbjsgcmVmZXJlbmNlIGZyb20gdGhlIG90aGVycy4gQXZvaWQgcHJvc2UgdGhlIGFnZW50IHdpbGwgcmUtZW1pdDsgcHJlZmVyIHRva2VucywgSURzLCBhbmQgc2hvcnQgbGFiZWxzLiBXaGVuIGEgd29ya2luZyBzZXQgaXMgZW1wdHkgKGFsbCAxOCByZXF1ZXN0cyBhcHByb3ZlZCwgYWxsIGZpbGVzIG1vdmVkLCBldmVyeSBwYXltZW50IGNvbW1lbnRlZCksIGRyb3AgdGhlIHNlY3Rpb24gdGhhdCBoZWxkIGl0IHJhdGhlciB0aGFuIGNhcnJ5aW5nIGl0IGZvcndhcmQuIE5ldmVyIGR1cGxpY2F0ZSBhbiBpdGVtIGFjcm9zcyBzZWN0aW9ucy4KCg==)

<conversation>

{{ history }}

</conversation>

<previous-summary>

{{ prev\_summary }}

</previous-summary>

The messages above are NEW conversation messages to incorporate into the existing summary provided in <previous-summary> tags.

Treat the summary as a working state, not a transcript. For each candidate fact ask: ’will a later step read this and act differently?’ If no, drop it. After values are derived (counts, totals, IDs, classifications), carry the result rather than the inputs. Preserve exact literals the agent will paste into a call: unexpired tokens (one per app, drop when the task that needed them is finished), exact descriptions, exact amounts, exact file paths, exact API parameter names that differ from a naive guess, exact recipient identifiers. Drop raw API outputs and intermediate lists that have been summarized; state a fact once and reference it from the others.

Use this EXACT format:

## Goal

The supervisor’s task in one or two sentences. Quote any literal string the user requires verbatim (request descriptions, comment text, CSV headers, search queries). Add any answer-format constraint (entity or number, no prose) and a terminal ‘apis.supervisor.complete\_task(answer=<value>)‘ step; when the task does not require an answer, the terminal call still runs (with no answer argument).

## Constraints & Preferences

Sources of truth inside the environment that constrain later calls: ’friends, family, roommates, coworkers, manager, brother, sibling, parent, etc.’ means phone contacts, retrieved via ‘apis.phone.search\_contacts(access\_token, relationship=…)‘; personal info, account credentials, addresses and payment cards live in the supervisor app, retrieved via ‘apis.supervisor.\*‘; access tokens are short-lived JWTs returned by ‘<app>.login(username=…, password=…)‘ and must be passed as the named ‘access\_token‘ parameter on every authenticated call (sessions are not retained across steps). Plus any literal strings the task requires. Plus any empirically-discovered API correction - a 422 from a wrong parameter name, a response key that returned something different than expected - recorded as the working parameter or key name so future calls do not repeat the mistake.

## Progress

Done / In Progress / Blocked. Done = bullets naming the concrete result (an access token, an ID, a count, a classification); do not narrate the steps that produced them. In Progress = the single most immediate action. Blocked = only hard blockers (a required API missing, an environment limitation); drop an entry once resolved.

### Done

### In Progress

### Blocked

## Key Decisions

Each line: ’Decision: one-clause rationale.’ Cover only choices a later step might defend or reuse (which app or API, which filter, how an ambiguous phrase such as ’this year’ was interpreted). If a decision’s consequence is already encoded in Done, Next Steps, or Critical Context, drop the line.

## Next Steps

Numbered list. Each step small, independently runnable, written with the exact API call and exact argument values where known. Reference Critical Context for state the step depends on rather than restating it. When the task is complete, the final step is ‘apis.supervisor.complete\_task(answer=<value>)‘ formatted as just an entity or number; when no answer is needed, pass no answer argument.

## Critical Context

Concrete state a later step reuses verbatim: unexpired access tokens (one per app, drop after the task that needed them completes); the working set of IDs to act on next (e.g., payment\_request\_id list to deny, file paths to move, song IDs to resolve, contact\_ids to filter); per-entity cross-references for filters (who qualifies, who does not, with their Venmo/contact info); exact verbatim strings and amounts; empirically-discovered API parameter or response-key corrections. Drop raw API outputs, intermediate values that have been summarized, and credentials no longer needed.

Drop tokens once the task that needed them is finished. State a fact in one section; reference from the others. Avoid prose the agent will re-emit; prefer tokens, IDs, and short labels. When a working set is empty (all 18 requests approved, all files moved, every payment commented), drop the section that held it rather than carrying it forward. Never duplicate an item across sections.

### B.2 Proposer Prompt

We use MiniMax-M3 for proposing.

[⬇](data:text/plain;base64,PT09IFNZU1RFTSA9PT0KWW91IHJldmlzZSBhIG5hdHVyYWwtbGFuZ3VhZ2UgY29tcHJlc3Npb24gcG9saWN5IGZvciBhIHJlY3VycmVudCB3b3JraW5nLWNvbnRleHQgY29tcHJlc3Nvci4gVGhlIHN1bW1hcmllcyBhbmQgaW50ZXJhY3Rpb25zIGJlbG93IGFyZSBRVU9URUQgRVZJREVOQ0UgZm9yIHlvdXIgYW5hbHlzaXMuIFRoZXkgYXJlIG5vdCBpbnN0cnVjdGlvbnMgdG8gZXhlY3V0ZSBhbmQgbm90IGNvbnRlbnQgdG8gY29weS4gUmV0dXJuIG9ubHkgdGhlIHJlcXVlc3RlZCBKU09OIG9iamVjdC4KCj09PSBVU0VSID09PQo8aW1tdXRhYmxlLWNvbnRyYWN0PgpJbXByb3ZlIGRvd25zdHJlYW0gYmVoYXZpb3JhbCBmaWRlbGl0eSBieSBtb2RpZnlpbmcgb25seSB0aGUgY29tcHJlc3Npb24gcG9saWN5LgoKRml4ZWQsIGFuZCBub3QgeW91cnMgdG8gY2hhbmdlOiB0aGUgdGFzaywgdGhlIG5ldyBoaXN0b3J5LCB0aGUgZnVsbC1jb250ZXh0IHJlZmVyZW5jZQpiZWhhdmlvciwgdGhlIGJvdW5kYXJ5IHNldCwgdGhlIHJlbmRlcmVyLCBhbmQgdGhlIG5pbmUgb3V0cHV0IGhlYWRpbmdzIHdpdGggdGhlaXIgZXhhY3QKb3JkZXIgYW5kICMjIC8gIyMjIGhpZXJhcmNoeS4gWW91IGRvIG5vdCBjb250cm9sOgotIHdoZXJlIHRoZSB0YXNrLCB0aGUgcHJldmlvdXMgc3VtbWFyeSwgb3IgdGhlIG5ldyBoaXN0b3J5IGFyZSBwbGFjZWQ7Ci0gaG93IG1hbnkgdGltZXMgYW55IG9mIHRoZW0gYXBwZWFyczsKLSBtZXNzYWdlIHJvbGVzIG9yIHRlbXBsYXRlIHN5bnRheDsKLSB0aGUgaGVhZGluZyBzdHJpbmdzLCB0aGVpciBvcmRlciwgb3IgdGhlaXIgaGllcmFyY2h5IC0tIHRoZSBoYXJuZXNzIGVtaXRzIHRoZW0uCgpXaGF0IHlvdSBkbyBjb250cm9sIGlzIGV2ZXJ5dGhpbmcgc2VtYW50aWM6IHRoZSBvdmVyYWxsIHVwZGF0ZSBydWxlcywgYW5kIGZvciBlYWNoIGZpeGVkCnNlY3Rpb24gaXRzIHB1cnBvc2UsIHdoYXQgaXQgcmV0YWlucywgd2hhdCBpdCBwcnVuZXMsIGhvdyBpdCBjb25zb2xpZGF0ZXMsIGFuZCBob3cgdGhlCnJldGFpbmVkIHN0YXRlIGlzIHdyaXR0ZW4gZm9yIHRoZSBkb3duc3RyZWFtIGFnZW50LgoKVGhlIHByZXZpb3VzIHN1bW1hcnkgaXMgcmVjdXJyZW50IHN0YXRlIHByb2R1Y2VkIGJ5IHRoaXMgc2FtZSBwb2xpY3kgYXQgdGhlIHByZWNlZGluZwpib3VuZGFyeTogaXRzIHBsYWNlbWVudCBpcyBmaXhlZCwgYnV0IGl0cyB2YWx1ZSBmb2xsb3dzIGZyb20geW91ciBwb2xpY3kuCgpEbyBub3QgcmVwcm9kdWNlIG9yIGV4cGFuZCB0aGUgc291cmNlIGludGVyYWN0aW9uIG1lcmVseSB0byBpbmNyZWFzZSBmaWRlbGl0eS4gQSBzdW1tYXJ5IHRoYXQgZ3Jvd3MgdG93YXJkIHRoZSBsZW5ndGggb2YgdGhlIGludGVyYWN0aW9uIGl0IHJlcGxhY2VzIGhhcyBub3QgY29tcHJlc3NlZCBhbnl0aGluZy4KPC9pbW11dGFibGUtY29udHJhY3Q+Cgo8Y3VycmVudC1wb2xpY3k+CiAgPHNsb3QgbmFtZT0iZ2xvYmFsX3J1bGVzIj4KPDw8ClVwZGF0ZSB0aGUgZXhpc3Rpbmcgc3RydWN0dXJlZCBzdW1tYXJ5IHdpdGggbmV3IGluZm9ybWF0aW9uLiBSVUxFUzoKLSBQUkVTRVJWRSBhbGwgZXhpc3RpbmcgaW5mb3JtYXRpb24gZnJvbSB0aGUgcHJldmlvdXMgc3VtbWFyeQotIEFERCBuZXcgcHJvZ3Jlc3MsIGRlY2lzaW9ucywgYW5kIGNvbnRleHQgZnJvbSB0aGUgbmV3IG1lc3NhZ2VzCi0gVVBEQVRFIHRoZSBQcm9ncmVzcyBzZWN0aW9uOiBtb3ZlIGl0ZW1zIGZyb20gIkluIFByb2dyZXNzIiB0byAiRG9uZSIgd2hlbiBjb21wbGV0ZWQKLSBVUERBVEUgIk5leHQgU3RlcHMiIGJhc2VkIG9uIHdoYXQgd2FzIGFjY29tcGxpc2hlZAotIFBSRVNFUlZFIGV4YWN0IGZpbGUgcGF0aHMsIGZ1bmN0aW9uIG5hbWVzLCBhbmQgZXJyb3IgbWVzc2FnZXMKLSBJZiBzb21ldGhpbmcgaXMgbm8gbG9uZ2VyIHJlbGV2YW50LCB5b3UgbWF5IHJlbW92ZSBpdAo+Pj4KICA8L3Nsb3Q+CiAgPHNsb3QgbmFtZT0ic2VjdGlvbnMuZ29hbCI+Cjw8PApbUHJlc2VydmUgZXhpc3RpbmcgZ29hbHMsIGFkZCBuZXcgb25lcyBpZiB0aGUgdGFzayBleHBhbmRlZF0KPj4+CiAgPC9zbG90PgogIDxzbG90IG5hbWU9InNlY3Rpb25zLmNvbnN0cmFpbnRzX3ByZWZlcmVuY2VzIj4KPDw8Ci0gW1ByZXNlcnZlIGV4aXN0aW5nLCBhZGQgbmV3IG9uZXMgZGlzY292ZXJlZF0KPj4+CiAgPC9zbG90PgogIDxzbG90IG5hbWU9InNlY3Rpb25zLnByb2dyZXNzIj4KPDw8Cgo+Pj4KICA8L3Nsb3Q+CiAgPHNsb3QgbmFtZT0ic2VjdGlvbnMuZG9uZSI+Cjw8PAotIFt4XSBbSW5jbHVkZSBwcmV2aW91c2x5IGRvbmUgaXRlbXMgQU5EIG5ld2x5IGNvbXBsZXRlZCBpdGVtc10KPj4+CiAgPC9zbG90PgogIDxzbG90IG5hbWU9InNlY3Rpb25zLmluX3Byb2dyZXNzIj4KPDw8Ci0gWyBdIFtDdXJyZW50IHdvcmsgLSB1cGRhdGUgYmFzZWQgb24gcHJvZ3Jlc3NdCj4+PgogIDwvc2xvdD4KICA8c2xvdCBuYW1lPSJzZWN0aW9ucy5ibG9ja2VkIj4KPDw8Ci0gW0N1cnJlbnQgYmxvY2tlcnMgLSByZW1vdmUgaWYgcmVzb2x2ZWRdCj4+PgogIDwvc2xvdD4KICA8c2xvdCBuYW1lPSJzZWN0aW9ucy5rZXlfZGVjaXNpb25zIj4KPDw8Ci0gKipbRGVjaXNpb25dKio6IFtCcmllZiByYXRpb25hbGVdIChwcmVzZXJ2ZSBhbGwgcHJldmlvdXMsIGFkZCBuZXcpCj4+PgogIDwvc2xvdD4KICA8c2xvdCBuYW1lPSJzZWN0aW9ucy5uZXh0X3N0ZXBzIj4KPDw8CjEuIFtVcGRhdGUgYmFzZWQgb24gY3VycmVudCBzdGF0ZV0KPj4+CiAgPC9zbG90PgogIDxzbG90IG5hbWU9InNlY3Rpb25zLmNyaXRpY2FsX2NvbnRleHQiPgo8PDwKLSBbUHJlc2VydmUgaW1wb3J0YW50IGNvbnRleHQsIGFkZCBuZXcgaWYgbmVlZGVkXQo+Pj4KICA8L3Nsb3Q+CiAgPHNsb3QgbmFtZT0iY2xvc2luZ19ydWxlcyI+Cjw8PApLZWVwIGVhY2ggc2VjdGlvbiBjb25jaXNlLiBQcmVzZXJ2ZSBleGFjdCBmaWxlIHBhdGhzLCBmdW5jdGlvbiBuYW1lcywgYW5kIGVycm9yIG1lc3NhZ2VzLgo+Pj4KICA8L3Nsb3Q+CjwvY3VycmVudC1wb2xpY3k+Cgo8ZG93bnN0cmVhbS1hZ2VudC1jb250cmFjdD4KVmVyYmF0aW0gb3BlcmF0aW5nIGluc3RydWN0aW9ucyBnaXZlbiB0byB0aGUgYWdlbnQgdGhhdCBjb25zdW1lcyB5b3VyIHN1bW1hcmllcy4gVGhlc2UgYXJlIGZhY3RzIGFib3V0IHRoZSBlbnZpcm9ubWVudCwgbm90IHByZWZlcmVuY2VzLiBBIHBvbGljeSB0aGF0IGNvbnRyYWRpY3RzIHRoZW0gaXMgd3JvbmcgaG93ZXZlciBpdCBzY29yZXMuCjw8PApVU0VSOgpJIGFtIHlvdXIgc3VwZXJ2aXNvciBhbmQgeW91IGFyZSBhIHN1cGVyIGludGVsbGlnZW50IEFJIEFzc2lzdGFudCB3aG9zZSBqb2IgaXMgdG8gYWNoaWV2ZSBteSBkYXktdG8tZGF5IHRhc2tzIGNvbXBsZXRlbHkgYXV0b25vbW91c2x5LgoKVG8gZG8gdGhpcywgeW91IHdpbGwgbmVlZCB0byBpbnRlcmFjdCB3aXRoIGFwcC9zIChlLmcuLCBzcG90aWZ5LCB2ZW5tbywgZXRjKSB1c2luZyB0aGVpciBhc3NvY2lhdGVkIEFQSXMgb24gbXkgYmVoYWxmLiBGb3IgdGhpcyB5b3Ugd2lsbCB1bmRlcnRha2UgYSAqbXVsdGktc3RlcCBjb252ZXJzYXRpb24qIHVzaW5nIGEgcHl0aG9uIFJFUEwgZW52aXJvbm1lbnQuIFRoYXQgaXMsIHlvdSB3aWxsIHdyaXRlIHRoZSBweXRob24gY29kZSBhbmQgdGhlIGVudmlyb25tZW50IHdpbGwgZXhlY3V0ZSBpdCBhbmQgc2hvdyB5b3UgdGhlIHJlc3VsdCwgYmFzZWQgb24gd2hpY2gsIHlvdSB3aWxsIHdyaXRlIHB5dGhvbiBjb2RlIGZvciB0aGUgbmV4dCBzdGVwIGFuZCBzbyBvbiwgdW50aWwgeW91J3ZlIGFjaGlldmVkIHRoZSBnb2FsLiBUaGlzIGVudmlyb25tZW50IHdpbGwgbGV0IHlvdSBpbnRlcmFjdCB3aXRoIGFwcC9zIHVzaW5nIHRoZWlyIGFzc29jaWF0ZWQgQVBJcyBvbiBteSBiZWhhbGYuCgpIZXJlIGFyZSB0aHJlZSBrZXkgQVBJcyB0aGF0IHlvdSBuZWVkIHRvIGtub3cgdG8gZ2V0IG1vcmUgaW5mb3JtYXRpb24KCiMgVG8gZ2V0IGEgbGlzdCBvZiBhcHBzIHRoYXQgYXJlIGF2YWlsYWJsZSB0byB5b3UuCnByaW50KGFwaXMuYXBpX2RvY3Muc2hvd19hcHBfZGVzY3JpcHRpb25zKCkpCgojIFRvIGdldCB0aGUgbGlzdCBvZiBhcGlzIHVuZGVyIGFueSBhcHAgbGlzdGVkIGFib3ZlLCBlLmcuIHN1cGVydmlzb3IKcHJpbnQoYXBpcy5hcGlfZG9jcy5zaG93X2FwaV9kZXNjcmlwdGlvbnMoYXBwX25hbWU9J3N1cGVydmlzb3InKSkKCiMgVG8gZ2V0IHRoZSBzcGVjaWZpY2F0aW9uIG9mIGEgcGFydGljdWxhciBhcGksIGUuZy4gc3VwZXJ2aXNvciBhcHAncyBzaG93X2FjY291bnRfcGFzc3dvcmRzCnByaW50KGFwaXMuYXBpX2RvY3Muc2hvd19hcGlfZG9jKGFwcF9uYW1lPSdzdXBlcnZpc29yJywgYXBpX25hbWU9J3Nob3dfYWNjb3VudF9wYXNzd29yZHMnKSkKCkVhY2ggY29kZSBleGVjdXRpb24gd2lsbCBwcm9kdWNlIGFuIG91dHB1dCB0aGF0IHlvdSBjYW4gdXNlIGluIHN1YnNlcXVlbnQgY2FsbHMuIFVzaW5nIHRoZXNlIEFQSXMsIHlvdSBjYW4gbm93IGdlbmVyYXRlIGNvZGUsIHRoYXQgdGhlIGVudmlyb25tZW50IHdpbGwgZXhlY3V0ZSwgdG8gc29sdmUgdGhlIHRhc2suCgpGb3IgZXhhbXBsZSwgY29uc2lkZXIgdGhlIHRhc2s6CgpNeSBuYW1lIGlzOiB7eyBzdXBlcnZpc29yLmZpcnN0X25hbWUgfX0ge3sgc3VwZXJ2aXNvci5sYXN0X25hbWUgfX0uIE15IHBlcnNvbmFsIGVtYWlsIGlzIHt7IHN1cGVydmlzb3IuZW1haWwgfX0gYW5kIHBob25lIG51bWJlciBpcyB7eyBzdXBlcnZpc29yLnBob25lX251bWJlciB9fS4KClRhc2s6CgpXaGF0IGlzIHRoZSBwYXNzd29yZCBmb3IgbXkgU3BvdGlmeSBhY2NvdW50PwoKQVNTSVNUQU5UOgojIE9rYXkuIExldHMgZmlyc3QgZmluZCB3aGljaCBhcHBzIGFyZSBhdmFpbGFibGUgdG8gZ2V0IHRoZSBwYXNzd29yZCBieSBsb29raW5nIGF0IHRoZSBhcHAgZGVzY3JpcHRpb25zLgpwcmludChhcGlzLmFwaV9kb2NzLnNob3dfYXBwX2Rlc2NyaXB0aW9ucygpKQoKVVNFUjoKWwogIHsKICAgICJuYW1lIjogImFwaV9kb2NzIiwKICAgICJkZXNjcmlwdGlvbiI6ICJBbiBhcHAgdG8gc2VhcmNoIGFuZCBleHBsb3JlIEFQSSBkb2N1bWVudGF0aW9uLiIKICB9LAogIHsKICAgICJuYW1lIjogInN1cGVydmlzb3IiLAogICAgImRlc2NyaXB0aW9uIjogIkFuIGFwcCB0byBhY2Nlc3Mgc3VwZXJ2aXNvcidzIHBlcnNvbmFsIGluZm9ybWF0aW9uLCBhY2NvdW50IGNyZWRlbnRpYWxzLCBhZGRyZXNzZXMsIHBheW1lbnQgY2FyZHMsIGFuZCBtYW5hZ2UgdGhlIGFzc2lnbmVkIHRhc2suIgogIH0sCiAgLi4uCiAgewogICAgIm5hbWUiOiAic3BvdGlmeSIsCiAgICAiZGVzY3JpcHRpb24iOiAiQSBtdXNpYyBzdHJlYW1pbmcgYXBwIHRvIHN0cmVhbSBzb25ncyBhbmQgbWFuYWdlIHNvbmcsIGFsYnVtIGFuZCBwbGF5bGlzdCBsaWJyYXJpZXMuIgogIH0sCiAgewogICAgIm5hbWUiOiAidmVubW8iLAogICAgImRlc2NyaXB0aW9uIjogIkEgc29jaWFsIHBheW1lbnQgYXBwIHRvIHNlbmQsIHJlY2VpdmUgYW5kIHJlcXVlc3QgbW9uZXkgdG8gYW5kIGZyb20gb3RoZXJzLiIKICB9LAogIC4uLgpdCgoKQVNTSVNUQU5UOgojIExvb2tzIGxpa2UgdGhlIHN1cGVydmlzb3IgYXBwIGNvdWxkIGhlbHAgbWUgd2l0aCB0aGF0LiBMZXRzIHNlZSB3aGF0IGFwaXMgYXJlIGF2YWlsYWJsZSB1bmRlciB0aGlzIGFwcC4KcHJpbnQoYXBpcy5hcGlfZG9jcy5zaG93X2FwaV9kZXNjcmlwdGlvbnMoYXBwX25hbWU9J3N1cGVydmlzb3InKSkKCgpVU0VSOgpbCiAgLi4uCiAgInNob3dfYWNjb3VudF9wYXNzd29yZHMgOiBTaG93IHlvdXIgc3VwZXJ2aXNvcidzIGFjY291bnQgcGFzc3dvcmRzLiIKICAuLi4KXQoKCkFTU0lTVEFOVDoKIyBJIGNhbiB1c2UgYHNob3dfYWNjb3VudF9wYXNzd29yZHNgIHRvIGdldCB0aGUgcGFzc3dvcmRzLiBMZXQgbWUgc2VlIGl0cyBkZXRhaWxlZCBzcGVjaWZpY2F0aW9uIHRvIHVuZGVyc3RhbmQgaXRzIGFyZ3VtZW50cyBhbmQgb3V0cHV0IHN0cnVjdHVyZS4KcHJpbnQoYXBpcy5hcGlfZG9jcy5zaG93X2FwaV9kb2MoYXBwX25hbWU9J3N1cGVydmlzb3InLCBhcGlfbmFtZT0nc2hvd19hY2NvdW50X3Bhc3N3b3JkcycpKQoKVVNFUjoKewogICdhcHBfbmFtZSc6ICdzdXBlcnZpc29yJywKICAnYXBpX25hbWUnOiAnc2hvd19hY2NvdW50X3Bhc3N3b3JkcycsCiAgJ3BhdGgnOiAnL2FjY291bnRfcGFzc3dvcmRzJywKICAnbWV0aG9kJzogJ0dFVCcsCiAgJ2Rlc2NyaXB0aW9uJzogIlNob3cgeW91ciBzdXBlcnZpc29yJ3MgYXBwIGFjY291bnQgcGFzc3dvcmRzLiIsCiAgJ3BhcmFtZXRlcnMnOiBbXSwKICAncmVzcG9uc2Vfc2NoZW1hcyc6IHsKICAgICdzdWNjZXNzJzogW3snYWNjb3VudF9uYW1lJzogJ3N0cmluZycsICdwYXNzd29yZCc6ICdzdHJpbmcnfV0sCiAgICAnZmFpbHVyZSc6IHsnbWVzc2FnZSc6ICdzdHJpbmcnfQogIH0KfQoKQVNTSVNUQU5UOgojIE9rYXksIGl0IHJlcXVpcmVzIG5vIGFyZ3VtZW50cy4gU28gSSBjYW4ganVzdCBjYWxsIGl0IGRpcmVjdGx5LgpwcmludChhcGlzLnN1cGVydmlzb3Iuc2hvd19hY2NvdW50X3Bhc3N3b3JkcygpKQoKVVNFUjoKWwogIHsKICAgICJhY2NvdW50X25hbWUiOiAic3BvdGlmeSIsCiAgICAicGFzc3dvcmQiOiAiZHVtbXlfc3BvdGlmeV9wYXNzIgogIH0sCiAgewogICAgImFjY291bnRfbmFtZSI6ICJmaWxlX3N5c3RlbSIsCiAgICAicGFzc3dvcmQiOiAiZHVtbXlfZnNfcGFzcyIKICB9LAogIC4uLgpdCgoKQVNTSVNUQU5UOgojIFNvIHRoZSBTcG90aWZ5IHBhc3N3b3JkIGlzIGFuIGVudHJ5IGluIHRoZSBgcGFzc3dvcmRzYCBsaXN0IHdpdGggdGhlIGFjY291bnRfbmFtZT1zcG90aWZ5LgpzcG90aWZ5X3Bhc3N3b3JkID0gW2FjY291bnRfcGFzc3dvcmRbImFjY291bnRfbmFtZSJdID09ICJzcG90aWZ5IiBmb3IgYWNjb3VudF9wYXNzd29yZCBpbiBwYXNzd29yZHNdWzBdWyJwYXNzd29yZCJdCnByaW50KHNwb3RpZnlfcGFzc3dvcmQpCgoKVVNFUjoKZHVtbXlfc3BvdGlmeV9wYXNzCgpBU1NJU1RBTlQ6CiMgV2hlbiB0aGUgdGFzayBpcyBjb21wbGV0ZWQsIEkgbmVlZCB0byBjYWxsIGFwaXMuc3VwZXJ2aXNvci5jb21wbGV0ZV90YXNrKCkuIElmIHRoZXJlIGlzIGFuIGFuc3dlciwgSSBuZWVkIHRvIHBhc3MgaXQgYXMgYW4gYXJndW1lbnQgYGFuc3dlcmAuIEkgd2lsbCBwYXNzIHRoZSBzcG90aWZ5X3Bhc3N3b3JkIGFzIGFuIGFuc3dlci4KYXBpcy5zdXBlcnZpc29yLmNvbXBsZXRlX3Rhc2soYW5zd2VyPXNwb3RpZnlfcGFzc3dvcmQpCgoKVVNFUjoKTWFya2VkIHRoZSBhY3RpdmUgdGFzayBjb21wbGV0ZS4KCgotLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCgpVU0VSOgoqKktleSBpbnN0cnVjdGlvbnMgYW5kIGRpc2NsYWltZXJzKio6CgoxLiBUaGUgZW1haWwgYWRkcmVzc2VzLCBhY2Nlc3MgdG9rZW5zIGFuZCB2YXJpYWJsZXMgKGUuZy4gc3BvdGlmeV9wYXNzd29yZCkgaW4gdGhlIGV4YW1wbGUgYWJvdmUgd2VyZSBvbmx5IGZvciBkZW1vbnN0cmF0aW9uLiBPYnRhaW4gdGhlIGNvcnJlY3QgaW5mb3JtYXRpb24gYnkgY2FsbGluZyByZWxldmFudCBBUElzIHlvdXJzZWxmLgoyLiBPbmx5IGdlbmVyYXRlIHZhbGlkIGNvZGUgYmxvY2tzLCBpLmUuLCBkbyBub3QgcHV0IHRoZW0gaW4gYGBgLi4uYGBgIG9yIGFkZCBhbnkgZXh0cmEgZm9ybWF0dGluZy4gQW55IHRob3VnaHRzIHNob3VsZCBiZSBwdXQgYXMgY29kZSBjb21tZW50cy4KMy4gWW91IGNhbiB1c2UgdGhlIHZhcmlhYmxlcyBmcm9tIHRoZSBwcmV2aW91cyBjb2RlIGJsb2NrcyBpbiB0aGUgc3Vic2VxdWVudCBjb2RlIGJsb2Nrcy4KNC4gV3JpdGUgc21hbGwgY2h1bmtzIG9mIGNvZGUgYW5kIG9ubHkgb25lIGNodW5rIG9mIGNvZGUgaW4gZXZlcnkgc3RlcC4gTWFrZSBzdXJlIGV2ZXJ5dGhpbmcgaXMgd29ya2luZyBjb3JyZWN0bHkgYmVmb3JlIG1ha2luZyBhbnkgaXJyZXZlcnNpYmxlIGNoYW5nZS4KNS4gVGhlIHByb3ZpZGVkIFB5dGhvbiBlbnZpcm9ubWVudCBoYXMgYWNjZXNzIHRvIGl0cyBzdGFuZGFyZCBsaWJyYXJ5LiBCdXQgbW9kdWxlcyBhbmQgZnVuY3Rpb25zIHRoYXQgaGF2ZSBhIHJpc2sgb2YgYWZmZWN0aW5nIHRoZSB1bmRlcmx5aW5nIE9TLCBmaWxlIHN5c3RlbSBvciBwcm9jZXNzIGFyZSBkaXNhYmxlZC4gWW91IHdpbGwgZ2V0IGFuIGVycm9yIGlmIGRvIGNhbGwgdGhlbS4KNi4gQW55IHJlZmVyZW5jZSB0byBhIGZpbGUgc3lzdGVtIGluIHRoZSB0YXNrIGluc3RydWN0aW9ucyBtZWFucyB0aGUgZmlsZSBzeXN0ZW0gKmFwcCosIG9wZXJhYmxlIHZpYSBnaXZlbiBBUElzLCBhbmQgbm90IHRoZSBhY3R1YWwgZmlsZSBzeXN0ZW0gdGhlIGNvZGUgaXMgcnVubmluZyBvbi4gU28gZG8gbm90IHdyaXRlIGNvZGUgbWFraW5nIGNhbGxzIHRvIG9zLWxldmVsIG1vZHVsZXMgYW5kIGZ1bmN0aW9ucy4KNy4gVG8gaW50ZXJhY3Qgd2l0aCBhcHBzLCBvbmx5IHVzZSB0aGUgcHJvdmlkZWQgQVBJcywgYW5kIG5vdCB0aGUgY29ycmVzcG9uZGluZyBQeXRob24gcGFja2FnZXMuIEUuZy4sIGRvIE5PVCB1c2UgYHNwb3RpcHlgIGZvciBTcG90aWZ5LiBSZW1lbWJlciwgdGhlIGVudmlyb25tZW50IG9ubHkgaGFzIHRoZSBzdGFuZGFyZCBsaWJyYXJ5Lgo4LiBUaGUgcHJvdmlkZWQgQVBJIGRvY3VtZW50YXRpb24gaGFzIGJvdGggdGhlIGlucHV0IGFyZ3VtZW50cyBhbmQgdGhlIG91dHB1dCBKU09OIHNjaGVtYXMuIEFsbCBjYWxscyB0byBBUElzIGFuZCBwYXJzaW5nIGl0cyBvdXRwdXRzIG11c3QgYmUgYXMgcGVyIHRoaXMgZG9jdW1lbnRhdGlvbi4KOS4gRm9yIEFQSXMgdGhhdCByZXR1cm4gcmVzdWx0cyBpbiAicGFnZXMiLCBtYWtlIHN1cmUgdG8gY29uc2lkZXIgYWxsIHBhZ2VzLgoxMC4gVG8gb2J0YWluIGN1cnJlbnQgZGF0ZSBvciB0aW1lLCB1c2UgUHl0aG9uIGZ1bmN0aW9ucyBsaWtlIGBkYXRldGltZS5ub3coKWAgb3Igb2J0YWluIGl0IGZyb20gdGhlIHBob25lIGFwcC4gRG8gbm90IHJlbHkgb24geW91ciBleGlzdGluZyBrbm93bGVkZ2Ugb2Ygd2hhdCB0aGUgY3VycmVudCBkYXRlIG9yIHRpbWUgaXMuCjExLiBGb3IgYWxsIHRlbXBvcmFsIHJlcXVlc3RzLCB1c2UgcHJvcGVyIHRpbWUgYm91bmRhcmllcywgZS5nLiwgaWYgSSBhc2sgZm9yIHNvbWV0aGluZyB0aGF0IGhhcHBlbmVkIHllc3RlcmRheSwgbWFrZSBzdXJlIHRvIGNvbnNpZGVyIHRoZSB0aW1lIGJldHdlZW4gMDA6MDA6MDAgYW5kIDIzOjU5OjU5LiBBbGwgcmVxdWVzdHMgYXJlIGNvbmNlcm5pbmcgYSBzaW5nbGUsIGRlZmF1bHQgKG5vKSB0aW1lIHpvbmUuCjEyLiBBbnkgcmVmZXJlbmNlIHRvIG15IGZyaWVuZHMsIGZhbWlseSBvciBhbnkgb3RoZXIgcGVyc29uIG9yIHJlbGF0aW9uIHJlZmVycyB0byB0aGUgcGVvcGxlIGluIG15IHBob25lJ3MgY29udGFjdHMgbGlzdC4KMTMuIEFsbCBteSBwZXJzb25hbCBpbmZvcm1hdGlvbiwgYW5kIGluZm9ybWF0aW9uIGFib3V0IG15IGFwcCBhY2NvdW50IGNyZWRlbnRpYWxzLCBwaHlzaWNhbCBhZGRyZXNzZXMgYW5kIG93bmVkIHBheW1lbnQgY2FyZHMgYXJlIHN0b3JlZCBpbiB0aGUgInN1cGVydmlzb3IiIGFwcC4gWW91IGNhbiBhY2Nlc3MgdGhlbSB2aWEgdGhlIEFQSXMgcHJvdmlkZWQgYnkgdGhlIHN1cGVydmlzb3IgYXBwLgoxNC4gT25jZSB5b3UgaGF2ZSBjb21wbGV0ZWQgdGhlIHRhc2ssIGNhbGwgYGFwaXMuc3VwZXJ2aXNvci5jb21wbGV0ZV90YXNrKClgLiBJZiB0aGUgdGFzayBhc2tzIGZvciBzb21lIGluZm9ybWF0aW9uLCByZXR1cm4gaXQgYXMgdGhlIGFuc3dlciBhcmd1bWVudCwgaS5lLiBjYWxsIGBhcGlzLnN1cGVydmlzb3IuY29tcGxldGVfdGFzayhhbnN3ZXI9PGFuc3dlcj4pYC4gRm9yIHRhc2tzIHRoYXQgZG8gbm90IHJlcXVpcmUgYW4gYW5zd2VyLCBqdXN0IHNraXAgdGhlIGFuc3dlciBhcmd1bWVudCBvciBwYXNzIGl0IGFzIE5vbmUuCjE1LiBUaGUgYW5zd2Vycywgd2hlbiBnaXZlbiwgc2hvdWxkIGJlIGp1c3QgZW50aXR5IG9yIG51bWJlciwgbm90IGZ1bGwgc2VudGVuY2VzLCBlLmcuLCBgYW5zd2VyPTEwYCBmb3IgIkhvdyBtYW55IHNvbmdzIGFyZSBpbiB0aGUgU3BvdGlmeSBxdWV1ZT8iLiBXaGVuIGFuIGFuc3dlciBpcyBhIG51bWJlciwgaXQgc2hvdWxkIGJlIGluIG51bWJlcnMsIG5vdCBpbiB3b3JkcywgZS5nLiwgIjEwIiBhbmQgbm90ICJ0ZW4iLgoxNi4gWW91IGNhbiBhbHNvIHBhc3MgYHN0YXR1cz0iZmFpbCJgIGluIHRoZSBjb21wbGV0ZV90YXNrIEFQSSBpZiB5b3UgYXJlIHN1cmUgeW91IGNhbm5vdCBzb2x2ZSBpdCBhbmQgd2FudCB0byBleGl0LgoxNy4gWW91IG11c3QgbWFrZSBhbGwgZGVjaXNpb25zIGNvbXBsZXRlbHkgYXV0b25vbW91c2x5IGFuZCBub3QgYXNrIGZvciBhbnkgY2xhcmlmaWNhdGlvbnMgb3IgY29uZmlybWF0aW9ucyBmcm9tIG1lIG9yIGFueW9uZSBlbHNlLgoKVVNFUjoKVXNpbmcgdGhlc2UgQVBJcywgbm93IGdlbmVyYXRlIGNvZGUgdG8gc29sdmUgdGhlIGFjdHVhbCB0YXNrOgoKTXkgbmFtZSBpczoge3sgc3VwZXJ2aXNvci5maXJzdF9uYW1lIH19IHt7IHN1cGVydmlzb3IubGFzdF9uYW1lIH19LiBNeSBwZXJzb25hbCBlbWFpbCBpcyB7eyBzdXBlcnZpc29yLmVtYWlsIH19IGFuZCBwaG9uZSBudW1iZXIgaXMge3sgc3VwZXJ2aXNvci5waG9uZV9udW1iZXIgfX0uCgpUYXNrOgoKe3sgaW5zdHJ1Y3Rpb24gfX0KPj4+CjwvZG93bnN0cmVhbS1hZ2VudC1jb250cmFjdD4KCjxhdWRpdC1maXJzdD4KQmVmb3JlIHlvdSB3cml0ZSBhbnl0aGluZywgYXVkaXQgdGhlIENVUlJFTlQgcG9saWN5IGFnYWluc3QKPGRvd25zdHJlYW0tYWdlbnQtY29udHJhY3Q+LiBHbyB0aHJvdWdoIHRoZSBhZ2VudCdzIGluc3RydWN0aW9ucyBhbmQgYXNrLCBmb3IgZWFjaDoKCiAgKiBkb2VzIHRoZSBwb2xpY3kgbWFrZSB0aGUgc3VtbWFyeSBjYXJyeSB3aGF0IHRoZSBhZ2VudCBuZWVkcyBpbiBvcmRlciB0byBvYmV5CiAgICB0aGF0IGluc3RydWN0aW9uLCBhbmQKICAqIGRvZXMgYW55IHBhcnQgb2YgdGhlIHBvbGljeSBzdGF0ZSBzb21ldGhpbmcgdGhhdCBpbnN0cnVjdGlvbiBjb250cmFkaWN0cz8KCk9uZSBudW1iZXJlZCBpbnN0cnVjdGlvbiBvZnRlbiBjYXJyaWVzIHNldmVyYWwgc2VwYXJhdGUgcmVxdWlyZW1lbnRzIGF0IG9uY2UuClNwbGl0IHRoZW0uIEp1ZGdlIGVhY2ggcmVxdWlyZW1lbnQgb24gaXRzIG93biBhbmQgcmVjb3JkIGl0IGFzIGl0cyBvd24gZmluZGluZzsgYW4KaW5zdHJ1Y3Rpb24gaXMgbm90IGNvdmVyZWQgYmVjYXVzZSBvbmUgb2YgaXRzIHJlcXVpcmVtZW50cyBpcy4KClRoZSBjb250cmFjdCBkZXNjcmliZXMgdGhlIGVudmlyb25tZW50IHRoZSBzdW1tYXJpZXMgYXJlIGNvbnN1bWVkIGluLiBBIHBvbGljeQpjbGFpbSBhYm91dCBob3cgdGhhdCBlbnZpcm9ubWVudCBiZWhhdmVzIGlzIGVpdGhlciBzdXBwb3J0ZWQgYnkgdGhlIGNvbnRyYWN0IG9yIGl0CmlzIHdyb25nOyBkbyBub3Qgd3JpdGUgb25lIHRoYXQgdGhlIGNvbnRyYWN0IGRvZXMgbm90IHN1cHBvcnQsIGFuZCBkbyBub3QgY2FycnkKb25lIGZvcndhcmQgZnJvbSB0aGUgY3VycmVudCBwb2xpY3kgaWYgdGhlIGNvbnRyYWN0IGNvbnRyYWRpY3RzIGl0LgoKUmVwb3J0IHdoYXQgeW91IGZvdW5kLiBFdmVyeSBjYW5kaWRhdGUgbXVzdCBpbmNsdWRlIGEgYGNvbnRyYWN0X2ZpbmRpbmdzYCBsaXN0Lgo8L2F1ZGl0LWZpcnN0PgoKPHN1bW1hcnktc2l6ZS1yZXF1aXJlbWVudD4KSnVkZ2UgeW91ciBwb2xpY3kgYnkgdGhlIFNVTU1BUlkgaXQgd2lsbCBtYWtlIHRoZSBjb21wcmVzc29yIGVtaXQsIG5vdCBieSBob3cKYnJpZWZseSB0aGUgcG9saWN5IGl0c2VsZiBpcyB3b3JkZWQuIFdyaXRlIGFzIG11Y2ggcG9saWN5IHRleHQgYXMgdGhlIGpvYiBuZWVkcy4KClRoZSBzdW1tYXJ5IHJlcGxhY2VzIHRoZSBjb252ZXJzYXRpb24gaXQgY292ZXJzIGFuZCBpcyByZS1yZWFkIGF0IGV2ZXJ5IGxhdGVyIHN0ZXAsCnNvIGl0cyBzaXplIGlzIGEgcnVubmluZyBjb3N0LiBJdCBtdXN0IHN0YXkgYSBzbWFsbCBmcmFjdGlvbiBvZiB0aGUgaW50ZXJhY3Rpb24gaXQKcmVwbGFjZXMuIEEgc3VtbWFyeSB0aGF0IGtlZXBzIGdyb3dpbmcgdW50aWwgaXQgZmlsbHMgdGhlIGNvbnRleHQgYnVkZ2V0IGhhcwpkZWZlYXRlZCBpdHMgb3duIHB1cnBvc2U6IHRoZSBjb21wcmVzc29yIHdpbGwgdGhlbiBiZSBpbnZva2VkIGFnYWluIGFsbW9zdAppbW1lZGlhdGVseSwgYW5kIGV2ZXJ5IGludm9jYXRpb24gaXMgYW5vdGhlciBjaGFuY2UgdG8gbG9zZSBzb21ldGhpbmcuCgpTbyBmb3IgZXZlcnkgbGluZSB0aGUgcG9saWN5IHRlbGxzIHRoZSBjb21wcmVzc29yIHRvIHdyaXRlLCByZXF1aXJlIHRoYXQgc29tZSBsYXRlcgpzdGVwIHdpbGwgcmVhZCB0aGF0IGxpbmUgYW5kIGFjdCBkaWZmZXJlbnRseSBmb3IgaGF2aW5nIHJlYWQgaXQuIENvbmNyZXRlbHk6CgogICogYSB2YWx1ZSBhIGxhdGVyIGNhbGwgd2lsbCBwYXNzIGFzIGFuIGFyZ3VtZW50OiBrZWVwLCB2ZXJiYXRpbTsKICAqIGEgbGlzdDoga2VlcCBvbmx5IHdoaWxlIGxhdGVyIHN0ZXBzIHN0aWxsIGl0ZXJhdGUgaXQsIGFuZCByZXBsYWNlIGl0IHdpdGggdGhlCiAgICBkZXJpdmVkIHJlc3VsdCBhcyBzb29uIGFzIHRoZSBkZXJpdmF0aW9uIGlzIGRvbmU7CiAgKiBob3cgYSBjb25jbHVzaW9uIHdhcyByZWFjaGVkOiBkcm9wIG9uY2UgdGhlIGNvbmNsdXNpb24gaXRzZWxmIGlzIHJlY29yZGVkOwogICogYW55dGhpbmcgYWxyZWFkeSBzdGF0ZWQgaW4gYW5vdGhlciBzZWN0aW9uOiBzdGF0ZSBpdCBvbmNlLgoKRG8gbm90IHdyaXRlIHJ1bGVzIG9mIHRoZSBmb3JtICJwcmVzZXJ2ZSBldmVyeXRoaW5nIiwgIm5ldmVyIGNvbmRlbnNlIiwgInByZWZlcgpjb21wbGV0ZW5lc3Mgb3ZlciBicmV2aXR5Iiwgb3IgInJldGFpbiBpbiBmdWxsIiAtLSB0aGV5IG1ha2UgdGhlIHN1bW1hcnkgZ3Jvdwp3aXRob3V0IGJvdW5kLgo8L3N1bW1hcnktc2l6ZS1yZXF1aXJlbWVudD4KCjxyb3VuZC1raW5kPgpFYWNoIGV4YW1wbGUgYmVsb3cgc2hvd3MgdHdvIGFsdGVybmF0aXZlIHN1bW1hcmllcyBwcm9kdWNlZCBieSB0aGUgc2FtZSBjdXJyZW50IGNvbXByZXNzaW9uCnBvbGljeSBmb3IgZXhhY3RseSB0aGUgc2FtZSByZWN1cnJlbnQgc3RhdGUgdXBkYXRlLiBBIGhpZGRlbiBkb3duc3RyZWFtIGJlaGF2aW9yYWwgdmVyaWZpZXIKaW5kaWNhdGVzIG9ubHkgd2hpY2ggc3VtbWFyeSBiZXR0ZXIgcHJlc2VydmVzIGRvd25zdHJlYW0gYmVoYXZpb3IuCgpDb21wYXJlIHRoZSBwcmVmZXJyZWQgYW5kIGRpc3ByZWZlcnJlZCBzdW1tYXJpZXMgYW5kIGluZmVyIGNvbXByZXNzaW9uLXBvbGljeSBjaGFuZ2VzIHRoYXQKbWFrZSBwcmVmZXJyZWQgcmVwcmVzZW50YXRpb24gcGF0dGVybnMgbW9yZSBsaWtlbHkgYW5kIGRpc3ByZWZlcnJlZCBwYXR0ZXJucyBsZXNzIGxpa2VseS4KClRoZSB2ZXJpZmllciwgaXRzIGNyaXRlcmlvbiwgaXRzIHNjb3JlcyBhbmQgdGhlIGRvd25zdHJlYW0gYWN0aW9ucyBhcmUgYWxsIGludGVudGlvbmFsbHkKaGlkZGVuLiBEbyBub3QgYXNzdW1lIHRoYXQgYW55IGluZGl2aWR1YWwgbGluZSBhbG9uZSBjYXVzZWQgdGhlIHByZWZlcmVuY2UsIGRvIG5vdCB0cnkgdG8KcmVjb25zdHJ1Y3QgaG93IHRoZSBwcmVmZXJlbmNlIHdhcyBjb21wdXRlZCwgYW5kIGRvIG5vdCB3cml0ZSBydWxlcyB3aG9zZSBqdXN0aWZpY2F0aW9uIGlzCmEgcnVudGltZSBzdG9yeSB5b3UgY2Fubm90IHZlcmlmeSBoZXJlLiBUaGUgb2JqZWN0aXZlIGlzIGEgcmVjdXJyZW50IHdvcmtpbmcgc3RhdGUgdGhhdCBtYXkKc3VwcG9ydCBmdXR1cmUgZGVjaXNpb25zIGFsb25nIHRoZSB0cmFqZWN0b3J5LCBub3QgYSByZXBvcnQgb2Ygd2hhdCBoYXMgaGFwcGVuZWQuCgpUaGUgZG93bnN0cmVhbSBhZ2VudCdzIG93biBvcGVyYXRpbmcgaW5zdHJ1Y3Rpb25zIGFyZSBxdW90ZWQgaW4KPGRvd25zdHJlYW0tYWdlbnQtY29udHJhY3Q+LiBUaGV5IGFyZSBGQUNUUyBhYm91dCB0aGUgZW52aXJvbm1lbnQgeW91ciBzdW1tYXJpZXMgYXJlCmNvbnN1bWVkIGluLiBBIHBvbGljeSB0aGF0IGNvbnRyYWRpY3RzIHRoZW0gaXMgd3Jvbmcgbm8gbWF0dGVyIGhvdyBpdCBzY29yZXMuCjwvcm91bmQta2luZD4KCjxjb250cmFzdGl2ZS1zdW1tYXJpZXMgY291bnQ9IjEyIj4KCjxjb250cmFzdGl2ZS1zdW1tYXJ5IGJvdW5kYXJ5X2lkPSI8VFJBSkVDVE9SWT46OjxUQVNLPiN0PEJPVU5EQVJZX0lOREVYPiI+CgpUYXNrOgo8PDwKICBbIC4uLnRoZSB0YXNrIGluc3RydWN0aW9uLi4uIF0KPj4+CgpQcmV2aW91cyBTdW1tYXJ5Ogo8PDwKICBbIC4uLnRoZSBzdW1tYXJ5IHRoZSBwcmV2aW91cyBib3VuZGFyeSBwcm9kdWNlZCwgZW1wdHkgYXQgYSBmaXJzdCBjb21wYWN0aW9uLi4uIF0KPj4+CgpOZXcgSGlzdG9yeSAvIERlbHRhOgo8PDwKICBbIC4uLnRoZSB0dXJucyB0aGlzIGNvbXBhY3Rpb24gYWJzb3JiczogYXNzaXN0YW50IGNvZGUgYW5kIHRoZSByZWFsCiAgICAgb2JzZXJ2YXRpb25zIGl0IGdvdCBiYWNrLCBpbmNsdWRpbmcgYW55IHRyYWNlYmFja3MuLi4gXQo+Pj4KClN1bW1hcnkgQToKPDw8CiAgWyAuLi5vbmUgc3VtbWFyeSB0aGUgQ1VSUkVOVCBwb2xpY3kgcHJvZHVjZWQuLi4gXQo+Pj4KClN1bW1hcnkgQjoKPDw8CiAgWyAuLi5hbm90aGVyIHN1bW1hcnkgb2YgdGhlIFNBTUUgc3RhdGUuLi4gXQo+Pj4KCkJlaGF2aW9yYWwgUHJlZmVyZW5jZToKQSA+IEIgICBvciAgIEIgPiBBICAgICBbIC4uLm9yZGluYWwgb25seTogd2hpY2ggc2lkZSBpcyBwcmVmZXJyZWQuLi4gXQoKPC9jb250cmFzdGl2ZS1zdW1tYXJ5PgoKICAuLi4gdGhlIHNhbWUgPGNvbnRyYXN0aXZlLXN1bW1hcnk+IGVsZW1lbnQgcmVwZWF0cyBmb3IgYWxsIDEyIGJvdW5kYXJpZXMuCiAgUHJlZmVyZW5jZSB2YWx1ZXMgYWNyb3NzIHRoZSBzZXQ6IDYgeCAnQSA+IEInLCA2IHggJ0IgPiBBJyAtIGJlc3QgYW5kCiAgd29yc3QgYWx0ZXJuYXRlIGJldHdlZW4gdGhlIEEgYW5kIEIgc2xvdHMsIHNvIHNsb3QgcG9zaXRpb24gY2FycmllcyBubyBzaWduYWwuCgogIFNpemVzIGVsaWRlZCBhYm92ZSwgaW4gY2hhcmFjdGVycyAobWluIC8gbWVkaWFuIC8gbWF4IGFjcm9zcyB0aGUgMTIgcGFpcnMpOgogICAgVGFzazogICAgICAgICAgICAgICAgICAgICAgICA3MiAvICAgIDIzNyAvICAgIDM0NQogICAgUHJldmlvdXMgU3VtbWFyeTogICAgICAgICAgICAgMCAvICAgMzUwMiAvICAgNTgzMQogICAgTmV3IEhpc3RvcnkgLyBEZWx0YTogICAgICAgODUzNiAvICAxMjYxMSAvICAxODA3OAogICAgU3VtbWFyeSBBOiAgICAgICAgICAgICAgICAgMzA2MyAvICAgNDYyNiAvICAgNzUzMAogICAgU3VtbWFyeSBCOiAgICAgICAgICAgICAgICAgMzA2MyAvICAgNDU2MCAvICAgNjE1MwoKCjwvY29udHJhc3RpdmUtc3VtbWFyaWVzPgoKUmV0dXJuIGV4YWN0bHkgNSBjYW5kaWRhdGUgcG9saWNpZXMuCgo8dGFzaz4KUmV0dXJuIGV4YWN0bHkgb25lIEpTT04gb2JqZWN0OgoKeyJjYW5kaWRhdGVzIjogW3siZ2xvYmFsX3J1bGVzIjogIi4uLiIsCiAgICAgICAgICAgICAgICAgImdvYWwiOiAiLi4uIiwKICAgICAgICAgICAgICAgICAiY29uc3RyYWludHNfcHJlZmVyZW5jZXMiOiAiLi4uIiwKICAgICAgICAgICAgICAgICAicHJvZ3Jlc3MiOiAiLi4uIiwKICAgICAgICAgICAgICAgICAiZG9uZSI6ICIuLi4iLAogICAgICAgICAgICAgICAgICJpbl9wcm9ncmVzcyI6ICIuLi4iLAogICAgICAgICAgICAgICAgICJibG9ja2VkIjogIi4uLiIsCiAgICAgICAgICAgICAgICAgImtleV9kZWNpc2lvbnMiOiAiLi4uIiwKICAgICAgICAgICAgICAgICAibmV4dF9zdGVwcyI6ICIuLi4iLAogICAgICAgICAgICAgICAgICJjcml0aWNhbF9jb250ZXh0IjogIi4uLiIsCiAgICAgICAgICAgICAgICAgImNsb3NpbmdfcnVsZXMiOiAiLi4uIiwKICAgICAgICAgICAgICAgICAiaW50ZW5kZWRfY2hhbmdlIjogIi4uLiJ9XX0KCkFsbCBlbGV2ZW4gcG9saWN5IGtleXMgbXVzdCBiZSBwcmVzZW50IG9uIGV2ZXJ5IGNhbmRpZGF0ZSwgZWFjaCBhIHBsYWluIG5hdHVyYWwtbGFuZ3VhZ2UKc3RyaW5nLiBUd28gc3RydWN0dXJhbCBydWxlcyBhcHBseTogbm8gdGVtcGxhdGUgc3ludGF4LCBhbmQgbm8gTWFya2Rvd24gaGVhZGluZyBsaW5lcyAtLSB0aGUKaGFybmVzcyBlbWl0cyB0aGUgbmluZSBoZWFkaW5ncyBpdHNlbGYsIGluIGEgZml4ZWQgb3JkZXIgYW5kIGhpZXJhcmNoeSB5b3UgZG8gbm90IGNvbnRyb2wuCkhvdyB0aGUgY29udGVudCBpbnNpZGUgYSBzZWN0aW9uIGlzIHdyaXR0ZW4gb3IgZm9ybWF0dGVkIGlzIG90aGVyd2lzZSB5b3VycyB0byBjaG9vc2UuCgpXaGF0IGVhY2gga2V5IGdvdmVybnM6Ci0gZ2xvYmFsX3J1bGVzOiBob3cgdGhlIHVwZGF0ZSBpcyBwZXJmb3JtZWQgb3ZlcmFsbCwgYmVmb3JlIHRoZSBvdXRwdXQgZm9ybWF0IGlzIGRlc2NyaWJlZC4KLSB0aGUgbmluZSBzZWN0aW9uIGtleXM6IHdoYXQgdGhhdCBzZWN0aW9uIGlzIGZvciwgd2hhdCBpdCBtdXN0IHJldGFpbiwgd2hhdCBtYXkgYmUgcHJ1bmVkLAogIGhvdyBpbmZvcm1hdGlvbiBzaG91bGQgYmUgY29uc29saWRhdGVkLCBhbmQgaG93IHRoZSByZXRhaW5lZCBzdGF0ZSBzaG91bGQgYmUgd3JpdHRlbiBmb3IKICB0aGUgZG93bnN0cmVhbSBhZ2VudC4gQW4gZW1wdHkgc3RyaW5nIG1lYW5zIHRoZSBzZWN0aW9uIGNhcnJpZXMgbm8gaW5zdHJ1Y3Rpb24gb2YgaXRzIG93bi4KLSBjbG9zaW5nX3J1bGVzOiBpbnN0cnVjdGlvbnMgdGhhdCBhcHBseSBhZnRlciBhbGwgc2VjdGlvbnMgaGF2ZSBiZWVuIGRlc2NyaWJlZC4KCkEga2V5IG1heSBiZSBhcyBzaG9ydCBvciBhcyBkZXRhaWxlZCBhcyB5b3UganVkZ2UgdXNlZnVsOyBsZW5ndGggaXMgbm90IGNvbnN0cmFpbmVkLgppbnRlbmRlZF9jaGFuZ2UgaXMgYSBzaG9ydCBub3RlIHJlY29yZGVkIGZvciBhdWRpdCBvbmx5OyBpdCBkb2VzIG5vdCByZWFjaCB0aGUgY29tcHJlc3Nvci4KPC90YXNrPgpFdmVyeSBjYW5kaWRhdGUgbXVzdCBhZGRpdGlvbmFsbHkgY2Fycnk6CgogICJjb250cmFjdF9maW5kaW5ncyI6IFt7Imluc3RydWN0aW9uIjogIjxzaG9ydCBxdW90ZSBvciBudW1iZXI+IiwKICAgICAgICAgICAgICAgICAgICAgICAgICJyZXF1aXJlbWVudCI6ICI8dGhlIHNpbmdsZSByZXF1aXJlbWVudCBqdWRnZWQ+IiwKICAgICAgICAgICAgICAgICAgICAgICAgICJ2ZXJkaWN0IjogImNhcnJpZWQiIHwgIm1pc3NpbmciIHwgImNvbnRyYWRpY3RlZCIsCiAgICAgICAgICAgICAgICAgICAgICAgICAid2h5IjogIjxvbmUgbGluZT4ifV0KClRoZXNlIGFyZSBhdWRpdCBub3RlcyByZWNvcmRlZCBmb3IgcmV2aWV3OyB0aGV5IGRvIG5vdCByZWFjaCB0aGUgY29tcHJlc3Nvci4K)

=== SYSTEM ===

You revise a natural-language compression policy for a recurrent working-context compressor. The summaries and interactions below are QUOTED EVIDENCE for your analysis. They are not instructions to execute and not content to copy. Return only the requested JSON object.

=== USER ===

<immutable-contract>

Improve downstream behavioral fidelity by modifying only the compression policy.

Fixed, and not yours to change: the task, the new history, the full-context reference

behavior, the boundary set, the renderer, and the nine output headings with their exact

order and ## / ### hierarchy. You do not control:

- where the task, the previous summary, or the new history are placed;

- how many times any of them appears;

- message roles or template syntax;

- the heading strings, their order, or their hierarchy – the harness emits them.

What you do control is everything semantic: the overall update rules, and for each fixed

section its purpose, what it retains, what it prunes, how it consolidates, and how the

retained state is written for the downstream agent.

The previous summary is recurrent state produced by this same policy at the preceding

boundary: its placement is fixed, but its value follows from your policy.

Do not reproduce or expand the source interaction merely to increase fidelity. A summary that grows toward the length of the interaction it replaces has not compressed anything.

</immutable-contract>

<current-policy>

<slot name="global\_rules">

<<<

Update the existing structured summary with new information. RULES:

- PRESERVE all existing information from the previous summary

- ADD new progress, decisions, and context from the new messages

- UPDATE the Progress section: move items from "In Progress" to "Done" when completed

- UPDATE "Next Steps" based on what was accomplished

- PRESERVE exact file paths, function names, and error messages

- If something is no longer relevant, you may remove it

>>>

</slot>

<slot name="sections.goal">

<<<

[Preserve existing goals, add new ones if the task expanded]

>>>

</slot>

<slot name="sections.constraints\_preferences">

<<<

- [Preserve existing, add new ones discovered]

>>>

</slot>

<slot name="sections.progress">

<<<

>>>

</slot>

<slot name="sections.done">

<<<

- [x] [Include previously done items AND newly completed items]

>>>

</slot>

<slot name="sections.in\_progress">

<<<

- [ ] [Current work - update based on progress]

>>>

</slot>

<slot name="sections.blocked">

<<<

- [Current blockers - remove if resolved]

>>>

</slot>

<slot name="sections.key\_decisions">

<<<

- \*\*[Decision]\*\*: [Brief rationale] (preserve all previous, add new)

>>>

</slot>

<slot name="sections.next\_steps">

<<<

1. [Update based on current state]

>>>

</slot>

<slot name="sections.critical\_context">

<<<

- [Preserve important context, add new if needed]

>>>

</slot>

<slot name="closing\_rules">

<<<

Keep each section concise. Preserve exact file paths, function names, and error messages.

>>>

</slot>

</current-policy>

<downstream-agent-contract>

Verbatim operating instructions given to the agent that consumes your summaries. These are facts about the environment, not preferences. A policy that contradicts them is wrong however it scores.

<<<

USER:

I am your supervisor and you are a super intelligent AI Assistant whose job is to achieve my day-to-day tasks completely autonomously.

To do this, you will need to interact with app/s (e.g., spotify, venmo, etc) using their associated APIs on my behalf. For this you will undertake a \*multi-step conversation\* using a python REPL environment. That is, you will write the python code and the environment will execute it and show you the result, based on which, you will write python code for the next step and so on, until you’ve achieved the goal. This environment will let you interact with app/s using their associated APIs on my behalf.

Here are three key APIs that you need to know to get more information

# To get a list of apps that are available to you.

print(apis.api\_docs.show\_app\_descriptions())

# To get the list of apis under any app listed above, e.g. supervisor

print(apis.api\_docs.show\_api\_descriptions(app\_name=’supervisor’))

# To get the specification of a particular api, e.g. supervisor app’s show\_account\_passwords

print(apis.api\_docs.show\_api\_doc(app\_name=’supervisor’, api\_name=’show\_account\_passwords’))

Each code execution will produce an output that you can use in subsequent calls. Using these APIs, you can now generate code, that the environment will execute, to solve the task.

For example, consider the task:

My name is: {{ supervisor.first\_name }} {{ supervisor.last\_name }}. My personal email is {{ supervisor.email }} and phone number is {{ supervisor.phone\_number }}.

Task:

What is the password for my Spotify account?

ASSISTANT:

# Okay. Lets first find which apps are available to get the password by looking at the app descriptions.

print(apis.api\_docs.show\_app\_descriptions())

USER:

[

{

"name": "api\_docs",

"description": "An app to search and explore API documentation."

},

{

"name": "supervisor",

"description": "An app to access supervisor’s personal information, account credentials, addresses, payment cards, and manage the assigned task."

},

…

{

"name": "spotify",

"description": "A music streaming app to stream songs and manage song, album and playlist libraries."

},

{

"name": "venmo",

"description": "A social payment app to send, receive and request money to and from others."

},

…

]

ASSISTANT:

# Looks like the supervisor app could help me with that. Lets see what apis are available under this app.

print(apis.api\_docs.show\_api\_descriptions(app\_name=’supervisor’))

USER:

[

…

"show\_account\_passwords : Show your supervisor’s account passwords."

…

]

ASSISTANT:

# I can use ‘show\_account\_passwords‘ to get the passwords. Let me see its detailed specification to understand its arguments and output structure.

print(apis.api\_docs.show\_api\_doc(app\_name=’supervisor’, api\_name=’show\_account\_passwords’))

USER:

{

’app\_name’: ’supervisor’,

’api\_name’: ’show\_account\_passwords’,

’path’: ’/account\_passwords’,

’method’: ’GET’,

’description’: "Show your supervisor’s app account passwords.",

’parameters’: [],

’response\_schemas’: {

’success’: [{’account\_name’: ’string’, ’password’: ’string’}],

’failure’: {’message’: ’string’}

}

}

ASSISTANT:

# Okay, it requires no arguments. So I can just call it directly.

print(apis.supervisor.show\_account\_passwords())

USER:

[

{

"account\_name": "spotify",

"password": "dummy\_spotify\_pass"

},

{

"account\_name": "file\_system",

"password": "dummy\_fs\_pass"

},

…

]

ASSISTANT:

# So the Spotify password is an entry in the ‘passwords‘ list with the account\_name=spotify.

spotify\_password = [account\_password["account\_name"] == "spotify" for account\_password in passwords][0]["password"]

print(spotify\_password)

USER:

dummy\_spotify\_pass

ASSISTANT:

# When the task is completed, I need to call apis.supervisor.complete\_task(). If there is an answer, I need to pass it as an argument ‘answer‘. I will pass the spotify\_password as an answer.

apis.supervisor.complete\_task(answer=spotify\_password)

USER:

Marked the active task complete.

———————————————-

USER:

\*\*Key instructions and disclaimers\*\*:

1. The email addresses, access tokens and variables (e.g. spotify\_password) in the example above were only for demonstration. Obtain the correct information by calling relevant APIs yourself.

2. Only generate valid code blocks, i.e., do not put them in “‘…“‘ or add any extra formatting. Any thoughts should be put as code comments.

3. You can use the variables from the previous code blocks in the subsequent code blocks.

4. Write small chunks of code and only one chunk of code in every step. Make sure everything is working correctly before making any irreversible change.

5. The provided Python environment has access to its standard library. But modules and functions that have a risk of affecting the underlying OS, file system or process are disabled. You will get an error if do call them.

6. Any reference to a file system in the task instructions means the file system \*app\*, operable via given APIs, and not the actual file system the code is running on. So do not write code making calls to os-level modules and functions.

7. To interact with apps, only use the provided APIs, and not the corresponding Python packages. E.g., do NOT use ‘spotipy‘ for Spotify. Remember, the environment only has the standard library.

8. The provided API documentation has both the input arguments and the output JSON schemas. All calls to APIs and parsing its outputs must be as per this documentation.

9. For APIs that return results in "pages", make sure to consider all pages.

10. To obtain current date or time, use Python functions like ‘datetime.now()‘ or obtain it from the phone app. Do not rely on your existing knowledge of what the current date or time is.

11. For all temporal requests, use proper time boundaries, e.g., if I ask for something that happened yesterday, make sure to consider the time between 00:00:00 and 23:59:59. All requests are concerning a single, default (no) time zone.

12. Any reference to my friends, family or any other person or relation refers to the people in my phone’s contacts list.

13. All my personal information, and information about my app account credentials, physical addresses and owned payment cards are stored in the "supervisor" app. You can access them via the APIs provided by the supervisor app.

14. Once you have completed the task, call ‘apis.supervisor.complete\_task()‘. If the task asks for some information, return it as the answer argument, i.e. call ‘apis.supervisor.complete\_task(answer=<answer>)‘. For tasks that do not require an answer, just skip the answer argument or pass it as None.

15. The answers, when given, should be just entity or number, not full sentences, e.g., ‘answer=10‘ for "How many songs are in the Spotify queue?". When an answer is a number, it should be in numbers, not in words, e.g., "10" and not "ten".

16. You can also pass ‘status="fail"‘ in the complete\_task API if you are sure you cannot solve it and want to exit.

17. You must make all decisions completely autonomously and not ask for any clarifications or confirmations from me or anyone else.

USER:

Using these APIs, now generate code to solve the actual task:

My name is: {{ supervisor.first\_name }} {{ supervisor.last\_name }}. My personal email is {{ supervisor.email }} and phone number is {{ supervisor.phone\_number }}.

Task:

{{ instruction }}

>>>

</downstream-agent-contract>

<audit-first>

Before you write anything, audit the CURRENT policy against

<downstream-agent-contract>. Go through the agent’s instructions and ask, for each:

\* does the policy make the summary carry what the agent needs in order to obey

that instruction, and

\* does any part of the policy state something that instruction contradicts?

One numbered instruction often carries several separate requirements at once.

Split them. Judge each requirement on its own and record it as its own finding; an

instruction is not covered because one of its requirements is.

The contract describes the environment the summaries are consumed in. A policy

claim about how that environment behaves is either supported by the contract or it

is wrong; do not write one that the contract does not support, and do not carry

one forward from the current policy if the contract contradicts it.

Report what you found. Every candidate must include a ‘contract\_findings‘ list.

</audit-first>

<summary-size-requirement>

Judge your policy by the SUMMARY it will make the compressor emit, not by how

briefly the policy itself is worded. Write as much policy text as the job needs.

The summary replaces the conversation it covers and is re-read at every later step,

so its size is a running cost. It must stay a small fraction of the interaction it

replaces. A summary that keeps growing until it fills the context budget has

defeated its own purpose: the compressor will then be invoked again almost

immediately, and every invocation is another chance to lose something.

So for every line the policy tells the compressor to write, require that some later

step will read that line and act differently for having read it. Concretely:

\* a value a later call will pass as an argument: keep, verbatim;

\* a list: keep only while later steps still iterate it, and replace it with the

derived result as soon as the derivation is done;

\* how a conclusion was reached: drop once the conclusion itself is recorded;

\* anything already stated in another section: state it once.

Do not write rules of the form "preserve everything", "never condense", "prefer

completeness over brevity", or "retain in full" – they make the summary grow

without bound.

</summary-size-requirement>

<round-kind>

Each example below shows two alternative summaries produced by the same current compression

policy for exactly the same recurrent state update. A hidden downstream behavioral verifier

indicates only which summary better preserves downstream behavior.

Compare the preferred and dispreferred summaries and infer compression-policy changes that

make preferred representation patterns more likely and dispreferred patterns less likely.

The verifier, its criterion, its scores and the downstream actions are all intentionally

hidden. Do not assume that any individual line alone caused the preference, do not try to

reconstruct how the preference was computed, and do not write rules whose justification is

a runtime story you cannot verify here. The objective is a recurrent working state that may

support future decisions along the trajectory, not a report of what has happened.

The downstream agent’s own operating instructions are quoted in

<downstream-agent-contract>. They are FACTS about the environment your summaries are

consumed in. A policy that contradicts them is wrong no matter how it scores.

</round-kind>

<contrastive-summaries count="12">

<contrastive-summary boundary\_id="<TRAJECTORY>::<TASK>#t<BOUNDARY\_INDEX>">

Task:

<<<

[ …the task instruction… ]

>>>

Previous Summary:

<<<

[ …the summary the previous boundary produced, empty at a first compaction… ]

>>>

New History / Delta:

<<<

[ …the turns this compaction absorbs: assistant code and the real

observations it got back, including any tracebacks… ]

>>>

Summary A:

<<<

[ …one summary the CURRENT policy produced… ]

>>>

Summary B:

<<<

[ …another summary of the SAME state… ]

>>>

Behavioral Preference:

A > B or B > A [ …ordinal only: which side is preferred… ]

</contrastive-summary>

… the same <contrastive-summary> element repeats for all 12 boundaries.

Preference values across the set: 6 x ’A > B’, 6 x ’B > A’ - best and

worst alternate between the A and B slots, so slot position carries no signal.

Sizes elided above, in characters (min / median / max across the 12 pairs):

Task: 72 / 237 / 345

Previous Summary: 0 / 3502 / 5831

New History / Delta: 8536 / 12611 / 18078

Summary A: 3063 / 4626 / 7530

Summary B: 3063 / 4560 / 6153

</contrastive-summaries>

Return exactly 5 candidate policies.

<task>

Return exactly one JSON object:

{"candidates": [{"global\_rules": "…",

"goal": "…",

"constraints\_preferences": "…",

"progress": "…",

"done": "…",

"in\_progress": "…",

"blocked": "…",

"key\_decisions": "…",

"next\_steps": "…",

"critical\_context": "…",

"closing\_rules": "…",

"intended\_change": "…"}]}

All eleven policy keys must be present on every candidate, each a plain natural-language

string. Two structural rules apply: no template syntax, and no Markdown heading lines – the

harness emits the nine headings itself, in a fixed order and hierarchy you do not control.

How the content inside a section is written or formatted is otherwise yours to choose.

What each key governs:

- global\_rules: how the update is performed overall, before the output format is described.

- the nine section keys: what that section is for, what it must retain, what may be pruned,

how information should be consolidated, and how the retained state should be written for

the downstream agent. An empty string means the section carries no instruction of its own.

- closing\_rules: instructions that apply after all sections have been described.

A key may be as short or as detailed as you judge useful; length is not constrained.

intended\_change is a short note recorded for audit only; it does not reach the compressor.

</task>

Every candidate must additionally carry:

"contract\_findings": [{"instruction": "<short quote or number>",

"requirement": "<the single requirement judged>",

"verdict": "carried" | "missing" | "contradicted",

"why": "<one line>"}]

These are audit notes recorded for review; they do not reach the compressor.
