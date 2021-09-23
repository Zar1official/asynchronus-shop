from aiogram import types
from loader import basketDB


async def set_prices(user_id):
    basket_data = await basketDB.get_basket(user_id)
    if basket_data:
        prices = []
        for doc in basket_data:
            prices.append(
                types.LabeledPrice(label=f"{doc['product_name']} - {doc['product_count']} шт.",
                                   amount=doc['product_count'] * doc['product_price'] * 100))
        return prices
    return None
