# Weather ETL & Power BI Dashboard (Open-Meteo)

This project demonstrates an end-to-end data analytics workflow:
Open-Meteo API → Python ETL → Star Schema → Power BI Dashboard.

## Objective
To showcase practical Data Analyst skills including:
- API data extraction using Python
- JSON normalization and transformation using Pandas
- Data cleaning and validation
- Star schema modeling
- Interactive Power BI reporting

## Data Source
- Open-Meteo Historical Weather API
- Cities: Muscat, Dubai, London, New York, Mumbai
- Period: Last ~90 days

## ETL Pipeline
1. Extract weather data from API using latitude and longitude
2. Transform data using Pandas (cleaning, dtype conversion, validation)
3. Load analytics-ready tables for Power BI

## Project Structure
src/
config.py
extract.py
transform.py
load.py
main.py

## Power BI Dashboard
Pages included:
1. Overview
2. Temperature Analysis
3. Rain and Wind
4. Data Quality & Pipeline

## Technologies Used
- Python (Pandas, Requests)
- REST API
- Power BI
- Star Schema Design