from db import Session

async def get_db_session():
    async with Session() as session:
        yield session

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
