#!/usr/bin/env python

import os
import json
import time

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

        resp = app.response_class(
            mimetype='application/json',
            headers={ 'Access-Control-Allow-Origin' : '*'}
        )

        if not ('case' in request.files and 'product' in request.files):

            resp.response=json.dumps("File not found")
            resp.status='400'

        case = request.files['case']
        if case.filename and case:
            filename = "Case"
            case.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            resp.response=json.dumps("Inappropriate case file!")
            resp.status='400'

        product = request.files['product']
        if product.filename and product:
            filename = "Product"
            product.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            resp.response=json.dumps("Inappropriate case file!")
            resp.status='400'

    resp.response=json.dumps("Success!")
    resp.status='200'


    return resp
