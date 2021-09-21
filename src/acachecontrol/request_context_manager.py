from .constants import DEFAULT_WAIT_TIMEOUT


class RequestContextManager:
    """Wrapper around _RequestContextManager from aiohttp."""

    def __init__(self, client_session, cache, method, url, **params):
        self.cache = cache
        self.method = method
        self.url = url
        self.params = params
        self.client_session = client_session
        self.timeout = params.get("timeout", DEFAULT_WAIT_TIMEOUT)
        # TODO: consider canonify url
        self.key = (method, url)
        self.response = None
        self.headers = None

    async def __aenter__(self):
        await self.cache.register_new_key(self.key, self.timeout)

        if not self.cache.has_valid_entry(self.key):
            async with self.client_session.request(
                self.method, self.url, **self.params
            ) as response:
                await response.read()
                self.response = response
        else:
            self.response = self.cache.get(self.key)

        self.headers = self.response.headers
        self.status = self.response.status
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.response = None
        self.headers = None

    async def text(self):
        """Return response in plain str format."""
        if not self.cache.has_valid_entry(self.key):
            response = await self.response.text()
            self.cache.add(self.key, self.response, self.headers)
        else:
            response = await self.cache.get(self.key).text()
        return response

    async def json(self):
        """Return response in json format."""
        if not self.cache.has_valid_entry(self.key):
            response = await self.response.json()
            self.cache.add(self.key, self.response, self.headers)
        else:
            response = await self.cache.get(self.key).json()
        return response
