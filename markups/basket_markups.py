from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

basket_nav = InlineKeyboardMarkup().add(InlineKeyboardButton("Оформить заказ", callback_data="confirm_basket")).add(
                                        InlineKeyboardButton("Отменить заказ", callback_data="cancel_basket")
)