import os
import MySQLdb
from datetime import datetime, timedelta
import smtplib
from email.MIMEText import MIMEText
import sys

db = MySQLdb.connect(host="mysql50.websupport.sk", # your host, usually localhost
                     port=3308,
                     user="nova_15182", # your username
                     passwd="StopSkurvencom1256", # your password
                     db="nova_15182") # name of the data base

cur = db.cursor()

#how old travels will be notified is distinguished by str(datetime.now() - timedelta(days=35))
cur.execute("SELECT user_id FROM details where start_date < '%s' and email = 0 and end_date = '0000-00-00 00:00:00';" % str(datetime.now() - timedelta(days=35))) 

userIDsToSendMail = list()
rows = cur.fetchall()

for row in rows:
    for col in row:
        userIDsToSendMail.append(col)
        
def getMail(id):
    cur.execute("SELECT email FROM jos_users where id = %s;" %id)
    mails = cur.fetchall()
    for mail in mails:
        for col in mail:
            mail = col
    return mail

def sendM(userIds):
    for id in userIds:
        fp = open(os.environ['OPENSHIFT_REPO_DIR'] + '/jobs/mail.txt', 'rb')
        msg = MIMEText(fp.read())
        fp.close()
        fromAdd = "info@cestasnp.sk"
        toAdd = getMail(id) # vrati email uzivatela kam poslat upozornenie
        bcc = ['info@cestasnp.sk']
        msg['Subject'] = 'LIVE sledovanie: upozornenie'
        msg['From'] = fromAdd
        msg['To'] = toAdd
        
        server = smtplib.SMTP('smtp.cestasnp.sk', 25)
        #server.set_debuglevel(1)
        #server.ehlo()
        server.starttls()
        server.login('info@cestasnp.sk', 'sedlo1256')        
        try:
            print 'idem poslat mail'    
            toAdd = [toAdd] + bcc
            server.sendmail(fromAdd , toAdd, msg.as_string())
            server.quit()
            print 'poslane na email: %s' %toAdd
            cur.execute("UPDATE `nova_15182`.`details` SET `email` = '1' WHERE `details`.`user_id` = %s;" %id)
        except Exception, exc:
            sys.exit( "mail failed; %s" % str(exc) ) # give a error message        

sendM(userIDsToSendMail)
        
        