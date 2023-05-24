import pymongo
import config

class MongoConnect:

    def __init__(self):
        try:
          self.connect = pymongo.MongoClient(
            host = config.HOST,
            port = config.PORT
          )

          self.db = self.connect.get_database(config.DB_NAME)
        except Exception as e:
          print("Deu ruim boy")
    
    def get_collection(self, collection):
        return self.db.get_collection(collection)
