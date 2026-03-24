from pydantic import BaseModel

import os
from sqlalchemy import Integer, Text, String, Column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


from datetime import datetime
from typing import Optional

class AdvertisementBase(BaseModel):
    title: str
    description: str
    price: float
    author: str

class AdvertisementCreate(AdvertisementBase):
    ...

class AdvertisementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    author: Optional[str] = None

class AdvertisementResponse(AdvertisementBase):
    id: int
