from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime
import uuid


Base = declarative_base()


class ShortUrl(Base):
    __tablename__ = 'short_urls'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shortcode = Column(String(6), unique=True, index=True, nullable=False)
    url = Column(Text, nullable=False)
    redirect_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)
    last_redirect_at = Column(DateTime)
