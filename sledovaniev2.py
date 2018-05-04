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
from details import details
from gettingstarted import gettingstarted
import uuid
import phpass
from cloudinary.uploader import upload


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
app.register_blueprint(details)
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
        print("robim query na Jos_users s username '%s'" %username)


    except:
        print(" query na Jos_users skoncila s chybou")
        flash('hjustne mame problem 1')
        return redirect(url_for('login'))

    registered_user = saved_password
        
    try:

        saved_password = saved_password.password
        new_password_to_check = saved_password

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
                print("old_password_ok z Jos_users je vyhodnotene ako True na zaklade md5")
        except:
            new_password_ok = phpass.PasswordHash()
            new_password_ok = new_password_ok.check_password(pw=password, stored_hash=new_password_to_check)
            print("old_password_ok z Jos_users je vyhodnotene ako %s na zaklade phpass" %new_password_ok)

        print("old_password_ok %s, new_password_ok %s" %(old_password_ok, new_password_ok))
        if old_password_ok == False and new_password_ok == False:
            print("ani jedno heslo nie je spravne")
            flash('U%s%svate%ssk%s meno alebo heslo nie je spr%svne' % (
            u"\u017E", u"\u00ED", u"\u013E", u"\u00E9", u"\u00E1"))
            return redirect(url_for('login'))

        print("idem robit login")
        login_user(registered_user, remember=True)

        print("query na details")
        print(registered_user.id)

        usersId = Details.query.filter_by(user_id=registered_user.id).first()
        try:
            print("skusam usersId.meno")
            usersId = usersId.meno
        except:
            return redirect(url_for('details.details_show'))
            print("redirect na details")


        return redirect(request.args.get('next') or url_for('index'))

    except:

        try:
            db_con = mysql.connector.connect(os.environ['WORDPRESS_DB'])
            print("connected to wordpres DB")

            cursor5= db_con.cursor()
            query = ("SELECT id, user_login, user_pass, user_email FROM ippmgpusers WHERE 1")

            cursor5.execute(query)

            for abcd, user_login, user_pass, user_email in cursor5:
                if user_login == username:
                    heslo_db = user_pass
                    email = user_email


            cursor5.close()
            db_con.close()


            user = Jos_users(name=username, username=username, email=email, password=heslo_db)


            db.session()
            db.session.add(user)
            db.session.commit()


            try:
                saved_password = Jos_users.query.filter_by(username=username).first()

            except:
                flash('hjustne mame problem 1')
                return redirect(url_for('login'))

            saved_password = saved_password.password
            new_password_to_check = saved_password


            new_password_ok = phpass.PasswordHash()
            new_password_ok = new_password_ok.check_password(pw=password, stored_hash=new_password_to_check)

            if new_password_ok == False:
                flash('U%s%svate%ssk%s meno alebo heslo nie je spr%svne' % (
                    u"\u017E", u"\u00ED", u"\u013E", u"\u00E9", u"\u00E1"))
                return redirect(url_for('login'))

            login_user(registered_user, remember=True)

            try:
                usersId = Details.query.filter_by(user_id=registered_user.id).first()
                usersId = usersId.meno
            except:
                return redirect(url_for('details'))
            # flash('uzivatel s menom %s uz vyplnil detaily'  %usersId)
            return redirect(request.args.get('next') or url_for('index'))

        except:
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
        if not request.form['lat']:
            flash('Title is required', 'error')
        elif not request.form['lon']:
            flash('Text is required', 'error')
        elif not request.form['text']:
            flash('Text is required', 'error')
        else:
            file = request.files['file']
            if file and allowed_file(file.filename):
                file_to_upload = request.files['file']
                upload_result = upload(
                    file_to_upload,
                    tags="live_sledovanie",
                    eager={'width': 248, 'height': 140, 'crop': 'fill'}
                )
                filename = upload_result["url"]
                print("fotka poslana na cloudinary, DONE")
            else:
                upload_result = None
                filename = None
            print("presnost je podla formularu %s") %request.form['accuracy']
            if not request.form['accuracy']:
                print("accuracy nie je nastavena a bude 100")
                accuracy = 100
            else:
                print("presnost bude teraz nastavena na int")
                accuracy = int(request.form['accuracy'])
                print("presnost je teraz nastavena na int")
                print(accuracy)

            print("latitude")
            print(request.form['lat'])
            print("longitude")
            print(request.form['lon'])
            print("text")
            print(request.form['text'])

            try:
                details = Details.query.with_entities(Details.id).filter_by(user_id=g.user.id).first()
                print("detais id je: %s") %details.id
            except:
                print("details id nie je v SQl, hladam v mongu")
                detail_mongo = details_mongo.find_one({'user_id': g.user.id})


                if detail_mongo is None:
                    print("detail v mongu nie je")
                    flash('Spr%sva nebola ulo%sen%s, vypln Detail o tvojej Ceste' % (u"\u00E1", u"\u017E", u"\u00E1"))
                    return redirect(url_for('details.details_add'))
                print("details id v mongu je ako: %s") % detail_mongo['_id']

            print("ukladam spravu")
            sprava = Sprava(request.form['lat'], request.form['lon'], request.form['text'], filename,
                            accuracy)

            sprava.user_id = g.user.id
            sprava.details_id = details.id
            #sprava.accuracy = request.form['accuracy']
            # save to DB
            print("do SQL vkladam")
            print(sprava)
            db.session()    
            db.session.add(sprava)
            db.session.commit()

            sprava_json = {
                             "lat": float(request.form['lat']),
                             "lon": float(request.form['lon']),
                             "text": request.form['text'],
                             "img": upload_result,
                             "pub_date": str(cas()).split('+')[0].split('.')[0],
                             "pub_date_milseconds": "timestamp",
                             "user_id": int(g.user.id),
                             "details_id": int(details.id),
                             "accuracy": accuracy
            }
            try:
                print("LOG inserting od message into mongoDB will start")
                spravy_mongo.insert_one(sprava_json)
                print("LOG inserting into mongoDB done")
            except:
                print("ERROR error saving sprava to mongoDB")
            flash('Spr%sva bola ulo%sen%s' %(u"\u00E1", u"\u017E", u"\u00E1"))
            return redirect(url_for('index'))


    suradnice = Sprava.query.filter_by(user_id = g.user.id).order_by(Sprava.pub_date.desc()).first()
    return render_template('spravy.html', suradnice=suradnice)

