from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from extensions import db
from models.member import Member, PendingMember
from models.team import Team
from flask_login import login_required, current_user
import re

member_bp = Blueprint('members', __name__, template_folder='../templates')


@member_bp.route('/')
@login_required
def list_members():
    # show only approved members (Members are created by admin or via approval)
    members = Member.query.order_by(Member.id.desc()).all()
    teams = Team.query.all()
    return render_template('members.html', members=members, teams=teams)


@member_bp.route('/pending')
@login_required
def pending_members():
    if not getattr(current_user, 'is_admin', False):
        abort(403)
    pendings = PendingMember.query.order_by(PendingMember.created_at.desc()).all()
    return render_template('pending_members.html', pendings=pendings)


@member_bp.route('/pending/approve/<int:id>', methods=['POST'])
@login_required
def approve_pending(id):
    if not getattr(current_user, 'is_admin', False):
        abort(403)
    p = PendingMember.query.get_or_404(id)
    m = Member(name=p.name, email=p.email, team_id=p.team_id)
    db.session.add(m)
    # ensure delete by query to avoid potential session issues
    PendingMember.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Đã duyệt thành viên', 'success')
    return redirect(url_for('members.pending_members'))


@member_bp.route('/pending/delete/<int:id>', methods=['POST'])
@login_required
def delete_pending(id):
    if not getattr(current_user, 'is_admin', False):
        abort(403)
    p = PendingMember.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('Đã xóa đăng ký', 'warning')
    return redirect(url_for('members.pending_members'))


@member_bp.route('/add', methods=['POST'])
@login_required
def add_member():
    name = (request.form.get('name') or '').strip()
    email = (request.form.get('email') or '').strip() or None
    team_id = request.form.get('team_id') or None

    members = Member.query.all()
    teams = Team.query.all()
    form = {'name': name, 'email': email, 'team_id': team_id}
    errors = []

    if not name:
        errors.append('Tên là bắt buộc')

    if email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        errors.append('Email không hợp lệ')

    if team_id and not Team.query.get(team_id):
        errors.append('Nhóm không tồn tại')

    if errors:
        return render_template('members.html', members=members, teams=teams, form=form, errors=errors)

    m = Member(name=name, email=email, team_id=team_id)
    db.session.add(m)
    db.session.commit()
    flash('Thêm thành viên thành công', 'success')
    return redirect(url_for('members.list_members'))


@member_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_member(id):
    m = Member.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    flash('Xóa thành viên', 'warning')
    return redirect(url_for('members.list_members'))


@member_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_member(id):
    m = Member.query.get_or_404(id)
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip() or None
        team_id = request.form.get('team_id') or None

        form = {'name': name, 'email': email, 'team_id': team_id}
        errors = []

        if not name:
            errors.append('Tên là bắt buộc')

        if email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors.append('Email không hợp lệ')

        if team_id and not Team.query.get(team_id):
            errors.append('Nhóm không tồn tại')

        if errors:
            teams = Team.query.all()
            return render_template('member_edit.html', member=m, teams=teams, form=form, errors=errors)

        m.name = name
        m.email = email
        m.team_id = team_id
        db.session.commit()
        flash('Cập nhật thành viên', 'success')
        return redirect(url_for('members.list_members'))
    teams = Team.query.all()
    return render_template('member_edit.html', member=m, teams=teams)


@member_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    teams = Team.query.all()
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip() or None
        team_id = request.form.get('team_id') or None
        message = (request.form.get('message') or '').strip() or None

        form = {'name': name, 'email': email, 'team_id': team_id, 'message': message}
        errors = []

        if not name:
            errors.append('Tên là bắt buộc')
        if email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors.append('Email không hợp lệ')
        if team_id and not Team.query.get(team_id):
            errors.append('Nhóm không tồn tại')

        if errors:
            return render_template('signup.html', teams=teams, form=form, errors=errors)

        p = PendingMember(name=name, email=email, team_id=team_id, message=message)
        db.session.add(p)
        db.session.commit()
        flash('Đăng ký đã được gửi, vui lòng chờ duyệt', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', teams=teams)

