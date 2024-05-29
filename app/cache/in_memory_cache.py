from typing import Dict, Optional

from app.db.models import ShortUrl


class InMemoryCache:
    cache: Dict[str, ShortUrl]

    def __init__(self):
        self.cache = {}

    def get(self, key: str) -> Optional[ShortUrl]:
        return self.cache.get(key)

    def upsert(self, key: str, su: ShortUrl) -> None:
        self.cache[key] = ShortUrl(
            id=su.id,
            shortcode=su.shortcode,
            url=su.url,
            redirect_count=su.redirect_count,
            created_at=su.created_at,
            last_redirect_at=su.last_redirect_at,
        )
