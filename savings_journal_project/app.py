from pymongo.server_api import ServerApi
from flask import Flask, render_template, request, url_for, session, redirect, flash
from pymongo import MongoClient
import bcrypt
from pydantic import BaseModel, ValidationError
from typing import Optional, List
from datetime import date


class User(BaseModel):
    username: str
    email: str
    password: str
    goals: Optional[List]  # goal ids


class Goal(BaseModel):  # each goal will have the username
    title: str
    amount: int
    deadline: date
    notes: Optional[str]
    username: str


app = Flask(__name__)
uri = "mongodb+srv://Cluster61649:UWFPfm9BXGFp@cluster61649.dcrddgj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.flask_db


# db.users
# db.goals

# client.add_resource(User, '/user/<string:username>')
# client.add_resource(Goal, '/user/<string:username/goal/<string:title>')

def add_user(hashed):
    user = db.users.insert_one(
        {'username': request.form['username'],
         'password': hashed,
         'email': request.form['email']})
    try:
        User.model_validate_json(user)
    except ValidationError as e:
        print(e)


@app.route('/')
def index():  # adjust this to go to whatever page we want it to go to after logging in
    #if 'username' in session:
        #return 'Welcome, ' + session['username'] + '!'
    return render_template('index.html') # sign in menu

@app.route('/index2/')
def index2():  # adjust this to go to whatever page we want it to go to after logging in
    #if 'username' in session:
        #return 'Welcome, ' + session['username'] + '!'
    return render_template('index2.html/') # savings journal menu

@app.route("/signup/", methods=['POST', 'GET'])
def signup():  # gets username, password, email and adds to user collection
    # allow user to register if post
    if request.method == 'POST':
        user = db.users.find_one({'username': request.form['username']})
        if user is None:
            hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            add_user(hashed)
            session['username'] = request.form['username']
            # flash(session['username'])
            return redirect(url_for('index2'))
        return redirect(url_for('signin'))  # where user exists already
    return render_template('signup.html')  # where it's a get not a post request


@app.route('/signin/', methods=['POST'])
def signin():
    user = db.users.find_one({'username': request.form['username']})
    if user:  # compare passwords
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), user['password'].encode('utf-8')) == \
                user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index2')) # takes you to page for savings journal menu
        return 'Invalid username or password.'

 
@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('signin'))


def add_goal(goal_id):
    # add new goal to the user's list of goals
    # don't need to return anything or connect to a routing
    user = db.users.find_one({'username': session['username']})
    goals = user.get['goals']
    goals.append(goal_id)


def remove_goal(goal_id):
    # add new goal to the user's list of goals
    # don't need to return anything or connect to a routing
    user = db.users.find_one({'username': session['username']})
    goals = user.get['goals']
    goals.remove(goal_id)


# does the context for goal/goal_id have to be goal_id or _id or just goal?
@app.route("/goal/", methods=['POST', 'GET'])
def create_goal():
    # create goal--adding data to mongo and going back to savings journal page (or goal page?)
    if request.method == 'POST':
        username = session['username']
        goal = {
            "title": request.form['title'],  # required
            "amount": request.form['amount'],  # required
            "deadline": request.form['deadline'],  # required
            "notes": request.form['notes'],
            "username": username  # required
        }
        try:
            Goal.model_validate_json(goal)
            db.goals.insert_one(goal)
            add_goal(username, goal['_id'])
            return render_template('goal/<goal_id>.html', goal_id=goal['_id'])
        except ValidationError as e:
            return e
    return render_template('goal.html')  # if a GET request (just the blank goal form)


# @app.route("/user/<string:username>/goal/", methods=['GET'])
# can't edit anything on this page so no Posting, Deleting, or Patching
def get_goal_list():
    username = session['username']
    user_goals = db.goals.find({"username": username})  # find goals by user _id
    user_goal_list = []
    if user_goals:
        for goal in user_goals:
            user_goal_list.add(goal)
        return user_goal_list
    return None # if no user goals

@app.route("/savings_journal/", methods=['GET'])
def list_goals():
    # list all goals for the user
    user_goal_list = get_goal_list()
    if user_goal_list():
        return render_template('savings_journal.html', goals=user_goal_list)
    return redirect(url_for('goal'))  # if no goals exist yet, give option to create one


