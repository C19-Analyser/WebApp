from flask import Flask, render_template, request, redirect, flash, url_for
from mail import sendAlert
import model
import urllib.request
from app import app
from werkzeug.utils import secure_filename
from model import getPrediction,getModel
import os

import string
import random

import magic

import threading

import pytest

defaultUser = {'nom': 'NOM','prenom': 'PRENOM','mail': 'MAIL'}

@pytest.fixture
def app_context():
    with app.app_context():
        yield

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

class Envoi (threading.Thread):
    def __init__(self, subject,user=defaultUser,filename="FILENAME",result="RESULT",modelType="MODEL TYPE"):
        threading.Thread.__init__(self) 
        self.subject = subject
        self.user = user
        self.filename = filename
        self.result = result  
        self.modelType = modelType

    def run(self,app_context):
        sendAlert(self.subject,filename=self.filename,user=self.user,result=self.result,modelType=self.modelType)

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
                imageType = magic.from_file('uploads/COVID19460.jpg', mime=True)
                filename = get_random_string(3) + '_' + (filename.split('.',1))[0] + '.' + (imageType.split('/'))[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            
            model = getModel()
            print('model go')
            result = getPrediction(filename,model)
            print(result)

            if result == '1.0' :
                flash("Normal")
            elif result == '0.0':
                flash("Covid")
            else:
                flash("Undefined")

            flash(filename)

            print('mail before')

            envoi = Envoi('prediction',filename=filename)

            envoi.start()

            print('mail end')

            return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)