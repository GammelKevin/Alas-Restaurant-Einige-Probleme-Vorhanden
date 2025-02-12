from extensions import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'))
    image = db.Column(db.String(255))
    vegetarian = db.Column(db.Boolean, default=False)
    vegan = db.Column(db.Boolean, default=False)
    spicy = db.Column(db.Boolean, default=False)
    gluten_free = db.Column(db.Boolean, default=False)
    lactose_free = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    category = db.relationship('MenuCategory', backref=db.backref('items', lazy=True))

class MenuCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)

class OpeningHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)
    open_time_1 = db.Column(db.String(5))
    close_time_1 = db.Column(db.String(5))
    open_time_2 = db.Column(db.String(5))
    close_time_2 = db.Column(db.String(5))
    closed = db.Column(db.Boolean, default=False)
    vacation_start = db.Column(db.Date)
    vacation_end = db.Column(db.Date)
    vacation_active = db.Column(db.Boolean, default=False)

class GalleryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    order = db.Column(db.Integer, default=0)

class PageVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))

class GalleryView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('gallery_image.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))

class DailyStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    total_visits = db.Column(db.Integer, nullable=False, default=0)
    unique_visitors = db.Column(db.Integer, nullable=False, default=0)
    gallery_views = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, date=None, total_visits=0, unique_visitors=0, gallery_views=0):
        self.date = date
        self.total_visits = total_visits
        self.unique_visitors = unique_visitors
        self.gallery_views = gallery_views
