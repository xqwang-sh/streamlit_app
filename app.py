import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# 配置页面
st.set_page_config(
    page_title="巨无霸指数与中美汇率分析",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 添加CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 2rem;
    }
    .description {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .instruction {
        margin-top: 1rem;
        padding-left: 1rem;
        border-left: 3px solid #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

# 主页面
st.markdown("<h1 class='main-header'>巨无霸指数与中美汇率分析</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>国际金融课程互动分析平台</h2>", unsafe_allow_html=True)

# 介绍
st.markdown("""
<div class='instruction'>
欢迎使用<strong>巨无霸指数与中美汇率分析互动平台！</strong>

本应用基于《经济学人》的巨无霸指数，结合中美实际汇率数据，帮助您深入理解购买力平价理论在实践中的应用。

通过本平台，您可以：
<ul>
    <li>学习购买力平价理论和巨无霸指数的基本原理</li>
    <li>上传或使用内置的巨无霸指数和汇率数据进行分析</li>
    <li>通过可视化图表直观了解汇率偏差的变化趋势</li>
    <li>利用AI工具深入分析汇率偏差的经济原因</li>
    <li>导出分析结果用于课程报告撰写</li>
</ul>
</div>
""", unsafe_allow_html=True)

# 导航说明
st.markdown("""
<div class='instruction'>
<p><strong>使用指南</strong>：在左侧导航栏中，您可以找到以下功能页面：</p>
<ul>
    <li><strong>理论学习</strong> - 系统学习购买力平价理论和巨无霸指数的概念、计算方法及其局限性</li>
    <li><strong>数据导入</strong> - 上传巨无霸指数和汇率数据，或使用平台内置的示例数据</li>
    <li><strong>数据分析</strong> - 通过图表和AI分析工具，深入探究汇率偏差的经济含义</li>
</ul>
</div>
""", unsafe_allow_html=True)

# 开始使用
st.markdown("### 开始使用")
st.markdown("请按照左侧导航栏中的页面顺序，逐步完成分析任务。")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("第一步：学习理论知识", icon="📚")
with col2:
    st.info("第二步：导入分析数据", icon="📊")
with col3:
    st.info("第三步：深入数据分析", icon="🤖")

# 底部
st.markdown("---")
st.markdown("**国际金融课程** | 数据来源：《经济学人》巨无霸指数 & 中国人民银行汇率数据") 