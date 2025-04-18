import pandas as pd
from consts import ROOT_DIR
from pathlib import Path
from datetime import datetime

from db import get_engine


def prepare_origin_df_from_file(
    filedir: str | Path = Path(f"{ROOT_DIR}/saved_data/history/SZSE/"),
    filename="20250101.csv",
):
    origin_df = pd.read_csv(Path(filedir) / filename)
    return origin_df


def prepare_origin_df_from_db(startDate: datetime, endDate: datetime):
    """**endDate not included**"""
    origin_df = pd.read_sql(
        f"select * from original where date >= '{ startDate.strftime('%Y-%m-%d') }' AND date <= '{endDate.strftime('%Y-%m-%d')}'",
        get_engine(),
    )
    return origin_df
