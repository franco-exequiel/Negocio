from flask import Blueprint, request, jsonify, render_template
from core.db import db
from features.orders.models import Order, OrderItem
from features.users.models import User
from features.products.models import Product
from typing import Any


from flask import Blueprint, request, jsonify
from .models import Order, OrderItem
from features.products.models import Product
from features.users.models import User
from .schemas import OrderCreate
from core.db import db


orders_bp = Blueprint("orders", __name__, url_prefix="/orders")

# Página HTML de prueba
@orders_bp.route("/web", methods=["GET"])
def order_form() -> Any:
    users = User.query.all()
    products = Product.query.all()
    orders = Order.query.all()
    return render_template("orders.html", users=users, products=products, orders=orders)

# Obtener todas las órdenes (JSON)
@orders_bp.route("/", methods=["GET"])
def get_orders() -> Any:
    orders = Order.query.all()
    return jsonify([
        {
            "id": o.id,
            "user": {"id": o.user.id, "name": o.user.name},
            "created_at": o.created_at.isoformat(),
            "items": [
                {
                    "product_id": i.product_id,
                    "product_name": i.product.name,
                    "quantity": i.quantity
                } for i in o.items
            ]
        }
        for o in orders
    ]), 200

# Crear nueva orden (formulario o JSON)
@orders_bp.route("/", methods=["POST"])
def create_order():
    try:
        data = request.get_json()
        validated = OrderCreate(**data)

        # Verificar que el usuario exista
        user = User.query.get(validated.user_id)
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Crear la orden
        order = Order(user_id=user.id)
        db.session.add(order)
        db.session.flush()  # Para obtener el order.id antes de agregar items

        for item_data in validated.items:
            product = Product.query.get(item_data.product_id)
            if not product:
                return jsonify({"error": f"Producto ID {item_data.product_id} no encontrado"}), 404
            
            if product.stock < item_data.quantity:
                return jsonify({"error": f"No hay suficiente stock para el producto '{product.name}'"}), 400

            # Restar stock
            product.stock -= item_data.quantity

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item_data.quantity,
            )
            db.session.add(order_item)

        db.session.commit()

        return jsonify({"message": "Orden creada exitosamente."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


