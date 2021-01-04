import pytest

from acachecontrol import AsyncCacheControl
from acachecontrol.cache import AsyncCache


class CacheObserver(AsyncCache):
    def __init__(self):
        super().__init__()
        self.add_calls = []
        self.get_calls = []

    def add(self, key, value, headers):
        super().add(key, value, headers)
        self.add_calls.append((key, value, headers))

    def get(self, key):
        value = self.cache.get(self._make_key_hashable(key))["value"]
        self.get_calls.append(key)
        return value


@pytest.mark.asyncio
async def test_request():
    async with AsyncCacheControl() as cached_sess:
        async with cached_sess.request("GET", "http://example.com") as resp:
            resp_text = await resp.text()
            assert "Example Domain" in resp_text


@pytest.mark.asyncio
async def test_hit_cache():
    cache_observer = CacheObserver()
    async with AsyncCacheControl(cache=cache_observer) as cached_sess:
        async with cached_sess.request("GET", "http://example.com") as resp:
            resp_text = await resp.text()
            assert "Example Domain" in resp_text

        async with cached_sess.request("GET", "http://example.com") as resp:
            resp_text = await resp.text()
            assert "Example Domain" in resp_text

        assert ("GET", "http://example.com", {}) in cache_observer.get_calls


@pytest.mark.asyncio
async def test_hit_cache_json():
    url = "https://my-json-server.typicode.com/typicode/demo/posts"
    expected_json = [
        {"id": 1, "title": "Post 1"},
        {"id": 2, "title": "Post 2"},
        {"id": 3, "title": "Post 3"},
    ]
    cache_observer = CacheObserver()
    async with AsyncCacheControl(cache=cache_observer) as cached_sess:
        async with cached_sess.request("GET", url) as resp:
            resp_json = await resp.json()
            assert resp_json == expected_json

        async with cached_sess.request("GET", url) as resp:
            resp_json = await resp.json()
            assert resp_json == expected_json

        assert ("GET", url, {}) in cache_observer.get_calls
