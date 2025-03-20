import unittest
import pandas as pd
from pathlib import Path
from features.featext import (
    calculate_sma,
    calculate_pe_percentile,
    calculate_rsi,
    calculate_macd,
    calculate_bollinger,
    calculate_volume_ma,
    extract_feature,
)

from config.configs import ROOT_DIR


class testFeatureExtraction(unittest.TestCase):
    def setUp(self) -> None:
        self.filename = "20250101.csv"
        self.origin_df = pd.read_csv(
            Path(f"{ROOT_DIR}/saved_data/history/SZSE/{self.filename}")
        )

    def testAllFeatures(self):
        res, _ = extract_feature(self.origin_df)
        self.assertTrue(True)
        path = Path(f"{ROOT_DIR}/feature")
        path.mkdir(parents=True, exist_ok=True)
        res.to_csv(path / self.filename)
