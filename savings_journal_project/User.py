class User:

    def __init__(self, email, password, name):
        self._email = email
        self._password = password
        self._name = name

    # email
    def get_email(self):
        return self._email

    def set_email(self, x):
        self._email = x

    # password
    def get_password(self):
        return self._password

    def set_password(self, x):
        self._password = x

    # name
    def get_name(self):
        return self._name

    def set_name(self, x):
        self._name = x

    def save_user_info(email, password, name):
        # save to Mongo in dictionary type style

    def show_user_info():
        # call on user info page


"""
skye = User()
skye.set_email(hi@gmail.com)
print(skye.get_email())
print(skye._email)
"""
