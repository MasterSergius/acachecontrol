import aiohttp
import cachecontrol

from .cache import AsyncCache
from .request_context_manager import RequestContextManager


class AsyncCacheControl:
    def __init__(self, cache=AsyncCache()):
        self.cache = cache
        self._async_session = aiohttp.ClientSession()

    def request(self, method, url, **params):
        return RequestContextManager(self.cache, self._async_session.request(method, url, **params))
        #return self._async_session.request(method, url, **params)

    def get(self, url, *, allow_redirects=True, **kwargs):
        return self._async_session.get(url, allow_redirects=allow_redirects, **kwargs)

    def post(self, url, *, data, **kwargs):
        return self._async_session.post(url, data=data, **kwargs)

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
