from DataBase.database import async_session, User, Counter
from sqlalchemy import select


async def set_user(tg_id: int, username: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            user.username = username
        else:
            user = User(tg_id=tg_id, username=username)
            session.add(user)
            await session.flush()

            counter = Counter(user_id=user.id, count=0)
            session.add(counter)
        
        await session.commit()


async def update_count(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user: 
            counter = await session.scalar(select(Counter).where(Counter.user_id==user.id))

            if counter:
                counter.count += 1
            else:
                counter = Counter(user_id=user.id, count=1)
                session.add(counter)

            await session.commit()