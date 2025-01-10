# import prerequisite
import streamlit as st
from datetime import datetime
from pyfiglet import Figlet
import time

import os
import pandas as pd

from datetime import datetime, timedelta

# imoport pyairtable
from pyairtable import Api
from pyairtable import Table
from pyairtable import Base
from pyairtable.formulas import match

st.set_page_config(layout="wide")

# ------------------------------------------------------------------------------------------------
# import airtable API key
AT_API_KEY = st.secrets["AT_API_KEY"]

# ------------------------------------------------------------------------------------------------
# import airtable API key, configure the table
auth_token = AT_API_KEY
api = Api(auth_token)
solution_base = Base(api, 'appyobVRNRPGJFNSV')
RMT_base = Base(api, 'appiPDknThxWdhHR2')
# ------------------------------------------------------------------------------------------------
# function to get the week of the date
def week_of_date(date):
    # Find the Monday of the current week
    start_of_week = date - timedelta(days=date.weekday())
    return f"Week of {start_of_week.strftime('%Y-%m-%d')}"

now = datetime.now()
formatted_date = week_of_date(now)

# ------------------------------------------------------------------------------------------------
# fetch the data from product roadmap
PRODUCT_ROADMAP_TAB = Table(None, solution_base, '欧洲产品路线图')
condition = match({"周报": True})
Product_Roadmap_result = PRODUCT_ROADMAP_TAB.all(formula=condition)

product_roadmap_flattened_data = []
for item in Product_Roadmap_result:
    flat_item = {
        '产品特性': item['fields'].get('产品特性', ''),
        '备注': item['fields'].get('备注', ''),
        '时间线备注': item['fields'].get('时间线备注', ''),
        '基线完成时间': item['fields'].get('基线完成时间', ''),
        '实际完成预估时间': item['fields'].get('实际完成预估时间', '')
    }
    product_roadmap_flattened_data.append(flat_item)

# Convert to DataFrame
product_roadmap_df = pd.DataFrame(product_roadmap_flattened_data)

try:
    Product_Roadmap = product_roadmap_df[['产品特性', '备注', '时间线备注', '基线完成时间', '实际完成预估时间']]
    Product_Roadmap = Product_Roadmap.sort_values(by=['产品特性'])
except KeyError:
    Product_Roadmap = product_roadmap_df

# fetch the data from RMT requirement list
RMT_TAB = Table(None, RMT_base, 'Requirement List')
condition = match({"RMT会议": True})
RMT_result = RMT_TAB.all(formula=condition)

RMT_flattened_data = []
for item in RMT_result:
    flat_item = item['fields']
    RMT_flattened_data.append(flat_item)

RMT_df = pd.DataFrame(RMT_flattened_data)

# Ensure columns '研发承诺时间.' and '预测交付时间.' exist in the DataFrame
columns_to_check = ['研发承诺时间.', '预测交付时间.', '研发进展更新']
for column in columns_to_check:
    if column not in RMT_df.columns:
        RMT_df[column] = ''

RMT_df['研发承诺时间.'] = RMT_df['研发承诺时间.'].fillna('')
RMT_df['预测交付时间.'] = RMT_df['预测交付时间.'].fillna('')
RMT_df['研发进展更新'] = RMT_df['研发进展更新'].fillna('')

priority_order = ["最高", "高", "中", "低"]
RMT_df['需求优先级'] = pd.Categorical(RMT_df['需求优先级 Priority'], categories=priority_order, ordered=True)

try:
    RMT = RMT_df[['需求简述 Requirement description', '国家/区域', 'Status Name', '需求优先级', '研发进展更新', '研发承诺时间.', '预测交付时间.']]
except KeyError:
    RMT = RMT_df

RMT = RMT.sort_values(by=['国家/区域', 'Status Name', '需求优先级'], ascending=[True, False, True])

# fetch the data from market insight
MARKET_INSIGHT_TAB = Table(None, solution_base, '市场洞察')
data = match({"Week": formatted_date})
Market_Insight_result = MARKET_INSIGHT_TAB.all(formula=data)

market_insight_flattened_data = []
for item in Market_Insight_result:
    flat_item = item['fields']
    market_insight_flattened_data.append(flat_item)

# Convert to DataFrame
market_insight_df = pd.DataFrame(market_insight_flattened_data)
try:
    if 'Attachment' in market_insight_df.columns and market_insight_df['Attachment'].notnull().any():
        Market_Insight = market_insight_df.drop(columns=['Attachment', 'Link to Details', '领域分类', '中文详情','English Summary', 'English Title', '输入人', 'Ready', '记录日期', 'Week', '周报？'])
    else:
        Market_Insight = market_insight_df.drop(columns=['Link to Details', '领域分类', '中文详情', 'English Summary', 'English Title', '输入人', 'Ready', '记录日期', 'Week', '周报？'])
except KeyError:
    Market_Insight = market_insight_df

# fetch the data from products doc log
PROD_DOC_LOG_TAB = Table(None, solution_base, '产品资料库更新LOG')
data = match({"Week": formatted_date})
Prod_Doc_log_result = PROD_DOC_LOG_TAB.all(formula=data)

prod_doc_log_flattened_data = []
try:
    for item in Prod_Doc_log_result:
        flat_item = item['fields']
        # Add the "产品变种 Variant Name" field if it doesn't exist
        if '产品变种 Variant Name' not in flat_item:
            flat_item['产品变种 Variant Name'] = ''
        if '文件种类 Category' not in flat_item:
            flat_item['文件种类 Category'] = ''
        if '语言 Locale' not in flat_item:
            flat_item['语言 Locale'] = ''
        prod_doc_log_flattened_data.append(flat_item)
