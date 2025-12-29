# routes/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user import User
from models.member import Member
from werkzeug.security import generate_password_hash
from config import Config
import random

auth_bp = Blueprint("auth", __name__)


# ===============================
# ĐĂNG NHẬP
# ===============================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Hỗ trợ cả tên trường tiếng Việt cũ và template hiện tại (identifier/password)
        tai_khoan = request.form.get("tai_khoan") or request.form.get("identifier")  # email hoặc sdt
        mat_khau = request.form.get("mat_khau") or request.form.get("password")
        user = User.query.filter(
            (User.email == tai_khoan) | (User.so_dien_thoai == tai_khoan)
        ).first()

        if not user or not user.kiem_tra_mat_khau(mat_khau):
            flash("Sai tài khoản hoặc mật khẩu", "danger")
            return redirect(url_for("auth.login"))


        login_user(user)
        flash("Đăng nhập thành công", "success")
        return redirect(url_for("index"))

    return render_template("auth/login.html")


# ===============================
# ĐĂNG KÝ THÀNH VIÊN
# ===============================
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        sdt = request.form.get("so_dien_thoai")

        if User.query.filter_by(email=email).first():
            flash("Email đã tồn tại", "danger")
            return redirect(url_for("auth.signup"))

        if User.query.filter_by(so_dien_thoai=sdt).first():
            flash("Số điện thoại đã tồn tại", "danger")
            return redirect(url_for("auth.signup"))

        user = User(
            email=email,
            so_dien_thoai=sdt,
            quyen=Config.QUYEN_THANH_VIEN,
            da_duyet=True
        )
        # Hỗ trợ cả tên trường cũ và template hiện tại (mat_khau / password)
        mat_khau = request.form.get("mat_khau") or request.form.get("password")
        if not mat_khau:
            flash("Mật khẩu không được để trống", "danger")
            return redirect(url_for("auth.signup"))

        user.dat_mat_khau(mat_khau)

        # Yêu cầu trường 'ho_ten' và 'ngay_sinh' nhập đầy đủ
        from datetime import date

        ho_ten = request.form.get("ho_ten")
        ngay_sinh_str = request.form.get("ngay_sinh")
        if not ho_ten or not ngay_sinh_str:
            flash("Vui lòng nhập họ tên và ngày sinh", "danger")
            return redirect(url_for("auth.signup"))

        try:
            ngay_sinh = date.fromisoformat(ngay_sinh_str)
        except Exception:
            flash("Ngày sinh không hợp lệ", "danger")
            return redirect(url_for("auth.signup"))

        member = Member(
            ho_ten=ho_ten,
            ngay_sinh=ngay_sinh,
            khoa=request.form.get("khoa"),
            lop=request.form.get("lop"),
            nganh=request.form.get("nganh"),
            ngay_vao_clb=request.form.get("ngay_vao_clb") or date.today(),
            trang_thai=Config.TRANG_THAI_HOAT_DONG,
            user=user
        )

        try:
            db.session.add(user)
            db.session.add(member)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Lỗi khi đăng ký: {e}", "danger")
            return redirect(url_for("auth.signup"))

        # Tự động đăng ký là đã được duyệt và tự login
        login_user(user)
        flash("Đăng ký thành công. Tài khoản đã kích hoạt và bạn đã được đăng nhập.", "success")
        return redirect(url_for("index"))

    return render_template("auth/signup.html")


# ===============================
# ĐĂNG XUẤT
# ===============================
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Đã đăng xuất", "info")
    return redirect(url_for("auth.login"))


# ===============================
# QUÊN MẬT KHẨU – GỬI MÃ
# ===============================
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email không tồn tại", "danger")
            return redirect(url_for("auth.forgot_password"))

        otp = str(random.randint(100000, 999999))
        session["otp"] = otp
        session["reset_user_id"] = user.id

        # 🔥 MOCK GỬI EMAIL
        print(f"[OTP RESET PASSWORD]: {otp}")

        flash("Mã xác nhận đã được gửi về email", "info")
        return redirect(url_for("auth.reset_password"))

    return render_template("auth/forgot_password.html")


# ===============================
# ĐẶT LẠI MẬT KHẨU
# ===============================
@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        otp = request.form.get("otp")
        mat_khau_moi = request.form.get("mat_khau")

        if otp != session.get("otp"):
            flash("Mã xác nhận không đúng", "danger")
            return redirect(url_for("auth.reset_password"))

        user = User.query.get(session.get("reset_user_id"))
        user.dat_mat_khau(mat_khau_moi)

        db.session.commit()
        session.clear()

        flash("Đổi mật khẩu thành công", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html")


# ===============================
# ĐỔI MẬT KHẨU CÁ NHÂN
# ===============================
@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old = request.form.get("mat_khau_cu")
        new = request.form.get("mat_khau_moi")

        if not current_user.kiem_tra_mat_khau(old):
            flash("Mật khẩu cũ không đúng", "danger")
            return redirect(url_for("auth.change_password"))

        current_user.dat_mat_khau(new)
        db.session.commit()

        flash("Đổi mật khẩu thành công", "success")
        return redirect(url_for("index"))

    return render_template("auth/change_password.html")
