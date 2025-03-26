import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_processor import DataProcessor
try:
    from utils.ai_analyzer import DeepSeekAnalyzer
except ImportError:
    # 创建一个简单的类用于示例
    class DeepSeekAnalyzer:
        def __init__(self):
            pass
        
        def set_api_key(self, api_key):
            pass
        
        def _call_api(self, prompt):
            return "这是一个示例AI分析结果。实际部署时，这里将显示AI生成的分析内容。"
        
        def mock_analyze_metrics(self, metrics):
            return "这是一个示例AI分析结果。实际部署时，这里将显示AI生成的基于指标的分析内容。"
        
        def mock_analyze_trends(self, start_year, end_year):
            return "这是一个示例AI分析结果。实际部署时，这里将显示AI生成的趋势分析内容。"

# 页面配置
st.set_page_config(
    page_title="数据分析 - 巨无霸指数分析",
    page_icon="📈",
    layout="wide"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .chart-container {
        background-color: #ffffff;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .insight-card {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 5px solid #4e73df;
    }
    .insight-title {
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .note-box {
        background-color: #e7f3fe;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #2196f3;
        margin: 1rem 0;
    }
    .policy-card {
        background-color: #ffe8cc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #fd7e14;
        margin: 1rem 0;
    }
    .policy-title {
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #d63384;
    }
    .api-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .analysis-result {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 页面标题
st.markdown('<div class="main-header">数据分析与AI洞察</div>', unsafe_allow_html=True)

st.write("在这个页面，您可以对巨无霸指数和汇率数据进行深入分析，探索其中的模式和趋势，并通过AI获取智能洞察。")

# 检查分析数据是否已加载
if 'analysis_data' not in st.session_state or st.session_state.analysis_data is None:
    st.warning("您尚未完成数据预处理，请先前往 **数据导入** 页面进行数据处理。")
    st.stop()

# 获取分析数据
analysis_data = st.session_state.analysis_data

# 初始化AI分析器
if 'ai_analyzer' not in st.session_state:
    st.session_state.ai_analyzer = DeepSeekAnalyzer()

# API密钥设置（放在侧边栏）
with st.sidebar:
    st.markdown("## AI分析设置")
    
    st.markdown("""
    <div class="api-box">
    <b>获取DeepSeek API密钥：</b>
    1. 访问 <a href="https://www.deepseek.com" target="_blank">DeepSeek官网</a>
    2. 注册/登录账号
    3. 在开发者中心获取API密钥
    </div>
    """, unsafe_allow_html=True)
    
    # 设置默认API密钥
    default_api_key = "sk-9f93d5bf3dec40a3bb52d5824b261f6c"
    
    # 在输入框中显示默认API密钥
    api_key = st.text_input("输入DeepSeek API密钥", value=default_api_key, type="password")
    
    if st.button("设置API密钥"):
        if api_key:
            try:
                st.session_state.ai_analyzer.set_api_key(api_key)
                st.success("API密钥设置成功！")
            except Exception as e:
                st.error(f"API设置失败: {str(e)}")

# 创建侧边栏过滤器
st.sidebar.markdown("## 数据过滤")

# 时间范围选择
min_date = analysis_data['date'].min().to_pydatetime()
max_date = analysis_data['date'].max().to_pydatetime()

date_range = st.sidebar.date_input(
    "选择时间范围",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_data = analysis_data[(analysis_data['date'] >= pd.Timestamp(start_date)) & 
                                 (analysis_data['date'] <= pd.Timestamp(end_date))].copy()
else:
    filtered_data = analysis_data.copy()

# 数据分析选项卡
tab1, tab2, tab3 = st.tabs(["基本统计分析", "汇率政策与趋势", "显著变化点分析"])

# 基本统计分析选项卡
with tab1:
    st.markdown('<div class="sub-header">基本统计与可视化</div>', unsafe_allow_html=True)
    
    # 创建双Y轴图表
    fig_compare = make_subplots(specs=[[{"secondary_y": True}]])
    
    # 添加市场汇率
    fig_compare.add_trace(
        go.Scatter(x=filtered_data['date'], y=filtered_data['actual_rate'], 
                 name="实际市场汇率", line=dict(color='#4e73df', width=2)),
        secondary_y=False,
    )
    
    # 添加巨无霸汇率
    fig_compare.add_trace(
        go.Scatter(x=filtered_data['date'], y=filtered_data['big_mac_rate'], 
                 name="巨无霸汇率", line=dict(color='#1cc88a', width=2, dash='dash')),
        secondary_y=False,
    )
    
    # 添加偏差百分比
    fig_compare.add_trace(
        go.Scatter(x=filtered_data['date'], y=filtered_data['deviation_pct'], 
                 name="偏差百分比", line=dict(color='#e74a3b', width=2)),
        secondary_y=True,
    )
    
    # 添加水平零线
    fig_compare.add_hline(y=0, line_dash="dot", line_color="gray", secondary_y=True)
    
    # 更新图表布局
    fig_compare.update_layout(
        title_text="市场汇率与巨无霸汇率对比",
        hovermode="x unified"
    )
    
    # 设置Y轴标题
    fig_compare.update_yaxes(title_text="汇率 (CNY/USD)", secondary_y=False)
    fig_compare.update_yaxes(title_text="偏差百分比 (%)", secondary_y=True)
    
    st.plotly_chart(fig_compare, use_container_width=True)
    
    # 计算关键指标
    period_start = filtered_data['date'].min().strftime('%Y-%m-%d')
    period_end = filtered_data['date'].max().strftime('%Y-%m-%d')
    avg_deviation = filtered_data['deviation_pct'].mean()
    start_deviation = filtered_data.iloc[0]['deviation_pct']
    end_deviation = filtered_data.iloc[-1]['deviation_pct']
    trend_change = end_deviation - start_deviation
    
    # 基本统计指标
    st.markdown("### 基本统计指标")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 汇率偏差的基本统计量
        deviation_stats = {
            "平均偏差 (%)": filtered_data['deviation_pct'].mean(),
            "标准差 (%)": filtered_data['deviation_pct'].std(),
            "最大偏差 (%)": filtered_data['deviation_pct'].max(),
            "最小偏差 (%)": filtered_data['deviation_pct'].min(),
            "偏差中位数 (%)": filtered_data['deviation_pct'].median(),
            "分析周期": f"{period_start} 至 {period_end}",
            "初始偏差 (%)": start_deviation,
            "结束偏差 (%)": end_deviation
        }
        
        # 创建统计表
        stats_df = pd.DataFrame(list(deviation_stats.items()), columns=['指标', '值'])
        
        # 修复类型错误：逐行处理而不是批量处理，对数值类型应用round()
        for i, row in stats_df.iterrows():
            if row['指标'] != "分析周期" and isinstance(row['值'], (int, float)):
                stats_df.at[i, '值'] = round(row['值'], 2)
        
        st.dataframe(stats_df, use_container_width=True)
    
    with col2:
        # 偏差分布直方图
        fig_hist = px.histogram(filtered_data, x='deviation_pct', 
                               title='偏差百分比分布',
                               labels={'deviation_pct': '偏差百分比 (%)', 'count': '频次'},
                               color_discrete_sequence=['#4e73df'])
        
        fig_hist.add_vline(x=0, line_dash="dash", line_color="red")
        fig_hist.add_vline(x=filtered_data['deviation_pct'].mean(), 
                          line_dash="dot", line_color="green",
                          annotation_text="平均值")
        
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # 年度走势图
    st.markdown("### 年度分析")
    
    # 计算年度平均值
    yearly_data = filtered_data.copy()
    yearly_data['year'] = yearly_data['date'].dt.year
    yearly_avg = yearly_data.groupby('year').agg({
        'actual_rate': 'mean',
        'big_mac_rate': 'mean',
        'local_price': 'mean',
        'dollar_price': 'mean',
        'deviation_pct': 'mean'
    }).reset_index()
    
    # 年度对比表格
    yearly_comparison = yearly_avg[['year', 'actual_rate', 'big_mac_rate', 'deviation_pct']].rename(
        columns={
            'year': '年份', 
            'actual_rate': '市场汇率(平均)', 
            'big_mac_rate': '巨无霸汇率(平均)',
            'deviation_pct': '偏差百分比(平均)'
        }
    )
    
    # 格式化数值
    yearly_comparison['市场汇率(平均)'] = yearly_comparison['市场汇率(平均)'].round(4)
    yearly_comparison['巨无霸汇率(平均)'] = yearly_comparison['巨无霸汇率(平均)'].round(4)
    yearly_comparison['偏差百分比(平均)'] = yearly_comparison['偏差百分比(平均)'].round(2)
    
    st.dataframe(yearly_comparison, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 年度偏差走势
        fig_yearly = px.bar(yearly_avg, x='year', y='deviation_pct',
                           title='年度平均偏差百分比',
                           labels={'year': '年份', 'deviation_pct': '偏差百分比 (%)'},
                           color_discrete_sequence=['#4e73df'])
        
        # 添加趋势线
        fig_yearly.add_trace(
            go.Scatter(x=yearly_avg['year'], y=yearly_avg['deviation_pct'], 
                      mode='lines+markers', name='趋势线',
                      line=dict(color='red', width=2))
        )
        
        # 添加零线
        fig_yearly.add_hline(y=0, line_dash="dash", line_color="gray")
        
        st.plotly_chart(fig_yearly, use_container_width=True)
    
    with col2:
        # 计算各指标的同比变化率
        yearly_avg['actual_rate_yoy'] = yearly_avg['actual_rate'].pct_change() * 100
        yearly_avg['big_mac_rate_yoy'] = yearly_avg['big_mac_rate'].pct_change() * 100
        
        # 年度同比变化图
        fig_yoy = go.Figure()
        
        fig_yoy.add_trace(
            go.Scatter(x=yearly_avg['year'].dropna(), y=yearly_avg['actual_rate_yoy'].dropna(), 
                      mode='lines+markers', name='市场汇率变化率')
        )
        
        fig_yoy.add_trace(
            go.Scatter(x=yearly_avg['year'].dropna(), y=yearly_avg['big_mac_rate_yoy'].dropna(), 
                      mode='lines+markers', name='巨无霸汇率变化率')
        )
        
        # 添加零线
        fig_yoy.add_hline(y=0, line_dash="dash", line_color="gray")
        
        # 更新布局
        fig_yoy.update_layout(
            title='汇率年度变化率对比',
            xaxis_title='年份',
            yaxis_title='变化率 (%)',
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_yoy, use_container_width=True)
    
    # 替换固定的AI分析结果为AI交互区域
    st.markdown('<div class="sub-header">AI分析洞察</div>', unsafe_allow_html=True)
    
    # 收集指标数据用于AI分析
    metrics = {
        "data_period": f"{period_start} 至 {period_end}",
        "avg_deviation": avg_deviation,
        "max_deviation": filtered_data['deviation_pct'].max(),
        "min_deviation": filtered_data['deviation_pct'].min(),
        "latest_deviation": end_deviation,
        "over_under": "高估" if end_deviation > 0 else "低估"
    }
    
    # 添加提示词模板
    st.markdown("### 获取AI分析")
    
    prompt_template = f"""
    请基于以下中美汇率与巨无霸指数偏差数据进行经济分析：
    
    - 分析时间段: {metrics['data_period']}
    - 平均偏差百分比: {metrics['avg_deviation']:.2f}%
    - 最大偏差百分比: {metrics['max_deviation']:.2f}%
    - 最小偏差百分比: {metrics['min_deviation']:.2f}%
    - 最新偏差百分比: {metrics['latest_deviation']:.2f}%
    - 汇率状态: 人民币相对美元{metrics['over_under']}
    
    请分析：
    1. 根据巨无霸指数，人民币相对美元汇率的总体状况如何？是被高估还是低估？程度如何？
    2. 这种偏差的主要经济原因可能是什么？
    3. 这种现象与中国的经济政策和国际贸易地位有何关联？
    4. 巨无霸指数在预测中国汇率方面有哪些局限性？
    
    请给出专业、简洁的分析。
    """
    
    custom_prompt = st.text_area("自定义提示词（修改或使用默认）", prompt_template, height=300)
    
    if st.button("生成指标智能分析"):
        with st.spinner("AI正在分析数据..."):
            try:
                # 尝试使用真实API
                if api_key:
                    analysis_result = st.session_state.ai_analyzer._call_api(custom_prompt)
                else:
                    # 使用模拟数据进行演示
                    analysis_result = st.session_state.ai_analyzer.mock_analyze_metrics(metrics)
                
                # 显示分析结果
                st.markdown('<div class="analysis-result">', unsafe_allow_html=True)
                st.markdown(analysis_result)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 保存分析结果到会话状态
                st.session_state.metrics_analysis = analysis_result
                
                # 显示下载按钮
                if st.download_button(
                    label="下载分析结果",
                    data=analysis_result,
                    file_name="巨无霸指数指标分析.md",
                    mime="text/markdown"
                ):
                    st.success("分析结果下载成功！")
            except Exception as e:
                st.error(f"分析过程中出错: {str(e)}")

# 汇率政策与趋势选项卡
with tab2:
    st.markdown('<div class="sub-header">人民币汇率政策与偏差趋势分析</div>', unsafe_allow_html=True)
    
    # 偏差趋势图
    fig_trend = px.line(filtered_data, x='date', y='deviation_pct', 
                       title='人民币汇率偏差百分比趋势',
                       labels={'date': '日期', 'deviation_pct': '偏差百分比 (%)'},
                       color_discrete_sequence=['#4e73df'])
    
    # 添加零线
    fig_trend.add_hline(y=0, line_dash="dash", line_color="gray", 
                      annotation_text="无偏差线", 
                      annotation_position="bottom right")
    
    # 添加移动平均线
    ma_period = st.slider("移动平均周期", min_value=1, max_value=12, value=3)
    
    filtered_data['ma'] = filtered_data['deviation_pct'].rolling(window=ma_period).mean()
    fig_trend.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['ma'], 
                                  mode='lines', name=f'{ma_period}期移动平均线',
                                  line=dict(color='red', width=2)))
    
    # 添加重要汇率政策时间点
    policy_events = [
        {"date": "1994-01-01", "event": "官方汇率与市场汇率并轨", "description": "中国实施汇率并轨，人民币官方汇率与外汇调剂市场汇率并轨，实行以市场供求为基础的、单一的、有管理的浮动汇率制度。"},
        {"date": "2005-07-21", "event": "人民币汇率改革启动", "description": "中国开始实行以市场供求为基础、参考一篮子货币进行调节、有管理的浮动汇率制度。人民币兑美元汇率一次性升值2%。"},
        {"date": "2008-09-15", "event": "金融危机爆发", "description": "雷曼兄弟破产引发全球金融危机，中国暂停人民币升值进程，重新盯住美元以维持汇率稳定。"},
        {"date": "2010-06-19", "event": "重启汇改", "description": "中国央行宣布进一步推进人民币汇率形成机制改革，增强人民币汇率弹性。"},
        {"date": "2015-08-11", "event": "汇改扩大浮动区间", "description": "中国央行完善人民币兑美元汇率中间价报价机制，人民币汇率一次性贬值近2%，波动区间扩大。"},
        {"date": "2016-12-31", "event": "外汇储备下降与资本管制", "description": "面对外汇储备快速下降压力，中国加强资本流出管制，限制对外投资。"},
        {"date": "2018-01-01", "event": "中美贸易摩擦开始", "description": "中美贸易摩擦影响人民币汇率预期，汇率波动加大。"},
        {"date": "2019-08-05", "event": "人民币破7", "description": "人民币兑美元汇率突破7.0关口，为2008年以来首次。"},
        {"date": "2022-04-15", "event": "外汇存款准备金率下调", "description": "中国央行下调金融机构外汇存款准备金率，缓解人民币升值压力。"}
    ]
    
    # 将政策日期转换为pandas datetime，并筛选在显示时间范围内的事件
    policy_dates = []
    policy_names = []
    policy_details = []
    
    for event in policy_events:
        event_date = pd.Timestamp(event["date"])
        date_min = pd.Timestamp(filtered_data['date'].min())
        date_max = pd.Timestamp(filtered_data['date'].max())
        if event_date >= date_min and event_date <= date_max:
            policy_dates.append(event_date)
            policy_names.append(event["event"])
            policy_details.append(event["description"])
    
    # 添加政策事件标记
    for i, date in enumerate(policy_dates):
        # 找到最接近事件日期的数据点
        closest_date_idx = (filtered_data['date'] - date).abs().idxmin()
        closest_date = filtered_data.loc[closest_date_idx, 'date']
        y_value = filtered_data.loc[closest_date_idx, 'deviation_pct']
        
        # 添加事件标记
        fig_trend.add_annotation(
            x=closest_date,
            y=y_value,
            text=policy_names[i],
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor="#FF5733",
            ax=0,
            ay=-40,
            bgcolor="#FFF9E6",
            bordercolor="#FF5733",
            font=dict(size=10)
        )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # 汇率政策影响分析
    st.markdown("### 重要汇率政策影响分析")
    
    # 创建汇率政策时间轴
    if policy_dates:  # 如果有符合条件的政策事件
        for i, (date, event, description) in enumerate(zip(policy_dates, policy_names, policy_details)):
            st.markdown(f'<div class="policy-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="policy-title">{date.strftime("%Y年%m月%d日")} - {event}</div>', unsafe_allow_html=True)
            st.write(description)
            
            # 找到政策前后的数据进行对比分析
            policy_date = pd.Timestamp(date)
            date_min_plus = pd.Timestamp(filtered_data['date'].min() + pd.Timedelta(days=180))
            date_max_minus = pd.Timestamp(filtered_data['date'].max() - pd.Timedelta(days=180))
            
            # 政策前6个月和后6个月的数据
            if policy_date >= date_min_plus and policy_date <= date_max_minus:
                before_policy = filtered_data[(filtered_data['date'] >= policy_date - pd.Timedelta(days=180)) & 
                                           (filtered_data['date'] < policy_date)]
                after_policy = filtered_data[(filtered_data['date'] >= policy_date) & 
                                          (filtered_data['date'] < policy_date + pd.Timedelta(days=180))]
                
                if not before_policy.empty and not after_policy.empty:
                    before_avg = before_policy['deviation_pct'].mean()
                    after_avg = after_policy['deviation_pct'].mean()
                    change = after_avg - before_avg
                    
                    st.write(f"**政策影响分析：**")
                    st.write(f"- 政策前6个月平均偏差: {before_avg:.2f}%")
                    st.write(f"- 政策后6个月平均偏差: {after_avg:.2f}%")
                    st.write(f"- 变化: {change:.2f}% ({'上升' if change > 0 else '下降'})")
                    
                    # 简单解释
                    if abs(change) > 5:
                        st.write(f"- 评估: 该政策对人民币汇率偏差产生了**显著影响**")
                    elif abs(change) > 2:
                        st.write(f"- 评估: 该政策对人民币汇率偏差产生了**中等影响**")
                    else:
                        st.write(f"- 评估: 该政策对人民币汇率偏差影响**较小**")
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("所选时间范围内没有重要汇率政策事件")
    
    # 汇率制度概述
    st.markdown("### 中国汇率制度演变")
    
    st.markdown("""
    中国汇率制度大致经历了以下几个阶段：
    
    1. **1994年以前：**双轨制汇率体系，存在官方汇率和市场汇率
    2. **1994-2005：**单一的、有管理的浮动汇率制，实际上是盯住美元的固定汇率制
    3. **2005-2008：**有管理的浮动汇率制，参考一篮子货币，人民币开始升值
    4. **2008-2010：**全球金融危机期间，重新盯住美元
    5. **2010-2015：**重启汇改，扩大浮动区间，增强弹性
    6. **2015至今：**完善中间价形成机制，市场化程度提高，但仍保持有管理的浮动特征
    """)
    
    # 汇率政策与巨无霸指数偏差关系
    st.markdown('<div class="note-box">', unsafe_allow_html=True)
    st.markdown("**汇率政策与巨无霸指数偏差的关系：**", unsafe_allow_html=True)
    st.write("""
    1. 当中国实行较为固定的汇率制度时，巨无霸指数往往显示人民币被低估，这反映了政策性汇率与市场购买力之间的差距。
    
    2. 汇率改革后，随着人民币汇率弹性增加，巨无霸指数显示的低估程度逐渐减小，表明汇率更多地反映了市场因素。
    
    3. 外部冲击(如金融危机、贸易摩擦)往往导致汇率政策转向保守，此时巨无霸指数偏差可能会扩大。
    
    4. 自2015年汇改以来，人民币汇率形成机制市场化程度提高，但央行仍通过"逆周期因子"等工具对汇率进行管理，使巨无霸指数偏差呈现波动特征。
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # 替换固定的AI分析结果为AI交互区域
    st.markdown('<div class="sub-header">AI分析洞察</div>', unsafe_allow_html=True)
    
    # 提取时间周期和计算趋势指标
    start_year = filtered_data['date'].min().year
    end_year = filtered_data['date'].max().year
    
    # 计算趋势指标
    start_deviation = filtered_data.iloc[0]['deviation_pct']
    end_deviation = filtered_data.iloc[-1]['deviation_pct']
    change = end_deviation - start_deviation
    
    # 查找峰值和谷值
    peak = filtered_data['deviation_pct'].max()
    peak_date = filtered_data.loc[filtered_data['deviation_pct'].idxmax(), 'date'].strftime('%Y-%m-%d')
    trough = filtered_data['deviation_pct'].min()
    trough_date = filtered_data.loc[filtered_data['deviation_pct'].idxmin(), 'date'].strftime('%Y-%m-%d')
    
    # 获取政策事件数据用于AI分析
    policy_dates_str = []
    policy_events_str = []
    
    for i, (date, event, description) in enumerate(zip(policy_dates, policy_names, policy_details)):
        policy_dates_str.append(date.strftime('%Y-%m-%d'))
        policy_events_str.append(f"{event}：{description}")
    
    st.markdown("### 获取AI分析")
    
    # 根据图表和政策事件构建更具针对性的提示词
    if policy_dates:
        policy_events_text = "\n".join([f"- {date}: {event}" for date, event in zip(policy_dates_str, policy_events_str)])
        trend_prompt_template = f"""
        请基于以下人民币汇率政策与巨无霸指数偏差数据进行深入分析：

        ## 时间序列数据
        - 分析时间段: {filtered_data['date'].min().strftime('%Y-%m-%d')} 至 {filtered_data['date'].max().strftime('%Y-%m-%d')}
        - 初始偏差: {start_deviation:.2f}%
        - 最终偏差: {end_deviation:.2f}%
        - 总体变化: {change:.2f}% ({'上升' if change > 0 else '下降'})
        - 最高偏差: {peak:.2f}% (于 {peak_date})
        - 最低偏差: {trough:.2f}% (于 {trough_date})
        
        ## 时间段内的重要汇率政策事件
        {policy_events_text}
        
        请分析：
        1. 这些汇率政策事件如何影响了人民币汇率偏差？特别是分析政策前后的偏差变化。
        2. 哪些政策对汇率偏差产生了最显著的影响？为什么？
        3. 从汇率制度演变的角度，如何解释巨无霸指数偏差的长期趋势？
        4. 基于历史政策效果分析，对未来中国汇率政策有何建议？
        
        请给出专业、深入的分析，重点关注政策与汇率偏差的因果关系。
        """
    else:
        trend_prompt_template = f"""
        请基于以下人民币汇率与巨无霸指数偏差趋势数据进行分析：
        
        - 分析时间段: {filtered_data['date'].min().strftime('%Y-%m-%d')} 至 {filtered_data['date'].max().strftime('%Y-%m-%d')}
        - 初始偏差: {start_deviation:.2f}%
        - 最终偏差: {end_deviation:.2f}%
        - 总体变化: {change:.2f}% ({'上升' if change > 0 else '下降'})
        - 最高偏差: {peak:.2f}% (于 {peak_date})
        - 最低偏差: {trough:.2f}% (于 {trough_date})
        
        注意：在所选时间范围内未发现重要汇率政策事件。
        
        请分析：
        1. 在没有明显政策干预的情况下，哪些因素可能导致了观察到的汇率偏差变化？
        2. 这种相对稳定的政策环境对人民币汇率偏差产生了什么影响？
        3. 为什么某些时期即使没有明确的政策变化，汇率偏差仍会波动？
        4. 对于相对稳定的政策环境下的汇率管理，有哪些建议？
        
        请给出专业、简洁的分析，结合宏观经济视角解释观察到的趋势。
        """
    
    trend_custom_prompt = st.text_area("自定义提示词（修改或使用默认）", trend_prompt_template, height=300, key="trend_prompt")
    
    if st.button("生成趋势智能分析"):
        with st.spinner("AI正在分析趋势数据..."):
            try:
                # 尝试使用真实API
                if api_key:
                    trend_analysis = st.session_state.ai_analyzer._call_api(trend_custom_prompt)
                else:
                    # 使用模拟数据进行演示
                    trend_analysis = st.session_state.ai_analyzer.mock_analyze_trends(start_year, end_year)
                
                # 显示分析结果
                st.markdown('<div class="analysis-result">', unsafe_allow_html=True)
                st.markdown(trend_analysis)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 保存分析结果到会话状态
                st.session_state.trend_analysis = trend_analysis
                
                # 显示下载按钮
                if st.download_button(
                    label="下载趋势分析结果",
                    data=trend_analysis,
                    file_name="人民币汇率偏差趋势分析.md",
                    mime="text/markdown"
                ):
                    st.success("分析结果下载成功！")
            except Exception as e:
                st.error(f"分析过程中出错: {str(e)}")

# 显著变化点分析选项卡
with tab3:
    st.markdown('<div class="sub-header">巨无霸指数显著变化点分析</div>', unsafe_allow_html=True)
    
    st.write("本分析识别出人民币汇率偏差发生显著变化的时间点，帮助理解影响汇率偏差的关键事件。")
    
    # 计算偏差同比变化率和绝对变化量
    filtered_data['monthly_change'] = filtered_data['deviation_pct'].diff()
    filtered_data['abs_monthly_change'] = filtered_data['monthly_change'].abs()
    
    # 设置阈值 - 默认使用90%分位数，但允许用户调整
    change_threshold = st.slider(
        "变化量阈值百分位数", 
        min_value=80, 
        max_value=99, 
        value=90, 
        help="调整以识别更多或更少的显著变化点。较高的百分位数将识别出更少但更显著的变化点。"
    )
    
    threshold_value = filtered_data['abs_monthly_change'].quantile(change_threshold/100)
    st.write(f"当前阈值: 月度绝对变化量 > {threshold_value:.2f}%")
    
    # 识别变化显著的点
    significant_changes = filtered_data[filtered_data['abs_monthly_change'] > threshold_value].copy()
    
    if not significant_changes.empty:
        significant_changes = significant_changes.sort_values('date')
        
        # 图表可视化
        fig_changes = px.scatter(
            significant_changes, 
            x='date', 
            y='deviation_pct',
            size='abs_monthly_change',  # 气泡大小代表变化量
            color='monthly_change',  # 颜色代表变化方向
            color_continuous_scale=["red", "white", "green"],  # 红色代表负向变化，绿色代表正向变化
            size_max=20,
            title='人民币汇率偏差显著变化点',
            labels={
                'date': '日期',
                'deviation_pct': '偏差百分比 (%)',
                'abs_monthly_change': '变化绝对值 (%)',
                'monthly_change': '变化量 (%)'
            }
        )
        
        # 添加背景线
        fig_changes.add_trace(
            go.Scatter(
                x=filtered_data['date'],
                y=filtered_data['deviation_pct'],
                mode='lines',
                line=dict(color='lightgray', width=1),
                name='偏差趋势',
                hoverinfo='skip'
            )
        )
        
        # 添加零线
        fig_changes.add_hline(y=0, line_dash="dash", line_color="gray")
        
        # 更新布局
        fig_changes.update_layout(
            hovermode="closest",
            showlegend=True
        )
        
        st.plotly_chart(fig_changes, use_container_width=True)
        
        # 生成变化点表格
        st.markdown("### 显著变化点详情")
        
        # 为每个变化点添加方向和幅度描述
        significant_changes['方向'] = significant_changes['monthly_change'].apply(
            lambda x: '上升' if x > 0 else '下降'
        )
        significant_changes['变化幅度'] = significant_changes['abs_monthly_change'].apply(
            lambda x: '极大' if x > threshold_value * 2 else ('较大' if x > threshold_value * 1.5 else '显著')
        )
        
        # 显示表格
        display_df = significant_changes[['date', 'deviation_pct', 'monthly_change', '方向', '变化幅度']].rename(
            columns={
                'date': '日期', 
                'deviation_pct': '偏差百分比 (%)', 
                'monthly_change': '变化量 (%)'
            }
        ).sort_values('日期', ascending=False)
        
        # 格式化数值
        display_df['偏差百分比 (%)'] = display_df['偏差百分比 (%)'].round(2)
        display_df['变化量 (%)'] = display_df['变化量 (%)'].round(2)
        
        st.dataframe(display_df, use_container_width=True)
        
        # 突变分析
        st.markdown("### 变化点与重大事件对照分析")
        
        # 重大全球和中国经济事件时间表
        major_events = [
            {"date": "2007-08-09", "event": "全球金融危机初期", "category": "global", "description": "法国巴黎银行冻结三只投资基金，全球金融危机初现"},
            {"date": "2008-09-15", "event": "雷曼兄弟破产", "category": "global", "description": "雷曼兄弟申请破产保护，全球金融危机全面爆发"},
            {"date": "2010-05-02", "event": "欧债危机", "category": "global", "description": "希腊接受欧盟和IMF救助，欧债危机开始"},
            {"date": "2011-08-05", "event": "美国信用评级下调", "category": "global", "description": "标普下调美国主权信用评级，全球市场动荡"},
            {"date": "2015-08-11", "event": "人民币汇改", "category": "china", "description": "中国央行调整人民币中间价定价机制，人民币贬值2%"},
            {"date": "2016-06-24", "event": "英国脱欧公投", "category": "global", "description": "英国公投决定脱离欧盟，引发全球市场波动"},
            {"date": "2016-11-08", "event": "特朗普当选美国总统", "category": "global", "description": "特朗普当选美国总统，影响全球贸易和汇率预期"},
            {"date": "2018-03-22", "event": "中美贸易战开始", "category": "china", "description": "美国宣布对中国商品加征关税，中美贸易战开始"},
            {"date": "2019-08-05", "event": "人民币破7", "category": "china", "description": "人民币兑美元汇率突破7.0关口，为2008年以来首次"},
            {"date": "2020-03-11", "event": "新冠疫情全球大流行", "category": "global", "description": "世卫组织宣布新冠疫情为全球大流行，全球经济受到严重冲击"},
            {"date": "2022-02-24", "event": "俄乌冲突", "category": "global", "description": "俄罗斯对乌克兰发起军事行动，全球能源和商品市场剧烈波动"}
        ]
        
        # 将事件日期转换为pandas datetime格式
        for event in major_events:
            event["date"] = pd.Timestamp(event["date"])
        
        # 筛选在数据时间范围内的事件
        date_min = filtered_data['date'].min()
        date_max = filtered_data['date'].max()
        filtered_events = [
            event for event in major_events 
            if event["date"] >= date_min and event["date"] <= date_max
        ]
        
        # 创建一个变量存储所有nearby_events
        all_nearby_events = []
        
        # 对每个显著变化点，查找前后30天内发生的重大事件
        for i, row in significant_changes.iterrows():
            change_date = row['date']
            st.markdown(f'<div class="insight-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="insight-title">{change_date.strftime("%Y年%m月%d日")} - 偏差{row["方向"]}了 {abs(row["monthly_change"]):.2f}%</div>', unsafe_allow_html=True)
            
            # 找出该变化点前后30天内的事件
            nearby_events = [
                event for event in filtered_events
                if abs((event["date"] - change_date).days) <= 30
            ]
            
            # 添加到全局列表
            all_nearby_events.extend(nearby_events)
            
            if nearby_events:
                st.write("**可能相关的重大事件：**")
                for event in nearby_events:
                    event_date = event["date"].strftime("%Y年%m月%d日")
                    days_diff = (event["date"] - change_date).days
                    time_rel = "之前" if days_diff < 0 else "之后"
                    st.write(f"- **{event['event']}** ({event_date}，{abs(days_diff)}天{time_rel})：{event['description']}")
                
                # 简单分析
                china_events_nearby = any(event["category"] == "china" for event in nearby_events)
                if china_events_nearby:
                    st.write("👉 **分析：** 此变化点与中国国内政策或事件时间接近，可能存在直接关联。")
                else:
                    st.write("👉 **分析：** 此变化点与全球重大事件时间接近，可能受到国际因素影响。")
            else:
                st.write("在此变化点前后30天内未发现重大事件。可能是由于市场因素、季节性因素或未记录的政策变化导致。")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 变化点模式分析
        st.markdown("### 变化点模式分析")
        
        # 计算变化点的统计特征
        avg_magnitude = significant_changes['abs_monthly_change'].mean()
        pos_changes = significant_changes[significant_changes['monthly_change'] > 0]
        neg_changes = significant_changes[significant_changes['monthly_change'] < 0]
        pos_pct = len(pos_changes) / len(significant_changes) * 100 if len(significant_changes) > 0 else 0
        
        st.markdown('<div class="note-box">', unsafe_allow_html=True)
        st.write(f"**1. 整体模式：** 在所选时间范围内，共识别出 {len(significant_changes)} 个显著变化点，平均变化幅度为 {avg_magnitude:.2f}%。")
        st.write(f"**2. 变化方向：** {len(pos_changes)} 个向上变化点 ({pos_pct:.1f}%)，{len(neg_changes)} 个向下变化点 ({100-pos_pct:.1f}%)。")
        
        # 时间分布
        if len(significant_changes) >= 3:
            yearly_changes = significant_changes.groupby(significant_changes['date'].dt.year).size()
            most_volatile_year = yearly_changes.idxmax()
            yearly_changes_str = ", ".join([f"{year}年({count}次)" for year, count in yearly_changes.items()])
            st.write(f"**3. 时间分布：** 变化点在各年份的分布：{yearly_changes_str}，其中 {most_volatile_year}年 变化最为频繁。")
        
        # 关联分析
        if filtered_events:
            global_events = [e for e in filtered_events if e["category"] == "global"]
            china_events = [e for e in filtered_events if e["category"] == "china"]
            # 使用集合去重，避免重复计数
            unique_nearby_events = []
            if all_nearby_events:  # 确保all_nearby_events不为空
                unique_nearby_events = list({e["event"]: e for e in all_nearby_events}.values())
            st.write(f"**4. 事件关联：** 在这些变化点中，约有 {len(unique_nearby_events)} 个与重大事件时间接近，包括 {len(global_events)} 个全球事件和 {len(china_events)} 个中国事件。")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("在所选时间范围和阈值设置下未发现显著的变化点。")

    # 替换固定的AI分析结果为AI交互区域
    st.markdown('<div class="sub-header">AI分析洞察</div>', unsafe_allow_html=True)
    
    # 计算变化点的基本统计
    num_change_points = len(significant_changes) if not significant_changes.empty else 0
    
    st.markdown("### 获取AI分析")
    
    if num_change_points > 0:
        # 提取变化点详细数据用于AI分析
        change_points_data = []
        for _, row in significant_changes.iterrows():
            change_date = row['date'].strftime('%Y-%m-%d')
            deviation_value = round(row['deviation_pct'], 2)
            change_value = round(row['monthly_change'], 2)
            change_direction = row['方向']
            change_magnitude = row['变化幅度']
            
            # 查找相关事件
            related_events = []
            for event in filtered_events:
                if abs((event["date"] - row['date']).days) <= 30:
                    event_date = event["date"].strftime('%Y-%m-%d')
                    days_diff = (event["date"] - row['date']).days
                    time_rel = "之前" if days_diff < 0 else "之后"
                    related_events.append(f"{event['event']}({event_date}，{abs(days_diff)}天{time_rel})")
            
            events_str = "，".join(related_events) if related_events else "无明显相关事件"
            
            change_points_data.append(f"- {change_date}: 偏差为{deviation_value}%，{change_direction}了{abs(change_value)}%（{change_magnitude}）。相关事件：{events_str}")
        
        change_points_text = "\n".join(change_points_data)
        
        # 构建更具针对性的提示词
        change_prompt_template = f"""
        请基于以下人民币汇率偏差的显著变化点详细数据进行深入分析：
        
        ## 基本统计
        - 分析时间段: {filtered_data['date'].min().strftime('%Y-%m-%d')} 至 {filtered_data['date'].max().strftime('%Y-%m-%d')}
        - 识别出的显著变化点数量: {num_change_points}个
        - 平均变化幅度: {avg_magnitude:.2f}%
        - 上升变化点: {pos_changes}个
        - 下降变化点: {neg_changes}个
        
        ## 具体变化点及相关事件
        {change_points_text}
        
        ## 时间分布
        {yearly_changes_str if 'yearly_changes_str' in locals() else ''}
        
        请分析：
        1. 这些显著变化点与相关经济事件之间存在怎样的因果关系？是否能够观察到某些规律？
        2. 为什么有些重大事件会导致汇率偏差的显著变化，而有些则影响较小？
        3. 变化点的方向分布（上升vs下降）和时间分布反映了什么样的汇率调整模式？
        4. 基于这些变化点的分析，投资者和政策制定者应该如何预测和应对未来可能的汇率偏差波动？
        
        请进行专业、深入的分析，关注变化点的时序特征和经济含义。
        """
    else:
        # 构建无变化点的提示词
        change_prompt_template = f"""
        请分析以下情况：在对{filtered_data['date'].min().strftime('%Y-%m-%d')}至{filtered_data['date'].max().strftime('%Y-%m-%d')}期间的人民币汇率偏差数据进行分析时，使用{change_threshold}%分位数作为阈值（绝对变化量>{threshold_value:.2f}%），未发现显著的变化点。
        
        ## 数据基本特征
        - 时间段内偏差平均值: {filtered_data['deviation_pct'].mean():.2f}%
        - 时间段内偏差标准差: {filtered_data['deviation_pct'].std():.2f}%
        - 时间段内偏差范围: {filtered_data['deviation_pct'].min():.2f}% 至 {filtered_data['deviation_pct'].max():.2f}%
        - 时间段内变化量平均值: {filtered_data['monthly_change'].mean():.2f}%
        - 时间段内绝对变化量平均值: {filtered_data['abs_monthly_change'].mean():.2f}%
        
        请分析：
        1. 汇率偏差缺乏显著变化点可能反映了什么样的经济或政策环境？
        2. 这种相对平稳的变化模式对理解人民币汇率调整机制有何启示？
        3. 相对稳定的汇率偏差对中国经济和国际贸易有何影响？
        4. 如果降低阈值标准，哪些时间点可能会被识别为相对重要的变化点？为什么？
        5. 对投资者和政策制定者有何建议？
        
        请给出专业、深入的分析，关注数据稳定性背后的经济原因。
        """
    
    change_custom_prompt = st.text_area("自定义提示词（修改或使用默认）", change_prompt_template, height=300, key="change_prompt")
    
    if st.button("生成变化点智能分析"):
        with st.spinner("AI正在分析变化点数据..."):
            try:
                # 尝试使用真实API
                if api_key:
                    change_analysis = st.session_state.ai_analyzer._call_api(change_custom_prompt)
                else:
                    # 使用模拟数据进行演示
                    change_analysis = "这是变化点分析的示例结果。实际部署时，这里将显示AI根据变化点数据生成的分析内容。"
                
                # 显示分析结果
                st.markdown('<div class="analysis-result">', unsafe_allow_html=True)
                st.markdown(change_analysis)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 保存分析结果到会话状态
                st.session_state.change_analysis = change_analysis
                
                # 显示下载按钮
                if st.download_button(
                    label="下载变化点分析结果",
                    data=change_analysis,
                    file_name="人民币汇率显著变化点分析.md",
                    mime="text/markdown"
                ):
                    st.success("分析结果下载成功！")
            except Exception as e:
                st.error(f"分析过程中出错: {str(e)}")

# 修改页面底部提示
st.markdown("""
---
👉 **通过数据分析与AI洞察结合，您可以全面了解巨无霸指数反映的人民币汇率偏差状况及其背后的原因。请尝试使用提供的提示词模板，或根据您的需求自定义提示词，与AI互动获取更深入的分析。**
""") 