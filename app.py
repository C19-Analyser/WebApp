from flask import Flask

from flask_mail import Mail

app = Flask(__name__)

mail = Mail(app)

app.secret_key = "klIop44557xjdkzpsJJIx6y77"

# Config for upload file
app.config['UPLOAD_FOLDER'] = 'uploads'

# Config for mail system
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'c19.analyser@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
