import streamlit as st
import os

# 页面配置
st.set_page_config(
    page_title="国际金融课程互动分析平台",
    page_icon="📊",
    layout="wide"
)

# 自定义CSS
st.markdown("""
<style>
    /* 全局样式 */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* 主标题样式 */
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-align: center;
        color: #1a237e;
        padding: 2rem 0;
        background: linear-gradient(120deg, #e3f2fd, #bbdefb);
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* 欢迎文本样式 */
    .welcome-text {
        font-size: 1.6rem;
        color: #1E88E5;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* 内容块样式 */
    .content-block {
        margin-bottom: 1.5rem;
        padding: 0 1rem;
    }
    
    /* 功能列表样式 */
    .feature-list {
        margin-left: 1.5rem;
        line-height: 1.8;
    }
    
    /* 步骤区域样式 */
    .steps-container {
        display: flex;
        justify-content: space-between;
        gap: 2rem;
        margin: 1rem 0;
    }
    
    /* 步骤卡片样式 */
    .step-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .step-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: #1a237e;
    }
    
    .step-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1a237e;
        margin-bottom: 0.5rem;
    }
    
    .step-subtitle {
        font-size: 1.4rem;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .step-description {
        font-size: 1rem;
        color: #666;
    }
    
    /* 标题样式 */
    h1, h2, h3 {
        color: #1a237e;
        margin-bottom: 0.8rem;
    }
    
    /* 列表样式 */
    ul {
        list-style-type: none;
        padding-left: 1.5rem;
        margin: 0.5rem 0;
    }
    
    ul li {
        padding: 0.3rem 0;
        position: relative;
    }
    
    ul li:before {
        content: "•";
        color: #1E88E5;
        font-weight: bold;
        display: inline-block;
        width: 1em;
        margin-left: -1em;
    }

    /* 分隔线样式 */
    hr {
        margin: 1.5rem 0;
        border: 0;
        height: 1px;
        background: #e0e0e0;
    }

    /* 重要信息块样式 */
    .info-block {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 页面标题
st.markdown('<div class="main-header">国际金融课程互动分析平台</div>', unsafe_allow_html=True)

# 欢迎语
st.markdown('<div class="welcome-text">欢迎使用巨无霸指数与中美汇率分析互动平台！</div>', unsafe_allow_html=True)

# 项目简介
st.markdown('<div class="content-block">', unsafe_allow_html=True)
st.write("""
本应用基于《经济学人》的巨无霸指数，结合中美实际汇率数据，帮助您深入理解购买力平价理论在实践中的应用。
""")
st.markdown('</div>', unsafe_allow_html=True)

# 步骤展示
st.markdown('<div class="steps-container">', unsafe_allow_html=True)

# 第一步
st.markdown("""
<div class="step-card">
    <div class="step-icon">📚</div>
    <div class="step-title">第一步</div>
    <div class="step-subtitle">学习理论知识</div>
    <div class="step-description">系统掌握相关概念和方法</div>
</div>
""", unsafe_allow_html=True)

# 第二步
st.markdown("""
<div class="step-card">
    <div class="step-icon">📊</div>
    <div class="step-title">第二步</div>
    <div class="step-subtitle">导入分析数据</div>
    <div class="step-description">准备数据进行深入分析</div>
</div>
""", unsafe_allow_html=True)

# 第三步
st.markdown("""
<div class="step-card">
    <div class="step-icon">🔍</div>
    <div class="step-title">第三步</div>
    <div class="step-subtitle">深入数据分析</div>
    <div class="step-description">探索数据背后的经济含义</div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 功能介绍
st.markdown('<div class="content-block">', unsafe_allow_html=True)
st.markdown("### 🎯 通过本平台，您可以：")
st.markdown("""
- 学习购买力平价理论和巨无霸指数的基本原理
- 上传或使用内置的巨无霸指数和汇率数据进行分析
- 通过可视化图表直观了解汇率偏差的变化趋势
- 利用AI工具深入分析汇率偏差的经济原因
""")
st.markdown('</div>', unsafe_allow_html=True)

# 使用指南
st.markdown('<div class="content-block">', unsafe_allow_html=True)
st.markdown("### 📖 使用指南")
st.markdown("在左侧导航栏中，您可以找到以下功能页面：")
st.markdown("""
- 🎓 **理论学习** - 系统学习购买力平价理论和巨无霸指数的概念、计算方法及其局限性
- 📊 **数据预处理** - 上传巨无霸指数和汇率数据，或使用平台内置的示例数据
- 🔍 **AI数据分析** - 通过图表和AI分析工具，深入探究汇率偏差的经济含义
""")
st.markdown('</div>', unsafe_allow_html=True)

# 底部信息
st.markdown('<div class="info-block">', unsafe_allow_html=True)
st.markdown("### 📑 数据来源")
st.markdown("""
- 📰 巨无霸指数数据来自《经济学人》杂志
- 💹 汇率数据来自公开市场数据
""")

st.markdown("### 💡 使用提示")
st.markdown("""
1. 建议按照导航顺序依次浏览各个页面
2. 在数据分析和可视化页面，您可以使用交互式控件调整显示效果
3. 所有图表都支持放大和下载
""")
st.markdown('</div>', unsafe_allow_html=True) 