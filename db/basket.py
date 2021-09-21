from .database import DB


class BasketDB(DB):
    async def get_basket(self, user_id):
        cursor = self.collection.find({"user_id": user_id})
        result = []
        async for document in cursor:
            result.append(document)
        return result

    async def add_to_basket(self, user_id, product_id, product_name, product_price):
        await self.collection.insert_one(
            {
                "user_id": user_id,
                "product_id": product_id,
                "product_name": product_name,
                "product_count": 1,
                "product_price": product_price
            }
        )

    async def is_in_basket(self, user_id, product_id):
        result = await self.collection.find_one(
            {
                "user_id": user_id,
                "product_id": product_id
            }
        )
        return result

    async def update_in_basket(self, user_id, product_id):
        count = await self.get_attr_in_basket(user_id, product_id, "product_count")
        await self.collection.update_one({"product_id": product_id}, {"$set": {"product_count": count + 1}})

    async def get_attr_in_basket(self, user_id, product_id, attr):
        result = await self.is_in_basket(user_id, product_id)
        return result[attr]

    async def remove_basket(self, user_id):
        print(user_id)
        await self.collection.delete_many({"user_id": user_id})
