import pymongo
from flask_mongoengine import MongoEngine
from flask import Flask

app = Flask('my_app')

app.config['MONGODB_SETTINGS'] = {
    'db': 'geolocation_database',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db_init=db.init_app(app)


def check_db_connection():
    try:
        client = pymongo.MongoClient(host=app.config['MONGODB_SETTINGS']['host'],
                                     port=app.config['MONGODB_SETTINGS']['port'],
                                     serverSelectionTimeoutMS=1000)
        client.server_info()  # force connection on a request as the
        if app.config['MONGODB_SETTINGS']['db'] not in client.list_database_names():
            return False
        return True
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(err)
        return False
