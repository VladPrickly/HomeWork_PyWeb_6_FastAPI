import uvicorn
from fastapi import FastAPI, Depends, Query, HTTPException, status
from typing import Annotated, List, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UniqueViolationError
from db import Session
from models import Advertisement
from schemas import AdvertisementResponse, AdvertisementCreate, AdvertisementUpdate, OKResponse
from services import add_item, get_item, update_item, delete_item, search_item
from lifespan import lifespan
from dependencies import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(
    titel="Advertisement",
    description="Buy/Sell Service",
    version="0.0.1",
    # lifespan=lifespan,
)

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


@app.get('/')
def print_hello_world():
    return {'message': 'Hello world'}


# POST
@app.post("/advertisement", response_model=AdvertisementResponse, status_code=201, summary="Создаем новое объявление")
async def create_advertisement(ad: AdvertisementCreate, session: SessionDep):
    new_adv = await add_item(session, Advertisement, ad)
    return AdvertisementResponse(id=new_adv.id)


# GET
@app.get("/advertisement/{advertisement_id}", response_model=AdvertisementResponse, status_code=200,
         summary="Инфо по объявлению")
async def get_advertisement(advertisement_id: int, session: SessionDep):
    adv = await get_item(session, Advertisement, advertisement_id)
    return AdvertisementResponse(**adv.to_dict)


# PATCH
@app.patch("/advertisement/{advertisement_id}", response_model=AdvertisementResponse, status_code=200,
           summary="Редактируем объявление")
async def update_advertisement(advertisement_id: int, update_data: AdvertisementUpdate, session: SessionDep):
    updated_adv = await update_item(session, Advertisement, advertisement_id, update_data)
    return AdvertisementUpdate(**updated_adv.to_dict)


# DELETE
@app.delete("/advertisement/{advertisement_id}", response_model=OKResponse, status_code=200,
            summary="Удаляем объявление")
async def delete_advertisement(advertisement_id: int, session: SessionDep):
    await delete_item(session, Advertisement, advertisement_id)
    return OKResponse()


# GET (querystring)
@app.get("/advertisement/", response_model=List[AdvertisementResponse], summary="Объявления по параметрам")
async def get_query_string_advertisement(
        title: Optional[str] = Query(None),
        description: Optional[str] = Query(None),
        price: Optional[float] = Query(None),
        author: Optional[str] = Query(None),
        db: Session = Depends(get_db_session)
):
    adv = search_item(
        db=db,
        title=title,
        description=description,
        price=price,
        author=author
    )
    return adv


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
