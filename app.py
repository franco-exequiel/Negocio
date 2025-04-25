# app.py
from flask import Flask,render_template
from core.config import settings
from core.db import db

def create_app():

    app = Flask(__name__, template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Importar y registrar blueprints después de init_app
    #########################################################
    # from features.products.routes import products_bp      #
    # app.register_blueprint(products_bp)                   #
    #########################################################
    from features.products.routes import products_bp
    from features.users.routes import users_bp
    from features.orders.routes import orders_bp

    app.register_blueprint(products_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(orders_bp)


    

    @app.route("/")
    def home():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=settings.DEBUG)