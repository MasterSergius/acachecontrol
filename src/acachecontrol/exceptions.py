class BaseACacheControlException(Exception):
    pass


class TimeoutException(BaseACacheControlException):
    pass


class CacheException(BaseACacheControlException):
    pass
