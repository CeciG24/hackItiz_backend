from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from .config import Config

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar Mongo
    mongo.init_app(app)

    from .routes.FlightsRoutes import flights_bp
    
    #Agregar el Blueprint
    app.register_blueprint(flights_bp)
    
    CORS(app)
    return app