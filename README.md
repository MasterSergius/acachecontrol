# Async CacheControl for aiohttp

> Requires Python3.6+

### Note: Library is under development.
### For contributing see development_notes.md as starting guide

## What and why

There is a good and simple library [CacheControl](https://github.com/ionrock/cachecontrol) written for python requests library. And there is nothing similar for aiohttp. "Async CacheControl" project strives to cover this hole.

## Usage

```py
import asyncio
from acachecontrol import AsyncCacheControl


async def main():
    async with AsyncCacheControl() as cached_sess:
        async with cached_sess.request('GET', 'http://example.com') as resp:
            resp_text = await resp.text()
            print(resp_text)


asyncio.run(main())
```
