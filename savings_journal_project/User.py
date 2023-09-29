# pydantic/ id stuff
# routing
from typing import List
import flask
from savings_journal_project.PydanticObjectId import PydanticObjectId
from app import app, db
import Goal
from flask import Flask, request, jsonify, Resource
from pydantic import BaseModel


class User(BaseModel, Resource):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    slug: str
    username: str
    email: str
    password: str
    goals: List[Goal]

    # done
    @app.route("/user", methods=['POST', 'GET'])
    def add_user():
        # save all user info
        if request.method == 'POST':
        user_create = request.get_json()
        user = User(**user_create)
        insert_result = db.users.insert_one(user.to_bson())
        user.id = PydanticObjectId(str(insert_result.inserted_id))
        return user.to_json()
        return render_template("")

    # done
    @app.route("/user/<string: username>", methods=['GET'])
    def get_user(self, username):
        # get all user info
        user = db.users.find_one_or_404({"username": username})
        return User(**user).to_json()

    # done
    @app.route("/user/<string: username>", methods=['DELETE'])
    def delete_user(self, username):
        # delete a user
        user = db.users.find_one_and_delete({'username': username})
        if user:
            return User(**user).to_json()
        else:
            flask.abort(404, "Cocktail not found")

    # add the goal to the list
    @app.route("/user/<string:username>/goal", methods=['POST'])
    def add_goal(self, username):
        # create goal
        # id = self.get_user_id()
        goal_create = request.get_json()
        goal = Goal(**goal_create)
        insert_result = db.goals.insert_one(goal.to_bson())  # goal.dict()?
        goal.id = PydanticObjectId(str(insert_result.inserted_id))

        # add goal to list of goals for user
        user = self.get_user({'username': username})
        user.update_goal_list(username, goal.id)

    # figure out if this will update one field or more fields
    @app.route("/user/<string:username>/goal/<PydanticObjectId:_id>", methods=['PATCH'])
    def update_user(self, username, _id):
        goal = self.get_goal(username, _id)
        # update goal entry
        updated_user = db.users.find_one_and_update(
            {"username": username},
            {"$set": goal.to_bson()},
            return_document=ReturnDocument.AFTER,
        )
        if updated_user:
            return Goal(**updated_user.to_json())
        else:
            flask.abort(404, 'Goal not found')

    """ other method, not correct
    @app.route("/user/<_id>", methods =['GET'])
    def get_user_info(self, id):
    # get all user info
        user = db.users.find_one_or_404({"_id": id})
        return User(**user).to_json()
        return render_template("user.html",
            user=user)
    """


"""

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
