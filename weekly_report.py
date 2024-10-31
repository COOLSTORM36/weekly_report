import streamlit as st
from pyfiglet import 

st.title("Hel")

f = Figlet(font='slant')
st.text(f.renderText('Hello, Streamlit!'))
