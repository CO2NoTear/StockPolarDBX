from typing import Literal
from flask import Flask, jsonify
from flask_cors import CORS  # 解决跨域问题
import pandas as pd
from db import get_engine
import pymysql

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
        return pd.read_sql(sql, get_engine()).fillna("-")


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
        return jsonify(data.to_dict("list"))
    else:
        return None


@app.route("/api/getTopK/<k>/<date>", methods=["GET"])
def get_top_k(k: int, date: str):
    sql = f"select date, code, rankScore from features where date='{date}' AND rankScore<={k} ORDER BY(rankScore) ASC"
    data = _query_db(sql)
    if data is not None:
        return jsonify(data.to_dict("list"))
    else:
        return None


if __name__ == "__main__":
    # 启动服务，允许外部访问（host='0.0.0.0'），默认端口5000
    app.run(host="0.0.0.0", port=2425, debug=True)
