from flask import Blueprint
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g, send_from_directory

gettingstarted = Blueprint('gettingstarted', __name__, template_folder='templates')

@gettingstarted.route('/akozacat', methods=['GET'])
@login_required
def akozacat():
    if request.method == 'GET':
        return render_template('gettingstarted.html')