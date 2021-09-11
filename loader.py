from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
import asyncio

from dbs.mongo_db import SubDB, ShopDB

loop = asyncio.get_event_loop()
bot = Bot(token=config.TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, loop, storage)
subscribeDB = SubDB(config.MONGO_KEY_2, config.SUBSCRIBE_DB_NAME, config.SUBSCRIBE_DB_COLLECTION)
shopDB = ShopDB(config.MONGO_KEY_1, config.SHOP_DB_NAME, config.SHOP_DB_COLLECTION)



