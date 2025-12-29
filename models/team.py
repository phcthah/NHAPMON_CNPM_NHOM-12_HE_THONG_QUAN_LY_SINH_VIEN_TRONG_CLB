from extensions import db

class Team(db.Model):
    """
    ===============================
    BẢNG BAN / TIỂU BAN
    Lưu thông tin các ban trong CLB
    ===============================
    """
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)

    # Tên ban (ví dụ: Ban Truyền Thông, Ban Kỹ Thuật)
    ten_ban = db.Column(db.String(150), nullable=False, unique=True)

    # Mô tả chức năng của ban
    mo_ta = db.Column(db.Text)

    def __repr__(self):
        return f"<Ban {self.ten_ban}>"
