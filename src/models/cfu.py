import uuid
from random import shuffle

from common.database import Database

class CFUMessage(object):
    def __init__(self, message, user_id, _id=None):
        self.message = message
        self.user_id = user_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='cfus', data=self.json())

    def json(self):
        return {'_id': self._id,
                'user_id': self.user_id,
                'message': self.message}

    @classmethod
    def get_from_mongo(cls, _id):
        cfu_data = Database.find_one(collection='cfus', query={'_id':_id})
        return cls(**cfu_data)

    @classmethod
    def find_by_user_id(cls, user_id):
        cfus = Database.find(collection='cfus', query={'user_id': user_id})
        return [cls(**cfu_data) for cfu_data in cfus]



class MultipleChoiceCFU(CFUMessage):
    def __init__(self, question, options, user_id, _id=None):
        CFUMessage.__init__(self,
                            self._make_message(question, options),
                            user_id, _id)

    def _make_message(self, question, options, shuffle_opts=False):
        message = question + '\n'

        if shuffle_opts:
            shuffle(options)

        for i, opt in enumerate(options):
            message += str(i) + '. ' + opt + '\n'

        return message


class FreeResponse(CFUMessage):
    def __init(self, question, user_id, _id=None):
        CFUMessage.__init__(self, question, user_id, _id)
