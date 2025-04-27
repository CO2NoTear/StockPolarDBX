from typing import Literal
from flask import Flask, jsonify
from flask_cors import CORS  # 解决跨域问题
import pandas as pd
from crawlHistory import crawlAllHistory
from db import get_engine
from sqlalchemy.sql import text

# 创建 Flask 应用实例
app = Flask(__name__)
CORS(app)  # 允许所有域名跨域访问（生产环境建议配置具体域名）

FEATURE_COLS = [
    "SMA_20",
    "5d_Return",
    "RSI",
    "MACD",
    "MACD_Signal",
    "MACD_Hist",
    "Bollinger_Upper",
    "Bollinger_Lower",
    "Volume_MA_20",
    "PE_Pct",
]


def _query_db(sql: str) -> pd.DataFrame | None:
    if sql != "":
        return pd.read_sql(sql, get_engine())


@app.route("/api/getData/<feature>/<stockCode>", methods=["GET"])
def get_data(
    feature: Literal[
        "original",
        "SMA_20",
        "5d_Return",
        "RSI",
        "MACD",
        "MACD_Signal",
        "MACD_Hist",
        "Bollinger_Upper",
        "Bollinger_Lower",
        "Volume_MA_20",
        "PE_Pct",
    ],
    stockCode,
):
    """返回最新数据的API接口"""
    data = None
    sql = ""
    if feature == "original":
        sql = f"select * from original where code={stockCode}"
    elif feature in FEATURE_COLS:
        sql = f"select date, `{feature}` from features where code={stockCode}"

    data = _query_db(sql)

    if data is not None:
        if feature != "original":
            return jsonify(data.fillna("-").to_dict("list"))
        else:
            sql = f"select date, `SMA_20`, `Bollinger_Upper`, `Bollinger_Lower` from features where code={stockCode}"
            featureData = _query_db(sql)
            jsonResult = data.fillna("-").to_dict("list")
            if featureData is None:
                return jsonify(jsonResult)
            closeData = data[data["date"].isin(featureData["date"].to_list())][
                ["date", "close"]
            ]
            featureData = featureData.join(closeData.set_index("date"), on=["date"])
            print(featureData)
            jsonResult["buyPoints"] = featureData[
                featureData["Bollinger_Lower"] > featureData["close"]
            ]["date"].to_list()
            jsonResult["buyPointsClose"] = featureData[
                featureData["Bollinger_Lower"] > featureData["close"]
            ]["close"].to_list()
            jsonResult["sellPoints"] = featureData[
                featureData["Bollinger_Upper"] < featureData["close"]
            ]["date"].to_list()
            jsonResult["sellPointsClose"] = featureData[
                featureData["Bollinger_Upper"] < featureData["close"]
            ]["close"].to_list()
            return jsonify(jsonResult)
    else:
        return None


@app.route("/api/getTopK/<k>/<strategy>", methods=["GET"])
def get_top_k(k: int, strategy: str):
    sql = f"select code, AVG(`rankScore_{strategy}`) from features GROUP BY code ORDER BY AVG(`rankScore_{strategy}`) ASC LIMIT {k}"
    data = _query_db(sql)
    if data is not None:
        return jsonify(data.fillna("-").to_dict("list"))
    else:
        return None


@app.route("/api/crawlHistory/", methods=["GET"])
def crawl_history():
    try:
        with get_engine().connect() as connection:
            connection.execute(text("delete from original;"))
            connection.commit()
        crawlAllHistory(ex="SZSE", year=2024)
        crawlAllHistory(ex="SZSE", year=2025)
        return jsonify(success=True)
    except:
        return jsonify(success=False)


if __name__ == "__main__":
    # 启动服务，允许外部访问（host='0.0.0.0'），默认端口5000
    app.run(host="0.0.0.0", port=2425, debug=True)
