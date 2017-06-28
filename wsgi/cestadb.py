from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from cas import cas
from datetime import datetime, timedelta
from flask import Flask
from pymongo import MongoClient
import os
import mysql.connector

db = SQLAlchemy()

#mongoDB for location data

client = MongoClient("mongodb://admin:51dBVLs4ZLpi@%s:%s/" \
                     % (os.environ['OPENSHIFT_MONGODB_DB_HOST'],os.environ['OPENSHIFT_MONGODB_DB_PORT']))
mongodb = client.sledovanie
poi = mongodb.poi

    #
    #"mongo":        "mongodb://admin:51dBVLs4ZLpi@%s:%s/" \
    #                       %(os.environ['OPENSHIFT_MONGODB_DB_HOST'],os.environ['OPENSHIFT_MONGODB_DB_PORT'])
    #
    #"mongo":        "mongodb://admin:51dBVLs4ZLpi@%s:%s/" %("127.0.0.1","27017")
    #   rhc port-forward -a sledovanie



#SQL for others

class Jos_users(db.Model):
    __tablename__ = 'jos_users'
    __bind_key__ = 'db1'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(150))
    username = db.Column('username', db.String(75))
    email = db.Column('email', db.String(300))
    password = db.Column('password', db.String(300))
    """
    usertype = db.Column('usertype', db.String(75))
    block = db.Column('block', db.Integer())
    sendemail = db.Column('sendemail', db.Integer()) # Field name made lowercase.
    gid = db.Column('gid', db.Integer())
    registerdate = db.Column('registerdate' , db.DateTime) # Field name made lowercase.
    lastvisitdate = db.Column('lastvisitdate' , db.DateTime) # Field name made lowercase.
    activation = db.Column('activation', db.String(300))
    params = db.Column('params',db.String(300))
    """
     
    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
    
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<Jos_users %r>' % (self.username)

""""CREATE TABLE `ippmgpusers` (
  `ID` bigint(20) UNSIGNED NOT NULL,
  `user_login` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_pass` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_nicename` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_url` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_registered` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `user_activation_key` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `user_status` int(11) NOT NULL DEFAULT '0',
  `display_name` varchar(250) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"""


class Ippmgpusers(db.Model):
    __tablename__ = 'ippmgpusers'
    __bind_key__ = 'db2'
    id = db.Column('id', db.Integer, primary_key=True)
    user_login = db.Column('user_login', db.String(60))
    user_pass = db.Column('user_pass', db.String(255))
    user_nicename = db.Column('user_nicename', db.String(50))
    user_email = db.Column('user_email', db.String(100))
    user_url = db.Column('user_url', db.String(100))
    user_registered = db.Column('user_registered', db.DateTime)  # Field name made lowercase.
    user_status = db.Column('user_status', db.Integer)  # Field name made lowercase.
    display_name = db.Column('display_name', db.String(250))

    def __init__(self, id, display_name, user_login, user_pass, user_email):
        self.id = id
        self.name = display_name
        self.username = user_login
        self.password = user_pass
        self.email = user_email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Ippmgpusers %r>' % (self.user_login)


class Sprava(db.Model):
    __tablename__ = 'spravy'
    __bind_key__ = 'db1'
    id = db.Column('id', db.Integer, primary_key=True)
    lat = db.Column('lat', db.Float(precision='2,5'))
    lon = db.Column('lon', db.Float(precision='2,5'))
    text = db.Column('text', db.String(2500))
    img = db.Column('img', db.String(100))
    pub_date = db.Column('pub_date', db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('jos_users.id'))
    details_id = db.Column(db.Integer, db.ForeignKey('details.id'))
    accuracy = db.Column('accuracy', db.Integer)
    
 
    def __init__(self, lat, lon, text, img, accuracy, user_id):
        self.lat = lat
        self.lon = lon
        self.text = text
        self.img = img
        self.pub_date = cas()
        self.accuracy = accuracy
        self.user_id = user_id
    
    def lessOne(self, sprava):
        if sprava.pub_date > (datetime.utcnow() + timedelta(hours=1)): #kvoli letnemu casu pridavm k UTC 1hodinu (UTC + 1h)
            return True
        else:
            return False
    
    def fotoUploaded(self, sprava):
        if sprava.img == 'None':
            return False
        else:
            return True

class Details(db.Model):
    __tablename__ = 'details'
    __bind_key__ = 'db1'
    id = db.Column('id', db.Integer, primary_key=True)
    meno = db.Column('meno', db.String(32))
    text = db.Column('text', db.String(2500))
    start_date = db.Column('start_date', db.DateTime)
    end_date = db.Column('end_date', db.DateTime)
    completed = db.Column('completed', db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('jos_users.id'))
    start_miesto = db.Column('start_miesto', db.String(32))
    number = db.Column('number', db.Integer)
    email = db.Column('email',db.Boolean)
    articleID = db.Column('articleID', db.Integer)
    
    def __init__(self, meno, text, start_date, end_date, completed, user_id, start_miesto, number, email, articleID):
        self.meno = meno
        self.text = text
        self.start_date = start_date
        self.end_date = end_date
        self.completed = completed
        self.user_id = user_id
        self.start_miesto = start_miesto
        self.number = number
        self.email = email
        self.articleID = articleID


class Jos_jcomments(db.Model):
    __tablename__ = 'jos_jcomments'
    __bind_key__ = 'db1'
    id = db.Column('id', db.Integer, primary_key=True)
    #parent = db.Column('parent', db.Integer())
    #path = db.Column('path', db.String(255))
    #level = db.Column('level', db.Boolean)
    object_id = db.Column('object_id', db.Integer())
    #object_group = db.Column('object_group', db.String(255))
    #object_params = db.Column('object_params', db.String(300))
    #lang = db.Column('lang', db.String(255))
    #userid = db.Column('userid', db.Integer())
    username = db.Column('username', db.String(255))
    comment = db.Column('comment', db.String(300))
    date = db.Column('date', db.DateTime)
    published = db.Column('published', db.Boolean)
     
    def __init__(self , object_id, username ,comment , date, published):
        self.object_id = object_id
        self.username = username
        self.comment = comment
        self.date = cas()
        self.published = published
        
class Miesta(db.Model):
    __tablename__ = 'miesta'
    __bind_key__ = 'db1'
    id = db.Column('id', db.Integer, primary_key=True)
    lat = db.Column('lat', db.Float)
    lon = db.Column('lon', db.Float)
    accuracy = db.Column('accuracy', db.Integer)
    category = db.Column('category', db.String(2500))
    name = db.Column('name', db.String(2500))
    text = db.Column('text', db.String(2500))
    img = db.Column('img', db.String(100))
    pub_date = db.Column('pub_date', db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('jos_users.id'))    
    
    def __init__(self, lat, lon, accuracy, category, name, text, img):
        self.lat = lat
        self.lon = lon
        self.accuracy = accuracy
        self.category = category
        self.name = name
        self.text = text
        self.img = img
        self.pub_date = cas()
    
    def fotoMiestoUploaded(self, miesto):
        if miesto.img == 'None':
            return False
        else:
            return True