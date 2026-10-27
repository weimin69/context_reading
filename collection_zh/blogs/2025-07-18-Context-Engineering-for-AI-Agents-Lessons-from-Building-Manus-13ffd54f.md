> 本文为简体中文机器翻译，使用 Google Translate 公开接口并统一技术术语，尚未经逐句人工校对。代码、链接和公式按原文保留；实验数字及技术结论请对照原文。
> [查看本地英文原文](../../collection/blogs/2025-07-18-Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus-13ffd54f.md) · [原始来源](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)

# AI 智能体上下文工程：构建 Manus 的经验

- 来源: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus- 发布日期: 2025-07-18- 日期依据: curated source date (search verified)- 类型: blog- 主题: KV-cache、文件系统记忆、可恢复压缩- 抓取状态: article_html- 正文来源: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus- 抓取时间 UTC: 2026-10-26T09:26:45.571740+00:00

## 阅读提示（人工整理）

关注缓存稳定性、外置文件、任务清单和错误统计在生产智能体中的作用。

## 来源摘要/页面简介

这篇文章分享了 Manus 通过我们自己的“SGD”得出的局部最优值。如果您正在构建自己的人工智能智能体，我们希望这些原则可以帮助您更快地收敛。

## 抓取正文（中文翻译）

[Manus 2.0 简介](http://manus.im/blog/introducing-manus-2-0)

[产品](https://manus.im/blog?kind=PRODUCT)·7 月 18 日，星期五

# AI 智能体的上下文工程：构建 Manus 的经验教训

![](https://files.manuscdn.com/assets/dashboard/materials/2025/07/18/eaafe9e6a174b29458c314ccc225dbdd39a7c9d66e60786235165d9aba23f578.webp)

2025/7/18 --纪一超‘巅峰’

在 [Manus](https://manus.im/app) 项目一开始，我和我的团队面临一个关键决定：我们应该使用开源基础训练端到端智能体模型，还是在前沿模型的[上下文学习](https://arxiv.org/abs/2301.00234) 能力之上构建一个智能体？

回到我进入 NLP 的第一个十年，我们并没有这样的奢侈选择。在 [BERT](https://arxiv.org/abs/1810.04805) 的遥远日子里（是的，已经过去了七年），模型必须经过微调和评估才能转移到新任务。尽管模型与当今的法学硕士相比很小，但该过程每次迭代通常需要数周时间。对于快速移动的应用程序，尤其是 PMF 之前的应用程序，如此缓慢的反馈循环会破坏交易。这是我上一次创业的惨痛教训，我从头开始训练模型以进行[开放信息提取](https://en.wikipedia.org/wiki/Open_information_extraction)和语义搜索。然后是[GPT-3](https://arxiv.org/abs/2005.14165)和[Flan-T5](https://arxiv.org/abs/2210.11416)，我的内部模型一夜之间变得无关紧要。讽刺的是，这些相同的模型标志着情境学习的开始——以及一条全新的前进道路。

这个来之不易的教训让他做出了明确的选择：马努斯将把赌注押在上下文工程上。这使我们能够在数小时而不是数周内完成改进，并使我们的产品与底层模型保持正交：如果模型进展是不断上涨的潮流，我们希望 Manus 成为船，而不是粘在海底的柱子。

尽管如此，上下文工程却被证明并不是一件简单的事情。这是一门实验科学，我们已经重建了智能体框架四次，每次都是在发现更好的方式来塑造上下文之后。我们亲切地将这种架构搜索、快速摆弄和经验猜测的手动过程称为“随机研究生下降”。它并不优雅，但很有效。

这篇文章分享了我们通过自己的“SGD”得出的局部最优值。如果您正在构建自己的人工智能智能体，我希望这些原则可以帮助您更快地收敛。

### 围绕 KV 缓存进行设计

如果我必须只选择一个指标，我认为 KV 缓存命中率是生产阶段 AI 智能体最重要的指标。它直接影响延迟和成本。为了理解其中的原因，我们来看看[典型智能体](https://arxiv.org/abs/2210.03629)是如何运作的：

收到用户输入后，智能体将通过一系列工具使用来完成任务。在每次迭代中，模型根据当前上下文从预定义的操作空间中选择一个操作。然后在环境（例如 Manus 的虚拟机沙箱）中执行该操作以产生观察结果。操作和观察被附加到上下文中，形成下一次迭代的输入。这个循环一直持续到任务完成。

正如您可以想象的那样，上下文随着每一步而增长，而输出（通常是结构化函数调用）仍然相对较短。与聊天机器人相比，这使得智能体中的预填充和解码之间的比率高度倾斜。例如，在 Manus 中，平均输入与输出词元比率约为 100:1。

幸运的是，具有相同前缀的上下文可以利用 [KV-cache](https://medium.com/@joaolages/kv-caching-explained-276520203249)，这大大减少了首次词元时间 (TTFT) 和推理成本 - 无论您是使用自托管模型还是调用推理 API。我们谈论的并不是小额节省：例如，对于 Claude Sonnet，缓存的输入词元成本为 0.30 美元/MTok，而未缓存的输入词元成本为 3 美元/MTok，相差 10 倍。

![](https://d1oupeiobkpcny.cloudfront.net/user_upload_by_module/markdown/310708716691272617/OhdKxGRSXCcuqOvz.png)

﻿

从上下文工程的角度来看，提高KV缓存命中率涉及几个关键实践：

1.保持提示符前缀稳定。由于 LLM 的[自回归](https://en.wikipedia.org/wiki/Autoregressive_model)性质，即使是单个词元差异也可能使该词元之后的缓存失效。一个常见的错误是在系统提示符的开头包含时间戳（尤其是精确到秒的时间戳）。当然，它可以让模型告诉您当前时间，但它也会降低您的缓存命中率。

2.使您的上下文仅可附加。避免修改以前的行动或观察。确保您的序列化是确定性的。许多编程语言和库在序列化 JSON 对象时不保证稳定的键顺序，这可能会悄悄破坏缓存。

3.在需要时显式标记缓存断点。某些模型提供程序或推理框架不支持自动增量前缀缓存，而是需要在上下文中手动插入缓存断点。分配这些时，请考虑潜在的缓存过期，并至少确保断点包括系统提示的结尾。

此外，如果您使用 [vLLM](https://github.com/vllm-project/vllm) 等框架进行自托管模型，请确保启用 [前缀/提示缓存](https://docs.vllm.ai/en/stable/design/v1/prefix_caching.html)，并且您正在使用会话 ID 等技术在分布式工作人员之间一致地路由请求。

### 面膜，请勿摘除

随着您的智能体拥有更多功能，其操作空间自然会变得更加复杂 - 简而言之，工具的数量会呈爆炸式增长。最近[MCP](https://modelcontextprotocol.io/introduction)的流行只会火上浇油。如果您允许用户配置工具，请相信我：有人将不可避免地将数百种神秘工具插入您精心策划的操作空间中。因此，模型更有可能选择错误的操作或采取低效的路径。简而言之，你的全副武装的特工会变得更加愚蠢。

自然的反应是设计一个动态动作空间——也许使用类似 [RAG](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) 的东西按需加载工具。我们在马努斯也尝试过。但我们的实验提出了一个明确的规则：除非绝对必要，否则避免在迭代中动态添加或删除工具。造成这种情况的主要原因有两个：

1.在大多数LLM中，工具定义在序列化后位于上下文的前面附近，通常在系统提示符之前或之后。因此，任何更改都会使所有后续操作和观察的 KV 缓存失效。

2.当以前的操作和观察仍然引用当前上下文中不再定义的工具时，模型会变得混乱。如果没有[约束解码](https://platform.openai.com/docs/guides/structured-outputs)，这通常会导致模式违规或幻觉行为。

为了解决这个问题，同时仍然改进操作选择，Manus 使用上下文感知的[状态机](https://en.wikipedia.org/wiki/Finite-state_machine) 来管理工具可用性。它不是删除工具，而是在解码期间屏蔽词元逻辑，以防止（或强制）基于当前上下文选择某些操作。

![](https://d1oupeiobkpcny.cloudfront.net/user_upload_by_module/markdown/310708716691272617/cWxINCvUfrmlbvfV.png)

﻿

在实践中，大多数模型提供程序和推理框架都支持某种形式的响应预填充，这允许您在不修改工具定义的情况下约束操作空间。函数调用一般有三种模式（以NousResearch的[Hermes格式](https://github.com/NousResearch/Hermes-Function-Calling)为例）：

•自动——模型可以选择是否调用函数。通过仅预填回复前缀来实现：<|im\_start|>assistant

•必需——模型必须调用函数，但选择不受限制。通过预填充工具调用词元来实现：<|im\_start|>assistant<tool\_call>

• 指定——模型必须调用特定子集中的函数。通过预填充到函数名称的开头来实现：<|im\_start|>assistant<tool\_call>{"name":“browser\_

使用此功能，我们通过直接屏蔽 词元 logits 来限制操作选择。例如，当用户提供新输入时，Manus 必须立即回复而不是采取操作。我们还特意设计了具有一致前缀的操作名称，例如，所有与浏览器相关的工具都以 browser\_, 开头，命令行工具以 shell\_. 开头。这使我们能够轻松强制智能体仅在给定状态下从一组工具中进行选择，而不使用有状态 logits 处理器。

这些设计有助于确保 Manus 智能体循环保持稳定——即使在模型驱动的架构下也是如此。

### 使用文件系统作为上下文

现代前沿法学硕士现在提供 128K 词元或更多的上下文窗口。但在现实世界的智能体场景中，这通常是不够的，有时甚至是一种负担。常见的痛点有以下三个：

1.观察结果可能很大，尤其是当智能体与网页或 PDF 等非结构化数据交互时。突破上下文限制很容易。

2.模型性能往往会在超过一定上下文长度后下降，即使窗口在技术上支持它。

3.即使使用前缀缓存，长输入也很昂贵。您仍然需要支付传输和预填充每个词元的费用。

为了解决这个问题，许多智能体系统实施上下文截断或压缩策略。但过于激进的压缩不可避免地会导致信息丢失。这个问题是根本性的：智能体本质上必须根据所有先前状态来预测下一步行动，而您无法可靠地预测十步后哪些观察可能会变得至关重要。从逻辑的角度来看，任何不可逆的压缩都会带来风险。

这就是为什么我们将文件系统视为 Manus 中的最终上下文：大小不受限制，本质上是持久的，并且可以由智能体本身直接操作。该模型学习按需写入和读取文件——文件系统不仅用作存储，还用作结构化的外部化内存。

![](https://d1oupeiobkpcny.cloudfront.net/user_upload_by_module/markdown/310708716691272617/sBITCOxGnHNUPHTD.png)

﻿

我们的压缩策略始终设计为可恢复的。例如，只要保留 URL，就可以从上下文中删除网页的内容；如果文档的路径在沙箱中仍然可用，则可以省略文档的内容。这使得 Manus 能够缩短上下文长度，而不会永久丢失信息。

在开发此功能时，我发现自己在想象状态空间模型 (SSM) 在智能体环境中如何有效工作。与 Transformers 不同，SSM 缺乏充分的关注，并且与远程向后依赖作斗争。但如果他们能够掌握基于文件的记忆——将长期状态外化，而不是将其保存在上下文中——那么他们的速度和效率可能会解锁一类新的智能体。 Agentic SSM 可能是[神经图灵机](https://arxiv.org/abs/1410.5401)的真正继承者。

### 通过背诵控制注意力

如果您使用过 Manus，您可能会注意到一些奇怪的事情：在处理复杂任务时，它往往会创建一个 todo.md 文件，并随着任务的进展逐步更新它，检查已完成的项目。

这不仅仅是可爱的行为——这是一种故意操纵注意力的机制。

![](https://d1oupeiobkpcny.cloudfront.net/user_upload_by_module/markdown/310708716691272617/OYpTzfPZaBeeWFOx.png)

﻿

Manus 中的一项典型任务平均需要大约 50 次工具调用。这是一个很长的循环，而且由于 Manus 依赖法学硕士进行决策，因此很容易偏离主题或忘记早期的目标，尤其是在较长的背景或复杂的任务中。

通过不断重写待办事项列表，马努斯将其目标背诵到上下文的末尾。这将全局计划推入模型最近的注意力范围内，避免“迷失在中间”的问题并减少目标不一致。实际上，它使用自然语言将自己的注意力集中在任务目标上，而不需要特殊的架构更改。

### 保留错误的内容

智能体会犯错误。这不是一个错误——这是现实。语言模型产生幻觉、环境返回错误、外部工具行为不当以及意外的边缘情况始终会出现。在多步骤任务中，失败也不例外。它是循环的一部分。

然而，一个常见的冲动是隐藏这些错误：清理跟踪，重试操作，或重置模型的状态并将其留给神奇的“[温度](https://arxiv.org/abs/2405.00492)”。这感觉更安全、更可控。但这是有代价的：清除失败就会消除证据。如果没有证据，该模型就无法适应。

![](https://d1oupeiobkpcny.cloudfront.net/user_upload_by_module/markdown/310708716691272617/dBjZlVbKJVhjgQuF.png)

﻿

根据我们的经验，改善智能体行为的最有效方法之一看似简单：在上下文中留下错误的转弯。当模型看到失败的操作以及由此产生的观察或堆栈跟踪时，它会隐式更新其内部信念。这使其先验不再采取类似的行动，从而减少了重复相同错误的机会。事实上，我们认为错误恢复是真正智能体行为的最清晰指标之一。然而，它在大多数学术工作和公共基准中的代表性仍然不足，这些基准通常关注理想条件下任务的成功。

### 不要被枪杀

[少镜头提示](https://www.promptingguide.ai/techniques/fewshot)是提高LLM输出的常用技术。但在智能体系统中，它可能会以微妙的方式适得其反。

语言模型是极好的模仿者；他们模仿情境中的行为模式。如果您的上下文充满了类似的过去的动作观察对，则模型将倾向于遵循该模式，即使它不再是最佳的。

这在涉及重复决策或行动的任务中可能是危险的。例如，当使用 Manus 帮助审核一批 20 份简历时，智能体经常会陷入一种节奏——仅仅因为在上下文中看到的内容而重复类似的操作。这会导致漂移、过度概括，有时甚至产生幻觉。

![](https://d1oupeiobkpcny.cloudfront.net/user_upload_by_module/markdown/310708716691272617/IIyBBdwwuMDJUnUc.png)

﻿

解决办法是增加多样性。马努斯在行动和观察中引入了少量的结构化变化——不同的序列化模板、替代措辞、顺序或格式中的微小噪音。这种受控的随机性有助于打破模式并调整模型的注意力。换句话说，不要让自己陷入墨守成规的境地。你的上下文越统一，你的智能体就会变得越脆弱。

### 结论

上下文工程仍然是一门新兴科学，但对于智能体系统来说，它已经是必不可少的了。模型可能会变得更强、更快、更便宜，但任何原始能力都无法取代对内存、环境和反馈的需求。您塑造上下文的方式最终决定了智能体的行为方式：运行速度、恢复效果以及扩展程度。

在 Manus，我们通过反复重写、死胡同以及对数百万用户的实际测试吸取了这些教训。我们在这里分享的内容都不是普遍真理，但这些都是对我们有用的模式。如果它们可以帮助您避免哪怕是一次痛苦的迭代，那么这篇文章就完成了它的任务。

智能体式的未来将一次构建一个环境。精心设计它们。

### 下载桌面和移动应用程序

随时随地访问 Manus。

[macOS](https://download.manus.im/Manus-Setup-2.0.4.dmg)[Windows](https://apps.microsoft.com/detail/9phv7m7v4s5l)[iOS](https://manus.go.link/eyNGY)[Android](https://manus.go.link/eyNGY)

![下载 Manus 桌面版和移动版应用程序](https://files.manuscdn.com/webapp/_next/static/media/app-download.1xk9ndtmj8t91.webp)

## 更少的结构，更多的智能。

### 产品

[定价](https://manus.im/pricing)[Web应用程序](https://manus.im/features/webapp)[AI设计](https://manus.im/tools/ai-design)[AI幻灯片](https://manus.im/tools/nano-banana-pro-slides)[AI图像生成器](https://manus.im/tools/ai-image-generator)[AI音乐生成器](https://manus.im/tools/ai-music-generator)[视频](https://manus.im/features/video)[广泛研究](https://manus.im/features/wide-research)[Slack集成](https://manus.im/integrations/slack)[所有型号](https://manus.im/models)[更多功能](https://manus.im/features)

### 资源

[下载](https://manus.im/download)[博客](https://manus.im/blog)[文档](https://manus.im/docs)[更新](https://manus.im/updates)[帮助中心](https://help.manus.im/en)[信任中心](https://trust.manus.im/)[API](https://open.manus.ai/docs)[团队计划](https://manus.im/team)[初创公司](https://manus.im/startups)[剧本](https://manus.im/playbook)[品牌资产](https://manus.im/brand)

### 社区

[活动](https://manus.im/events)[研究员](https://manus.im/fellows)

### 比较

[VS ChatGPT](https://manus.im/compare/vs-chatgpt)[VS 可爱](https://manus.im/compare/lovable)[VS Replit](https://manus.im/compare/manus-vs-replit)

### 下载

[移动应用程序](https://manus.go.link/eyNGY)[桌面应用程序](https://manus.im/desktop)我的浏览器

### 商业

[团队计划](https://manus.im/team)[SSO](https://help.manus.im/en/articles/12807937-where-can-i-enable-subscribe-to-a-single-sign-on-sso-subscription-for-manus-team)[API](https://open.manus.ai/docs)

### 公司

[关于我们](https://manus.im/about)[工作机会](https://careers.manus.im/)[媒体](mailto:media@manus.ai)[服务条款](https://manus.im/terms)[隐私政策](https://manus.im/privacy)

© 2026 马努斯人工智能

[العربية](https://manus.im/ar/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[印尼语](https://manus.im/id/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[捷克](https://manus.im/cs/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[德语](https://manus.im/de/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[西班牙语](https://manus.im/es/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[西班牙语（拉丁美洲）](https://manus.im/es-419/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[繁體中文](https://manus.im/zh-tw/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[繁體中文（香港）](https://manus.im/zh-hk/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[法语](https://manus.im/fr/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[한국어](https://manus.im/ko/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[हिन्दी](https://manus.im/hi/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[意大利语](https://manus.im/it/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[简体中文](https://manus.im/zh-cn/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[荷兰](https://manus.im/nl/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[日本語](https://manus.im/ja/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[波兰](https://manus.im/pl/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[葡萄牙语（巴西）](https://manus.im/pt-br/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[葡萄牙语（葡萄牙）](https://manus.im/pt-pt/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[ไทย](https://manus.im/th/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[越南](https://manus.im/vi/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[土耳其](https://manus.im/tr/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)[Українська](https://manus.im/uk/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)

