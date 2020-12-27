"""Cache implementation for async app.

Current implementation is just a draft, wrapper around simple dict.
"""
import asyncio
import hashlib
import json
from typing import Any, Dict, Tuple

from .exceptions import TimeoutException


class AsyncCache:
    def __init__(self):
        self.cache = {}  # type: Dict
        self._wait_until_completed = set()

    def __contains__(self, key):
        return self._make_key_hashable(key) in self.cache

    def add(self, key: Tuple[str, str, Dict], value: Any) -> None:
        """Add value to the cache.

        # TODO: Values should be stored within the following structure:
        {'created_at': <unix_timestamp>, 'max_age': <seconds>, 'value': <value>}
        """
        hashable_key = self._make_key_hashable(key)
        self.cache[hashable_key] = value
        self.release_new_key(key)

    def get(self, key: Tuple[str, str, Dict]) -> Any:
        return self.cache.get(self._make_key_hashable(key))

    def delete(self, key: Tuple[str, str, Dict]) -> None:
        self.cache.pop(self._make_key_hashable(key), None)

    def clear_cache(self) -> None:
        self.cache = {}

    async def register_new_key(
        self, key: Tuple[str, str, Dict], wait_timeout: float = 10.0
    ):
        """Register new key before actual request, so all subsequent requests
        will know and wait until this one returned a result.

        This should avoid dog-piling problem.
        More details here: https://en.wikipedia.org/wiki/Cache_stampede
        """
        total_wait_time = 0.0
        hashable_key = self._make_key_hashable(key)
        while True:
            if hashable_key not in self._wait_until_completed:
                break
            await asyncio.sleep(0.1)
            total_wait_time += 0.1
            if total_wait_time >= wait_timeout:
                raise TimeoutException(f"Timeout exceeded for {key}")
        if hashable_key not in self.cache:
            self._wait_until_completed.add(hashable_key)

    def release_new_key(self, key: Tuple[str, str, Dict]):
        try:
            self._wait_until_completed.remove(self._make_key_hashable(key))
        except Exception:
            # TODO: consider adding debug log here
            pass

    def _make_key_hashable(
        self, key: Tuple[str, str, Dict]
    ) -> Tuple[str, str, str]:
        """Currently, key structure is always (str, str, dict)

        Thus, we need to convert last parameter only
        """
        method, url, params = key
        return method, url, self._dict_hash(params)

    @staticmethod
    def _dict_hash(input_dict: Dict) -> str:
        """Get dict hash."""
        return hashlib.sha256(json.dumps(input_dict).encode()).hexdigest()
