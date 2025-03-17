以下是6个**广泛使用且易于实现**的核心指标，包含数学公式和Python代码实现（基于Pandas）：

---

### 1. 简单移动平均线（SMA）
**公式**：  
\[ \text{SMA}_N = \frac{1}{N} \sum_{i=1}^{N} \text{Close}_{t-i} \]  
**代码**：
```python
def calculate_sma(df, window=20, price_col='今日收盘价'):
    df[f'SMA_{window}'] = df[price_col].rolling(window).mean()
    return df
```

---

### 2. 相对强弱指数（RSI）
**公式**：  
1. 计算价格变化：\(\Delta = \text{Close}_t - \text{Close}_{t-1}\)  
2. 平均增益（Avg Gain）和平均损失（Avg Loss）：  
   \[ \text{Avg Gain}_N = \frac{\sum \text{Gain}}{N}, \quad \text{Avg Loss}_N = \frac{\sum \text{Loss}}{N} \]  
3. RS = \(\frac{\text{Avg Gain}}{\text{Avg Loss}}\)  
4. RSI = \(100 - \frac{100}{1 + RS}\)  

**代码**：
```python
def calculate_rsi(df, window=14, price_col='今日收盘价'):
    delta = df[price_col].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df
```

---

### 3. MACD（指数移动平均）
**公式**：  
- EMA12 = 今日收盘价的12日指数移动平均  
- EMA26 = 今日收盘价的26日指数移动平均  
- MACD线 = EMA12 - EMA26  
- 信号线 = MACD线的9日EMA  
- 柱状图 = MACD线 - 信号线  

**代码**：
```python
def calculate_macd(df, fast=12, slow=26, signal=9, price_col='今日收盘价'):
    ema_fast = df[price_col].ewm(span=fast, adjust=False).mean()
    ema_slow = df[price_col].ewm(span=slow, adjust=False).mean()
    df['MACD'] = ema_fast - ema_slow
    df['MACD_Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    return df
```

---

### 4. 布林带（Bollinger Bands）
**公式**：  
- 中轨 = 20日SMA  
- 上轨 = 中轨 + 2×20日标准差  
- 下轨 = 中轨 - 2×20日标准差  

**代码**：
```python
def calculate_bollinger(df, window=20, std=2, price_col='今日收盘价'):
    sma = df[price_col].rolling(window).mean()
    rolling_std = df[price_col].rolling(window).std()
    df['Bollinger_Upper'] = sma + (rolling_std * std)
    df['Bollinger_Lower'] = sma - (rolling_std * std)
    return df
```

---

### 5. 成交量移动平均（Volume MA）
**公式**：  
\[ \text{VolumeMA}_N = \frac{1}{N} \sum_{i=1}^{N} \text{Volume}_{t-i} \]  

**代码**：
```python
def calculate_volume_ma(df, window=20, volume_col='成交量(万股)'):
    df[f'Volume_MA_{window}'] = df[volume_col].rolling(window).mean()
    return df
```

---

### 6. 市盈率分位数（PE Percentile）
**公式**：  
\[ \text{PE Percentile} = \frac{\text{当前PE在历史PE中的排名}}{\text{总样本数}} \times 100\% \]  

**代码**：
```python
def calculate_pe_percentile(df, window=252, pe_col='市盈率'):
    df['PE_Pct'] = df[pe_col].rolling(window).rank(pct=True) * 100
    return df
```

---

### 完整调用示例
```python
import pandas as pd

# 加载数据（假设df已包含原始字段）
df = pd.read_csv('stock_data.csv')

# 计算所有指标
df = calculate_sma(df, window=20)
df = calculate_rsi(df, window=14)
df = calculate_macd(df)
df = calculate_bollinger(df)
df = calculate_volume_ma(df)
df = calculate_pe_percentile(df)

# 结果展示
print(df[['交易日期', '证券代码', 'SMA_20', 'RSI', 'MACD', 'Bollinger_Upper', 'Volume_MA_20', 'PE_Pct']].tail())
```

---

### 关键说明
1. **数据要求**：输入数据需按**证券代码分组并按日期排序**，确保滚动计算正确。
2. **参数优化**：可根据实际数据调整窗口周期（如RSI常用14日，SMA常用20/50/200日）。
3. **去极值处理**：建议对PE等基本面指标做winsorize处理（如去除前1%和后1%的极端值）。
4. **动态排名**：梯度榜生成时，可用`df.groupby('日期').rank()`实现每日横截面排名。

这些指标涵盖了趋势（SMA、布林带）、动量（RSI、MACD）、成交量（Volume MA）和估值（PE分位数），是构建多因子股票推荐系统的核心基础。
