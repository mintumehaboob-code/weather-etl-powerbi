import json
import os
from datetime import date
import pandas as pd

from .config import CITIES, START_DATE, END_DATE
from .extract import geocode_city, fetch_historical_daily
from .transform import build_daily_fact, remove_duplicates, audit_invalid_rows, make_star_schema
from .load import ensure_dirs, save_csv, save_excel, save_sqlite

def run():
    ensure_dirs()

    start_str = START_DATE.isoformat()
    end_str = END_DATE.isoformat()

    all_facts = []
    geo_rows = []

    for city in CITIES:
        city_row = geocode_city(city)
        if not city_row:
            print(f"[WARN] No geocode result for: {city}")
            continue

        geo_rows.append(city_row)

        lat = city_row["latitude"]
        lon = city_row["longitude"]

        weather_json = fetch_historical_daily(lat, lon, start_str, end_str)

        
        raw_path = f"data/raw/{city.replace(' ', '_').lower()}_{start_str}_to_{end_str}.json"
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(weather_json, f, ensure_ascii=False, indent=2)

        fact = build_daily_fact(city_row, weather_json)
        all_facts.append(fact)

    if not all_facts:
        raise RuntimeError("No data collected. Check API connectivity / city names.")

    fact_daily = pd.concat(all_facts, ignore_index=True)

    # Remove duplicates
    fact_daily = remove_duplicates(fact_daily)

    # Audit invalid rows
    fact_daily_clean, audit_df = audit_invalid_rows(fact_daily)

    # Star schema
    dim_city, dim_date, fact_weather_daily = make_star_schema(fact_daily_clean)

    # Save outputs
    save_csv(fact_daily_clean, "data/processed/fact_daily_clean.csv")
    save_csv(audit_df, "data/audit/audit_invalid_rows.csv")

    save_excel(
        {
            "dim_city": dim_city,
            "dim_date": dim_date,
            "fact_weather_daily": fact_weather_daily,
            "audit_invalid_rows": audit_df,
        },
        "data/processed/weather_star_schema.xlsx",
    )

    save_sqlite(
        {
            "dim_city": dim_city,
            "dim_date": dim_date,
            "fact_weather_daily": fact_weather_daily,
            "audit_invalid_rows": audit_df,
        }
    )

    print("✅ Done!")
    print("Outputs:")
    print("- db/weather.sqlite")
    print("- data/processed/fact_daily_clean.csv")
    print("- data/processed/weather_star_schema.xlsx")
    print("- data/audit/audit_invalid_rows.csv")

if __name__ == "__main__":
    run()
