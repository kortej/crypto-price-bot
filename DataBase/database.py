from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///DataBase/bot.db')

async_session = async_sessionmaker(engine)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(30))
    counter: Mapped["Counter"] = relationship("Counter", back_populates='user', uselist=False)


class Counter(Base):
    __tablename__ = 'counter'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    count: Mapped[int] = mapped_column(default=0)
    user: Mapped['User'] = relationship("User", back_populates='counter')


class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(20))
    token_requests: Mapped[list["TokenRequest"]] = relationship(back_populates="token")


class TokenRequest(Base):
    __tablename__ = 'token_request'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  
    token_id: Mapped[int] = mapped_column(ForeignKey("tokens.id"))  
    request_count: Mapped[int] = mapped_column(default=0) 
    token: Mapped["Token"] = relationship(back_populates="token_requests")
    user: Mapped["User"] = relationship("User")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)