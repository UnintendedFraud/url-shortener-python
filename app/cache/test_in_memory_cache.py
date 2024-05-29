from app.cache.in_memory_cache import InMemoryCache
from app.db.models import ShortUrl


def test_in_memory_cache():
    cache = InMemoryCache()

    assert cache.cache == {}

    assert cache.get("key") is None

    value = ShortUrl(id="123")
    cache.upsert("key", value)

    assert cache.get("key").id == value.id

    updated_value = ShortUrl(id="321")
    cache.upsert("key", updated_value)

    assert cache.get("key").id == updated_value.id
