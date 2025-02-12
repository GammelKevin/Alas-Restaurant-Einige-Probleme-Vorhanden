from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Bitte melden Sie sich an, um auf den Admin-Bereich zuzugreifen.'
    login_manager.login_message_category = 'error'