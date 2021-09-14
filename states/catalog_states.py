from aiogram.dispatcher.filters.state import StatesGroup, State


class BuyProduct(StatesGroup):
    buy = State()

