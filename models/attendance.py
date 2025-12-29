from extensions import db
from datetime import date

class Attendance(db.Model):
    """
    =================================================
    BẢNG ĐIỂM DANH
    Lưu trạng thái điểm danh theo:
    - Thành viên
    - Ngày điểm danh
    =================================================
    """

    __tablename__ = "attendances"

    # ===============================
    # KHÓA CHÍNH
    # ===============================
    id = db.Column(db.Integer, primary_key=True)

    # ===============================
    # LIÊN KẾT THÀNH VIÊN
    # ===============================
    thanh_vien_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=False
    )

    # ===============================
    # THỜI GIAN
    # ===============================
    ngay = db.Column(
        db.Date,
        default=date.today,
        nullable=False
    )

    # ===============================
    # TRẠNG THÁI ĐIỂM DANH
    # ===============================
    co_mat = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    # ===============================
    # GHI CHÚ (NẾU CÓ)
    # ===============================
    ghi_chu = db.Column(db.String(255))

    # ===============================
    # QUAN HỆ
    # ===============================
    thanh_vien = db.relationship(
        "Member",
        backref=db.backref("lich_su_diem_danh", lazy="dynamic")
    )

    # ===============================
    # RÀNG BUỘC
    # Mỗi thành viên chỉ có 1 bản ghi / ngày
    # ===============================
    __table_args__ = (
        db.UniqueConstraint(
            "thanh_vien_id",
            "ngay",
            name="uq_thanh_vien_ngay"
        ),
    )

    # ===============================
    # TIỆN ÍCH
    # ===============================
    def danh_dau_co_mat(self):
        self.co_mat = True

    def danh_dau_vang(self):
        self.co_mat = False

    def __repr__(self):
        return f"<Attendance ThanhVien={self.thanh_vien_id} Ngay={self.ngay} CoMat={self.co_mat}>"

