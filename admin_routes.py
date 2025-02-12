from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from models import MenuItem, MenuCategory, OpeningHours, GalleryImage, PageVisit, GalleryView, DailyStats
from extensions import db
from datetime import datetime, timedelta
from sqlalchemy import func
from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, BooleanField
from wtforms.validators import DataRequired

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')

@admin.route('/menu')
@login_required
def menu():
    categories = MenuCategory.query.order_by(MenuCategory.order).all()
    items = MenuItem.query.order_by(MenuItem.category_id, MenuItem.order).all()
    return render_template('admin/menu.html', categories=categories, items=items)

@admin.route('/opening-hours', methods=['GET', 'POST'])
@login_required
def opening_hours():
    form = FlaskForm()
    hours = OpeningHours.query.order_by(OpeningHours.id).all()
    
    if form.validate_on_submit():
        try:
            opening_hour = OpeningHours(
                day=request.form.get('day'),
                open_time_1=None,
                close_time_1=None,
                open_time_2=None,
                close_time_2=None,
                closed=request.form.get('closed') == 'on',
                vacation_start=request.form.get('vacation_start'),
                vacation_end=request.form.get('vacation_end'),
                vacation_active=request.form.get('vacation_active') == 'on'
            )
            
            # Only set time fields if not on vacation and not closed
            if not opening_hour.vacation_active and not opening_hour.closed:
                opening_hour.open_time_1 = request.form.get('open_time_1')
                opening_hour.close_time_1 = request.form.get('close_time_1')
                opening_hour.open_time_2 = request.form.get('open_time_2')
                opening_hour.close_time_2 = request.form.get('close_time_2')
            
            opening_hour.validate_times()
            db.session.add(opening_hour)
            db.session.commit()
            flash('Öffnungszeiten wurden aktualisiert.', 'success')
        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash('Ein Fehler ist aufgetreten.', 'error')
            db.session.rollback()
            
        return redirect(url_for('admin.opening_hours'))
    
    return render_template('admin/opening_hours.html', form=form, hours=hours)

