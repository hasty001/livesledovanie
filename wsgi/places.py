from flask import Blueprint, jsonify
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g, send_from_directory
from pymongo import MongoClient
from bson import json_util
import json
import os
from cestadb import *
from ftpcopy import resize_and_copy_to_cesta_ftp


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

@places.route('/ajax/pois', methods=['GET'])


@places.route('/mapa', methods=['GET'])
#@login_required
def mapa():
    if request.method == 'GET':
        return render_template('mapa.html')


# koli moznosti mat mapu verejne
#@login_required
def pois():
    if request.method == 'GET':
        pois = poi.find()
        pois = str(json.dumps(list(pois),default=json_util.default))
        return pois



@places.route('/ajax/pois/icons/<category>', methods=['GET'])
#@login_required
def icons(category):
    if request.method == 'GET':
        icons_to_png = {
            'pramen': 'http://cestasnp.sk/web/images/mapa/watter.png',
            'pristresok': 'http://cestasnp.sk/web/images/mapa/hut.png',
            'utulna': 'http://cestasnp.sk/web/images/mapa/hut.png',
            'chata': 'http://cestasnp.sk/web/images/mapa/cottage.png',
            'potraviny': 'http://cestasnp.sk/web/images/mapa/grocery.png',
            'krcma_jedlo': 'http://cestasnp.sk/web/images/mapa/nutrition.png'
        }

        icon = {
            'iconUrl': icons_to_png[category],
            #'iconRetinaUrl': 'my-icon@2x.png',
            #'iconSize': [38, 95],
            'iconAnchor': [22, 94],
            'popupAnchor': [-3, -76],
            #shadowUrl: 'my-icon-shadow.png',
            #shadowRetinaUrl: 'my-icon-shadow@2x.png',
            #shadowSize: [68, 95],
            #shadowAnchor: [22, 94]
        }

        return jsonify(icon)