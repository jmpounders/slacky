from common.database import Database
import models.cfu as cfu

from bson.objectid import ObjectId


Database.initialize()

user_id =  ObjectId('5a12e08022bfea7b6574b6b3')
cfu1 = cfu.MultipleChoiceCFU('Q:', ['one', 'two'], user_id)
print(cfu1.json())

cfu1.save_to_mongo()

print()
for i, r in enumerate([result for result in Database.find('cfus', {})]):
    print(i, r)

