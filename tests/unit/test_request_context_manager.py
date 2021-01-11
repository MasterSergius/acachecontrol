from acachecontrol.cache import AsyncCache
from acachecontrol.request_context_manager import RequestContextManager


def test_init(mocker):
    method = "GET"
    url = "http://example.com"
    timeout = 10
    cache = AsyncCache()
    rcm = RequestContextManager(
        mocker.Mock(), cache, method, url, timeout=timeout, allow_redirects=True
    )

    assert rcm.method == method
    assert rcm.url == url
    assert rcm.key == (method, url)
    assert rcm.params == {"timeout": timeout, "allow_redirects": True}
    assert rcm.cache == cache
    assert rcm.cache.wait_timeout == timeout
