from fastapi import APIRouter, Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from dotenv import load_dotenv

from app.api.api import Api, ShortenPayload


import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

db_engine = create_engine(DATABASE_URL)

router = APIRouter()

SessionLocal = scoped_session(sessionmaker(
    autocommit=False,
    bind=db_engine,
))

api = Api()


def get_db():
    db = SessionLocal()
    try:
        yield db

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


@router.get("/{shortcode}/stats")
def get_shortcode_stats(shortcode: str, db: Session = Depends(get_db)):
    return api.get_shortcode_stats(db, shortcode)


@ router.get("/{shortcode}")
def redirect_to_url(shortcode: str, db: Session = Depends(get_db)):
    return api.redirect_to_url(db, shortcode)


@ router.post("/shorten")
def shorten_url(payload: ShortenPayload, db: Session = Depends(get_db)):
    return api.shorten_url(db, payload)
