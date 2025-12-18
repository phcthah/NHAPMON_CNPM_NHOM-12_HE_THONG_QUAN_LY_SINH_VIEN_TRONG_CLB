from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db, login_manager
from models.user import User
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__, template_folder='../templates')


from urllib.parse import urlparse


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next') or request.form.get('next')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            # Redirect to next if it's a safe relative path
            if next_page and urlparse(next_page).netloc == '':
                return redirect(next_page)
            return redirect(url_for('members.list_members'))
        flash('Sai tên đăng nhập hoặc mật khẩu', 'danger')
    return render_template('login.html', next=next_page)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất', 'info')
    return redirect(url_for('auth.login'))



