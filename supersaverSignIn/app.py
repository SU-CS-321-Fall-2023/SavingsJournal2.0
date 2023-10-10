from flask import jsonify
from flask import Flask, render_template, request, url_for, session, redirect
import bcrypt
from pydantic import ValidationError
import uuid
from models import Goal, User
from mongo_service import db, users, goals
from helpers import add_user, add_goal, remove_goal

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

@app.route('/', methods=['GET'])  # login/ signup buttons on top
def index():  # adjust this to go to whatever page we want it to go to after logging in
    return render_template('index.html')
    # if 'username' in session:
    # return 'Welcome, ' + session['username'] + '!'
    # return render_template('index.html')

@app.route('/index2/', methods=['GET'])  # savings tabs on top
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
            # flash(session['username'])
            return redirect(url_for('index2'))
        # return redirect(url_for('signIn'))  # where user exists already
        return 'Username already exists.'
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

@app.route("/create_goal/", methods=['POST', 'GET'])
def create_goal():
    # create goal--adding data to mongo and going back to savings journal page (or goal page?)
    if request.method == 'POST':
        # if 'username' in session:
        username = session['username']
        goal = {
            "title": request.form['title'],  # required
            "amount": request.form['amount'],  # required
            "deadline": request.form['deadline'],  # required
            "notes": request.form['notes'],
            "username": username  # required
        }
        print(goal)
        try:
            goal_obj = Goal(**goal)
            goals.insert_one(goal_obj.model_dump())
            add_goal(username, goal_obj.model_dump())  # pass goal into add_goal as a dictionary
            return render_template('goal/<string:goal_id>.html', goal_id=goal['_id'])
        except ValidationError as e:
            return jsonify({'message': 'Validation error', 'errors': e.errors()}), 400
        # if Goal.model_validate_json(dumps(goal)):
        # goals.insert_one(goal) # then add to goal collection
        # add_goal(username, dumps(goal)) # pass goal into add_goal as a dictionary
        # return render_template('goal/<goal_id>.html', goal_id=goal['_id'])
        # else:
        #   return 'Goal information cannot be added in this format.'
    # return render_template('create_goal.html')  # if a GET request (just the blank goal form)

def get_goal_list():
    if 'username' in session:
        username = session['username']
        user = users.find_one({"username": username})  # get the user
        user_goal_list = user['goals']  # get their list of goals
        return user_goal_list

@app.route("/savings_journal/", methods=['GET'])
def savings_journal():
    if 'username' in session:
        # list all goals for the user
        user_goal_list = get_goal_list()
        if user_goal_list is None:
            return render_template('savings_journal.html', goals=[])
            # return redirect(url_for('create_goal'))  # if no goals exist yet, give option to create one when this page is finished
        return render_template('savings_journal.html', goals=user_goal_list)
        # return user_goal_list

@app.route("/goal/string:<goal_id>/", methods=['GET', 'DELETE', 'PATCH'])
def goal(goal_id):
    from bson import ObjectId
    _id = ObjectId(goal_id)
    goal = goals.find_one_or_404({'_id': _id})
    if request.method == 'GET':
        return render_template('/goal/<string:goal_id>.html', goal=goal)  # view the goal
    if request.method == 'DELETE':
        remove_goal(goal['_id'])  # remove goal from user list
        goals.remove(goal)
        return redirect(url_for('savings_journal'))  # see the remaining goals
    if request.method == 'PATCH':
        goal = goals.find_one_and_update({'_id': _id}, {'$set':
                                                            {"title": request.form['title'],
                                                             "amount": request.form['amount'],
                                                             "deadline": request.form['deadline'],
                                                             "notes": request.form['notes']}
                                                        })
        try:
            Goal(**goal)
            return render_template('goal/<string:goal_id>.html', goal=goal)  # view the goal
        except ValidationError as e:
            return jsonify({'message': 'Validation error', 'errors': e.errors()}), 400

# need to test
@app.route("/goal/string:<status>/", methods=['GET'])
def check_status(status):  # status will be string 'done', 'doing', or 'to do'
    goal_list = goals.find({"status": status})
    return render_template('.html', goal_list=goal_list)

if __name__ == '__main__':
    app.run(debug=True)