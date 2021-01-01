import streamlit as st
from PIL import Image

def app():
    st.title('Breakdown by Race & Gender')
    st.write('In progress')
    
    # was bail paid?
    image = Image.open('figures/bail_paid_race.png')
    st.image(image)