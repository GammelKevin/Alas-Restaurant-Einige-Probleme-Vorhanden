from flask import request
from datetime import datetime, timedelta
from models import PageVisit, GalleryView, DailyStats
from extensions import db

def track_page_visit(page):
    try:
        # Speichere den Seitenaufruf
        visit = PageVisit(
            page=page,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(visit)
        
        # Aktualisiere die Tagesstatistik
        today = datetime.now().date()
        stats = DailyStats.query.filter_by(date=today).first()
        
        if not stats:
            stats = DailyStats(date=today)
            db.session.add(stats)
        
        stats.total_visits += 1
        
        # Zähle eindeutige Besucher (basierend auf IP)
        unique_ips = PageVisit.query.filter(
            PageVisit.timestamp >= datetime.now().replace(hour=0, minute=0, second=0),
            PageVisit.ip_address == request.remote_addr
        ).count()
        
        if unique_ips == 1:  # Erste Anfrage von dieser IP heute
            stats.unique_visitors += 1
        
        db.session.commit()
    except Exception as e:
        print(f"Fehler beim Tracking des Seitenaufrufs: {str(e)}")
        db.session.rollback()

def track_gallery_view(image_id):
    try:
        # Speichere den Galerieaufruf
        view = GalleryView(
            image_id=image_id,
            ip_address=request.remote_addr
        )
        db.session.add(view)
        
        # Aktualisiere die Tagesstatistik
        today = datetime.now().date()
        stats = DailyStats.query.filter_by(date=today).first()
        
        if not stats:
            stats = DailyStats(date=today)
            db.session.add(stats)
        
        stats.gallery_views += 1
        db.session.commit()
    except Exception as e:
        print(f"Fehler beim Tracking des Galerieaufrufs: {str(e)}")
        db.session.rollback()

def get_statistics(days=30):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    return DailyStats.query.filter(
        DailyStats.date >= start_date,
        DailyStats.date <= end_date
    ).order_by(DailyStats.date.desc()).all()
