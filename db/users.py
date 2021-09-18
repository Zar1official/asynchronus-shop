from .database import DB


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


class AdminsDB(DB):

    async def add_admin(self, user_id, user_name):
        await self.collection.insert_one(
            {
                "user_id": int(user_id),
                "user_name": user_name
            }
        )

    async def get_admins(self):
        cursor = self.collection.find({})
        result = []
        async for document in cursor:
            result.append(document["user_id"])
        return result

    async def remove_admin(self, user_id):
        await self.collection.delete_one(
            {
                "user_id": user_id
            }
        )

    async def admin_exists(self, user_id):
        result = await self.collection.find_one(
            {
                "user_id": int(user_id)
            }
        )
        return result
