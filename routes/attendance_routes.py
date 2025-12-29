# routes/attendance_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from datetime import date, datetime
from extensions import db
from models.attendance import Attendance
from models.member import Member

attendance_bp = Blueprint("attendance", __name__)


# =================================================
# KIỂM TRA QUYỀN VÀO ĐIỂM DANH
# =================================================
def co_quyen_diem_danh():
    if current_user.la_thu_quy():
        abort(403)


def co_quyen_chinh_sua():
    return current_user.la_admin() or current_user.la_bdh()


# =================================================
# BẢNG ĐIỂM DANH (NGANG)
# =================================================
@attendance_bp.route("/")
@login_required
def bang_diem_danh():
    co_quyen_diem_danh()

    # ngày đang xem (mặc định hôm nay)
    ngay_str = request.args.get("ngay")
    if ngay_str:
        ngay = datetime.strptime(ngay_str, "%Y-%m-%d").date()
    else:
        ngay = date.today()

    members = Member.query.filter_by(trang_thai="hoat_dong").all()

    # map attendance: member_id -> Attendance
    attendance_map = {
        a.thanh_vien_id: a
        for a in Attendance.query.filter_by(ngay=ngay).all()
    }

    total_members = Member.query.count()
    present_today = Attendance.query.filter_by(ngay=ngay, co_mat=True).count()
    absent_today = total_members - present_today
    attendance_rate = 0
    if total_members:
        attendance_rate = round((present_today / total_members) * 100, 1)

    return render_template(
        "attendance/attendance.html",
        members=members,
        attendance_map=attendance_map,
        ngay=ngay,
        co_quyen_chinh_sua=co_quyen_chinh_sua(),
        total_members=total_members,
        present_today=present_today,
        absent_today=absent_today,
        attendance_rate=attendance_rate
    )


# =================================================
# TICK / BỎ TICK ĐIỂM DANH
# =================================================
@attendance_bp.route("/toggle", methods=["POST"])
@login_required
def toggle_attendance():
    if not co_quyen_chinh_sua():
        abort(403)

    member_id = int(request.form.get("member_id"))
    ngay = datetime.strptime(request.form.get("ngay"), "%Y-%m-%d").date()

    attendance = Attendance.query.filter_by(
        thanh_vien_id=member_id,
        ngay=ngay
    ).first()

    if not attendance:
        attendance = Attendance(
            thanh_vien_id=member_id,
            ngay=ngay,
            co_mat=True
        )
        db.session.add(attendance)
    else:
        attendance.co_mat = not attendance.co_mat

    db.session.commit()
    return redirect(url_for("attendance.bang_diem_danh", ngay=ngay))


# =================================================
# LỊCH SỬ ĐIỂM DANH THEO THÀNH VIÊN
# =================================================
@attendance_bp.route("/member/<int:member_id>")
@login_required
def lich_su_diem_danh(member_id):
    co_quyen_diem_danh()

    member = Member.query.get_or_404(member_id)

    records = Attendance.query.filter_by(
        thanh_vien_id=member.id
    ).order_by(Attendance.ngay.desc()).all()

    return render_template(
        "attendance/attendance_history.html",
        member=member,
        records=records
    )


# =================================================
# XUẤT BÁO CÁO (PDF / EXCEL – CHỈ ADMIN / BDH)
# =================================================
@attendance_bp.route("/export")
@login_required
def export_attendance():
    if not co_quyen_chinh_sua():
        abort(403)

    # placeholder – sẽ xử lý export sau
    return "EXPORT ATTENDANCE (PDF / EXCEL)"
