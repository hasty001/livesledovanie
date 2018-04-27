from flask import Blueprint, jsonify
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g, send_from_directory, current_app
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from cestadb import *

details = Blueprint('details', __name__, template_folder='templates')


@details.route('/details', methods=['GET','POST'])
@login_required
def details_add():
    if request.method == 'GET':
        return render_template('details.html')
    end_date='NULL'
    #user_id = g.user
    completed = 0
    #detail = Details(request.form['meno'], request.form['text'], datetime.strptime(request.form['start_date'], "%d.%m.%Y"), datetime.strptime(request.form['end_date'], "%d.%m.%Y"), completed, g.user.id, request.form['start_miesto'], request.form['number'], 0, 0)detail = Details(request.form['meno'], request.form['text'], datetime.strptime(request.form['start_date'], "%d.%m.%Y"), datetime.strptime(request.form['end_date'], "%d.%m.%Y"), completed, g.user.id, request.form['start_miesto'], request.form['number'], 0, 0)
    detail = Details(request.form['meno'], request.form['text'], datetime.strptime(request.form['start_date'], "%d.%m.%Y"), end_date, completed, g.user.id, request.form['start_miesto'], request.form['number'], 0, 0)
    db.session()
    db.session.add(detail)
    db.session.commit()

    detail_json = {
        "meno": request.form['meno'],
        "text": request.form['text'],
        "start_date": str(datetime.strptime(request.form['start_date'], "%d.%m.%Y")),
        "end_date": end_date,
        "completed": completed,
        "user_id": int(g.user.id),
        "start_miesto": request.form['start_miesto'],
        "number": request.form['number'],
        "email": 0,
        "articleID": 0
    }

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
    detail = Details.query.filter_by(user_id=g.user.id).first()
    if detail == None:
        return redirect(url_for('details'))
    try:
        detail.start_date = detail.start_date.strftime('%d.%m.%Y')
    except:
        pass
    try:
        detail.end_date = detail.end_date.strftime('%d.%m.%Y')
    except:
        pass

    if detail.end_date == None:
        detail.end_date = 'Cesta nie je ukon%sen%s' % (u"\u010D", u"\u00E1")

    if detail.completed == True:
        detail.completed = 'Ano'
    if detail.completed == False:
        detail.completed = 'Nie'

    if request.method == 'GET':
        return render_template('details_show.html', detail=detail)


@details.route('/details_edit', methods=['GET', 'POST'])
@login_required
def details_edit():
    detail = Details.query.filter_by(user_id=g.user.id).first()
    if request.method == 'GET':
        try:
            detail.start_date = detail.start_date.strftime('%d.%m.%Y')
        except:
            pass
        try:
            detail.end_date = detail.end_date.strftime('%d.%m.%Y')
        except:
            pass

        if detail.end_date == None:
            detail.end_date = 'Cesta nie je ukon%sen%s' % (u"\u010D", u"\u00E1")

        if detail.completed == False:
            activeBtn = '0'
        if detail.completed == True:
            activeBtn = '1'

        # return render_template('details_edit.html', detail=detail)
        return render_template('details_edit.html', detail=detail, active_btns=activeBtn)

    detail.meno = request.form['meno']
    detail.text = request.form['text']
    detail.number = request.form['number']
    detail.start_miesto = request.form['start_miesto']
    detail.start_date = datetime.strptime(request.form['start_date'], "%d.%m.%Y")
    detail.end_date = request.form['end_date']

    komplet = request.form.get('gender', '')

    if komplet == '1':
        detail.completed = True
    if komplet == '0':
        detail.completed = False

    try:
        detail.end_date = datetime.strptime(request.form['end_date'], "%d.%m.%Y")
    except:
        detail.end_date = None
    db.session()
    db.session.add(detail)
    db.session.commit()
    return redirect(url_for('details.details_show'))

