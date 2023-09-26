# creating a collection
# Get the database using the method we defined in pymongo_test_insert file

# for app.py file
# connecting Flask, App to Mongo Database

# how do we make entries on the web page?
    # how do the users type
    # how is the data received?
# when are we calling these functions? or are they called by the routings?
from pymongo.server_api import ServerApi
from flask import Flask
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from flask_restful import Resource
import Goal
import User
import collections_models

app = Flask(__name__)
uri = "mongodb+srv://Cluster61649:UWFPfm9BXGFp@cluster61649.dcrddgj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.flask_db
users = db.users
goals = db.goals

client.add_resource(User, '/')
client.add_resource(Goal, '/')
client.add_resource(collections_models.py, '/')


# code to insert/ do whatever operations

client.close()
# signup
# log in
# log out
# homepage
@app.route("/")
def home_page():
    online_users = mongo.db.users.find({"online": True})
    return render_template("index.html",
        online_users=online_users)

"""

# example
# get these as inputs from the user # user_1 = User(email_in, password_in, name_in)
# make password private (bcrypt)
# could we just use the email as the userID?
user_1 = User("jimmy@gmail.com", "vhhbeflhbfel2", "Jimmy")
# generate a random userID--put this in a method in User class
# this will all go into a function in user class for saving data
user_1.save_user(user_ID, user_1.get_name(), user_1.get_email(), user_1.get_password())
user_1.get_user()
user_1.get_user_info()

# function to add a goal to a user
goal_1 = Goal("Buy a Car", "$26,000", "June 2024", "Subaru Crosstrek")
user_1.add_goal(goal_1)
user_1.delete_goal(goal_1)

"""


"""
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from pymongo.collection import Collection, ReturnDocument
import flask
from flask import Flask, request, url_for, jsonify
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError
from collections_models import User
from collections_models import Goal
import PydanticObjectId
from pymongo_get_database import get_database
import User
import Goal

#Secret key?
app = Flask(__name__)
# other method to connect Flask-mongo
# app.config['SECRET KEY'] = 'what goes here?'
# app.config['MONGO_dbname'] = 'users'
# app.config["MONGO_URI"] = "mongodb+srv://Cluster61649:UWFPfm9BXGFp@cluster61649.dcrddgj.mongodb.net/?retryWrites=true&w=majority"
# mongo = PyMongo(app)
# users: Collection = pymongo.db.users
# goals: Collection = pymongo.db.goals
"""