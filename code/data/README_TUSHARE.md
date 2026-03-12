# Tushare 数据获取模块使用文档

## 📚 目录
1. [模块介绍](#模块介绍)
2. [环境配置](#环境配置)
3. [核心功能](#核心功能)
4. [使用示例](#使用示例)
5. [API限制说明](#api限制说明)
6. [常见问题](#常见问题)

## 模块介绍

`tushare_fetcher.py` 是一个封装了Tushare Pro API的数据获取模块，提供了统一、易用的接口来获取A股市场数据。

### 主要特点
- ✅ 统一的API接口封装
- ✅ 自动处理复权数据
- ✅ 批量数据获取支持
- ✅ 完整的错误处理
- ✅ 支持多种数据类型

## 环境配置

### 1. 安装依赖
```bash
pip install tushare pandas python-dotenv
```

### 2. 获取Tushare Token
1. 注册账号：https://tushare.pro/register
2. 获取token：https://tushare.pro/user/token
3. 积分说明：新用户有120积分，可获取基础数据

### 3. 配置Token
在 `/Users/jaylorden/Documents/quant/code/.env` 文件中添加：
```
TUSHARE_TOKEN=your_token_here
```

## 核心功能

### 类结构
```python
from data.tushare_fetcher import TushareFetcher

# 初始化
fetcher = TushareFetcher()  # 自动从.env读取token
# 或
fetcher = TushareFetcher(token="your_token")  # 直接传入token
```

### 功能分类

#### 1. 股票基础信息
| 方法 | 描述 | 积分要求 |
|-----|------|---------|
| `get_stock_list()` | 获取股票列表 | 120 |
| `get_stock_info()` | 获取单只股票详情 | 120 |
| `get_trade_calendar()` | 获取交易日历 | 120 |

#### 2. 行情数据
| 方法 | 描述 | 积分要求 |
|-----|------|---------|
| `get_daily_data()` | 获取日线数据（支持复权） | 120 |
| `get_weekly_data()` | 获取周线数据 | 120 |
| `get_monthly_data()` | 获取月线数据 | 120 |
| `get_realtime_quote()` | 获取实时行情 | 120 |

#### 3. 财务数据
| 方法 | 描述 | 积分要求 |
|-----|------|---------|
| `get_income_statement()` | 获取利润表 | 120 |
| `get_balance_sheet()` | 获取资产负债表 | 120 |
| `get_cashflow()` | 获取现金流量表 | 120 |
| `get_financial_indicators()` | 获取财务指标 | 120 |

#### 4. 指数数据
| 方法 | 描述 | 积分要求 |
|-----|------|---------|
| `get_index_daily()` | 获取指数日线 | 120 |
| `get_index_components()` | 获取指数成份股 | 400+ |

#### 5. 批量功能
| 方法 | 描述 |
|-----|------|
| `batch_get_daily_data()` | 批量获取多只股票日线 |
| `get_stock_pool()` | 获取股票池（沪深300等） |

## 使用示例

### 示例1：获取单只股票数据
```python
from data.tushare_fetcher import TushareFetcher

# 初始化
fetcher = TushareFetcher()

# 获取平安银行最近30天的日线数据（前复权）
df = fetcher.get_daily_data(
    ts_code='000001.SZ',
    start_date='20240201',
    end_date='20240301',
    adj='qfq'  # 前复权
)

print(df.head())
```

### 示例2：批量获取数据
```python
# 批量获取银行股数据
bank_stocks = ['000001.SZ', '600036.SH', '601166.SH']

data_dict = fetcher.batch_get_daily_data(
    ts_codes=bank_stocks,
    start_date='20240201',
    end_date='20240301'
)

# 分析每只股票
for ts_code, df in data_dict.items():
    returns = (df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100
    print(f"{ts_code} 月收益率: {returns:.2f}%")
```

### 示例3：获取财务数据
```python
# 获取招商银行财务指标
indicators = fetcher.get_financial_indicators(
    ts_code='600036.SH',
    start_date='20230101'
)

# 查看ROE趋势
print(indicators[['end_date', 'roe', 'roa']].head())
```

### 示例4：技术指标计算
```python
# 获取数据
df = fetcher.get_daily_data('000002.SZ', '20240101', '20240301')

# 计算移动平均
df['MA5'] = df['close'].rolling(5).mean()
df['MA20'] = df['close'].rolling(20).mean()

# 金叉死叉信号
df['signal'] = 0
df.loc[df['MA5'] > df['MA20'], 'signal'] = 1
df.loc[df['MA5'] < df['MA20'], 'signal'] = -1
```

### 示例5：保存数据到本地
```python
# 获取一年的数据
df = fetcher.get_daily_data(
    ts_code='600519.SH',
    start_date='20230301',
    end_date='20240301'
)

# 保存为CSV
df.to_csv('data/csv/600519_SH_2023.csv', index=False)

# 保存为Excel（需要安装openpyxl）
df.to_excel('data/excel/600519_SH_2023.xlsx', index=False)
```

## API限制说明

### 积分系统
- 新用户：120积分（免费）
- 可获取数据：基础股票数据、日线数据、基础财务数据
- 限制：部分高级数据需要更高积分

### 调用频率限制
- 每分钟最多200次
- 建议在循环中添加延时：
```python
import time

for stock in stock_list:
    data = fetcher.get_daily_data(stock, start, end)
    time.sleep(0.3)  # 延时0.3秒
```

### 数据更新时间
- 日线数据：每天15:30后更新
- 财务数据：季报公布后1-2天更新
- 实时数据：交易时间实时更新

## 常见问题

### Q1: Token配置错误
**错误信息**: `请设置TUSHARE_TOKEN环境变量或传入token参数`

**解决方案**:
1. 检查.env文件是否存在
2. 确认Token是否正确
3. 重启Python环境

### Q2: 数据为空
**可能原因**:
1. 股票代码错误（注意后缀：.SZ深圳 .SH上海）
2. 日期范围内股票未上市或已退市
3. 非交易日没有数据

### Q3: 积分不足
**错误信息**: `积分不足`

**解决方案**:
1. 检查账户积分：https://tushare.pro/user/token
2. 使用基础接口（120积分可用）
3. 考虑使用yfinance等免费数据源

### Q4: 获取实时数据失败
**注意事项**:
- 实时数据只在交易时间可用（9:30-15:00）
- 部分数据有15分钟延迟

## 数据字段说明

### 日线数据字段
| 字段 | 说明 |
|-----|------|
| ts_code | 股票代码 |
| trade_date | 交易日期 |
| open | 开盘价 |
| high | 最高价 |
| low | 最低价 |
| close | 收盘价 |
| pre_close | 昨收价 |
| change | 涨跌额 |
| pct_chg | 涨跌幅 |
| vol | 成交量（手） |
| amount | 成交额（千元） |

### 财务指标字段
| 字段 | 说明 |
|-----|------|
| roe | 净资产收益率 |
| roa | 总资产收益率 |
| debt_to_assets | 资产负债率 |
| current_ratio | 流动比率 |
| quick_ratio | 速动比率 |

## 进阶用法

### 自定义数据处理
```python
class MyDataFetcher(TushareFetcher):
    def get_data_with_indicators(self, ts_code, start, end):
        # 获取基础数据
        df = self.get_daily_data(ts_code, start, end)
        
        # 添加技术指标
        df['MA5'] = df['close'].rolling(5).mean()
        df['MA20'] = df['close'].rolling(20).mean()
        df['VOL_MA5'] = df['vol'].rolling(5).mean()
        
        # 计算MACD
        df['EMA12'] = df['close'].ewm(span=12).mean()
        df['EMA26'] = df['close'].ewm(span=26).mean()
        df['DIF'] = df['EMA12'] - df['EMA26']
        df['DEA'] = df['DIF'].ewm(span=9).mean()
        df['MACD'] = 2 * (df['DIF'] - df['DEA'])
        
        return df
```

### 数据缓存策略
```python
import os
import pickle
from datetime import datetime

def get_cached_data(ts_code, start, end):
    cache_dir = 'data/cache'
    os.makedirs(cache_dir, exist_ok=True)
    
    cache_file = f"{cache_dir}/{ts_code}_{start}_{end}.pkl"
    
    # 检查缓存
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    
    # 获取新数据
    fetcher = TushareFetcher()
    df = fetcher.get_daily_data(ts_code, start, end)
    
    # 保存缓存
    with open(cache_file, 'wb') as f:
        pickle.dump(df, f)
    
    return df
```

## 运行示例程序

```bash
# 运行交互式示例
python data/tushare_examples.py

# 选择示例：
# 1 - 基础使用
# 2 - 行情数据
# 3 - 财务数据
# 4 - 指数数据
# 5 - 批量下载
# 6 - 股票池
# 7 - 技术分析
# 8 - 数据保存
# all - 运行全部
```

## 相关资源

- [Tushare官方文档](https://tushare.pro/document/2)
- [Tushare数据字典](https://tushare.pro/document/2?doc_id=25)
- [积分获取说明](https://tushare.pro/document/1?doc_id=13)

---

*最后更新：2025年3月*