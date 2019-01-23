#!/usr/bin/env python

import os

from flask import Flask, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def hello():
    return 'Hello, world!'


@app.route('/api/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        if 'orders' not in request.files:
            return 'File not found', 400

        orders = request.files['orders']
        if orders.filename and orders:
            filename = secure_filename(orders.filename)
            orders.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            return 'Inappropriate file', 400

    return 'File uploaded successfully'
