"""Google ADK tools for Quercle web search and URL fetching."""

from __future__ import annotations

import json
from typing import Callable, Coroutine

from quercle import (
    AsyncQuercleClient,
    QuercleClient,
    tool_metadata,
)
from quercle.models import ExtractBodyFormat, RawFetchBodyFormat, RawSearchBodyFormat

# Build docstrings from quercle SDK descriptions (DRY)
_FETCH_DOCSTRING = f"""{tool_metadata["fetch"]["description"]}

    Args:
        url: {tool_metadata["fetch"]["parameters"]["url"]}
        prompt: {tool_metadata["fetch"]["parameters"]["prompt"]}

    Returns:
        The AI-processed result from the fetched content.
    """

_SEARCH_DOCSTRING = f"""{tool_metadata["search"]["description"]}

    Args:
        query: {tool_metadata["search"]["parameters"]["query"]}
        allowed_domains: {tool_metadata["search"]["parameters"]["allowed_domains"]}
        blocked_domains: {tool_metadata["search"]["parameters"]["blocked_domains"]}

    Returns:
        AI-synthesized answer based on search results.
    """

_RAW_FETCH_DOCSTRING = f"""{tool_metadata["raw_fetch"]["description"]}

    Args:
        url: {tool_metadata["raw_fetch"]["parameters"]["url"]}
        format: {tool_metadata["raw_fetch"]["parameters"]["format"]}
        use_safeguard: {tool_metadata["raw_fetch"]["parameters"]["use_safeguard"]}

    Returns:
        Raw page content in the requested format.
    """

_RAW_SEARCH_DOCSTRING = f"""{tool_metadata["raw_search"]["description"]}

    Args:
        query: {tool_metadata["raw_search"]["parameters"]["query"]}
        format: {tool_metadata["raw_search"]["parameters"]["format"]}
        use_safeguard: {tool_metadata["raw_search"]["parameters"]["use_safeguard"]}

    Returns:
        Raw search results in the requested format.
    """

_EXTRACT_DOCSTRING = f"""{tool_metadata["extract"]["description"]}

    Args:
        url: {tool_metadata["extract"]["parameters"]["url"]}
        query: {tool_metadata["extract"]["parameters"]["query"]}
        format: {tool_metadata["extract"]["parameters"]["format"]}
        use_safeguard: {tool_metadata["extract"]["parameters"]["use_safeguard"]}

    Returns:
        Extracted content chunks relevant to the query.
    """

# Module-level default clients (lazy initialized)
_default_client: QuercleClient | None = None
_default_async_client: AsyncQuercleClient | None = None


def _get_default_client() -> QuercleClient:
    """Get or create the default sync Quercle client."""
    global _default_client
    if _default_client is None:
        _default_client = QuercleClient()
    return _default_client


def _get_default_async_client() -> AsyncQuercleClient:
    """Get or create the default async Quercle client."""
    global _default_async_client
    if _default_async_client is None:
        _default_async_client = AsyncQuercleClient()
    return _default_async_client


def _format_result(response) -> str:
    """Format a response result as a string, JSON-encoding non-string results."""
    return response.result if isinstance(response.result, str) else json.dumps(response.result)


# =============================================================================
# Sync Tools
# =============================================================================


def quercle_fetch(url: str, prompt: str) -> str:
    return _get_default_client().fetch(url=url, prompt=prompt).result


quercle_fetch.__doc__ = _FETCH_DOCSTRING


def quercle_search(
    query: str,
    allowed_domains: list[str] | None = None,
    blocked_domains: list[str] | None = None,
) -> str:
    return _get_default_client().search(
        query,
        allowed_domains=allowed_domains,
        blocked_domains=blocked_domains,
    ).result


quercle_search.__doc__ = _SEARCH_DOCSTRING


def quercle_raw_fetch(
    url: str,
    format: RawFetchBodyFormat | None = None,
    use_safeguard: bool | None = None,
) -> str:
    return _format_result(
        _get_default_client().raw_fetch(url, format=format, use_safeguard=use_safeguard)
    )


quercle_raw_fetch.__doc__ = _RAW_FETCH_DOCSTRING


def quercle_raw_search(
    query: str,
    format: RawSearchBodyFormat | None = None,
    use_safeguard: bool | None = None,
) -> str:
    return _format_result(
        _get_default_client().raw_search(query, format=format, use_safeguard=use_safeguard)
    )


quercle_raw_search.__doc__ = _RAW_SEARCH_DOCSTRING


def quercle_extract(
    url: str,
    query: str,
    format: ExtractBodyFormat | None = None,
    use_safeguard: bool | None = None,
) -> str:
    return _format_result(
        _get_default_client().extract(url, query, format=format, use_safeguard=use_safeguard)
    )


