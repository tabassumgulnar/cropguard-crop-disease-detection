"""
CropGuard Weather Risk Engine
Fetches real-time temperature, relative humidity, and precipitation from Open-Meteo API (no API key required)
and computes rule-based agro-meteorological fungal and pest disease proliferation risks.
"""

from typing import Dict, Any, Tuple
import requests

OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_current_weather(latitude: float, longitude: float, timeout: int = 5) -> Dict[str, Any]:
    """
    Fetches real-time weather parameters from Open-Meteo API.
    Returns dictionary with temperature, humidity, precipitation, and status.
    Gracefully falls back to representative agro-climatic defaults if offline or network fails.
    """
    params = {
        "latitude": round(latitude, 4),
        "longitude": round(longitude, 4),
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "weather_code", "wind_speed_10m"],
        "timezone": "auto",
        "forecast_days": 1,
    }

    try:
        response = requests.get(OPEN_METEO_BASE_URL, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        current = data.get("current", {})

        temp = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        precip = current.get("precipitation", 0.0)
        wind_speed = current.get("wind_speed_10m", 0.0)
        weather_code = current.get("weather_code", 0)

        return {
            "success": True,
            "source": "Open-Meteo Live API",
            "temperature": round(float(temp), 1) if temp is not None else 26.5,
            "humidity": round(float(humidity), 1) if humidity is not None else 72.0,
            "precipitation": round(float(precip), 2) if precip is not None else 0.0,
            "wind_speed": round(float(wind_speed), 1) if wind_speed is not None else 8.5,
            "weather_code": weather_code,
            "error": None,
        }
    except Exception as e:
        # Fallback for offline mode or network timeouts
        return {
            "success": False,
            "source": "Offline Fallback (Historical Norm)",
            "temperature": 27.0,
            "humidity": 68.0,
            "precipitation": 0.0,
            "wind_speed": 10.0,
            "weather_code": 0,
            "error": f"Live weather unavailable ({str(e)}). Using standard agro-climatic seasonal reference.",
        }


def compute_disease_weather_risk(
    temperature: float,
    humidity: float,
    precipitation: float,
    crop: str = "tomato",
) -> Tuple[str, str, Dict[str, Any]]:
    """
    Computes rule-based fungal and vector pest disease proliferation risk.

    Scientific Agro-Meteorological Rationale:
    - Fungal pathogens (Early Blight, Late Blight, Purple Blotch, Downy Mildew)
      require free leaf moisture or sustained relative humidity (>75-80%)
      and moderate temperatures (16°C - 30°C) for spore germination.
    - Sucking pests (whiteflies transmitting leaf curl virus, thrips) thrive
      in warm, drier spells (26°C - 35°C, RH 40-70%) with low rainfall that doesn't wash nymphs away.
    - Bacterial blight expands rapidly during humid, warm conditions (25-32°C, RH >80%)
      accompanied by wind-driven rain splashes.

    Returns:
        level: "High", "Medium", or "Low"
        explanation: Detailed rationale in clear language
        metrics: Detailed sub-scores
    """
    fungal_score = 0
    pest_score = 0
    factors = []

    # 1. Moisture & Humidity Analysis
    if humidity >= 85.0 or (humidity >= 75.0 and precipitation > 0.5):
        fungal_score += 4
        factors.append(f"Very high moisture (RH {humidity}%, Rain {precipitation}mm) causes sustained leaf wetness ideal for fungal spore germination.")
    elif humidity >= 70.0:
        fungal_score += 2
        factors.append(f"Moderate-high relative humidity ({humidity}%) creates favorable microclimate for foliar pathogens.")
    elif humidity < 50.0:
        fungal_score -= 1
        factors.append(f"Dry ambient air ({humidity}% RH) inhibits fungal sporulation.")

    # 2. Temperature Analysis for Fungi (Blite/Mildew)
    if 18.0 <= temperature <= 28.0:
        fungal_score += 3
        factors.append(f"Optimal temperature ({temperature}°C) for vegetative fungal mycelium proliferation.")
    elif 14.0 <= temperature < 18.0 or 28.0 < temperature <= 32.0:
        fungal_score += 1
        factors.append(f"Permissive temperature ({temperature}°C) supporting moderate pathogen incubation.")
    else:
        fungal_score -= 2
        factors.append(f"Temperature extremes ({temperature}°C) restrict most fungal life-cycles.")

    # 3. Pest / Vector (Whitefly / Caterpillar) Analysis
    if 25.0 <= temperature <= 35.0 and humidity <= 70.0 and precipitation < 1.0:
        pest_score += 3
        factors.append(f"Warm and relatively dry conditions ({temperature}°C, {humidity}% RH) favor rapid reproduction of whitefly and thrip disease vectors.")
    elif temperature >= 22.0 and precipitation < 2.0:
        pest_score += 1

    # Combined assessment
    total_score = fungal_score + (1 if pest_score >= 2 else 0)

    if total_score >= 5 or (fungal_score >= 4 and precipitation > 1.0):
        level = "High"
        color = "red"
        action_advice = "Crucial window: Fungal blight and leaf spot risks are elevated. Inspect lower canopy, check leaf undersides, avoid evening sprinkler irrigation, and keep biological bio-protectants ready."
    elif total_score >= 2 or pest_score >= 2:
        level = "Medium"
        color = "orange"
        action_advice = "Moderate risk: Weather permits steady pathogen and pest incubation. Conduct routine scouting, keep sticky traps active, and ensure plant canopy remains well ventilated."
    else:
        level = "Low"
        color = "green"
        action_advice = "Low climatic risk: Current ambient weather does not favor immediate fungal disease outbreaks. Continue standard cultural farm management."

    explanation = " ".join(factors) + " " + action_advice

    return level, explanation, {
        "fungal_score": fungal_score,
        "pest_score": pest_score,
        "color": color,
        "action_advice": action_advice,
    }


if __name__ == "__main__":
    weather = get_current_weather(18.5204, 73.8567)  # Pune
    print("Weather at Pune:", weather)
    risk, expl, details = compute_disease_weather_risk(
        weather["temperature"], weather["humidity"], weather["precipitation"]
    )
    print(f"Risk: {risk}\nExplanation: {expl}")
