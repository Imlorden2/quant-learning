"""
Tushare数据获取模块
提供统一的Tushare API数据获取接口
"""

import os
import pandas as pd
import tushare as ts
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Union
from dotenv import load_dotenv


class TushareFetcher:
    """Tushare数据获取器"""
    
    def __init__(self, token: Optional[str] = None):
        """
        初始化Tushare接口
        
        Args:
            token: Tushare API token，如果不提供则从环境变量读取
        """
        load_dotenv()
        
        if token is None:
            token = os.getenv('TUSHARE_TOKEN')
            if not token:
                raise ValueError("请设置TUSHARE_TOKEN环境变量或传入token参数")
        
        ts.set_token(token)
        self.pro = ts.pro_api()
        print("✅ Tushare API初始化成功")
    
    # ==================== 股票基础信息 ====================
    
    def get_stock_list(self, 
                       list_status: str = 'L',
                       exchange: str = '',
                       fields: Optional[List[str]] = None) -> pd.DataFrame:
        """
        获取股票列表
        
        Args:
            list_status: 上市状态 L上市 D退市 P暂停上市，默认L
            exchange: 交易所 SSE上交所 SZSE深交所
            fields: 需要的字段列表
        
        Returns:
            股票列表DataFrame
        """
        df = self.pro.stock_basic(
            list_status=list_status,
            exchange=exchange,
            fields=fields or 'ts_code,symbol,name,area,industry,list_date'
        )
        print(f"获取到 {len(df)} 只股票信息")
        return df
    
    def get_stock_info(self, ts_code: str) -> Dict:
        """
        获取单只股票详细信息
        
        Args:
            ts_code: 股票代码（如：000001.SZ）
        
        Returns:
            股票信息字典
        """
        basic = self.pro.stock_basic(ts_code=ts_code)
        company = self.pro.stock_company(ts_code=ts_code)
        
        info = {}
        if not basic.empty:
            info.update(basic.iloc[0].to_dict())
        if not company.empty:
            info.update(company.iloc[0].to_dict())
        
        return info
    
    def get_trade_calendar(self, 
                          start_date: str,
                          end_date: str,
                          exchange: str = 'SSE') -> pd.DataFrame:
        """
        获取交易日历
        
        Args:
            start_date: 开始日期 (YYYYMMDD)
            end_date: 结束日期 (YYYYMMDD)
            exchange: 交易所 SSE上交所 SZSE深交所
        
        Returns:
            交易日历DataFrame
        """
        df = self.pro.trade_cal(
            exchange=exchange,
            start_date=start_date,
            end_date=end_date
        )
        return df[df['is_open'] == 1]
    
    # ==================== 行情数据 ====================
    
    def get_daily_data(self,
                      ts_code: str,
                      start_date: str,
                      end_date: str,
                      adj: str = 'qfq') -> pd.DataFrame:
        """
        获取日线行情数据
        
        Args:
            ts_code: 股票代码
            start_date: 开始日期 (YYYYMMDD)
            end_date: 结束日期 (YYYYMMDD)
            adj: 复权类型 None未复权 qfq前复权 hfq后复权
        
        Returns:
            日线数据DataFrame
        """
        # 获取未复权数据
        df = self.pro.daily(
            ts_code=ts_code,
            start_date=start_date,
            end_date=end_date
        )
        
        if df.empty:
            print(f"警告：{ts_code} 在 {start_date}-{end_date} 期间没有数据")
            return df
        
        # 如果需要复权
        if adj in ['qfq', 'hfq']:
            factors = self.pro.adj_factor(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date
            )
            
            if not factors.empty:
                df = df.merge(factors[['trade_date', 'adj_factor']], on='trade_date')
                
                price_cols = ['open', 'high', 'low', 'close', 'pre_close']
                for col in price_cols:
                    if col in df.columns:
                        df[col] = df[col] * df['adj_factor']
        
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df = df.sort_values('trade_date')
        
        print(f"获取 {ts_code} 日线数据 {len(df)} 条")
        return df
    
    def get_weekly_data(self,
                       ts_code: str,
                       start_date: str,
                       end_date: str) -> pd.DataFrame:
        """
        获取周线数据
        
        Args:
            ts_code: 股票代码
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            周线数据DataFrame
        """
        df = self.pro.weekly(
            ts_code=ts_code,
            start_date=start_date,
            end_date=end_date
        )
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df = df.sort_values('trade_date')
        return df
    
    def get_monthly_data(self,
                        ts_code: str,
                        start_date: str,
                        end_date: str) -> pd.DataFrame:
        """
        获取月线数据
        
        Args:
            ts_code: 股票代码
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            月线数据DataFrame
        """
        df = self.pro.monthly(
            ts_code=ts_code,
            start_date=start_date,
            end_date=end_date
        )
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df = df.sort_values('trade_date')
        return df
    
    def get_realtime_quote(self, ts_code: Union[str, List[str]]) -> pd.DataFrame:
        """
        获取实时行情数据
        
        Args:
            ts_code: 股票代码或代码列表
        
        Returns:
            实时行情DataFrame
        """
        if isinstance(ts_code, str):
            ts_code = [ts_code]
        
        ts_code_str = ','.join(ts_code)
        df = ts.realtime_quote(ts_code=ts_code_str)
        return df
    
    # ==================== 财务数据 ====================
    
    def get_income_statement(self,
                           ts_code: str,
                           period: Optional[str] = None,
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> pd.DataFrame:
        """
        获取利润表数据
        
        Args:
            ts_code: 股票代码
            period: 报告期(如20230331)
            start_date: 公告开始日期
            end_date: 公告结束日期
        
        Returns:
            利润表DataFrame
        """
        df = self.pro.income(
            ts_code=ts_code,
            period=period,
            start_date=start_date,
            end_date=end_date
        )
        return df
    
    def get_balance_sheet(self,
                         ts_code: str,
                         period: Optional[str] = None,
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None) -> pd.DataFrame:
        """
        获取资产负债表数据
        
        Args:
            ts_code: 股票代码
            period: 报告期
            start_date: 公告开始日期
            end_date: 公告结束日期
        
        Returns:
            资产负债表DataFrame
        """
        df = self.pro.balancesheet(
            ts_code=ts_code,
            period=period,
            start_date=start_date,
            end_date=end_date
        )
        return df
    
    def get_cashflow(self,
                    ts_code: str,
                    period: Optional[str] = None,
                    start_date: Optional[str] = None,
                    end_date: Optional[str] = None) -> pd.DataFrame:
        """
        获取现金流量表数据
        
        Args:
            ts_code: 股票代码
            period: 报告期
            start_date: 公告开始日期
            end_date: 公告结束日期
        
        Returns:
            现金流量表DataFrame
        """
        df = self.pro.cashflow(
            ts_code=ts_code,
            period=period,
            start_date=start_date,
            end_date=end_date
        )
        return df
    
    def get_financial_indicators(self,
                                ts_code: str,
                                start_date: Optional[str] = None,
                                end_date: Optional[str] = None) -> pd.DataFrame:
        """
        获取财务指标数据
        
        Args:
            ts_code: 股票代码
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            财务指标DataFrame
        """
        df = self.pro.fina_indicator(
            ts_code=ts_code,
            start_date=start_date,
            end_date=end_date
        )
        return df
    
    # ==================== 指数数据 ====================
    
    def get_index_daily(self,
                       ts_code: str,
                       start_date: str,
                       end_date: str) -> pd.DataFrame:
        """
        获取指数日线数据
        
        Args:
            ts_code: 指数代码（如：000001.SH 上证指数）
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            指数日线DataFrame
        """
        df = self.pro.index_daily(
            ts_code=ts_code,
            start_date=start_date,
            end_date=end_date
        )
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        df = df.sort_values('trade_date')
        return df
    
    def get_index_components(self, index_code: str) -> pd.DataFrame:
        """
        获取指数成份股
        
        Args:
            index_code: 指数代码（如：000300.SH 沪深300）
        
        Returns:
            成份股DataFrame
        """
        df = self.pro.index_weight(index_code=index_code)
        return df
    
    # ==================== 批量获取功能 ====================
    
    def batch_get_daily_data(self,
                           ts_codes: List[str],
                           start_date: str,
                           end_date: str,
                           adj: str = 'qfq') -> Dict[str, pd.DataFrame]:
        """
        批量获取多只股票的日线数据
        
        Args:
            ts_codes: 股票代码列表
            start_date: 开始日期
            end_date: 结束日期
            adj: 复权类型
        
        Returns:
            字典，key为股票代码，value为对应的数据DataFrame
        """
        result = {}
        total = len(ts_codes)
        
        for i, ts_code in enumerate(ts_codes, 1):
            print(f"正在获取 [{i}/{total}] {ts_code}")
            try:
                df = self.get_daily_data(ts_code, start_date, end_date, adj)
                if not df.empty:
                    result[ts_code] = df
            except Exception as e:
                print(f"获取 {ts_code} 失败: {e}")
                continue
        
        print(f"成功获取 {len(result)}/{total} 只股票数据")
        return result
    
    def get_stock_pool(self, 
                      pool_type: str = 'hs300',
                      date: Optional[str] = None) -> List[str]:
        """
        获取股票池
        
        Args:
            pool_type: 股票池类型
                - 'hs300': 沪深300
                - 'zz500': 中证500
                - 'zz1000': 中证1000
                - 'sz50': 上证50
            date: 日期，默认最新
        
        Returns:
            股票代码列表
        """
        index_map = {
            'hs300': '000300.SH',
            'zz500': '000905.SH',
            'zz1000': '000852.SH',
            'sz50': '000016.SH'
        }
        
        if pool_type not in index_map:
            raise ValueError(f"不支持的股票池类型: {pool_type}")
        
        df = self.pro.index_weight(
            index_code=index_map[pool_type],
            trade_date=date
        )
        
        if df.empty:
            return []
        
        return df['con_code'].tolist()


if __name__ == "__main__":
    # 使用示例
    fetcher = TushareFetcher()
    
    # 1. 获取股票列表
    stocks = fetcher.get_stock_list(exchange='SSE')
    print(f"\n上交所股票数量: {len(stocks)}")
    
    # 2. 获取单只股票日线数据
    df = fetcher.get_daily_data(
        ts_code='000001.SZ',
        start_date='20240101',
        end_date='20240131'
    )
    print(f"\n平安银行1月数据:\n{df.head()}")