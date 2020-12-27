class RequestContextManager:
    """Wrapper around _RequestContextManager from aiohttp."""

    def __init__(self, client_session, cache, method, url, **params):
        self.cache = cache
        self.method = method
        self.url = url
        self.params = params
        self.client_session = client_session
        self.cache_key = (method, url, params)
        self.response = None
        self.headers = None

    async def __aenter__(self):
        await self.cache.register_new_key(self.cache_key)

        if self.cache_key not in self.cache:
            async with self.client_session.request(
                self.method, self.url, **self.params
            ) as response:
                await response.read()
                self.response = response
                self.headers = response.headers
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.response = None
        self.headers = None

    async def text(self):
        if self.cache_key not in self.cache:
            response = await self.response.text()
            self.cache.add(self.cache_key, self.response)
        else:
            response = await self.cache.get(self.cache_key).text()
        return response

    async def json(self):
        if self.cache_key not in self.cache:
            response = await self.response.json()
            self.cache.add(self.cache_key, self.response)
        else:
            response = await self.cache.get(self.cache_key).json()
        return response
