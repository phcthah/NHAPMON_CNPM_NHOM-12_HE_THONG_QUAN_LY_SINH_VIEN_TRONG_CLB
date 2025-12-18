from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from extensions import db
from models.attendance import Attendance
from models.member import Member
from datetime import date
from flask_login import login_required, current_user

attendance_bp = Blueprint('attendance', __name__, template_folder='../templates')


@attendance_bp.route('/')
@login_required
def list_attendance():
    today = date.today()
    members = Member.query.all()
    records = Attendance.query.filter_by(attended_date=today).all()
    present_ids = {r.member_id for r in records}
    return render_template('attendance.html', members=members, present_ids=present_ids, today=today)


@attendance_bp.route('/record', methods=['POST'])
@login_required
def record_attendance():
    today = date.today()
    # remove existing for today
    Attendance.query.filter_by(attended_date=today).delete()
    present = request.form.getlist('present')  # list of member ids
    for mid in present:
        a = Attendance(member_id=int(mid), attended_date=today, present=True)
        db.session.add(a)
    db.session.commit()
    flash('Điểm danh đã được cập nhật', 'success')
    return redirect(url_for('attendance.list_attendance'))


@attendance_bp.route('/history')
@login_required
def attendance_history():
    # list unique dates with counts
    rows = db.session.query(Attendance.attended_date, db.func.count(Attendance.id).label('present_count')).group_by(Attendance.attended_date).order_by(Attendance.attended_date.desc()).all()
    history = [{'date': r.attended_date, 'present_count': r.present_count} for r in rows]
    return render_template('attendance_history.html', history=history)


@attendance_bp.route('/view/<date_str>')
@login_required
def view_attendance(date_str):
    try:
        d = date.fromisoformat(date_str)
    except ValueError:
        flash('Ngày không hợp lệ', 'danger')
        return redirect(url_for('attendance.attendance_history'))
    members = Member.query.all()
    records = Attendance.query.filter_by(attended_date=d).all()
    present_ids = {r.member_id for r in records}
    return render_template('attendance_view.html', members=members, present_ids=present_ids, date=d)


@attendance_bp.route('/delete_date/<date_str>', methods=['POST'])
@login_required
def delete_attendance_date(date_str):
    if not getattr(current_user, 'is_admin', False):
        abort(403)
    try:
        d = date.fromisoformat(date_str)
    except ValueError:
        flash('Ngày không hợp lệ', 'danger')
        return redirect(url_for('attendance.attendance_history'))
    Attendance.query.filter_by(attended_date=d).delete()
    db.session.commit()
    flash('Đã xóa điểm danh cho ngày này', 'warning')
    return redirect(url_for('attendance.attendance_history'))