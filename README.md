# 🛒 Negocio – Sistema de Gestión con Flask

Este proyecto es un sistema de gestión modular desarrollado con **Python + Flask**, que incluye manejo de **usuarios**, **productos** y **órdenes**.  
Cuenta con una API RESTful y un frontend simple con HTML para pruebas.

---

## 🚀 Tecnologías usadas

- Python 3.10+
- Flask (con Blueprints)
- SQLAlchemy (ORM)
- PostgreSQL
- HTML + Jinja2 (frontend básico)
- Git + GitHub
- (Opcional) Ngrok para test de endpoints externos

---

## 📂 Estructura del proyecto
Negocio/ 
├── app.py 
├── core/ 
│ ├── config.py 
│ ├── db.py 
│ └── init_db.py 
├── features/ 
│ ├── users/ 
│ │ ├── models.py 
│ │ └── routes.py 
│ ├── products/ 
│ │ ├── models.py 
│ │ └── routes.py 
│ └── orders/ 
│ ├── models.py 
│ └── routes.py 
├── templates/ 
│ ├── base.html 
│ ├── index.html 
│ ├── users.html 
│ ├── products.html 
│ └── orders.html 
├── .env.example 
└── requirements.txt



📦 Instalación y setup
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos
python -m core.init_db

# Iniciar el servidor
python app.py




🌐 Rutas disponibles
_______________________________________________________________
📋 Usuarios
Método	  Ruta	         Descripción
GET	      /users/	       Obtener usuarios (JSON)
POST	    /users/	       Crear usuario
GET	      /users/web     Formulario HTML
_______________________________________________________________
📦 Productos
Método	      Ruta	          Descripción
GET	          /products/	    Obtener productos (JSON)
POST	        /products/	    Crear producto
GET	          /products/web	  Formulario HTML
_______________________________________________________________
📦 Órdenes
Método	       Ruta	          Descripción
GET	           /orders/	      Obtener órdenes (JSON)
POST	         /orders/	      Crear orden
GET	           /orders/web	  Formulario HTML
_______________________________________________________________


🏷️ Versión actual
v1.0.0 – Backend y frontend mínimo funcional con integración a base de datos.

📌 TODOs futuros

-Autenticación de usuarios
-Panel de administración
-Exportar datos a CSV/PDF
-Bot de WhatsApp (sección en pausa)

👤 Autor
Franco Exequiel
Licencia: MIT
