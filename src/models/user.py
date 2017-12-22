import uuid

from flask import session

from common.database import Database

from flask import session

class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one('users', {'email':email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one('users', {'_id':_id})
        if data is not None:
            return cls(**data)


    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password):
        user = User.get_by_email(email)
        if user is None:
            # create user
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False


    @staticmethod
    def login(user_email):
        # Login_valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_cfus(self):
        return CFUMessage.find_by_user_id(self._id)

    @staticmethod
    def new_cfu(message):
        # TODO expand to other CFU types
        cfu = CFUMessage(message, self._id)
        cfu.save_to_mongo()

    def json(self):
        return {'email': self.email,
                '_id': self._id}

    def save_to_mongo(self):
        Database.insert('users', self.json())
