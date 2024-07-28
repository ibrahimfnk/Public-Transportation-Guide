from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import MySQLdb.cursors
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

app = Flask(__name__)

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


app.config.from_object('config.Config')

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route("/")
@app.route("/home")
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html')
    

@app.route("/register", methods=['GET', 'POST'])
def register():
    form  = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Store into database

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",(username, email, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)