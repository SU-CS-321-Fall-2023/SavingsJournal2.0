# creating a collection
# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database
import User
import Goal

db = get_database()
user_collection = db["users"]
goal_collection = db["goals"] #collection inside a collection?
# setting up a collection of goals for one user
# can we put all the users inside a collection?
# it's a reference

# example
# get these as inputs from the user # user_1 = User(email_in, password_in, name_in)
# make password private (bcrypt)
# could we just use the email as the userID?
user_1 = User("jimmy@gmail.com", "vhhbeflhbfel2", "Jimmy")
# generate a random userID--put this in a method in User class
user_ID = 32
# this will all go into a function in user class for saving data
user_1.save_user_info(user_ID, user_1.get_name(), user_1.get_email(), user_1.get_password())
user_1.get_user_info()
user_1.show_user_info()

# function to add a goal to a user
goal_1 = Goal("Buy a Car", "$26,000", "June 2024", "Subaru Crosstrek")
user_1.add_goal(goal_1)
user_1.delete_goal(goal_1)

# once someone logs in, all of their relevant data should pull up
    # get the relevant data based on their email?
