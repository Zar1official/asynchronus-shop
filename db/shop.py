from .database import DB
from bson import ObjectId


class ShopDB(DB):
    async def add_product(self, product_name, product_description,
                          product_count, product_price, product_photo):
        await self.collection.insert_one(
            {
                "name": product_name,
                "description": product_description,
                "count": product_count,
                "price": product_price,
                "photo": product_photo
            }
        )

    async def remove_product(self, product_id):
        await self.collection.delete_many({"_id": ObjectId(product_id)})

    async def clean_shop(self):
        await self.collection.delete_many({})

    async def get_products(self):
        await super().get_all_data()

    async def edit_product(self, product_id, key, value):
        await self.collection.update_one({"_id": ObjectId(product_id)}, {"$set": {key: value}})

    async def get_product_data(self, product_id):
        return await self.collection.find_one({"_id": ObjectId(product_id)})

    async def get_product_attr(self, product_id, key):
        data = await self.get_product_data(product_id)
        return data[key]