quercle_extract.__doc__ = _EXTRACT_DOCSTRING


# =============================================================================
# Async Tools
# =============================================================================


async def async_quercle_fetch(url: str, prompt: str) -> str:
    return (await _get_default_async_client().fetch(url=url, prompt=prompt)).result


async_quercle_fetch.__doc__ = _FETCH_DOCSTRING


async def async_quercle_search(
    query: str,
    allowed_domains: list[str] | None = None,
    blocked_domains: list[str] | None = None,
) -> str:
    return (await _get_default_async_client().search(
        query,
        allowed_domains=allowed_domains,
        blocked_domains=blocked_domains,
    )).result


async_quercle_search.__doc__ = _SEARCH_DOCSTRING


async def async_quercle_raw_fetch(
    url: str,
    format: RawFetchBodyFormat | None = None,
    use_safeguard: bool | None = None,
) -> str:
    return _format_result(
        await _get_default_async_client().raw_fetch(url, format=format, use_safeguard=use_safeguard)
    )


async_quercle_raw_fetch.__doc__ = _RAW_FETCH_DOCSTRING


async def async_quercle_raw_search(
    query: str,
    format: RawSearchBodyFormat | None = None,
    use_safeguard: bool | None = None,
) -> str:
    return _format_result(
        await _get_default_async_client().raw_search(
            query, format=format, use_safeguard=use_safeguard,
        )
    )


async_quercle_raw_search.__doc__ = _RAW_SEARCH_DOCSTRING


async def async_quercle_extract(
    url: str,
    query: str,
    format: ExtractBodyFormat | None = None,
    use_safeguard: bool | None = None,
) -> str:
    return _format_result(
        await _get_default_async_client().extract(
            url, query, format=format, use_safeguard=use_safeguard,
        )
    )


async_quercle_extract.__doc__ = _EXTRACT_DOCSTRING


# =============================================================================
# Sync Factory Functions
# =============================================================================


def create_quercle_fetch(
    api_key: str | None = None,
    timeout: float = 120.0,
) -> Callable[[str, str], str]:
    """Create a quercle_fetch tool with custom configuration.

    Use this factory function when you need to customize the API key or timeout
    settings for the fetch tool.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds. Defaults to 120.0.

    Returns:
        A quercle_fetch function configured with the specified settings.
    """
    client = QuercleClient(api_key=api_key)

    def quercle_fetch(url: str, prompt: str) -> str:
        return client.fetch(url=url, prompt=prompt, timeout=timeout).result

    quercle_fetch.__doc__ = _FETCH_DOCSTRING
    return quercle_fetch


def create_quercle_search(
    api_key: str | None = None,
    timeout: float = 120.0,
) -> Callable[[str, list[str] | None, list[str] | None], str]:
    """Create a quercle_search tool with custom configuration.

    Use this factory function when you need to customize the API key or timeout
    settings for the search tool.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds. Defaults to 120.0.

    Returns:
        A quercle_search function configured with the specified settings.
    """
    client = QuercleClient(api_key=api_key)

    def quercle_search(
        query: str,
        allowed_domains: list[str] | None = None,
        blocked_domains: list[str] | None = None,
    ) -> str:
        return client.search(
            query,
            allowed_domains=allowed_domains,
            blocked_domains=blocked_domains,
            timeout=timeout,
        ).result

    quercle_search.__doc__ = _SEARCH_DOCSTRING
    return quercle_search


