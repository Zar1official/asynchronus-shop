from aiogram.dispatcher.filters.state import StatesGroup, State


class Basket(StatesGroup):
    on_buy = State()
