from sqlalchemy.orm import Session

from db.models import ShortUrl


def create_short_url(db: Session, url: str, shortcode: str):
    db.add(ShortUrl(
        url=url,
        shortcode=shortcode,
    ))
