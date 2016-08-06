import os
import MySQLdb
from datetime import datetime, timedelta
import smtplib
import sys

db = MySQLdb.connect(host="mysql50.websupport.sk", # your host, usually localhost
                     port=3308,
                     user="nova_15182", # your username
                     passwd="StopSkurvencom1256", # your password
                     db="nova_15182") # name of the data base

cur = db.cursor()

cur.execute("SELECT * FROM miesta;" )
miesta = cur.fetchall()

for m in miesta:
    print m[4]
    """
    miesto = {
                'accuracy': int(float(m.accuracy)),
                'category': m.category,
                'name': m.name,
                'img_url': m.img,
                'user_id': m.user_id,
                'created': m.pub_date,
                'text': m.text
            }
    miesto['coordinates'] = (float(m.lon), float(m.lat))
    """



"""
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

poi.insert_one(miesto)

"""