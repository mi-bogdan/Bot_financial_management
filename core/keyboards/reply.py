from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from core.db.queries import AsyncQueryCategory


management = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Моя статистика 📊"),
            KeyboardButton(text="Настройки ⚙️")],
        [
            KeyboardButton(text="Добавить доходы 📉"),
            KeyboardButton(text="Добавить расходы 📈"),
        ],
    ],
    resize_keyboard=True,
)

settings_reply_Keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Установить люмит 🚫"),
            KeyboardButton(text="Изменить люмит 🚫")
        ],
    ],
    resize_keyboard=True,
)


async def reply_keyboard_builder_category(transactions_type):
    category = await AsyncQueryCategory.get_category_type(transactions_type)
    keyboard = ReplyKeyboardBuilder()
    for cat in category:
        keyboard.add(KeyboardButton(text=cat.title))
    return keyboard.adjust(2).as_markup()
