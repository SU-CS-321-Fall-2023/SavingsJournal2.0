
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/') # login/ signup buttons on top
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
    return render_template('savings_journal.html', goals=goals)

@app.route('/index2/')
def index2():
    return render_template('index2.html')


if __name__ == '__main__':
    app.run(debug=True)

# SKYLER CODE

from pymongo.server_api import ServerApi
from flask import Flask, render_template, request, url_for, session, redirect, flash
from pymongo import MongoClient
import bcrypt
from pydantic import BaseModel, ValidationError
from typing import Optional, List
from json import dumps
import uuid
from datetime import date


class Goal(BaseModel):  # each goal will have the username
    title: str
    amount: int
    deadline: str
    notes: Optional[str]
    username: str


class User(BaseModel):
    username: str
    email: Optional[str]
    password: str
    goals: Optional[List]  # goals as jsons


app = Flask(__name__)
uri = "mongodb+srv://Cluster61649:UWFPfm9BXGFp@cluster61649.dcrddgj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.db
users = db.users
goals = db.goals


# client.add_resource(User, '/user/<string:username>')
# client.add_resource(Goal, '/user/<string:username/goal/<string:title>')
def add_user(hashed):
    user = {'username': request.form['username'],
            'password': hashed,
            'email': request.form['email']}
    try:
        User.model_validate_json(dumps(user))
        users.insert_one(user)
    except ValidationError as e:
        print(e)

@app.route('/')  # login/ signup buttons on top
def index():  # adjust this to go to whatever page we want it to go to after logging in
    return render_template('index.html')
    # if 'username' in session:
    # return 'Welcome, ' + session['username'] + '!'
    # return render_template('index.html')


@app.route('/index2/')  # savings tabs on top
def index2():  # adjust this to go to whatever page we want it to go to after logging in
    return render_template('index2.html')


@app.route("/signUp/", methods=['POST', 'GET'])
def signUp():  # gets username, password, email and adds to user collection
    # allow user to register if post
    if request.method == 'POST':
        user = users.find_one({'username': request.form['username']})
        if user is None:
            hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            add_user(hashed)
            session['username'] = request.form['username']
            flash(session['username'])
            return redirect(url_for('index2'))
        # return redirect(url_for('signIn'))  # where user exists already
        return render_template('signIn.html')
    return render_template('signUp.html')  # where it's a get not a post request


@app.route('/signIn/', methods=['GET', 'POST'])
def signIn():
    if request.method == 'POST':
        user = users.find_one({'username': request.form['username']})
        if user:  # compare passwords
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), user['password'].encode('utf-8')) == \
                    user['password'].encode('utf-8'):
                session['username'] = request.form['username']
                return redirect(url_for('index2'))  # if info matches
            return 'Invalid username or password.'  # if info doesn't match
        return 'Username does not exist.'
    return render_template('signIn.html')


@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/spending_habits/')
def spending_habits():
    return render_template('spending_habits.html')


@app.route('/total_savings/')
def total_savings():
    return render_template('total_savings.html')


def add_goal(goal):
    # add new goal to the user's list of goals
    # don't need to return anything or connect to a routing
    user = users.find_one({'username': session['username']})
    goals = user.get['goals']
    goals.append(goal)  # add goal dictionary to user's list


def remove_goal(goal_id):
    # add new goal to the user's list of goals
    # don't need to return anything or connect to a routing
    user = users.find_one({'username': session['username']})
    goals = user.get['goals']
    for goal in goals:
        if goal_id == goal.get['_id']:
            goals.remove(goal_id)


# does the context for goal/goal_id have to be goal_id or _id or just goal?
@app.route("/create_goal/", methods=['POST', 'GET'])
def create_goal():
    # create goal--adding data to mongo and going back to savings journal page (or goal page?)
    if request.method == 'POST':
        #if 'username' in session:
        username = session['username']
        goal = {
            "title": request.form['title'],  # required
            "amount": request.form['amount'],  # required
            "deadline": request.form['deadline'],  # required
            "notes": request.form['notes'],
            "username": username  # required
        }
        try:
            Goal.model_validate_json(dumps(goal))  # check that goal follows schema (proper fields and data types)
            goals.insert_one(goal)  # then add to goal collection
            add_goal(username, goal)  # pass goal into add_goal as a dictionary (with the Id)
            return render_template('goal/<goal_id>.html', goal_id=goal['_id'])
        except ValidationError as e:
            return e
    return render_template('create_goal.html')  # if a GET request (just the blank goal form)


# @app.route("/user/<string:username>/goal/", methods=['GET'])
# can't edit anything on this page so no Posting, Deleting, or Patching
def get_goal_list():
    if 'username' in session:
        username = session['username']
    # user_goals = db.goals.find({"username": username})  # find goals by user _id
        user = users.find_one({"username": username})  # get the user
        user_goal_list = user.get['goals']  # get their list of goals
        if user_goal_list:
         # for goal in user_goal_list:
            # user_goal_list.add(goal)
            return user_goal_list
        return None  # if no user goals


@app.route("/savings_journal/", methods=['GET'])
def savings_journal():
    # list all goals for the user

    ## FOLLOWING UNCOMMENTED BECAUSE IT BREAKS ROUTE
    ## NEED MORE IMPLEMENTATION TO GET IT TO WORK
    # user_goal_list = get_goal_list()
    # if user_goal_list is None:
    #     return redirect(url_for('index2'))
    user_goals = [
        {
        'name': 'Vacation', 
        'description': 'Trip to Hawaii',
        'amount': 5000,
        'deadline': '2024-06-30',
        'status': 'todo'
        },
        {
        'name': 'Car',
        'description': 'Downpayment on new car',
        'amount': 15000, 
        'deadline': '2025-05-01',
        'status': 'done'
        },
        {
        'name': 'Roof',
        'description': 'Fix roof',
        'amount': 8000,
        'deadline': '2023-11-15', 
        'status': 'doing'
        }
    ]
    
    return render_template('savings_journal.html', goals=user_goals)
    #return redirect(url_for('create_goal'))  # if no goals exist yet, give option to create one
    

# @app.route("/user/<string:username>/goal/<PydanticObjectId:_id>", methods=['GET'])
# access a single goal only through the savings journal page where all the goals are
# so put savings journal in the route?
@app.route("/goal/<goal_id>/", methods=['GET', 'DELETE', 'PATCH'])
def goal(_id):
    goal = goals.find_one_or_404({'_id': _id})
    if request.method == 'GET':
        return render_template('/goal/<goal_id>.html', goal=goal)  # view the goal
    if request.method == 'DELETE':
        remove_goal(goal['_id'])  # remove goal from user list
        goals.remove(goal)
        flash('Goal removed!')
        return redirect(url_for('savings_journal'))  # see the remaining goals
    if request.method == 'PATCH':
        goal = goals.find_one_and_update({'_id': _id}, {'$set':
                                                            {"title": request.form['title'],
                                                             "amount": request.form['amount'],
                                                             "deadline": request.form['deadline'],
                                                             "notes": request.form['notes']}
                                                        })
        try:  # check schema after update
            Goal.model_validate_json(dumps(goal))
            return render_template('goal/<goal_id>.html', goal=goal)  # view the goal
        except ValidationError as e:
            return e


if __name__ == '__main__':
    app.run(debug=True)
    app.secret_key = uuid.uuid4().hex

# mongo connection closes
# client.close()
