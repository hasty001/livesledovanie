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

    miesto = {
                'accuracy': int(float(m[3])),
                'category': m[4],
                'name': m[5],
                'img_url': m[7],
                'user_id': m[9],
                'created': m[8],
                'text': m[6]
            }
    miesto['coordinates'] = (float(m[2]), float(m[1]))

    print miesto



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