@admin.route('/opening-hours/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_opening_hours(id):
    opening_hour = OpeningHours.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            form = FlaskForm()
            if not form.validate():
                return jsonify({'success': False, 'error': 'CSRF-Token ungültig'}), 400
                
            opening_hour.day = request.form.get('day')
            opening_hour.vacation_active = request.form.get('vacation_active') == 'on'
            opening_hour.closed = request.form.get('closed') == 'on'
            
            # Handle vacation first
            if opening_hour.vacation_active:
                opening_hour.vacation_start = request.form.get('vacation_start')
                opening_hour.vacation_end = request.form.get('vacation_end')
                # Clear time fields and closed status for vacation days
                opening_hour.closed = False
                opening_hour.open_time_1 = None
                opening_hour.close_time_1 = None
                opening_hour.open_time_2 = None
                opening_hour.close_time_2 = None
            else:
                opening_hour.vacation_start = None
                opening_hour.vacation_end = None
                
                # Handle closed status
                if opening_hour.closed:
                    # Clear time fields for closed days
                    opening_hour.open_time_1 = None
                    opening_hour.close_time_1 = None
                    opening_hour.open_time_2 = None
                    opening_hour.close_time_2 = None
                else:
                    # Only set time fields if not closed and not on vacation
                    opening_hour.open_time_1 = request.form.get('open_time_1')
                    opening_hour.close_time_1 = request.form.get('close_time_1')
                    opening_hour.open_time_2 = request.form.get('open_time_2')
                    opening_hour.close_time_2 = request.form.get('close_time_2')
            
            opening_hour.validate_times()
            db.session.commit()
            return jsonify({'success': True})
        except ValueError as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': 'Ein Fehler ist aufgetreten.'}), 400
    
    # GET request - return current values
    return jsonify({
        'id': opening_hour.id,
        'day': opening_hour.day,
        'open_time_1': opening_hour.open_time_1 or '',
        'close_time_1': opening_hour.close_time_1 or '',
        'open_time_2': opening_hour.open_time_2 or '',
        'close_time_2': opening_hour.close_time_2 or '',
        'closed': opening_hour.closed,
        'vacation_start': opening_hour.vacation_start or '',
        'vacation_end': opening_hour.vacation_end or '',
        'vacation_active': opening_hour.vacation_active
    })

@admin.route('/opening-hours/delete/<int:id>', methods=['POST'])
@login_required
def delete_opening_hours(id):
    try:
        form = FlaskForm()
        if not form.validate():
            return jsonify({'success': False, 'error': 'CSRF-Token ungültig'}), 400
            
        opening_hour = OpeningHours.query.get_or_404(id)
        db.session.delete(opening_hour)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@admin.route('/gallery')
@login_required
def gallery():
    images = GalleryImage.query.order_by(GalleryImage.order).all()
    return render_template('admin/gallery.html', images=images)

@admin.route('/statistics')
@login_required
def statistics():
    # Zeitraum für die Statistiken (letzte 30 Tage)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Seitenaufrufe pro Tag
    daily_visits = db.session.query(
        func.date(PageVisit.timestamp).label('date'),
        func.count(PageVisit.id).label('count')
    ).filter(
        PageVisit.timestamp >= start_date,
        PageVisit.timestamp <= end_date
    ).group_by(
        func.date(PageVisit.timestamp)
    ).order_by(
        func.date(PageVisit.timestamp)
    ).all()
    
    # Galerie-Aufrufe pro Tag
    gallery_views = db.session.query(
        func.date(GalleryView.timestamp).label('date'),
        func.count(GalleryView.id).label('count')
    ).filter(
        GalleryView.timestamp >= start_date,
        GalleryView.timestamp <= end_date
    ).group_by(
        func.date(GalleryView.timestamp)
    ).order_by(
        func.date(GalleryView.timestamp)
    ).all()
    
    # Tägliche Statistiken
    daily_stats = DailyStats.query.filter(
        DailyStats.date >= start_date.date(),
        DailyStats.date <= end_date.date()
    ).order_by(DailyStats.date).all()
    
    # Formatiere die Daten für die Diagramme
    dates = [(end_date - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30)]
    visits_data = {str(date): count for date, count in daily_visits}
    gallery_data = {str(date): count for date, count in gallery_views}
    stats_data = {str(stat.date): stat for stat in daily_stats}
    
    # Erstelle die vollständigen Datenlisten (mit Nullen für fehlende Tage)
    visits = [visits_data.get(date, 0) for date in dates]
    gallery = [gallery_data.get(date, 0) for date in dates]
    conversion = []
    
    for date in dates:
        if date in stats_data and stats_data[date].total_visits > 0:
            rate = (stats_data[date].converted_visits / stats_data[date].total_visits) * 100
            conversion.append(round(rate, 2))
        else:
            conversion.append(0)
    
    return render_template('admin/statistics.html',
                         dates=dates,
                         visits=visits,
                         gallery=gallery,
                         conversion=conversion)

@admin.route('/menu/add', methods=['POST'])
@login_required
def add_menu_item():
    try:
        data = request.get_json()
        
        # Überprüfe, ob alle erforderlichen Felder vorhanden sind
        required_fields = ['name', 'description', 'price', 'category_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Feld {field} fehlt'}), 400
        
        # Erstelle ein neues MenuItem
        item = MenuItem(
            name=data['name'],
            description=data['description'],
            price=float(data['price']),
            category_id=int(data['category_id']),
            order=data.get('order', 0)  # Optional, Standard ist 0
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'item': {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'category_id': item.category_id,
                'order': item.order
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@admin.route('/menu/delete/<int:id>', methods=['POST'])
@login_required
def delete_menu_item(id):
    try:
        item = MenuItem.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        flash('Item wurde erfolgreich gelöscht.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Fehler beim Löschen des Items.', 'error')
    return redirect(url_for('admin.menu'))
    return redirect(url_for('admin.menu'))
