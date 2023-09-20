class SavingsAlgorithms:

    currentsavings = None # how much $ has already been saved towwards all goals collectively
    totalneeded = None # how much $ is needed for all goals to be completed (includes amount already collected)
    recentlysaved = None # 'temporary' value for when $ is made towards a goal
    addedgoal = None # 'temporary' value for freshly added goal amount

    # to do:
    # - connect progressbar variable to progressbar on savings page
    # - connect total savings variables to displayed variables on savings page
    # find way to load/access value for currentsavings and totalneeded

    def progressbar():
        percent = currentsavings / totalneeded
        # commit to webpage

    # total savings function -- will include the first goal being created
    # all will compile as new goals are added or as savings are updated
    def updatetotalsavings():
        # if change detected, do the thing
        if recentlysaved: # if a goal has progress made towards it, add that to what's been saved already
            currentsavings += recentlysaved
            recentlysaved = None
            progressbar() # reflects changes in the progress bar
        if addedgoal: # if a new goal is added, add that amount to totalneeded
            totalneeded += addedgoal
            addedgoal = None
            progressbar() # reflects changes in the progress bar