@app.route('/spravy/<int:id>', methods=['GET','POST'])
@login_required
def show_or_update(id):
    sprava = Sprava.query.get(id)
    print(sprava.pub_date)
    sprava_mongo = spravy_mongo.find_one({'$and':[{'user_id': g.user.id}, {'pub_date':str(sprava.pub_date)}]})
    print(sprava_mongo)
    if request.method == 'GET':
        return render_template('edit.html',sprava=sprava)

    sprava.lat = request.form['lat']
    sprava.lon = request.form['lon']
    sprava.text = request.form['text']
    sprava.accuracy = request.form['accuracy']

    # save changes to DB
    db.session()
    db.session.commit()

    try:
        print("writing to mongo STARTING")
        print(request.form['text'])
        spravy_mongo.update_one({'$and': [{'user_id': g.user.id}, {'pub_date':str(sprava.pub_date)}]},
                                 {'$set':
                                      {
                                          'lat': request.form['lat'],
                                          'lon': request.form['lon'],
                                          'text': request.form['text'],
                                          'accuracy': request.form['accuracy']
                                      }
                                  }, upsert=False)
        print("writing to mongo DONE\n")
    except:
        print("some error")
        pass

    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return redirect('https://cestasnp.sk/images/stories/Ostatne/sledovanie_upload/%s' %filename)


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
            file_to_upload = request.files['file']
            upload_result = upload(
                file_to_upload,
                tags="pois",
                eager={'width': 248, 'height': 140, 'crop': 'fill'}
            )
        else:
            upload_result = None

        try:
            accuracy = int(float(request.form['accuracy']))
        except:
            accuracy = None

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
                'accuracy': accuracy,
                'category': request.form['category'],
                'name': request.form['name'],
                'img_url': upload_result,
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
    app.run(debug=True, host='0.0.0.0', port=5000)
"""