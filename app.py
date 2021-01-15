from flask import Flask

from flask_mail import Mail

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = "klIop44557xjdkzpsJJIx6y77" # Secrets

# Config for upload file
app.config['UPLOAD_FOLDER'] = 'uploads'

# Config for mail system
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'c19.analyser@gmail.com'
app.config['MAIL_PASSWORD'] = 'jovho1-cypguW-cuzmaz' # Secrets
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# db config 
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c19webApp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create mail intance
mail = Mail(app)

# Create db instance 
db = SQLAlchemy(app)

# login manager instance 
login_manager = LoginManager(app)