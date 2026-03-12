# 量化交易分析框架

## 📖 项目简介

这是一个模块化的量化交易分析框架，专注于股票市场的流动性分析、技术指标计算和交易策略开发。项目采用分层架构设计，便于扩展和维护。

## 🏗️ 项目结构

```
quant_trading/
├── data/                    # 数据层
│   ├── fetcher.py          # 数据获取器（tushare、yfinance等）
│   ├── cleaner.py          # 数据清洗器
│   ├── storage.py          # 数据存储管理
│   └── loader.py           # 数据加载器
│
├── analysis/                # 分析层
│   ├── spread.py           # 买卖价差分析
│   ├── liquidity.py        # 流动性指标分析
│   ├── volatility.py       # 波动率分析
│   └── metrics.py          # 技术指标计算
│
├── strategy/                # 策略层
│   ├── base.py            # 策略基类
│   ├── momentum.py        # 动量策略
│   └── mean_revert.py     # 均值回归策略
│
├── backtest/               # 回测层
│   ├── engine.py          # 回测引擎
│   └── evaluator.py       # 绩效评估
│
├── utils/                  # 工具层
│   ├── config.py          # 配置管理
│   ├── logger.py          # 日志管理
│   └── validators.py      # 数据验证
│
├── visualization/          # 可视化层
│   ├── charts.py          # 图表生成
│   └── reports.py         # 报告生成
│
├── tests/                  # 测试
├── config/                 # 配置文件
├── notebooks/             # Jupyter笔记本
├── docs/                  # 文档
│
├── main.py               # 主程序入口
├── requirements.txt      # 依赖包
└── README.md            # 本文件
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pandas, numpy, matplotlib
- tushare (可选，需要token)
- yfinance (免费数据源)

### 安装依赖

```bash
pip install pandas numpy matplotlib tushare yfinance python-dotenv
```

### 配置设置

#### 1. 创建环境变量文件
```bash
# 复制配置模板
cp .env.example .env

# 编辑.env文件，添加你的API密钥
# .env
TUSHARE_TOKEN=your_tushare_token_here
```

#### 2. 获取Tushare Token
1. 注册账号：https://tushare.pro/register
2. 获取token：https://tushare.pro/user/token
3. 将token添加到.env文件中

### 使用示例

#### 1. Tushare数据获取（推荐）
```python
import os
from dotenv import load_dotenv
import tushare as ts

# 加载环境变量
load_dotenv()

# 获取Tushare接口
token = os.getenv('TUSHARE_TOKEN')
pro = ts.pro_api(token)

# 获取股票日线数据
df = pro.daily(ts_code='000001.SZ', start_date='20240301', end_date='20240331')
print(f"获取到 {len(df)} 条数据")
```

#### 2. 流动性分析
```python
from analysis.liquidity import LiquidityAnalyzer

# 创建分析器
analyzer = LiquidityAnalyzer()

# 分析单只股票
result = analyzer.analyze_stock('000001.SZ', period=30)

# 批量对比
stocks = ['000001.SZ', '000002.SZ', '600000.SH'] 
comparison = analyzer.compare_stocks(stocks)
```

#### 3. 免费数据源备选
```python
import yfinance as yf

# 获取美股数据
ticker = yf.Ticker("AAPL")
data = ticker.history(period="1mo")
print(data.head())
```

## 🔧 核心功能

### 数据处理
- ✅ Tushare API集成（支持A股数据）
- ✅ 环境变量配置管理（.env文件）
- ✅ 多数据源支持（tushare、yfinance）
- ✅ 数据清洗和预处理
- ✅ 灵活的数据存储方案

### 市场分析
- ✅ 买卖价差分析（Roll模型）
- ✅ 流动性指标（Amihud、换手率等）
- ✅ 波动率分析
- ✅ 技术指标计算

### 策略开发
- 🚧 策略基类框架
- 🚧 动量策略
- 🚧 均值回归策略
- 🚧 套利策略

### 回测系统
- 🚧 历史数据回测
- 🚧 绩效指标计算
- 🚧 参数优化

### 可视化
- ✅ 流动性对比图表
- ✅ 分析报告生成
- 🚧 实时监控面板

*图例：✅ 已完成，🚧 开发中，⏳ 计划中*

## 📊 已完成的示例

### 流动性分析器

当前已实现完整的流动性分析功能：

- **价差分析**：Roll价差估计、相对价差、日内价差
- **流动性指标**：平均成交量、成交额、Amihud非流动性指标
- **对比分析**：多股票批量对比和排名
- **可视化**：6种图表展示流动性指标
- **报告生成**：文本格式的分析报告

### 使用的原有文件

- `liquidity_analyzer.py` - 完整的流动性分析器（待重构到新框架）

## 🛠️ 开发计划

### Phase 1: 基础架构（当前）
- [x] 项目目录结构
- [x] 流动性分析功能
- [x] 环境变量配置管理（.env + python-dotenv）
- [x] Tushare API集成
- [ ] 模块化重构

### Phase 2: 数据模块
- [ ] 统一的数据获取接口
- [ ] 数据清洗和验证
- [ ] 本地数据缓存

### Phase 3: 分析模块
- [ ] 技术指标库
- [ ] 统计分析工具
- [ ] 因子分析

### Phase 4: 策略模块  
- [ ] 策略框架设计
- [ ] 基础策略实现
- [ ] 策略组合

### Phase 5: 回测模块
- [ ] 回测引擎
- [ ] 风险管理
- [ ] 绩效分析

## 📝 学习记录

这个项目是量化交易学习的实践项目，对应学习进度：

- **1.1.1 交易机制** ✅ 已完成
- **1.1.2 金融产品** ✅ 已完成  
- **1.1.3 市场微观结构** ✅ 已完成
- **1.1.4 基本术语** 🚧 学习中

学习资料和笔记位于：`/Users/jaylorden/Documents/quant/`

## 🤝 贡献指南

1. 每个模块保持单一职责
2. 遵循Python PEP 8编码规范
3. 添加适当的文档字符串
4. 编写单元测试
5. 更新README文档

## 📞 联系方式

- 项目作者：Claude Code Assistant
- 学习者：Jay Lorden
- 开始时间：2025年3月4日

## 📄 许可证

本项目仅供学习和研究使用。

---

*这是一个持续演进的学习项目，欢迎探索和改进！*