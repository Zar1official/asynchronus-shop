import motor.motor_asyncio
from bson import ObjectId


class DB:
    def __init__(self, key, db_name, coll_name):
        self.cluster = motor.motor_asyncio.AsyncIOMotorClient(key)
        self.db = self.cluster[f'{db_name}']
        self.collection = self.db[f'{coll_name}']


class SubDB(DB):
    async def add_user(self, user_id):
        await self.collection.insert_one(
            {
                "_id": user_id
            }
        )

    async def delete_user(self, user_id):
        await self.collection.delete_one(
            {
                "_id": user_id
            }
        )

    async def user_exists(self, user_id):
        result = await self.collection.find_one(
            {
                "_id": user_id
            }
        )
        return result

    async def get_users(self):
        cursor = self.collection.find({})
        result = []
        async for document in cursor:
            result.append(document)
        return result


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
        cursor = self.collection.find({})
        result = []
        async for document in cursor:
            result.append(document)
        return result

    async def edit_product(self, product_id, key, value):
        await self.collection.update_one({"_id": ObjectId(product_id)}, {"$set": {key: value}})

    async def get_product_data(self, product_id):
        return await self.collection.find_one({"_id": ObjectId(product_id)})

