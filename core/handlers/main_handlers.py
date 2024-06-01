from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.db.models import TransactionsType
from core.db.queries import (AsyncQueryCategory, AsyncQueryTransactions,
                             AsyncQueryUser, AsyncQueryBudgets, AsyncQueryJoin)
from core.states.states import TransactionsForm, BudgetsForm, ApprovalForm
from core.keyboards.reply import management, reply_keyboard_builder_category, settings_reply_Keyboard, yes_no
from core.keyboards.inline import inline_back_transaction, inline_back_limite

import datetime

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "🤑 Приветствую, я помогу в управлении личными финансами и бюджетом, для начала зарегитсрируйтесь /registration",
        reply_markup=management,
    )

# -------------------------------ДОБАВЛЕНИЕ ТРАНЗАКЦИЙ ДОХОДОВ И РАСХОДОВ-------------------------------------


@router.message(F.text == "Добавить расходы 📈")
async def add_expenses(message: Message, state: FSMContext) -> None:
    if await AsyncQueryUser.is_user(message.from_user.id):
        await state.set_state(TransactionsForm.category)
        await state.update_data(type=TransactionsType.expenses)
        category = await AsyncQueryCategory.get_category_type(TransactionsType.expenses)
        await message.answer(
            "Выберите категорию расходов 📈",
            reply_markup=await reply_keyboard_builder_category(
                category
            ),
        )
        await message.answer('↩ Нажмите кнопку если хотите вернуться назад', reply_markup=inline_back_transaction)
    else:
        await message.answer("Для дальнейшей работы зарегистрируйтесь /registration")


@router.message(F.text == "Добавить доходы 📉")
async def add_income(message: Message, state: FSMContext) -> None:

    if await AsyncQueryUser.is_user(message.from_user.id):
        await state.update_data(type=TransactionsType.income)
        await state.set_state(TransactionsForm.category)
        category = await AsyncQueryCategory.get_category_type(TransactionsType.income)
        await message.answer(
            "Выберите категорию доходов 📉",
            reply_markup=await reply_keyboard_builder_category(category),
        )
        await message.answer('↩ Нажмите кнопку если хотите вернуться назад', reply_markup=inline_back_transaction)
    else:
        await message.answer("Для дальнейшей работы зарегистрируйтесь /registration")


