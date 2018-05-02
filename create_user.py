import phpass
import mysql.connector

user1 = 'test'
password1 = "Testtest1"
hashed_password1 = "$P$BKHLCarEga65BH14TTJkvs3Fa8PovM/"

user2 = "test2"
password2 = "TestTest123"
hashed_password2 = "$P$BlkR5RoIuPvhiwPWiZWDJ3tfkHiP6R1"

db_con = mysql.connector.connect(
    user = 'k72ny9v0yxb0',
    password = 'gqnkzd22wzlk',
    host = 'mariadb101.websupport.sk',
    port = '3312',
    database = 'k72ny9v0yxb0'
)
cursor = db_con.cursor()
#query = ("SELECT user_login, user_pass FROM ippmgpusers WHERE user_login = '%s'")
#query = ("UPDATE ippmgpusers SET user_pass = 'test345678' WHERE ippmgpusers.ID = 1006")
query = ("SELECT id, user_login, user_pass, user_email FROM ippmgpusers WHERE 1")

cursor.execute(query)

print cursor

for abcd, user_login, user_pass, user_email in cursor:
    if user_login == user1:
        print user_pass
        heslo_db = user_pass
        email = user_email
        print abcd

cursor.close()
db_con.close()



wp_database = "k72ny9v0yxb0:gqnkzd22wzlk@mariadb101.websupport.sk:3312"



my_password = phpass.PasswordHash()
my_password = my_password.check_password(pw=password1, stored_hash=heslo_db)
print my_password