import requests

def readWeatherAPI():
    # Example: Pandharpur, Maharashtra
    lat = 17.68
    lon = 75.32

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m"
    )

    response = requests.get(url, timeout=5)
    data = response.json()

    temp = data["current"]["temperature_2m"]
    humidity = data["current"]["relative_humidity_2m"]

    # Simulated soil moisture (0–100 scale)
    moisture = max(10, min(90, 100 - humidity))

    return temp, humidity, moisture


#print(readWeatherAPI())