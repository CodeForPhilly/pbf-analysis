import streamlit as st
from PIL import Image

def app():
    st.title('Breakdown by Race & Gender')
    st.write('In progress')
    
    # Aggregate race statistics
    st.subheader("Percentage of bail type, by race")
    image = Image.open('figures/bail_type_by_race_pct.png')
    st.image(image, use_column_width=True)
    st.write("Compared to White defendants, Black defendants were less frequently granted ROR bail, which has no monetary payment stipulation, and were more frequently denied bail.")

    st.subheader("Percentage of bail amount, by race")
    image = Image.open('figures/bail_set_bin.png')
    st.image(image, use_column_width=True)
    st.write("When monetary bail is set, White defendants were more frequently assigned a bail amount between $10,000 and $25,000, and Black defendants were more frequently assigned a bail amount between $100,000 and $500,000.")
    
    # was bail paid?
    st.subheader("Percentage of bail paid, by race")
    image = Image.open('figures/bail_paid_race.png')
    st.image(image)