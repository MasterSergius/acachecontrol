# Async CacheControl for aiohttp

> Requires Python3.6+

### Note: Library is under development.
### For contributing see development_notes.md as starting guide

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
