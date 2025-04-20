# app.py
from flask import Flask
from config import settings
from core.db import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Importar y registrar blueprints después de init_app
    # from features.products.routes import products_bp
    # app.register_blueprint(products_bp)
    from features.products.routes import products_bp
    app.register_blueprint(products_bp)



    @app.route("/")
    def index():
        return "Servidor Flask funcionando."

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=settings.DEBUG)