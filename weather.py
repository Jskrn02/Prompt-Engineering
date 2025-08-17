import requests
import datetime

# ========== Configuration ==========
API_KEY = "53f035b79901ff59c9893302003d01c7"  # 🔑 Replace with your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"  # 5-day forecast API
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"  # Current weather
UNITS = "metric"  # or 'imperial'

# ========== Functions ==========

def get_current_weather(city):
    """Fetches current weather data from OpenWeatherMap"""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': UNITS
    }
    response = requests.get(CURRENT_URL, params=params)
    response.raise_for_status()
    return response.json()


def get_forecast(city):
    """Fetches 5-day forecast data from OpenWeatherMap"""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': UNITS
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()


def display_current_weather(data):
    """Prints current weather in a readable format"""
    print("\n🌤️ CURRENT WEATHER:")
    print(f"City: {data['name']}")
    print(f"Temperature: {data['main']['temp']}°C")
    print(f"Condition: {data['weather'][0]['description'].title()}")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Wind Speed: {data['wind']['speed']} m/s")


def display_forecast(data):
    """Prints 5-day forecast in 3-hour intervals"""
    print("\n📅 5-DAY FORECAST:")
    for entry in data['list']:
        dt = datetime.datetime.fromtimestamp(entry['dt'])
        temp = entry['main']['temp']
        condition = entry['weather'][0]['description'].title()
        print(f"{dt.strftime('%a %d %b %I:%M %p')} | {temp}°C | {condition}")


def main():
    print("🌦️ Live Weather Forecast App")
    city = input("Enter city name: ")

    try:
        current = get_current_weather(city)
        forecast = get_forecast(city)

        display_current_weather(current)
        display_forecast(forecast)

    except requests.exceptions.HTTPError as err:
        print(f"❌ Error fetching weather data: {err}")
    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()