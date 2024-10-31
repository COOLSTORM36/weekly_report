import streamlit as st
from pyfiglet import Figlet

st.title("Hello")

f = Figlet(font='slant')
st.text(f.renderText('Hello, Streamlit!'))
