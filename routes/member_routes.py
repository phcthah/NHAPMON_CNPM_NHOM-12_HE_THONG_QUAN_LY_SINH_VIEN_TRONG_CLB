# routes/member_routes.py
from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
from models.member import Member
from models.user import User
from models.team import Team
from models.notification import Notification
from models.position import Position
from config import Config
from werkzeug.security import generate_password_hash

member_bp = Blueprint("member", __name__)


# =================================================
# KIỂM TRA QUYỀN XEM THÀNH VIÊN
# =================================================
def co_quyen_xem_thanh_vien():
    if current_user.la_thu_quy():
        abort(403)


# =================================================
# DANH SÁCH THÀNH VIÊN (CHIA THEO BAN)
# =================================================
@member_bp.route("/")
@login_required
def danh_sach_thanh_vien():
    co_quyen_xem_thanh_vien()

    keyword = request.args.get("q", "").strip()

    query = Member.query
    if keyword:
        query = query.filter(Member.ho_ten.ilike(f"%{keyword}%"))

    members = query.all()
    teams = Team.query.all()

    total_members = Member.query.count()
    active_members = Member.query.filter_by(trang_thai="hoat_dong").count()
    pending_members = User.query.filter_by(da_duyet=False).count()
    teams_count = Team.query.count()

    return render_template(
        "members/members.html",
        members=members,
        teams=teams,
        keyword=keyword,
        total_members=total_members,
        active_members=active_members,
        pending_members=pending_members,
        teams_count=teams_count
    )


# =================================================
# XEM CHI TIẾT THÀNH VIÊN
# =================================================
@member_bp.route("/<int:member_id>")
@login_required
def chi_tiet_thanh_vien(member_id):
    co_quyen_xem_thanh_vien()

    member = Member.query.get_or_404(member_id)
    user = member.user

    # ===============================
    # THÀNH VIÊN XEM NGƯỜI KHÁC → GIỚI HẠN
    # ===============================
    if current_user.la_thanh_vien() and current_user.id != user.id:
        # Thành viên không xem được email / sđt của người khác — che đi bằng template
        return render_template(
            "members/member_detail.html",
            member=member,
            che_do="gioi_han"
        )

    # ===============================
    # ADMIN / BDH hoặc xem CHÍNH MÌNH
    # ===============================
    return render_template(
        "members/member_detail.html",
        member=member,
        che_do="day_du"
    )


# =================================================
# FORM CHỈNH SỬA THÀNH VIÊN (ADMIN / BDH)
# =================================================
@member_bp.route("/<int:member_id>/edit")
@login_required
def sua_thanh_vien(member_id):
    # Cho phép admin/BDH hoặc chính chủ (owner) chỉnh sửa
    if not (current_user.la_admin() or current_user.la_bdh() or (current_user.member and current_user.member.id == member_id)):
        abort(403)

    member = Member.query.get_or_404(member_id)
    teams = Team.query.all()
    positions = Position.query.all()

    return render_template(
        "members/member_edit.html",
        member=member,
        teams=teams,
        positions=positions
    )


# =================================================
# CẬP NHẬT THÀNH VIÊN (ADMIN / BDH)
# =================================================
@member_bp.route("/<int:member_id>/update", methods=["POST"])
@login_required
def cap_nhat_thanh_vien(member_id):
    member = Member.query.get_or_404(member_id)

    # Admin/BDH có thể cập nhật cả team/position/trang_thai và thông tin cá nhân
    if current_user.la_admin() or current_user.la_bdh():
        member.team_id = request.form.get("team_id") or None
        member.position_id = request.form.get("position_id") or None
        member.trang_thai = request.form.get("trang_thai")

    # Chủ tài khoản (owner) hoặc admin có thể cập nhật thông tin cá nhân
    if current_user.member and current_user.member.id == member_id or current_user.la_admin() or current_user.la_bdh():
        member.ho_ten = request.form.get("ho_ten") or member.ho_ten
        ngay_sinh_str = request.form.get("ngay_sinh")
        if ngay_sinh_str:
            from datetime import date
            try:
                member.ngay_sinh = date.fromisoformat(ngay_sinh_str)
            except Exception:
                pass
        member.khoa = request.form.get("khoa")
        member.lop = request.form.get("lop")
        member.nganh = request.form.get("nganh")
    else:
        # Không có quyền cập nhật
        abort(403)

    from extensions import db
    db.session.commit()

    return render_template(
        "members/member_detail.html",
        member=member,
        che_do="day_du",
        thong_bao="Cập nhật thành công"
    )

@member_bp.route("/add", methods=["GET", "POST"])
@login_required
def them_thanh_vien():
    if not (current_user.la_admin() or current_user.la_bdh()):
        abort(403)

    if request.method == "POST":
        # Lấy thông tin tài khoản (Dùng cho User)
        email = request.form.get("email")
        password = request.form.get("password")
        so_dien_thoai = request.form.get("so_dien_thoai")

        # Lấy thông tin cá nhân (Dùng cho Member)
        ho_ten = request.form.get("ho_ten")
        ngay_sinh_str = request.form.get("ngay_sinh")
        team_id = request.form.get("team_id") or None
        position_id = request.form.get("position_id") or None
        khoa = request.form.get("khoa")
        lop = request.form.get("lop")
        nganh = request.form.get("nganh")

        from extensions import db
        from datetime import date, datetime

        # 1. Kiểm tra sdt, email tồn tại chưa
        user_ton_tai = User.query.filter((User.email == email) | (User.so_dien_thoai == so_dien_thoai)).first()
        if user_ton_tai:
            return "Sdt hoặc Email này đã được sử dụng!", 400

        try:
            # 2. Tạo User trước
            new_user = User(
                email=email,
                mat_khau=generate_password_hash(password),
                so_dien_thoai=so_dien_thoai,
            )
            db.session.add(new_user)
            db.session.flush()

            # 3. Tạo Member liên kết với User vừa tạo
            ngay_sinh = date.fromisoformat(ngay_sinh_str) if ngay_sinh_str else None

            new_member = Member(
                user_id=new_user.id,
                ho_ten=ho_ten,
                ngay_sinh=ngay_sinh,
                team_id=team_id,
                position_id=position_id,
                khoa=khoa,
                lop=lop,
                nganh=nganh,
                trang_thai=Config.TRANG_THAI_HOAT_DONG
            )
            db.session.add(new_member)

            ten_ban = "thành viên mới"
            if team_id:
                t = Team.query.get(team_id)
                if t: ten_ban = f"thành viên Ban {t.ten_ban}"

            welcome_notif = Notification(
                tieu_de="✨ Chào mừng thành viên mới",
                noi_dung=f"Hệ thống vừa chào đón {ho_ten} gia nhập với vai trò {ten_ban}.",
                nguoi_gui_id=current_user.id,
                thoi_gian_gui=datetime.utcnow()
            )
            db.session.add(welcome_notif)

            db.session.commit() # Lưu cả hai vào Database

            return render_template(
                "members/member_detail.html",
                member=new_member,
                che_do="day_du",
                thong_bao="Thành viên và Tài khoản đã được tạo!"
            )
        except Exception as e:
            db.session.rollback() # Xóa dữ liệu tạm nếu lỗi
            return f"Lỗi hệ thống: {str(e)}", 500

    teams = Team.query.all()
    positions = Position.query.all()
    return render_template("members/member_add.html", teams=teams, positions=positions)