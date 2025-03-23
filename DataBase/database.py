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


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)