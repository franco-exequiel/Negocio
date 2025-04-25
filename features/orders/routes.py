from flask import Blueprint, request, jsonify, render_template
from core.db import db
from features.orders.models import Order, OrderItem
from features.users.models import User
from features.products.models import Product
from typing import Any, Dict, List

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
def create_order() -> Any:
    if request.form:
        # 📦 Datos desde formulario HTML
        user_id = request.form.get("user_id")
        raw_items = {
            int(key.split("[")[1][:-1]): int(val)
            for key, val in request.form.items()
            if key.startswith("items[") and val and int(val) > 0
        }
        items_data = [{"product_id": pid, "quantity": qty} for pid, qty in raw_items.items()]
    else:
        # 📦 Datos desde API (JSON)
        data: Dict[str, Any] = request.get_json()
        user_id = data.get("user_id")
        items_data = data.get("items") or []

    # ⚠️ Validaciones
    if not user_id or not items_data:
        return jsonify({"error": "Faltan datos necesarios (user_id, items)"}), 400

    # 🧾 Crear orden
    order = Order(user_id=user_id)
    db.session.add(order)
    db.session.flush()  # Necesario para obtener el order.id

    for item in items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item["product_id"],
            quantity=item.get("quantity", 1)
        )
        db.session.add(order_item)

    db.session.commit()

    # 🔁 Si fue desde HTML, redibujar la vista
    if request.form:
        return render_template("orders.html", users=User.query.all(), products=Product.query.all(), orders=Order.query.all())

    # ✅ Si fue API, responder JSON
    return jsonify({"message": "Orden creada", "order_id": order.id}), 201