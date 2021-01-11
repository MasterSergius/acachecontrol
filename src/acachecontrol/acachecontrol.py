import aiohttp

from .cache import AsyncCache
from .request_context_manager import RequestContextManager


class AsyncCacheControl:
    def __init__(
        self,
        request_context_manager_cls=RequestContextManager,
        cache=AsyncCache(),
    ):
        self._request_context_manager_cls = request_context_manager_cls
        self.cache = cache
        self._async_client_session = aiohttp.ClientSession()

    def _request(self, method, url, **params):
        return self._request_context_manager_cls(
            self._async_client_session, self.cache, method, url, **params
        )

    def head(self, url, allow_redirects=True, **params):
        return self._request(
            "HEAD", url, allow_redirects=allow_redirects, **params
        )

    def get(self, url, allow_redirects=True, **params):
        return self._request(
            "GET", url, allow_redirects=allow_redirects, **params
        )

    def post(self, url, data, **params):
        return self._request("POST", url, data=data, **params)

    def put(self, url, data, **params):
        return self._request("PUT", url, data=data, **params)

    def patch(self, url, data, **params):
        return self._request("PATCH", url, data=data, **params)

    def delete(self, url, **params):
        return self._request("DELETE", url, **params)

    def clear_cache(self):
        self.cache.clear_cache()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._async_client_session.close()
