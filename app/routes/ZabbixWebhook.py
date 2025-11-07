# app/routes/ZabbixWebhook.py

from pymongo import MongoClient
from flask import Blueprint, request, jsonify
from ..config import Config
from datetime import datetime

# Conexión a Mongo
client = MongoClient(Config.MONGO_URI)
db = client["vuelosDB"]
alerts_collection = db["alerts"]

# Blueprint
zabbix_bp = Blueprint("zabbix", __name__, url_prefix="/zabbix")

# Endpoint para recibir alertas desde Zabbix
@zabbix_bp.route("/webhook", methods=["POST"])
def receive_zabbix_alert():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibió JSON"}), 400

        # Extraer datos esperados
        trigger_name = data.get("trigger") or data.get("trigger_name")
        status = data.get("status")
        severity = data.get("severity")
        hostname = data.get("hostname")
        event_time = data.get("datetime") or datetime.utcnow().isoformat()

        # Construir documento limpio
        alert_doc = {
            "trigger": trigger_name,
            "status": status,
            "severity": severity,
            "hostname": hostname,
            "datetime": event_time,
            "raw": data,  # Guarda todo por si luego lo necesitas
        }

        # Insertar en Mongo
        alerts_collection.insert_one(alert_doc)
        print(f"[ZABBIX ALERT] {trigger_name} ({status}, sev: {severity})")

        return jsonify({
            "received": True,
            "message": "Alerta guardada correctamente",
            "alert": alert_doc
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para consultar alertas (para frontend)
@zabbix_bp.route("/alerts", methods=["GET"])
def get_alerts():
    try:
        alerts = list(alerts_collection.find({}, {"_id": 0}))
        return jsonify(alerts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
