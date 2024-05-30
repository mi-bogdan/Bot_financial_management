from sqlalchemy import ScalarResult, insert, select
from sqlalchemy.orm import joinedload

from core.utils.data import category_list

from .database import async_session, engine
from .models import Base, Budgets, Category, Transactions, User


class DataBase:
    """Управление БД"""

    @staticmethod
    async def drop_all_table() -> None:
        """Удлаление всех таблиц"""
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @staticmethod
    async def create_all_table() -> None:
        """Создание всех таблиц"""
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


class AsyncQueryUser:
    """Запросы пользователей"""

    @staticmethod
    async def get_user(user_tg_id: int) -> User | None:
        """Получение пользователя"""
        async with async_session() as session:
            query = await session.execute(select(User).where(User.tg_id == user_tg_id))
            return query.scalar()

    @staticmethod
    async def create_user(
        tg_id: int, first_name: str, last_name: str, username: str
    ) -> None:
        """Создание пользователя"""
        async with engine.connect() as conn:
            query = insert(User).values(
                [
                    {
                        "tg_id": tg_id,
                        "first_name": first_name,
                        "last_name": last_name,
                        "username": username,
                    }
                ]
            )
            await conn.execute(query)
            await conn.commit()

    @staticmethod
    async def is_user(tg_id: int) -> bool:
        async with engine.connect() as conn:
            query = select(User).where(User.tg_id == tg_id)
            result = await conn.execute(query)
            workers = result.scalars().first()
            if workers:
                return True
            else:
                return False


class AsyncQueryCategory:
    """Запросы категорий"""

    @staticmethod
    async def get_category_type(transactions_type: str) -> ScalarResult[Category]:
        """Получение категорий по типу"""
        async with async_session() as session:
            query = await session.scalars(
                select(Category).where(Category.transactions_type == transactions_type)
            )
            return query

    @staticmethod
    async def get_category_title_and_type(
        title: str, transactions_type: str
    ) -> Category | None:
        """Получение одной категории по названию и типу доходности"""
        async with async_session() as session:
            query = await session.scalar(
                select(Category).where(
                    Category.title == title,
                    Category.transactions_type == transactions_type,
                )
            )
            return query

    @staticmethod
    async def insert_category() -> ScalarResult[Category]:
        """Добавление фиксированных категорий"""
        async with engine.connect() as conn:
            stmt = insert(Category).values(category_list)
            await conn.execute(stmt)
            await conn.commit()


class AsyncQueryTransactions:
    """Запросы транзакции"""

    @staticmethod
    async def create_transactions(amount: int, category_id: int, user_id: int) -> None:
        """Создание транзакции"""
        async with async_session() as session:
            session.add(
                Transactions(amount=amount, category_id=category_id, user_id=user_id)
            )
            await session.commit()

    @staticmethod
    async def get_transactions(user_id):
        async with async_session() as session:
            query = await session.execute(select(Transactions).where(Budgets.user_id == user_id))
            return query.scalar()


class AsyncQueryBudgets:
    """Запросы бюджета"""
    @staticmethod
    async def create_budget(limit: int, user_id: int, category_id: int, month, year):
        """Создание бюджета для люмита"""
        async with async_session() as session:
            session.add(Budgets(limit=limit, user_id=user_id, category_id=category_id, month=month, year=year))
            await session.commit()

    @staticmethod
    async def get_budgets(user_id, category_id, month, year):
        async with async_session() as session:
            query = await session.execute(select(Budgets).filter(Budgets.user_id == user_id, Budgets.category_id == category_id, Budgets.month == month, Budgets.year == year))
            return query.scalar()

    @staticmethod
    async def universal_get_budgets(*args, **kwargs):
        async with async_session() as session:
            query = await session.execute(select(Budgets).filter(*args, **kwargs))
            return query.scalars().all()


class AsyncQueryJoin:
    @staticmethod
    async def get_user_budget_categories(user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Category)
                .join(Budgets, Category.id == Budgets.category_id)
                .where(Budgets.user_id == user_id)
                .options(joinedload(Category))
            )
            categories = result.scalars().all()
            return categories
