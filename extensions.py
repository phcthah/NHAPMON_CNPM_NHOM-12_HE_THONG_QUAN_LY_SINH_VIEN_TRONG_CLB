from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Create instances here so models and app can import them without circular imports
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Vui lòng đăng nhập để tiếp tục.'
login_manager.login_message_category = 'warning'
