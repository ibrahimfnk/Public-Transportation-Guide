from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import MySQLdb.cursors
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Email
from models import create_user, verify_user

app = Flask(__name__)

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
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

        create_user(username, email, hashed_password)

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if verify_user(username, password):
            return redirect(url_for("dashboard"))
        else:
            flash("Login Failed! Please check Username and Password")
            return redirect(url_for("login"))
        
    return render_template('login.html', form=form)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard():
    if 'id' in session:
        id = session['id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id=%s ", (id, ))
        user = cur.fetchone()
        cur.close()

        if user:
            return render_template('dashboard.html', user = user)

    return redirect('login')


if __name__ == '__main__':
    app.run(debug=True)