#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask, render_template, send_file, request
from datetime import datetime, timedelta
from os import path
from glob import glob
import werkzeug
app = Flask(__name__)

#Folder where the camera images are stored
IMAGES_FOLDER='/home/airadier/ip_webcam'
#The pattern to search for images for a specified minute
MINUTE_PATTERN='cam-%Y%m%d-%H%M*.jpg'
#The date string format that the files use
DATE_PATTERN='cam-%Y%m%d-%H%M%S.%f.jpg'
#Max second difference between requested time and an existing image. If diff greater than this, no image will be returned
MAX_SECONDS_DIFF=3

@app.route('/')
def view():
    return render_template('view.html')

@app.route('/getimg')
def get_image():
    timestamp = int(request.args.get('t', 0)) / 1000.0
    time = datetime.fromtimestamp(timestamp)
    f = get_file_for_time(time)
    if f:
        return send_file(f, mimetype='image/jpeg')
    else:
        return "Not found", 404

@app.route('/getfile')
def get_file():
    timestamp = int(request.args.get('t', 0)) / 1000.0
    time = datetime.fromtimestamp(timestamp) 
    if timestamp == 0:
      time = datetime.now()
    files = get_files_near(time)
    return get_nearest_file(files, time)

def get_file_for_time(time):
    files = get_files_near(time)
    return get_nearest_file(files, time)

def get_files_near(time):
    time_next = time + timedelta(minutes=1)
    time_prev = time - timedelta(minutes=1)
    date_pattern = path.join(IMAGES_FOLDER, MINUTE_PATTERN)
    files = glob(time.strftime(date_pattern))
    files.extend(glob(time_next.strftime(date_pattern)))
    files.extend(glob(time_prev.strftime(date_pattern)))
    return files

def get_nearest_file(files, time):
    nearest = -1
    delta = MAX_SECONDS_DIFF
    for i, f in enumerate(files):
        try:
            name = path.basename(f)
            file_date = datetime.strptime(name, DATE_PATTERN)
            file_delta = abs((time - file_date).total_seconds())
            if file_delta < delta:
                delta = file_delta
                nearest = i
        except Exception as e:
             pass 
    return files[nearest] if nearest >= 0 and len(files) > 0 else ""
