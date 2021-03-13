
from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,default = datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

class Jobb(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    Arbeidsgiver = db.Column(db.String(100),nullable=False)
    Stillingstittel = db.Column(db.String(100),nullable=False)
    Frist = db.Column(db.String(100),nullable=False)
    Ansettelsesform = db.Column(db.String(100),nullable=False)
    Sektor = db.Column(db.String(100),nullable=False)
    Bransje = db.Column(db.String(100),nullable=False)
    Stillingsfunksjon = db.Column(db.String(100),nullable=False)
    Url = db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Jobb('{self.id}, {self.arbeidsgiver}')"


class Small(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    test = db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Jobb('{self.id}, {self.test}')"

class New(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    arbeidsgiver = db.Column(db.String(100),nullable=False)
    stillingstittel = db.Column(db.String(100),nullable=False)
    frist = db.Column(db.String(100),nullable=False)
    ansettelsesform = db.Column(db.String(100),nullable=False)
    sektor = db.Column(db.String(100),nullable=False)
    bransje = db.Column(db.String(100),nullable=False)
    stillingsfunksjon = db.Column(db.String(100),nullable=False)
    url = db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"Jobb('{self.id}, {self.arbeidsgiver}')"