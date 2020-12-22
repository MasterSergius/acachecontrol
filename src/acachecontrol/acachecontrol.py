import aiohttp
import cachecontrol

from .cache import AsyncCache
from .request_context_manager import RequestContextManager


class AsyncCacheControl:
    def __init__(self, cache=AsyncCache()):
        self.cache = cache
        self._async_session = aiohttp.ClientSession()

    def request(self, method, url, **params):
        return RequestContextManager(self._async_session,
                                     self.cache,
                                     method,
                                     url,
                                     **params)

    def get(self, url, *, allow_redirects=True, **params):
        return self.request('GET', url, allow_redirects=allow_redirects, **params)

    def post(self, url, *, data, **params):
        return self.request('POST', url, data=data, **params)

    def _cache_request(self, request, response):
        pass

    def _get_response_from_cache(self, request):
        pass

    def _remove_from_cache(self, request):
        pass

    def clear_cache(self):
        self.cache.clear()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._async_session.close()
