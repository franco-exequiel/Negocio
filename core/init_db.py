# init_db.py
"""
Script de inicialización para el proyecto Tienda.
Crea TODAS las tablas de la base de datos (usuarios, productos, pedidos).

Este archivo es SEGURO para subir a GitHub: no contiene claves ni tokens.
"""

from app import create_app
from core.db import db

# Importar TODOS los modelos antes de db.create_all()
from features.products.models import Product
from features.users.models import User
from features.orders.models import Order, OrderItem

def init_database() -> None:
    app = create_app()

    with app.app_context():
        print("📦 Creando tablas...")
        try:
            db.create_all()
        except Exception as e:
            print("❌ Error al crear las tablas:", str(e))
            raise   
        print("✅ Todas las tablas fueron creadas correctamente.")

        # Cargar datos de ejemplo solo si la base está vacía
        if not Product.query.first():
            demo = Product(name="Producto demo", price=100.0, stock=10)
            db.session.add(demo)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print("❌ Error al cargar datos demo:", str(e))
            print("🧪 Producto de ejemplo cargado.")

if __name__ == "__main__":
    init_database()