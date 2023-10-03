from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signIn/')
def signIn():
    return render_template('signIn.html')

@app.route('/signUp/')
def signUp():
    return render_template('signUp.html')

@app.route('/spending_habits/')
def spending_habits():
    return render_template('spending_habits.html')

@app.route('/total_savings/')
def total_savings():
    return render_template('total_savings.html')

@app.route('/savings_journal/')
def savings_journal():
    return render_template('savings_journal.html')

@app.route('/index2/')
def index2():
    return render_template('index2.html')


if __name__ == '__main__':
    app.run(debug=True)

#SKYLAR CODE

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
    goals: Optional[List] # goal ids


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
    if 'username' in session:
        return 'Welcome, ' + session['username'] + '!'
    return render_template('index2.html')


@app.route("/signup", methods=['POST', 'GET'])
def signup():  # gets username, password, email and adds to user collection
    # allow user to register if post
    if request.method == 'POST':
        user = db.users.find_one({'username': request.form['username']})
        if user is None:
            hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            add_user(hashed)
            session['username'] = request.form['username']
            flash(session['username'])
            return redirect(url_for('index'))
        return redirect(url_for('signin'))  # where user exists already
    return render_template('signup.html')  # where it's a get not a post request


@app.route('/signin', methods=['POST'])
def signin():
    user = db.users.find_one({'username': request.form['username']})
    if user:  # compare passwords
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), user['password'].encode('utf-8')) == \
                user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index2'))
        return 'Invalid username or password.'


@app.route('/logout')
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
@app.route("/goal", methods=['POST', 'GET'])
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
            return render_template('goal/<goal_id>.html', goal=goal)
        except ValidationError as e:
            return e
    return render_template('goal.html')  # if a GET request (just the blank goal form)


# @app.route("/user/<string:username>/goal/", methods=['GET'])
# can't edit anything on this page so no Posting, Deleting, or Patching
@app.route("/savings_journal/", methods=['GET'])
def list_goals():
    # list all goals for the user
    username = session['username']
    user_goals = db.goals.find({"username": username})  # find goals by user _id
    user_goal_list = []
    if user_goals:
        for goal in user_goals:
            user_goal_list.add(goal)
        return render_template('savings_journal.html', goals=user_goal_list)
    return redirect(url_for('goal'))  # if no goals exist yet, give option to create one


# @app.route("/user/<string:username>/goal/<PydanticObjectId:_id>", methods=['GET'])
# access a single goal only through the savings journal page where all the goals are
# so put savings journal in the route?
@app.route("/goal/<goal_id>", methods=['GET', 'DELETE', 'PATCH'])
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
            return render_template('goal/<goal_id>.html', goal=goal)  # view the goal
        except ValidationError as e:
            return e


# mongo connection closes
#client.close()

