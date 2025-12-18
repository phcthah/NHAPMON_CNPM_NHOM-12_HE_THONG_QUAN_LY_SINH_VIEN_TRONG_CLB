from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from extensions import db
from models.user import User
from flask_login import current_user, login_required
from functools import wraps

users_bp = Blueprint('users', __name__, template_folder='../templates')


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated


@users_bp.route('/')
@admin_required
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@users_bp.route('/add', methods=['POST'])
@admin_required
def add_user():
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = bool(request.form.get('is_admin'))
    if not username or not password:
        flash('Tên đăng nhập và mật khẩu là bắt buộc', 'danger')
        return redirect(url_for('users.list_users'))
    if User.query.filter_by(username=username).first():
        flash('Tên đăng nhập đã tồn tại', 'danger')
        return redirect(url_for('users.list_users'))
    u = User(username=username, is_admin=is_admin)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    flash('Người dùng đã được tạo', 'success')
    return redirect(url_for('users.list_users'))


@users_bp.route('/delete/<int:id>', methods=['POST'])
@admin_required
def delete_user(id):
    u = User.query.get_or_404(id)
    if u.id == current_user.id:
        flash('Bạn không thể xóa chính mình', 'warning')
        return redirect(url_for('users.list_users'))
    db.session.delete(u)
    db.session.commit()
    flash('Người dùng đã được xóa', 'warning')
    return redirect(url_for('users.list_users'))


@users_bp.route('/reset_password/<int:id>', methods=['POST'])
@admin_required
def reset_password(id):
    u = User.query.get_or_404(id)
    new_pw = request.form.get('new_password')
    if not new_pw:
        flash('Mật khẩu mới không được để trống', 'danger')
        return redirect(url_for('users.list_users'))
    u.set_password(new_pw)
    db.session.commit()
    flash('Mật khẩu đã được đặt lại', 'success')
    return redirect(url_for('users.list_users'))
