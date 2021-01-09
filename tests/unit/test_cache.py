import time

from acachecontrol.cache import AsyncCache


def test_add_happy_path(monkeypatch):
    current_timestamp = time.time()
    monkeypatch.setattr(time, "time", lambda: current_timestamp)
    acache = AsyncCache()
    acache.add(
        key=("GET", "test_url"),
        value="test_response",
        headers={
            "Cache-Control": "max-age=604800",
            "Content-Type": "text/html; charset=UTF-8",
        },
    )
    cache_key = ("GET", "test_url")
    assert cache_key in acache.cache
    assert acache.cache[cache_key]["created_at"] == current_timestamp
    assert acache.cache[cache_key]["max-age"] == 604800
    assert acache.cache[cache_key]["value"] == "test_response"


def test_non_cacheable_method():
    acache = AsyncCache()
    acache.add(
        key=("test_method", "test_url"),
        value="test_response",
        headers={
            "Cache-Control": "max-age=604800",
            "Content-Type": "text/html; charset=UTF-8",
        },
    )
    assert len(acache.cache) == 0


def test_add_no_cache():
    acache = AsyncCache()
    acache.add(
        key=("GET", "test_url"),
        value="test_response",
        headers={
            "Cache-Control": "max-age=604800,no-cache",
            "Content-Type": "text/html; charset=UTF-8",
        },
    )
    assert len(acache.cache) == 0

    acache.add(
        key=("GET", "test_url"),
        value="test_response",
        headers={
            "Cache-Control": "max-age=604800,no-store",
            "Content-Type": "text/html; charset=UTF-8",
        },
    )
    assert len(acache.cache) == 0
