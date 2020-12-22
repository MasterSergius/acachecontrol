"""Cache implementation for async app.

Current implementation is just a draft, wrapper around simple dict.
"""

# TODO: solve dog-piling problem: https://en.wikipedia.org/wiki/Cache_stampede
# Take a look at py-memoize library

class AsyncCache:
    def __init__(self):
        self.cache = {}

    def __contains__(self, key):
        return self._make_key_hashable(key) in self.cache

    def add(self, key, value):
        self.cache[self._make_key_hashable(key)] = value

    def get(self, key):
        return self.cache.get(self._make_key_hashable(key))

    def delete(self, key):
        pass

    def clear_cache(self):
        self.cache = {}

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
