from flask_jwt_extended import JWTManager,create_access_token
import pytz
from database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement =True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum('user', 'librarian'), nullable=False, default='user')
    login_date = db.Column(db.DateTime,default=datetime.now(pytz.utc))

# Configure JWTManager (assuming app is your Flask application instance)
jwt = JWTManager()

# SECTION/CATEGORY CLASS
class Section(db.Model):
    __tablename__ = 'section'
    sid = db.Column(db.Integer, primary_key=True,autoincrement = True)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String,nullable=False)
    description = db.Column(db.Text)
    books = db.relationship('EBook', backref='e_book', lazy='dynamic')


    
# PRODUCT CLASS
class EBook(db.Model):
    __tablename__ = 'e_book'
    ebid = db.Column(db.Integer, primary_key=True,autoincrement = True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.String,nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer,nullable=False)
    file = db.Column(db.String(255))        
    sectionid = db.Column(db.Integer, db.ForeignKey('section.sid'))

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    borrow_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    Status = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('e_book.ebid'), nullable=False)

class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ebid = db.Column(db.Integer, db.ForeignKey('e_book.ebid'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)