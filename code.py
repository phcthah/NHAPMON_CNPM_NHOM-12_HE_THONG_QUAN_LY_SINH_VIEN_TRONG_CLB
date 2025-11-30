import csv

# Danh sách hội viên
members = []

# ----------------------------
# Hàm CRUD cơ bản
# ----------------------------
def add_member():
    name = input("Tên hội viên: ")
    age = input("Tuổi: ")
    email = input("Email: ")
    member = {"name": name, "age": age, "email": email}
    members.append(member)
    print(f"Hội viên {name} đã được thêm.")

def view_members():
    if not members:
        print("Chưa có hội viên nào.")
        return
    print("\nDanh sách hội viên:")
    for i, m in enumerate(members, 1):
        print(f"{i}. {m['name']} - {m['age']} tuổi - {m['email']}")

def update_member():
    view_members()
    idx = int(input("Chọn số thứ tự hội viên muốn sửa: ")) - 1
    if idx < 0 or idx >= len(members):
        print("Không hợp lệ.")
        return
    members[idx]['name'] = input("Tên mới: ")
    members[idx]['age'] = input("Tuổi mới: ")
    members[idx]['email'] = input("Email mới: ")
    print("Cập nhật thành công.")

def delete_member():
    view_members()
    idx = int(input("Chọn số thứ tự hội viên muốn xóa: ")) - 1
    if idx < 0 or idx >= len(members):
        print("Không hợp lệ.")
        return
    removed = members.pop(idx)
    print(f"Đã xóa hội viên {removed['name']}.")

# ----------------------------
# Nhập danh sách từ CSV
# ----------------------------
def import_from_csv(filename):
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                members.append(row)
        print(f"Đã nhập {len(members)} hội viên từ {filename}.")
    except FileNotFoundError:
        print("File không tồn tại.")

# ----------------------------
# Xem danh sách theo bộ lọc
# ----------------------------
def filter_members():
    keyword = input("Nhập từ khóa để tìm kiếm (tên/email): ").lower()
    filtered = [m for m in members if keyword in m['name'].lower() or keyword in m['email'].lower()]
    if not filtered:
        print("Không tìm thấy hội viên.")
        return
    print("\nKết quả lọc:")
    for i, m in enumerate(filtered, 1):
        print(f"{i}. {m['name']} - {m['age']} tuổi - {m['email']}")

# ----------------------------
# Menu chính
# ----------------------------
def main():
    while True:
        print("\n--- Quản lý hội viên ---")
        print("1. Thêm hội viên")
        print("2. Xem danh sách hội viên")
        print("3. Cập nhật hội viên")
        print("4. Xóa hội viên")
        print("5. Nhập danh sách từ CSV")
        print("6. Tìm kiếm hội viên")
        print("0. Thoát")
        choice = input("Chọn chức năng: ")
        
        if choice == '1':
            add_member()
        elif choice == '2':
            view_members()
        elif choice == '3':
            update_member()
        elif choice == '4':
            delete_member()
        elif choice == '5':
            filename = input("Nhập tên file CSV: ")
            import_from_csv(filename)
        elif choice == '6':
            filter_members()
        elif choice == '0':
            print("Thoát chương trình.")
            break
        else:
            print("Chọn không hợp lệ.")

if __name__ == "__main__":
    main()
