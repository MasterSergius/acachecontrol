class RequestContextManager:
    """Wrapper around _RequestContextManager from aiohttp."""

    def __init__(self, session, cache, method, url, **params):
        self.cache = cache
        self.request = session.request(method, url, **params)
        self.cache_key = (method, url, params)
        self.in_request = False

    async def __aenter__(self):
        await self.cache.register_new_key(self.cache_key)
        if self.cache_key not in self.cache:
            self.in_request = await self.request.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.in_request:
            return await self.request.__aexit__(exc_type, exc_val, exc_tb)

    async def text(self):
        if self.cache_key not in self.cache:
            self.response = await self.in_request.text()
            self.cache.add(self.cache_key, self.response)
        else:
            self.response = self.cache.get(self.cache_key)
        return self.response
