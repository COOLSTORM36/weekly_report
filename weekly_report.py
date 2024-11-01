import streamlit as st
from datetime import datetime
from pyfiglet import Figlet
import time

st.set_page_config(layout="wide")

st.title("Hello")

st.title(st.secrets[AT_API_KEY])

# Create a placeholder
placeholder = st.empty()

while True:
    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Update the placeholder with the current time
    placeholder.markdown(f"<h2 style='text-align: center;'>Current UK time: {current_time}</h2>", unsafe_allow_html=True)
    
    # Wait for 1 second before updating again
    time.sleep(1)
