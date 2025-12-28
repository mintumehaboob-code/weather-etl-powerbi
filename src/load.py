import os
import pandas as pd
from sqlalchemy import create_engine
def ensure_dirs():
    os.makedirs("data/processed",exist_ok=True)
    os.makedirs("data/audit", exist_ok=True)
    os.makedirs("db", exist_ok=True)
def save_csv(df:pd.DataFrame,path:str):
    df.to_csv(path, index=False, encoding="utf-8")
def save_excel(dfs: dict, path: str):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for sheet, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet[:31], index=False)
def save_sqlite(dfs: dict, sqlite_path: str = "db/weather.sqlite"):
    engine = create_engine(f"sqlite:///{sqlite_path}")
    for table_name, df in dfs.items():
        df.to_sql(table_name, engine, if_exists="replace", index=False)