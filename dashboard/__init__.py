
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/first'
app.config['SECRET_KEY'] = '00929c5480c821a729d91a71'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "home_page"
login_manager.login_message_category = "info"
from dashboard import routes