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
