from flask import Flask, jsonify
from flask_cors import CORS  # 解决跨域问题
import pandas as pd
from db import get_engine
import pymysql

# 创建 Flask 应用实例
app = Flask(__name__)
CORS(app)  # 允许所有域名跨域访问（生产环境建议配置具体域名）

# 模拟数据（可替换为数据库查询或其他动态数据）
latest_data = {
    "status": "success",
    "message": "Data retrieved successfully",
    "data": {"timestamp": ["2023-10-05 14:30:00"], "value": [23]},
}


@app.route("/api/getData/<feature>/<stockCode>", methods=["GET"])
def get_data(feature, stockCode):
    """返回最新数据的API接口"""
    original_data = pd.read_sql(
        f"select * from original where code={stockCode}", get_engine()
    )
    return jsonify(original_data.to_dict("list"))


if __name__ == "__main__":
    # 启动服务，允许外部访问（host='0.0.0.0'），默认端口5000
    app.run(host="0.0.0.0", port=2425, debug=True)
