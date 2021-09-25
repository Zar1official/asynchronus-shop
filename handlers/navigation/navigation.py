from aiogram import types
from loader import dp, bot, subscribeDB, adminsDB
from markups import subscribe_mailing_markups, admin_markups, basket_markups
from utils.navigation_utils import send_products
from utils.basket_utils import set_prices
from states import Basket, BuyProduct
from config import YOO_TOKEN


@dp.message_handler()
async def navigation(message: types.Message):
    if message.text == "Товары 🔥":
        await BuyProduct.buy.set()
        await send_products(bot, message.from_user.id)
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
    elif message.text == "Корзина 🧺":
        prices = await set_prices(message.from_user.id)
        if prices is not None:
            await bot.send_invoice(
                message.from_user.id,
                title=f"Заказ №{message.from_user.id}",
                description="Товары в корзине:",
                provider_token=YOO_TOKEN,
                currency='rub',
                is_flexible=False,
                prices=prices,
                start_parameter='basket',
                payload=f'pay_{message.from_user.id}',
                reply_markup=basket_markups.basket_nav,
            )
            await Basket.on_buy.set()
        else:
            await message.answer("Корзина пуста!")
