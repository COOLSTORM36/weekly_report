import streamlit as st
from datetime import datetime
from pyfiglet import Figlet

st. set_page_config(layout="wide")

st.title("Hello")

f = Figlet(font='slant')
st.text(f.renderText('Solution Team'))




# Get the current time
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Display the current time in Streamlit
st.write("Current time:", current_time)
