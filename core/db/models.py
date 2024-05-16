import datetime
import enum
from typing import Annotated

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class TransactionsType(enum.Enum):
    income = "Доходы"
    expenses = "Расходы"


class User(Base):
    """Модель пользователей"""

    __tablename__ = "users"

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(unique=True)
    first_name: Mapped[str | None] = mapped_column()
    last_name: Mapped[str | None] = mapped_column()
    username: Mapped[str | None] = mapped_column()


class Category(Base):
    """Модель категорий"""

    __tablename__ = "category"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(100))
    transactions_type: Mapped[TransactionsType]


class Transactions(Base):
    """Модель транзакций"""

    __tablename__ = "transactions"

    id: Mapped[intpk]
    amount: Mapped[int] = mapped_column()
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id", ondelete="CASCADE")
    )
    create_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.timezone("UTC", func.now())
    )
    update_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.timezone("UTC", func.now()),
        onupdate=func.timezone("UTC", func.now()),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))


class Budgets(Base):
    """Модель Бюджета"""

    __tablename__ = "budgets"

    id: Mapped[intpk]
    limit: Mapped[int | None] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id", ondelete="CASCADE")
    )
    month: Mapped[int] = mapped_column()
    year: Mapped[int] = mapped_column()
