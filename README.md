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

3. Mặc định có 1 user admin:

   username: admin
   password: admin

4. Cài đặt thư viện:
   pip install Flask>=2.0 Flask-Login>=0.5 Flask-SQLAlchemy>=2.5 Werkzeug>=2.0 PyMySQL>=1.0 Flask-Migrate>=4.0

Các tệp chính: `app.py`, `config.py`, `models/`, `routes/`, `templates/`, `static/`.