except KeyError:
    prod_doc_log_flattened_data = []

# Convert to DataFrame
prod_doc_log_df = pd.DataFrame(prod_doc_log_flattened_data)
try:
    Prod_Doc_log = prod_doc_log_df.drop(columns=['Modify time', 'Week', '产品变种 Variant Name'])
except KeyError:
    Prod_Doc_log = prod_doc_log_df

# fetch the data from weekly task update
WEEKLY_TASK_UPDATE_TAB = Table(None, solution_base, '团队任务')
data = match({"周报": True})
Weekly_Task_Update_result = WEEKLY_TASK_UPDATE_TAB.all(formula=data)

weekly_task_update_flattened_data = []
for item in Weekly_Task_Update_result:
    flat_item = item['fields']
    weekly_task_update_flattened_data.append(flat_item)

Weekly_Task_Update_df = pd.DataFrame(weekly_task_update_flattened_data)
try:
    Weekly_Task_Update = Weekly_Task_Update_df['RAID Item']
except KeyError:
    Weekly_Task_Update = Weekly_Task_Update_df
    
# ------------------------------------------------------------------------------------------------
# Streamlit Framework
st.title("本周小组任务更新")
st.subheader(formatted_date)

st.text("")
st.text("")
st.text("""Hi Bruce，

以下是小组本周任务更新：""")
# ------------------------------------------------------------------------------------------------
st.header("1. 产品规划路线图（Kayla）")
# st.dataframe(Product_Roadmap, hide_index=True, use_container_width=True)
st.table(Product_Roadmap)
st.markdown('Click <a href="https://airtable.com/appyobVRNRPGJFNSV/pag9rGZ4MM7Iy4LjG" target="_blank">here</a> to Read More', unsafe_allow_html=True)

# ------------------------------------------------------------------------------------------------
st.header("2. 关键需求管理（Kayla）")
st.subheader("a) RMT会议纪要")
RMT.index = [''] * len(RMT)
st.table(RMT)

# ------------------------------------------------------------------------------------------------
st.header("3. 样机管理(Kayla & Weisheng)")

st.markdown('Click <a href="https://airtable.com/appyobVRNRPGJFNSV/pagSix3iZiaXnRkiv" target="_blank">here</a> to Read More', unsafe_allow_html=True)
# ------------------------------------------------------------------------------------------------
st.header("4. 测试计划路线图（穆朕）")

# st.markdown('Click <a href="https://airtable.com/appyobVRNRPGJFNSV/tblfjX58nWhlgQxZE/viwU3pRonYTG6REhB?blocks=hide" target="_blank">here</a> to Read More', unsafe_allow_html=True)

# ------------------------------------------------------------------------------------------------
st.header("5. 市场洞察&产品资料库更新（Kayla & Weisheng）")
st.subheader("a) 市场洞察")
# st.dataframe(Market_Insight, hide_index=True, use_container_width=True)
Market_Insight.index = [''] * len(Market_Insight)
st.table(Market_Insight)

st.text("Read more:")
st.markdown('<a href="https://airtable.com/appkXGg44hvl2aahl/shrIlvjhIxdF9tVVk" target="_blank">中文版本</a>', unsafe_allow_html=True)
st.markdown('<a href="https://airtable.com/appkXGg44hvl2aahl/shrqVDDCURO8T5SKa" target="_blank">English Version</a>', unsafe_allow_html=True)

st.subheader("b) 产品资料库更新")
# st.dataframe(Prod_Doc_log, hide_index=True, use_container_width=True)
Prod_Doc_log.index = [''] * len(Prod_Doc_log)
st.table(Prod_Doc_log)

# st.markdown("https://airtable.com/appyobVRNRPGJFNSV/shr80zbdjJbo8bKnn/tbl5trjDXTokyuUMF")
st.markdown('Click <a href="https://airtable.com/appyobVRNRPGJFNSV/shrZdNUfuawVDC9Xg" target="_blank">here</a> to Read More', unsafe_allow_html=True)

# ------------------------------------------------------------------------------------------------
st.header("6. 小组周主要任务更新")
Weekly_Task_Update.index = [''] * len(Weekly_Task_Update)
st.table(Weekly_Task_Update)

# ------------------------------------------------------------------------------------------------
st.text("")
st.text("""谢谢。

祝好，

周末愉快。""")

# ------------------------------------------------------------------------------------------------
# Hide index from the table

# Inject custom JavaScript to hide the index column
hide_index_js = """
<script>
    const tables = window.parent.document.querySelectorAll('table');
    tables.forEach(table => {
        const indexColumn = table.querySelector('thead th:first-child');
        if (indexColumn) {
            indexColumn.style.display = 'none';
        }
        const indexCells = table.querySelectorAll('tbody th');
        indexCells.forEach(cell => {
            cell.style.display = 'none';
        });
    });
</script>
"""

# Use components.html to inject the JavaScript
st.components.v1.html(hide_index_js, height=0)

# ------------------------------------------------------------------------------------------------
# Add a button to stop the Streamlit server
# if st.button("停止服务器"):
#     st.warning("服务器即将停止...")
#     # Get the current process ID and terminate it
#     pid = os.getpid()
#     process = psutil.Process(pid)
#     process.terminate()
