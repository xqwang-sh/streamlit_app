import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_processor import DataProcessor

# 页面配置
st.set_page_config(
    page_title="数据预处理 - 巨无霸指数分析",
    page_icon="📊",
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
    .data-info {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    .note-box {
        background-color: #e7f3fe;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #2196f3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 页面标题
st.markdown('<div class="main-header">数据预处理</div>', unsafe_allow_html=True)

st.write("在这个环节中，您可以选择使用内置数据或上传自己的数据进行分析。")

# 初始化会话状态变量
if 'bigmac_data' not in st.session_state:
    st.session_state.bigmac_data = None
if 'exchange_rate_data' not in st.session_state:
    st.session_state.exchange_rate_data = None
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None

# 导航选项卡
tab1, tab2, tab3 = st.tabs(["数据导入", "数据预览", "数据预处理"])

# 数据导入选项卡
with tab1:
    st.markdown('<div class="sub-header">选择数据来源</div>', unsafe_allow_html=True)
    
    # 选择数据来源
    data_source = st.radio(
        "请选择数据来源",
        ["使用内置数据", "上传自定义数据"],
        help="内置数据包含示例巨无霸指数和汇率数据，您也可以上传自己的数据进行分析。"
    )
    
    if data_source == "使用内置数据":
        st.markdown('<div class="note-box">您选择了使用内置数据，这将使用示例数据进行演示。</div>', unsafe_allow_html=True)
        
        if st.button("加载内置数据"):
            try:
                # 使用数据处理器加载内置数据
                processor = st.session_state.data_processor
                
                # 加载内置数据
                bigmac_data = processor.load_builtin_bigmac_data()
                exchange_rate_data = processor.load_builtin_exchange_rate_data()
                
                # 保存到会话状态
                st.session_state.bigmac_data = bigmac_data
                st.session_state.exchange_rate_data = exchange_rate_data
                
                st.markdown('<div class="success-box">✅ 内置数据加载成功！</div>', unsafe_allow_html=True)
                st.markdown("您现在可以切换到 **数据预览** 选项卡查看数据，或者继续进行数据预处理。")
                
                # 启用数据预览页面
                st.session_state.data_loaded = True
                
            except Exception as e:
                st.error(f"加载内置数据时出错: {str(e)}")
                st.session_state.data_loaded = False
    
    else:
        st.markdown('<div class="sub-header">上传数据</div>', unsafe_allow_html=True)
        
        # 巨无霸数据上传
        st.markdown('<div class="sub-header">上传巨无霸指数数据</div>', unsafe_allow_html=True)
        st.markdown("""
        请上传包含巨无霸指数数据的CSV文件。文件应包含以下列：
        - date: 日期
        - iso_a3: 国家代码
        - currency_code: 货币代码
        - name: 国家名称
        - local_price: 当地货币价格
        - dollar_ex: 兑美元汇率
        - dollar_price: 美元价格
        """)
        
        # 提供数据获取指导
        st.markdown('<div class="note-box">您可以从《经济学人》网站获取巨无霸指数数据：<a href="https://github.com/TheEconomist/big-mac-data" target="_blank">The Economist Big Mac Index Data</a></div>', unsafe_allow_html=True)
        
        uploaded_bigmac = st.file_uploader("选择巨无霸指数数据文件", type=["csv"])
        
        # 汇率数据上传
        st.markdown('<div class="sub-header">上传汇率数据</div>', unsafe_allow_html=True)
        st.markdown("""
        请上传包含汇率数据的Excel或CSV文件。文件应包含以下列：
        - date: 日期
        - actual_rate 或 actual_rates: 美元兑人民币汇率
        
        或者包含可识别的日期列和汇率列（包含"日期"或"date"，"汇率"或"rate"关键词）
        """)
        
        # 提供数据获取指导
        st.markdown('<div class="note-box">您可以从中国人民银行网站或国际金融数据库中获取汇率数据</div>', unsafe_allow_html=True)
        
        uploaded_exchange = st.file_uploader("选择汇率数据文件", type=["xlsx", "xls", "csv"])
        
        # 处理上传的数据
        if uploaded_bigmac is not None and uploaded_exchange is not None:
            if st.button("处理上传的数据"):
                try:
                    # 使用数据处理器加载上传的数据
                    processor = st.session_state.data_processor
                    
                    # 处理巨无霸数据
                    bigmac_data = processor.load_bigmac_data(uploaded_bigmac)
                    
                    # 处理汇率数据
                    exchange_rate_data = processor.load_exchange_rate_data(uploaded_exchange)
                    
                    # 保存到会话状态
                    st.session_state.bigmac_data = bigmac_data
                    st.session_state.exchange_rate_data = exchange_rate_data
                    
                    st.markdown('<div class="success-box">✅ 数据上传并处理成功！</div>', unsafe_allow_html=True)
                    st.markdown("您现在可以切换到 **数据预览** 选项卡查看数据，或者继续进行数据预处理。")
                    
                    # 启用数据预览页面
                    st.session_state.data_loaded = True
                    
                except Exception as e:
                    st.error(f"处理上传的数据时出错: {str(e)}")
                    st.session_state.data_loaded = False
        else:
            st.info("请上传巨无霸指数数据和汇率数据文件后继续。")

# 数据预览选项卡
with tab2:
    if 'data_loaded' in st.session_state and st.session_state.data_loaded:
        st.markdown('<div class="sub-header">巨无霸指数数据预览</div>', unsafe_allow_html=True)
        
        if st.session_state.bigmac_data is not None:
            # 显示基本信息
            df_bigmac = st.session_state.bigmac_data
            
            st.markdown('<div class="data-info">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("数据行数", f"{len(df_bigmac):,}")
            with col2:
                st.metric("开始日期", df_bigmac['date'].min().strftime('%Y-%m-%d'))
            with col3:
                st.metric("结束日期", df_bigmac['date'].max().strftime('%Y-%m-%d'))
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 预览数据
            st.dataframe(df_bigmac.head(10), use_container_width=True)
            
            # 可视化巨无霸价格趋势
            st.markdown("### 中国巨无霸价格趋势")
            
            # 过滤中国数据
            china_data = df_bigmac.copy()
            
            if not china_data.empty:
                fig = px.line(china_data, x='date', y=['local_price', 'dollar_price'], 
                              title='中国巨无霸价格趋势',
                              labels={
                                  'date': '日期',
                                  'value': '价格',
                                  'variable': '价格类型'
                              },
                              color_discrete_map={
                                  'local_price': '#1f77b4',  # 人民币价格颜色
                                  'dollar_price': '#ff7f0e'  # 美元价格颜色
                              })
                
                fig.update_layout(legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ))
                
                # 修改图例标签
                newnames = {'local_price': '人民币价格', 'dollar_price': '美元价格'}
                fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("找不到中国的巨无霸数据，无法生成趋势图。")
        
        st.markdown('<div class="sub-header">汇率数据预览</div>', unsafe_allow_html=True)
        
        if st.session_state.exchange_rate_data is not None:
            # 显示基本信息
            df_fx = st.session_state.exchange_rate_data
            
            st.markdown('<div class="data-info">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("数据行数", f"{len(df_fx):,}")
            with col2:
                st.metric("开始日期", df_fx['date'].min().strftime('%Y-%m-%d'))
            with col3:
                st.metric("结束日期", df_fx['date'].max().strftime('%Y-%m-%d'))
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 预览数据
            st.dataframe(df_fx.head(10), use_container_width=True)
            
            # 可视化汇率趋势
            st.markdown("### 美元兑人民币汇率趋势")
            
            # 获取汇率列名
            rate_col = 'actual_rate' if 'actual_rate' in df_fx.columns else 'actual_rates'
            
            fig = px.line(df_fx, x='date', y=rate_col, 
                          title='美元兑人民币汇率历史走势',
                          labels={
                              'date': '日期',
                              rate_col: '美元兑人民币汇率'
                          },
                          color_discrete_sequence=['#2ca02c'])
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("请先在 '数据导入' 选项卡中上传数据。")

# 数据预处理选项卡
with tab3:
    if 'data_loaded' in st.session_state and st.session_state.data_loaded:
        st.markdown('<div class="sub-header">数据预处理</div>', unsafe_allow_html=True)
        
        st.write("在这个步骤中，我们将对上传的数据进行预处理，包括：")
        st.write("1. 筛选中国数据")
        st.write("2. 合并巨无霸指数和汇率数据")
        st.write("3. 计算巨无霸汇率和汇率偏差")
        st.write("4. 分析结果")
        
        if st.button("执行数据预处理"):
            try:
                # 获取数据处理器
                processor = st.session_state.data_processor
                
                # 执行分析
                comparison_data = processor.analyze_data()
                
                # 保存分析结果到会话状态
                st.session_state.analysis_data = comparison_data
                
                st.markdown('<div class="success-box">✅ 数据预处理成功！</div>', unsafe_allow_html=True)
                
                # 显示结果预览
                st.markdown("### 分析结果预览")
                st.dataframe(comparison_data.head(10), use_container_width=True)
                
                # 可视化巨无霸汇率与实际汇率对比
                st.markdown("### 巨无霸汇率与实际汇率对比")
                
                fig_rates = px.line(comparison_data, x='date', y=['big_mac_rate', 'actual_rate'],
                                   title='巨无霸汇率 vs 实际市场汇率',
                                   labels={
                                       'date': '日期',
                                       'value': '汇率 (CNY/USD)',
                                       'variable': '汇率类型'
                                   },
                                   color_discrete_map={
                                       'big_mac_rate': '#1f77b4',  # 巨无霸汇率颜色
                                       'actual_rate': '#ff7f0e'    # 实际汇率颜色
                                   })
                
                fig_rates.update_layout(legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ))
                
                # 修改图例标签
                newnames = {'big_mac_rate': '巨无霸指数汇率', 'actual_rate': '实际市场汇率'}
                fig_rates.for_each_trace(lambda t: t.update(name = newnames[t.name]))
                
                st.plotly_chart(fig_rates, use_container_width=True)
                
                # 计算巨无霸汇率指标
                avg_bigmac_rate = comparison_data['big_mac_rate'].mean()
                latest_bigmac_rate = comparison_data.iloc[-1]['big_mac_rate']
                latest_actual_rate = comparison_data.iloc[-1]['actual_rate']
                
                # 显示巨无霸汇率指标
                st.markdown("### 巨无霸汇率指标")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("平均巨无霸汇率", f"{avg_bigmac_rate:.4f}")
                with col2:
                    st.metric("最新巨无霸汇率", f"{latest_bigmac_rate:.4f}")
                with col3:
                    st.metric("最新实际汇率", f"{latest_actual_rate:.4f}")
                
                # 可视化汇率偏差
                st.markdown("### 人民币汇率偏差百分比")
                
                fig = px.line(comparison_data, x='date', y='deviation_pct', 
                              title='人民币相对美元的汇率偏差百分比',
                              labels={
                                  'date': '日期',
                                  'deviation_pct': '偏差百分比 (%)'
                              },
                              color_discrete_sequence=['#d62728'])
                
                # 添加零线
                fig.add_hline(y=0, line_dash="dash", line_color="gray", 
                              annotation_text="无偏差线", 
                              annotation_position="bottom right")
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 计算关键指标
                avg_deviation = comparison_data['deviation_pct'].mean()
                max_deviation = comparison_data['deviation_pct'].max()
                min_deviation = comparison_data['deviation_pct'].min()
                latest_deviation = comparison_data.iloc[-1]['deviation_pct']
                
                st.markdown("### 关键指标")
                
                # 创建指标展示
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("平均偏差", f"{avg_deviation:.2f}%")
                with col2:
                    st.metric("最大偏差", f"{max_deviation:.2f}%")
                with col3:
                    st.metric("最小偏差", f"{min_deviation:.2f}%")
                with col4:
                    st.metric("最新偏差", f"{latest_deviation:.2f}%")
                
                # 判断高估还是低估
                over_under = "高估" if latest_deviation > 0 else "低估"
                over_under_color = "#d62728" if latest_deviation > 0 else "#2ca02c"
                
                st.markdown(f"""
                <div style="text-align: center; margin: 2rem 0; font-size: 1.5rem;">
                    根据巨无霸指数，人民币相对美元<span style="color: {over_under_color}; font-weight: bold;">{over_under}</span>了<span style="color: {over_under_color}; font-weight: bold;">{abs(latest_deviation):.2f}%</span>
                </div>
                """, unsafe_allow_html=True)
                
                # 保存关键指标到会话状态
                st.session_state.metrics = {
                    'avg_deviation': avg_deviation,
                    'max_deviation': max_deviation,
                    'min_deviation': min_deviation,
                    'latest_deviation': latest_deviation,
                    'over_under': over_under,
                    'data_period': f"{comparison_data['date'].min().strftime('%Y-%m-%d')} 至 {comparison_data['date'].max().strftime('%Y-%m-%d')}"
                }
                
                # 导出选项
                st.markdown("### 导出数据")
                
                if st.download_button(
                    label="下载分析结果为Excel",
                    data=processor.export_analysis_data(comparison_data),
                    file_name="巨无霸指数分析结果.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ):
                    st.success("数据导出成功！")
                
            except Exception as e:
                st.error(f"数据预处理出错: {str(e)}")
        
        # 引导用户进入下一步
        if 'analysis_data' in st.session_state and st.session_state.analysis_data is not None:
            st.markdown("""
            ---
            👉 **数据预处理完成！您现在可以前往 [数据分析](/数据分析) 页面进行更深入的分析。**
            """)
    else:
        st.info("请先在 '数据导入' 选项卡中上传数据。") 