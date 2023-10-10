from flask import request, session , jsonify
from models import User
from mongo_service import db, users, goals
from pydantic import ValidationError

def add_user(hashed):
    user = {'username': request.form['username'],
            'password': hashed,
            'email': '',
            'goals': []}
    try:
        user_obj = User(**user)
        users.insert_one(user_obj.model_dump())  # inserts to collection as dictionary
    except ValidationError as e:
        return jsonify({'message': 'Validation error', 'errors': e.errors()}), 400

def add_goal(goal):
    # add new goal to the user's list of goals
    # don't need to return anything or connect to a routing
    user = users.find_one({'username': session['username']})
    goals = user['goals']
    goals.append(goal)  # add goal dictionary to user's list
    users.update_one({'username': session['username']}, {'$set': {'goals': goals}})  # update user entry


def remove_goal(goal_id):
    # add new goal to the user's list of goals
    # don't need to return anything or connect to a routing
    user = users.find_one({'username': session['username']})
    goal_list = user['goals']
    for goal in goal_list:
        if goal_id == goal.get['_id']:
            goals.remove(goal)
    users.update_one({'username': session['username']}, {'$set': {'goals': goals}})  # update user entry