from aiogram.dispatcher.filters.state import StatesGroup, State


class AddProduct(StatesGroup):
    name = State()
    description = State()
    count = State()
    price = State()
    photo = State()
    confirm_product = State()
    notify_about_product = State()


class MessageSubs(StatesGroup):
    message = State()


