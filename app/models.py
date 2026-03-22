from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.orm import MappedColumn, mapped_column
from sqlalchemy.sql import func
from db import Base

class Advertisement(Base):
    __tablename__ = "advertisements"

    title: MappedColumn[str] = mapped_column(String)
    description: MappedColumn[str] = mapped_column(Text)
    price = Column(Integer)
    author: MappedColumn[str] = mapped_column(String)
    created_at: MappedColumn[datetime] = mapped_column(DateTime, server_default=func.now())

