from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.db.queries import AsyncQueryUser

router_register = Router()


@router_register.message(Command("registration"))
async def cmd_start(message: Message) -> None:
    user_data = message.from_user
    user = await AsyncQueryUser.get_user(user_data.id)
    if user is None:
        await AsyncQueryUser.create_user(
            tg_id=user_data.id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
        )
        await message.answer(f"Спасибо за регистрацияю, {user_data.first_name}")
    else:
        await message.answer(f"{user_data.first_name} Вы уже зарегистрированы")
