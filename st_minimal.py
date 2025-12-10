import streamlit as st

st.title("Streamlit Minimal Test")

st.write("If you can see this in the browser, Streamlit + WebSocket is working correctly.")

number = st.slider("Pick a number", 0, 10, 5)
st.write("You picked:", number)
