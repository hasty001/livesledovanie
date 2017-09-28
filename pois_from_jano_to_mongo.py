# -*- coding: utf-8 -*-
from pymongo import MongoClient
from datetime import datetime
import untangle

#mongoDB for migrating jano's data
client = MongoClient("mongodb://admin:51dBVLs4ZLpi@%s:%s/" %("127.0.0.1","27017"))
mongodb = client.sledovanie
poi = mongodb.poi

#opening file
poi_file_home = "db_od_jana/"
poi_to_category_mapping = {
    "chata":"chaty.gpx",
    "utulna":"budy.gpx",
    "pristresok":"sennik.gpx",
    "pramen":"pramene.gpx",
    "pristresok":"posed.gpx"
}
#
# file = open((poi_file_home+poi_to_category_mapping['pristresok']),"r")
# file = file.read()


# <gpx>
# <wpt lat="49.181306" lon="19.049389">
# 	<ele>1423.00</ele>
# 	<time>2016-10-20T14:22:26.619Z</time>
# 	<name>Chata pod Chlebom</name>
# 	<desc><![CDATA[15.01.2007
# Popis
#
# společná noclehárna
# elektrická přípojka
# teplá voda
# občerstvení
# Najvyššie položená chata v Malej Fatre. Prvé zmienky o Chate pod Chlebom sú známe z obdobia zo začiatku druhej svetovej vojny. Žiaľ existencia tejto chaty podobne ako väčšiny ostatných v tomto období nemala dlhé trvanie, v roku 1945 bola vypálená ustupujúcimi nemeckými vojakmi. Neskôr bola postavená veľká chata pre 60-70 osôb. Z tejto éry pochádzajú aj dva lyžiarske vleky v blízkom okolí oba sú už desať rokov nefunkčné. I túto veľkú chatu postihol najväčší nepriateľ horských chát požiar. V roku 1982 do tla vyhorela, podarilo sa akurát uhasiť spojovací tunel s hospodárskou budovou. Z tejto hospodárskej budovy (skladov) vznikla dnešná Chalúpka pod Chlebom.
#
# Nejvhodnější doba návštěvy
# Chata funguje celoročne.]]></desc>
# 	<link href="./chaty-attachments/37_obr_2.jpg" />
# </wpt>

o = untangle.parse(poi_file_home+poi_to_category_mapping['chata'])

for wpt in o.gpx.wpt:
    print wpt.name


"""
if file:
    filename = "name from XML"
else:
    filename = 'None'

miesto_mongo = {
    'accuracy': 0,
    'category': request.form['category'],
    'name': request.form['name'],
    'img_url': filename,
    # 'user_id': int(g.user.id),
    'created': datetime.now(),
    'text': request.form['text']
}

miesto_mongo['coordinates'] = (float(request.form['lon']), float(request.form['lat']))

print("LOG poi json object has been created: \n %s" %miesto)
try:
    print("LOG inserting into mongoDB will start")
    poi.insert_one(miesto)
    print("LOG inserting into mongoDB done")
except:
    print("ERROR error saving miesto to mongoDB")
    """