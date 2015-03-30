#!/usr/bin/python
import urllib2
import json
from collections import OrderedDict
from pymongo import MongoClient, GEOSPHERE, TEXT

class DataProcessor:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test
        self.table = self.db.foodtrucks
        self.datasetUrl = 'https://data.sfgov.org/api/views/rqzj-sfat/rows.json?accessType=DOWNLOAD'

    # Populate food trucks data in MongoDB from the raw data file
    def addDataToDb(self):
        self.table.drop()
        headers = {0:'locationid', 1:'Applicant', 2:'FacilityType', 3:'cnn', 4:'LocationDescription', 5:'Address', 6:'blocklot', 7:'block', 8:'lot', 9:'permit', 10:'Status', 11:'FoodItems', 12:'X', 13:'Y', 14:'Latitude', 15:'Longitude', 16:'Schedule', 17:'NOISent', 18:'Approved', 19:'Received', 20:'PriorPermit', 21:'ExpirationDate', 22:'Location'}
        # Get dataset from url
        rawData = urllib2.urlopen(self.datasetUrl).read()
        data = json.loads(rawData).get('data')
        # Parse data
        for d in data:
            row = {}
            # Create row from food truck info
            for i in range(8, len(d)):
                if not d[i]:
                    continue

                # Split food items into a list, so that we can create multi index on it
                if headers[i-8] == 'FoodItems':
                    items = [ item.lower().strip() for item in d[i].split(':') ]
                    row['FoodItems'] = items
                    continue

                # Add location in the required lng, lat format in db
                elif headers[i-8] == 'Location':
                    if not d[i][1] or not d[i][2]:
                        continue
                    loc = OrderedDict()
                    loc['Longitude'] = float(d[i][2])
                    loc['Latitude'] = float(d[i][1])
                    row['Location'] = loc
                else:
                    row[headers[i-8]] = d[i]
            self.table.insert(row)
        self.createIndices()

    # Create geo index for location and multi index on food items
    def createIndices(self):
        self.table.create_index([("Location", GEOSPHERE)])
        self.table.create_index("FoodItems")

if __name__=='__main__':
    dp = DataProcessor()
    dp.addDataToDb()