@router.message(TransactionsForm.category)
async def form_category(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    category_get = await AsyncQueryCategory.get_category_title_and_type(message.text, data['type'])
    if not category_get:
        await message.reply("Пожалуйста, введите корректную категорию❗")
    else:
        await state.update_data(category=message.text)
        await state.set_state(TransactionsForm.amount)
        await message.answer("💵 Введите сумму транзакции или ↩ нажмите кнопку назад", reply_markup=inline_back_transaction)


@router.message(TransactionsForm.amount)
async def form_amount(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        await state.update_data(amount=message.text)
        data = await state.get_data()
        await state.clear()
        if data['type'] == TransactionsType.income:
            category = await AsyncQueryCategory.get_category_title_and_type(
                data["category"], TransactionsType.income
            )
        else:
            category = await AsyncQueryCategory.get_category_title_and_type(
                data["category"], TransactionsType.expenses
            )
        user_tg_id = message.from_user.id
        user = await AsyncQueryUser.get_user(user_tg_id)
        try:
            await AsyncQueryTransactions.create_transactions(
                int(data["amount"]),
                category.id,
                user.id,
            )
            message_text = "Ваши доходы записаны 💵" if data['type'] == TransactionsType.income else "Ваши расходы записаны 💵"

            await message.answer(message_text, reply_markup=management)

        except:
            await message.answer(
                "Что-то пошло не так повторите операцию еще раз 😔",
                reply_markup=management,
            )
    else:
        await message.answer("Введите число еще раз❗")

# ------------------------------------------УСТАНОВКА ИЗМЕНЕНИЯ ЛЮМИТА---------------------------------------------------------------------


@router.message(F.text == 'Настройки ⚙️')
async def settings(message: Message) -> None:
    if await AsyncQueryUser.is_user(message.from_user.id):
        await message.answer("Выберите действия ↓", reply_markup=settings_reply_Keyboard)
        await message.answer('↩ Главное меню', reply_markup=inline_back_limite)
    else:
        await message.answer("Для дальнейшей работы зарегистрируйтесь /registration")


@router.message(F.text == 'Установить люмит 🚫')
async def settings(message: Message, state: FSMContext) -> None:
    await state.update_data(type_limit='add')
    await state.set_state(BudgetsForm.category)
    category = await AsyncQueryCategory.get_category_type(TransactionsType.expenses)
    await message.answer("Выберите категории расходов 📈", reply_markup=await reply_keyboard_builder_category(category))
    await message.answer('Нажмите кнопку если хотите вернуться назад', reply_markup=inline_back_limite)


@router.message(F.text == 'Изменить люмит 🚫')
async def settings(message: Message, state: FSMContext) -> None:
    await state.update_data(type_limit='update')
    await state.set_state(BudgetsForm.category)
    user = await AsyncQueryUser.get_user(message.from_user.id)
    month, year = datetime.datetime.now().month, datetime.datetime.now().year
    budgets_category = await AsyncQueryJoin.get_user_budget_categories(user.id, month, year)
    if budgets_category:
        await message.answer('Выберите категорию для изменения бюджета', reply_markup=await reply_keyboard_builder_category(budgets_category))
        await message.answer('Нажмите кнопку если хотите вернуться назад', reply_markup=inline_back_limite)
    else:
        await message.answer('Сначала установите люмиты', reply_markup=settings_reply_Keyboard)
        await message.answer('Нажмите кнопку если хотите вернуться назад', reply_markup=inline_back_limite)


@router.message(BudgetsForm.category)
async def form_category(message: Message, state: FSMContext) -> None:
    category_get = await AsyncQueryCategory.get_category_title_and_type(message.text, TransactionsType.expenses)
    if not category_get:
        await message.reply("Пожалуйста, введите корректную категорию❗")
    else:
        user_tg_id = message.from_user.id
        user = await AsyncQueryUser.get_user(user_tg_id)
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        data = await state.get_data()
        if data['type_limit'] == 'add':
            if not await AsyncQueryBudgets.get_budgets(user.id, category_get.id, month, year):
                await state.update_data(category=message.text)
                await state.set_state(BudgetsForm.limit)
                await message.answer(f"Введите сумму люмита на расходы -> '{message.text} или вернитесь назад'", reply_markup=inline_back_limite)
            else:
                await message.reply("У вас уже установлен люмит на данную категорию!")
        elif data['type_limit'] == 'update':
            await state.update_data(category=message.text)
            await state.set_state(BudgetsForm.limit)
            await message.answer(f"Введите сумму для изменения люмита на расходы -> '{message.text} или вернитесь назад'", reply_markup=inline_back_limite)
        else:
            await message.answer('Ваше действие не определено, поавторите еще раз!!!')


@router.message(BudgetsForm.limit)
async def form_amount(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        await state.update_data(limit=message.text)
        data = await state.get_data()
        await state.clear()
        category = await AsyncQueryCategory.get_category_title_and_type(data['category'], TransactionsType.expenses)
        user_tg_id = message.from_user.id
        user = await AsyncQueryUser.get_user(user_tg_id)
        month, year = datetime.datetime.now().month, datetime.datetime.now().year
        if data['type_limit'] == 'add':
            await AsyncQueryBudgets.create_budget(int(data['limit']), user.id, category.id, month, year)
        elif data['type_limit'] == 'update':
            budget = await AsyncQueryBudgets.get_budgets(user.id, category.id, month, year)
            await AsyncQueryBudgets.update_budget_limit(budget.id, int(data['limit']))
        text = 'установили' if data['type_limit'] == 'add' else 'обновили'
        await message.answer(f"Вы {text} люмит {data['limit']} рублей на '{data['category']}'", reply_markup=management)
    else:
        await message.answer("Вы ввели не число❗")


@router.message(F.text == 'Удалить люмит 🚫')
async def settings(message: Message, state: FSMContext) -> None:
    await state.set_state(ApprovalForm.category)
    user = await AsyncQueryUser.get_user(message.from_user.id)
    month, year = datetime.datetime.now().month, datetime.datetime.now().year
    budgets_category = await AsyncQueryJoin.get_user_budget_categories(user.id, month, year)
    if budgets_category:
        await message.answer('Выберите категорию для удаления бюджета', reply_markup=await reply_keyboard_builder_category(budgets_category))
        await message.answer('Нажмите кнопку если хотите вернуться назад', reply_markup=inline_back_limite)
    else:
        await message.answer('Сначала установите люмиты', reply_markup=settings_reply_Keyboard)
        await message.answer('Нажмите кнопку если хотите вернуться назад', reply_markup=inline_back_limite)


@router.message(ApprovalForm.category)
async def form_category(message: Message, state: FSMContext) -> None:
    category_get = await AsyncQueryCategory.get_category_title_and_type(message.text, TransactionsType.expenses)
    if not category_get:
        await message.reply("Пожалуйста, введите корректную категорию❗")
    else:
        user_tg_id = message.from_user.id
        user = await AsyncQueryUser.get_user(user_tg_id)
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        if await AsyncQueryBudgets.get_budgets(user.id, category_get.id, month, year):
            await state.update_data(category=message.text)
            await state.set_state(ApprovalForm.approval)
            await message.answer(f"Вы точно хотите удалить люмит на категорию?", reply_markup=yes_no)
        else:
            await message.reply("У вас не установлен люмит на данную категорию!")


@router.message(ApprovalForm.approval)
async def form_category(message: Message, state: FSMContext) -> None:
    if message.text == 'Да':
        await state.update_data(approval=message.text)
        data = await state.get_data()
        await state.clear()
        category = await AsyncQueryCategory.get_category_title_and_type(data['category'], TransactionsType.expenses)
        user_tg_id = message.from_user.id
        user = await AsyncQueryUser.get_user(user_tg_id)
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        budgets = await AsyncQueryBudgets.get_budgets(user.id, category.id, month, year)
        await AsyncQueryBudgets.delete_budget(budgets.id)
        await message.answer(f"Вы удалили люмит на '{data['category']}' ", reply_markup=management)
    elif message.text == 'Нет':
        await state.clear()
        await message.answer("Выберите действие", reply_markup=settings_reply_Keyboard)
        await message.answer('↩ Главное меню', reply_markup=inline_back_limite)
    else:
        await message.answer("Сделайте правильное действие")


# ---------------------------------------------СТАТИСТИКА-------------------------------------------------------------------------------------------

@router.message(F.text == 'Моя статистика 📊')
async def settings(message: Message) -> None:
    user_tg_id = message.from_user.id
    user = await AsyncQueryUser.get_user(user_tg_id)
    today = datetime.datetime.utcnow()
    start_date = today - datetime.timedelta(days=30)

    statistics = await AsyncQueryJoin.get_statistics_by_date_and_category(start_date, today, user.id)

    if not statistics:
        await message.answer("Нет данных за выбранный период.")
        return

    stats_message = "Статистика по категориям за последние 30 дней:\n\n"
    for category, total_amount in statistics:
        stats_message += f"{category}: {total_amount} рублей\n"

    await message.answer(stats_message)

# ----------------------------------------------ОБРАБОТЧИКИ КНОПОК НАЗАД----------------------------------------------------------------------------------


@router.callback_query(F.data == 'back_transaction')
async def back(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == TransactionsForm.amount.state:
        await state.set_state(TransactionsForm.category)
        data = await state.get_data()
        category = await AsyncQueryCategory.get_category_type(data['type'])
        await callback.message.answer("Выберите категорию 📝", reply_markup=await reply_keyboard_builder_category(category))
        await callback.message.edit_text('↩ Главное меню', reply_markup=inline_back_transaction)
    elif current_state == TransactionsForm.category.state:
        await state.clear()
        await callback.message.answer("Вы вернулись в главное меню 📑", reply_markup=management)
    await callback.answer('Вы вернулись назад')


@router.callback_query(F.data == 'back_limit')
async def back(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    data = await state.get_data()
    if current_state == BudgetsForm.limit.state:
        await state.set_state(BudgetsForm.category)
        if data['type_limit'] == 'add':
            category = await AsyncQueryCategory.get_category_type(TransactionsType.expenses)
        else:
            user = await AsyncQueryUser.get_user(callback.from_user.id)
            month, year = datetime.datetime.now().month, datetime.datetime.now().year
            category = await AsyncQueryJoin.get_user_budget_categories(user.id, month, year)
        await callback.message.answer("Выберите категории расходов 📈", reply_markup=await reply_keyboard_builder_category(category))
        await callback.message.answer('↩ Вернуться назад', reply_markup=inline_back_limite)
    elif current_state == BudgetsForm.category.state:
        await state.clear()
        await callback.message.answer("Выберите действие", reply_markup=settings_reply_Keyboard)
        await callback.message.answer('↩ Главное меню', reply_markup=inline_back_limite)

    else:
        await callback.message.answer("Вы вернулись в главное меню 📑", reply_markup=management)
    await callback.answer('Вы вернулись назад')
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
