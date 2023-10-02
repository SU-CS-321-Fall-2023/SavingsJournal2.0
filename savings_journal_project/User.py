# pydantic/ id stuff
# routing
"""
from typing import List
import flask
from pymongo import ReturnDocument

import PydanticObjectId
import app
import Goal
from flask import Flask, request, jsonify, render_template, flash
from pydantic import BaseModel
from flask_restful import Resource
db = app.get_database()
class User(BaseModel, Resource):

    #mongo automatically generates the id--make sure this never repeats
    #id: Optional[PydanticObjectId] = Field(None, alias="_id")
    username: str
    email: str
    password: str
    goals: List[Goal]

    # done
    @app.route("/user", methods=['POST', 'GET'])
    def add_user(self, hashed):
        insert_result = db.users.insert(
            {'username': request.form['username'],
                'password': hashed,
                'email': request.form['email']})
        #self.id = PydanticObjectId(str(insert_result.inserted_id))
        insert_product = db.product.find_one({"_id": insert_result.inserted_id})
        if insert_product:
            return insert_result



        # save all user info
        if request.method == 'POST':
        user_create = request.get_json()
        user = User(**user_create)
        insert_result = db.users.insert_one(user.to_bson())
        user.id = PydanticObjectId(str(insert_result.inserted_id))
        return user.to_json()


don't need this yet
    @app.route("/user/<string: username>", methods=['GET'])
    def get_user(self, username):
        username = request.form['username'] # prompt user for username?
        # get all user info
        user = db.users.find_one_or_404({"username": username})
        return User(**user).to_json()



    # figure out if this will update one field or more fields
    @app.route("/user/<string:username>/goal/<PydanticObjectId:_id>", methods=['PATCH'])
    def update_user(self, username, _id, field, data):
        db.users.update_one({"_id": _id}, {"$set": {field: data}})
        goal = self.get_goal(username, _id)
        # update goal entry
        updated_user = db.users.find_one_and_update(
            {"username": username},
            {"$set": goal.to_bson()},
            return_document=ReturnDocument.AFTER,
        )
        if updated_user:
            flash('User information has been updated!')
            return Goal(**updated_user.to_json())
        else:
            flask.abort(404, 'Goal not found')

    # done
    @app.route("/user/<string: username>", methods=['DELETE'])
    def delete_user(self, username):
        # delete a user
        user = db.users.find_one_and_delete({'username': username})
        if user:
            flash('User has been deleted.')
            return render_template('signup.html')
        # user not found
        flask.abort(404, "User not found.")

    # figure out request.get_json()
    @app.route("/user/<string:username>/goal", methods=['POST'])
    def create_goal(self, username):
        # create goal
        goal = {
            "title": request.form['title'],
            "amount": request.form['amount'],
            "deadline": request.form['deadline'],
            "notes": request.form['notes'],
            "username": username
        }
        # goal_create = request.get_json()
        # goal = Goal(**goal_create)
        insert_result = db.goals.insert_one(goal.to_bson())  # goal.dict()?
        #goal.id = PydanticObjectId(str(insert_result.inserted_id))
        # id = self.get_user_id()
        goal.update_user_goals()

        # make update_goal_list_method
        # what to add to list
        @app.route("/user/<string:username>/goal", methods=['POST'])
        def update_user_goals():
            new_goal = request.get_json()
            username = db.goals.get['username']
            user = db.users.find_one({'username': username})
            goals = user.get['goals']
            goals.append(new_goal)



 other method, not correct
    @app.route("/user/<_id>", methods =['GET'])
    def get_user_info(self, id):
    # get all user info
        user = db.users.find_one_or_404({"_id": id})
        return User(**user).to_json()
        return render_template("user.html",
            user=user)





class User(Resource):
    def __init__(self, email, password, name):
        self._email = email
        self._password = password
        self._name = name

    # email
    def get_email(self):
        return self._email

    def set_email(self, x):
        self._email = x

    # password
    def get_password(self):
        return self._password

    def set_password(self, x):
        self._password = x

    # name
    def get_name(self):
        return self._name

    def set_name(self, x):
        self._name = x

"""
