import streamlit as st
from datetime import datetime
from pyfiglet import Figlet
import time

import os
import psutil
import pandas as pd

from datetime import datetime, timedelta

# imoport pyairtable
from pyairtable import Api
from pyairtable import Table
from pyairtable.formulas import match

st.set_page_config(layout="wide")

st.title("Hello")

AT_API_KEY = st.secrets["AT_API_KEY"]


# ------------------------------------------------------------------------------------------------
# import airtable API key

table = Table(AT_API_KEY, 'appyobVRNRPGJFNSV', 'tbl5trjDXTokyuUMF')

# ------------------------------------------------------------------------------------------------
# function to get the week of the date
def week_of_date(date):
    # Find the Monday of the current week
    start_of_week = date - timedelta(days=date.weekday())
    return f"Week of {start_of_week.strftime('%Y-%m-%d')}"

now = datetime.now()
formatted_date = week_of_date(now)

# ------------------------------------------------------------------------------------------------
# get the data from airtable
data = match({"Week": formatted_date})
result = table.all(formula=data)



# Extract fields and flatten the structure
flattened_data = []
for item in result:
    flat_item = item['fields']
    # Add the "产品变种 Variant Name" field if it doesn't exist
    if '产品变种 Variant Name' not in flat_item:
        flat_item['产品变种 Variant Name'] = ''
    flattened_data.append(flat_item)

# Convert to DataFrame
df = pd.DataFrame(flattened_data)
Prod_Doc_log = df.drop(columns=['Modify time', 'Week'])

# ------------------------------------------------------------------------------------------------
# Streamlit Framework
st.title("本周小组任务更新")
st.subheader(formatted_date)

# ------------------------------------------------------------------------------------------------
st.header("1. 产品规划路线图（Kayla）")
st.text_area("产品规划路线图更新", height=100)

# ------------------------------------------------------------------------------------------------
st.header("2. 关键需求管理（颖怡）")
st.subheader("a) RMT会议纪要")
st.text_area("RMT会议纪要", height=100)

# ------------------------------------------------------------------------------------------------
st.header("3. 样机管理(颖怡)")
st.text_area("样机管理更新", height=100)

# ------------------------------------------------------------------------------------------------
st.header("4. 测试计划路线图（穆朕）")
st.text_area("测试计划路线图更新", height=100)

# ------------------------------------------------------------------------------------------------
st.header("5. 市场洞察&产品资料库更新（Kayla&暐晟）")
st.subheader("a) 市场洞察")
st.text_area("市场洞察更新", height=100)
st.subheader("b) 产品资料库更新")
Prod_Doc_log.index = [''] * len(Prod_Doc_log)
st.dataframe(Prod_Doc_log)

# st.markdown("https://airtable.com/appyobVRNRPGJFNSV/shr80zbdjJbo8bKnn/tbl5trjDXTokyuUMF")
st.markdown('<a href="https://airtable.com/appyobVRNRPGJFNSV/shr80zbdjJbo8bKnn/tbl5trjDXTokyuUMF" target="_blank">Click here to Read More</a>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------------------------
st.header("6. 小组周主要任务更新")
st.text_area("小组周主要任务更新", height=150)

# ------------------------------------------------------------------------------------------------
# Add a button to stop the Streamlit server
# if st.button("停止服务器"):
#     st.warning("服务器即将停止...")
#     # Get the current process ID and terminate it
#     pid = os.getpid()
#     process = psutil.Process(pid)
#     process.terminate()
