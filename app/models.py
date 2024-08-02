from flask import Flask, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object('config.Config')

mysql = MySQL(app)

def create_user(username, email, password):
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s)", (username, email, password))
    mysql.connection.commit()
    cur.close()

def verify_user(username, password):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username, ))
        user = cur.fetchone()
        if user and bcrypt.check_password_hash(user[3], password):
            session['id'] = user[0]
            return True
        else:
            return False

