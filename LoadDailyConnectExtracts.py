import json
import os
import base64
import configparser
from pprint import pprint
from pymongo import MongoClient

'''
Purpose: Purpose of this script is to take json and jpeg photos
            from node.js data extract from DailyConnect, transform
            as needed and load in mongodb
Requirements:
        MongoDB database setup
        Configure DailyConnect.ini file with appropriate detail
        Json and jpeg output from DailyConnect
Note: Goes along with dailyconnect-api - will hopefully eventually
        be replaced using all node.js
'''

'''
Keys and their meanings/values:
    By: Id of who entered
    Cat: Id of category of entry
    Id: Entry Id
    Kid: Kid id
    Pdt: Date (format: YYMMDD)
    Txt: Information (i.e. starts sleeping)
    Utm: Time (format: HHMM)
    p: other detail??
    Photo: Photo id
    lId: ???
    ms: ???
    isst: ???
    d: ???
    e: ???
    n: Note??
'''

# get config detais to use
config = configparser.ConfigParser()
config.read('DailyConnect.ini')
dbServer = config['DatabaseDetail']['DatabaseServer']
dbName = config['DatabaseDetail']['DatabaseName']
rootPath = config['Filepaths']['RootPath']

# connect to remote mongodb
client = MongoClient(dbServer)

# crete/get db and document category
db = client[dbName]
collection = db['activities']

# counts for processing limits (if desired) - set max to 0 to process all
maxFileCount = 30
currentFileCount = 0

# other constants used
archive = 'Archive/'
txtExt = '.txt'
imgFormat = 'jpg'

# loop through files
for root, dirs, files in os.walk(rootPath):

    archivePath = root + archive
    if not os.path.exists(archivePath):
        os.makedirs(archivePath)

    for filename in files:
        if maxFileCount > 0 and currentFileCount >= maxFileCount:
            break

        if txtExt in filename:
            print(filename)
            currentFileCount += 1

            fullFile = root + filename
            archiveDatePath = ''
            with open(fullFile, encoding="utf8") as f:
                data = json.load(f)
                for v in data:
                    archiveDatePath = archivePath + str(v['Pdt']) + '/'
                    if not os.path.exists(archiveDatePath):
                        os.makedirs(archiveDatePath)
                    
                    b64EncodeImage = ''
                    category = v['Cat']
                    activityId = v['Id']
                    activityProcessed = False
                    if collection.find({"activityId": activityId}).count() > 0:
                        activityProcessed = True # issue with multiple kids requiring this logic
                    if category == 1000:
                        imageFileName = filename.replace('Status_.txt', str(v['Photo']) + '.' + imgFormat)
                        fullImageFile = root + imageFileName
                        imageFileExists = os.path.exists(fullImageFile)
                        if activityProcessed and not imageFileExists:
                            print(imageFileName,  " skipped for", activityId)
                        else:
                            with open(fullImageFile, "rb") as imageFile:
                                i = imageFile.read()
                                b64EncodeImage = base64.b64encode(i)
                            os.rename(fullImageFile, archiveDatePath + imageFileName)
                    if activityProcessed:
                        print('Already processed:', activityId)
                        continue
                    collection.insert_one(
                        {'activityId': activityId,
                         'kid_id': v['Kid'],
                         'sender_id': v['By'],
                         'category_id': category,
                         'date': v['Pdt'],
                         'time': v['Utm'],
                         'text': v['Txt'] if 'Txt' in v else '',
                         'p': v['p'] if 'p' in v else '',
                         'lId': v['lId'] if 'lId' in v else 0,
                         'ms': v['ms'] if 'ms' in v else 0,
                         'isst': v['isst'] if 'isst' in v else 0,
                         'd': v['d'] if 'd' in v else 0,
                         'e': v['e'] if 'e' in v else '',
                         'n': v['n'] if 'n' in v else '',
                         'photo': b64EncodeImage,
                         'photoImgType': imgFormat})
            os.rename(fullFile, archiveDatePath + filename)
    break