def create_quercle_raw_fetch(
    api_key: str | None = None,
    timeout: float = 120.0,
) -> Callable[[str, RawFetchBodyFormat | None, bool | None], str]:
    """Create a quercle_raw_fetch tool with custom configuration.

    Use this factory function when you need to customize the API key or timeout
    settings for the raw fetch tool.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds. Defaults to 120.0.

    Returns:
        A quercle_raw_fetch function configured with the specified settings.
    """
    client = QuercleClient(api_key=api_key)

    def quercle_raw_fetch(
        url: str,
        format: RawFetchBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        return _format_result(
            client.raw_fetch(url, format=format, use_safeguard=use_safeguard, timeout=timeout)
        )

    quercle_raw_fetch.__doc__ = _RAW_FETCH_DOCSTRING
    return quercle_raw_fetch


def create_quercle_raw_search(
    api_key: str | None = None,
    timeout: float = 120.0,
) -> Callable[[str, RawSearchBodyFormat | None, bool | None], str]:
    """Create a quercle_raw_search tool with custom configuration.

    Use this factory function when you need to customize the API key or timeout
    settings for the raw search tool.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds. Defaults to 120.0.

    Returns:
        A quercle_raw_search function configured with the specified settings.
    """
    client = QuercleClient(api_key=api_key)

    def quercle_raw_search(
        query: str,
        format: RawSearchBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        return _format_result(
            client.raw_search(query, format=format, use_safeguard=use_safeguard, timeout=timeout)
        )

    quercle_raw_search.__doc__ = _RAW_SEARCH_DOCSTRING
    return quercle_raw_search


def create_quercle_extract(
    api_key: str | None = None,
    timeout: float = 120.0,
) -> Callable[[str, str, ExtractBodyFormat | None, bool | None], str]:
    """Create a quercle_extract tool with custom configuration.

    Use this factory function when you need to customize the API key or timeout
    settings for the extract tool.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds. Defaults to 120.0.

    Returns:
        A quercle_extract function configured with the specified settings.
    """
    client = QuercleClient(api_key=api_key)

    def quercle_extract(
        url: str,
        query: str,
        format: ExtractBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        return _format_result(
            client.extract(url, query, format=format, use_safeguard=use_safeguard, timeout=timeout)
        )

    quercle_extract.__doc__ = _EXTRACT_DOCSTRING
    return quercle_extract


def get_quercle_tools(
    api_key: str | None = None,
    timeout: float = 120.0,
) -> list[Callable]:
    """Get all sync Quercle tools configured with the specified settings.

    This is a convenience function that returns all Quercle tools
    configured with the same settings. All tools share a single client.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds. Defaults to 120.0.

    Returns:
        A list containing all sync Quercle tool functions.
    """
    client = QuercleClient(api_key=api_key)

    def _fetch(url: str, prompt: str) -> str:
        return client.fetch(url=url, prompt=prompt, timeout=timeout).result

    def _search(
        query: str,
        allowed_domains: list[str] | None = None,
        blocked_domains: list[str] | None = None,
    ) -> str:
        return client.search(
            query,
            allowed_domains=allowed_domains,
            blocked_domains=blocked_domains,
            timeout=timeout,
        ).result

    def _raw_fetch(
        url: str,
        format: RawFetchBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        return _format_result(
            client.raw_fetch(
                url, format=format, use_safeguard=use_safeguard,
                timeout=timeout,
            )
        )

    def _raw_search(
        query: str,
        format: RawSearchBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        return _format_result(
            client.raw_search(
                query, format=format, use_safeguard=use_safeguard,
                timeout=timeout,
            )
        )

    def _extract(
        url: str,
        query: str,
        format: ExtractBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        return _format_result(
            client.extract(
                url, query, format=format, use_safeguard=use_safeguard,
                timeout=timeout,
            )
        )

    _fetch.__doc__ = _FETCH_DOCSTRING
    _search.__doc__ = _SEARCH_DOCSTRING
    _raw_fetch.__doc__ = _RAW_FETCH_DOCSTRING
    _raw_search.__doc__ = _RAW_SEARCH_DOCSTRING
    _extract.__doc__ = _EXTRACT_DOCSTRING

    return [_fetch, _search, _raw_fetch, _raw_search, _extract]


# =============================================================================
# Async Factory Functions
# =============================================================================


def create_async_quercle_fetch(
    api_key: str | None = None,
    timeout: float = 120.0,
) -> Callable[[str, str], Coroutine[None, None, str]]:
    """Create an async quercle_fetch tool with custom configuration.

    Use this factory function when you need to customize the API key or timeout
    settings for the async fetch tool.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds. Defaults to 120.0.

    Returns:
        An async quercle_fetch function configured with the specified settings.
    """
    client = AsyncQuercleClient(api_key=api_key)

    async def async_quercle_fetch(url: str, prompt: str) -> str:
        return (await client.fetch(url=url, prompt=prompt, timeout=timeout)).result

    async_quercle_fetch.__doc__ = _FETCH_DOCSTRING
    return async_quercle_fetch


def create_async_quercle_search(
    api_key: str | None = None,
    timeout: float = 120.0,
) -> Callable[[str, list[str] | None, list[str] | None], Coroutine[None, None, str]]:
    """Create an async quercle_search tool with custom configuration.

    Use this factory function when you need to customize the API key or timeout
    settings for the async search tool.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds. Defaults to 120.0.

    Returns:
        An async quercle_search function configured with the specified settings.
    """
    client = AsyncQuercleClient(api_key=api_key)

    async def async_quercle_search(
        query: str,
        allowed_domains: list[str] | None = None,
        blocked_domains: list[str] | None = None,
    ) -> str:
        return (await client.search(
            query,
            allowed_domains=allowed_domains,
            blocked_domains=blocked_domains,
            timeout=timeout,
        )).result

    async_quercle_search.__doc__ = _SEARCH_DOCSTRING
    return async_quercle_search


def create_async_quercle_raw_fetch(
    api_key: str | None = None,
    timeout: float = 120.0,
) -> Callable[[str, RawFetchBodyFormat | None, bool | None], Coroutine[None, None, str]]:
    """Create an async quercle_raw_fetch tool with custom configuration.

    Use this factory function when you need to customize the API key or timeout
    settings for the async raw fetch tool.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds. Defaults to 120.0.

    Returns:
        An async quercle_raw_fetch function configured with the specified settings.
    """
    client = AsyncQuercleClient(api_key=api_key)

    async def async_quercle_raw_fetch(
        url: str,
        format: RawFetchBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        return _format_result(
            await client.raw_fetch(url, format=format, use_safeguard=use_safeguard, timeout=timeout)
        )

    async_quercle_raw_fetch.__doc__ = _RAW_FETCH_DOCSTRING
    return async_quercle_raw_fetch


def create_async_quercle_raw_search(
    api_key: str | None = None,
    timeout: float = 120.0,
) -> Callable[[str, RawSearchBodyFormat | None, bool | None], Coroutine[None, None, str]]:
    """Create an async quercle_raw_search tool with custom configuration.

    Use this factory function when you need to customize the API key or timeout
    settings for the async raw search tool.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds. Defaults to 120.0.

    Returns:
        An async quercle_raw_search function configured with the specified settings.
    """
    client = AsyncQuercleClient(api_key=api_key)

    async def async_quercle_raw_search(
        query: str,
        format: RawSearchBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        return _format_result(
            await client.raw_search(
                query, format=format, use_safeguard=use_safeguard,
                timeout=timeout,
            )
        )

    async_quercle_raw_search.__doc__ = _RAW_SEARCH_DOCSTRING
    return async_quercle_raw_search


def create_async_quercle_extract(
    api_key: str | None = None,
    timeout: float = 120.0,
) -> Callable[[str, str, ExtractBodyFormat | None, bool | None], Coroutine[None, None, str]]:
    """Create an async quercle_extract tool with custom configuration.

    Use this factory function when you need to customize the API key or timeout
    settings for the async extract tool.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds. Defaults to 120.0.

    Returns:
        An async quercle_extract function configured with the specified settings.
    """
    client = AsyncQuercleClient(api_key=api_key)

    async def async_quercle_extract(
        url: str,
        query: str,
        format: ExtractBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        return _format_result(
            await client.extract(
                url, query, format=format, use_safeguard=use_safeguard,
                timeout=timeout,
            )
        )

    async_quercle_extract.__doc__ = _EXTRACT_DOCSTRING
    return async_quercle_extract


def get_async_quercle_tools(
    api_key: str | None = None,
    timeout: float = 120.0,
) -> list[Callable]:
    """Get all async Quercle tools configured with the specified settings.

    This is a convenience function that returns all async Quercle tools
    configured with the same settings. All tools share a single client.
    Use these for optimal performance with Google ADK's async runners.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds. Defaults to 120.0.

    Returns:
        A list containing all async Quercle tool functions.
    """
    client = AsyncQuercleClient(api_key=api_key)

    async def _fetch(url: str, prompt: str) -> str:
        return (await client.fetch(
            url=url, prompt=prompt, timeout=timeout,
        )).result

    async def _search(
        query: str,
        allowed_domains: list[str] | None = None,
        blocked_domains: list[str] | None = None,
    ) -> str:
        return (await client.search(
            query,
            allowed_domains=allowed_domains,
            blocked_domains=blocked_domains,
            timeout=timeout,
        )).result

    async def _raw_fetch(
        url: str,
        format: RawFetchBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        return _format_result(
            await client.raw_fetch(
                url, format=format, use_safeguard=use_safeguard,
                timeout=timeout,
            )
        )

    async def _raw_search(
        query: str,
        format: RawSearchBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        return _format_result(
            await client.raw_search(
                query, format=format, use_safeguard=use_safeguard,
                timeout=timeout,
            )
        )

    async def _extract(
        url: str,
        query: str,
        format: ExtractBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        return _format_result(
            await client.extract(
                url, query, format=format, use_safeguard=use_safeguard,
                timeout=timeout,
            )
        )

    _fetch.__doc__ = _FETCH_DOCSTRING
    _search.__doc__ = _SEARCH_DOCSTRING
    _raw_fetch.__doc__ = _RAW_FETCH_DOCSTRING
    _raw_search.__doc__ = _RAW_SEARCH_DOCSTRING
    _extract.__doc__ = _EXTRACT_DOCSTRING

    return [_fetch, _search, _raw_fetch, _raw_search, _extract]
