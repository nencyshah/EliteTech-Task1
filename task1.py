# Weather Forecast Visualization using OpenWeatherMap API and Seaborn
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Define City and API Key
print("Weather Forecast Visualization using OpenWeatherMap API and Seaborn")

city_name = 'Gujrat'
API_KEY = "1c03d876de9a8d3b6945e66313bdc489"

# Use the CORRECT Forecast API
url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&appid={API_KEY}'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Extract weather forecast data
    dates = []
    temps = []
    humidity = []
    wind_speed = []

    for entry in data["list"]:
        dates.append(datetime.datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S"))
        temps.append(entry["main"]["temp"])
        humidity.append(entry["main"]["humidity"])
        wind_speed.append(entry["wind"]["speed"])

    # Set Seaborn style
    sns.set_theme(style="darkgrid")

    # Create a figure with multiple subplots
    fig, axes = plt.subplots(3, 1, figsize=(10, 12))

    # Temperature Plot
    sns.lineplot(x=dates, y=temps, ax=axes[0], marker="o", color="red")
    axes[0].set_title("Temperature Forecast")
    axes[0].set_ylabel("Temperature (°C)")

    # Humidity Plot
    sns.lineplot(x=dates, y=humidity, ax=axes[1], marker="o", color="blue")
    axes[1].set_title("Humidity Forecast")
    axes[1].set_ylabel("Humidity (%)")

    # Wind Speed Plot
    sns.lineplot(x=dates, y=wind_speed, ax=axes[2], marker="o", color="green")
    axes[2].set_title("Wind Speed Forecast")
    axes[2].set_ylabel("Wind Speed (m/s)")

    # Rotate x-axis labels
    for ax in axes:
        ax.set_xlabel("Date & Time")
        ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()

else:
    print(f"Failed to fetch weather data. HTTP Status Code: {response.status_code}")
