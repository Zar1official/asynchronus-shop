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
        await super().get_all_data()


class AdminsDB(DB):

    async def add_admin(self, user_id, user_name):
        await self.collection.insert_one(
            {
                "user_id": int(user_id),
                "user_name": user_name
            }
        )

    async def get_admins(self):
        await super().get_all_data()

    async def get_admins_ids(self):
        cursor = self.collection.find({})
        result = []
        async for document in cursor:
            result.append(document["user_id"])
        return result

    async def is_admin(self, user_id):
        admins = await self.get_admins_ids()
        return int(user_id) in admins

    async def remove_admin(self, user_id):
        await self.collection.delete_one(
            {
                "user_id": int(user_id)
            }
        )

    async def admin_exists(self, user_id):
        result = await self.collection.find_one(
            {
                "user_id": int(user_id)
            }
        )
        return result
