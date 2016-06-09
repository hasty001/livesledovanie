from flask import Blueprint, jsonify
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g, send_from_directory

places = Blueprint('places', __name__, template_folder='templates')

@places.route('/poi', methods=['GET'])
#@login_required
def poi():
    if request.method == 'GET':
        return render_template('places.html')
    
@places.route('/scitaj')
#@login_required
def vysledok():
    a = request.args.get('a', 0, type=float)
    b = request.args.get('b', 0, type=float)
    c = request.args.get('c', 0, type=float)
    return jsonify(result=c + b)