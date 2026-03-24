import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated, List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import UniqueViolationError
from db import Session
from models import Advertisement
from schemas import AdvertisementResponse, AdvertisementCreate
from lifespan import lifespan
from dependencies import get_db_session

app = FastAPI(
    titel="Advertisement",
    description="Buy/Sell Service",
    version="0.0.1",
    lifespan=lifespan,
)

SessionDep = Annotated[Session, Depends(get_db_session)]

@app.post("/advertisement", response_model=AdvertisementResponse, status_code=201, summary="Создаем новое объявление")
async def create_advertisement(ad: AdvertisementCreate, session: SessionDep):
    new_ad = Advertisement(
        id = ad.id,
        title = ad.title,
        description = ad.description,
        price = ad.price,
        author = ad.author,
    )

    session.add(new_ad)
    await session.commit()
    await session.refresh(new_ad)
    return AdvertisementResponse(id=new_ad.id)

'''

@app.post("/advertisement", response_model=AdvertisementOut, status_code=201)
def create_advertisement(ad: AdvertisementIn):
    ad_id = uuid4()
    item = {
        "id": ad_id,
        "title": ad.title,
        "description": ad.description,
        "price": ad.price,
        "author": ad.author,
        "created_at": current_time_iso(),
    }
    db[ad_id] = AdvertisementIn(**item)
    return AdvertisementOut(**item)
'''

@app.get("/advertisement/{advertisement_id}", response_model=AdvertisementResponse)
async def get_advertisement(ad: AdvertisementCreate, session: SessionDep):
    ...

@app.patch("/advertisement/{advertisement_id}", response_model=AdvertisementResponse)
def update_advertisement(ad: AdvertisementCreate, session: SessionDep):
    ...

@app.delete("/advertisement/{advertisement_id}")
def delete_advertisement(advertisement_id: int, session: SessionDep):
    ...


@app.get("/advertisement", response_model=List[AdvertisementResponse])
async def get_special_advertisement(ad: AdvertisementCreate, session: SessionDep):
    ...



if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