# @app.route("/user/<string:username>/goal/<PydanticObjectId:_id>", methods=['GET'])
# access a single goal only through the savings journal page where all the goals are
# so put savings journal in the route?
@app.route("/goal/<goal_id>/", methods=['GET', 'DELETE', 'PATCH'])
def goal(_id):
    goal = db.goals.find_one_or_404({'_id': _id})
    if request.method == 'GET':
        return render_template('/goal/<goal_id>.html', goal=goal)  # view the goal
    if request.method == 'DELETE':
        remove_goal(goal['_id'])  # remove goal from user list
        db.goals.remove(goal)
        flash('Goal removed!')
        return redirect(url_for('savings_journal'))  # see the remaining goals
    if request.method == 'PATCH':
        goal = db.goals.find_one_and_update({'_id': _id}, {'$set':
                                                               {"title": request.form['title'],
                                                                "amount": request.form['amount'],
                                                                "deadline": request.form['deadline'],
                                                                "notes": request.form['notes']}
                                                           })
        try:  # check schema after update
            Goal.model_validate_json(goal)
            return render_template('goal/<goal_id>.html', goal_id=goal['_id'])  # view the goal
        except ValidationError as e:
            return e


if __name__ == '__main__':
    app.run(debug=True)

# mongo connection closes
# client.close()

"""
    @app.route("/savings_journal/post/<string:goal._id>", methods=['POST']) # create new entry on savings journal page
    @app.route("/goals/post/<string:goal._id>", methods=['POST']) #create new entry on goals page
    def save_goal(self):
        #user_id = self.get_user_id()
        goal_create = request.get_json()
        goal = Goal(**goal_create)
        insert_result = db.goals.insert_one(goal.to_bson()) #goal.dict()?
        goal.id = PydanticObjectId(str(insert_result.inserted_id))
    @app.route("/savings_journal/<string:goal._id>", methods=['GET'])
    def get_goal_info(self):
        # get one goal
        goal = db.goals.find_one_or_404({'_id':self._id})
        return Goal(**goal).to_json()

    @app.route("/", methods=['GET'])
    def get_goal_piece(self, info_piece):
    # could get whatever field you want return user.get("_id")
    #user = db.users.find_one(self._id)
        return self._id.get(info_piece)

    @app.route("/goals/delete/<str ing:goal._id>", methods=['DELETE'])
    @app.route("/savings_journal/delete/<string:goal._id>", methods=['DELETE'])
    def delete_goal(self):
    # delete a  goal
        db.goals.remove(self._id)
    @app.route("/saving_journal/edit/<string:goal._id>", methods=['PATCH'])
    @app.route("/saving_journal/edit/<string:goal._id>", methods=['PATCH'])
    def update_goal(self):
    # update goal entry
        goal = Goal(**request.get_json())
        updated_goal = db.goals.find_one_and_update(
            {"_id": self._id},
            {"$set" : goal.to_bson()},
            return_document = ReturnDocument.AFTER,
        )
        if updated_goal:
            return Goal(**updated_goal.to_json())
        else:
            flask.abort(404, 'Goal not found')

    def save_goal_info(self, goal_ID, title, amount, deadline, notes):
        # save to Mongo in dictionary type style
        # Mongodb document (JSON-style) inserting into collection
        goal_ID = {
            "title": title,
            "amount": amount,
            "deadline": deadline,
            "notes": notes
        }
        user_collection.insert_one([goal_ID])  # for a single document
        # user_collection.insert_many([user_1,user_2]) # for multiple docs

    def show_goals(self, user_ID):
        # call savings journal page and goal page
        # viewing all the users dictionaries
        # Retrieve a collection named "user_info" from database
        user_goals = user_collection.find(user_ID)
        # change the format this is returned in
        # change what info is returned
        for goal in user_goals:
            print(goal)

    # function to search for something specific (ex like a goal?)
    # indexing
    # user_details = user_collection.find({"email": user_1.get_email()})

    def get_goal_info(self, user_ID, goal_ID):

    def update_goal(self, goal):



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
