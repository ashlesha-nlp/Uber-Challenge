#!/usr/bin/python
import flask
import pymongo
import googlemaps
import memcache 
import pygmaps
import logging 

class Config:
    flaskConfigFile = 'flaskConfig'
    memcacheHost = '127.0.0.1'
    memcachePort = '11211'
    googleApiKey = 'AIzaSyDCKWyYtRBocjN401p85SRwJ_RcA71GG7s'

app = flask.Flask(__name__)
app.config.from_object(Config.flaskConfigFile)

@app.route('/', methods=['GET'])
def index():
    form = flask.request.form
    return flask.render_template('index.html', title='Find Food Trucks', form=form)

@app.route('/', methods=['POST'])
def postResults():
    form = flask.request.form
    items = []
    if 'item' in form:
        items = form.getlist('item')
    if not form['address']:
        return flask.render_template('index.html', title='Find Food Trucks', form=form, error=True)
    address = form['address']
    distanceInMiles = form['distance']
    location = memcacheClient.get(address)
    if location:
        lat, lng = location[0], location[1]
    else:
        lat, lng = getUserLocation(address)
        memcacheClient.set(address, (lat, lng), 60)
    logger.info("Logging request: %s, %s, %s", address, str(distanceInMiles), str(items)) 
    distance = int(distanceInMiles)*1600
    results = getNearbyTrucks(lat, lng, distance, items)
    mapView = createMapView(lat, lng, results)
    return flask.render_template('index.html', title='Find Food Trucks', form=form, results=True)

def createMapView(lat, lng, results):    
    mapView = pygmaps.maps(lat, lng, 15)
    for truck in results:
        fooditems = ''
        if "FoodItems" in truck:
            fooditems = ', '.join(truck["FoodItems"])
        mapView.addpoint(truck["Location"]["Latitude"], truck["Location"]["Longitude"], "#0000FF", truck["Applicant"], fooditems)
    mapView.draw('./templates/maps.html')
    return mapView

@app.route('/maps', methods=['GET'])
def getMap():
    return flask.render_template('maps.html', title='Map')

def getUserLocation(address):
    logger.info("User location: %s", address)
    location = mapsClient.geocode(address)[0]
    lat = location['geometry']['location']['lat']
    lng = location['geometry']['location']['lng']
    logger.info("User location: lat %f, lng %f", lat, lng)
    return lat, lng

def getNearbyTrucks(lat, lng, distance, items=[]):
    db = mongoClient.test
    if items:
        trucks = db.foodtrucks.find({"Location": {"$nearSphere": { "$geometry": {"type": "Point", "coordinates": [lng, lat]}, "$maxDistance": distance}}, "FoodItems": {"$in": items}}, {"Applicant": 1, "Location":1, "FoodItems": 1, "_id": 0})
    else:
        trucks = db.foodtrucks.find({"Location": {"$nearSphere": { "$geometry": {"type": "Point", "coordinates": [lng, lat]}, "$maxDistance": distance}}}, {"Applicant": 1, "Location":1, "FoodItems": 1, "_id": 0})
    logger.info("Total results: %d", trucks.count())
    return trucks

def setupLogger():
    logger = logging.getLogger('UberLogs')
    logger.setLevel(logging.INFO)
    fileHandler = logging.FileHandler('findFoodTrucks.log')
    fileHandler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    return logger

if __name__=='__main__':
    memcacheClient = memcache.Client([Config.memcacheHost+':'+Config.memcachePort], check_keys=False)
    mapsClient = googlemaps.Client(Config.googleApiKey)
    mongoClient = pymongo.MongoClient()
    logger = setupLogger()
    app.run(debug=True)

