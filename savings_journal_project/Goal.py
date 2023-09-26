from urllib import request
from savings_journal_project.PydanticObjectId import PydanticObjectId
from savings_journal_project.app import db
from datetime import date
from flask import Flask, request, jsonify
from pymongo.collection import ReturnDocument


class Goal(Resource):

    def __init__(self, title, amount, deadline, notes):
        self._title = title
        self._amount = amount
        self._deadline = deadline
        self._notes = notes

    # title
    def get_title(self):
        return self._title

    def set_title(self, x):
        self._title = x

    # amount
    def get_amount(self):
        return self._amount

    def set_amount(self, x):
        self._amount = x

    # deadline
    def get_deadline(self):
        return self._deadline

    def set_deadline(self, x):
        self._deadline = x

    # notes
    def get_notes(self):
        return self._notes

    def set_notes(self, x):
        self._notes = x

        # w
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


"""
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
    """


