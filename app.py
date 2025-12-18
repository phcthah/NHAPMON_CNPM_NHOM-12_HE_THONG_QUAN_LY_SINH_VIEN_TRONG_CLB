from flask import Flask, redirect, url_for
from extensions import db, login_manager
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Enable DB migrations (Flask-Migrate)
    try:
        from flask_migrate import Migrate
        Migrate(app, db)
    except Exception:
        # If Flask-Migrate isn't available, app still runs using SQLALchemy directly
        pass

    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.member_routes import member_bp
    from routes.team_routes import team_bp
    from routes.finance_routes import finance_bp
    from routes.attendance_routes import attendance_bp
    from routes.user_routes import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(member_bp, url_prefix='/members')
    app.register_blueprint(team_bp, url_prefix='/teams')
    app.register_blueprint(finance_bp, url_prefix='/finance')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    app.register_blueprint(users_bp, url_prefix='/users')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # Create DB and a default admin if none exists
    with app.app_context():
        db.create_all()
        try:
            from models.user import User
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(username='admin', is_admin=True)
                admin.set_password('admin')
                db.session.add(admin)
            else:
                if not admin.is_admin:
                    admin.is_admin = True
            db.session.commit()
        except Exception:
            db.session.rollback()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
