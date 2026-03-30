from datetime import datetime
from pydantic import Field, BaseModel, ConfigDict
from sqlalchemy import Integer, String, Text, Boolean, DateTime, Numeric
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func
from db import Base

class Advertisement(Base):
    __tablename__ = "advertisements"

    title: Mapped[str] = mapped_column(String, comment="Заголовок объявления")
    description: Mapped[str] = mapped_column(Text, comment="Описание объявления")
    price: Mapped[float]= mapped_column(Numeric, comment="Цена")
    author: Mapped[str] = mapped_column(String, comment="Автор")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    @property
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'author': self.author,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return (f'<Advertisement (id = "{self.id}")>')

