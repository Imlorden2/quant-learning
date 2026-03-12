"""
Tushare数据获取使用示例
演示各种常用的数据获取场景
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.tushare_fetcher import TushareFetcher
import pandas as pd
from datetime import datetime, timedelta


def example_basic_usage():
    """基础使用示例"""
    print("=" * 50)
    print("1. 基础使用示例")
    print("=" * 50)
    
    # 初始化
    fetcher = TushareFetcher()
    
    # 获取股票列表
    print("\n获取深交所主板股票列表:")
    stocks = fetcher.get_stock_list(exchange='SZSE')
    print(stocks.head())
    
    # 获取单只股票信息
    print("\n获取平安银行详细信息:")
    info = fetcher.get_stock_info('000001.SZ')
    for key, value in list(info.items())[:10]:
        print(f"  {key}: {value}")


def example_market_data():
    """行情数据获取示例"""
    print("\n" + "=" * 50)
    print("2. 行情数据获取示例")
    print("=" * 50)
    
    fetcher = TushareFetcher()
    
    # 获取日线数据（前复权）
    print("\n获取贵州茅台近3个月日线数据（前复权）:")
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')
    
    df = fetcher.get_daily_data(
        ts_code='600519.SH',
        start_date=start_date,
        end_date=end_date,
        adj='qfq'
    )
    print(df.tail())
    
    # 计算简单统计
    print(f"\n期间统计:")
    print(f"  最高价: {df['high'].max():.2f}")
    print(f"  最低价: {df['low'].min():.2f}")
    print(f"  平均成交量: {df['vol'].mean():.0f}")
    print(f"  累计涨跌幅: {(df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100:.2f}%")


def example_financial_data():
    """财务数据获取示例"""
    print("\n" + "=" * 50)
    print("3. 财务数据获取示例")
    print("=" * 50)
    
    fetcher = TushareFetcher()
    
    # 获取财务指标
    print("\n获取招商银行最近4个季度财务指标:")
    df = fetcher.get_financial_indicators(
        ts_code='600036.SH',
        start_date='20230101'
    )
    
    if not df.empty:
        # 选择关键指标
        key_columns = ['end_date', 'roe', 'roa', 'debt_to_assets', 'current_ratio']
        available_columns = [col for col in key_columns if col in df.columns]
        print(df[available_columns].head(4))


def example_index_data():
    """指数数据获取示例"""
    print("\n" + "=" * 50)
    print("4. 指数数据获取示例")
    print("=" * 50)
    
    fetcher = TushareFetcher()
    
    # 获取上证指数数据
    print("\n获取上证指数近1个月数据:")
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
    
    df = fetcher.get_index_daily(
        ts_code='000001.SH',
        start_date=start_date,
        end_date=end_date
    )
    
    if not df.empty:
        print(df.tail())
        print(f"\n期间涨跌幅: {(df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100:.2f}%")


def example_batch_download():
    """批量数据获取示例"""
    print("\n" + "=" * 50)
    print("5. 批量数据获取示例")
    print("=" * 50)
    
    fetcher = TushareFetcher()
    
    # 批量获取多只股票数据
    print("\n批量获取银行股数据:")
    bank_stocks = [
        '000001.SZ',  # 平安银行
        '600036.SH',  # 招商银行
        '601166.SH',  # 兴业银行
    ]
    
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
    
    data_dict = fetcher.batch_get_daily_data(
        ts_codes=bank_stocks,
        start_date=start_date,
        end_date=end_date
    )
    
    # 计算收益率对比
    print("\n各股票期间收益率:")
    for ts_code, df in data_dict.items():
        if not df.empty and len(df) > 1:
            returns = (df['close'].iloc[-1] / df['close'].iloc[0] - 1) * 100
            print(f"  {ts_code}: {returns:.2f}%")


def example_stock_pool():
    """股票池获取示例"""
    print("\n" + "=" * 50)
    print("6. 股票池获取示例")
    print("=" * 50)
    
    fetcher = TushareFetcher()
    
    # 获取沪深300成份股
    print("\n获取沪深300成份股:")
    hs300_stocks = fetcher.get_stock_pool('hs300')
    print(f"沪深300包含 {len(hs300_stocks)} 只股票")
    if hs300_stocks:
        print(f"前10只: {hs300_stocks[:10]}")


def example_technical_analysis():
    """技术分析数据准备示例"""
    print("\n" + "=" * 50)
    print("7. 技术分析数据准备示例")
    print("=" * 50)
    
    fetcher = TushareFetcher()
    
    # 获取数据用于技术分析
    print("\n获取数据计算技术指标:")
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=100)).strftime('%Y%m%d')
    
    df = fetcher.get_daily_data(
        ts_code='000002.SZ',
        start_date=start_date,
        end_date=end_date
    )
    
    if not df.empty and len(df) >= 20:
        # 计算简单移动平均
        df['MA5'] = df['close'].rolling(window=5).mean()
        df['MA20'] = df['close'].rolling(window=20).mean()
        
        # 计算RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        print(df[['trade_date', 'close', 'MA5', 'MA20', 'RSI']].tail())


def example_save_to_csv():
    """数据保存示例"""
    print("\n" + "=" * 50)
    print("8. 数据保存示例")
    print("=" * 50)
    
    fetcher = TushareFetcher()
    
    # 获取数据并保存
    print("\n获取数据并保存到CSV:")
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
    
    df = fetcher.get_daily_data(
        ts_code='000858.SZ',
        start_date=start_date,
        end_date=end_date
    )
    
    if not df.empty:
        # 创建data目录下的csv子目录
        csv_dir = os.path.join(os.path.dirname(__file__), 'csv')
        os.makedirs(csv_dir, exist_ok=True)
        
        # 保存文件
        filename = os.path.join(csv_dir, f"000858_SZ_{start_date}_{end_date}.csv")
        df.to_csv(filename, index=False)
        print(f"数据已保存到: {filename}")
        print(f"数据条数: {len(df)}")


def main():
    """运行所有示例"""
    examples = [
        ("基础使用", example_basic_usage),
        ("行情数据", example_market_data),
        ("财务数据", example_financial_data),
        ("指数数据", example_index_data),
        ("批量下载", example_batch_download),
        ("股票池", example_stock_pool),
        ("技术分析", example_technical_analysis),
        ("数据保存", example_save_to_csv),
    ]
    
    print("\n" + "=" * 50)
    print("Tushare数据获取示例集合")
    print("=" * 50)
    print("\n可用示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    try:
        choice = input("\n请选择要运行的示例 (1-8, 或 'all' 运行全部, 'q' 退出): ").strip()
        
        if choice.lower() == 'q':
            print("退出程序")
            return
        elif choice.lower() == 'all':
            for name, func in examples:
                try:
                    func()
                except Exception as e:
                    print(f"\n运行 {name} 时出错: {e}")
        else:
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                examples[idx][1]()
            else:
                print("无效的选择")
    except ValueError:
        print("请输入有效的数字")
    except Exception as e:
        print(f"运行出错: {e}")


if __name__ == "__main__":
    main()