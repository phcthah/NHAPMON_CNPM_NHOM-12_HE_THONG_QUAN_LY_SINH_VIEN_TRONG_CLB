from extensions import db
from datetime import datetime


class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=True)

    team_id = db.Column(
        db.Integer,
        db.ForeignKey('teams.id'),
        nullable=True
    )

    team = db.relationship('Team', backref='members')

    def __repr__(self):
        return f"<Member {self.name}>"
class PendingMember(db.Model):
    __tablename__ = 'pending_members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=True)

    team_id = db.Column(
        db.Integer,
        db.ForeignKey('teams.id'),
        nullable=True
    )

    message = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    team = db.relationship('Team')

    def __repr__(self):
        return f"<PendingMember {self.name}>"
