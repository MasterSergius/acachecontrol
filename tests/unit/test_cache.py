import time

from acachecontrol.cache import AsyncCache


def test_add_happy_path(monkeypatch):
    current_timestamp = time.time()
    monkeypatch.setattr(time, "time", lambda: current_timestamp)
    acache = AsyncCache()
    acache.add(
        key=("test_method", "test_url", {"data": "test_data"}),
        value="test_response",
        headers={
            "Cache-Control": "max-age=604800",
            "Content-Type": "text/html; charset=UTF-8",
        },
    )
    cache_key = (
        "test_method",
        "test_url",
        "95f4fd1dd8c46219f8cbb42419a2dc53317f6eb3b95711a752773c042f623483",
    )
    assert cache_key in acache.cache
    assert acache.cache[cache_key]["created_at"] == current_timestamp
    assert acache.cache[cache_key]["max-age"] == 604800
    assert acache.cache[cache_key]["value"] == "test_response"


def test_add_no_cache():
    acache = AsyncCache()
    acache.add(
        key=("test_method", "test_url", {"data": "test_data"}),
        value="test_response",
        headers={
            "Cache-Control": "max-age=604800,no-cache",
            "Content-Type": "text/html; charset=UTF-8",
        },
    )
    assert len(acache.cache) == 0

    acache.add(
        key=("test_method", "test_url", {"data": "test_data"}),
        value="test_response",
        headers={
            "Cache-Control": "max-age=604800,no-store",
            "Content-Type": "text/html; charset=UTF-8",
        },
    )
    assert len(acache.cache) == 0
