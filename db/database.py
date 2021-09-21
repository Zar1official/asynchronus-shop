from aiogram.utils.exceptions import ChatNotFound
import motor.motor_asyncio
from aiogram import Dispatcher


class DB:
    def __init__(self, key, db_name, coll_name):
        self.cluster = motor.motor_asyncio.AsyncIOMotorClient(key)
        self.db = self.cluster[f'{db_name}']
        self.collection = self.db[f'{coll_name}']

    @staticmethod
    def is_user_valid(user_id) -> bool:
        try:
            int(user_id)
        except ValueError:
            return False
        return True

    @staticmethod
    async def is_chat_valid(chat_id, dp: Dispatcher) -> bool:
        try:
            await dp.bot.get_chat(int(chat_id))
        except ChatNotFound:
            return False
        return True


