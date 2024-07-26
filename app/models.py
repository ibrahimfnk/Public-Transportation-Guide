from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config.Config')

mysql = MySQL(app)

def create_user(username, email, password):
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s)", (username, email, password))
    mysql.connection.commit()
    cur.close()

def verify_user(username, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username, ))
    user = cur.fetchone()
    cur.close()
    if user and password == user[3]:
        return True
    return False