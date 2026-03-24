import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated, List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UniqueViolationError
from db import Session
from models import Advertisement
from schemas import AdvertisementResponse, AdvertisementCreate, AdvertisementUpdate
from services import add_item, get_item, update_item
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
    return {'Greeting': 'Hello world'}

# POST
@app.post("/advertisement", response_model=AdvertisementResponse, status_code=201, summary="Создаем новое объявление")
async def create_advertisement(ad: AdvertisementCreate, session: SessionDep):
    new_adv = await add_item(session, Advertisement, ad)
    return AdvertisementResponse(id=new_adv.id)

# GET
@app.get("/advertisement/{advertisement_id}", response_model=AdvertisementResponse, status_code=200, summary="Инфо по объявлению")
async def get_advertisement(advertisement_id: int, session: SessionDep):

    adv = await get_item(session, Advertisement, advertisement_id)
    return AdvertisementResponse(**adv.to_dict)


# PATCH
@app.patch("/advertisement/{advertisement_id}", response_model=AdvertisementResponse, status_code=200, summary="Редактируем объявление")
async def update_advertisement(advertisement_id: int, update_data: AdvertisementUpdate, session: SessionDep):

    updated_adv = await update_item(session, Advertisement, advertisement_id, update_data)
    return AdvertisementUpdate(**updated_adv.to_dict)


# DELETE
@app.delete("/advertisement/{advertisement_id}", status_code=200, summary="Удаляем объявление")
async def delete_advertisement(advertisement_id: int, session: SessionDep):
    ...

# GET (querystring)
@app.get("/advertisement", response_model=List[AdvertisementResponse])
async def get_special_advertisement(ad: AdvertisementCreate, session: SessionDep):
    ...


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
