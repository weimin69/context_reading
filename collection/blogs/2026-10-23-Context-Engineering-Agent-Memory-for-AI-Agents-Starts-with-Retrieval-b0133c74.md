# Context Engineering (Agent Memory) for AI Agents Starts with Retrieval

- 来源: https://www.langchain.com/blog/context-engineering-starts-with-retrieval
- 发布日期: 2026-10-23
- 日期依据: JSON-LD datePublished
- 类型: blog
- 主题: 上下文选择、检索
- 抓取状态: article_html
- 正文来源: https://www.langchain.com/blog/context-engineering-starts-with-retrieval
- 抓取时间 UTC: 2026-10-26T09:28:02.471505+00:00

## 来源摘要 / 页面简介

Agents waste time and context on clumsy searches, oversized results and stale data. Learn the retrieval techniques LangChain's Deep Agents harness uses to get the right context in.

## 抓取正文

Deep Agents

Conceptual Guide

# Context Engineering Starts with Retrieval

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6acfb8492227373b922e7719_Screenshot%202026-10-14%20at%2010.12.17%E2%80%AFAM.png)

Jess Weng

October 23, 2026

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69ce2c533137196179bae949_Icon-7.svg)

11

min

[Go back to blog](https://www.langchain.com/blog)

[Create agents](https://www.langchain.com/blog/context-engineering-starts-with-retrieval#)

[Create agents](https://www.langchain.com/blog/context-engineering-starts-with-retrieval#)

Share

## Key Takeaways

* Agents work with a limited context window, and information retrieval breaks in three ways: inefficient searching, too much context at once, and irrelevant or stale context.
* The Deep Agents harness keeps searches small out of the box. The built-in filesystem tools search before they read: glob matches file names, grep finds matching lines, and read\_file reads a page at a time. Oversized tool results are offloaded: the full result is saved to files, but the agent gets just the path and a preview.
* For custom search tools (like RAG), use "retrieve, offload, delegate": save results to files, return the paths, and let subagents read them. The main agent only sees what's relevant.

Imagine you’re taking an open book exam: you technically have all the answers, but somehow that makes it even harder to find the *right* one.

* Where do you even start searching?
* When do you know that your sources are correct?
* How do you optimize your time so that you don’t blow all your energy on redundant searches?

Finding the right information efficiently isn’t that straightforward.

Hand an agent a question and it’s left with a similar predicament: it has a limited context window, so like us humans, it has to **retrieve** information to complete certain tasks (instead of having everything memorized). When searching, agents struggle with:

* **Inefficient searching:** every search costs tokens and time. An agent that searches clumsily (e.g. opens every file just to see what's inside, or keeps rewording the same query) can fill its context with search results before it finds anything useful.
* **Too much context at once:** one search that dumps a full data export or a dozen documents fills the context window in a single move, leaving no room for the work itself.
* **Irrelevant or stale context:** outdated or off-topic information can look just as convincing to a model as the right answer. Once it's in the context window, the agent may build on it (and the mistake will carry through every step after).

Luckily, there are several techniques at an agent’s disposal that allow it to retrieve the *correct* information. It’s the job of an [agent harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness) to apply these techniques strategically to get the model **the right context at the right time** for the given task.

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada6def0e658ad27256aef7_harness-embedded%20(1).png)

This blog covers the challenges with agent retrieval (finding and pulling in only the information necessary for the task at hand), the techniques at our disposal to combat them, and how to keep these in mind when designing an agent harness (using [LangChain’s Deep Agents](https://www.langchain.com/deep-agents) harness as an example).

For more on how to manage context once it's *in* the context window, check out this [blog on Context Engineering](https://www.langchain.com/blog/context-engineering-deep-agents-remember).

## Our example: a competitive analysis agent

Let’s see how this can be applied in a real-world use case: a competitive analysis agent. Every Monday, an agent researches hundreds of competitors and writes a report in the team's template. It needs to:

* Find last week's notes on Company A
* Look up a specific revenue number in a huge market data export
* Search a news archive for anything new

Each of these is a different kind of retrieval and therefore faces different problems. We've built our agent using the [Deep Agents harness](https://docs.langchain.com/oss/python/deepagents/overview) so there are a few techniques that we can apply out of the box to minimize these problems.

## 1. Inefficient searching

Our agent has to find three things for each competitor. If each one takes a dozen tries (opening files just to see what's inside, or rewording a search because the source uses different words), its context window fills up with failed searches before it even writes a word of the report.

Therefore, the best search is the one the agent doesn't have to repeat, and that means using the right tool for each job.

### Start with the built-in filesystem tools

One of the most common ways for an agent to search through information is with a filesystem. However, if our agent opens every file to see what's inside, it's searching very inefficiently: each file it reads lands in its context window, so it can fill up just from looking.

A better approach is to check **names** and **keywords** first (the way you'd scan a book's index instead of reading every page during an open-book exam). Two common filesystem tools do exactly that:

* `glob` finds files by name pattern. For example, `**/company-a*.md` finds last week's notes on Company A.
* `grep` searches inside files without loading them into the context window. It matches literal text and can return the matching files, the matching lines, or counts.

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada6e01fd3bbf8a61b345c3_d1-scan-first.png)

Every deep agent comes with [these tools built in](https://docs.langchain.com/oss/python/deepagents/tools#built-in-harness-tools), alongside `ls`, `read_file`, `write_file` and `edit_file`. The same tools work no matter where the files live (agent state, local disk, a persistent store or a sandbox), because they all go through the agent's [backend](https://docs.langchain.com/oss/python/deepagents/backends).

### Add a retrieval tool when keywords aren't enough

[Grep](https://reference.langchain.com/python/deepagents/backends/protocol/BackendProtocol/grep) is great when you know what words to look for, but it only matches the *exact* text you give it. That's a problem for the third job in our example: searching a news archive for anything new. If our agent greps for "Company A funding," it will miss an article titled "Company A closes $50M Series B," even though that's exactly what it's looking for.

To search by meaning instead of exact words (semantic search), you add a [**retrieval tool**](https://docs.langchain.com/oss/python/deepagents/retrieval) backed by a [vector store](https://docs.langchain.com/oss/python/integrations/vectorstores). A retrieval tool is any tool the agent can call to fetch information: it takes a query, looks it up in some data source, and returns what it finds (the closest matches).

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada6e1017deb689203baeb8_d2-grep-vs-semantic%20(1).png)

How a retrieval tool matches depends on the data source behind it. Backed by a vector store, it matches by meaning, but a retrieval tool can sit on top of other data sources too:

* A SQL database, for structured lookups (like sales figures or customer records)
* A search API (for fresh information from the web)
* An [MCP server](https://docs.langchain.com/oss/python/deepagents/tools#mcp-tools) (for tools someone else already built, like a documentation search)

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada6e26b85ddacbcd3d660f_d3-retrieval-tool%20(1).png)

For a deeper look at how semantic search works, see [LangChain’s guide](https://docs.langchain.com/oss/python/langchain/knowledge-base).

### Letting the agent decide when to search

Many retrieval setups search once at the start, then answer. That works for an FAQ bot ([2-step RAG](https://docs.langchain.com/oss/python/deepagents/retrieval#2-step-rag)), but not for our agent. Let’s say halfway through researching Company C, it finds an article about a product launch it didn't know about, and now it needs that product's pricing (which it couldn't have known to look for at the start). With only one search, the report goes out without it.

Research agents need [agentic retrieval](https://docs.langchain.com/oss/python/deepagents/retrieval#agentic-rag) (instead of 2-step RAG): the agent decides when to search, what to search for, and whether it needs more. With Deep Agents, it already works this way by default: the agent runs in a loop and can call any tool as many times as it needs.

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada6e34e5e14ab012badab9_d4-rag-vs-agentic%20(1).png)

### Package your search know-how as a skill

To help the agent search well, you can package your search know-how as a [skill](https://docs.langchain.com/oss/python/deepagents/skills): a set of instructions for a specific task (like which index to use, how to phrase queries and how to format citations).

The agent only sees each skill's name and a short description until a task calls for it; then it loads the full instructions, so niche know-how is there when it's needed without taking up context the rest of the time (a technique called [progressive disclosure](https://docs.langchain.com/oss/python/deepagents/skills#how-skills-work)). Here is a [video explanation](https://www.youtube.com/watch?v=bv1qgkbWhms).

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada779317deb68920402eca_skills-progressive-disclosure-light%20(1).gif)

Progressive Disclosure (animated)

## 2. Too much context at once

However, despite optimizing the search process, even the *right* search can return too much. Our agent needs just one number from the market data export (Company B's quarterly revenue), but loading all 40,000 rows to find it would fill its context window. Our retrieval tool has the same problem: if it returns every news article straight to the model, four results per search across five companies adds up fast.

### Reading large files one page at a time

The filesystem tools are built to return as little as possible. `read_file` reads a file one page at a time (100 lines by default), and the agent can set an offset (which line to start from) and a limit (how many lines to read) to jump to the part it needs. So to find Company B's revenue, the agent greps for it, then reads just the few lines around the match.

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada717e600aacfde1b63063_p1-paged-reading.png)

### Let the harness offload oversized results

Sometimes a tool returns more than expected anyway. When a tool result is too large (over about 20,000 tokens), the harness saves it to a file under /large\_tool\_results/ and gives the agent the path plus a short preview (the first and last few lines). The agent can then read back just the parts it needs with `read_file`'s offset and limit.

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada718d18a99d15b175faf2_p2-offload-results%20(1).png)

### Have your retrieval tool return file paths

You can apply the same idea to your own retrieval tool instead of waiting for the size limit: have it write each result to a file and return only the paths. This is the first part of a pattern called “retrieve, offload, delegate” ([LangChain’s RAG guide](https://docs.langchain.com/oss/python/deepagents/rag) walks through it in full).

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada719604267bfb9db5b667_p3-search-paths.png)

Here's a simplified retrieval tool. It runs the search, saves each result as a file in the agent's [backend](https://docs.langchain.com/oss/python/deepagents/backends#statebackend), and hands back only the list of file paths:

```
backend = StateBackend()

@tool
def search_news(query: str) -> str:
    """Search the news archive and save each result to a file."""
    docs = vector_store.similarity_search(query, k=4)
    files = [(f"/retrieved/result_{i}.md", doc.page_content.encode()) for i, doc in enumerate(docs)]
    backend.upload_files(files)
    return "Saved results to: " + ", ".join(path for path, _ in files)
```

Now the main agent sees four short paths instead of four full articles.

## 3. Irrelevant or stale context

Small results don't help if they're the *wrong* results. Any of those four files could be about a different company with a similar name, or a story from two years ago. Off-topic or outdated text looks just as convincing to a model as the right answer, so the goal is to keep it out of the main agent's context entirely.

### Let subagents filter the results

However, the main agent *still* has to read those files to find out which ones matter (and every off-topic article it opens does land in its context). That's where the “delegate” part of the “retrieve, offload, delegate” pattern comes in: a [subagent](https://docs.langchain.com/oss/python/deepagents/subagents) reads each retrieved file and returns only the key facts.

1. Define the subagent: the description tells the main agent when to use it (one file per call), and the system prompt tells the subagent what to do with that file.

```
chunk_analyst = {
		"name": "chunk-analyst",
		"description": "Analyze one retrieved file. Pass the question and a single path under /retrieved/.",
		"system_prompt": "Use read_file to read the assigned file. Return the key facts and the source URL.",
}
```

2. Give the main agent the retrieval tool and the subagent. Pass the same backend you used in `search_news`, so the subagent can read the files the tool saved.

```
agent = create_deep_agent(
		model=model,
		tools=[search_news],
		backend=backend,  # same instance, so read_file can see /retrieved/
		subagents=[chunk_analyst],
)
```

Now the flow is:

1. **Search**: the main agent calls `search_news` and gets back four paths.
2. **Delegate**: it sends each path to a chunk-analyst subagent, and they can run in parallel.
3. **Synthesize**: each analyst returns a short summary with its source. The main agent combines them and searches again if something is missing.

![__wf_reserved_inherit](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ada7251706d82f584744c9d_s1-subagents-filter%20(1).png)

Raw results go to files, the noisy reading happens in subagents with their own context windows, and the main agent only ever sees conclusions. Anything off-topic stays in the subagent's context, and the main agent's context window stays clear!

### Pull from up-to-date sources

Filtering does keep off-topic results out, but it can't fix results that are out of date. Our competitive analysis agent runs every Monday, so last month's index won't catch this week's news.

A solution: a search API or MCP server could give the agent current information (instead of whatever was indexed months ago). If your data has dates, filtering by date in the retrieval tool would also keep old results out.

### Be careful with retrieved text

On the flip side, relevant current results can cause problems! Since retrieved text is data, not instructions, anything you retrieve could contain a [prompt injection](https://docs.langchain.com/oss/python/deepagents/rag#security-considerations) (and no prompt or delimiter strategy fully prevents this). Make sure to validate outputs: check that answers cite the sources you expect and that claims match them.

## Retrieval strategies to keep in mind

Here's what to look out for (regardless of whatever harness you're building on):

* **Use the most efficient tool that works.** If you know the words, grep beats an embedding lookup. Save semantic search for when you actually need it.
* **Page instead of loading**. Read large files in pieces instead of all at once.
* **Return pointers instead of payloads.** Write retrieved content to files and hand the agent the paths.
* **Delegate the reading**. Let subagents read and summarize so the main agent only sees conclusions.
* **Verify grounding**. Check answers against what was retrieved, and treat retrieved text as untrusted.

## Try it

```
uv add deepagents
```

Want to learn more from a live instructor? I'll be covering this on November 9th: Register [HERE](https://events.langchain.com/register/agent-memory-102-context-retrieval-storage/)!

‍

**Retrieval is only half of the story: how information finds its way to the agent. How do we manage the agent’s context window as it starts to build up information over time?**

*To learn more check out:*

* Blog on [context engineering with Deep Agents](https://www.langchain.com/blog/context-engineering-deep-agents-remember)
* [Deep Agents course](https://academy.langchain.com/courses/foundation-introduction-to-deepagents) on LangChain Academy (free, online and self-paced).

### Related content

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6add442530f2704b9d5e03af_HVZbWoXb0AAOzqm.png)

Deep Agents

#### The five components of building a "company harness"

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6a056ea05f3880a1361b47cf_Harrison.avif)

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6a56f3a3a4a725f72a70441f_caspar-b.jpeg)

Harrison Chase

Caspar Broekhuizen

October 24, 2026

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

6

min

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ac6d12e05f73fc9690266a8_dark-74%20characters%20max.png)

Deep Agents

Conceptual Guide

#### Context Engineering: How Deep Agents Remember

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6acfb8492227373b922e7719_Screenshot%202026-10-14%20at%2010.12.17%E2%80%AFAM.png)

Jess Weng

October 14, 2026

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

10

min

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ac91132385fb9bbe1cb53b1_mda-reactions-blog-cover-navy-1200x675.png)

Deep Agents

Tutorials & How-Tos

#### Build great out-of-the-box user experiences with Managed Deep Agents

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6ab416d4dafca27a7246c1d0_Nathan%20Drezner.jpg)

Nathan Drezner

October 9, 2026

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

5

min

![](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69ce01ea562f8cc223cabf25_Frame%202147254328.svg)

Thank you! Your submission has been received!

Oops! Something went wrong while submitting the form.

### See what your agent is really doing

LangSmith, our agent engineering platform, helps developers debug every agent decision, eval changes, and deploy in one click.

[Try LangSmith](https://smith.langchain.com/)[Get a demo](https://www.langchain.com/contact-sales)
