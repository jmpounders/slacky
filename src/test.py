from common.database import Database
import models.cfu as cfu


Database.initialize()

cfu1 = cfu.MultipleChoiceCFU('Q:', ['one', 'two'])
print(cfu1.json())

# cfu1.save_to_mongo()

print()
for i, r in enumerate([result for result in Database.find('cfus', {})]):
    print(i, r)

