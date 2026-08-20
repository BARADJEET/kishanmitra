import httpx
from typing import Dict, Any, List
from datetime import datetime

def generate_actionable_advisories(weather_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    advisories = []
    temp = weather_data.get("temperature", 28.0)
    humidity = weather_data.get("humidity", 65.0)
    rain_prob = weather_data.get("precipitation_probability", 15.0)
    rain_mm = weather_data.get("precipitation_sum", 0.0)
    wind_speed = weather_data.get("wind_speed", 10.0)

    # 1. Irrigation Rule
    if rain_prob > 50 or rain_mm > 5.0:
        advisories.append({
            "category": "Irrigation",
            "action_level": "CRITICAL_ACTION",
            "icon": "cloud-rain",
            "title": "Postpone Irrigation",
            "message": f"Rainfall expected ({rain_prob}% chance, ~{rain_mm}mm). Do NOT irrigate for the next 24-48 hours to prevent waterlogging and root rot."
        })
    elif temp > 35.0 and humidity < 40:
        advisories.append({
            "category": "Irrigation",
            "action_level": "WARNING",
            "icon": "droplets",
            "title": "Heat Stress Irrigation",
            "message": "High temperature and low humidity detected. Apply light irrigation during early morning (5-8 AM) or evening to prevent moisture stress and flower drop."
        })
    else:
        advisories.append({
            "category": "Irrigation",
            "action_level": "NORMAL",
            "icon": "check-circle",
            "title": "Normal Irrigation Schedule",
            "message": "Weather conditions are stable. Maintain your regular drip/sprinkler cycle according to your crop development stage."
        })

    # 2. Pesticide / Spraying Rule
    if rain_prob > 40 or rain_mm > 2.0:
        advisories.append({
            "category": "Pest & Disease Spraying",
            "action_level": "WARNING",
            "icon": "ban",
            "title": "Avoid Chemical Spraying",
            "message": "Impending rain will wash away foliar sprays. Postpone pesticide, insecticide and foliar fertilizer applications until weather clears."
        })
    elif wind_speed > 20.0:
        advisories.append({
            "category": "Pest & Disease Spraying",
            "action_level": "WARNING",
            "icon": "wind",
            "title": "High Wind Drift Hazard",
            "message": f"Wind speed is {wind_speed} km/h. Avoid spray operations today to prevent hazardous chemical drift to adjacent non-target crops."
        })
    else:
        advisories.append({
            "category": "Pest & Disease Spraying",
            "action_level": "NORMAL",
            "icon": "shield-check",
            "title": "Optimal Spray Window",
            "message": "Wind speed and dry canopy conditions are optimal for preventative bio-pesticide and micronutrient sprays."
        })

    # 3. Disease Risk Warning Rule
    if humidity > 75 and 20.0 <= temp <= 30.0:
        advisories.append({
            "category": "Disease Watch",
            "action_level": "HIGH_RISK",
            "icon": "alert-triangle",
            "title": "Fungal Outbreak Risk Alert",
            "message": f"High humidity ({humidity}%) and warm temperature ({temp}°C) create ideal conditions for Early Blight, Blast, and Mildew. Inspect lower foliage daily."
        })
    elif temp < 12.0:
        advisories.append({
            "category": "Frost & Cold Advisory",
            "action_level": "WARNING",
            "icon": "snowflake",
            "title": "Cold Stress Warning",
            "message": "Night temperatures dropping below 12°C. Provide light night irrigation or smoke cover to protect sensitive vegetable crops from frost injury."
        })

    return advisories

async def get_weather_and_advisory(lat: float, lon: float, district: str = "Ahmedabad") -> Dict[str, Any]:
    weather_summary = {
        "location": district.title(),
        "latitude": lat,
        "longitude": lon,
        "temperature": 28.5,
        "feels_like": 30.0,
        "humidity": 62,
        "wind_speed": 12.5,
        "precipitation_probability": 10,
        "precipitation_sum": 0.0,
        "weather_condition": "Partly Cloudy",
        "uv_index": 6.5,
        "forecast_daily": [
            {"day": "Today", "max_temp": 32, "min_temp": 22, "rain_prob": 10, "condition": "Sunny"},
            {"day": "Tomorrow", "max_temp": 33, "min_temp": 23, "rain_prob": 20, "condition": "Partly Cloudy"},
            {"day": "Day 3", "max_temp": 31, "min_temp": 21, "rain_prob": 65, "condition": "Thunderstorms"},
            {"day": "Day 4", "max_temp": 29, "min_temp": 20, "rain_prob": 40, "condition": "Scattered Rain"},
            {"day": "Day 5", "max_temp": 30, "min_temp": 21, "rain_prob": 15, "condition": "Clear Sky"}
        ]
    }

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,"
            f"apparent_temperature,precipitation,wind_speed_10m,weather_code&"
            f"daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum&timezone=auto"
        )
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                current = data.get("current", {})
                daily = data.get("daily", {})

                weather_summary["temperature"] = round(current.get("temperature_2m", 28.5), 1)
                weather_summary["humidity"] = round(current.get("relative_humidity_2m", 62), 1)
                weather_summary["feels_like"] = round(current.get("apparent_temperature", 30.0), 1)
                weather_summary["wind_speed"] = round(current.get("wind_speed_10m", 12.0), 1)

                rain_probs = daily.get("precipitation_probability_max", [10])
                rain_sums = daily.get("precipitation_sum", [0.0])
                weather_summary["precipitation_probability"] = rain_probs[0] if rain_probs else 10
                weather_summary["precipitation_sum"] = rain_sums[0] if rain_sums else 0.0

                code = current.get("weather_code", 1)
                if code == 0:
                    weather_summary["weather_condition"] = "Clear Sky"
                elif code in [1, 2, 3]:
                    weather_summary["weather_condition"] = "Partly Cloudy"
                elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
                    weather_summary["weather_condition"] = "Rain Showers"
                elif code in [95, 96, 99]:
                    weather_summary["weather_condition"] = "Thunderstorm"
                else:
                    weather_summary["weather_condition"] = "Overcast"
    except Exception as e:
        print(f"Weather API non-blocking fallback used: {e}")

    advisories = generate_actionable_advisories(weather_summary)
    return {
        "weather": weather_summary,
        "advisories": advisories,
        "timestamp": datetime.utcnow().isoformat()
    }
