import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g, send_from_directory, jsonify
from flask import Blueprint
from werkzeug import secure_filename
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
import hashlib
from ftpcopy import resize_and_copy_to_cesta_ftp, delete_openshift_img
from cas import cas
from cestadb import *
from places import places
from gettingstarted import gettingstarted
import uuid
import phpass


app = Flask(__name__)

app.config['SQLALCHEMY_POOL_RECYCLE'] = 60
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['MYSQL_DB']
app.config['SQLALCHEMY_BINDS'] = {
    'db1': app.config['SQLALCHEMY_DATABASE_URI'],
    'db2': os.environ['WORDPRESS_DB']
}

app.secret_key = os.environ['APP_SECRET_KEY']

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u"Prihl%ss sa pou%sit%sm prihl. %sdajov CestaSNP.sk." %(u"\u00E1", u"\u017E", u"\u00ED", u"\u00FA")

#path = '/Users/lcicon/Documents/Openshift/sledovanie/img/'
#path = '/home/hasty/Developement/web/OpenShift/sledovanie/wsgi/img/'
path = 'img/'
app.config['UPLOAD_FOLDER'] = path
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif', 'JPG', 'JPEG'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@login_manager.user_loader
def load_user(id):
    return Jos_users.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
        
def detailsExist(datils):
    if details.user_id == g.user:
        return True
    else:
        return False

#zacinaju views
app.register_blueprint(places)
app.register_blueprint(gettingstarted)

