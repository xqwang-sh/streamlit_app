import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os
import sys
import matplotlib.pyplot as plt

# 页面配置
st.set_page_config(
    page_title="巨无霸指数与汇率理论学习",
    page_icon="📚",
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
    .concept {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
    }
    .concept-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .formula {
        background-color: #e6f3ff;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    .note-box {
        background-color: #fffacd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ffcc00;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 页面标题
st.markdown('<div class="main-header">巨无霸指数与购买力平价理论</div>', unsafe_allow_html=True)

st.write("本页面将介绍巨无霸指数的基本概念、计算方法以及其与购买力平价理论的关系，帮助您更好地理解后续的数据分析。")

# 介绍巨无霸指数
st.markdown('<div class="sub-header">1. 巨无霸指数简介</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    **巨无霸指数**（Big Mac Index）是由《经济学人》杂志在1986年创建的一个非正式指标，用于衡量各国货币的购买力平价。
    
    该指数基于一个简单的思想：在完全竞争的市场中，相同的商品在不同国家应该有相同的价格（以同一货币计算）。由于麦当劳的巨无霸汉堡在全球范围内都有销售，且产品相对标准化，因此被选为比较的基准商品。
    
    巨无霸指数是购买力平价理论的一种通俗化表达，它通过比较不同国家购买巨无霸汉堡所需的本国货币数量，来估算各国货币的"真实"汇率水平。
    """)
    
    st.markdown('<div class="note-box"><b>注意：</b> 巨无霸指数仅是一个参考指标，它简化了许多经济因素，并不能完全准确地反映货币的真实价值。但作为一个直观的比较工具，它确实为我们提供了理解汇率与购买力关系的简便方法。</div>', unsafe_allow_html=True)

with col2:
    # 在实际部署时，应使用真实图片路径
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Big_Mac_Index_2020.png/600px-Big_Mac_Index_2020.png", caption="巨无霸指数世界地图示例")

# 计算方法
st.markdown('<div class="sub-header">2. 巨无霸指数的计算方法</div>', unsafe_allow_html=True)

st.markdown("""
巨无霸指数的计算方法相对简单，主要基于以下步骤：

1. 收集各国以本国货币表示的巨无霸汉堡价格
2. 计算巨无霸汇率（隐含汇率）
3. 与实际市场汇率比较，计算货币的高估或低估程度
""")

st.markdown('<div class="formula">巨无霸汇率 = 本国巨无霸价格 ÷ 美国巨无霸价格</div>', unsafe_allow_html=True)

st.markdown('<div class="formula">货币高估/低估程度 = (巨无霸汇率 - 实际汇率) ÷ 实际汇率 × 100%</div>', unsafe_allow_html=True)

st.markdown("""
**例如：**

假设在中国购买一个巨无霸需要21元人民币，而在美国需要5美元。

- 巨无霸汇率 = 21元人民币 ÷ 5美元 = 4.2元人民币/美元
- 如果当前实际市场汇率是6.5元人民币/美元
- 那么人民币的低估程度 = (4.2 - 6.5) ÷ 6.5 × 100% = -35.4%

这表明，根据巨无霸指数，人民币相对于美元被低估了约35.4%。
""")

# 购买力平价理论
st.markdown('<div class="sub-header">3. 购买力平价理论</div>', unsafe_allow_html=True)

st.write("购买力平价(Purchasing Power Parity, PPP)理论是国际经济学中关于汇率决定的重要理论。")

col3, col4 = st.columns([1, 1])

with col3:
    st.markdown('<div class="concept"><div class="concept-title">绝对购买力平价</div>认为相同的商品篮子在不同国家应该有相同的价格（以同一货币计算）。如果不同，则表明货币被高估或低估。</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="concept"><div class="concept-title">相对购买力平价</div>关注的是价格变化率，认为汇率变化应该反映两国通货膨胀率的差异。</div>', unsafe_allow_html=True)

st.markdown("""
购买力平价理论的基础是"一价定律"（Law of One Price），即在没有交易成本和贸易壁垒的情况下，相同商品在不同市场应该以相同价格出售。

根据相对购买力平价理论，汇率变化应该反映两国通货膨胀率的差异：

""")

st.markdown('<div class="formula">汇率变化率 ≈ 国内通货膨胀率 - 国外通货膨胀率</div>', unsafe_allow_html=True)

# 巨无霸指数与购买力平价的关系
st.markdown('<div class="sub-header">4. 巨无霸指数与购买力平价的关系</div>', unsafe_allow_html=True)

st.markdown("""
巨无霸指数是购买力平价理论的一种简化应用：

- **理论基础相同**：都基于"一价定律"，认为相同商品应该有相同价格
- **简化操作**：巨无霸指数只使用单一商品作为比较基准，而非整个商品篮子
- **直观理解**：巨无霸指数提供了理解购买力平价的简单方式
- **实际应用**：尽管简化，巨无霸指数仍被广泛用于讨论货币估值问题
""")

# 局限性
st.markdown('<div class="sub-header">5. 巨无霸指数的局限性</div>', unsafe_allow_html=True)

st.markdown("""
尽管巨无霸指数提供了一种简便的方法来比较不同国家的购买力，但它存在一些明显的局限性：

1. **单一商品**：只基于一种商品，无法反映整体经济情况
2. **非贸易品因素**：忽略了非贸易品（如土地、劳动力）价格差异的影响
3. **市场定位差异**：麦当劳在不同国家的市场定位可能不同，如在一些发展中国家可能是相对高端消费
4. **成本结构差异**：不同国家的原材料成本、租金、工资水平存在差异
5. **税收影响**：未考虑不同国家的税收政策对价格的影响
6. **服务成本差异**：服务成分在巨无霸价格中所占比例在不同国家可能不同
7. **品牌价值差异**：不同市场对麦当劳品牌的估值可能不同
""")

st.markdown('<div class="note-box"><b>思考问题：</b> 在中国背景下，巨无霸指数在评估人民币汇率方面可能存在哪些特殊的局限性？这些因素如何影响指数的准确性？</div>', unsafe_allow_html=True)

# 巴拉萨-萨缪尔森效应
st.markdown('<div class="sub-header">6. 巴拉萨-萨缪尔森效应</div>', unsafe_allow_html=True)

st.markdown("""
**巴拉萨-萨缪尔森效应**（Balassa-Samuelson Effect）是解释为什么发展中国家的货币在购买力平价计算中往往显得被低估的一个重要理论。

该理论认为，在经济增长过程中，贸易品部门（如制造业）的生产率提高会推动该部门工资上升。由于劳动力可以在部门间流动，非贸易品部门（如服务业）的工资也会上升，但这部分生产率提升较少，导致非贸易品价格相对提高。

在发展中国家，贸易品与非贸易品的生产率差距通常大于发达国家，这使得按市场汇率计算时，发展中国家的物价水平（特别是服务类）相对较低，造成购买力平价计算中的"低估"现象。
""")

# 互动学习部分
st.markdown('<div class="sub-header">7. 互动练习</div>', unsafe_allow_html=True)

st.write("通过以下练习，加深对巨无霸指数和购买力平价理论的理解：")

# 简单计算练习
with st.expander("练习1：巨无霸汇率计算"):
    st.write("假设您有以下数据，请计算巨无霸汇率和货币高估/低估程度：")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        country = st.selectbox("选择国家", ["日本", "英国", "欧元区", "澳大利亚"])
        
        country_data = {
            "日本": {"price": 390, "currency": "日元", "exchange_rate": 110},
            "英国": {"price": 3.49, "currency": "英镑", "exchange_rate": 0.72},
            "欧元区": {"price": 4.1, "currency": "欧元", "exchange_rate": 0.85},
            "澳大利亚": {"price": 6.4, "currency": "澳元", "exchange_rate": 1.3}
        }
        
        us_price = st.number_input("美国巨无霸价格(美元)", value=5.0, min_value=0.0, max_value=100.0, step=0.1)
        local_price = st.number_input(f"{country}巨无霸价格({country_data[country]['currency']})", 
                                    value=float(country_data[country]["price"]), 
                                    min_value=0.0,
                                    max_value=1000.0,
                                    step=0.1)
        market_rate = st.number_input(f"市场汇率(1美元={country_data[country]['currency']})", 
                                    value=float(country_data[country]["exchange_rate"]), 
                                    min_value=0.0,
                                    max_value=1000.0,
                                    step=0.01)
    
    with col_b:
        if st.button("计算"):
            # 计算巨无霸汇率
            big_mac_rate = local_price / us_price
            
            # 计算高估/低估程度
            over_under = (big_mac_rate - market_rate) / market_rate * 100
            
            currency_status = "高估" if over_under > 0 else "低估"
            
            st.markdown(f"""
            ### 计算结果
            
            - 巨无霸汇率：1美元 = {big_mac_rate:.2f} {country_data[country]['currency']}
            - 市场汇率：1美元 = {market_rate:.2f} {country_data[country]['currency']}
            - {country}货币相对美元{currency_status}了 {abs(over_under):.2f}%
            """)
            
            # 可视化对比
            fig, ax = plt.subplots(figsize=(8, 5))
            bars = ax.bar(["巨无霸汇率", "市场汇率"], [big_mac_rate, market_rate], color=["#ff9999", "#66b3ff"])
            ax.set_ylabel(f"汇率(1美元兑换{country_data[country]['currency']})")
            ax.set_title(f"{country}货币汇率对比")
            
            # 添加数据标签
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f"{height:.2f}",
                        ha='center', va='bottom')
            
            st.pyplot(fig)

# 概念理解问题
with st.expander("练习2：理论理解"):
    st.write("测试你对购买力平价理论和巨无霸指数的理解：")
    
    q1 = st.radio(
        "1. 如果一个国家的货币根据巨无霸指数被低估30%，这意味着什么？",
        ["按照市场汇率，这个国家的巨无霸价格比美国贵30%",
         "按照市场汇率，这个国家的巨无霸价格比美国便宜30%",
         "该国实际汇率高于巨无霸汇率30%",
         "该国实际汇率低于巨无霸汇率30%"]
    )
    
    if q1 == "该国实际汇率高于巨无霸汇率30%":
        st.success("正确！货币被低估30%意味着实际市场汇率比巨无霸汇率高30%。")
    elif q1:
        st.error("不正确，请再思考一下。货币被低估意味着实际市场汇率比巨无霸汇率高。")
    
    q2 = st.radio(
        "2. 根据巴拉萨-萨缪尔森效应，为什么发展中国家的货币通常会表现为被低估？",
        ["因为发展中国家通常实行出口导向型经济政策，有意压低汇率",
         "因为发展中国家的贸易品与非贸易品部门的生产率差距通常大于发达国家",
         "因为《经济学人》杂志的数据收集方法有偏差",
         "因为发展中国家的麦当劳采用本地化原料，成本更低"]
    )
    
    if q2 == "因为发展中国家的贸易品与非贸易品部门的生产率差距通常大于发达国家":
        st.success("正确！巴拉萨-萨缪尔森效应解释了为什么经济发展中的国家随着贸易品部门生产率提高，会出现实际汇率升值现象。")
    elif q2:
        st.error("不正确，请再思考一下巴拉萨-萨缪尔森效应的核心机制。")

# 延伸资源
st.markdown('<div class="sub-header">8. 延伸学习资源</div>', unsafe_allow_html=True)

st.markdown("""
- [《经济学人》巨无霸指数官方页面](https://www.economist.com/big-mac-index)
- [国际货币基金组织：购买力平价解释](https://www.imf.org/external/pubs/ft/fandd/basics/ppp.htm)
- [世界银行：国际比较项目](https://www.worldbank.org/en/programs/icp)
- 推荐书籍：《国际金融新编》(姜波克)
- 推荐论文：Balassa, B. (1964). "The Purchasing-Power Parity Doctrine: A Reappraisal"
""")

# 总结
st.markdown('<div class="sub-header">总结</div>', unsafe_allow_html=True)

st.markdown("""
巨无霸指数作为购买力平价理论的一种通俗化表达，为我们提供了一种简单、直观的方法来比较不同国家货币的购买力。尽管它存在许多局限性，但作为一个经济学工具，它帮助我们更好地理解汇率、购买力和跨国价格比较的基本概念。

在接下来的分析中，我们将利用实际的巨无霸指数数据，结合中美汇率数据，来探究人民币汇率的估值状况及其历史变化趋势。
""")

# 引导用户进入下一步
st.markdown("""
---
👉 **完成理论学习后，您可以继续前往 [数据导入](/数据导入) 环节，开始实际的数据分析过程。**
""") 