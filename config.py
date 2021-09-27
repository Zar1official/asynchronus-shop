TOKEN = "BOT_TOKEN"
YOO_TOKEN = "YOOKASSA_TOKEN"

USER_NAME = "user_name"
USER_PASSWORD = "user_password"
CLUSTER_NAME = "Cluster0"

SHOP_DB_NAME = "products"
BASKET_DB_NAME = "basket"
USERS_DB_NAME = "users"

BASKET_COLLECTION = "customers"
SUBSCRIBE_COLLECTION = "subscribers"
ADMINS_COLLECTION = "admins"
SHOP_DB_COLLECTION = "catalog"


MONGO_KEY_1 = f"mongodb+srv://{USER_NAME}:{USER_PASSWORD}@{CLUSTER_NAME}.nyjf3.mongodb.net/{SHOP_DB_NAME}?retryWrites=true&w=majority"
MONGO_KEY_2 = f"mongodb+srv://{USER_NAME}:{USER_PASSWORD}@{CLUSTER_NAME}.nyjf3.mongodb.net/{USERS_DB_NAME}?retryWrites=true&w=majority"
MONGO_KEY_3 = f"mongodb+srv://{USER_NAME}:{USER_PASSWORD}@{CLUSTER_NAME}.nyjf3.mongodb.net/{BASKET_DB_NAME}?retryWrites=true&w=majority"
