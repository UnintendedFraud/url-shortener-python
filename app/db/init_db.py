from sqlalchemy import create_engine

from dotenv import load_dotenv

from models import Base

import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
