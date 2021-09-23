from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

basket_nav = InlineKeyboardMarkup().add(InlineKeyboardButton("Оплатить", pay=True)).add(
                                        InlineKeyboardButton("Отменить заказ", callback_data="remove_basket")).add(
                                        InlineKeyboardButton("Назад", callback_data="cancel_basket")
)