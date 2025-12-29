from extensions import db
from config import Config


class Permission(db.Model):
    """
    =================================================
    BẢNG QUYỀN HỆ THỐNG
    =================================================
    """

    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    ma_quyen = db.Column(db.String(100), unique=True, nullable=False)
    ten_quyen = db.Column(db.String(255), nullable=False)
    mo_ta = db.Column(db.Text)

    def __repr__(self):
        return f"<Quyen {self.ma_quyen}>"

    # =================================================
    # MAP QUYỀN THEO VAI TRÒ (CỐ ĐỊNH)
    # =================================================
    @staticmethod
    def quyen_theo_vai_tro():
        return {
            Config.QUYEN_ADMIN: [
                "quan_ly_tai_khoan",
                "cap_quyen_he_thong",
                "duyet_thanh_vien",
                "xem_danh_sach_thanh_vien",
                "chinh_sua_thanh_vien",
                "quan_ly_ban",
                "gan_chuc_vu",
                "diem_danh",
                "xuat_bao_cao_diem_danh",
                "gui_thong_bao",
                "upload_tai_lieu",
                "xem_quy",
                "quan_ly_quy",
                "xac_nhan_chuyen_khoan",
                "xuat_bao_cao_quy",
                "xuat_bao_cao",
            ],
            Config.QUYEN_BDH: [
                "duyet_thanh_vien",
                "xem_danh_sach_thanh_vien",
                "chinh_sua_thanh_vien",
                "quan_ly_ban",
                "gan_chuc_vu",
                "diem_danh",
                "xuat_bao_cao_diem_danh",
                "gui_thong_bao",
                "upload_tai_lieu",
                "xem_quy",
                "xuat_bao_cao",
            ],
            Config.QUYEN_THU_QUY: [
                "xem_quy",
                "quan_ly_quy",
                "xac_nhan_chuyen_khoan",
                "xuat_bao_cao_quy",
            ],
            Config.QUYEN_THANH_VIEN: [
                "xem_quy",
            ],
        }

    # =================================================
    # TẠO QUYỀN HỆ THỐNG (CHẠY 1 LẦN)
    # =================================================
    @staticmethod
    def tao_quyen_mac_dinh():
        tat_ca_ma = set()

        for ds in Permission.quyen_theo_vai_tro().values():
            tat_ca_ma.update(ds)

        for ma in tat_ca_ma:
            if not Permission.query.filter_by(ma_quyen=ma).first():
                db.session.add(
                    Permission(
                        ma_quyen=ma,
                        ten_quyen=ma.replace("_", " ").capitalize()
                    )
                )

        db.session.commit()
