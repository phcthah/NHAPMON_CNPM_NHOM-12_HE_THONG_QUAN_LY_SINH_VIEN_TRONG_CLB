from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# ===============================
# DATABASE
# ===============================
db = SQLAlchemy()

# ===============================
# LOGIN MANAGER
# ===============================
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Vui lòng đăng nhập để tiếp tục"
login_manager.login_message_category = "warning"

# ===============================
# MIGRATE (nâng cấp DB)
# ===============================
migrate = Migrate()
