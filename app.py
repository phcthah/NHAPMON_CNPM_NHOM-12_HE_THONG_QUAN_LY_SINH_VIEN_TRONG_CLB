from flask import Flask, render_template
from config import Config
from extensions import db, login_manager, migrate

# ===============================
# IMPORT MODELS
# ===============================
from models.user import User
from models.member import Member
from models.permission import Permission
from models.attendance import Attendance
from models.finance import Finance

# ===============================
# IMPORT BLUEPRINTS (CHẶNG 2)
# ===============================
from routes.auth_routes import auth_bp
from routes.member_routes import member_bp
from routes.attendance_routes import attendance_bp
from routes.finance_routes import finance_bp
from routes.dashboard_routes import dashboard_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ===============================
    # INIT EXTENSIONS
    # ===============================
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # ===============================
    # REGISTER BLUEPRINTS
    # (CÁC CHỨC NĂNG ƯU TIÊN – CHẶNG 2)
    # ===============================
    app.register_blueprint(auth_bp)
    app.register_blueprint(member_bp, url_prefix="/members")
    app.register_blueprint(attendance_bp, url_prefix="/attendance")
    app.register_blueprint(finance_bp, url_prefix="/finance")
    app.register_blueprint(dashboard_bp)

    # ===============================
    # TRANG CHỦ
    # ===============================
    @app.route("/")
    def index():
        return render_template("dashboard.html")

    # ===============================
    # ERROR HANDLERS
    # ===============================
    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    # ===============================
    # KHỞI TẠO DATABASE & ADMIN MẶC ĐỊNH
    # (PHÙ HỢP FLASK 3.x)
    # ===============================
    with app.app_context():
        db.create_all()

        # Tạo danh sách quyền mặc định
        Permission.tao_quyen_mac_dinh()

        # Tạo tài khoản ADMIN mặc định
        admin = User.query.filter_by(email="admin@admin.com").first()
        if not admin:
            admin = User(
                email="admin@admin.com",
                so_dien_thoai="0000000000",
                quyen=Config.QUYEN_ADMIN,
                da_duyet=True
            )
            admin.dat_mat_khau("admin")
            db.session.add(admin)
            db.session.commit()

            print("✔ Đã tạo tài khoản ADMIN mặc định")

    return app


# ===============================
# CHẠY ỨNG DỤNG
# ===============================
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
