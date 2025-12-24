from extensions import db
from datetime import datetime


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

    team = db.relationship('Team', back_populates='members')

    def __repr__(self):
        return f"<Member {self.name}>"


class PendingMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    message = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    team = db.relationship('Team')

    def __repr__(self):
        return f"<PendingMember {self.name}>"
