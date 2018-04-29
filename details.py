from flask import Blueprint, jsonify
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g, send_from_directory, current_app
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from cestadb import *
from bson import json_util
import json
from werkzeug import secure_filename
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import uuid
import os

details = Blueprint('details', __name__, template_folder='templates')

def dump_response(response):
    print("Upload response:")
    for key in sorted(response.keys()):
        print("  %s: %s" % (key, response[key]))

path = 'img/'

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'jpeg', 'gif', 'JPG', 'JPEG', 'PNG'])

@details.route('/details', methods=['GET','POST'])
@login_required
def details_add():
    if request.method == 'GET':
        return render_template('details.html')
    end_date='NULL'
    #user_id = g.user

    detail_json = {

    }
    completed = 0
    file = request.files['file']

    if file and allowed_file(file.filename):
        file_to_upload = request.files['file']
        upload_result = upload(
            file_to_upload,
            tags="live_sledovanie_profile",
            eager={'width': 248, 'height': 140, 'crop': 'fill' }
        )
        detail_json["img"] = upload_result
    else:
        detail_json["img"] = None

    detail_json["meno"] = request.form['meno']
    detail_json["text"] = request.form['text']
    detail_json["start_date"] = str(datetime.strptime(request.form['start_date'], "%d.%m.%Y"))
    detail_json["end_date"] = "0000-00-00 00:00:00"
    detail_json["completed"] = completed
    detail_json["user_id"] = int(g.user.id)
    detail_json["start_miesto"] = request.form['start_miesto']
    detail_json["number"] = request.form['number']
    detail_json["email"] = 0
    detail_json["articleID"] = 0
    detail_json["finished"] = False


    try:
        print("LOG inserting 'detail' into mongoDB will start")
        details_mongo.insert_one(detail_json)
        print("LOG inserting into mongoDB done")
    except:
        print("ERROR error saving 'deatil' to mongoDB")
    flash('Spr%sva bola ulo%sen%s' % (u"\u00E1", u"\u017E", u"\u00E1"))
    return redirect(url_for('gettingstarted.akozacat'))


@details.route('/details_show', methods=['GET'])
@login_required
def details_show():
    detail_mongo = details_mongo.find_one({'user_id':g.user.id})

    if detail_mongo is None:
        return redirect(url_for('details.details_add'))
    try:
        detail_mongo['start_date'] = detail_mongo['start_date'] .strftime('%d.%m.%Y')
    except:
        pass
    try:
        detail_mongo['end_date'] = detail_mongo['end_date'].strftime('%d.%m.%Y')
    except:
        pass

    if detail_mongo['end_date'] == "0000-00-00 00:00:00":
        detail_mongo['end_date'] = 'Cesta nie je ukon%sen%s' % (u"\u010D", u"\u00E1")

    if int(detail_mongo['completed']) == 1:
        detail_mongo['cela'] = 'Ano'
    if int(detail_mongo['completed']) == 0:
        detail_mongo['cela'] = 'Nie'

    try:
        if detail_mongo['finished'] == False:
            detail_mongo['ukoncil'] = 'Nie'
        if detail_mongo['finished'] == True:
            detail_mongo['ukoncil'] = 'Ano'
    except:
        detail_mongo['ukoncil'] = 'Ano'

    if request.method == 'GET':
        return render_template('details_show.html', detail=detail_mongo)


@details.route('/details_edit', methods=['GET', 'POST'])
@login_required
def details_edit():
    detail_mongo = details_mongo.find_one({'user_id': g.user.id})
    if request.method == 'GET':
        try:
            detail_mongo['start_date'] = detail_mongo['start_date'].strftime('%d.%m.%Y')
        except:
            pass
        try:
            detail_mongo['start_date'] = detail_mongo['start_date'].strftime('%d.%m.%Y')
        except:
            pass

        if detail_mongo['end_date'] == "0000-00-00 00:00:00":
            detail_mongo['end_date'] = 'Cesta nie je ukon%sen%s' % (u"\u010D", u"\u00E1")

        if detail_mongo['completed'] == False:
            activeBtn = '0'
        if detail_mongo['completed'] == True:
            activeBtn = '1'

        try:
            if detail_mongo['finished'] == False:
                cesta_ukoncena = '0'
            if detail_mongo['finished'] == True:
                cesta_ukoncena = '1'
        except:
            cesta_ukoncena = '1'

        # return render_template('details_edit.html', detail=detail)
        return render_template('details_edit.html', detail=detail_mongo, active_btns=activeBtn, active_btns_route=cesta_ukoncena)


    file = request.files['file']
    if file and allowed_file(file.filename):
        file_to_upload = request.files['file']
        upload_result = upload(
            file_to_upload,
            tags="live_sledovanie_profile",
            eager={'width': 248, 'height': 140, 'crop': 'fill' }
        )
        dump_response(upload_result)

        print("file to cloudinary uploaded")
    else:
        print("no file to upload using original")
        upload_result = detail_mongo['img']

    komplet = request.form.get('gender', '')

    if komplet == '1':
        komplet = True
    if komplet == '0':
        komplet = False

    try:
        print("writing to mongo STARTING")
        print(detail_mongo)
        detail_mongo.update_one(
            {'user_id': g.user.id},
            {'$set':
                 {
                     'meno': request.form['meno'],
                     'text': request.form['text'],
                     'number': request.form['number'],
                     'start_miesto': request.form['start_miesto'],
                     'start_date': datetime.strptime(request.form['start_date'], "%d.%m.%Y"),
                     'end_date': request.form['end_date'],
                     'completed': komplet,
                     'img': upload_result
                 }
            },
            upsert=True, wtimeout=1000
        )
        print("writing to mongo DONE\n")
    except:
        print("some error")
        pass

    return redirect(url_for('details.details_show'))

