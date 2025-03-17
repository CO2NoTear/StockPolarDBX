from abc import ABCMeta, abstractmethod
from typing import Any
import pandas as pd


class AbsModel(metaclass=ABCMeta):
    model_: Any
    train_data_: pd.DataFrame
    test_data_: pd.DataFrame
    feature_cols_: list[str]
    groupby_col_: str

    def __init__(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        feature_cols: list[str],
        group_col="交易日期",
    ) -> None:
        self.feature_cols_ = feature_cols
        self.groupby_col_ = group_col
        self.train_data_ = self.prepare_df(train_data)
        self.test_data_ = self.prepare_df(test_data)

    @abstractmethod
    def prepare_df(self, origin_df: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def train_model(self) -> pd.DataFrame | None:
        pass

    @abstractmethod
    def predict_model(self) -> pd.DataFrame:
        pass
