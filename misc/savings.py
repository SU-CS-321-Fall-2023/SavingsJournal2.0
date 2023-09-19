class SavingsAlgorithms:

    currentsavings = x # find way to load/access value
    totalneeded = x # find way to load/access value
    recentlysaved = x # temporary value for when $ is made towards a goal
    addedgoal = x # temporary value for freshly added goal amount
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
        if change detected:
            if change in currentsavings: # if a goal has progress made towards it
                currentsavings += recentlysaved # update currentsavings
            if change in totalneeded: # if a new goal is added
                totalneeded += addedgoal # update totalneeded
            progressbar()