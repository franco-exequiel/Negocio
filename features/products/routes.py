from flask import Blueprint, request, jsonify, render_template
from core.db import db
from features.products.models import Product
from typing import Any, Dict
from .schemas import ProductCreate

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
def create_product():
    try:
        data = request.form.to_dict()
        validated = ProductCreate(**data)

        product = Product(
            name=validated.name,
            price=validated.price,
            stock=validated.stock,
        )
        db.session.add(product)
        db.session.commit()

        return jsonify({"message": "Producto creado exitosamente."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
