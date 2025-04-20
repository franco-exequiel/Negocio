# features/products/models.py

from core.db import db
from typing import Optional

class Product(db.Model):
    __tablename__ = "products"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    price: float = db.Column(db.Float, nullable=False)
    description: Optional[str] = db.Column(db.Text)
    stock: int = db.Column(db.Integer, default=0)

    def __repr__(self) -> str:
        return f"<Product {self.name}>"