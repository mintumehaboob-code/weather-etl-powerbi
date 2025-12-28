from dataclasses import dataclass
from datetime import date, timedelta

CITIES = [
    "Muscat",
    "Dubai",
    "London",
    "New York",
    "Mumbai",
]

# Last 90 days is a great portfolio range (enough trend, still fast)
END_DATE = date.today()
START_DATE = END_DATE - timedelta(days=90)

@dataclass(frozen=True)
class ApiConfig:
    geocoding_base_url: str = "https://geocoding-api.open-meteo.com/v1/search"
    historical_base_url: str = "https://archive-api.open-meteo.com/v1/archive"  # historical endpoint :contentReference[oaicite:4]{index=4}
    timezone: str = "auto"  # Open-Meteo supports timezone=auto :contentReference[oaicite:5]{index=5}

API = ApiConfig()
