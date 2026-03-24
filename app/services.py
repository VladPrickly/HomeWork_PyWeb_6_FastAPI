from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UniqueViolationError
from models import Advertisement
from schemas import AdvertisementCreate

from sqlalchemy import select
from datetime import datetime, timezone

import models
import schemas

async def add_item(
    session: AsyncSession,
    orm_model: type[Advertisement],
    item_data: AdvertisementCreate
) -> Advertisement:

    new_item = orm_model(**item_data.model_dump())
    session.add(new_item)
    try:
        await session.commit()
        await session.refresh(new_item)
        return new_item
    except IntegrityError as e:
        await session.rollback()
        # Проверяем, является ли ошибка нарушением уникальности (код 23505 для PostgreSQL)
        if isinstance(e.orig, UniqueViolationError) and e.orig.pgcode == '23505':
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Item with such data already exists." )
        else:
            raise e

async def add_item():
    ...