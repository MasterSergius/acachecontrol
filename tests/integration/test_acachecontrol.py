import pytest

from acachecontrol import AsyncCacheControl


@pytest.mark.asyncio
async def test_request():
    async with AsyncCacheControl() as cached_sess:
        async with cached_sess.request('GET', 'http://example.com') as resp:
            resp_text = await resp.text()
            assert 'Example Domain' in resp_text


@pytest.mark.asyncio
async def test_hit_cache():
    async with AsyncCacheControl() as cached_sess:
        async with cached_sess.request('GET', 'http://example.com') as resp:
            resp_text = await resp.text()
            assert 'Example Domain' in resp_text

        async with cached_sess.request('GET', 'http://example.com') as resp:
            resp_text = await resp.text()
            assert 'Example Domain' in resp_text

        # TODO: mock cache obj, assert get was called


@pytest.mark.asyncio
async def test_hit_cache_json():
    url = 'https://my-json-server.typicode.com/typicode/demo/posts'
    expected_json = [
        {
          "id": 1,
          "title": "Post 1"
        },
        {
          "id": 2,
          "title": "Post 2"
        },
        {
          "id": 3,
          "title": "Post 3"
        }
    ]
    async with AsyncCacheControl() as cached_sess:
        async with cached_sess.request('GET', url) as resp:
            resp_json = await resp.json()
            assert resp_json == expected_json

        async with cached_sess.request('GET', url) as resp:
            resp_json = await resp.json()
            assert resp_json == expected_json

        # TODO: mock cache obj, assert get was called
