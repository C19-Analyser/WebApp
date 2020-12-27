from flask import Flask, render_template, request, redirect, flash, url_for, session
from mail import send_async
import model
import urllib.request
from app import app,db,login_manager
from werkzeug.utils import secure_filename
from model import getPrediction,getModel
import os

from sqlalchemy.exc import SQLAlchemyError

from flask_login import current_user, login_user

from dbmanager import User

from forms import SigninForm

import string
import random

import magic

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file folder')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename) # Security essential !!
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],filename)):
                imageType = magic.from_file('uploads/' + filename, mime=True)
                filename = get_random_string(3) + '_' + (filename.split('.',1))[0] + '.' + (imageType.split('/'))[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            
            model = getModel()
            result = getPrediction(filename,model)

            if result == '1.0' :
                flash("Normal")
            elif result == '0.0':
                flash("Covid")
            else:
                flash("Undefined")

            flash(filename)

            send_async('prediction',filename=filename)

            return redirect('/')

@app.route("/login",methods=['GET', 'POST'])
def login():
    form = SigninForm()

    if current_user.is_authenticated:
        return redirect('/admin')

    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()  
        
        if user and user.check_password(password=form.password.data):
            login_user(user)
            return redirect('/admin')
        else:
            flash('Invalid username/password combination')
        
        return redirect('/admin')
    
    return render_template(
        'login.html',
        form=form
    )

@app.route("/admin",methods=['GET'])
def getAdminBoard():
    return render_template('admin.html')


@app.route("/register")
def register():
    try:
        user = User(
                name="name name",
                email="mail@mail"
            )
        user.set_password("pass")
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
    return render_template("index.html")

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

if __name__ == "__main__":
    app.run(debug=True)