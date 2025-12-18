from extensions import db
from datetime import date


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    attended_date = db.Column(db.Date, default=date.today)
    present = db.Column(db.Boolean, default=True)

    member = db.relationship('Member')

    def __repr__(self):
        return f"<Attendance {self.member_id} {self.attended_date} {self.present}>"
