from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.position import Position
from extensions import db

position_bp = Blueprint("position", __name__)

# --- DANH SÁCH & THÊM ---
@position_bp.route("/", methods=["GET", "POST"])
def quan_ly_chuc_vu():
    if request.method == "POST":
        ten = request.form.get("ten_chuc_vu")
        mo_ta = request.form.get("mo_ta")
        
        if Position.query.filter_by(ten_chuc_vu=ten).first():
            flash("Chức vụ này đã tồn tại!", "danger")
        else:
            new_pos = Position(ten_chuc_vu=ten, mo_ta=mo_ta)
            db.session.add(new_pos)
            db.session.commit()
            flash("Thêm chức vụ thành công!", "success")
        return redirect(url_for("position.quan_ly_chuc_vu"))

    positions = Position.query.all()
    return render_template("admin/positions.html", positions=positions)

# --- SỬA ---
@position_bp.route("/edit/<int:id>", methods=["POST"])
def sua_chuc_vu(id):
    pos = Position.query.get_or_404(id)
    pos.ten_chuc_vu = request.form.get("ten_chuc_vu")
    pos.mo_ta = request.form.get("mo_ta")
    db.session.commit()
    flash("Cập nhật thành công!", "success")
    return redirect(url_for("position.quan_ly_chuc_vu"))

# --- XÓA ---
@position_bp.route("/delete/<int:id>", methods=["POST"])
def xoa_chuc_vu(id):
    pos = Position.query.get_or_404(id)
    # Kiểm tra nếu có thành viên đang giữ chức vụ này thì không cho xóa (tùy chọn)
    if pos.danh_sach_thanh_vien: 
        flash("Không thể xóa chức vụ đang có thành viên đảm nhiệm!", "warning")
    else:
        db.session.delete(pos)
        db.session.commit()
        flash("Đã xóa chức vụ!", "success")
    return redirect(url_for("position.quan_ly_chuc_vu"))