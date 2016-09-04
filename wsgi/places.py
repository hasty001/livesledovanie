from flask import Blueprint, jsonify
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g, send_from_directory, current_app
from pymongo import MongoClient
from bson import json_util
import json
import os
from cestadb import *
from ftpcopy import resize_and_copy_to_cesta_ftp
from functools import wraps
from datetime import datetime


places = Blueprint('places', __name__, template_folder='templates')

"""
client = MongoClient("mongodb://admin:51dBVLs4ZLpi@%s:%s/" \
                           %(os.environ['OPENSHIFT_MONGODB_DB_HOST'],os.environ['OPENSHIFT_MONGODB_DB_PORT']))
db = client.sledovanie

poi = db.poi
"""
    #
    #"mongo":        "mongodb://admin:51dBVLs4ZLpi@%s:%s/" \
    #                       %(os.environ['OPENSHIFT_MONGODB_DB_HOST'],os.environ['OPENSHIFT_MONGODB_DB_PORT'])
    #"mongo":        "mongodb://admin:51dBVLs4ZLpi@%s:%s/" %("127.0.0.1","27017")


def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data) + ')'
            return current_app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)
    return decorated_function


@places.route('/mapa', methods=['GET'])
#@login_required
def mapa():
    if request.method == 'GET':
        return render_template('mapa.html')


# koli moznosti mat mapu verejne
#@login_required
@places.route('/ajax/pois', methods=['GET'])
def pois():
    if request.method == 'GET':
        pois = poi.find()
        pois = str(json.dumps(list(pois),default=json_util.default))
        return pois



@places.route('/ajax/pois/onroute', methods=['GET'])
#@login_required
@support_jsonp
def icons():
    if request.method == 'GET':
        #find ids of current travelers in MySQL - details
        all_detail_ids = Details.query.with_entities(Details.user_id, Details.meno).filter_by(end_date='0000-00-00 00:00:00')
        all_active_messages =[]
        #for each id query jos_article for article ID
        for detail_id in all_detail_ids:

            user_id = int(detail_id.user_id)
            group_name = detail_id.meno
            print(user_id)
            #get last messages of travelers based on results from
            #ugly way having many queries to mysql :( spravy=Sprava.query.filter_by(user_id = g.user.id).order_by(Sprava.pub_date.desc()).all()
            if user_id == 62 or user_id == 64 or user_id == 287 or user_id == 304:
                #do nothing testing id
                print('testing ID')
            else:
                try:
                    message = Sprava.query.with_entities(Sprava.text, Sprava.pub_date, Sprava.lat, Sprava.lon).filter_by(user_id=user_id).order_by(Sprava.pub_date.desc()).first()

                    #print(message.text)
                    json_message = {
                        "date":  message.pub_date.strftime('%d.%m.%Y %H:%M:%S'),
                        "group": group_name,
                         "coordinates": [message.lon, message.lat],
                        "text": message.text
                    }

                    all_active_messages.append(json_message)
                    #print jsonify(json_message)

                except:
                    print("user has no messages")

        test_message = {
                        "date": "2015-12-23",
                        "group": "Test",
                         "coordinates": ["18.02", "49.09"],
                        "text": "boli isle dosli a pijeme pivo"
                    }

        return jsonify(data=all_active_messages)