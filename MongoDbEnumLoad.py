import configparser
from pymongo import MongoClient

'''
Purpose:
        Purpose of this script is to provide enum mapping values
        in appropriate documents for ids found in dailyconnect extract
Requirements:
        MongoDB database setup
        Configure DailyConnect.ini file with appropriate detail
Note: Goes along with dailyconnect-api - will hopefully eventually
        be replaced using all node.js
'''

# get config detais to use
config = configparser.ConfigParser()
config.read('DailyConnect.ini')
dbServer = config['DatabaseDetail']['DatabaseServer']
dbName = config['DatabaseDetail']['DatabaseName']
kid1Id = config['Kids']['Kid1Id']
kid1Name = config['Kids']['Kid1Name']
kid2Id = config['Kids']['Kid2Id']
kid2Name = config['Kids']['Kid2Name']
parent1Id = config['Parents']['Parent1Id']
parent1Name = config['Parents']['Parent1Name']
parent2Id = config['Parents']['Parent2Id']
parent2Name = config['Parents']['Parent2Name']

# kid enum
kidsList = {int(kid1Id):kid1Name, int(kid2Id):kid2Name}

# category enum
categoriesList = {101:'SignIn', 102:'SignOut', 200:'AteFood', 300:'Bottle',
            401: 'DiaperPoop', 402:'DiaperPoopPee', 403:'DiaperPee', 501:'Sleeping',
            502:'Slept', 700:'Activity', 1000:'Photo', 1100:'Message',
            2500:'PottyPee'}

# message_by enum
senderList = {190994816:'NewHorizon', 4551294744264704:'NewHorizon',
              int(parent1Id):parent1Name, int(parent2Id):parent2Name}

# connect to remote mongodb
client = MongoClient(dbServer)

# crete/get db
db = client[dbName]

# insert kids
kids = db['kids']
for kid in kidsList:
    if kids.find({'kidId': kid}).count() == 0:
        kids.insert_one({'kidId': kid, 'kidName': kidsList[kid]})

print('---------KIDS---------')
results = kids.find({})
for result in results:
    print(result)

# insert categories
categories = db['categories']
for category in categoriesList:
    if categories.find({'categoryId': category}).count() == 0:
        categories.insert_one({'categoryId': category, 'categoryName': categoriesList[category]})

print('-------CATEGORIES-------')
results = categories.find({})
for result in results:
    print(result)

# insert senders
senders = db['senders']
for sender in senderList:
    if senders.find({'categoryId': sender}).count() == 0:
        senders.insert_one({'senderId': sender, 'senderName': senderList[sender]})

print('---------SENDERS---------')
results = senders.find({})
for result in results:
    print(result)






