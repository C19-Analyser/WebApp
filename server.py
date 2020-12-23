from flask import Flask, render_template, request, redirect, flash, url_for
from mail import sendAlert
import model
import urllib.request
from app import app
from werkzeug.utils import secure_filename
from model import getPrediction,getModel
import os

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

            try:
                sendAlert('prediction')
            except:
                print("Mail sending error.")

            return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)