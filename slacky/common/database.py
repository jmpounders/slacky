import pymongo

class Database():
    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    @staticmethod
    def initialize():
        # Initialize the connection to the mongo URI
        client = pymongo.MongoClient(Database.URI)

        # Get the slacky database from the connection
        Database.DATABASE = client['slacky']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert_one(data)

    @staticmethod
    def delete(collection, data):
        Database.DATABASE[collection].delete_one(data)

    @staticmethod
    def update(collection, criterion, new_data):
        Database.DATABASE[collection].update_one(criterion, {'$set': new_data})

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
