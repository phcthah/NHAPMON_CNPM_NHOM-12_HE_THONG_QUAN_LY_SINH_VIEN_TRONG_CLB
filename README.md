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
