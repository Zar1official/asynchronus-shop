from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
import asyncio

from db import ShopDB, SubDB, AdminsDB, BasketDB

loop = asyncio.get_event_loop()
bot = Bot(token=config.TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, loop, storage)
subscribeDB = SubDB(config.MONGO_KEY_2, config.USERS_DB_NAME, config.SUBSCRIBE_COLLECTION)
shopDB = ShopDB(config.MONGO_KEY_1, config.SHOP_DB_NAME, config.SHOP_DB_COLLECTION)
adminsDB = AdminsDB(config.MONGO_KEY_2, config.USERS_DB_NAME, config.ADMINS_COLLECTION)
basketDB = BasketDB(config.MONGO_KEY_3, config.BASKET_DB_NAME, config.BASKET_COLLECTION)


