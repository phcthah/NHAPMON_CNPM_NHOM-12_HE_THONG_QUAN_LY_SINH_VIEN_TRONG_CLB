from extensions import db


class Position(db.Model):
    """
    ===============================
    BẢNG CHỨC VỤ
    Ví dụ:
    - Chủ nhiệm
    - Phó chủ nhiệm
    - Ủy viên
    - Thành viên
    ===============================
    """

    __tablename__ = "positions"

    id = db.Column(db.Integer, primary_key=True)

    # Tên chức vụ (hiển thị tiếng Việt)
    ten_chuc_vu = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    # Mô tả vai trò (nếu cần)
    mo_ta = db.Column(db.String(255))

    def __repr__(self):
        return f"<ChucVu {self.ten_chuc_vu}>"
