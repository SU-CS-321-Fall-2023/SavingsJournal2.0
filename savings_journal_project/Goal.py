class Goal:

    def __init__(self, title, amount, deadline, notes):
        self._title = title
        self._amount = amount
        self._deadline = deadline
        self._notes = notes

    # title
    def get_title(self):
        return self._title

    def set_title(self, x):
        self._title = x

    # amount
    def get_amount(self):
        return self._amount

    def set_amount(self, x):
        self._amount = x

    # deadline
    def get_deadline(self):
        return self._deadline

    def set_deadline(self, x):
        self._deadline = x

    # notes
    def get_notes(self):
        return self._notes

    def set_notes(self, x):
        self._notes = x

    def save_goal_info(title, amount, deadline, notes):
        # save to Mongo in dictionary-type style
    def show_goal():
        # call on savings journal page
        # call on goal page


