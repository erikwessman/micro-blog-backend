from pymongo import MongoClient
from flask import current_app


class DBManager:
    __instance = None
    db_host = current_app.config["DB_HOST"]
    db_port = int(current_app.config["DB_PORT"])
    db_name = current_app.config["DB_NAME"]

    @staticmethod
    def get_db():
        if DBManager.__instance == None:
            DBManager()
        return DBManager.__instance[DBManager.db_name]

    def __init__(self):
        if DBManager.__instance != None:
            raise Exception("Only one instance of this class is allowed")
        else:
            try:
                print(
                    f'Attempting to connect to database with URL {self.db_host} and port {self.db_port}...')
                maxSevSelDelay = 1
                DBManager.__instance = MongoClient(
                    host=self.db_host, port=self.db_port, serverSelectionTimeoutMS=maxSevSelDelay)
                DBManager.__instance.server_info()
                print('Connected to database')
            except:
                print('Unable to connect to database')
                exit()
