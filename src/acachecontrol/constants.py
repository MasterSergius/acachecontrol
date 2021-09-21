"""Common constants used across different modules.
"""
CACHEABLE_METHODS = ("HEAD", "GET")

# Values below provided in seconds
DEFAULT_MAX_AGE = 120
DEFAULT_WAIT_TIMEOUT = 60 * 5  # same value as in aiohttp library
DEFAULT_SLEEP_TIME = 0.1

DEFAULT_CACHE_CAPACITY = 100  # max amount of records in cache
