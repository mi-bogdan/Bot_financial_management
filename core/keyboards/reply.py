from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder




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
        [
            KeyboardButton(text="Удалить люмит 🚫"),
        ],
    ],
    resize_keyboard=True,
)

yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет")
        ],

    ],
    resize_keyboard=True,
)




async def reply_keyboard_builder_category(categories):
    keyboard = ReplyKeyboardBuilder()
    for cat in categories:
        keyboard.add(KeyboardButton(text=cat.title))
    return keyboard.adjust(2).as_markup(resize_keyboard=True)
