from savings_journal_project.PydanticObjectId import PydanticObjectId
from savings_journal_project.app import db
import Goal
from datetime import date
from flask import Flask, request, jsonify

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
    class User(BaseModel):
        user_id: Optional[PydanticObjectId] = Field(None, alias="_id")
        slug: str
        name: str
        email: str
        password: str
    """

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

        """
        def save_user_info(self, user_ID, name, email, password):
            # save to Mongo in dictionary type style
            # Mongodb document (JSON-style) inserting into collection
            user_ID = {
                "user_id" : id
                "name": name,
                "email": email,
                "password": password,
                "goals": [
                    {"title": "",
                     "amount":"",
                     "deadline":"",
                     "notes":""}
                ]
                # "goals": #a reference to another collection which is goals (will put the user id with this)
            }
            user_collection.insert_one([user_ID])  # for a single document
            # user_collection.insert_many([user_1,user_2]) # for multiple docs
    
            """
