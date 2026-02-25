# google-adk-quercle

Quercle web search, fetch, and extraction tools for [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/).

## Installation

```bash
uv add google-adk-quercle
# or
pip install google-adk-quercle
```

## Setup

Set your API key as an environment variable:

```bash
export QUERCLE_API_KEY=qk_...
```

Get your API key at [quercle.dev](https://quercle.dev).

## Quick Start

```python
from google.adk.agents import Agent
from google_adk_quercle import get_async_quercle_tools

agent = Agent(
    model="gemini-2.0-flash",
    name="research_agent",
    instruction="You are a helpful research assistant. Use the search and fetch "
    "tools to find accurate, up-to-date information.",
    tools=get_async_quercle_tools(),
)
```

## Tools

| Tool | Description |
|---|---|
| `quercle_search` | AI-synthesized web search with optional domain filtering |
| `quercle_fetch` | Fetch a URL and analyze the content with AI |
| `quercle_raw_search` | Raw web search results (no AI synthesis) |
| `quercle_raw_fetch` | Raw URL content (no AI analysis) |
| `quercle_extract` | Extract content relevant to a query from a URL |

## Direct Tool Usage

### Sync

```python
from google_adk_quercle import (
    quercle_search,
    quercle_fetch,
    quercle_raw_search,
    quercle_raw_fetch,
    quercle_extract,
)

# AI-synthesized search
result = quercle_search(query="best practices for building AI agents")
print(result)

# Search with domain filtering
result = quercle_search(
    query="Python documentation",
    allowed_domains=["docs.python.org"],
)
print(result)

# Fetch and analyze a page with AI
result = quercle_fetch(
    url="https://en.wikipedia.org/wiki/Python_(programming_language)",
    prompt="Summarize the key features of Python",
)
print(result)

# Raw search results (no AI synthesis)
result = quercle_raw_search(query="Python web frameworks", format="markdown")
print(result)

# Raw page content
result = quercle_raw_fetch(url="https://example.com", format="markdown")
print(result)

# Extract relevant content from a page
result = quercle_extract(
    url="https://en.wikipedia.org/wiki/Python_(programming_language)",
    query="What are Python's main features?",
    format="markdown",
)
print(result)
```

### Async

```python
import asyncio
from google_adk_quercle import (
    async_quercle_search,
    async_quercle_fetch,
    async_quercle_raw_search,
    async_quercle_raw_fetch,
    async_quercle_extract,
)

async def main():
    result = await async_quercle_search(query="latest AI agent frameworks")
    print(result)

    result = await async_quercle_fetch(
        url="https://en.wikipedia.org/wiki/TypeScript",
        prompt="What is TypeScript?",
    )
    print(result)

    result = await async_quercle_raw_search(query="Python web frameworks")
    print(result)

    result = await async_quercle_raw_fetch(url="https://example.com")
    print(result)

    result = await async_quercle_extract(
        url="https://en.wikipedia.org/wiki/TypeScript",
        query="TypeScript type system",
    )
    print(result)

asyncio.run(main())
```

### Custom API Key

```python
from google_adk_quercle import (
    create_quercle_search,
    create_quercle_fetch,
    create_quercle_raw_search,
    create_quercle_raw_fetch,
    create_quercle_extract,
)

search = create_quercle_search(api_key="qk_...")
fetch = create_quercle_fetch(api_key="qk_...")
raw_search = create_quercle_raw_search(api_key="qk_...")
raw_fetch = create_quercle_raw_fetch(api_key="qk_...")
extract = create_quercle_extract(api_key="qk_...")
```

## Agentic Usage

### With Google ADK Agent

```python
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google_adk_quercle import get_async_quercle_tools

agent = Agent(
    model="gemini-2.0-flash",
    name="research_agent",
    instruction="You are a research assistant. Search the web to find "
    "accurate, up-to-date information and analyze relevant pages.",
    tools=get_async_quercle_tools(),
)

session_service = InMemorySessionService()
runner = Runner(agent=agent, app_name="research_app", session_service=session_service)

session = await session_service.create_session(app_name="research_app", user_id="user1")

response = await runner.run_async(
    session_id=session.id,
    user_id="user1",
    new_message=types.Content(
        role="user",
        parts=[types.Part(text="Research the latest developments in WebAssembly")],
    ),
)

for event in response:
    if event.content and event.content.parts:
        print(event.content.parts[0].text)
```

### Sync Agent (with sync tools)

```python
from google_adk_quercle import get_quercle_tools

agent = Agent(
    model="gemini-2.0-flash",
    name="sync_agent",
    instruction="You are a helpful assistant.",
    tools=get_quercle_tools(),
)
```

## Configuration

| Parameter | Default | Description |
|---|---|---|
| `api_key` | `QUERCLE_API_KEY` env var | Your Quercle API key |
| `timeout` | `120.0` | Request timeout in seconds |

## API Reference

### Module-Level Tools (use `QUERCLE_API_KEY` env var)

| Function | Description |
|---|---|
| `quercle_search(query, ...)` | AI-synthesized web search |
| `quercle_fetch(url, prompt)` | Fetch URL + AI analysis |
| `quercle_raw_search(query, ...)` | Raw web search results |
| `quercle_raw_fetch(url, ...)` | Raw URL content |
| `quercle_extract(url, query, ...)` | Extract relevant content from URL |
| `async_quercle_search(query, ...)` | Async AI-synthesized web search |
| `async_quercle_fetch(url, prompt)` | Async fetch URL + AI analysis |
| `async_quercle_raw_search(query, ...)` | Async raw web search results |
| `async_quercle_raw_fetch(url, ...)` | Async raw URL content |
| `async_quercle_extract(url, query, ...)` | Async extract relevant content from URL |

### Factory Functions (custom API key / timeout)

| Function | Description |
|---|---|
| `create_quercle_search(...)` | Create a sync search tool |
| `create_quercle_fetch(...)` | Create a sync fetch tool |
| `create_quercle_raw_search(...)` | Create a sync raw search tool |
| `create_quercle_raw_fetch(...)` | Create a sync raw fetch tool |
| `create_quercle_extract(...)` | Create a sync extract tool |
| `create_async_quercle_search(...)` | Create an async search tool |
| `create_async_quercle_fetch(...)` | Create an async fetch tool |
| `create_async_quercle_raw_search(...)` | Create an async raw search tool |
| `create_async_quercle_raw_fetch(...)` | Create an async raw fetch tool |
| `create_async_quercle_extract(...)` | Create an async extract tool |
| `get_quercle_tools(...)` | Get all 5 sync tools as a list |
| `get_async_quercle_tools(...)` | Get all 5 async tools as a list |

## License

MIT
