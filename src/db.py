import pymongo
from flask import current_app
from urllib.parse import quote_plus


class DBManager:
    __instance = None
    db_host = current_app.config.get("DB_HOST") or 'localhost'
    db_name = current_app.config.get("DB_NAME") or 'micro-blog'
    db_user = current_app.config.get("DB_USER")
    db_pass = current_app.config.get("DB_PASS")

    if db_user:
        mongo_uri = "mongodb+srv://%s:%s@%s/?retryWrites=true&w=majority" % (
            quote_plus(db_user), quote_plus(db_pass), db_host)
    else:
        mongo_uri = "mongodb://" + db_host + "/?retryWrites=true&w=majority"

    @staticmethod
    def get_db():
        if DBManager.__instance == None:
            DBManager()
        return DBManager.__instance[current_app.config["DB_NAME"]]

    def __init__(self):
        if DBManager.__instance != None:
            raise Exception("Only one instance of this class is allowed")
        else:
            print(
                f'Attempting to connect to database with URL {self.mongo_uri}...')
            try:
                DBManager.__instance = pymongo.MongoClient(self.mongo_uri)
                try:
                    DBManager.__instance.server_info()
                except pymongo.errors.ConnectionFailure as e:
                    print(e)
                print('Connected to database')
            except Exception as e:
                print(e)
                print('Unable to connect to database')
                exit()

    def drop_all():
        if DBManager.__instance != None:
            DBManager.__instance.drop_database(current_app.config["DB_NAME"])
        else:
            raise Exception("No DB instance active")
