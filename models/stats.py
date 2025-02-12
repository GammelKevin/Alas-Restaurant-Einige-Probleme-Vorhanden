from extensions import db
from datetime import datetime

class PageVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))  # IPv6 Unterstützung
    user_agent = db.Column(db.String(255))

class GalleryView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))

class DailyStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    total_visits = db.Column(db.Integer, default=0)
    unique_visitors = db.Column(db.Integer, default=0)
    gallery_views = db.Column(db.Integer, default=0)