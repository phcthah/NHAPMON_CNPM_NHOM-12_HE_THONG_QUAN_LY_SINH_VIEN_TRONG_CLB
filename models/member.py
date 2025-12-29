from datetime import date
from extensions import db
from config import Config
class Member(db.Model):
    """
    Bảng THÀNH VIÊN
    Lưu thông tin chi tiết của người dùng trong CLB
    """

    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)

    # ===============================
    # LIÊN KẾT USER
    # ===============================
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    # ===============================
    # THÔNG TIN CÁ NHÂN
    # ===============================
    ho_ten = db.Column(db.String(150), nullable=False)
    ngay_sinh = db.Column(db.Date, nullable=False)

    khoa = db.Column(db.String(100))
    lop = db.Column(db.String(50))
    nganh = db.Column(db.String(100))

    ngay_vao_clb = db.Column(db.Date, default=date.today)

    # ===============================
    # BAN / CHỨC VỤ
    # ===============================
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    position_id = db.Column(db.Integer, db.ForeignKey("positions.id"))

    # ===============================
    # TRẠNG THÁI
    # ===============================
    trang_thai = db.Column(
        db.String(50),
        default=Config.TRANG_THAI_HOAT_DONG,
        nullable=False
    )

    # ===============================
    # QUAN HỆ
    # ===============================
    user = db.relationship(
        "User",
        back_populates="member",
        lazy=True
    )

    team = db.relationship(
        "Team",
        backref=db.backref("danh_sach_thanh_vien", lazy=True)
    )

    position = db.relationship(
        "Position",
        backref=db.backref("danh_sach_thanh_vien", lazy=True)
    )

    # ===============================
    # LOGIC
    # ===============================
    def dang_hoat_dong(self):
        return self.trang_thai == Config.TRANG_THAI_HOAT_DONG

    def la_cuu_thanh_vien(self):
        return self.trang_thai == Config.TRANG_THAI_CUU

    def ten_ban(self):
        return self.team.ten_ban if self.team else "Chưa có ban"

    def ten_chuc_vu(self):
        return self.position.ten_chuc_vu if self.position else "Chưa có chức vụ"

    def thong_tin_cong_khai(self):
        return {
            "ho_ten": self.ho_ten,
            "ngay_sinh": self.ngay_sinh,
            "khoa": self.khoa,
            "lop": self.lop,
            "nganh": self.nganh,
            "ban": self.ten_ban(),
            "chuc_vu": self.ten_chuc_vu(),
            "trang_thai": self.trang_thai,
        }

    def __repr__(self):
        return f"<Member {self.ho_ten}>"
