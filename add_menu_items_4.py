from app import db, app, MenuCategory, MenuItem

def add_menu_items():
    def get_category(name):
        return MenuCategory.query.filter_by(name=name).first()

    # Spezialitäten vom Lamm
    lamm_spezialitaeten = [
        {'name': 'Lammkoteletts', 'description': 'Mit Kartoffelscheiben, grünen Bohnen & Tzatziki.', 'price': 21.60, 'category': 'spezialitaeten_vom_lamm'},
        {'name': 'Zarte Lammhaxen aus dem Backofen', 'description': 'Mit Schafskäse gratiniert, dazu Kartoffelscheiben & gemischter Salat.', 'price': 21.20, 'category': 'spezialitaeten_vom_lamm'},
        {'name': 'Mit dicken Bohnen', 'price': 17.90, 'category': 'spezialitaeten_vom_lamm'},
        {'name': 'Mit Bamies (Okraschoten)', 'price': 17.20, 'category': 'spezialitaeten_vom_lamm'},
        {'name': 'Mit Spaghetti', 'price': 19.90, 'category': 'spezialitaeten_vom_lamm'},
        {'name': 'Stifado', 'description': 'Zartes Lammfleisch mit Schalotten in Tomaten-Kräutersauce.', 'price': 17.80, 'category': 'spezialitaeten_vom_lamm'},
        {'name': 'Kleftiko', 'description': 'Marinierte Lammhaxe mit Schafskäse, in Alufolie gebacken, aromatisiert mit Knoblauch, Dill, Thymian, serviert mit Bratkartoffeln.', 'price': 19.90, 'category': 'spezialitaeten_vom_lamm'}
    ]

    # Fleischgerichte
    fleischgerichte = [
        {'name': 'Sutzukakia', 'description': 'Gegrillte Hackfleischröllchen, mit Tomatenreis & Tzatziki.', 'price': 14.90, 'category': 'fleischgerichte'},
        {'name': 'Gyros', 'description': 'Serviert mit Tomatenreis & Tzatziki.', 'price': 15.90, 'category': 'fleischgerichte', 'homemade': True},
        {'name': 'Souflaki', 'description': 'Zwei Spieße, serviert mit Tomatenreis & Tzatziki.', 'price': 15.90, 'category': 'fleischgerichte'},
        {'name': 'Bifteki', 'description': 'Hacksteak gefüllt mit Schafskäse, serviert mit Tomatenreis & Tzatziki.', 'price': 17.50, 'category': 'fleischgerichte'},
        {'name': 'Hähnchenfilet', 'description': 'Serviert mit Tomatenreis & Tzatziki.', 'price': 15.60, 'category': 'fleischgerichte'},
        {'name': 'Bauernspieß', 'description': 'Vom Schwein mit Paprika & Zwiebeln, saftig gegrillt, dazu Folienkartoffel & Tzatziki.', 'price': 20.50, 'category': 'fleischgerichte'},
        {'name': 'Kalbsleber', 'description': 'Mit gerösteten Zwiebeln, einem Hauch von Knoblauch, Kartoffelscheiben & Tzatziki.', 'price': 17.50, 'category': 'fleischgerichte'},
        {'name': 'Rückensteak vom Grill', 'description': '(Vom Schwein) mit Kräuterbutter & Tomatenreis & Tzatziki.', 'price': 17.50, 'category': 'fleischgerichte'},
        {'name': 'Medaillons vom Grill', 'description': '(Vom Schwein) mit Kräuterbutter & Tomatenreis & Tzatziki.', 'price': 19.60, 'category': 'fleischgerichte'},
        {'name': 'Schnitzel Wiener Art', 'description': '(Vom Schwein) mit Pommes Frites & Tzatziki.', 'price': 16.80, 'category': 'fleischgerichte'}
    ]

    # Gemischte Fleischplatten
    fleischplatten = [
        {'name': 'Mia-Platte', 'description': 'Gyros, Lammkotelett, Souflaki, Sutzuki mit Tomatenreis, dazu Tzatziki.', 'price': 17.90, 'category': 'gemischte_fleischplatten'},
        {'name': 'Alas-Platte', 'description': 'Souflaki, Kalbsleber, Sutzuki, Gyros mit Tomatenreis, dazu Tzatziki.', 'price': 17.20, 'category': 'gemischte_fleischplatten'},
        {'name': 'Meteora-Platte', 'description': 'Gyros, 2 St. Kalbsleber mit Tomatenreis, dazu Tzatziki.', 'price': 19.90, 'category': 'gemischte_fleischplatten'},
        {'name': 'Trikala-Platte', 'description': 'Gyros & Souflaki mit Tomatenreis, dazu Tzatziki.', 'price': 17.80, 'category': 'gemischte_fleischplatten'},
        {'name': 'Thessalia-Platte', 'description': 'Gyros & Kalamari mit Tomatenreis, dazu Tzatziki.', 'price': 17.80, 'category': 'gemischte_fleischplatten'},
        {'name': 'Volos-Platte', 'description': 'Gyros & 2 St. Sutzuki mit Tomatenreis, dazu Tzatziki.', 'price': 18.20, 'category': 'gemischte_fleischplatten'},
        {'name': 'Dorf-Platte', 'description': 'Gyros, 1 St. Souflaki & 1 St. Rückensteak mit Tomatenreis, dazu Tzatziki.', 'price': 18.20, 'category': 'gemischte_fleischplatten'}
    ]

    # Combine all items
    all_items = lamm_spezialitaeten + fleischgerichte + fleischplatten

    for item_data in all_items:
        category = get_category(item_data['category'])
        if category:
            item = MenuItem(
                name=item_data['name'],
                description=item_data.get('description', ''),
                price=item_data['price'],
                category_id=category.id,
                homemade=item_data.get('homemade', False)
            )
            db.session.add(item)

    db.session.commit()
    print("Lamb specialties and meat dishes added successfully!")

if __name__ == '__main__':
    with app.app_context():
        add_menu_items()
