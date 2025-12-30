from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user
from config import Config

# =====================================================
# BẮT BUỘC ĐĂNG NHẬP + KIỂM TRA TRẠNG THÁI THÀNH VIÊN
# =====================================================
def dang_nhap_va_hoat_dong(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Chưa đăng nhập
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

        # Chỉ kiểm tra với THÀNH VIÊN
        if current_user.quyen == Config.QUYEN_THANH_VIEN:
            # Chưa được duyệt
            if not current_user.da_duyet:
                flash("Tài khoản của bạn chưa được Ban điều hành duyệt.", "warning")
                return redirect(url_for("index"))

            # Trạng thái không còn hoạt động
            if not current_user.thanh_vien or \
               current_user.thanh_vien.trang_thai != Config.TRANG_THAI_HOAT_DONG:
                flash("Tài khoản của bạn hiện không còn hoạt động.", "danger")
                return redirect(url_for("index"))

        return func(*args, **kwargs)
    return wrapper


# =====================================================
# KIỂM TRA QUYỀN HỆ THỐNG
# =====================================================
def yeu_cau_quyen(ma_quyen):
    """
    ma_quyen: chuỗi quyền, ví dụ:
    - quan_ly_tai_khoan
    - duyet_thanh_vien
    - quan_ly_quy
    - xuat_bao_cao
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Chưa đăng nhập
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))

            # ==========================
            # ADMIN – TOÀN QUYỀN
            # ==========================
            if current_user.quyen == Config.QUYEN_ADMIN:
                # CẤM admin xem / đổi mật khẩu người khác
                if ma_quyen in ["xem_mat_khau", "doi_mat_khau_nguoi_khac"]:
                    abort(403)
                return func(*args, **kwargs)

            # ==========================
            # CÁC QUYỀN KHÁC
            # ==========================
            if not current_user.co_quyen(ma_quyen):
                flash("Bạn không có quyền thực hiện chức năng này.", "danger")
                abort(403)

            return func(*args, **kwargs)
        return wrapper
    return decorator
