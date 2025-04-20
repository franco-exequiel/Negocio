# core/db.py
from flask_sqlalchemy import SQLAlchemy


#Sólo inicializa el ORM y se importa desde .app.py
db = SQLAlchemy()
