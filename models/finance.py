from extensions import db
from datetime import date


class Finance(db.Model):
    """
    ===============================
    BẢNG GIAO DỊCH QUỸ
    THU / CHI của CLB
    ===============================
    """
    __tablename__ = "finances"

    id = db.Column(db.Integer, primary_key=True)

    # ===============================
    # LOẠI GIAO DỊCH
    # ===============================
    # THU | CHI
    loai = db.Column(db.String(10), nullable=False)

    # ===============================
    # SỐ TIỀN
    # ===============================
    so_tien = db.Column(db.Integer, nullable=False)

    # ===============================
    # GHI CHÚ
    # ===============================
    ghi_chu = db.Column(db.Text)

    # ===============================
    # NGÀY GIAO DỊCH
    # ===============================
    ngay = db.Column(db.Date, default=date.today, nullable=False)

    # ===============================
    # THÀNH VIÊN NỘP QUỸ (CHỈ THU)
    # ===============================
    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=True
    )

    # ===============================
    # ẢNH CHUYỂN KHOẢN (CHỈ THU)
    # ===============================
    anh_chuyen_khoan = db.Column(db.String(255))

    # ===============================
    # XÁC NHẬN (THỦ QUỸ)
    # ===============================
    da_xac_nhan = db.Column(db.Boolean, default=False)

    # ===============================
    # QUAN HỆ
    # ===============================
    member = db.relationship(
        "Member",
        backref=db.backref("giao_dich_quy", lazy=True)
    )

    # ===============================
    # TIỆN ÍCH
    # ===============================
    def la_thu(self):
        return self.loai == "THU"

    def la_chi(self):
        return self.loai == "CHI"

    def __repr__(self):
        return f"<Finance {self.loai} - {self.so_tien}>"
