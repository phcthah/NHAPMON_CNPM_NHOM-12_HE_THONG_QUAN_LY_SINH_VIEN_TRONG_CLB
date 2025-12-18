# NHAPMON_CNPM_NHOM-12_HE_THONG_QUAN_LY_SINH_VIEN_TRONG_CLB
Tầm nhìn sản phẩm:
Xây dựng một hệ thống quản lý sinh viên hiện đại, minh bạch và hiệu quả, góp phần số hóa hoạt động quản lý của CLB, tạo nền tảng bền vững cho việc phát triển, kết nối và hỗ trợ các thành viên một cách toàn diện.
Hiện đại: Ứng dụng công nghệ mới (web/app, cơ sở dữ liệu tập trung, giao diện thân thiện) để tự động hóa và tối ưu quy trình quản lý.
Minh bạch: Dữ liệu rõ ràng, truy cập dễ dàng, giúp Ban điều hành nắm bắt tình hình hoạt động, thành viên, điểm danh, thành tích, v.v.
Hiệu quả: Giảm tải công việc thủ công, tiết kiệm thời gian cho cả Ban quản lý và thành viên.
Kết nối – Hỗ trợ: Tạo môi trường tương tác, trao đổi thông tin, hỗ trợ thành viên phát triển kỹ năng và gắn kết cộng đồng CLB.

Công nghệ lập trình: Visual Studio code;
Ngôn ngữ lập trình: Python làm hệ thống và html,css làm giao diện;
Cơ sở dữ liệu: SQLite;
Quản lí dự án, phân công việc và tổng hợp công việc bằng: Github, Git Bash, Trello.

Hướng dẫn chạy:

Tên thành viên:
1. Phan Công Thành:
2. Hồ Diệu Linh
3. Hồ Thị Quỳnh Hương
4. Lê Phương Linh
5. Phùng Thị Châu Giang
6. Nguyễn Thị Tuyết Nhung

# Flask Club (CLB)

Cấu trúc ban đầu của project được tạo sẵn. Các hướng dẫn nhanh:

1. Tạo virtualenv và cài dependencies:

   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt

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
