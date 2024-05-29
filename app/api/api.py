from typing import Optional

from fastapi import HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql.functions import now

from pydantic import BaseModel


from app.db.short_urls import ShortUrlObj
from app.utils.shortcode import is_shortcode_valid, generate_shortcode
from app.utils.url import maybe_add_https, is_url_valid
from app.cache.in_memory_cache import InMemoryCache

from psycopg2.errors import UniqueViolation

import logging


class ShortenPayload(BaseModel):
    url: str
    shortcode: Optional[str] = None


class Api:
    cache: InMemoryCache

    def __init__(self):
        self.cache = InMemoryCache()

    def get_shortcode_stats(self, db: Session, shortcode: str):
        shortcode = shortcode.strip()

        if not is_shortcode_valid(shortcode):
            raise HTTPException(status_code=400, detail="invalid shortcode")

        short_url = self.cache.get(shortcode)

        if short_url is None:
            try:
                short_url = ShortUrlObj().get_by_shortcode(db, shortcode)

            except Exception as e:
                logging.error(f"{e}")

                raise HTTPException(
                    status_code=500,
                    detail=f"failed to get stats for shortcode [{shortcode}]",
                )

        if short_url is None:
            raise HTTPException(status_code=404, detail="shortcode not found")

        self.cache.upsert(short_url.shortcode, short_url)

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

    def redirect_to_url(self, db: Session, shortcode: str):
        shortcode = shortcode.strip()

        if not is_shortcode_valid(shortcode):
            raise HTTPException(status_code=400, detail="invalid shortcode")

        try:
            short_url = ShortUrlObj().get_by_shortcode(db, shortcode)

        except Exception as e:
            logging.error(f"{e}")

            raise HTTPException(
                status_code=500,
                detail=f"failed to redirect with shortcode [{shortcode}]",
            )

        if short_url is None:
            raise HTTPException(status_code=404, detail="shortcode not found")

        try:
            short_url.redirect_count += 1
            short_url.last_redirect_at = now()
            db.commit()

        except Exception as e:
            logging.error(f"{e}")

            raise HTTPException(
                status_code=500,
                detail=f"failed to redirect with shortcode [{shortcode}]",
            )

        self.cache.upsert(short_url.shortcode, short_url)

        return RedirectResponse(short_url.url, status_code=302)

    def shorten_url(self, db: Session, payload: ShortenPayload):
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
            ShortUrlObj().create(db, url, shortcode)
            db.commit()

        except DBAPIError as e:
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
            logging.error(f"{e}")

            raise HTTPException(
                status_code=500,
                detail="failed to shorten the url",
            )

        return JSONResponse({"shortcode": shortcode}, status_code=201)
