from urllib import request
from savings_journal_project.main import user_collection, db
from savings_journal_project.main import goal_collection
from datetime import date
from flask import Flask, request, jsonify


class Goal:

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

    # model.py
    class Goal(BaseModel): #each goal will have the user ID
        goal_id: Optional[PydanticObjectId] = Field(None, alias="_id")
        #slug: str
        user_id : int
        title: str
        amount: int
        deadline: date
        notes: str
        #date_added: Optional[datetime]
        #date_updated: Optional[datetime]

        def to_json(self):
            return jsonable_encoder(self, exclude_none=True)

        def to_bson(self):
            data = self.dict(by_alias=True, exclude_none=True)
            if data["_id"] is None:
                data.pop("_id")
            return data

        #change print style
        @app.route("/get/<user_id>", methods=['GET'])
        def get_all_goals(user_id):
            user_goals = goal_collection.find({"user_id": int(user_id)})
            for goal in user_goals:
                print(goal) #dispaly as dictionaries

        #change print style
        @app.route("/get/<user_id>", methods=['GET'])
        def get_one_goal(user_id, title): #might not search by goal_id
            goal = user_collection.find_one({"user_id": int(user_id), 'title': title})
            return goal #as dictionary


        @app.route("/edit/<goal_id>", methods=['POST'])
        @app.route("/delete/<goal_id>", methods=['DELETE'])
        @app.route("/", methods=['POST'])

    #

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


