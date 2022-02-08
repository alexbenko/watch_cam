import pymongo
class Database(object):
  def __init__(self):
    self.client = pymongo.MongoClient
  def __del__(self):
    self.client.close()

