from app import db, app, MenuCategory, MenuItem

def add_menu_items():
    def get_category(name):
        return MenuCategory.query.filter_by(name=name).first()

    # Aperitifs
    aperitifs = [
        {'name': 'Tsipouro mit oder ohne Anis', 'price': 3.90, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Ouzo', 'price': 3.90, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Ouzo rose mit Rosen Likör', 'price': 4.00, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Ouzo mit Olive oder Feige', 'price': 4.20, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Ouzo mit Eiswürfeln', 'price': 3.90, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Martini Bianco oder Rosso', 'price': 4.50, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Orange- oder Sekt', 'price': 4.50, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Lillet Wild Berry', 'price': 4.50, 'category': 'aperitifs', 'contains_alcohol': True},
        {'name': 'Campari', 'price': 3.90, 'category': 'aperitifs', 'contains_alcohol': True}
    ]

    # Suppen
    suppen = [
        {'name': 'Tirokafteri', 'description': 'Pikanter Schafskäsedip.', 'price': 6.80, 'category': 'suppen'},
        {'name': 'Rote Beete-Salat', 'description': 'Mit Ziegenkäse & Walnüssen.', 'price': 7.20, 'category': 'suppen', 'vegetarian': True},
        {'name': 'Schafskäse', 'price': 7.50, 'category': 'suppen', 'vegetarian': True},
        {'name': 'Meeresfrüchte-Salat', 'description': 'Hausgemacht.', 'price': 13.90, 'category': 'suppen', 'homemade': True}
    ]

    # Salate
    salate = [
        {'name': 'Pikilia kria', 'description': 'Traditionelle gemischte kalte Vorspeisenplatte.', 'price': 15.20, 'category': 'salate'},
        {'name': 'Dolmades', 'description': 'Weinblätter mit Reis (kalt).', 'price': 6.70, 'category': 'salate', 'vegetarian': True},
        {'name': 'Dolmadakia', 'description': 'Gefüllte Weinblätter mit Reis & Hackfleisch.', 'price': 8.80, 'category': 'salate'},
        {'name': 'Zucchini-Bällchen', 'description': 'Hausgemachte Zucchinibällchen mit Feta, Frühlingszwiebeln & Tzatziki.', 'price': 7.80, 'category': 'salate', 'vegetarian': True, 'homemade': True},
        {'name': 'Gegrillte Peperoni', 'description': 'Mit Olivenöl & Balsamico.', 'price': 6.40, 'category': 'salate', 'vegetarian': True, 'vegan': True},
        {'name': 'Melitzanes / Kolokithakia', 'description': 'Gebratene Auberginen mit Zucchini & Tzatziki.', 'price': 9.60, 'category': 'salate', 'vegetarian': True},
        {'name': 'Talagani', 'description': 'Traditioneller Grillkäse, dazu Marmelade.', 'price': 9.60, 'category': 'salate', 'vegetarian': True},
        {'name': 'Florinis', 'description': 'Gegrillte rote Paprika, gefüllt mit Schafskäse.', 'price': 8.60, 'category': 'salate', 'vegetarian': True},
        {'name': 'Feta aus dem Ofen', 'description': 'Mit Tomaten, Peperoni, Oliven, Knoblauch, Zwiebeln & Olivenöl.', 'price': 8.90, 'category': 'salate', 'vegetarian': True},
        {'name': 'Feta saganaki', 'description': 'Schafskäse in einer goldbraunen Hülle gebraten.', 'price': 8.40, 'category': 'salate', 'vegetarian': True},
        {'name': 'Scampi saganaki', 'description': 'In einer pikanten Tomatensauce mit Fetakäse überbacken.', 'price': 15.20, 'category': 'salate'},
        {'name': 'Octopus vom Grill', 'price': 16.20, 'category': 'salate'},
        {'name': 'Gavros tiganitos', 'description': 'Sardellen in einer goldbraunen Hülle gebraten.', 'price': 10.80, 'category': 'salate'},
        {'name': 'Pikilia Zesti', 'description': 'Traditionelle gemischte warme Vorspeisenplatte.', 'price': 16.20, 'category': 'salate'},
        {'name': 'Knoblauchbrot', 'description': 'Überbackenes Brot mit Knoblauch & Käse.', 'price': 5.70, 'category': 'salate', 'vegetarian': True},
        {'name': 'Calamari Krönchen', 'description': 'Kleine knusprig frittierte Calamari-Tentakel in goldbrauner Panade.', 'price': 9.60, 'category': 'salate'},
        {'name': 'Faros', 'description': 'Fluffige Käsebällchen aus verschiedenen Käsesorten, goldbraun frittiert, mit würzigem Schafskäse-Paprika-Dip.', 'price': 11.90, 'category': 'salate', 'vegetarian': True}
    ]

    all_items = aperitifs + suppen + salate

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
                homemade=item_data.get('homemade', False),
                contains_alcohol=item_data.get('contains_alcohol', False)
            )
            db.session.add(item)

    db.session.commit()
    print("Additional menu items added successfully!")

if __name__ == '__main__':
    with app.app_context():
        add_menu_items()
