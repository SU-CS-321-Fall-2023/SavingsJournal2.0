from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def get_database():
    uri = "mongodb+srv://Cluster61649:UWFPfm9BXGFp@cluster61649.dcrddgj.mongodb.net/?retryWrites=true&w=majority"
    # uri = "mongodb+srv://cluster61649.dcrddgj.mongodb.net"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # Create the database
    return client['user']
