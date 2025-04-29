from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Lista de países con coordenadas (personalizable)
PAISES = [
    {"nombre": "Nueva York", "lat": 40.7128, "lon": -74.0060},
    {"nombre": "Londres", "lat": 51.5074, "lon": -0.1278},
    {"nombre": "Tokio", "lat": 35.6762, "lon": 139.6503},
    {"nombre": "París", "lat": 48.8566, "lon": 2.3522},
    {"nombre": "Sídney", "lat": -33.8688, "lon": 151.2093}
]

def obtener_datos_meteo(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "timezone": "auto",
        "forecast_days": 1
    }
    try:
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None
    except:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    # País seleccionado (por defecto: primer país de la lista)
    pais_seleccionado = PAISES[0]
    
    if request.method == 'POST':
        # Obtener el índice del país seleccionado del formulario
        indice = int(request.form['pais'])
        pais_seleccionado = PAISES[indice]
    
    # Obtener datos meteorológicos
    datos = obtener_datos_meteo(pais_seleccionado["lat"], pais_seleccionado["lon"])
    
    if datos:
        return render_template('index.html',
            horas=json.dumps(datos['hourly']['time']),
            temperaturas=json.dumps(datos['hourly']['temperature_2m']),
            paises=PAISES,
            indice_seleccionado=PAISES.index(pais_seleccionado)
        )
    else:
        return "Error al obtener datos."
    
if __name__ == '__main__':
    app.run(debug=True)