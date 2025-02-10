from app import db, app, MenuCategory, MenuItem

def add_menu_items():
    def get_category(name):
        return MenuCategory.query.filter_by(name=name).first()

    # Fischgerichte
    fischgerichte = [
        {'name': 'Baby Calamari vom Grill', 'description': 'Gegrillte Baby-Calamari mit Zitronen-Olivenöl, frischem Butterreis & Senfsauce.', 'price': 19.20, 'category': 'fischgerichte'},
        {'name': 'Frittierte Baby Calamari', 'description': 'Panierter und frittierter Baby-Calamari mit Zitronen-Olivenöl, frischem Butterreis & Senfsauce.', 'price': 19.20, 'category': 'fischgerichte'},
        {'name': 'Garnelen Souflaki', 'description': 'Gegrillte Garnelen am Spieß mit frischem Butterreis & Senfsauce.', 'price': 22.60, 'category': 'fischgerichte'},
        {'name': 'Fischteller', 'description': 'Frittierte Calamari, gegrilltes Doradefilet, gegrillter Lachs, gegrillte Garnelen, frischer Butterreis, dazu Senfsauce.', 'price': 24.50, 'category': 'fischgerichte'},
        {'name': 'Dorade Royal', 'description': 'Zwei Doradenfilets mit Zitronen-Olivenöl, dazu frischer Butterreis und hausgemachte Senfsauce.', 'price': 24.50, 'category': 'fischgerichte'},
        {'name': 'Lachsfilet vom Grill', 'description': 'Gegrilltes Lachsfilet, mit frischem Butterreis, dazu Senfsauce.', 'price': 22.60, 'category': 'fischgerichte'}
    ]

    # Vegetarische Gerichte
    vegetarische_gerichte = [
        {'name': 'Stamna', 'description': 'Griechische Nudeln, frisches Gemüse und Kartoffeln aus dem Ofen.', 'price': 7.80, 'category': 'vegetarische_gerichte', 'vegetarian': True},
        {'name': 'Griechische Nudeln mit Gemüse & Tomatensauce', 'price': 9.30, 'category': 'vegetarische_gerichte', 'vegetarian': True},
        {'name': 'Gemüse Ograten', 'description': 'Gemüsemischung in Schlagsahne, mit Käse überbacken.', 'price': 7.80, 'category': 'vegetarische_gerichte', 'vegetarian': True}
    ]

    # Steak vom Grill
    steak_vom_grill = [
        {'name': 'Rumpsteak (ca. 300 g)', 'description': 'Mit Kräuterbutter & Ofenkartoffel.', 'price': 28.90, 'category': 'steak_vom_grill'}
    ]

    # Pfannengerichte
    pfannengerichte = [
        {'name': 'Gyros-Pfanne', 'description': 'In Metaxasauce zubereitet, mit Schafskäse überbacken, dazu Kartoffelscheiben.', 'price': 17.50, 'category': 'pfannengerichte'},
        {'name': 'Gyros überbacken mit Käse', 'description': 'In Metaxasauce zubereitet, dazu Kartoffelscheiben.', 'price': 17.50, 'category': 'pfannengerichte'},
        {'name': 'Psaronefri-Pfanne', 'description': 'Schweinefiletmedaillons mit Rahmsauce flambiert, dazu Kartoffelscheiben.', 'price': 19.60, 'category': 'pfannengerichte'},
        {'name': 'Musakas – Der weltbekannte Auflauf', 'description': 'Mit Auberginen, Hackfleisch & Kartoffeln, überbacken mit einer feinen Béchamel-Sauce.', 'price': 17.90, 'category': 'pfannengerichte'},
        {'name': 'Kotopulo-Pfanne', 'description': 'Hähnchenbrustfilet, überbacken in Metaxasauce, dazu Kartoffelscheiben.', 'price': 17.80, 'category': 'pfannengerichte'},
        {'name': 'Keftedakia Smyrneika – Pfanne', 'description': 'Frikadellen in Tomatensauce überbacken, dazu Kartoffelscheiben.', 'price': 18.20, 'category': 'pfannengerichte'}
    ]

    # Combine all items
    all_items = fischgerichte + vegetarische_gerichte + steak_vom_grill + pfannengerichte

    for item_data in all_items:
        category = get_category(item_data['category'])
        if category:
            item = MenuItem(
                name=item_data['name'],
                description=item_data.get('description', ''),
                price=item_data['price'],
                category_id=category.id,
                vegetarian=item_data.get('vegetarian', False),
                vegan=item_data.get('vegan', False),
                homemade=item_data.get('homemade', False)
            )
            db.session.add(item)

    db.session.commit()
    print("Fish dishes and more added successfully!")

if __name__ == '__main__':
    with app.app_context():
        add_menu_items()
