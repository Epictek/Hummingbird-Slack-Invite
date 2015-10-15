from app import db
import datetime

class User(db.Model):
    invite_id = db.Column(db.String(36),unique=True, primary_key=True)
    hb_user = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    ip = db.Column(db.String(12))
    verified = db.Column(db.Boolean)
    date = db.Column(db.DateTime)

    def __init__(self,invite_id, hb_user, email, ip):
        self.invite_id = invite_id
        self.hb_user = hb_user
        self.email = email
        self.ip = ip
        self.verified = False
        self.date = datetime.datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % (self.hb_user)

