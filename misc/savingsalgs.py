# import Goal
from flask import Flask, request


class SavingsAlgorithms:

    # currentsavings = 0  # how much $ has already been saved towwards all goals collectively
    totalneeded = 0  # how much $ is needed for all goals to be completed 
    # recentlysaved = None  # 'temporary' value for when $ is made towards a goal
    # addedgoal = None  # 'temporary' value for freshly added goal amount -- link to Goal.amount
    percent = 0  # percent for the progressbar, defined outside the func so it can be accessed externally

    @app.route("/total_savings")
    def progressbar():
        percent = currentsavings / totalneeded
        # commit to webpage -- progressBg
        # progress bar needs setup on html -- use percent variable here as % for progressbar to be filled

    # total savings function -- will include the first goal being created
    # all will compile as new goals are added or as savings are updated
    @app.route("/total_savings/<totalNumbers>")
    def updatetotalsavings():
        '''
        # if change detected, do the thing
        if recentlysaved:  # if a goal has progress made towards it, add that to what's been saved already
            currentsavings += recentlysaved
            totalNumbers -= recentlysaved  # shown on webpage
            recentlysaved = None
            progressbar()  # reflects changes in the progress bar
        if addedgoal:  # if a new goal is added, add that amount to totalneeded
            totalneeded += addedgoal
            totalNumbers += addedgoal  # shown on webpage
            addedgoal = None
            progressbar()  # reflects changes in the progress bar
        '''
        # rewritten to no longer need extra variables
        # need user_goal_list from list_goals() (define it separately, reset it when list_goals() is run)
        totalneeded = 0  # so previous counts don't affect the recalculations
        goal_list = get_goal_list  # from app.py
        if goal_list:
            for Goal in goal_list:
                totalneeded += Goal.amount
        # as money is saved, compile it
        # for savingsacquired: currentsavings += savings
        totalNumbers = totalneeded  # - currentsavings
        # ^ subtract currently saved from total to see how much is still needed
        # do we have a function anywhere else to deal with money as it gets saved toward goals??
        progressbar()  # reflect changes in the progress bar