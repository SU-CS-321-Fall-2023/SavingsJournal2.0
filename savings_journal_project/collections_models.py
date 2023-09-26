from savings_journal_project.PydanticObjectId import PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from flask_restful import Resource
from app import db


class User(BaseModel, Resource):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    slug: str
    name: str
    email: str
    password: str

    # routing
    @app.route("/", methods=['POST'])
    def save_user(self, User):
    # save all user info
        user_create = request.get_json()
        user = User(**user_create)
        insert_result = db.users.insert_one(user.to_bson())
        user.id = PydanticObjectId(str(insert_result.inserted_id))

    # routing?
    @app.route("/user/<_id>")
    def get_user_info(self):
    # get all user info
        user = db.users.find_one_or_404({"_id" :self._id})
        return User(**user).to_json()
        return render_template("user.html",
            user=user)

    #routing?
    #
    @app.route("/", methods=['GET'])
    def get_user_piece(self, info_piece):
        # could get whatever field you want return user.get("_id")
        #user = db.users.find_one(self._id)
        return self._id.get(info_piece)

    # @app.route("/savings_journal/get/<user_id>", methods=['GET'])
    def get_user_goals(self):
        # get all goals for the user
        user_goals = db.goals.find({"_id": self._id}) #find goals by user _id
        for goal in user_goals:
            print(Goal(**goal).to_json())

    def delete_user(self):
        # delete a user
        db.users.find_one_and_delete({'_id': self._id})

class Goal(User, BaseModel, Resource):  # each goal will have the user ID
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    user_id: User.id
    slug: str
    title: str
    amount: int
    deadline: date
    notes: str

    # date_added: Optional[datetime]
    # date_updated: Optional[datetime]

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data["_id"] is None:
            data.pop("_id")
        return data

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

