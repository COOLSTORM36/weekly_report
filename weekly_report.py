import streamlit as st
from pyfiglet import Figlet

st. set_page_config(layout="wide")

st.title("Hello")

f = Figlet(font='slant')
st.text(f.renderText('Hello, Streamlit!'))


# Check if the user is the owner
is_owner = st.session_state.get('is_owner', False)

# Define a function to check if the user is the owner
def is_owner():
    # Replace with your logic to determine if the user is the owner
    return st.session_state.get('is_owner', False)

# Initialize session state
if 'is_owner' not in st.session_state:
    st.session_state.is_owner = False

# Create a text area that is editable for the owner and read-only for others
text = st.text_area("Enter your text here:", "This is a sample text.", disabled=not is_owner())

# Display the text
st.write("You entered:", text)

# Button to toggle edit mode (for demonstration purposes)
if st.button("Toggle Edit Mode"):
    st.session_state.is_owner = not st.session_state.is_owner
