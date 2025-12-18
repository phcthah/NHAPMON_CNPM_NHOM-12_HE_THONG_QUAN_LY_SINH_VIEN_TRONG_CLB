from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.team import Team
from flask_login import login_required

team_bp = Blueprint('teams', __name__, template_folder='../templates')


@team_bp.route('/')
@login_required
def list_teams():
    teams = Team.query.all()
    return render_template('teams.html', teams=teams)


@team_bp.route('/add', methods=['POST'])
@login_required
def add_team():
    name = (request.form.get('name') or '').strip()
    teams = Team.query.all()
    form = {'name': name}
    errors = []

    if not name:
        errors.append('Tên nhóm không được để trống')
    elif Team.query.filter_by(name=name).first():
        errors.append('Tên nhóm đã tồn tại')

    if errors:
        return render_template('teams.html', teams=teams, form=form, errors=errors)

    t = Team(name=name)
    db.session.add(t)
    db.session.commit()
    flash('Thêm nhóm thành công', 'success')
    return redirect(url_for('teams.list_teams'))


@team_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_team(id):
    t = Team.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    flash('Xóa nhóm', 'warning')
    return redirect(url_for('teams.list_teams'))


@team_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_team(id):
    t = Team.query.get_or_404(id)
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        form = {'name': name}
        errors = []
        if not name:
            errors.append('Tên nhóm không được để trống')
        elif Team.query.filter(Team.id != id, Team.name == name).first():
            errors.append('Tên nhóm đã tồn tại')
        if errors:
            return render_template('team_edit.html', team=t, form=form, errors=errors)
        t.name = name
        db.session.commit()
        flash('Cập nhật nhóm thành công', 'success')
        return redirect(url_for('teams.list_teams'))
    return render_template('team_edit.html', team=t)
