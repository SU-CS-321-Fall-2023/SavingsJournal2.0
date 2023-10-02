import Goal
from flask import Flask, request


class SavingsAlgorithms:

    currentsavings = None  # how much $ has already been saved towwards all goals collectively
    totalneeded = None  # how much $ is needed for all goals to be completed (includes amount already collected)
    recentlysaved = None  # 'temporary' value for when $ is made towards a goal
    addedgoal = None  # 'temporary' value for freshly added goal amount -- link to Goal.amount

    @app.route("/total_savings/<progressBg>")
    def progressbar():
        percent = currentsavings / totalneeded
        # commit to webpage -- progressBg

    # total savings function -- will include the first goal being created
    # all will compile as new goals are added or as savings are updated
    @app.route("/total_savings/<totalNumbers>", methods=["GET"])
    def updatetotalsavings():
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