from flask import Blueprint, render_template
from flask_login import login_required
from extensions import db
from models.member import Member
from models.user import User
from models.attendance import Attendance
from models.finance import Finance
from models.notification import Notification
from datetime import date

dashboard_bp = Blueprint("dashboard", __name__)
@dashboard_bp.route("/")
@login_required
def dashboard():
    # Tổng thành viên
    tong_thanh_vien = Member.query.count()

    # Thành viên đang hoạt động
    dang_hoat_dong = Member.query.filter_by(
        trang_thai="HOAT_DONG"
    ).count()

    # User chờ duyệt
    cho_duyet = User.query.filter_by(
        da_duyet=False
    ).count()

    # Tính số dư quỹ
    tong_thu = db.session.query(
        db.func.coalesce(db.func.sum(Finance.so_tien), 0)
    ).filter_by(loai="THU", da_xac_nhan=True).scalar()

    tong_chi = db.session.query(
        db.func.coalesce(db.func.sum(Finance.so_tien), 0)
    ).filter_by(loai="CHI").scalar()

    so_du_quy = tong_thu - tong_chi

    # Thông báo mới nhất
    thong_bao_moi = Notification.query.order_by(
        Notification.thoi_gian_gui.desc()
    ).limit(5).all()

    # Điểm danh hôm nay
    diem_danh_gan_nhat = Attendance.query.filter_by(
        ngay=date.today()
    ).limit(10).all()

    return render_template(
        "dashboard.html",
        tong_thanh_vien=tong_thanh_vien,
        dang_hoat_dong=dang_hoat_dong,
        cho_duyet=cho_duyet,
        so_du_quy=so_du_quy,
        thong_bao_moi=thong_bao_moi,
        diem_danh_gan_nhat=diem_danh_gan_nhat
    )
