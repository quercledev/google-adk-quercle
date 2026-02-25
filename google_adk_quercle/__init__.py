"""Google ADK tools for Quercle web search and URL fetching."""

from google_adk_quercle.tools import (
    # Async tools (recommended for Google ADK)
    async_quercle_extract,
    async_quercle_fetch,
    async_quercle_raw_fetch,
    async_quercle_raw_search,
    async_quercle_search,
    create_async_quercle_extract,
    create_async_quercle_fetch,
    create_async_quercle_raw_fetch,
    create_async_quercle_raw_search,
    create_async_quercle_search,
    # Sync tools
    create_quercle_extract,
    create_quercle_fetch,
    create_quercle_raw_fetch,
    create_quercle_raw_search,
    create_quercle_search,
    get_async_quercle_tools,
    get_quercle_tools,
    quercle_extract,
    quercle_fetch,
    quercle_raw_fetch,
    quercle_raw_search,
    quercle_search,
)

__version__ = "1.0.0"

__all__ = [
    # Async tools (recommended for Google ADK)
    "async_quercle_extract",
    "async_quercle_fetch",
    "async_quercle_raw_fetch",
    "async_quercle_raw_search",
    "async_quercle_search",
    "create_async_quercle_extract",
    "create_async_quercle_fetch",
    "create_async_quercle_raw_fetch",
    "create_async_quercle_raw_search",
    "create_async_quercle_search",
    "get_async_quercle_tools",
    # Sync tools
    "quercle_extract",
    "quercle_fetch",
    "quercle_raw_fetch",
    "quercle_raw_search",
    "quercle_search",
    "create_quercle_extract",
    "create_quercle_fetch",
    "create_quercle_raw_fetch",
    "create_quercle_raw_search",
    "create_quercle_search",
    "get_quercle_tools",
]
