from pathlib import Path
from typing import Literal

from config.configs import ROOT_DIR
from model.rankingModel import RankingModel
from featureExtraction.featext import extract_feature
from model.weightedScoreModel import WeightedScoreModel
from utils import prepare_origin_df
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

    train_origin_df = prepare_origin_df(filename="20240101.csv")
    test_origin_df = prepare_origin_df(filename="20250101.csv")

    train, feature_cols = extract_feature(train_origin_df)
    test, feature_cols = extract_feature(test_origin_df)

    model = getModel(args.model, train, test, feature_cols)

    model.train_model()
    result = model.predict_model()

    # result = result.sort_values("Rank", ascending=True)

    result.to_csv(f"{ROOT_DIR}/output/{args.model}_result.csv")

    print(
        result[result["交易日期"] == "2025-01-02"][result["Rank"] < 200]
        .drop(columns="交易日期")[
            # .sort_values(["Rank"])[["证券代码", "Rank"]]
            ["证券代码", "Rank"]
        ]
        .head(20)
    )
