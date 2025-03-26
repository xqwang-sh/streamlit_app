import requests
import json
import os
import pandas as pd
import io
import matplotlib.pyplot as plt
from typing import Optional, Dict, Any, List, Union

class DeepSeekAnalyzer:
    """DeepSeek API客户端，用于分析数据并生成报告"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        self.api_base_url = "https://api.deepseek.com"  # 更新为正确的API基础URL
        self.model = "deepseek-chat"  # 默认模型
        
    def set_api_key(self, api_key: str):
        """设置API密钥"""
        self.api_key = api_key
        
    def analyze_metrics(self, metrics: Dict[str, Any]) -> str:
        """分析汇率偏差指标"""
        if not self.api_key:
            return "请先设置DeepSeek API密钥"
            
        # 构建分析提示
        prompt = f"""
        请基于以下中美汇率与巨无霸指数偏差数据进行经济分析：
        
        - 分析时间段: {metrics['data_period']}
        - 平均偏差百分比: {metrics['avg_deviation']:.2f}%
        - 最大偏差百分比: {metrics['max_deviation']:.2f}%
        - 最小偏差百分比: {metrics['min_deviation']:.2f}%
        - 最新偏差百分比: {metrics['latest_deviation']:.2f}%
        - 汇率状态: 人民币相对美元{metrics['over_under']}
        
        请回答：
        1. 根据巨无霸指数，人民币相对美元汇率的总体状况如何？是被高估还是低估？程度如何？
        2. 这种偏差的主要经济原因可能是什么？
        3. 这种现象与中国的经济政策和国际贸易地位有何关联？
        4. 巨无霸指数在预测中国汇率方面有哪些局限性？
        
        请给出专业、简洁的分析，每个问题的回答控制在100字左右。
        """
        
        try:
            # 请求API
            response = self._call_api(prompt)
            return response
        except Exception as e:
            return f"分析失败: {str(e)}"
            
    def analyze_data_trends(self, comparison_data: pd.DataFrame, include_chart: bool = False, chart_path: Optional[str] = None) -> str:
        """分析汇率偏差趋势"""
        if not self.api_key:
            return "请先设置DeepSeek API密钥"
            
        # 提取关键时间点的数据
        recent_years = comparison_data.sort_values('date').tail(20)  # 最近的观测值
        yearly_data = comparison_data.resample('Y', on='date').mean().reset_index()  # 年度平均
            
        # 计算关键趋势指标
        start_deviation = comparison_data.iloc[0]['deviation_pct']
        end_deviation = comparison_data.iloc[-1]['deviation_pct']
        change = end_deviation - start_deviation
        
        # 查找峰值和谷值
        peak = comparison_data['deviation_pct'].max()
        peak_date = comparison_data.loc[comparison_data['deviation_pct'].idxmax(), 'date'].strftime('%Y-%m-%d')
        trough = comparison_data['deviation_pct'].min()
        trough_date = comparison_data.loc[comparison_data['deviation_pct'].idxmin(), 'date'].strftime('%Y-%m-%d')
        
        # 构建分析提示
        prompt = f"""
        请基于以下中美汇率与巨无霸指数偏差的趋势数据进行深入分析：
        
        - 分析时间段: {comparison_data['date'].min().strftime('%Y-%m-%d')} 至 {comparison_data['date'].max().strftime('%Y-%m-%d')}
        - 初始偏差: {start_deviation:.2f}%
        - 最终偏差: {end_deviation:.2f}%
        - 总体变化: {change:.2f}% ({'上升' if change > 0 else '下降'})
        - 最高偏差: {peak:.2f}% (于 {peak_date})
        - 最低偏差: {trough:.2f}% (于 {trough_date})
        
        请分析：
        1. 在分析期间内，人民币汇率相对于巨无霸指数的偏差呈现什么样的总体趋势？
        2. 偏差出现峰值和谷值的时间点与当时的重大经济事件有何对应关系？
        3. 近期趋势如何？这可能预示着什么样的未来发展？
        4. 基于巨无霸指数的分析，对中国汇率政策有何建议？
        
        请给出专业、简洁的分析，每个问题的回答控制在150字左右。
        """
        
        try:
            # 请求API
            response = self._call_api(prompt)
            return response
        except Exception as e:
            return f"分析失败: {str(e)}"
    
    def generate_report(self, metrics: Dict[str, Any], trend_analysis: str, metrics_analysis: str) -> str:
        """生成完整分析报告"""
        if not self.api_key:
            return "请先设置DeepSeek API密钥"
            
        # 构建报告提示
        prompt = f"""
        请基于以下中美汇率与巨无霸指数分析内容，编写一份简明的学术分析报告：
        
        ## 基本数据
        - 分析时间段: {metrics['data_period']}
        - 平均偏差百分比: {metrics['avg_deviation']:.2f}%
        - 最大偏差百分比: {metrics['max_deviation']:.2f}%
        - 最小偏差百分比: {metrics['min_deviation']:.2f}%
        - 最新偏差百分比: {metrics['latest_deviation']:.2f}%
        - 汇率状态: 人民币相对美元{metrics['over_under']}
        
        ## 指标分析
        {metrics_analysis}
        
        ## 趋势分析
        {trend_analysis}
        
        请根据以上内容，编写一份完整的报告，包含以下部分：
        
        1. 报告标题
        2. 引言：简述本研究的背景和目的
        3. 数据概览：列出关键数据和指标
        4. 分析发现：整合指标分析和趋势分析的主要发现
        5. 理论讨论：从购买力平价理论角度讨论分析结果
        6. 政策启示：基于分析结果提出的政策建议
        7. 结论：总结主要发现和建议
        
        请确保报告内容专业、简洁、有逻辑性，总字数控制在1000字左右。
        """
        
        try:
            # 请求API
            response = self._call_api(prompt)
            return response
        except Exception as e:
            return f"报告生成失败: {str(e)}"
    
    def _call_api(self, prompt: str) -> str:
        """调用DeepSeek API"""
        if not self.api_key:
            raise ValueError("未设置API密钥")
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是一个专业的经济分析师，擅长分析汇率和购买力平价理论。"},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(
                f"{self.api_base_url}/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
            
        except requests.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")
            
    # 模拟API调用的函数，实际部署时应删除此函数
    def mock_analyze_metrics(self, metrics: Dict[str, Any]) -> str:
        """模拟分析汇率偏差指标"""
        response = f"""
        ## 人民币汇率状况分析
        
        1. **总体状况**：根据巨无霸指数，人民币相对美元呈现{metrics['over_under']}状态，平均偏差为{metrics['avg_deviation']:.2f}%。这表明按照购买力平价理论，人民币的实际市场汇率与其理论价值存在一定差距。这种{metrics['over_under']}程度相对显著，反映了市场汇率与基础经济因素之间的不平衡。
        
        2. **经济原因**：这种偏差主要可能源于中国的出口导向型经济政策、资本管制措施以及政府对汇率的干预。此外，劳动力成本差异、生产效率差异和非贸易品价格差异也是重要因素。中国制造业的规模经济和成本优势导致了某些商品价格相对较低。
        
        3. **经济政策关联**：人民币的汇率状态与中国作为全球制造业中心和出口大国的地位密切相关。适度{metrics['over_under']}的货币有助于维持出口竞争力，支持"中国制造"的全球扩张。同时，这也是中国逐步开放资本市场和推进国际化进程中的过渡性现象。
        
        4. **巨无霸指数局限性**：在中国背景下，巨无霸指数有明显局限性。麦当劳在中国属于中高端消费，不完全反映中国整体物价水平。指数忽略了中国巨大的区域差异、服务成本差异和非贸易品因素。此外，指数仅基于单一商品，无法全面反映经济复杂性，特别是中国特殊的经济结构和市场特征。
        """
        return response
        
    def mock_analyze_trends(self, start_year: int, end_year: int) -> str:
        """模拟分析汇率偏差趋势"""
        response = f"""
        ## 人民币汇率偏差趋势分析 ({start_year}-{end_year})
        
        1. **总体趋势**：{start_year}年至{end_year}年间，人民币相对于巨无霸指数的偏差总体呈波动下降趋势，表明人民币低估程度整体上有所减弱。这一趋势反映了中国经济的结构性变化和逐步开放的汇率政策。值得注意的是，趋势并非线性下降，而是呈现出明显的周期性波动，这与全球经济周期和中国经济政策调整密切相关。
        
        2. **峰谷与事件对应**：偏差峰值主要出现在全球金融危机(2008-2009)和欧债危机(2011-2012)期间，这些时期国际资本流动剧烈，投资者追求安全资产，导致美元走强。谷值则多出现在中国经济高速增长期(2007)和美国量化宽松政策实施后(2013-2014)，当时中国贸易顺差大幅增加，外汇储备上升，人民币承受升值压力。2015年汇率改革和2018年中美贸易摩擦也对偏差产生了显著影响。
        
        3. **近期趋势**：近期趋势显示偏差有所扩大，这可能与疫情后全球经济复苏不均衡、通胀压力上升以及地缘政治紧张局势有关。这预示着未来人民币汇率可能面临更大波动性，尤其在美联储收紧货币政策背景下，中国央行需要平衡经济增长与汇率稳定的双重目标。如果这一趋势持续，可能预示中国将进一步加强资本管制，同时推进市场化改革。
        
        4. **政策建议**：基于巨无霸指数分析，建议中国继续推进汇率市场化改革，增强汇率弹性，但避免大幅度、单向调整。同时，应加快国内经济结构转型，减少对出口的依赖，增强内需对经济增长的贡献。此外，应进一步开放金融市场，吸引更多长期资本流入，平衡短期资本流动带来的汇率波动。最后，加强与主要贸易伙伴的汇率政策协调，共同维护全球金融稳定。
        """
        return response
        
    def mock_generate_report(self, metrics: Dict[str, Any]) -> str:
        """模拟生成完整分析报告"""
        response = f"""
        # 中美汇率与巨无霸指数分析报告
        
        ## 引言
        
        本研究基于《经济学人》的巨无霸指数，分析{metrics['data_period']}期间人民币兑美元汇率的实际表现与理论预期之间的偏差。购买力平价理论认为，长期而言，相同商品在不同国家的价格应当相等，巨无霸指数正是基于此原理构建的简化模型。通过对比巨无霸指数预测的汇率与市场实际汇率，本研究旨在评估人民币的估值状况，并探讨其背后的经济机制与政策含义。
        
        ## 数据概览
        
        本研究分析期间内，人民币兑美元汇率相对巨无霸指数平均{metrics['over_under']}了{abs(metrics['avg_deviation']):.2f}%，最大{metrics['over_under']}幅度达{abs(metrics['max_deviation']):.2f}%，最小为{abs(metrics['min_deviation']):.2f}%。最新观测数据显示，偏差为{metrics['latest_deviation']:.2f}%。总体而言，数据表明人民币兑美元存在持续且显著的{metrics['over_under']}现象，但偏差程度呈现一定的波动性。
        
        ## 分析发现
        
        研究发现，人民币相对美元的{metrics['over_under']}现象具有结构性特征，反映了中国作为出口导向型经济体的战略定位。偏差趋势与全球经济周期、中美经贸关系演变以及中国国内经济政策调整高度相关。特别是在2008年全球金融危机、2015年汇率改革以及2018年中美贸易摩擦等关键时间点，偏差波动明显增大。
        
        近年来，偏差水平有扩大趋势，这与中国经济增长放缓、全球供应链重构以及新冠疫情冲击下的国际资本流动变化密切相关。值得注意的是，尽管存在持续{metrics['over_under']}，市场汇率与巨无霸指数预测值之间的差距呈现逐步收敛的长期趋势，反映了中国在推进汇率市场化改革方面取得的进展。
        
        ## 理论讨论
        
        从购买力平价理论视角看，持续存在的偏差表明市场汇率并未完全反映基础经济面。然而，这一现象并非中国特有，大多数发展中经济体都表现出类似特征。理论上，商品贸易和资本流动应当推动汇率向购买力平价水平收敛，但实际上，以下因素限制了这一机制的有效性：
        
        1. 非贸易品因素：服务等非贸易品价格在不同国家可有显著差异
        2. 市场分割：贸易壁垒和运输成本导致市场不完全一体化
        3. 政策干预：央行干预和资本管制影响汇率形成
        4. 巴拉萨-萨缪尔森效应：发展中国家生产率增速较快导致实际汇率升值
        
        ## 政策启示
        
        基于分析结果，我们提出以下政策建议：
        
        1. 继续推进汇率形成机制改革，增强汇率弹性，减少行政干预
        2. 加快经济结构转型，促进从出口导向向内需驱动转变
        3. 稳步推进资本项目开放，吸引更多长期资本流入
        4. 加强与主要贸易伙伴的汇率政策协调，避免竞争性贬值
        5. 提高国内服务业生产效率，缩小与发达国家的生产率差距
        
        ## 结论
        
        巨无霸指数分析显示，人民币兑美元存在持续的{metrics['over_under']}现象，但这种偏差需要在中国特殊的经济发展阶段和政策框架下理解。虽然巨无霸指数提供了简单直观的国际比较工具，但其预测存在局限性，不能完全反映复杂的经济现实。
        
        展望未来，随着中国经济转型升级和金融市场开放程度提高，人民币汇率有望进一步向反映基础经济面的水平靠拢。政策制定者应在维护汇率稳定与推进市场化改革之间寻求平衡，为经济高质量发展创造有利的汇率环境。
        """
        return response 