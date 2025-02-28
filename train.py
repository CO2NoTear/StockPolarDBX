from pathlib import Path

from pandas.errors import EmptyDataError
from config.configs import ROOT_DIR
from model.model import RankingModel
from features.featext import extract_feature
from utils import prepare_origin_df
import pandas as pd


if __name__ == "__main__":
    Path(f"{ROOT_DIR}/output/").mkdir(exist_ok=True)

    train_origin_df = prepare_origin_df(filename="20240101.csv")
    test_origin_df = prepare_origin_df(filename="20250101.csv")

    train, feature_cols = extract_feature(train_origin_df)
    test, feature_cols = extract_feature(test_origin_df)

    model = RankingModel(train, test, feature_cols)

    result = model.train_ranking_model()
    result = model.predict_ranking_model()

    # result = result.sort_values("Rank", ascending=True)

    result.to_csv(f"{ROOT_DIR}/output/ranking.csv")

    print(result[["交易日期", "证券代码", "Rank"]].head(20))
