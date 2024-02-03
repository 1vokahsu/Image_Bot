from sqlalchemy import text
from sqlalchemy import select
from core.database.database import async_engine, Base, async_session_factory
from core.database.models import UsersORM


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def add_user_id(user_id: int, username: str):
        async with async_session_factory() as session:
            '''
            SELECT EXISTS (SELECT * FROM users WHERE user_id = 123)
            '''
            query = (
                select(select("*").select_from(UsersORM).where(UsersORM.user_id == user_id).exists())
            )
            exist_query = await session.execute(query)
            exist_query = exist_query.all()[0][0]
            if not exist_query:
                exist_query = UsersORM(user_id=user_id,
                                       username=username,
                                       gens=1,
                                       age="kid",
                                       sex="man",
                                       profession="Firefighter",
                                       rate=False)
                session.add(exist_query)
                await session.flush()
                await session.commit()

    @staticmethod
    async def add_age(user_id: int, age: str):
        async with async_session_factory() as session:
            stmt = text("UPDATE users SET age=:new_age WHERE user_id=:id").bindparams(new_age=age, id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_sex(user_id: int, sex: str):
        async with async_session_factory() as session:
            stmt = text("UPDATE users SET sex=:new_sex WHERE user_id=:id").bindparams(new_sex=sex, id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_prof(user_id: int, prof: str):
        async with async_session_factory() as session:
            stmt = text("UPDATE users SET profession=:new_prof WHERE user_id=:id").bindparams(new_prof=prof, id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_rate(user_id: int, rate: bool):
        async with async_session_factory() as session:
            stmt = text("UPDATE users SET rate=:new_rate WHERE user_id=:id").bindparams(new_rate=rate, id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def sub_gens(user_id: int):
        async with async_session_factory() as session:
            stmt = text("UPDATE users SET gens=gens - 1 WHERE user_id=:id").bindparams(id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_gens(user_id: int, val: int):
        async with async_session_factory() as session:
            stmt = text("UPDATE users SET gens=gens + :new_val WHERE user_id=:id").bindparams(new_val=val, id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def check_rate(user_id: int):
        async with async_session_factory() as session:
            query = (
                select(UsersORM.rate).select_from(UsersORM).filter_by(user_id=user_id)
            )
            check = await session.execute(query)
            return check.all()[0][0]

    @staticmethod
    async def get_sex_prof(user_id: int):
        async with async_session_factory() as session:
            query = (
                select(UsersORM.sex, UsersORM.profession).select_from(UsersORM).filter_by(user_id=user_id)
            )
            check = await session.execute(query)
            res = check.all()[0]
            return res

    @staticmethod
    async def get_gens(user_id: int):
        async with async_session_factory() as session:
            query = (
                select(UsersORM.gens).select_from(UsersORM).filter_by(user_id=user_id)
            )
            check = await session.execute(query)
            check = check.all()

            return check[0][0]

    @staticmethod
    async def get_sex(user_id: int):
        async with async_session_factory() as session:
            query = (
                select(UsersORM.sex).select_from(UsersORM).filter_by(user_id=user_id)
            )
            check = await session.execute(query)
            check = check.all()

            return check[0][0]
