class RequestContextManager:
    """Wrapper around _RequestContextManager from aiohttp."""
    def __init__(self, cache, request):
        self.cache = cache
        self.request = request
        self.in_request = False

    async def __aenter__(self):
        # TODO: look into cache
        # self.response = self.cache.get_from_cache(request)
        # if not self.response, perform regular request
        self.in_request = await self.request.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.request.__aexit__(exc_type, exc_val, exc_tb)

    async def text(self):
        # TODO: add response to cache, get cache key from self.request
        # should be smth like the following: self.cache.add_to_cache(request, response)
        # direct return self.response if it exists in cache
        self.response = await self.in_request.text()
        return self.response
