from app import db, app, MenuCategory, MenuItem

def add_menu_items():
    def get_category(name):
        return MenuCategory.query.filter_by(name=name).first()

    # Desserts
    desserts = [
        {'name': 'Griechischer Joghurt', 'description': 'Mit Honig & Walnüssen.', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Galaktoboureko', 'description': 'Blätterteig mit Vanilleeis-Grießcreme gefüllt & Vanilleeis.', 'price': 8.30, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Mille-feuille', 'description': 'Blätterteig gefüllt mit Vanillecreme, Erdbeeren & Pistazien.', 'price': 8.30, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Steirer-Eis', 'description': 'Vanilleeis mit Kürbiskernöl & karamellisierten Kürbiskernen.', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Coupé Ananas', 'description': 'Vanilleeis mit frischer Ananas & Schlagsahne.', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Heiße Feigen', 'description': 'Heiße Feigen gekocht in Cassis-Likör & Vanilleeis.', 'price': 6.70, 'category': 'desserts', 'vegetarian': True, 'contains_alcohol': True},
        {'name': 'Eis mit heißen Himbeeren', 'description': 'Vanilleeis mit heißen Himbeeren & Sahne.', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Gemischtes Eis', 'description': 'Vanille-, Erdbeer- und Schokoladeneis, dazu Sahne.', 'price': 6.70, 'category': 'desserts', 'vegetarian': True},
        {'name': 'Gadaifi', 'description': 'Knusprige Teigfäden mit Walnussfüllung und Zuckersirup, dazu Vanilleeis.', 'price': 8.30, 'category': 'desserts', 'vegetarian': True}
    ]

    # Kaffee & Tee
    kaffee_tee = [
        {'name': 'Espresso', 'price': 3.50, 'category': 'kaffee_und_tee'},
        {'name': 'Espresso Doppio', 'price': 3.50, 'category': 'kaffee_und_tee'},
        {'name': 'Espresso Macchiato', 'price': 3.50, 'category': 'kaffee_und_tee'},
        {'name': 'Affogato Espresso', 'price': 3.50, 'category': 'kaffee_und_tee'},
        {'name': 'Cappuccino', 'price': 3.60, 'category': 'kaffee_und_tee'},
        {'name': 'Latte Macchiato', 'price': 3.60, 'category': 'kaffee_und_tee'},
        {'name': 'Griechischer Mokka', 'price': 3.00, 'category': 'kaffee_und_tee'},
        {'name': 'Tasse Kaffee', 'price': 0.50, 'category': 'kaffee_und_tee'},
        {'name': 'Tasse Tee', 'price': 0.50, 'category': 'kaffee_und_tee'},
        {'name': 'Frappe', 'price': 3.00, 'category': 'kaffee_und_tee'},
        {'name': 'Eis-Schokolade', 'description': 'Mit Vanilleeis, Schokoladensauce & Sahne.', 'price': 6.70, 'category': 'kaffee_und_tee'},
        {'name': 'Eis-Kaffee', 'description': 'Mit Vanilleeis & Sahne.', 'price': 6.70, 'category': 'kaffee_und_tee'}
    ]

    # Wasser & Softdrinks
    getraenke = [
        {'name': 'Adldorfer Gourmet Natur 0,25l', 'price': 3.00, 'category': 'wasser_und_softdrinks'},
        {'name': 'Adldorfer Gourmet Natur 0,75l', 'price': 6.00, 'category': 'wasser_und_softdrinks'},
        {'name': 'Adldorfer Gourmet Klassik 0,25l', 'price': 3.00, 'category': 'wasser_und_softdrinks'},
        {'name': 'Adldorfer Gourmet Klassik 0,75l', 'price': 6.00, 'category': 'wasser_und_softdrinks'},
        {'name': 'Griechisches Wasser Still 0,5l', 'price': 4.80, 'category': 'wasser_und_softdrinks'},
        {'name': 'Tafelwasser 0,4l', 'price': 4.50, 'category': 'wasser_und_softdrinks'},
        {'name': 'Coca Cola 0,2l', 'price': 3.90, 'category': 'wasser_und_softdrinks'},
        {'name': 'Coca Cola 0,4l', 'price': 4.50, 'category': 'wasser_und_softdrinks'},
        {'name': 'Coca Cola Zero 0,2l', 'price': 3.90, 'category': 'wasser_und_softdrinks'},
        {'name': 'Coca Cola Zero 0,4l', 'price': 4.50, 'category': 'wasser_und_softdrinks'},
        {'name': 'Apfelschorle', 'price': 6.00, 'category': 'wasser_und_softdrinks'},
        {'name': 'Holunderschorle', 'price': 9.00, 'category': 'wasser_und_softdrinks'}
    ]

    # Combine all items
    all_items = desserts + kaffee_tee + getraenke

    for item_data in all_items:
        category = get_category(item_data['category'])
        if category:
            item = MenuItem(
                name=item_data['name'],
                description=item_data.get('description', ''),
                price=item_data['price'],
                category_id=category.id,
                vegetarian=item_data.get('vegetarian', False),
                contains_alcohol=item_data.get('contains_alcohol', False)
            )
            db.session.add(item)

    db.session.commit()
    print("Desserts and beverages added successfully!")

if __name__ == '__main__':
    with app.app_context():
        add_menu_items()
