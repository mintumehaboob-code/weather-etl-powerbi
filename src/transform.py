import re
import pandas as pd
from typing import Dict,Any,Optional
def clean_columns(df:pd.DataFrame)-> pd.DataFrame:
    df=df.copy()
    df.columns=(df.columns.astype(str)
                .str.strip()
                .str.lower()
                .str.replace(".","_",regex=False)
                .str.replace(r"\s","_",regex=True)
                .str.replace(r"[^a-z0-9_]","",regex=True)
                .str.replace(r"_+","_",regex=True)
                .str.strip("_")
    )
    return df
def build_daily_fact(city_row:Dict[str,Any],weather_json :Dict[str,Any])->pd.DataFrame:
     """
    Open-Meteo historical API returns daily arrays like:
    daily: { time: [...], temperature_2m_max: [...], ... } :contentReference[oaicite:8]{index=8}
    We'll convert those arrays into rows.
    """
     daily=weather_json.get("daily")or {}
     df=pd.DataFrame(daily)
     # Add city metadata columns (for joining later)
     df["city_name"]=city_row.get("name")
     df["country"]=city_row.get("country")
     df["latitude"]=city_row.get("latitude")
     df["longitude"]=city_row.get("longitude")
     df=clean_columns(df)
     #Coerce types
     df["time"]=pd.to_datetime(df["time"],errors="coerce")
     for col in ["temperature_2m_max","temperature_2m_min","precipitation_sum", "windspeed_10m_max"]:
          df[col]=pd.to_numeric(df[col],errors="coerce")
     return df
def remove_duplicates(df:pd.DataFrame)->pd.DataFrame:
     df=df.copy()
     df=df.sort_values(['city_name','time'])
     df=df.drop_duplicates(subset=["city_name","time"],keep="last")
     return df
def audit_invalid_rows(df:pd.DataFrame) -> tuple[pd.DataFrame,pd.DataFrame]:
      """
    Returns:
      - clean_df: rows with valid time
      - audit_df: rows with missing time or all metrics missing
    """
      df=df.copy()
      #invalid time
      bad_time=df[df["time"].isna()].assign(error_reason="invalid_or_missing_date")
      # all metrics missing (after coercion)
      metric_cols=["temperature_2m_max","temperature_2m_min","precipitation_sum", "windspeed_10m_max"]
      bad_metrics=df[df[metric_cols].isna().all(axis=1)].assign(error_mssage="all_metrics_missing")

      audit_df=pd.concat([bad_time,bad_metrics],ignore_index=True).drop_duplicates()
      clean_df=df.drop(index=audit_df.index,errors="ignore")
      return clean_df,audit_df
def make_star_schema(fact_daily:pd.DataFrame)->pd.DataFrame:
     """
    Build dim_city, dim_date, fact_weather_daily
    """
     fact=fact_daily.copy()
     #dim city
     dim_city=(fact[["city_name","country","latitude","longitude"]].drop_duplicates().reset_index(drop=True))
     dim_city["city_id"]=dim_city.index+1
     #dim date
     dim_date=pd.DataFrame({"date":pd.to_datetime(fact['time']).dt.normalize().dropna().unique()}).sort_values('date').reset_index(drop=True)
     dim_date["date_id"]=dim_date.index+1
     dim_date["year"]=dim_date['date'].dt.year
     dim_date["month"]=dim_date["date"].dt.month
     dim_date['month_name']=dim_date['date'].dt.month_name()
     dim_date["day"] = dim_date["date"].dt.day
     #fact table
     fact=fact.merge(dim_city,on=['city_name','country','latitude','longitude'],how="left")
     fact["date"]=pd.to_datetime(fact["time"]).dt.normalize()
     fact=fact.merge(dim_date[["date_id","date"]],on="date",how="left")
     fact_weather_daily=fact[["date_id","city_id","temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "windspeed_10m_max",]].copy()
     return dim_city, dim_date, fact_weather_daily


     


