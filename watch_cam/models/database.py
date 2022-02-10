from pymongo import MongoClient,DESCENDING
import os
from dotenv import load_dotenv
import json
class Database(object):
  def __init__(self):
    try:
      load_dotenv()
      #user = os.getenv("MONGODB_USERNAME")
      #password = os.getenv("MONGODB_PASSWORD")
      self.db_name = os.getenv("MONGODB_DATABASE")
      host = os.getenv("MONGODB_HOSTNAME", "localhost")
      connection_str = f"mongodb://{host}:27017"

      self.client = MongoClient(connection_str)
      print("Successfully connected to MongoDb")

    except Exception as error:
      print("Failed to Connect to MongoDb\n")
      print(error)

  def seed_ips(self):
    # when i set up port forwards for this app on my router, a decent amount of unwanted people tried to access my livestream app
    # luckily my internet provider blocked them and told me their ips, so i have been storing them in a json file so i can implement an ip banner/checker
    banned_ips = self.client[self.db_name]["ips"]
    ips = list(banned_ips.find({}))

    if len(ips) == 0:
      print("Seeding Banned Ip Collection...")
      with open('./data/ips.json') as file:
        file_data = json.load(file)
      banned_ips.insert_many(file_data)
      banned_ips.create_index([("ip", DESCENDING)],unique=True)
      print("Done Seeding!")
    else:
      print('Data exisits, no need to seed!')

  def get_one(self, collection, value):
    collection = self.client[self.db_name][collection]
    return collection.find_one(value)
