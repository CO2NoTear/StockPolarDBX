import pandas as pd
from config.configs import ROOT_DIR
from pathlib import Path


def prepare_origin_df(
    filedir: str | Path = Path(f"{ROOT_DIR}/saved_data/history/SZSE/"),
    filename="20250101.csv",
):
    origin_df = pd.read_csv(Path(filedir) / filename)
    return origin_df
