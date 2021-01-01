from flask import Flask, render_template, request, redirect, flash, url_for, session
from mail import send_async
import model
import urllib.request
from app import app,db,login_manager
from werkzeug.utils import secure_filename
from model import getPrediction,getModel
import os

from sqlalchemy.exc import SQLAlchemyError

from flask_login import current_user, login_user, logout_user, login_required

from dbmanager import User

from forms import SigninForm, SignupForm

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

@app.route("/admin")
@login_required
def getAdminBoard():
    return render_template('admin.html')


@app.route("/register",methods=['GET', 'POST'])
@login_required
def register():
    
    form = SignupForm()
    
    try:
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user is None:
                user = User(
                    name=form.name.data,
                    email=form.email.data
                )
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                return redirect("/admin")
            else:
                flash('A user already exists with that email address.')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        flash('Database error.')

    return render_template(
        'register.html',
        form=form
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)