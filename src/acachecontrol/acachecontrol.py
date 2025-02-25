"""
Copyright 2021 - Present Serhii Buniak

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import aiohttp

from .cache import AsyncCache
from .request_context_manager import RequestContextManager


class AsyncCacheControl:
    def __init__(
        self,
        cache: AsyncCache = AsyncCache(),
        request_context_manager_cls=RequestContextManager,
    ):
        self._request_context_manager_cls = request_context_manager_cls
        self.cache = cache
        self._async_client_session = aiohttp.ClientSession()

    def request(self, method, url, **params):
        return self._request_context_manager_cls(
            self._async_client_session, self.cache, method, url, **params
        )

    def head(self, url, allow_redirects=True, **params):
        return self.request(
            "HEAD", url, allow_redirects=allow_redirects, **params
        )

    def get(self, url, allow_redirects=True, **params):
        return self.request(
            "GET", url, allow_redirects=allow_redirects, **params
        )

    def post(self, url, data, **params):
        return self.request("POST", url, data=data, **params)

    def put(self, url, data, **params):
        return self.request("PUT", url, data=data, **params)

    def patch(self, url, data, **params):
        return self.request("PATCH", url, data=data, **params)

    def delete(self, url, **params):
        return self.request("DELETE", url, **params)

    def clear_cache(self):
        self.cache.clear_cache()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._async_client_session.close()
