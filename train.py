from datetime import datetime
from pathlib import Path
from typing import Literal

from consts import ROOT_DIR
from model.rankingModel import RankingModel
from featureExtraction.featext import extract_feature
from model.weightedScoreModel import WeightedScoreModel
from utils import prepare_origin_df_from_db
import pandas as pd

from argparse import ArgumentParser


def getModel(
    modelName: Literal["ranking", "weightedScore"],
    train: pd.DataFrame,
    test: pd.DataFrame,
    feature_cols: list[str],
):
    if modelName == "ranking":
        return RankingModel(train, test, feature_cols)
    if modelName == "weightedScore":
        weights = {
            "RSI": 0.15,  # 动量
            "MACD_Hist": 0.15,  # 趋势
            "Volume_MA_20": 0.2,  # 成交量
            "PE_Pct": 0.2,  # 估值
            # "Bollinger_%B": 0.1,  # 波动性（需计算：Bollinger %B）
            "5d_Return": 0.3,  # 短期收益率
        }

        return WeightedScoreModel(weights, train, test, feature_cols)
    raise ValueError(f"Unkonwn model name {modelName}")


if __name__ == "__main__":
    parser = ArgumentParser("Training models.")
    parser.add_argument(
        "-m", "--model", choices=["ranking", "weightedScore"], required=True
    )

    args = parser.parse_args()

    Path(f"{ROOT_DIR}/output/").mkdir(exist_ok=True)

    train_origin_df = prepare_origin_df_from_db(
        startDate=datetime(2024, 1, 1), endDate=datetime(2025, 1, 31)
    )
    test_origin_df = prepare_origin_df_from_db(
        startDate=datetime(2025, 2, 1), endDate=datetime(2025, 6, 1)
    )
    print(test_origin_df.head(20))

    train, feature_cols = extract_feature(train_origin_df)
    test, feature_cols = extract_feature(test_origin_df)

    model = getModel(args.model, train, test, feature_cols)

    model.train_model()
    result = model.predict_model()

    # result = result.sort_values("Rank", ascending=True)

    result.to_csv(f"{ROOT_DIR}/output/{args.model}_result.csv")

    print(
        result[result["date"] == "2025-01-02"][result["Rank"] < 200]
        .drop(columns="date")[
            # .sort_values(["Rank"])[["证券代码", "Rank"]]
            ["code", "Rank"]
        ]
        .head(20)
    )
