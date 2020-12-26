import aiohttp

from .cache import AsyncCache
from .request_context_manager import RequestContextManager


class AsyncCacheControl:
    def __init__(self, request_context_manager=RequestContextManager,
                 cache=AsyncCache()):
        self._request_context_manager = request_context_manager
        self.cache = cache
        self._async_session = aiohttp.ClientSession()

    def request(self, method, url, **params):
        return self._request_context_manager(self._async_session,
                                             self.cache,
                                             method,
                                             url,
                                             **params)

    def get(self, url, *, allow_redirects=True, **params):
        return self.request('GET',
                            url,
                            allow_redirects=allow_redirects,
                            **params)

    def post(self, url, *, data, **params):
        return self.request('POST', url, data=data, **params)

    def clear_cache(self):
        self.cache.clear()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._async_session.close()
