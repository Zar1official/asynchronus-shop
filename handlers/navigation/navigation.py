from aiogram import types
from loader import dp, subscribeDB, adminsDB
from markups import subscribe_mailing_markups, admin_markups
from utils.navigation_utils import send_products


@dp.message_handler()
async def navigation(message: types.Message):
    if message.text == "Товары 🔥":
        await send_products(dp, message.from_user.id)
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
        if not await adminsDB.is_admin(message.from_user.id):
            await message.answer('Вы не админ!')
        else:
            await message.answer(text="Панель администратора",
                                 reply_markup=admin_markups.admin_nav
                                 )
