from DataBase.database import async_session, User
from sqlalchemy import select


async def set_user(tg_id: int, username: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            user.username = username
        else:
            user = User(tg_id=tg_id, username=username)
            session.add(user)
        
        await session.commit()