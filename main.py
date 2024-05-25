from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError

from pydantic import BaseModel

from dotenv import load_dotenv

from db.short_urls import create_short_url

from psycopg2.errors import UniqueViolation

import re
import string
import random
import os
import logging

app = FastAPI()

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

db_engine = create_engine(DATABASE_URL)

# used to generate shortcode
SHORTCODE_ALLOWED_CHARACTERS = string.ascii_letters + string.digits + "_"


class ShortenPayload(BaseModel):
    url: Optional[str] = None
    shortcode: Optional[str] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/shorten")
def shorten_url(payload: ShortenPayload):
    if payload.url is None and len(payload.url) == 0:
        return JSONResponse({"message": "url not present"}, status_code=400)

    shortcode = (
        payload.shortcode if payload.shortcode is not None
        else generate_shortcode()
    )

    if not is_shortcode_valid(shortcode):
        return JSONResponse(
            {"message": "the provided shortcode is invalid"},
            status_code=412
        )

    try:
        db = Session(db_engine)
        create_short_url(db, payload.url, shortcode)
        db.commit()

    except DBAPIError as e:
        logging.error(f"{e}")

        if isinstance(e.orig, UniqueViolation):
            return JSONResponse({
                "message": "shortcode already in use"},
                status_code=409,
            )

        return JSONResponse({
            "error": "failed to shorten the url"},
            status_code=500,
        )

    except Exception as e:
        logging.error(f"{e}")
        return JSONResponse({
            "error": "failed to shorten the url"},
            status_code=500,
        )

    finally:
        db.close()

    return JSONResponse({"shortcode": shortcode}, status_code=201)


def generate_shortcode() -> str:
    return ''.join(random.choices(SHORTCODE_ALLOWED_CHARACTERS, k=6))


def is_shortcode_valid(code: str) -> bool:
    return re.match(r"^[a-zA-Z0-9_]{6}$", code)
