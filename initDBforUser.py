from pymongo import MongoClient

client = MongoClient('localhost', 27017)
#client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbterms
my_each_term = db["each_term"]

term = my_each_term.find_one()
print(term)

# doc = {
# 'userid': userid, 
# 'each_term': each_term   
# }


# db.learntermUser.insertMany(doc)
