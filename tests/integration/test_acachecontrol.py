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
        value = self.cache.get(key)["value"]
        self.get_calls.append(key)
        return value


@pytest.mark.asyncio
async def test_request():
    async with AsyncCacheControl() as cached_sess:
        async with cached_sess.get("http://example.com") as resp:
            resp_text = await resp.text()
            assert resp.status == 200
            assert "Example Domain" in resp_text


@pytest.mark.asyncio
async def test_head():
    async with AsyncCacheControl() as cached_sess:
        async with cached_sess.head("http://example.com") as resp:
            resp_text = await resp.text()
            assert resp.status == 200
            assert resp_text == ""
            assert resp.headers.get("Cache-Control") == "max-age=604800"


@pytest.mark.asyncio
async def test_get():
    async with AsyncCacheControl() as cached_sess:
        async with cached_sess.get("http://example.com") as resp:
            resp_text = await resp.text()
            assert resp.status == 200
            assert "Example Domain" in resp_text


@pytest.mark.asyncio
async def test_hit_cache():
    cache_observer = CacheObserver()
    async with AsyncCacheControl(cache=cache_observer) as cached_sess:
        async with cached_sess.get("http://example.com") as resp:
            resp_text = await resp.text()
            assert resp.status == 200
            assert "Example Domain" in resp_text

        async with cached_sess.get("http://example.com") as resp:
            resp_text = await resp.text()
            assert resp.status == 200
            assert "Example Domain" in resp_text

        assert ("GET", "http://example.com") in cache_observer.get_calls


@pytest.mark.asyncio
async def test_no_hit_cache():
    # response from given url contains 'no-cache' directive
    url = "https://my-json-server.typicode.com/typicode/demo/posts"
    expected_json = [
        {"id": 1, "title": "Post 1"},
        {"id": 2, "title": "Post 2"},
        {"id": 3, "title": "Post 3"},
    ]
    cache_observer = CacheObserver()
    async with AsyncCacheControl(cache=cache_observer) as cached_sess:
        async with cached_sess.get(url) as resp:
            resp_json = await resp.json()
            assert resp.status == 200
            assert resp_json == expected_json

        async with cached_sess.get(url) as resp:
            resp_json = await resp.json()
            assert resp.status == 200
            assert resp_json == expected_json

        assert len(cache_observer.get_calls) == 0


@pytest.mark.asyncio
async def test_hit_cache_json():
    # response from given url contains 'no-cache' directive
    url = "https://my-json-server.typicode.com/typicode/demo/posts"
    expected_json = [
        {"id": 1, "title": "Post 1"},
        {"id": 2, "title": "Post 2"},
        {"id": 3, "title": "Post 3"},
    ]
    cache_observer = CacheObserver()
    async with AsyncCacheControl(cache=cache_observer) as cached_sess:
        async with cached_sess.get(url) as resp:
            # clean headers to force cache response
            resp.headers = {}
            resp_json = await resp.json()
            assert resp.status == 200
            assert resp_json == expected_json

        async with cached_sess.get(url) as resp:
            resp_json = await resp.json()
            assert resp.status == 200
            assert resp_json == expected_json

        assert ("GET", url) in cache_observer.get_calls
