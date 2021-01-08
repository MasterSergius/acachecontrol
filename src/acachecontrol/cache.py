"""Cache implementation for async app.

Current implementation is just a draft, wrapper around simple dict.
"""
import asyncio
import hashlib
import json
import logging
import time
from typing import Any, Dict, Tuple

from .exceptions import CacheException, TimeoutException

logger = logging.getLogger(__name__)


# Values below provided in seconds
DEFAULT_MAX_AGE = 120
DEFAULT_WAIT_TIMEOUT = 30
DEFAULT_SLEEP_TIME = 0.1


class AsyncCache:
    def __init__(self, config={}):
        self.cache = {}  # type: Dict
        self._wait_until_completed = set()
        self.default_max_age = config.get("max_age", DEFAULT_MAX_AGE)
        self.wait_timeout = config.get("wait_timeout", DEFAULT_WAIT_TIMEOUT)
        self.sleep_time = config.get("sleep_time", DEFAULT_SLEEP_TIME)
        self.cacheable_methods = config.get(
            "cacheable_methods", ("HEAD", "GET")
        )

    def has_valid_entry(self, key) -> bool:
        """Check if entry exists and not expired, delete expired."""
        cache_key = self._make_key_hashable(key)
        if cache_key in self.cache:
            if not self.is_cache_entry_expired(key):
                return True

            logger.debug(f"Cache entry is expired for {key} key")
            self.delete(key)
        return False

    def add(self, key: Tuple[str, str, Dict], value: Any, headers: Any) -> None:
        """Add value to the cache.

        headers - any dict-like obj

        """
        cc_header = self.parse_cache_control_header(headers)
        if self._is_response_cacheable(key[0], cc_header):
            hashable_key = self._make_key_hashable(key)
            self.cache[hashable_key] = {
                "created_at": time.time(),
                "max-age": cc_header.get("max-age", self.default_max_age),
                "value": value,
            }
        self.release_new_key(key)
        logger.debug(f"Added a new entry to cache for {key} key")

    def get(self, key: Tuple[str, str, Dict]) -> Any:
        try:
            cache_entry = self.cache.get(self._make_key_hashable(key))
            if cache_entry:
                logger.debug(f"Get entry from cache for {key} key")
                return cache_entry["value"]
            raise CacheException(f"No cache entry for {key} key")
        except Exception:
            raise CacheException(
                f"Error getting value from cache for {key} key"
            )

    def delete(self, key: Tuple[str, str, Dict]) -> None:
        logger.debug(f"Delete entry from cache for {key} key")
        self.cache.pop(self._make_key_hashable(key), None)

    def clear_cache(self) -> None:
        self.cache = {}

    def is_cache_entry_expired(self, key: Tuple[str, str, Dict]) -> bool:
        entry = self.cache[self._make_key_hashable(key)]
        return entry["created_at"] + entry["max-age"] < time.time()

    async def register_new_key(self, key: Tuple[str, str, Dict]):
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
            await asyncio.sleep(self.sleep_time)
            total_wait_time += self.sleep_time
            if total_wait_time >= self.wait_timeout:
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

    def _is_response_cacheable(self, method, cc_header):
        if method not in self.cacheable_methods:
            return False
        # Although, no-cache means "The response may be stored by any cache,
        # but MUST always go through validation with the origin server first
        # before using it", we won't cache it for simplicity for now.
        if "no-cache" in cc_header or "no-store" in cc_header:
            return False
        return True

    @staticmethod
    def _dict_hash(input_dict: Dict) -> str:
        """Get dict hash."""
        return hashlib.sha256(
            json.dumps(sorted(input_dict.items())).encode()
        ).hexdigest()

    @staticmethod
    def parse_cache_control_header(headers) -> Dict:
        """Parse cache-control header, get max-age value.

        Args:
            headers: any dict-like object

        Returns:
            dict: parsed cache-control header

        Example:
            >>> headers = {"Cache-Control": "max-age=604800",
                           "Content-Type": "application/json"}
            >>> self.parse_cache_control_header(headers)
            {"max-age": 604800}
        """
        cache_control_header = headers.get(
            "cache-control",
            headers.get("Cache-Control", headers.get("CACHE-CONTROL", "")),
        )

        # Currently, parse the most important directives
        # TODO: consider parse all possible directives
        parsed_header = {}  # type: Dict[str, Any]
        for directive in cache_control_header.split(","):
            cleaned_directive = directive.strip().lower()
            # get directives without values
            if cleaned_directive in ("no-cache", "no-store"):
                parsed_header[cleaned_directive] = True
            elif "=" in cleaned_directive:
                key, value = directive.split("=", 1)
                if "max-age" == key:
                    parsed_header["max-age"] = int(value)
            # ignore all other directives except no-cache, no-store, max-age
        return parsed_header
