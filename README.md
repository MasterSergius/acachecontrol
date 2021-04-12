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
from acachecontrol import AsyncCache, AsyncCacheControl


async def main():
    cache = AsyncCache(config={"sleep_time": 0.2})
    # `AsyncCache()` with default configuration is used
    # if `cache` not provided
    async with AsyncCacheControl(cache=cache) as cached_sess:
        async with cached_sess.get('http://example.com') as resp:
            resp_text = await resp.text()
            print(resp_text)


asyncio.run(main())
```

### Extending or creating new classes

It is possible to use any cache backend, which should implement OrderedDict interfaces: `__contains__`, `__len__`, `__getitem__`, `__setitem__`, `get`, `pop`, `popitem`, `move_to_end`:

```py
class CustomCacheBackend():
    def __init__(self):
        self.item_order = []
        self.storage = {}

    def __contains__(self, key):
        return key in self.storage

    def __len__(self):
        return len(self.storage)

    def __getitem__(self, key):
        return self.storage[key]

    def __setitem__(self, key, value):
        self.storage[key] = value
        self.item_order.append(key)

    def pop(self, key):
        self.item_order.remove(key)
        return self.storage.pop(key)

    def move_to_end(self, key):
        last_index = len(self.item_order) - 1
        key_index = self.item_order.index(key)
        while key_index < last_index:
            self.item_order[key_index] = self.item_order[key_index+1]
            key_index += 1
        self.item_order[last_index] = key

    def popitem(self, last=True):
        key = self.item_order.pop() if last else self.item_order.pop(0)
        value = self.storage.pop(key)
        return value
```

Then you can use it in `AsyncCache`:

```py
import asyncio
from acachecontrol import AsyncCache, AsyncCacheControl


async def main():
    cache = AsyncCache(cache_backend=CustomCacheBackend())
    async with AsyncCacheControl(cache=cache) as cached_sess:
        async with cached_sess.get('http://example.com') as resp:
            resp_text = await resp.text()
            print(resp_text)


asyncio.run(main())
```

Similarly, you can replace RequestContextManager (assume its implementation in module `custom_implementations`):

```py
import asyncio
from acachecontrol import AsyncCache, AsyncCacheControl

from custom_implementations import CustomRequestContextManager


async def main():
    async with AsyncCacheControl(request_context_manager_cls=CustomRequestContextManager) as cached_sess:
        async with cached_sess.get('http://example.com') as resp:
            resp_text = await resp.text()
            print(resp_text)


asyncio.run(main())
```
