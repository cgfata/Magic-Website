from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    name = db.Column(db.String(255),nullable=False)
    edition = db.Column(db.String(255), nullable=False)
    cardnumber = db.Column(db.String(255))
    foil = db.Column(db.String(4))
    discordid = db.Column(db.String(255), db.ForeignKey('user.discordid'))

    def to_dict(self):
        return {
            'id': self.id,
            'count': self.count,
            'name': self.name,
            'edition': self.edition,
            'cardnumber': self.cardnumber,
            'foil': self.foil,
            'discordid': self.discordid
        }

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    discordid = db.Column(db.String(255),unique=True)
    cards = db.relationship('Inventory')

