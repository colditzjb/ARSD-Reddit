
from dashboard import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    posts = db.relationship('Post', backref='poster')
    comments = db.relationship('Comment', backref='commenter')
    def get_user_id(self):
        return self.id

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    subreddit = db.Column(db.String(21), nullable=False)
    submission_id = db.Column(db.String(100), nullable=False)
    body_text = db.Column(db.String(40000), nullable=False)
    num_comments = db.Column(db.Integer, nullable=False)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.BigInteger, nullable=False)
    parent = db.Column(db.String(100), nullable=False)
    subreddit = db.Column(db.String(21),nullable=False)
    body_text = db.Column(db.String(30000),nullable=False)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'))