# routes/admin_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from models.member import Member
from models.team import Team
from models.position import Position
from models.permission import Permission
from config import Config

admin_bp = Blueprint("admin", __name__)


# =================================================
# DECORATOR: CHỈ ADMIN
# =================================================
def admin_required():
    if not current_user.is_authenticated or not current_user.la_admin():
        abort(403)


# =================================================
# DASHBOARD ADMIN
# =================================================
@admin_bp.route("/")
@login_required
def dashboard():
    admin_required()

    from datetime import date
    from models.finance import Finance
    from models.attendance import Attendance

    tong_thanh_vien = Member.query.count()
    thanh_vien_hoat_dong = Member.query.filter_by(trang_thai="hoat_dong").count()

    thu = Finance.query.filter_by(loai="THU", da_xac_nhan=True).all()
    chi = Finance.query.filter_by(loai="CHI").all()
    so_du_quy = sum(t.so_tien for t in thu) - sum(c.so_tien for c in chi)

    so_luot_diem_danh = Attendance.query.filter_by(ngay=date.today(), co_mat=True).count()

    return render_template(
        "dashboard.html",
        tong_thanh_vien=tong_thanh_vien,
        thanh_vien_hoat_dong=thanh_vien_hoat_dong,
        so_du_quy=so_du_quy,
        so_luot_diem_danh=so_luot_diem_danh
    )


# =================================================
# DUYỆT THÀNH VIÊN ĐĂNG KÝ
# =================================================
@admin_bp.route("/pending-members")
@login_required
def pending_members():
    admin_required()
    users = User.query.filter_by(da_duyet=False).all()
    return render_template("members/pending_members.html", users=users)


@admin_bp.route("/approve-member/<int:user_id>", methods=["POST"])
@login_required
def approve_member(user_id):
    admin_required()
    user = User.query.get_or_404(user_id)

    user.da_duyet = True
    db.session.commit()

    flash("Đã duyệt thành viên", "success")
    return redirect(url_for("admin.pending_members"))


# =================================================
# QUẢN LÝ TÀI KHOẢN + CẤP ROLE
# =================================================
@admin_bp.route("/users")
@login_required
def manage_users():
    admin_required()
    users = User.query.all()
    return render_template("admin/users.html", users=users)


@admin_bp.route("/users/<int:user_id>/set-role", methods=["POST"])
@login_required
def set_role(user_id):
    admin_required()
    user = User.query.get_or_404(user_id)

    quyen = request.form.get("quyen")
    if quyen not in Permission.quyen_theo_vai_tro():
        flash("Quyền không hợp lệ", "danger")
        return redirect(url_for("admin.manage_users"))

    user.quyen = quyen
    db.session.commit()

    flash("Cập nhật quyền thành công", "success")
    return redirect(url_for("admin.manage_users"))


# =================================================
# QUẢN LÝ THÀNH VIÊN (MEMBER)
# =================================================
@admin_bp.route("/members")
@login_required
def manage_members():
    admin_required()
    members = Member.query.all()
    teams = Team.query.all()
    positions = Position.query.all()

    return render_template(
        "members/members.html",
        members=members,
        teams=teams,
        positions=positions
    )


@admin_bp.route("/members/<int:member_id>/update", methods=["POST"])
@login_required
def update_member(member_id):
    admin_required()
    member = Member.query.get_or_404(member_id)

    member.team_id = request.form.get("team_id") or None
    member.position_id = request.form.get("position_id") or None
    member.trang_thai = request.form.get("trang_thai")

    db.session.commit()
    flash("Cập nhật thành viên thành công", "success")
    return redirect(url_for("admin.manage_members"))


@admin_bp.route("/members/<int:member_id>/delete", methods=["POST"])
@login_required
def delete_member(member_id):
    admin_required()
    member = Member.query.get_or_404(member_id)

    db.session.delete(member.user)
    db.session.delete(member)
    db.session.commit()

    flash("Đã xoá thành viên", "success")
    return redirect(url_for("admin.manage_members"))


# =================================================
# QUẢN LÝ BAN / TIỂU BAN
# =================================================
@admin_bp.route("/teams", methods=["GET", "POST"])
@login_required
def manage_teams():
    admin_required()

    if request.method == "POST":
        ten_ban = request.form.get("ten_ban")
        mo_ta = request.form.get("mo_ta")

        if Team.query.filter_by(ten_ban=ten_ban).first():
            flash("Ban đã tồn tại", "danger")
            return redirect(url_for("admin.manage_teams"))

        db.session.add(Team(ten_ban=ten_ban, mo_ta=mo_ta))
        db.session.commit()
        flash("Thêm ban thành công", "success")

    teams = Team.query.all()
    return render_template("teams/teams.html", teams=teams)


@admin_bp.route("/teams/<int:team_id>/delete", methods=["POST"])
@login_required
def delete_team(team_id):
    admin_required()
    team = Team.query.get_or_404(team_id)

    db.session.delete(team)
    db.session.commit()

    flash("Đã xoá ban", "success")
    return redirect(url_for("admin.manage_teams"))


# =================================================
# QUẢN LÝ CHỨC VỤ
# =================================================
@admin_bp.route("/positions", methods=["GET", "POST"])
@login_required
def manage_positions():
    admin_required()

    if request.method == "POST":
        ten = request.form.get("ten_chuc_vu")
        mo_ta = request.form.get("mo_ta")

        if Position.query.filter_by(ten_chuc_vu=ten).first():
            flash("Chức vụ đã tồn tại", "danger")
            return redirect(url_for("admin.manage_positions"))

        db.session.add(Position(ten_chuc_vu=ten, mo_ta=mo_ta))
        db.session.commit()
        flash("Thêm chức vụ thành công", "success")

    positions = Position.query.all()
    return render_template("admin/positions.html", positions=positions)
