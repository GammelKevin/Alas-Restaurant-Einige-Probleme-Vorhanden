from extensions import db

class OpeningHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)
    open_time_1 = db.Column(db.String(5), nullable=True)
    close_time_1 = db.Column(db.String(5), nullable=True)
    open_time_2 = db.Column(db.String(5), nullable=True)
    close_time_2 = db.Column(db.String(5), nullable=True)
    closed = db.Column(db.Boolean, default=False)
    vacation_start = db.Column(db.String(10), nullable=True)
    vacation_end = db.Column(db.String(10), nullable=True)
    vacation_active = db.Column(db.Boolean, default=False)

    def validate_times(self):
        if not self.closed:
            if not self.open_time_1 or not self.close_time_1:
                raise ValueError("Erste Öffnungszeit und Schließzeit müssen angegeben werden")
            
            # Prüfe das Format der Zeiten (HH:MM)
            for time_str in [self.open_time_1, self.close_time_1]:
                if time_str and not time_str.replace(':', '').isdigit():
                    raise ValueError("Ungültiges Zeitformat. Bitte verwenden Sie HH:MM")
            
            # Wenn zweite Öffnungszeit angegeben ist, müssen beide Zeiten vorhanden sein
            if self.open_time_2 or self.close_time_2:
                if not self.open_time_2 or not self.close_time_2:
                    raise ValueError("Beide Zeiten der zweiten Öffnungszeit müssen angegeben werden")
                
                for time_str in [self.open_time_2, self.close_time_2]:
                    if time_str and not time_str.replace(':', '').isdigit():
                        raise ValueError("Ungültiges Zeitformat. Bitte verwenden Sie HH:MM")
    
    def __repr__(self):
        if self.closed:
            return f"{self.day}: Geschlossen"
        times = f"{self.open_time_1} - {self.close_time_1}"
        if self.open_time_2 and self.close_time_2:
            times += f" und {self.open_time_2} - {self.close_time_2}"
        if self.vacation_active:
            times += f" (Urlaub: {self.vacation_start} - {self.vacation_end})"
        return f"{self.day}: {times}"