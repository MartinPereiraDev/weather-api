from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

latitude=40.7128  # lat of New York
longitude=-74.0060  # lon of New York

def obtener_datos_meteo(lat=latitude, lon=longitude):
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
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    # Obtener datos de Nueva York por defecto
    datos = obtener_datos_meteo()
    if datos:
        # Preparar datos para el gráfico
        horas = datos['hourly']['time']
        temperaturas = datos['hourly']['temperature_2m']
        return render_template('index.html', 
                             horas=json.dumps(horas),
                             temperaturas=json.dumps(temperaturas))
    else:
        return "Error al obtener datos de la API."

if __name__ == '__main__':
    app.run(debug=True)