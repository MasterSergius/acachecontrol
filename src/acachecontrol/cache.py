"""Cache implementation for async app.

Current implementation is just a draft, wrapper around simple dict.
"""
import asyncio

from .exceptions import TimeoutException


class AsyncCache:
    def __init__(self):
        self.cache = {}
        self._wait_until_completed = set()

    def __contains__(self, key):
        return self._make_key_hashable(key) in self.cache

    def add(self, key, value):
        hashable_key = self._make_key_hashable(key)
        self.cache[hashable_key] = value
        self.release_new_key(key)

    def get(self, key):
        return self.cache.get(self._make_key_hashable(key))

    def delete(self, key):
        pass

    def clear_cache(self):
        self.cache = {}

    async def register_new_key(self, key, wait_timeout=10):
        """Register new key before actual request, so all subsequent requests
        will know and wait until this one returned a result.

        This should avoid dog-piling problem.
        More details here: https://en.wikipedia.org/wiki/Cache_stampede
        """
        total_wait_time = 0
        hashable_key = self._make_key_hashable(key)
        while True:
            if hashable_key not in self._wait_until_completed:
                break
            await asyncio.sleep(0.1)
            total_wait_time += 0.1
            if total_wait_time >= wait_timeout:
                raise TimeoutException(f'Timeout exceeded for {key}')
        if hashable_key not in self.cache:
            self._wait_until_completed.add(self._make_key_hashable(key))

    def release_new_key(self, key):
        try:
            self._wait_until_completed.remove(self._make_key_hashable(key))
        except:
            # TODO: consider adding debug log here
            pass

    def _make_key_hashable(self, key):
        """Currently, key structure is always (str, str, dict)

        Thus, we need to convert last parameter only
        """
        # TODO: make universal solution using recursion
        method, url, params = key
        return (method, url, self._dict_to_tuple(params))

    def _dict_to_tuple(self, input_dict):
        """Dict is not hashable, thus we need something else."""
        return tuple(sorted(input_dict.items()))
