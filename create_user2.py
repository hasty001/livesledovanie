import phpass
import mysql.connector
import os
import datetime
import hashlib
import phpass
import uuid
import passlib.hash


user = 'iiyhserk'
password = "p37ghkl9on9"

print user
print password

password_to_store = passlib.hash.phpass.encrypt(password)
print password_to_store
print passlib.hash.phpass.verify(password, password_to_store)


new_password_ok = phpass.PasswordHash()
new_password_ok = new_password_ok.check_password(pw=password, stored_hash=password_to_store)
print new_password_ok


db_con = mysql.connector.connect(host='mysql57.websupport.sk',
    database='26yghuzc',
    user='26yghuzc',
    password='nTsSKwubxa',
    port=3311)

cursor = db_con.cursor()
query = ("INSERT INTO `jos_users` (name, username, email, password, registerDate, lastvisitDate, params) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');"
         %(user, user, user, password_to_store, datetime.datetime.now(tz=None), datetime.datetime.now(tz=None), 'text'))

cursor.execute(query)

print cursor

cursor.close()
db_con.close()

