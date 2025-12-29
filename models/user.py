# models/user.py
from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

@login_manager.user_loader
def tai_nguoi_dung(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # ===============================
    # ĐĂNG NHẬP
    # ===============================
    email = db.Column(db.String(150), unique=True, nullable=False)
    so_dien_thoai = db.Column(db.String(20), unique=True, nullable=False)
    mat_khau = db.Column(db.String(255), nullable=False)

    # ===============================
    # PHÂN QUYỀN
    # ===============================
    quyen = db.Column(
        db.String(50),
        default=Config.QUYEN_THANH_VIEN,
        nullable=False
    )

    da_duyet = db.Column(db.Boolean, default=False)

    # ===============================
    # QUAN HỆ 1–1 VỚI MEMBER
    # ===============================
    member = db.relationship(
        "Member",
        back_populates="user",
        uselist=False
    )

    # ===============================
    # MẬT KHẨU
    # ===============================
    def dat_mat_khau(self, mat_khau):
        self.mat_khau = generate_password_hash(mat_khau)

    def kiem_tra_mat_khau(self, mat_khau):
        return check_password_hash(self.mat_khau, mat_khau)

    # ===============================
    # KIỂM TRA VAI TRÒ
    # ===============================
    def la_admin(self):
        return self.quyen == Config.QUYEN_ADMIN

    def la_bdh(self):
        return self.quyen == Config.QUYEN_BDH

    def la_thu_quy(self):
        return self.quyen == Config.QUYEN_THU_QUY

    def la_thanh_vien(self):
        return self.quyen == Config.QUYEN_THANH_VIEN

    # ===============================
    # KIỂM TRA QUYỀN
    # ===============================
    def co_quyen(self, ma_quyen):
        if self.la_admin():
            return True

        from models.permission import Permission
        quyen_map = Permission.quyen_theo_vai_tro()
        return ma_quyen in quyen_map.get(self.quyen, [])

    # ===============================
    # HIỂN THỊ
    # ===============================
    def ten_hien_thi(self):
        if self.member:
            return self.member.ho_ten
        return self.email
    def __repr__(self):
        return f"<User {self.email} – {self.quyen}>"
