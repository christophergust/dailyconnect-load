from pymongo import MongoClient
import base64
import configparser

'''
Purpose:
        Purpose of this script is to provide a sample set of insert,
        retrieve, and delete statements to both verify functions and
        provide sample commands to execute
Requirements:
        MongoDB database setup
        Configure DailyConnect.ini file with appropriate detail
        (future requirement)Pre-setup of appropriate category enums
Note:
        n/a
'''

# get config detais to use
config = configparser.ConfigParser()
config.read('DailyConnect.ini')
dbServer = config['DatabaseDetail']['DatabaseServer']
dbName = config['DatabaseDetail']['DatabaseName']

# connect to remote mongodb
client = MongoClient(dbServer)

# crete/get db and document category
db = client[dbName]
collection = db['activities']


# sample insert (note: if db not exist, will create
collection.insert_one(
    {'activityId': 0,
     'kid_id': 0,
     'sender_id': 0,
     'category_id': 0,
     'date': '180801',
     'time': '0000',
     'text': 'text',
     'p': 'p',
     'lId': 0,
     'ms': 0,
     'isst': 0,
     'd': 0,
     'e': 'e',
     'n': 'n',
     'photo': 'photo', # b64encode image
     'photoImgType': 'jpeg'})

# sample retrieval
#   possibly update in the future to query enums and/or specific details
out = collection.find({'activityId': 0})
for o in out:
    print(o)

# sample delete
collection.delete_one({'activityId': 0})
out = collection.find({'activityId': 0})
for o in out:
    print(o)
