# features/products/routes.py

from flask import Blueprint, request, jsonify
from core.db import db
from features.products.models import Product
from typing import Any, Dict

products_bp = Blueprint("products", __name__, url_prefix="/products")

# Obtener todos los productos
@products_bp.route("/", methods=["GET"])
def get_products() -> Any:
    products = Product.query.all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "description": p.description,
        "stock": p.stock
    } for p in products]), 200

# Obtener un solo producto por ID
@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id: int) -> Any:
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "stock": product.stock
    }), 200

# Crear nuevo producto
@products_bp.route("/", methods=["POST"])
def create_product() -> Any:
    data: Dict[str, Any] = request.get_json()

    if not data or not data.get("name") or not data.get("price"):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    new_product = Product(
        name=data["name"],
        price=data["price"],
        description=data.get("description", ""),
        stock=data.get("stock", 0)
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Producto creado", "id": new_product.id}), 201

# Actualizar producto existente
@products_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id: int) -> Any:
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    data: Dict[str, Any] = request.get_json()

    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.description = data.get("description", product.description)
    product.stock = data.get("stock", product.stock)

    db.session.commit()
    return jsonify({"message": "Producto actualizado"}), 200

# Eliminar producto
@products_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int) -> Any:
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Producto eliminado"}), 200