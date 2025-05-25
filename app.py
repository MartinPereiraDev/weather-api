from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# cities = a list with coordinates (latitude and longitude)
CITIES = [
    {"name": "Nueva York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Londres", "lat": 51.5074, "lon": -0.1278},
    {"name": "Tokio", "lat": 35.6762, "lon": 139.6503},
    {"name": "París", "lat": 48.8566, "lon": 2.3522},
    {"name": "Sídney", "lat": -33.8688, "lon": 151.2093},
    {"name": "Madrid", "lat": 40.4168, "lon": -3.7038},
    {"name": "Berlín", "lat": 52.5200, "lon": 13.4050},
    {"name": "Roma", "lat": 41.9028, "lon": 12.4964},
    {"name": "Ciudad de México", "lat": 19.4326, "lon": -99.1332},
    {"name": "Buenos Aires", "lat": -34.6037, "lon": -58.3816},
    {"name": "Santiago", "lat": -33.4489, "lon": -70.6693},
    {"name": "Brasilia", "lat": -15.7801, "lon": -47.9292},
    {"name": "Caracas", "lat": 10.4812, "lon": -66.8602},
    {"name": "Montevideo", "lat": -34.9011, "lon": -56.1645},
    {"name": "Paysandu", "lat": -32.3171, "lon": -58.08072}
]

def get_data_meteo(lat, lon):
    """
    Retrieves weather data from the Open-Meteo API for a specific location.
    
    Args:
        lat (float): Latitude of the target location
        lon (float): Longitude of the target location
    
    Returns:
        dict or error: Dictionary containing weather data if the request is successful,
                      error message in case of errors or invalid response.
    
    Workflow:
        1. Sets up API query parameters
        2. Executes a GET request to the API endpoint
        3. Validates the HTTP response status
        4. Returns parsed JSON data or error message if unsuccessful
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation,relativehumidity_2m,windspeed_10m",
        "timezone": "auto",
        "forecast_days": 1
    }
    try:
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        # Log the error message 

        return print("Error: ", e)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Country selected by default
    selected_city = CITIES[13]
    
    if request.method == 'POST':
        # Get the selected city index from the form

        index = int(request.form['city'])
        selected_city = CITIES[index]
    
    # Get the weather data for the selected city
    data = get_data_meteo(selected_city["lat"], selected_city["lon"])
    
    if data:
        # Extract the data from the API response
        # Extract the hourly data for temperature, precipitation, humidity, and wind speed
        # Calculate summary statistics
        hours = data['hourly']['time']
        temperatures = data['hourly']['temperature_2m']
        precipitation = data['hourly']['precipitation']
        humidity = data['hourly']['relativehumidity_2m']
        winds = data['hourly']['windspeed_10m']

        # Calculate summary statistics
        # Calculate the maximum and minimum temperatures
        # Calculate the total precipitation
        # Calculate the maximum wind speed
        resume = {
            "temp_max": max(temperatures),
            "temp_min": min(temperatures),
            "precip_total": sum(precipitation),
            "winds_max": max(winds)
        }
        return render_template('index.html',
            hours=json.dumps(hours),
            temperatures=json.dumps(temperatures),
            precipitation=json.dumps(precipitation),
            humidity=json.dumps(humidity),
            winds=json.dumps(winds),
            resume=resume,
            cities=CITIES,
            indice_seleccionado=CITIES.index(selected_city),
        )
    else:
        return "Error obtaining weather data from API."
    
if __name__ == '__main__':
    app.run(debug=True)