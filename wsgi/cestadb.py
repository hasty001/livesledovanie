from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from cas import cas
from datetime import datetime, timedelta
from flask import Flask

db = SQLAlchemy()

class Jos_users(db.Model):
    __tablename__ = 'jos_users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(150))
    username = db.Column('username', db.String(75))
    email = db.Column('email', db.String(300))
    password = db.Column('password', db.String(300))
    usertype = db.Column('usertype', db.String(75))
    block = db.Column('block', db.Integer())
    sendemail = db.Column('sendemail', db.Integer()) # Field name made lowercase.
    gid = db.Column('gid', db.Integer())
    registerdate = db.Column('registerdate' , db.DateTime) # Field name made lowercase.
    lastvisitdate = db.Column('lastvisitdate' , db.DateTime) # Field name made lowercase.
    activation = db.Column('activation', db.String(300))
    params = db.Column('params',db.String(300))
     
    def __init__(self , name, username ,password , email):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
    
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

class Sprava(db.Model):
    __tablename__ = 'spravy'
    id = db.Column('id', db.Integer, primary_key=True)
    lat = db.Column('lat', db.Float(precision='2,5'))
    lon = db.Column('lon', db.Float(precision='2,5'))
    text = db.Column('text', db.String(2500))
    img = db.Column('img', db.String(100))
    pub_date = db.Column('pub_date', db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('jos_users.id'))
    details_id = db.Column(db.Integer, db.ForeignKey('details.id'))
    accuracy = db.Column('accuracy', db.Integer)
    
 
    def __init__(self, lat, lon, text, img, accuracy):
        self.lat = lat
        self.lon = lon
        self.text = text
        self.img = img
        self.pub_date = cas()
        self.accuracy = accuracy
    
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

"""
jos_jcomments

`id` int(11) unsigned NOT NULL auto_increment,
  `parent` int(11) unsigned NOT NULL default '0',
  `path` varchar(255) NOT NULL default '',
  `level` tinyint(1) unsigned NOT NULL default '0',
  `object_id` int(11) unsigned NOT NULL default '0',
  `object_group` varchar(255) NOT NULL default '',
  `object_params` text NOT NULL,
  `lang` varchar(255) NOT NULL default '',
  `userid` int(11) unsigned NOT NULL default '0',
  `name` varchar(255) NOT NULL default '',
  `username` varchar(255) NOT NULL default '',
  `email` varchar(255) NOT NULL default '',
  `homepage` varchar(255) NOT NULL default '',
  `title` varchar(255) NOT NULL default '',
  `comment` text NOT NULL,
  `ip` varchar(15) NOT NULL default '',
  `date` datetime NOT NULL default '0000-00-00 00:00:00',
  `isgood` smallint(5) unsigned NOT NULL default '0',
  `ispoor` smallint(5) unsigned NOT NULL default '0',
  `published` tinyint(1) unsigned NOT NULL default '0',
  `subscribe` tinyint(1) unsigned NOT NULL default '0',
  `source` varchar(255) NOT NULL default '',
  `source_id` int(11) unsigned NOT NULL default '0',
  `checked_out` int(11) unsigned NOT NULL default '0',
  `checked_out_time` datetime NOT NULL default '0000-00-00 00:00:00',
  `editor` varchar(50) NOT NULL default '',
  PRIMARY KEY  (`id`),
  KEY `idx_userid` (`userid`),
  KEY `idx_source` (`source`),
  KEY `idx_email` (`email`),
  KEY `idx_lang` (`lang`),
  KEY `idx_subscribe` (`subscribe`),
  KEY `idx_checkout` (`checked_out`),
  KEY `idx_object` (`object_id`,`object_group`,`published`,`date`),
  KEY `idx_level` (`level`),
  KEY `idx_path` (`path`,`level`)
  
  test len s: id, object_id, username, comment, date, published
"""


class Jos_jcomments(db.Model):
    __tablename__ = 'jos_jcomments'
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