@app.route('/',methods=['GET'])
@login_required
def index():  
    try:
        spravy=Sprava.query.filter_by(user_id = g.user.id).order_by(Sprava.pub_date.desc()).all()
        return render_template('index.html', spravy=spravy)
    except:
        flash('Spojenie bolo ukoncene, prihlas sa znovu')
        return redirect(url_for('login'))

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_sprava(id):
    try:
        sprava = Sprava.query.get(id)
    except:
        flash('error occured in delete')
        return redirect(url_for('/delete/<int:id>'))
    
    if sprava.lessOne(sprava):
        if sprava.img != 'None':
            delete_openshift_img(sprava.img,g.user.id)
        db.session.delete(sprava)
        db.session.commit()
        flash('Spr%sva bola zmazan%s' %(u"\u00E1",u"\u00E1"))
    else:
        flash('Spr%svu u%s nie je mo%sn%s zmaza%s' %(u"\u00E1",  u"\u017E",  u"\u017E", u"\u00E9", u"\u0165"))
    return redirect(url_for('index')) 

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    
    try:
        saved_password = Jos_users.query.filter_by(username=username).first()
        print "robim query na Jos_users s username '%s'" %username


    except:
        print " query na Jos_users skoncila s chybou"
        flash('hjustne mame problem 1')
        return redirect(url_for('login'))

    registered_user = saved_password
        
    try:
        print "hladam heslo v saved_password"
        saved_password = saved_password.password
        new_password_to_check = saved_password

        print new_password_to_check

        old_password_ok = False
        new_password_ok = False

        try:
            list_of_password = saved_password.split(':')
            saved_password = list_of_password[0]
            salt = list_of_password[1]
            # check the password
            pwhash = hashlib.md5()
            pwhash.update(password)
            pwhash.update(salt)

            if pwhash.hexdigest() == saved_password:
                old_password_ok = True
                print "old password fro old joomla users is '%s'" %old_password_ok
        except:
            new_password_ok = phpass.PasswordHash()
            new_password_ok = new_password_ok.check_password(pw=password, stored_hash=new_password_to_check)
            print "new password for new wordpress users is '%s'" % new_password_ok


        if old_password_ok == False and new_password_ok == False:
            flash('U%s%svate%ssk%s meno alebo heslo nie je spr%svne' % (
            u"\u017E", u"\u00ED", u"\u013E", u"\u00E9", u"\u00E1"))
            return redirect(url_for('login'))

        print registered_user
        login_user(registered_user, remember=True)

        usersId = Details.query.filter_by(user_id=registered_user.id).first()
        try:
            usersId = usersId.meno
        except:
            return redirect(url_for('details'))
        # flash('uzivatel s menom %s uz vyplnil detaily'  %usersId)
        return redirect(request.args.get('next') or url_for('index'))

    except:

        try:
            print "skusam najst uzivatela v Ippmgpusers"
            print "pripajam sa k DB"
            db_con = mysql.connector.connect(
                user='k72ny9v0yxb0',
                password='gqnkzd22wzlk',
                host='mariadb101.websupport.sk',
                port='3312',
                database='k72ny9v0yxb0'
            )

            cursor5= db_con.cursor()
            query = ("SELECT id, user_login, user_pass, user_email FROM ippmgpusers WHERE 1")

            print "idem vykonat query na mysql"
            cursor5.execute(query)

            print cursor5

            for abcd, user_login, user_pass, user_email in cursor5:
                if user_login == username:
                    heslo_db = user_pass
                    email = user_email
                    print "uzivatel '%s' sa nasiel v ippmgpusers" %username

            cursor5.close()
            db_con.close()

            print "uzivatel sa nasiel v ippmgpusers. Vyrabam kopiu uivatela"

            user = Jos_users(name=username, username=username, email=email, password=heslo_db)

            print "ukladam kopiu uzivatela do Jos_users, %s" %user

            db.session()
            db.session.add(user)
            db.session.commit()

            print "kopia bola uzlozena uzivatela do Jos_users, %s" % user
            print "skusam prihlasit noveho usera"

            try:
                saved_password = Jos_users.query.filter_by(username=username).first()
                print "robim query na Jos_users s username '%s'" % username

            except:
                print " query na Jos_users skoncila s chybou"
                flash('hjustne mame problem 1')
                return redirect(url_for('login'))

            print "hladam heslo v saved_password"
            saved_password = saved_password.password
            new_password_to_check = saved_password

            print new_password_to_check

            new_password_ok = phpass.PasswordHash()
            new_password_ok = new_password_ok.check_password(pw=password, stored_hash=new_password_to_check)
            print "new password for new wordpress users is '%s'" % new_password_ok

            if new_password_ok == False:
                flash('U%s%svate%ssk%s meno alebo heslo nie je spr%svne' % (
                    u"\u017E", u"\u00ED", u"\u013E", u"\u00E9", u"\u00E1"))
                return redirect(url_for('login'))

            print registered_user
            login_user(registered_user, remember=True)

            try:
                usersId = Details.query.filter_by(user_id=registered_user.id).first()
                usersId = usersId.meno
            except:
                return redirect(url_for('details'))
            # flash('uzivatel s menom %s uz vyplnil detaily'  %usersId)
            return redirect(request.args.get('next') or url_for('index'))

        except:
            print " query na Ippmgpusers skoncila bez uzivatela"
            flash('U%s%svate%ssk%s meno alebo heslo nie je spr%svne' % (
                u"\u017E", u"\u00ED", u"\u013E", u"\u00E9", u"\u00E1"))
            flash('U%s%svate%ssk%s meno alebo heslo nie je spr%svne' %(u"\u017E", u"\u00ED", u"\u013E", u"\u00E9", u"\u00E1") )
            return redirect(url_for('login'))
    


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index')) 

#obsolete, drzime koli spatnaj kompatibilite ak ma nejaky user /sledovanie v zalozkach. zmazat mozne na konci leta
@app.route('/sledovanie', methods=['GET', 'POST'])
@login_required
def new():
    return redirect(url_for('spravy'))

