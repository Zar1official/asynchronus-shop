import motor.motor_asyncio


class DB:
    def __init__(self, key, db_name, coll_name):
        self.cluster = motor.motor_asyncio.AsyncIOMotorClient(key)
        self.db = self.cluster[f'{db_name}']
        self.collection = self.db[f'{coll_name}']

