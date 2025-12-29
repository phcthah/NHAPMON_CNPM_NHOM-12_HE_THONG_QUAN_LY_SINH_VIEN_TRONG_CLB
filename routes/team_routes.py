# routes/team_routes.py
from flask import (
    Blueprint, render_template, redirect,
    url_for, request, abort
)
from flask_login import login_required, current_user
from extensions import db
from models.team import Team
from models.member import Member

team_bp = Blueprint("team", __name__)

# ===============================
# PHÂN QUYỀN
# ===============================
def co_quyen_tao():
    return current_user.la_admin() or current_user.la_bdh()


def co_quyen_sua():
    return current_user.la_admin() or current_user.la_bdh()


def co_quyen_xoa():
    return current_user.la_admin()

# =================================================
# DANH SÁCH BAN
# =================================================
@team_bp.route("/")
@login_required
def danh_sach_ban():
    teams = Team.query.order_by(Team.ten_ban.asc()).all()

    return render_template(
        "team/list.html",
        teams=teams
    )


# =================================================
# CHI TIẾT BAN + DANH SÁCH THÀNH VIÊN
# =================================================
@team_bp.route("/<int:team_id>")
@login_required
def chi_tiet_ban(team_id):
    team = Team.query.get_or_404(team_id)

    members = (
        Member.query
        .filter_by(team_id=team.id)
        .order_by(Member.ho_ten.asc())
        .all()
    )

    return render_template(
        "team/detail.html",
        team=team,
        members=members
    )


# =================================================
# TẠO BAN
# =================================================
@team_bp.route("/create", methods=["GET", "POST"])
@login_required
def tao_ban():
    if not co_quyen_tao():
        abort(403)

    if request.method == "POST":
        ten_ban = request.form.get("ten_ban")
        mo_ta = request.form.get("mo_ta")

        if not ten_ban:
            abort(400)

        # Kiểm tra trùng tên
        if Team.query.filter_by(ten_ban=ten_ban).first():
            abort(400)

        team = Team(
            ten_ban=ten_ban,
            mo_ta=mo_ta
        )

        db.session.add(team)
        db.session.commit()

        return redirect(url_for("team.danh_sach_ban"))

    return render_template("team/create.html")


# =================================================
# CHỈNH SỬA BAN
# =================================================
@team_bp.route("/<int:team_id>/edit", methods=["GET", "POST"])
@login_required
def sua_ban(team_id):
    if not co_quyen_sua():
        abort(403)

    team = Team.query.get_or_404(team_id)

    if request.method == "POST":
        ten_ban = request.form.get("ten_ban")
        mo_ta = request.form.get("mo_ta")

        if not ten_ban:
            abort(400)

        # Tránh trùng tên với ban khác
        exists = (
            Team.query
            .filter(Team.ten_ban == ten_ban, Team.id != team.id)
            .first()
        )
        if exists:
            abort(400)

        team.ten_ban = ten_ban
        team.mo_ta = mo_ta

        db.session.commit()
        return redirect(url_for("team.chi_tiet_ban", team_id=team.id))

    return render_template(
        "team/edit.html",
        team=team
    )


# =================================================
# XÓA BAN
# =================================================
@team_bp.route("/<int:team_id>/delete", methods=["POST"])
@login_required
def xoa_ban(team_id):
    if not co_quyen_xoa():
        abort(403)

    team = Team.query.get_or_404(team_id)

    # Gỡ ban khỏi thành viên trước khi xóa
    members = Member.query.filter_by(team_id=team.id).all()
    for member in members:
        member.team_id = None

    db.session.delete(team)
    db.session.commit()

    return redirect(url_for("team.danh_sach_ban"))
