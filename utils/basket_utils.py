from aiogram import types
from loader import basketDB, shopDB


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


async def decrease_counts(user_id):
    basket_data = await basketDB.get_basket(user_id)
    for doc in basket_data:
        product_id = doc['product_id']
        product_count_in_basket = doc['product_count']
        product_count = await shopDB.get_product_attr(product_id, "count")
        if product_count == product_count_in_basket:
            await shopDB.remove_product(product_id)
        else:
            await shopDB.edit_product(product_id, "count", product_count - product_count_in_basket)

