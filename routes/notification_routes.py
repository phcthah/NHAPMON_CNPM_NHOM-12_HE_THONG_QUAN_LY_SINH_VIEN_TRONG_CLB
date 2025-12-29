# routes/notification_routes.py
from flask import Blueprint, render_template, redirect, url_for, abort, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from extensions import db
from models.notification import Notification
from models.notification_read import NotificationRead
from models.user import User
from config import Config

notification_bp = Blueprint("notification", __name__)


# =================================================
# TIỆN ÍCH PHÂN QUYỀN
# =================================================
def co_quyen_gui_thong_bao():
    return current_user.la_admin() or current_user.la_bdh()


# =================================================
# DANH SÁCH THÔNG BÁO (CÁ NHÂN)
# =================================================
@notification_bp.route("/")
@login_required
def danh_sach_thong_bao():
    thong_bao = (
        Notification.query
        .order_by(Notification.thoi_gian_gui.desc())
        .all()
    )

    da_doc_map = {
        r.notification_id: r
        for r in NotificationRead.query
        .filter_by(user_id=current_user.id)
        .all()
    }

    total_notifications = Notification.query.count()
    unread_notifications = Notification.query.count() - len(da_doc_map)

    from datetime import date
    sent_today = Notification.query.filter(
        Notification.thoi_gian_gui.between(
            datetime.combine(date.today(), datetime.min.time()),
            datetime.combine(date.today(), datetime.max.time())
        )
    ).count()

    readers_count = NotificationRead.query.count()

    return render_template(
        "notifications/list.html",
        thong_bao=thong_bao,
        da_doc_map=da_doc_map,
        total_notifications=total_notifications,
        unread_notifications=unread_notifications,
        sent_today=sent_today,
        readers_count=readers_count
    )


# =================================================
# ĐÁNH DẤU ĐÃ ĐỌC
# =================================================
@notification_bp.route("/<int:notification_id>/read", methods=["POST"])
@login_required
def danh_dau_da_doc(notification_id):
    notification = Notification.query.get_or_404(notification_id)

    doc = NotificationRead.query.filter_by(
        user_id=current_user.id,
        notification_id=notification.id
    ).first()

    if not doc:
        doc = NotificationRead(
            user_id=current_user.id,
            notification_id=notification.id
        )
        db.session.add(doc)

    doc.danh_dau_da_doc()
    db.session.commit()

    return redirect(url_for("notification.danh_sach_thong_bao"))


# =================================================
# ĐÁNH DẤU TẤT CẢ ĐÃ ĐỌC
# =================================================
@notification_bp.route("/read-all", methods=["POST"])
@login_required
def danh_dau_tat_ca_da_doc():
    thong_bao_ids = [
        tb.id for tb in Notification.query.all()
    ]

    da_doc_ids = {
        r.notification_id
        for r in NotificationRead.query
        .filter_by(user_id=current_user.id)
        .all()
    }

    for tb_id in thong_bao_ids:
        if tb_id not in da_doc_ids:
            db.session.add(NotificationRead(
                user_id=current_user.id,
                notification_id=tb_id,
                da_doc=True,
                thoi_diem_doc=datetime.utcnow()
            ))

    db.session.commit()
    return redirect(url_for("notification.danh_sach_thong_bao"))


# =================================================
# GỬI THÔNG BÁO
# =================================================
@notification_bp.route("/send", methods=["GET", "POST"])
@login_required
def gui_thong_bao():
    if not co_quyen_gui_thong_bao():
        abort(403)

    if request.method == "POST":
        tieu_de = request.form.get("tieu_de")
        noi_dung = request.form.get("noi_dung")

        if not tieu_de or not noi_dung:
            abort(400)

        thong_bao = Notification(
            tieu_de=tieu_de,
            noi_dung=noi_dung,
            nguoi_gui_id=current_user.id
        )

        db.session.add(thong_bao)
        db.session.commit()

        return redirect(url_for("notification.danh_sach_thong_bao"))

    return render_template("notifications/send.html")


# =================================================
# XEM AI ĐÃ ĐỌC (ADMIN / BDH)
# =================================================
@notification_bp.route("/<int:notification_id>/readers")
@login_required
def danh_sach_da_doc(notification_id):
    if not co_quyen_gui_thong_bao():
        abort(403)

    notification = Notification.query.get_or_404(notification_id)

    reads = (
        NotificationRead.query
        .filter_by(notification_id=notification.id)
        .join(User)
        .all()
    )

    return render_template(
        "notifications/readers.html",
        notification=notification,
        reads=reads
    )


# =================================================
# API: SỐ THÔNG BÁO CHƯA ĐỌC (CHUÔNG 🔔)
# =================================================
@notification_bp.route("/unread-count")
@login_required
def so_thong_bao_chua_doc():
    tong = Notification.query.count()

    da_doc = NotificationRead.query.filter_by(
        user_id=current_user.id,
        da_doc=True
    ).count()

    return jsonify({
        "unread": max(tong - da_doc, 0)
    })
