import requests
from typing import Dict,Any,Optional
from.config import API
def geocode_city(city:str,count:int=1)->Optional[Dict[str,Any]]:
    """
    Calls Open-Meteo Geocoding API: returns best match with lat/lon/country.
    Docs: https://open-meteo.com/en/docs/geocoding-api :contentReference[oaicite:6]{index=6}
    """
    params={
        'name':city,
        'count':count,
        'language':"en",
        "format":"json"
        }
    r=requests.get(API.geocoding_base_url,params=params,timeout=30)
    data=r.json()
    results=data.get("results") or []
    if not results:
        return None
    return results[0]
def fetch_historical_daily(lat:float,lon:float,start_date:str,end_date:str):
    """
    Calls Open-Meteo Historical Weather API (/v1/archive). :contentReference[oaicite:7]{index=7}
    Returns daily weather variables for a coordinate.
    """
    params={
        "latitude":lat,
        "longitude":lon,
        "start_date":start_date,
        "end_date":end_date,
        "timezone":API.timezone,
        "daily":",".join(["temperature_2m_max",
                          "temperature_2m_min",
                           "precipitation_sum",
                           "windspeed_10m_max",])
    }
    r=requests.get(API.historical_base_url,params=params,timeout=30)
    r.raise_for_status()
    return r.json()
    
