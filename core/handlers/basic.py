from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from core.db.models import TransactionsType
from core.db.queries import (AsyncQueryCategory, AsyncQueryTransactions,
                             AsyncQueryUser)
from core.keyboards.reply import management, reply_keyboard_builder_category

router = Router()


class TransactionsForm(StatesGroup):
    category = State()
    amount = State()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Приветствую, я помогу в управлении личными финансами и бюджетом, для начала зарегитсрируйтесь /registration",
        reply_markup=management,
    )


@router.message(F.text == "Добавить доходы 📉")
async def cmd_start(message: Message, state: FSMContext) -> None:
    if await AsyncQueryUser.is_user(message.from_user.id):
        await state.set_state(TransactionsForm.category)
        await message.answer(
            "Выберите категорию доходов",
            reply_markup=await reply_keyboard_builder_category(TransactionsType.income),
        )
    else:
        await message.answer("Для дальнейшей работы зарегистрируйтесь /registration")


@router.message(TransactionsForm.category)
async def form_category(message: Message, state: FSMContext) -> None:
    await state.update_data(category=message.text)
    await state.set_state(TransactionsForm.amount)
    await message.answer("Введите сумму транзакции ↓")


@router.message(TransactionsForm.amount)
async def form_amount(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        await state.update_data(amount=message.text)
        data = await state.get_data()
        category = await AsyncQueryCategory.get_category_title_and_type(
            data["category"], TransactionsType.income
        )
        user_tg_id = message.from_user.id
        user = await AsyncQueryUser.get_user(user_tg_id)
        try:
            await AsyncQueryTransactions.create_transactions(
                int(data["amount"]),
                category.id,
                user.id,
            )
            await message.answer("Ваши доходы записал 💵", reply_markup=management)
        except:
            await message.answer(
                "Что-то пошло не так повторите операцию еще раз 😔",
                reply_markup=management,
            )
    else:
        await message.answer("Введите число еще раз ↓")


@router.message(F.text == "Добавить расходы 📈")
async def cmd_start(message: Message, state: FSMContext) -> None:
    if await AsyncQueryUser.is_user(message.from_user.id):
        await state.set_state(TransactionsForm.category)
        await message.answer(
            "Выберите категорию расходов",
            reply_markup=await reply_keyboard_builder_category(
                TransactionsType.expenses
            ),
        )
    else:
        await message.answer("Для дальнейшей работы зарегистрируйтесь /registration")
