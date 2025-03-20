import pandas as pd

from model.model import AbsModel


class WeightedScoreModel(AbsModel):
    weights_: dict[str, float]

    def __init__(
        self,
        weights: dict[str, float],
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        feature_cols: list[str],
        group_col="交易日期",
    ) -> None:
        self.weights_ = weights
        super().__init__(train_data, test_data, feature_cols, group_col)

    def prepare_df(self, origin_df: pd.DataFrame) -> pd.DataFrame:
        # 准备数据（需标签：如未来收益率分档）
        df = origin_df.copy().fillna(0)
        df = df.sort_values(["证券代码", "交易日期"])
        # 标准化（此处用Rank标准化，避免极端值影响）
        for col in self.weights_.keys():
            df[f"{col}_rank"] = df.groupby("交易日期")[col].rank(pct=True)

        # 计算加权得分
        df["Score"] = sum(
            df[f"{col}_rank"] * weight for col, weight in self.weights_.items()
        )

        # 生成梯度榜
        df["Rank"] = df.groupby("交易日期")["Score"].rank(
            ascending=False, method="first"
        )
        return df

    def train_model(self):
        return self.train_data_

    def predict_model(self):
        return self.test_data_
