from sqlalchemy.orm import Session

from app.db.models import ShortUrl


def get_short_url(db: Session, shortcode: str) -> ShortUrl:
    return db.query(ShortUrl).filter_by(shortcode=shortcode).one()


def create_short_url(db: Session, url: str, shortcode: str):
    db.add(ShortUrl(
        url=url,
        shortcode=shortcode,
    ))
