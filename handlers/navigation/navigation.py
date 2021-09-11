from aiogram import types
import config
from loader import dp, subscribeDB
from markups import subscribe_mailing_markups, admin_markups


@dp.message_handler()
async def navigation(message: types.Message):
    if message.text == "Товары 🔥":
        pass
    elif message.text == "Рассылка ✉":
        if await subscribeDB.user_exists(message.from_user.id):
            await message.answer('Отписаться от рассылки?',
                                 reply_markup=subscribe_mailing_markups.un_sub_mailing
                                 )
        else:
            await message.answer('Подписаться на рассылку?',
                                 reply_markup=subscribe_mailing_markups.sub_mailing
                                 )
    elif message.text == "Админ 👨":
        if message.from_user.id not in config.ADMIN_IDS:
            await message.answer('Вы не админ!')
        else:
            await message.answer(text="Панель администратора",
                                 reply_markup=admin_markups.admin_nav
                                 )
