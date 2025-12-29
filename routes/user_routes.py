from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from config import Config

user_bp = Blueprint("user", __name__)

# Kiểm tra quyền Admin hoặc Ban điều hành
def la_quan_ly():
    return current_user.la_admin() or current_user.la_bdh()

# --- DANH SÁCH TÀI KHOẢN ---
@user_bp.route("/")
@login_required
def danh_sach_user():
    if not la_quan_ly():
        abort(403)
    # Sắp xếp: Ưu tiên người chưa duyệt lên đầu (da_duyet=False)
    users = User.query.order_by(User.da_duyet.asc(), User.id.desc()).all()
    return render_template("users/users.html", users=users)

# --- DUYỆT NHANH (1-CLICK) ---
@user_bp.route("/approve/<int:user_id>", methods=["POST"])
@login_required
def approve_user(user_id):
    if not la_quan_ly():
        abort(403)
    user = User.query.get_or_404(user_id)
    user.da_duyet = True
    db.session.commit()
    flash(f"Đã duyệt tài khoản {user.email} thành công!", "success")
    return redirect(url_for("user.danh_sach_user"))

# --- THAY ĐỔI VAI TRÒ ---
@user_bp.route("/set-role/<int:user_id>", methods=["POST"])
@login_required
def set_role(user_id):
    if not current_user.la_admin():
        abort(403)
    user = User.query.get_or_404(user_id)
    new_role = request.form.get("role")
    
    if user.id == current_user.id:
        flash("Bạn không thể tự đổi quyền của chính mình!", "warning")
        return redirect(url_for("user.danh_sach_user"))

    valid_roles = [Config.QUYEN_ADMIN, Config.QUYEN_BDH, Config.QUYEN_THU_QUY, Config.QUYEN_THANH_VIEN]
    if new_role in valid_roles:
        user.quyen = new_role
        db.session.commit()
        flash(f"Đã cập nhật quyền thành {new_role}", "success")
    return redirect(url_for("user.danh_sach_user"))

# --- HỒ SƠ CÁ NHÂN (Endpoint sửa lỗi BuildError) ---
@user_bp.route("/profile")
@login_required
def profile():
    return render_template("users/profile.html", user=current_user)

# --- CHỈNH SỬA HỒ SƠ (Endpoint sửa lỗi BuildError) ---
@user_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        current_user.so_dien_thoai = request.form.get("so_dien_thoai")
        db.session.commit()
        flash("Cập nhật thông tin thành công!", "success")
        return redirect(url_for("user.profile"))
    return render_template("users/profile_edit.html", user=current_user)

# --- XÓA TÀI KHOẢN ---
@user_bp.route("/delete/<int:user_id>", methods=["POST"])
@login_required
def xoa_user(user_id):
    if not current_user.la_admin():
        abort(403)
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Không thể xóa tài khoản đang sử dụng!", "danger")
        return redirect(url_for("user.danh_sach_user"))

    if user.member:
        db.session.delete(user.member)
    db.session.delete(user)
    db.session.commit()
    flash("Đã xóa tài khoản vĩnh viễn.", "success")
    return redirect(url_for("user.danh_sach_user"))