from typing import Optional

from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse, RedirectResponse

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.functions import now

from pydantic import BaseModel

from dotenv import load_dotenv

from app.db.short_urls import create_short_url, get_short_url
from app.utils.shortcode import is_shortcode_valid, generate_shortcode
from app.utils.url import maybe_add_https, is_url_valid

from psycopg2.errors import UniqueViolation


import os
import logging


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

db_engine = create_engine(DATABASE_URL)

router = APIRouter()


@router.get("/{shortcode}/stats")
def get_shortcode_stats(shortcode: str):
    shortcode = shortcode.strip()

    if not is_shortcode_valid(shortcode):
        raise HTTPException(status_code=400, detail="invalid shortcode")

    try:
        db = Session(db_engine)
        short_url = get_short_url(db, shortcode)

    except NoResultFound as e:
        logging.error(f"{e}")

        raise HTTPException(status_code=404, detail="shortcode not found")

    except Exception as e:
        logging.error(f"{e}")

        raise HTTPException(
            status_code=500,
            detail=f"failed to get stats for shortcode [{shortcode}]",
        )

    finally:
        db.close()

    last_redirect_at = (
        None if short_url.last_redirect_at is None
        else short_url.last_redirect_at.isoformat()
    )

    return JSONResponse({
        "created": short_url.created_at.isoformat(),
        "lastRedirect": last_redirect_at,
        "redirectCount": short_url.redirect_count,
    },
        status_code=200,
    )


@router.get("/{shortcode}")
def redirect_to_url(shortcode: str):
    shortcode = shortcode.strip()

    if not is_shortcode_valid(shortcode):
        raise HTTPException(status_code=400, detail="invalid shortcode")

    try:
        db = Session(db_engine)
        short_url = get_short_url(db, shortcode)
        short_url.redirect_count += 1
        short_url.last_redirect_at = now()
        url = short_url.url
        db.commit()

    except NoResultFound as e:
        db.rollback()
        logging.error(f"{e}")

        raise HTTPException(status_code=404, detail="shortcode not found")

    except Exception as e:
        db.rollback()
        logging.error(f"{e}")

        raise HTTPException(
            status_code=500,
            detail=f"failed to redirect with shortcode [{shortcode}]",
        )

    finally:
        db.close()

    return RedirectResponse(url, status_code=302)


class ShortenPayload(BaseModel):
    url: str
    shortcode: Optional[str] = None


@router.post("/shorten")
def shorten_url(payload: ShortenPayload):
    url = maybe_add_https(payload.url.strip())

    if not is_url_valid(url):
        raise HTTPException(
            status_code=400,
            detail="the provided url is invalid",
        )

    shortcode = (
        payload.shortcode.strip() if payload.shortcode is not None
        else generate_shortcode()
    )

    if not is_shortcode_valid(shortcode):
        raise HTTPException(
            status_code=412,
            detail="the provided shortcode is invalid",
        )

    try:
        db = Session(db_engine)
        create_short_url(db, url, shortcode)
        db.commit()

    except DBAPIError as e:
        db.rollback()
        logging.error(f"{e}")

        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(
                status_code=409,
                detail="shortcode already in use",
            )

        raise HTTPException(
            status_code=500,
            detail="failed to shorten the url",
        )

    except Exception as e:
        db.rollback()
        logging.error(f"{e}")

        raise HTTPException(
            status_code=500,
            detail="failed to shorten the url",
        )

    finally:
        db.close()

    return JSONResponse({"shortcode": shortcode}, status_code=201)
