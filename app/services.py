from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UniqueViolationError
from models import Advertisement
from schemas import AdvertisementCreate, AdvertisementUpdate
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


async def get_item(
    session: AsyncSession,
    orm_model: type[Advertisement],
    item_id: int
) -> Advertisement:

    adv = select(orm_model).where(orm_model.id == item_id)
    result = await session.execute(adv)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{orm_model.__name__} with id {item_id} not found"
        )
    return item


async def update_item(
    session: AsyncSession,
    orm_model: type[Advertisement],
    item_id: int,
    update_data: AdvertisementUpdate
) -> Advertisement:

    item = await get_item(session, orm_model, item_id)

    # Преобразуем update_data в словарь, исключая поля со значением None
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(item, key, value)

    await session.commit()
    await session.refresh(item)
    return item

async def delete_item(
    session: AsyncSession,
    orm_model: type[Advertisement],
    item_id: int
) -> None:
    """
    Удаляет запись.
    """
    item = await get_item(session, orm_model, item_id)
    await session.delete(item)
    await session.commit()


async def search_item(db: AsyncSession,
            title: Optional[str] = None,
            description: Optional[str] = None,
            price: Optional[float] = None,
            author: Optional[str] = None):
    query = select(Advertisement)

    if title:
        query = query.where(Advertisement.title.ilike(f"%{title}%"))
    if description:
        query = query.where(Advertisement.description.ilike(f"%{description}%"))
    if price:
        query = query.where(Advertisement.price == price)
    if author:
        query = query.where(Advertisement.author.ilike(f"%{author}%"))

    result = await db.execute(query)
    return result.scalars().all()
