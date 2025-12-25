# Flask Club (CLB)
# Thành viên nhóm 12
- **Hồ Diệu Linh** – Nhóm trưởng
- **Hồ Thị Quỳnh Hương**
- **Lê Phương Linh**
- **Phùng Châu Giang**
- **Nguyễn Thị Tuyết Nhung**
- **Phan Công Thành**

# HỆ THỐNG QUẢN LÝ SINH VIÊN TRONG CÂU LẠC BỘ
Giới thiệu: Hệ thống Quản lý Sinh viên trong Câu lạc bộ là một ứng dụng web giúp Ban Chủ nhiệm CLB quản lý thông tin thành viên, ban nhóm, điểm danh và kiểm soát tài chính CLB một cách khoa học – tiện lợi – hiệu quả. Hệ thống phù hợp với mô hình CLB sinh viên, phục vụ mục đích học tập và nghiên cứu trong học phần Nhập môn Công nghệ Phần mềm.

# Mục tiêu :
- Số hóa công tác quản lý CLB sinh viên
- Giảm thao tác thủ công, hạn chế sai sót
- Dễ sử dụng, dễ mở rộng
- Làm nền tảng cho các chức năng nâng cao trong tương lai

# Đối tượng sử dụng
- Ban Chủ nhiệm CLB
- Thành viên CLB

# Chức năng chính
- Đăng ký, đăng nhập, xác thực người dùng
- Quản lý thành viên CLB
- Quản lý ban / tiểu ban
- Quản lý điểm danh sinh hoạt
- Quản lý thu – chi tài chính CLB

# Công nghệ sử dụng
- Backend: Python, Flask
- Frontend: HTML, CSS, Bootstrap
- CSDL: MySQL
- ORM: Flask-SQLAlchemy
- Xác thực: Flask-Login

# Kiến trúc hệ thống
- Hệ thống được xây dựng theo mô hình MVC (Model – View – Controller):
- models/ – quản lý dữ liệu
- routes/ – xử lý nghiệp vụ và điều hướng
- templates/ – giao diện người dùng
- static/ – tài nguyên CSS, hình ảnh
# Phạm vi & Giới hạn
- Hệ thống phục vụ quản lý nội bộ CLB sinh viên
- Chưa hỗ trợ triển khai production
- Chưa tích hợp thanh toán trực tuyến
- Chưa hỗ trợ nhiều CLB trên cùng một hệ thống
# Hướng phát triển
- Phân quyền chi tiết (Admin / Trưởng ban / Thành viên)
- Xuất báo cáo Excel/PDF
- Thống kê hoạt động CLB
- Tách Frontend – Backend (REST API)
- Triển khai Docker / Cloud
- Thông báo & upload chia sẻ tài liệu
- Thống báo, xử lí, chỉnh sửa phân chia nhiệm vụ
- Quản lý tài liệu
- Đánh giá khen thưởng 

# Cấu trúc ban đầu của project được tạo sẵn. 
# Các hướng dẫn nhanh cài đặt & chạy hệ thống:
1. Yêu cầu môi trường

   Git ≥ 2.x

   Python ≥ 3.10

   Trình duyệt web (Chrome / Edge / Firefox)

1. Tạo virtualenv và cài dependencies:

   - Tạo môi trường ảo: python -m venv .venv
   - Kích hoạt môi trường ảo: source venv\Scripts\activate
   - Cài đặt thư viện cần thiết: pip install -r requirements.txt

2. Chạy app:

   python app.py

3. Thay đổi sang MySQL (tuỳ chọn)

   - Cài MySQL server (hoặc MariaDB) trên máy Windows.
   - Tạo database và user (ví dụ dùng MySQL client):

     mysql -u root -p
     CREATE DATABASE clb_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
     CREATE USER 'clbuser'@'localhost' IDENTIFIED BY 'your_password';
     GRANT ALL PRIVILEGES ON clb_db.* TO 'clbuser'@'localhost';
     FLUSH PRIVILEGES;

   - Cài driver Python và Flask-Migrate (đã có trong `requirements.txt`):

     pip install -r requirements.txt

   - Thiết lập biến môi trường `DATABASE_URL` (Windows PowerShell):

     setx DATABASE_URL "mysql+pymysql://clbuser:your_password@localhost/clb_db"

   - Khởi tạo migration và áp dụng:

     setx FLASK_APP "app:create_app"
     setx FLASK_ENV "development"
     flask db init
     flask db migrate -m "Initial migration"
     flask db upgrade

   Nếu bạn không muốn dùng MySQL ngay bây giờ, app vẫn dùng SQLite mặc định (`sqlite:///clb.db`).

4. Mặc định có 1 user admin:
 username: admin
 password: admin

Các tệp chính: `app.py`, `config.py`, `models/`, `routes/`, `templates/`, `static/`.
# Cấu trúc thư mục: 
├── app.py
├── config.py
├── extensions.py
├── models/
├── routes/
├── project/
├── templates/
├── static/
├── requirements.txt
├── README.md

