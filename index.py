#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask, render_template, send_file, request
from datetime import datetime, timedelta
from os import path
from glob import glob
import werkzeug
app = Flask(__name__)

IMAGES_FOLDER='/home/airadier/ip_webcam'
FILE_NAME='cam-%s.jpg'
MINUTE_PATTERN='cam-%Y%m%d-%H%M*.jpg'
DATE_PATTERN='cam-%Y%m%d-%H%M%S.%N.jpg'

@app.route('/')
def view():
    now = datetime.now()
    current = datetime(2020,04,25,9,20)
    date_pattern = path.join(IMAGES_FOLDER,MINUTE_PATTERN)
    files = glob(current.strftime(date_pattern))
    return render_template('view.html', files=files)

@app.route('/getimg')
def get_image():
    timestamp = int(request.args.get('t', 0))
    f = get_file_for_timestamp(timestamp/1000.0)
    if f:
        return send_file(f, mimetype='image/jpeg')
    else:
        return "Not found", 404

@app.route('/getfile')
def get_file():
    timestamp = int(request.args.get('t', 0))
    return get_file_for_timestamp(timestamp/1000.0)

def get_file_for_timestamp(t):
    time = datetime.fromtimestamp(t)
    time_next = time + timedelta(minutes=1)
    time_prev = time - timedelta(minutes=1)
    date_pattern = path.join(IMAGES_FOLDER, MINUTE_PATTERN)
    files = glob(time.strftime(date_pattern))
    files.extend(glob(time_next.strftime(date_pattern)))
    files.extend(glob(time_prev.strftime(date_pattern)))
    return get_nearest_file(files, time)

def get_nearest_file(files, time):
    return files[0] if len(files) > 0 else ""
