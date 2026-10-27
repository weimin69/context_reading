# Agent 上下文管理论文与博客资料库

此目录包含可运行的 Python 爬虫和实际下载的 Markdown 资料。先打开 [资料索引](collection/INDEX.md)。

中文版入口：[中文资料索引](collection_zh/INDEX.md)。中文译文独立保存在 `collection_zh/`，英文原文仍在 `collection/`。

## 中文翻译

`translate.py` 将所有已保存资料翻译为简体中文，不用摘要替代全文。原始条目只有摘要时也只翻译该摘要。当前使用 Google Translate 公开接口生成机器译文，未经逐句人工校对；公式、代码、URL、作者和来源元数据保持原文，技术术语做统一处理。公开接口并非具有可用性保证的付费 API，可能限流或发生变化。

```bash
.venv/bin/python translate.py --workers 3
```

脚本按段落拆分长文、检查受保护内容是否完整，并在 `.translation_cache/` 缓存分段译文。中断后可再次运行续译；每篇完成后才写入中文 Markdown，并同步更新中文索引和完成记录。`collection_zh/manifest.json` 记录每篇的源文件校验值、分段数和完成状态，各篇旁的 `.translation.json` 保存对应元数据。

机器翻译可能误译专有名词或复杂句子。实验数字、公式和技术结论应对照每篇顶部链接的英文原文。中文化不会修复原始抓取页面已有的公式或版式损失。

## 收集范围

本次收集区间为 2024-10-26 至 **2026-10-26** ，包含上下文工程、上下文选择与隔离、压缩与摘要、文件系统外置记忆、长期记忆、经验反思、记忆评估和工具输出管理。种子来源经过网络检索筛选，优先使用论文原站和作者／机构技术博客；这是主题资料集，并非穷尽全部论文的系统性综述。

论文日期采用 arXiv **首次提交 **v1**，不因近期修** 订而把旧论文归为新论文。博客优先采用网页元数据日期，缺失时使用已核实的种子日期；每篇记录日期依据。无法核实日期的页面不会混入正式资料。

## 文件

- `crawl.py`：抓取、日期过滤、HTML 转 Markdown、去重、断点续跑和索引生成。
- `sources.json`：人工筛选的种子链接和主题，可继续添加。
- `requirements.txt`：Python 依赖；已安装在当前目录 `.venv` 中。
- `collection/INDEX.md`：按日期排序的阅读入口，包含抓取失败及跳过原因。
- `collection/papers/`：论文 HTML 正文，无法取得正文时仅保存摘要并明确标注。
- `collection/blogs/`：博客正文。
- `collection/manifest.json`：来源、日期依据、状态、正文长度和抓取异常等机器可读记录。

## 运行

需要 Python 3.10+ 和可访问来源网站的网络环境，无需模型 API 或 API Key。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python crawl.py --start 2024-10-26 --end 2026-10-26
```

不传日期时，默认按运行当天向前两年。默认跳过已有成功条目并重试失败条目；`--refresh` 会重新抓取并覆盖本爬虫对应的 Markdown 文件。使用 `--output another_collection` 可保存另一份资料。

```bash
# 尝试从 arXiv API 扩展 30 篇最新论文（如果该接口允许机器人访问）
.venv/bin/python crawl.py --discover 30

# 指定较慢的站点请求间隔
.venv/bin/python crawl.py --delay 3
```

自动发现依赖 arXiv API 的可用性与 robots.txt 许可；如被拒绝会记录原因，并继续抓取种子来源，不绕过站点限制。自动发现论文会标注“待人工精读”，它们只有关键词相关性筛选，不代表人工推荐。博客发现目前通过维护 `sources.json` 完成。

## 阅读说明

`full_text_html` 表示取得论文 HTML 正文，`article_html` 表示取得博客页面正文，`abstract_only` 表示仅有摘要。正文保留来源语言，不自动翻译；少量中文阅读提示是人工整理，并与原文分开。

Markdown 是自动提取版本，公式、图示和复杂表格可能不完整，博客页面偶有相关内容残留。严格核查实验数字、公式和论文版本时，请打开原始来源。爬虫不下载 PDF、不绕过登录／付费限制，预印本不代表已经同行评审。原文版权归作者和原站所有。