@app.route('/spravy', methods=['GET', 'POST'])
@login_required
def spravy():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = str(uuid.uuid4()) + secure_filename(file.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resize_and_copy_to_cesta_ftp(filename,path,g.user.id)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Redirect the user to the uploaded_file route, which
            # will basically show on the browser the uploaded file
        else:
            filename = 'None'
        if not request.form['lat']:
            flash('Title is required', 'error')
        elif not request.form['lon']:
            flash('Text is required', 'error')
        elif not request.form['text']:
            flash('Text is required', 'error')
        else:
            details = Details.query.with_entities(Details.id).filter_by(user_id=g.user.id).first()
            sprava = Sprava(request.form['lat'], request.form['lon'], request.form['text'], filename, request.form['accuracy'])
            sprava.user_id = g.user.id
            sprava.details_id = details.id
            #sprava.accuracy = request.form['accuracy']
            # save to DB
            db.session()    
            db.session.add(sprava)
            db.session.commit()
            flash('Spr%sva bola ulo%sen%s' %(u"\u00E1", u"\u017E", u"\u00E1"))
            return redirect(url_for('index'))
    suradnice = Sprava.query.filter_by(user_id = g.user.id).order_by(Sprava.pub_date.desc()).first()
    return render_template('spravy.html', suradnice=suradnice)

@app.route('/spravy/<int:id>', methods=['GET','POST'])
@login_required
def show_or_update(id):
    sprava = Sprava.query.get(id)
    if request.method == 'GET':
        return render_template('edit.html',sprava=sprava)
    sprava.lat = request.form['lat']
    sprava.lon  = request.form['lon']
    sprava.text  = request.form['text']
    sprava.accuracy = request.form['accuracy']
    
    # save changes to DB
    db.session()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return redirect('https://cestasnp.sk/images/stories/Ostatne/sledovanie_upload/%s' %filename)

@app.route('/details', methods=['GET','POST'])
@login_required
def details():
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
    return redirect(url_for('gettingstarted.akozacat'))

@app.route('/details_show', methods=['GET'])
@login_required
def details_show():
    print "g.user.id na view s nazvom details_show je:"
    print g.user.id
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
        detail.end_date = 'Cesta nie je ukon%sen%s' %(u"\u010D", u"\u00E1")
        
    if detail.completed == True:
            detail.completed = 'Ano'
    if detail.completed == False:
            detail.completed = 'Nie'
            
    if request.method == 'GET':
        return render_template('details_show.html', detail=detail)

@app.route('/details_edit', methods=['GET','POST'])
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
            detail.end_date = 'Cesta nie je ukon%sen%s' %(u"\u010D", u"\u00E1")
        
        if detail.completed == False:
            activeBtn = '0'
        if detail.completed == True:
            activeBtn = '1'
            
        #return render_template('details_edit.html', detail=detail)
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
    return redirect(url_for('details_show'))

@app.route('/comments',methods=['GET'])
@login_required
def comments():  
    try:
        clanok = Details.query.with_entities(Details.articleID).filter_by(user_id=g.user.id).first()
        clanok_id = clanok.articleID
        comments=Jos_jcomments.query.filter_by(object_id = clanok_id).order_by(Jos_jcomments.date.desc()).all()
        return render_template('comments.html', comments=comments, clanok_id=clanok_id)
    except:
        flash('Spojenie bolo ukoncene, prihlas sa znovu')
        return redirect(url_for('index'))

@app.route('/miesta', methods=['GET','POST'])
@login_required
def miesta():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = str(uuid.uuid4()) + secure_filename(file.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("LOG img saved to openshift")
            resize_and_copy_to_cesta_ftp(filename,app.config['UPLOAD_FOLDER'],'miesta')
            print("LOG img copied to ftp")
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("LOG img deleted from openshift")
            # Redirect the user to the uploaded_file route, which
            # will basically show on the browser the uploaded file
        else:
            filename = 'None'

        if not request.form['lat']:
            flash('Suradnice neboli zadane', 'error')
        elif not request.form['lon']:
            flash('Suradnice neboli zadane', 'error')
        elif not request.form['name']:
            flash('Nazov nie je zadany', 'error')
        elif not request.form['category']:
            flash('Kategoria nebola zvolena', 'error')
        else:
            miesto = {
                'accuracy': int(float(request.form['accuracy'])),
                'category': request.form['category'],
                'name': request.form['name'],
                'img_url': filename,
                #'user_id': int(g.user.id),
                'created': datetime.now(),
                'text': request.form['text']
            }

            miesto['coordinates'] = (float(request.form['lon']), float(request.form['lat']))

            print("LOG poi json object has been created: \n %s" %miesto)
            try:
                print("LOG inserting into mongoDB will start")
                poi.insert_one(miesto)
                print("LOG inserting into mongoDB done")
            except:
                print("ERROR error saving miesto to mongoDB")

            flash('Miesto bolo ulo%sen%s. %sakujeme.' %(u"\u017E", u"\u00E9", u"\u010E"))
            return redirect(url_for('miesta'))
    return render_template('miesta.html')



if __name__ == '__main__':
    app.run(debug = False)
"""
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
"""