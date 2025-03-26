import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Optional
import os
import io

class DataProcessor:
    """处理巨无霸指数和汇率数据的工具类"""
    
    def __init__(self):
        self.bigmac_data = None
        self.exchange_rate_data = None
        self.comparison_data = None
        
    def load_builtin_bigmac_data(self) -> pd.DataFrame:
        """加载内置的巨无霸指数数据"""
        try:
            # 读取内置数据
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'big-mac-full-index.csv')
            self.bigmac_data = pd.read_csv(data_path)
            
            # 数据预处理
            # 转换日期格式
            self.bigmac_data['date'] = pd.to_datetime(self.bigmac_data['date'])
            
            # 筛选中国的数据
            cn_data = self.bigmac_data[self.bigmac_data['iso_a3'] == 'CHN']
            if 'USD_raw' in cn_data.columns:
                cn_data = cn_data[['date', 'name', 'local_price', 'dollar_ex', 'dollar_price', 'USD_raw']]
            else:
                cn_data = cn_data[['date', 'name', 'local_price', 'dollar_ex', 'dollar_price']]
            
            self.bigmac_data = cn_data
            return cn_data
        except Exception as e:
            raise ValueError(f"内置巨无霸指数数据加载失败: {str(e)}")
    
    def load_builtin_exchange_rate_data(self) -> pd.DataFrame:
        """加载内置的汇率数据"""
        try:
            # 读取内置数据
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'RESSET_FXBOCQUOT.xlsx')
            self.exchange_rate_data = pd.read_excel(data_path)
            
            # 数据预处理
            # 尝试找出日期列和汇率列
            date_cols = [col for col in self.exchange_rate_data.columns if '日期' in col or 'date' in col.lower() or '截止日期' in col]
            rate_cols = [col for col in self.exchange_rate_data.columns if '汇率' in col or 'rate' in col.lower() or '基准价' in col]
            
            if date_cols and rate_cols:
                date_col = date_cols[0]
                rate_col = rate_cols[0]
                
                # 创建新的DataFrame
                actual_rates = pd.DataFrame()
                actual_rates['date'] = pd.to_datetime(self.exchange_rate_data[date_col])
                
                # 处理汇率，如果是人民币/100美元格式，需要除以100
                if '100' in rate_col or self.exchange_rate_data[rate_col].mean() > 500:  # 假设如果均值大于500，可能是100外币的格式
                    actual_rates['actual_rate'] = self.exchange_rate_data[rate_col] / 100
                else:
                    actual_rates['actual_rate'] = self.exchange_rate_data[rate_col]
                
                # 处理日期缺失问题，使用最近的之前交易日报价填充
                actual_rates = actual_rates.sort_values('date')
                
                # 填充缺失日期
                date_range = pd.date_range(start=actual_rates['date'].min(), end=actual_rates['date'].max())
                full_dates = pd.DataFrame({'date': date_range})
                actual_rates = pd.merge(full_dates, actual_rates, on='date', how='left')
                actual_rates['actual_rate'] = actual_rates['actual_rate'].fillna(method='ffill')
                
                self.exchange_rate_data = actual_rates
                return actual_rates
            else:
                # 如果无法自动识别列名，尝试使用固定列名
                if 'date' in self.exchange_rate_data.columns and 'actual_rate' in self.exchange_rate_data.columns:
                    self.exchange_rate_data['date'] = pd.to_datetime(self.exchange_rate_data['date'])
                    return self.exchange_rate_data
                elif 'date' in self.exchange_rate_data.columns and 'actual_rates' in self.exchange_rate_data.columns:
                    # 重命名列
                    self.exchange_rate_data = self.exchange_rate_data.rename(columns={'actual_rates': 'actual_rate'})
                    self.exchange_rate_data['date'] = pd.to_datetime(self.exchange_rate_data['date'])
                    return self.exchange_rate_data
                else:
                    raise ValueError("无法识别日期列和汇率列，请确保文件包含'date'和'actual_rate'或'actual_rates'列")
        except Exception as e:
            raise ValueError(f"内置汇率数据加载失败: {str(e)}")
    
    def load_bigmac_data(self, uploaded_file) -> pd.DataFrame:
        """加载巨无霸指数数据"""
        if uploaded_file is None:
            raise ValueError("请上传巨无霸指数数据文件")
            
        try:
            # 读取上传的数据
            self.bigmac_data = pd.read_csv(uploaded_file)
            
            # 数据预处理
            # 转换日期格式
            self.bigmac_data['date'] = pd.to_datetime(self.bigmac_data['date'])
            
            # 筛选中国的数据
            cn_data = self.bigmac_data[self.bigmac_data['iso_a3'] == 'CHN']
            if 'USD_raw' in cn_data.columns:
                cn_data = cn_data[['date', 'name', 'local_price', 'dollar_ex', 'dollar_price', 'USD_raw']]
            else:
                cn_data = cn_data[['date', 'name', 'local_price', 'dollar_ex', 'dollar_price']]
            
            self.bigmac_data = cn_data
            return cn_data
        except Exception as e:
            raise ValueError(f"巨无霸指数数据处理失败: {str(e)}")
        
        return None
    
    def load_exchange_rate_data(self, uploaded_file) -> pd.DataFrame:
        """加载汇率数据"""
        if uploaded_file is None:
            raise ValueError("请上传汇率数据文件")
            
        try:
            # 读取上传的数据
            if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                self.exchange_rate_data = pd.read_excel(uploaded_file)
            else:
                self.exchange_rate_data = pd.read_csv(uploaded_file)
            
            # 数据预处理
            try:
                # 尝试找出日期列和汇率列
                date_cols = [col for col in self.exchange_rate_data.columns if '日期' in col or 'date' in col.lower() or '截止日期' in col]
                rate_cols = [col for col in self.exchange_rate_data.columns if '汇率' in col or 'rate' in col.lower() or '基准价' in col]
                
                if date_cols and rate_cols:
                    date_col = date_cols[0]
                    rate_col = rate_cols[0]
                    
                    # 创建新的DataFrame
                    actual_rates = pd.DataFrame()
                    actual_rates['date'] = pd.to_datetime(self.exchange_rate_data[date_col])
                    
                    # 处理汇率，如果是人民币/100美元格式，需要除以100
                    if '100' in rate_col or self.exchange_rate_data[rate_col].mean() > 500:  # 假设如果均值大于500，可能是100外币的格式
                        actual_rates['actual_rate'] = self.exchange_rate_data[rate_col] / 100
                    else:
                        actual_rates['actual_rate'] = self.exchange_rate_data[rate_col]
                    
                    # 处理日期缺失问题，使用最近的之前交易日报价填充
                    actual_rates = actual_rates.sort_values('date')
                    
                    # 填充缺失日期
                    date_range = pd.date_range(start=actual_rates['date'].min(), end=actual_rates['date'].max())
                    full_dates = pd.DataFrame({'date': date_range})
                    actual_rates = pd.merge(full_dates, actual_rates, on='date', how='left')
                    actual_rates['actual_rate'] = actual_rates['actual_rate'].fillna(method='ffill')
                    
                    self.exchange_rate_data = actual_rates
                    return actual_rates
                else:
                    # 如果无法自动识别列名，尝试使用固定列名
                    if 'date' in self.exchange_rate_data.columns and 'actual_rate' in self.exchange_rate_data.columns:
                        self.exchange_rate_data['date'] = pd.to_datetime(self.exchange_rate_data['date'])
                        return self.exchange_rate_data
                    elif 'date' in self.exchange_rate_data.columns and 'actual_rates' in self.exchange_rate_data.columns:
                        # 重命名列
                        self.exchange_rate_data = self.exchange_rate_data.rename(columns={'actual_rates': 'actual_rate'})
                        self.exchange_rate_data['date'] = pd.to_datetime(self.exchange_rate_data['date'])
                        return self.exchange_rate_data
                    else:
                        raise ValueError("无法识别日期列和汇率列，请确保文件包含'date'和'actual_rate'或'actual_rates'列")
            except Exception as e:
                raise ValueError(f"汇率数据处理失败: {str(e)}")
        except Exception as e:
            raise ValueError(f"汇率数据读取失败: {str(e)}")
        
        return None
    
    def analyze_data(self) -> pd.DataFrame:
        """分析巨无霸指数和汇率数据"""
        if self.bigmac_data is None or self.exchange_rate_data is None:
            raise ValueError("请先上传并加载巨无霸指数和汇率数据")
            
        # 确保两个数据集都有"date"列
        if 'date' not in self.bigmac_data.columns or 'date' not in self.exchange_rate_data.columns:
            raise ValueError("数据集缺少日期列")
            
        # 确保汇率数据有actual_rate列
        if 'actual_rate' not in self.exchange_rate_data.columns:
            if 'actual_rates' in self.exchange_rate_data.columns:
                self.exchange_rate_data = self.exchange_rate_data.rename(columns={'actual_rates': 'actual_rate'})
            else:
                raise ValueError("汇率数据缺少actual_rate列")
        
        # 合并数据集
        comparison_data = pd.merge_asof(
            self.bigmac_data.sort_values('date'), 
            self.exchange_rate_data.sort_values('date'), 
            on='date', 
            direction='nearest'
        )
        
        # 计算巨无霸汇率和偏差
        comparison_data['big_mac_rate'] = comparison_data['local_price'] / comparison_data['dollar_price']
        comparison_data['deviation_pct'] = ((comparison_data['actual_rate'] - comparison_data['big_mac_rate']) 
                                          / comparison_data['big_mac_rate'] * 100)
        
        self.comparison_data = comparison_data
        return comparison_data
    
    def generate_comparison_chart(self) -> plt.Figure:
        """生成汇率对比图表"""
        if self.comparison_data is None:
            raise ValueError("请先分析数据")
            
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 设置风格
        sns.set_style("whitegrid")
        
        # 绘制汇率比较
        ax.plot(self.comparison_data['date'], self.comparison_data['big_mac_rate'], 
                'b-', label='Big Mac Index Rate')
        ax.plot(self.comparison_data['date'], self.comparison_data['actual_rate'], 
                'r-', label='Actual Market Rate')
        
        # 设置标签
        ax.set_xlabel('Date')
        ax.set_ylabel('CNY/USD Exchange Rate')
        ax.set_title('Big Mac Index Predicted Rate vs Actual Market Rate')
        ax.legend(loc='best')
        
        # 优化布局
        plt.tight_layout()
        
        return fig
    
    def generate_deviation_chart(self) -> plt.Figure:
        """生成偏差分析图表"""
        if self.comparison_data is None:
            raise ValueError("请先分析数据")
            
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 设置风格
        sns.set_style("whitegrid")
        
        # 绘制偏差趋势
        ax.bar(self.comparison_data['date'], self.comparison_data['deviation_pct'], 
               color='green', alpha=0.7)
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        # 设置标签
        ax.set_xlabel('Date')
        ax.set_ylabel('Deviation Percentage (%)')
        ax.set_title('CNY/USD Exchange Rate: Market Rate vs Big Mac Index Prediction Deviation')
        
        # 优化布局
        plt.tight_layout()
        
        return fig
    
    def get_key_metrics(self) -> dict:
        """获取关键指标数据"""
        if self.comparison_data is None:
            raise ValueError("请先分析数据")
            
        metrics = {
            'avg_deviation': self.comparison_data['deviation_pct'].mean(),
            'max_deviation': self.comparison_data['deviation_pct'].max(),
            'min_deviation': self.comparison_data['deviation_pct'].min(),
            'latest_deviation': self.comparison_data.iloc[-1]['deviation_pct'],
            'avg_bigmac_rate': self.comparison_data['big_mac_rate'].mean(),
            'latest_bigmac_rate': self.comparison_data.iloc[-1]['big_mac_rate'],
            'latest_actual_rate': self.comparison_data.iloc[-1]['actual_rate'],
            'data_period': f"{self.comparison_data['date'].min().strftime('%Y-%m-%d')} 至 {self.comparison_data['date'].max().strftime('%Y-%m-%d')}",
            'over_under': "低估" if self.comparison_data.iloc[-1]['deviation_pct'] < 0 else "高估"
        }
        
        return metrics
    
    def export_analysis_data(self, data=None) -> io.BytesIO:
        """导出分析数据"""
        if data is None:
            if self.comparison_data is None:
                raise ValueError("请先分析数据")
            data = self.comparison_data
            
        # 创建Excel文件
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            data.to_excel(writer, sheet_name='分析数据', index=False)
            
            # 创建关键指标表
            metrics = pd.DataFrame([self.get_key_metrics()])
            metrics.to_excel(writer, sheet_name='关键指标', index=False)
            
        output.seek(0)
        return output 