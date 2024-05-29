from sqlalchemy.orm import Session

from app.db.models import ShortUrl


class ShortUrlObj:
    def get_by_shortcode(self, db: Session, shortcode: str) -> ShortUrl:
        return db.query(ShortUrl).filter_by(shortcode=shortcode).one_or_none()

    def create(self, db: Session, url: str, shortcode: str):
        db.add(ShortUrl(
            url=url,
            shortcode=shortcode,
        ))
