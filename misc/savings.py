class SavingsAlgorithms:

    currentsavings = None # find way to load/access value
    totalneeded = None # find way to load/access value
    recentlysaved = None # temporary value for when $ is made towards a goal
    addedgoal = None # temporary value for freshly added goal amount
    # may reset recentlysaved and addedgoal each time they're compiled into the savings?

    # to do:
    # - connect progressbar variable to progressbar on savings page
    # - connect total savings variables to displayed variables on savings page
    # - create change-detecting algorithm that will launch the total savings function

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