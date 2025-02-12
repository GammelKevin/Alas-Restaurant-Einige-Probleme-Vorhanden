from flask import request
from datetime import datetime, timedelta
from models import PageVisit, GalleryView, DailyStats
from extensions import db

def track_page_visit(page):
    try:
        now = datetime.utcnow()
        today = now.date()

        # Speichere den Seitenaufruf
        visit = PageVisit(
            page=page,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string if request.user_agent else None,
            timestamp=now
        )
        db.session.add(visit)
        db.session.flush()  # Flush, um sicherzustellen, dass der Besuch gespeichert ist
        
        # Aktualisiere die Tagesstatistik
        stats = DailyStats.query.filter_by(date=today).first()
        
        if not stats:
            stats = DailyStats(
                date=today,
                total_visits=1,
                unique_visitors=1 if not PageVisit.query.filter(
                    PageVisit.timestamp >= now.replace(hour=0, minute=0, second=0, microsecond=0),
                    PageVisit.ip_address == request.remote_addr,
                    PageVisit.page == page,
                    PageVisit.id != visit.id
                ).first() else 0,
                gallery_views=0
            )
            db.session.add(stats)
        else:
            stats.total_visits += 1
            
            # Zähle eindeutige Besucher (basierend auf IP)
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            previous_visits = PageVisit.query.filter(
                PageVisit.timestamp >= today_start,
                PageVisit.ip_address == request.remote_addr,
                PageVisit.page == page,
                PageVisit.id != visit.id
            ).count()
            
            if previous_visits == 0:  # Dies ist der erste Besuch von dieser IP heute für diese Seite
                stats.unique_visitors += 1
        
        db.session.commit()
        print(f"Tracked page visit: {page} from {request.remote_addr}")  # Debug-Ausgabe
    except Exception as e:
        print(f"Fehler beim Tracking des Seitenaufrufs: {str(e)}")
        db.session.rollback()

def track_gallery_view(image_id):
    try:
        print(f"Tracking gallery view for image {image_id}")  # Debug
        now = datetime.utcnow()
        today = now.date()

        # Speichere den Galerieaufruf
        view = GalleryView(
            image_id=image_id,
            ip_address=request.remote_addr,
            timestamp=now
        )
        print(f"Created view object: {view}")  # Debug
        db.session.add(view)
        db.session.flush()
        
        # Aktualisiere die Tagesstatistik
        stats = DailyStats.query.filter_by(date=today).first()
        print(f"Found stats for today: {stats}")  # Debug
        
        if not stats:
            print("Creating new stats for today")  # Debug
            stats = DailyStats(
                date=today,
                total_visits=0,
                unique_visitors=0,
                gallery_views=1
            )
            db.session.add(stats)
        else:
            print(f"Updating existing stats. Current gallery_views: {stats.gallery_views}")  # Debug
            stats.gallery_views += 1
            print(f"New gallery_views: {stats.gallery_views}")  # Debug
        
        db.session.commit()
        print("Successfully committed changes")  # Debug
        return True
    except Exception as e:
        print(f"Fehler beim Tracking des Galerieaufrufs: {str(e)}")
        db.session.rollback()
        raise

def get_statistics(days=30):
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days-1)  # -1 weil wir den aktuellen Tag mitzählen wollen
    
    # Hole alle existierenden Statistiken
    existing_stats = DailyStats.query.filter(
        DailyStats.date >= start_date,
        DailyStats.date <= end_date
    ).all()
    
    # Erstelle ein Dictionary für schnellen Zugriff
    stats_by_date = {stat.date: stat for stat in existing_stats}
    
    # Erstelle eine Liste aller Tage und fülle fehlende Tage mit leeren Statistiken
    all_stats = []
    current_date = start_date
    while current_date <= end_date:
        if current_date in stats_by_date:
            all_stats.append(stats_by_date[current_date])
        else:
            # Erstelle einen leeren Statistik-Eintrag für diesen Tag
            empty_stat = DailyStats(date=current_date, total_visits=0, unique_visitors=0, gallery_views=0)
            all_stats.append(empty_stat)
        current_date += timedelta(days=1)
    
    return all_stats
