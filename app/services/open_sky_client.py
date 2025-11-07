import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime
from requests.auth import HTTPBasicAuth

OPEN_SKY_URL = "https://opensky-network.org/api/states/all"
CDMX_PARAMS = {
    "lamin": 19.2,
    "lomin": -99.3,
    "lamax": 19.6,
    "lomax": -98.9
}

USERNAME = "ianarce-api-client"
PASSWORD = "DDAJ9FSt8lFWKkbqXfPgTmnYJctpzafd"

def create_session():
    """Create a session with retry strategy"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,  # number of retries
        backoff_factor=1,  # wait 1, 2, 4 seconds between retries
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    return session

def get_flights_over_cdmx():
    """Obtiene vuelos activos sobre CDMX desde OpenSky, usando credenciales si están disponibles"""
    try:
        session = create_session()
        
        # Intentamos con autenticación
        response = session.get(
            OPEN_SKY_URL,
            params=CDMX_PARAMS,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            timeout=30  # increased timeout to 30 seconds
        )

        # Si da 401 (credenciales incorrectas), caemos a acceso anónimo
        if response.status_code == 401:
            print("Credenciales inválidas, usando acceso anónimo")
            response = session.get(
                OPEN_SKY_URL, 
                params=CDMX_PARAMS, 
                timeout=30
            )

        response.raise_for_status()
        data = response.json()

        # ... rest of the existing code ...
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
