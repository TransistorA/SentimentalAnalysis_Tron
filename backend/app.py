#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.dirname(__file__))

import json
import time
import script
import pyutilib.subprocess.GlobalData

from datetime import datetime as dt
from flask import (Flask,
                   request,
                   redirect,
                   jsonify,
                   render_template,
                   send_from_directory)
from werkzeug.utils import secure_filename

# WARNING: turns off signal handlers (no Ctrl+C to kill process)
# hack to solve "signal only works in main thread glpk"
# refer: https://github.com/Pyomo/pyomo/issues/420
pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False

template_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               '..',
                               'frontend')
app = Flask(__name__, template_folder=template_folder)

UPLOAD_FOLDER = 'uploads'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(app.template_folder, path)


def create_resp(status, schedule=None, error=None):
    response = {
        'schedule': schedule,
        'error': error is not None,
        'error_message': error
    }
    resp = app.response_class(
        mimetype='application/json',
        headers={'Access-Control-Allow-Origin': "*"},
        response=json.dumps(response),
        status=str(status)
    )
    return resp


@app.route('/api/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':

        if not ('case' in request.files and 'product' in request.files):
            return create_resp(status=400,
                               error="One of the files was not available")

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        now = dt.now().strftime('%Y-%m-%dT%H-%M-%S')

        case = request.files['case']
        product = request.files['product']
        if not (case.filename and case):
            return create_resp(status=200,
                               error="Cases file is corrupted or has no file name")
        elif not (product.filename and product):
            return create_resp(status=200,
                               error="Product listing file is corrupted or has no file name")

        cases_file_path = 'case_{}_{}'.format(now, case.filename)
        cases_file_path = os.path.join(UPLOAD_FOLDER, cases_file_path)
        case.save(cases_file_path)

        product_file_path = 'product_{}_{}'.format(now, product.filename)
        product_file_path = os.path.join(UPLOAD_FOLDER, product_file_path)
        product.save(product_file_path)

        try:
            schedule = script.schedule(cases_file_path, product_file_path)
            schedule = str(schedule)
        except Exception as e:
            msg = 'Error building a schedule: {}'.format(str(e))
            return create_resp(status=200,
                               error=msg)
        else:
            return create_resp(status=200,
                               schedule=schedule)

    return create_resp(status=200,
                       error="Form not submitted properly (POST request not found, contact developers)")

if __name__ == "__main__":
    app.run(port=8080, debug=True)
