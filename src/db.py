from datetime import datetime
from uuid import uuid4

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from src.settings import DB_URL

engine = create_engine(DB_URL)
Base = declarative_base()


class UsedCarsInfo(Base):
    __tablename__ = "used_cars_info"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        default=uuid4,
    )
    url = Column(String(255), unique=True)
    title = Column(String(255))
    price_usd = Column(Integer)
    odometer = Column(Integer)
    username = Column(String(255))
    phone_number = Column(String(255))
    image_url = Column(String)
    image_count = Column(Integer)
    car_number = Column(String(255))
    car_vin = Column(String(255))
    datetime_found = Column(DateTime, default=datetime.now())
