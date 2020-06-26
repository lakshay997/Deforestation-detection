from flask import Flask, request, render_template, redirect, url_for
import requests
from flask_cors import CORS
import json
import os
import hashlib
# from flask_pymongo import PyMongo
# from pymongo import MongoClient
from constants import baseDirectory, baseURL, ORIGINAL, MODIFIED, DATA
from utils import getFilePath
from forest import findAcc
# from apscheduler.scheduler import Scheduler

app = Flask(__name__)
mapboxToken = os.getenv('MAPBOX_TOKEN')

# CORS
CORS(app)

# to be watched coords
coords = []

# # Initialized scheduler
# cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
# cron.start()
# @cron.interval_schedule(seconds=20)
# def job_function():
#     for lat, lng, name in coords:
#         updateData(lat, lng, name)


def updateData(location):
    dirName = getName(location)
    endpoint = location.get('lng') + ',' + location.get('lat') + ',15/800x600?access_token=' + mapboxToken
    URL = baseURL + endpoint
    r = requests.get(url = URL, stream = True)
    if r.status_code == 200:
        coords.append(location)
        path = os.path.join(baseDirectory, dirName)
        print(path)
        if (not os.path.exists(path)):
            os.mkdir(path)
        with open(os.path.join(path, ORIGINAL), 'wb') as f:
            f.write(r.content)
        with open(os.path.join(path, 'data'), 'w') as f:
            f.write(location.get('loc'))
        findAcc(path)
    else:
        return 'Mapbox API not responding.', 301

@app.route('/')
def root():
    return redirect('/home')

@app.route('/home')
def home():
    imagePaths = []
    for imgdir in os.scandir(baseDirectory):
        imagePathObject = {
            'original': getFilePath(ORIGINAL, imgdir),
            'modified': getFilePath(MODIFIED, imgdir),
            'title': open(getFilePath(DATA, imgdir), 'r').read()
        }
        imagePaths.append(imagePathObject)
    # TO-DO: Sort imagePaths w.r.t last modifed
    return render_template('index.html', imagePaths=imagePaths)

@app.route('/getpaths', methods=['GET'])
def getpaths():
    paths = [] # mongo.db.images.find({})
    results = []
    for res in paths:
        results.append([res['path'], res['name']])
        coords.append((res['lat'], res['lng'], res['name']))
    return json.dumps(results)
    
 
@app.route('/addnew', methods=['GET'])
def addnew():
    location = {
        'lat': request.args.get('lat', None),
        'lng': request.args.get('lng', None),
        'loc': request.args.get('location', None)
    }
    print(location)
    if isValidCoordinate(location):
        updateData(location)
        return redirect('/home', code=301)
    else:
        return redirect('/home', code=301)



# Utility
def isValidCoordinate(location):
    if location.get('lng', None) and location.get('lng', None) and location.get('loc', None):
        return True
    return False

def getName(location):
    hashString = (location.get('lat') + location.get('lng')).encode('utf-8')
    locationHash = hashlib.sha256(hashString).hexdigest()
    return locationHash[:6] + "-" + locationHash[-6:]