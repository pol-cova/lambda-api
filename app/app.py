from flask import Flask, render_template,url_for, redirect,request,jsonify,session,flash,send_file
from forms.forms import ContactForm
import pandas as pd
import sqlite3
import re
from werkzeug.security import generate_password_hash, check_password_hash
from io import BytesIO
from pytube import YouTube

app = Flask(__name__)
app.secret_key = 'G34+yhc[W#%zfnfp_KRpL#9&3?iKq^'

##### db Connection
def get_db_connection():
    conn = sqlite3.connect('./db/users.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db_connection()

@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username =session['username'])
    return redirect(url_for('login'))

@app.route('/sin',methods = ['GET','POST'])
def login():
    cur = conn.cursor()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)
        cur.execute('SELECT * FROM users WHERE username = ?', (username,))
        account = cur.fetchone()
        if account:
            password_rs = account['password']
            print(password_rs)
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
    return render_template('login.html')

@app.route('/sup',methods = ['GET','POST'])
def register():
    cur = conn.cursor()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    
        _hashed_password = generate_password_hash(password)
        #Check if account exists using MySQL
        cur.execute('SELECT * FROM users WHERE username = ?', (username,))
        account = cur.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            cur.execute("INSERT INTO users (fullname, username, password, email) VALUES (?,?,?,?)", (fullname, username, _hashed_password, email))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    return render_template('register.html')

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    cur = conn.cursor()
    if 'loggedin' in session:
        cur.execute('SELECT * FROM users WHERE id = ?', [session['id']])
        account = cur.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/contact', methods=['GET', 'POST'])
def get_contact():
    form = ContactForm()
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        res = pd.DataFrame({'name': name, 'email': email, 'subject': subject, 'message': message}, index=[0])
        res.to_csv('./contactusMessage.csv')
        return render_template('contact.html', form=form)
    else:
        return render_template('contact.html', form=form)

@app.route('/yt-api', methods=['GET', 'POST'])
def ytapi():
    return render_template('yt-api.html',
    data=[{'itag':'720p'},{'itag':'360p'}])

@app.route('/yt-api-down', methods=['GET', 'POST'])
def ytdownload():
    itag = request.form.get('comp_select')
    if request.method == 'POST':
        buffer = BytesIO()
        urlyt = request.form.get('url')
        yt = YouTube(urlyt)
        if itag =='720p':
            stream = yt.streams.get_by_itag(22)
            stream.stream_to_buffer(buffer)
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name="Video - {yt.title}.mp4", mimetype="video/mp4")
        elif itag =='360p':
            stream = yt.streams.get_by_itag(18)
            stream.stream_to_buffer(buffer)
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name="Video - {yt.title}.mp4", mimetype="video/mp4")
    return redirect(url_for('yt-api'))


if __name__ =='__main__':
    app.run(debug=True)