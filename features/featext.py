import pandas as pd


# 平滑移动线SMA
def calculate_sma(df, window=20, price_col="今收"):
    df[f"SMA_{window}"] = df[price_col].rolling(window).mean()
    return df


# RSI
def calculate_rsi(df, window=14, price_col="今收"):
    delta = df[price_col].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    return df


# 指数移动线
def calculate_macd(df, fast=12, slow=26, signal=9, price_col="今收"):
    ema_fast = df[price_col].ewm(span=fast, adjust=False).mean()
    ema_slow = df[price_col].ewm(span=slow, adjust=False).mean()
    df["MACD"] = ema_fast - ema_slow
    df["MACD_Signal"] = df["MACD"].ewm(span=signal, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]
    return df


# 布林带
def calculate_bollinger(df, window=20, std=2, price_col="今收"):
    sma = df[price_col].rolling(window).mean()
    rolling_std = df[price_col].rolling(window).std()
    df["Bollinger_Upper"] = sma + (rolling_std * std)
    df["Bollinger_Lower"] = sma - (rolling_std * std)
    return df


# 成交量移动平均（Volume MA）
def calculate_volume_ma(df, window=20, volume_col="成交量(万股)"):
    df[f"Volume_MA_{window}"] = df[volume_col].rolling(window).mean()
    return df


# 市盈率分位数（PE Percentile）
def calculate_pe_percentile(df, window=252, pe_col="市盈率"):
    df["PE_Pct"] = df[pe_col].rolling(window).rank(pct=True) * 100
    return df


def extractFeature(df: pd.DataFrame | None = None) -> pd.DataFrame:
    # 加载数据（假设df已包含原始字段）
    if df is None:
        origin_df = pd.read_csv("stock_data.csv")
    else:
        origin_df = df

    result_df = origin_df

    # 计算所有指标
    result_df = calculate_sma(result_df, window=20)
    result_df = calculate_rsi(result_df, window=14)
    result_df = calculate_macd(result_df)
    result_df = calculate_bollinger(result_df)
    result_df = calculate_volume_ma(result_df)
    result_df = calculate_pe_percentile(result_df)

    # 结果展示
    print(
        result_df[
            [
                "交易日期",
                "证券代码",
                "SMA_20",
                "RSI",
                "MACD",
                "Bollinger_Upper",
                "Volume_MA_20",
                "PE_Pct",
            ]
        ].tail()
    )
    return result_df
