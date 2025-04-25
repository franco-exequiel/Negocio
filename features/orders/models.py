from core.db import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="orders")  # ✅ genera user.orders
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(db.Model):
    __tablename__ = "order_items"

    id: int = db.Column(db.Integer, primary_key=True)
    order_id: int = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id: int = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity: int = db.Column(db.Integer, default=1)

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product")
