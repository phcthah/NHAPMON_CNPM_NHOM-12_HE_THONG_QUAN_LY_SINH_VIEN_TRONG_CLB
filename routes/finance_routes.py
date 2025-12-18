from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.finance import FinanceEntry
from flask_login import login_required

finance_bp = Blueprint('finance', __name__, template_folder='../templates')


@finance_bp.route('/')
@login_required
def list_finance():
    entries = FinanceEntry.query.order_by(FinanceEntry.date.desc()).all()
    return render_template('finance.html', entries=entries)


@finance_bp.route('/add', methods=['POST'])
@login_required
def add_entry():
    description = (request.form.get('description') or '').strip()
    amount_raw = (request.form.get('amount') or '').strip()
    entries = FinanceEntry.query.order_by(FinanceEntry.date.desc()).all()
    form = {'description': description, 'amount': amount_raw}
    errors = []

    if not description:
        errors.append('Mô tả bắt buộc')
    try:
        amount = float(amount_raw)
    except ValueError:
        errors.append('Số tiền không hợp lệ')

    if errors:
        return render_template('finance.html', entries=entries, form=form, errors=errors)

    e = FinanceEntry(description=description, amount=amount)
    db.session.add(e)
    db.session.commit()
    flash('Ghi nhận thu chi', 'success')
    return redirect(url_for('finance.list_finance'))


@finance_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
    e = FinanceEntry.query.get_or_404(id)
    if request.method == 'POST':
        description = (request.form.get('description') or '').strip()
        amount_raw = (request.form.get('amount') or '').strip()
        errors = []
        form = {'description': description, 'amount': amount_raw}
        if not description:
            errors.append('Mô tả bắt buộc')
        try:
            amount = float(amount_raw)
        except ValueError:
            errors.append('Số tiền không hợp lệ')
        if errors:
            return render_template('finance_edit.html', entry=e, form=form, errors=errors)
        e.description = description
        e.amount = amount
        db.session.commit()
        flash('Cập nhật mục tài chính', 'success')
        return redirect(url_for('finance.list_finance'))
    return render_template('finance_edit.html', entry=e)


@finance_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_entry(id):
    e = FinanceEntry.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    flash('Đã xóa mục tài chính', 'warning')
    return redirect(url_for('finance.list_finance'))
