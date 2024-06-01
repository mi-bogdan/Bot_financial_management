import datetime
import enum
from typing import Annotated

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):

    def __repr__(self):
        columns = [f"{c.name}={getattr(self, c.name)!r}" for c in self.__table__.columns]
        return f"<{self.__class__.__name__}({', '.join(columns)})>"


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

    budgets = relationship("Budgets", back_populates="category")
    transactions = relationship("Transactions", back_populates="category")


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
    category = relationship("Category", back_populates="transactions")


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

    category = relationship("Category", back_populates="budgets")
