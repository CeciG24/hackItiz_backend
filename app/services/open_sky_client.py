import requests
from datetime import datetime

from requests.auth import HTTPBasicAuth

OPEN_SKY_URL = "https://opensky-network.org/api/states/all"
CDMX_PARAMS = {
    "lamin": 19.2,
    "lomin": -99.3,
    "lamax": 19.6,
    "lomax": -98.9
}

def get_flights_over_cdmx():
    """Obtiene vuelos activos sobre CDMX desde OpenSky"""
    try:
        response = requests.get(OPEN_SKY_URL, params=CDMX_PARAMS,  auth=HTTPBasicAuth('ianarce-api-client', 'LPTPJviWRxciCcUbpLvjST47mAbml1Zq'),timeout=15)
        response.raise_for_status()
        data = response.json()

        if not data or "states" not in data:
            return []

        flights = []
        for state in data["states"]:
            flights.append({
                "icao24": state[0],
                "callsign": state[1].strip() if state[1] else None,
                "origin_country": state[2],
                "last_contact": datetime.utcfromtimestamp(state[4]),
                "longitude": state[5],
                "latitude": state[6],
                "baro_altitude": state[7],
                "on_ground": state[8],
                "velocity": state[9],
                "true_track": state[10],
                "vertical_rate": state[11],
                "geo_altitude": state[13],
                "squawk": state[14],
                "spi": state[15],
                "position_source": state[16],
                "timestamp": datetime.utcnow()
            })

        return flights
    except Exception as e:
        print(f"Error al consultar OpenSky: {e}")
        return []
