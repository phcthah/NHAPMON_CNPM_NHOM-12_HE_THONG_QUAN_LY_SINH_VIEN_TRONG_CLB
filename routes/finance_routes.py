# routes/finance_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from datetime import date
from extensions import db
from models.finance import Finance
from models.member import Member
from models.notification import Notification

finance_bp = Blueprint("finance", __name__)


# =================================================
# TIỆN ÍCH PHÂN QUYỀN
# =================================================
def co_quyen_quan_ly_quy():
    return current_user.la_admin() or current_user.la_thu_quy()


def co_quyen_xem_quy():
    return True  # tất cả đều được xem


def co_quyen_xac_nhan():
    return current_user.la_admin() or current_user.la_thu_quy()


# =================================================
# TRANG QUỸ (TỔNG HỢP)
# =================================================
@finance_bp.route("/")
@login_required
def trang_quy():
    if not co_quyen_xem_quy():
        abort(403)

    thu = Finance.query.filter_by(loai="THU").all()
    chi = Finance.query.filter_by(loai="CHI").all()

    tong_thu = sum(t.so_tien for t in thu if t.da_xac_nhan)
    tong_chi = sum(c.so_tien for c in chi)

    so_du = tong_thu - tong_chi

    pending_count = Finance.query.filter_by(loai="THU", da_xac_nhan=False).count()

    return render_template(
        "finance/finance.html",
        thu=thu,
        chi=chi,
        tong_thu=tong_thu,
        tong_chi=tong_chi,
        so_du=so_du,
        co_quyen_quan_ly=co_quyen_quan_ly_quy(),
        co_quyen_xac_nhan=co_quyen_xac_nhan(),
        pending_count=pending_count
    )


# =================================================
# THÊM KHOẢN THU (ADMIN / THỦ QUỸ)
# =================================================
@finance_bp.route("/thu/add", methods=["POST"])
@login_required
def them_thu():
    if not co_quyen_quan_ly_quy():
        abort(403)

    so_tien = int(request.form.get("so_tien"))
    ghi_chu = request.form.get("ghi_chu")
    member_id = request.form.get("member_id")

    # 1. Tạo bản ghi Finance
    finance = Finance(
        loai="THU",
        so_tien=so_tien,
        ghi_chu=ghi_chu,
        ngay=date.today(),
        member_id=member_id or None,
        da_xac_nhan=False
    )
    db.session.add(finance)

    # 2. Tạo thông báo hệ thống tự động
    ten_nguoi_nop = "vãng lai"
    if member_id:
        member = Member.query.get(member_id)
        if member:
            ten_nguoi_nop = member.ho_ten

    thong_bao = Notification(
        tieu_de="📣 Khoản thu mới chờ xác nhận",
        noi_dung=f"Có khoản thu mới: {so_tien:,} VNĐ từ {ten_nguoi_nop}. Nội dung: {ghi_chu}",
        nguoi_gui_id=current_user.id # Người tạo khoản thu là người gửi thông báo
    )
    db.session.add(thong_bao)
    db.session.commit()

    return redirect(url_for("finance.trang_quy"))


# =================================================
# THÀNH VIÊN UPLOAD ẢNH CHUYỂN KHOẢN
# =================================================
@finance_bp.route("/thu/<int:finance_id>/upload", methods=["POST"])
@login_required
def upload_anh_chuyen_khoan(finance_id):
    finance = Finance.query.get_or_404(finance_id)

    # chỉ cho upload nếu là khoản thu của chính mình
    if finance.member_id != current_user.member.id:
        abort(403)

    file = request.files.get("anh_chuyen_khoan")
    if file:
        path = f"uploads/finance/{finance_id}.png"
        file.save(path)
        finance.anh_chuyen_khoan = path
        db.session.commit()

    return redirect(url_for("finance.trang_quy"))


# =================================================
# XÁC NHẬN CHUYỂN KHOẢN
# =================================================
@finance_bp.route("/thu/<int:finance_id>/xac-nhan", methods=["POST"])
@login_required
def xac_nhan_thu(finance_id):
    if not co_quyen_xac_nhan():
        abort(403)

    finance = Finance.query.get_or_404(finance_id)
    finance.da_xac_nhan = not finance.da_xac_nhan

    db.session.commit()
    return redirect(url_for("finance.trang_quy"))


# =================================================
# THÊM KHOẢN CHI (ADMIN / THỦ QUỸ)
# =================================================
@finance_bp.route("/chi/add", methods=["POST"])
@login_required
def them_chi():
    if not co_quyen_quan_ly_quy():
        abort(403)

    finance = Finance(
        loai="CHI",
        so_tien=int(request.form.get("so_tien")),
        ghi_chu=request.form.get("ghi_chu"),
        ngay=date.today(),
        da_xac_nhan=True  # chi không cần xác nhận
    )

    db.session.add(finance)
    db.session.commit()
    return redirect(url_for("finance.trang_quy"))


# =================================================
# XOÁ GIAO DỊCH (ADMIN / THỦ QUỸ)
# =================================================
@finance_bp.route("/<int:finance_id>/delete", methods=["POST"])
@login_required
def xoa_giao_dich(finance_id):
    if not co_quyen_quan_ly_quy():
        abort(403)

    finance = Finance.query.get_or_404(finance_id)
    db.session.delete(finance)
    db.session.commit()

    return redirect(url_for("finance.trang_quy"))


# =================================================
# TỔNG KẾT THEO THÁNG / NĂM
# =================================================
@finance_bp.route("/summary")
@login_required
def tong_ket():
    if not co_quyen_quan_ly_quy():
        abort(403)

    year = int(request.args.get("year", date.today().year))

    thu = Finance.query.filter(
        Finance.loai == "THU",
        Finance.da_xac_nhan == True,
        Finance.ngay.between(date(year, 1, 1), date(year, 12, 31))
    ).all()

    chi = Finance.query.filter(
        Finance.loai == "CHI",
        Finance.ngay.between(date(year, 1, 1), date(year, 12, 31))
    ).all()

    return render_template(
        "finance/summary.html",
        thu=thu,
        chi=chi,
        year=year
    )


# =================================================
# EXPORT PDF / EXCEL (ADMIN / BDH / THỦ QUỸ)
# =================================================
@finance_bp.route("/export")
@login_required
def export_quy():
    if current_user.la_thanh_vien():
        abort(403)

    return "EXPORT QUỸ PDF / EXCEL"
@finance_bp.route("/thu")
@login_required
def danh_sach_thu():
    if not co_quyen_xem_quy():
        abort(403)

    thu = Finance.query.filter_by(loai="THU").all()
    return render_template(
        "finance/thu.html",
        thu=thu,
        co_quyen_quan_ly=co_quyen_quan_ly_quy(),
        co_quyen_xac_nhan=co_quyen_xac_nhan()
    )
@finance_bp.route("/chi")
@login_required
def danh_sach_chi():
    if not co_quyen_quan_ly_quy():
        abort(403)

    chi = Finance.query.filter_by(loai="CHI").all()
    return render_template(
        "finance/chi.html",
        chi=chi
    )
@finance_bp.route("/<int:finance_id>/edit", methods=["GET", "POST"])
@login_required
def edit_finance(finance_id):
    if not co_quyen_quan_ly_quy():
        abort(403)

    finance = Finance.query.get_or_404(finance_id)

    if request.method == "POST":
        finance.so_tien = int(request.form.get("so_tien"))
        finance.ghi_chu = request.form.get("ghi_chu")
        db.session.commit()
        return redirect(url_for("finance.trang_quy"))

    return render_template(
        "finance/finance_edit.html",
        finance=finance
    )

