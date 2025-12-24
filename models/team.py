from extensions import db


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    members = db.relationship('Member', back_populates='team', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Team {self.name}>"
