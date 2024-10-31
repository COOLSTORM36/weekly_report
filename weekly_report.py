import streamlit as st
from datetime import datetime
from pyfiglet import Figlet
import time

st. set_page_config(layout="wide")

st.title("Hello")

f = Figlet(font='slant')
st.text(f.renderText('Solution Team'))




# Create a placeholder
placeholder = st.empty()

while True:
    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Update the placeholder with the current time
    placeholder.subheader(f"Current time: {current_time}")
    
    # Wait for 1 second before updating again
    time.sleep(1)
