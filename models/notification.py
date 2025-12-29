from datetime import datetime
from extensions import db

class Notification(db.Model):
    """
    =================================================
    BẢNG THÔNG BÁO
    Gửi thông báo đến thành viên
    =================================================
    """

    __tablename__ = "notifications"

    # ===============================
    # KHÓA CHÍNH
    # ===============================
    id = db.Column(db.Integer, primary_key=True)

    # ===============================
    # NỘI DUNG
    # ===============================
    tieu_de = db.Column(db.String(255), nullable=False)
    noi_dung = db.Column(db.Text, nullable=False)

    # ===============================
    # NGƯỜI GỬI
    # ===============================
    nguoi_gui_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # ===============================
    # THỜI GIAN
    # ===============================
    thoi_gian_gui = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ===============================
    # QUAN HỆ
    # ===============================
    nguoi_gui = db.relationship(
        "User",
        backref=db.backref("thong_bao_da_gui", lazy=True)
    )

    # ===============================
    # TIỆN ÍCH
    # ===============================
    def __repr__(self):
        return f"<ThongBao {self.tieu_de}>"

