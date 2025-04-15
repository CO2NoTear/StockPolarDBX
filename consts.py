import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root

ORIGINAL_DATA_COLUMNS = set(
    [
        "交易日期",
        "证券代码",
        "前收",
        "开盘",
        "最高",
        "最低",
        "今收",
        "涨跌幅（%）",
        "成交量(万股)",
        "成交金额(万元)",
        "市盈率",
    ]
)

RENAME_MAPPER = {
    "交易日期": "date",
    "证券代码": "code",
    "前收": "pre_close",
    "开盘": "open",
    "最高": "high_price",
    "最低": "low_price",
    "今收": "close",
    "涨跌幅（%）": "inc_rate",
    "成交量(万股)": "volume",
    "成交金额(万元)": "turnover",
    "市盈率": "PE",
}
