import os
from datetime import timedelta

# ===============================
# ĐƯỜNG DẪN GỐC DỰ ÁN
# ===============================
THU_MUC_GOC = os.path.abspath(os.path.dirname(__file__))


class Config:
    # ===============================
    # BẢO MẬT
    # ===============================
    SECRET_KEY = os.environ.get("SECRET_KEY") or "clb-quan-ly-secret-key"

    # Thời gian giữ đăng nhập
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # ===============================
    # DATABASE (SQLite – dễ chạy)
    # ===============================
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "sqlite:///" + os.path.join(THU_MUC_GOC, "app.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ===============================
    # UPLOAD FILE
    # (ĐỒNG BỘ ĐÚNG CẤU TRÚC BẠN ĐƯA)
    # ===============================
    UPLOAD_FOLDER = os.path.join(THU_MUC_GOC, "static", "uploads")

    DOCUMENT_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, "documents")
    FINANCE_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, "finance")
    TRANSFER_PROOF_FOLDER = os.path.join(UPLOAD_FOLDER, "transfer_proofs")
    PDF_REPORT_FOLDER = os.path.join(UPLOAD_FOLDER, "pdf_reports")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # ===============================
    # ĐỊNH DẠNG FILE CHO PHÉP
    # ===============================
    ANH_CHO_PHEP = {"png", "jpg", "jpeg"}
    TAI_LIEU_CHO_PHEP = {"pdf", "docx", "xlsx"}

    # ===============================
    # PHÂN QUYỀN HỆ THỐNG
    # (DÙNG CHO permission.py, decorators.py)
    # ===============================
    QUYEN_ADMIN = "ADMIN"
    QUYEN_BDH = "BDH"
    QUYEN_THU_QUY = "THU_QUY"
    QUYEN_THANH_VIEN = "THANH_VIEN"

    DANH_SACH_QUYEN = [
        QUYEN_ADMIN,
        QUYEN_BDH,
        QUYEN_THU_QUY,
        QUYEN_THANH_VIEN,
    ]

    # ===============================
    # TRẠNG THÁI THÀNH VIÊN
    # ===============================
    TRANG_THAI_HOAT_DONG = "Hoạt động"
    TRANG_THAI_CUU = "Cựu thành viên"

    DANH_SACH_TRANG_THAI = [
        TRANG_THAI_HOAT_DONG,
        TRANG_THAI_CUU,
    ]

    # ===============================
    # QUỸ – THỜI GIAN
    # ===============================
    NAM_BAT_DAU = 2025
    NAM_KET_THUC = 2050

    # ===============================
    # EMAIL (QUÊN MẬT KHẨU)
    # ===============================
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

