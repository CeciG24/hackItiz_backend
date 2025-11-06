# app/__init__.py
from flask import Flask
from .config import Config
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa Mongo
    mongo.init_app(app)

    # Importa rutas aquí (para evitar importaciones circulares)
    from .routes.FlightsRoutes import flights_bp
    app.register_blueprint(flights_bp)

    return app
