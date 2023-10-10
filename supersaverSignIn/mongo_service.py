import pymongo.server_api
from pymongo import MongoClient

uri = "mongodb+srv://Cluster61649:UWFPfm9BXGFp@cluster61649.dcrddgj.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=pymongo.server_api.ServerApi('1'))

# print message indicating attempt to connect to the database
print(f"Attempting to connect to database {uri}...")

if client:
    print("Successfully connected to database! {db.name}")

db = client.db
users = db.users
goals = db.goals