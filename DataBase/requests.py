from DataBase.database import async_session, User, Counter, Token, TokenRequest
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


async def add_token_request(token_value: str):
    async with async_session() as session:
        # Знаходимо або створюємо токен
        result = await session.execute(select(Token).where(Token.token == token_value))
        token = result.scalars().first()
        if not token:
            token = Token(token=token_value)
            session.add(token)
            await session.flush()  # Отримуємо ID токен

        # Знаходимо або створюємо запис TokenRequest для цього токену
        result = await session.execute(
            select(TokenRequest)
            .where(TokenRequest.token_id == token.id)
        )
        token_request = result.scalars().first()
        if not token_request:
            token_request = TokenRequest(token_id=token.id, request_count=0)
            session.add(token_request)

        
        token_request.request_count += 1
        await session.commit()