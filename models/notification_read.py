from extensions import db
from datetime import datetime

class NotificationRead(db.Model):
    """
    =================================================
    BẢNG TRẠNG THÁI ĐỌC THÔNG BÁO
    Lưu việc người dùng đã đọc thông báo hay chưa
    =================================================
    """

    __tablename__ = "notification_reads"

    # ===============================
    # KHÓA CHÍNH
    # ===============================
    id = db.Column(db.Integer, primary_key=True)

    # ===============================
    # LIÊN KẾT NGƯỜI DÙNG
    # ===============================
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # ===============================
    # LIÊN KẾT THÔNG BÁO
    # ===============================
    notification_id = db.Column(
        db.Integer,
        db.ForeignKey("notifications.id"),
        nullable=False
    )

    # ===============================
    # TRẠNG THÁI
    # ===============================
    da_doc = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    # Thời điểm đọc thông báo
    thoi_diem_doc = db.Column(db.DateTime)

    # ===============================
    # QUAN HỆ
    # ===============================
    user = db.relationship(
        "User",
        backref=db.backref("thong_bao_da_doc", lazy="dynamic")
    )

    notification = db.relationship(
        "Notification",
        backref=db.backref("danh_sach_doc", lazy="dynamic")
    )

    # ===============================
    # TIỆN ÍCH
    # ===============================
    def danh_dau_da_doc(self):
        """Đánh dấu thông báo đã được đọc"""
        self.da_doc = True
        self.thoi_diem_doc = datetime.utcnow()

    def __repr__(self):
        return f"<NotificationRead user={self.user_id} notification={self.notification_id}>"
