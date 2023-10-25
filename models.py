from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    user_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    wca_id = db.Column(db.String(10),unique=True, nullable=True)
    email = db.Column(db.String(100),nullable=True)
    medlem = db.Column(db.Boolean)
    postnummer = db.Column(db.Integer,nullable=True)
    modtag_mails = db.Column(db.Boolean)
    sidste_comp = db.Column(db.DateTime,nullable=True)
    first_login = db.Column(db.DateTime,nullable=True)

    def __init__(self,userid,name,wcaid,email,medlem,postnummer,modtag_mails,sidste_comp,first_login) -> None:
        self.user_id = userid
        self.name = name
        self.wca_id = wcaid
        self.email = email
        self.medlem = medlem
        self.postnummer = postnummer
        self.modtag_mails = modtag_mails
        self.sidste_comp = sidste_comp
        self.first_login = first_login

class Admins(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),primary_key=True)
    user = db.relationship('Users', backref=db.backref('admins', lazy=True))

    def __init__(self,user_id) -> None:
        self.user_id = user_id

class External_payments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('external_payments', lazy=True))
    payment_date = db.Column(db.DateTime, nullable=False)

def init_db(app):
    db.init_app(app)

