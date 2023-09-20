from savings_journal_project.main import user_collection
import Goal
from datetime import date


class User:
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

    class User(BaseModel):
        id: Optional[PydanticObjectId] = Field(None, alias="_id")
        #slug: str
        name: str
        email: str
        password: str
        goals: [Goal]
        #date_added: Optional[date]
        #date_updated: Optional[date]

    def save_user_info(self, user_ID, name, email, password):
        # save to Mongo in dictionary type style
        # Mongodb document (JSON-style) inserting into collection
        user_ID = {
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

    def get_user_info(self):
        # viewing all the user's dictionaries
        # Retrieve a collection named "user_info" from database
        user_details = user_collection.find(self)
        # change the format this is returned in
        # change what info is returned
        for info in user_details:
            print(info)

    def show_user_info(self):
        #show on profile page

    def add_goal(self, goal):
        # add a newly created goal to a (the?) collection for the user


    def delete_goal(self, goal):
        # delet a goal from a (the?) collection for the user
        user_collection.remove({"title": goal.title()})
        # function to search for something specific (ex like a goal?)
        # indexing
        #user_details = user_collection.find({"email": user_1.get_email()})

    #can you update one piece at a time?
    def update_user_info():
        user_collection.update(
                {id : user_ID},
                {"email": ,
                "password":,
                "name":,
                }
        )



