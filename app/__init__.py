# app/__init__.py
from flask import Flask
from flask_cors import CORS

from .config import Config
from flask_pymongo import PyMongo
from flask_apscheduler import APScheduler
from app.services.open_sky_client import get_flights_over_cdmx
from .services.db_manager import save_flights

mongo = PyMongo()
scheduler = APScheduler()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa Mongo
    mongo.init_app(app)

    app.mongo = mongo

    # Importa rutas aquí (para evitar importaciones circulares)
    from .routes.FlightsRoutes import flights_bp
    from .routes.MetricsRoutes import metrics_bp
    from .routes.HealthRoutes import health_bp
    from .routes.ZabbixWebhook import zabbix_bp

    app.register_blueprint(flights_bp)
    app.register_blueprint(metrics_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(zabbix_bp)

    CORS(app)
    # Agrega el job una sola vez
    if not scheduler.running:
        scheduler.init_app(app)
        scheduler.add_job(
            id='RetrieveFlights',
            func=job_retrieve_flights,
            trigger='interval',
            seconds=30
        )
        scheduler.start()


    return app

def job_retrieve_flights():
    print("🛰️ Consultando vuelos...")
    flights = get_flights_over_cdmx()
    # Guarda en base de datos

    save_flights(flights)
    print(f"{len(flights)} vuelos guardados correctamente")