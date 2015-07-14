__author__ = 'Steve'


class User(object):
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Buyer(User):
    def __init__(self, username, password, email):
        super(self.__class__, self).__init__(username, password, email)


rec = Buyer(1, 10, 20)