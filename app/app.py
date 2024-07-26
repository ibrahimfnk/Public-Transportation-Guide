from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import MySQLdb.cursors

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "flaskadmin"
app.config["MYSQL_PASSWORD"] = "publictransport"
app.config["MYSQL_DB"] = "public_transportation_guide"

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)