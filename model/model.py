import lightgbm as lgb
from lightgbm.basic import Booster
import pandas as pd


class RankingModel:
    model_: Booster
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
        self.train_data_ = RankingModel.prepare_df(train_data)
        self.test_data_ = RankingModel.prepare_df(test_data)

    @staticmethod
    def prepare_df(origin_df: pd.DataFrame) -> pd.DataFrame:
        # 准备数据（需标签：如未来收益率分档）
        df = origin_df.copy()
        df = df.sort_values(["证券代码", "交易日期"])
        df["future_return"] = df.groupby("证券代码")["今收"].shift(-5).pct_change(5)
        df["label"] = pd.qcut(df["future_return"], 10, labels=False)  # 分10档
        # print(df["label"].tail())

        return df

    def train_ranking_model(self):
        # 构建LightGBM数据集
        train_dataset = lgb.Dataset(
            data=self.train_data_[self.feature_cols_],
            label=self.train_data_["label"],
            group=self.train_data_.groupby(self.groupby_col_)
            .size()
            .values,  # 按日期分组
        )
        # 训练排序模型
        params = {
            "objective": "lambdarank",
            "metric": "ndcg",
            "learning_rate": 0.05,
            "num_leaves": 31,
        }
        self.model_ = lgb.train(params, train_dataset, num_boost_round=100)

    def predict_ranking_model(self):
        result = self.test_data_.copy()
        # 生成排序
        result["Rank_Score"] = self.model_.predict(self.test_data_[self.feature_cols_])
        # print(result["Rank_Score"].tail(20))
        result["Rank"] = result.groupby("交易日期")["Rank_Score"].rank(ascending=False)
        return result
