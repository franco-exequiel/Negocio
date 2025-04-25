from flask import Blueprint, request, jsonify, render_template
from core.db import db
from features.products.models import Product
from typing import Any, Dict

products_bp = Blueprint("products", __name__, url_prefix="/products")

# Página HTML de productos
@products_bp.route("/web", methods=["GET"])
def product_form() -> Any:
    products = Product.query.all()
    return render_template("products.html", products=products)

# Obtener todos los productos (JSON)
@products_bp.route("/", methods=["GET"])
def get_products() -> Any:
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock
        } for p in products
    ]), 200

# Crear nuevo producto
@products_bp.route("/", methods=["POST"])
def create_product() -> Any:
    data: Dict[str, Any] = request.form if request.form else request.get_json()

    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock", 0)

    if not name or not price:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    product = Product(name=name, price=float(price), stock=int(stock))
    db.session.add(product)
    db.session.commit()

    if request.form:
        return render_template("products.html", products=Product.query.all())

    return jsonify({"message": "Producto creado", "id": product.id}), 201
