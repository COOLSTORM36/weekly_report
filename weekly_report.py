import streamlit as st
from pyfiglet import Figlet

st. set_page_config(layout="wide")

st.title("Hello")

f = Figlet(font='slant')
st.text(f.renderText('Hello, Streamlit!'))

st.text_input("Movie title", "Life of Brian")
