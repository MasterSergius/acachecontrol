[![PyPI](https://img.shields.io/pypi/v/acachecontrol)](https://pypi.org/project/acachecontrol/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# Async CacheControl for aiohttp

> Requires Python3.6+

### Note: Library is still under development, there might be a lot of bugs.
### For contributing see development_notes.md as a starting guide

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
