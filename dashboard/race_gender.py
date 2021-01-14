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
    
    # Matched analysis
    image = Image.open('figures/race_matched_type.png')
    st.image(image, use_column_width=True)    
    st.write("When comparing matched cases, there was no difference between bail types given to Black and White defendants.")
    
    st.subheader("Percentage of bail amount, by race")
    image = Image.open('figures/bail_set_bin.png')
    st.image(image, use_column_width=True)
    st.write("When monetary bail is set, White defendants were more frequently assigned a bail amount between $10,000 and $25,000, and Black defendants were more frequently assigned a bail amount between $100,000 and $500,000.")
    
    st.subheader("Percentage of bail paid, by race")
    image = Image.open('figures/bail_paid_race.png')
    st.image(image)
    
    st.markdown('*Breakdown By Bail Amount*')
    image = Image.open('figures/bail_paid_race_1k to 5k.png')
    st.image(image)
    image = Image.open('figures/bail_paid_race_5k to 10k.png')
    st.image(image)
    image = Image.open('figures/bail_paid_race_10k to 25k.png')
    st.image(image)
    image = Image.open('figures/bail_paid_race_25k to 50k.png')
    st.image(image)
    image = Image.open('figures/bail_paid_race_50k to 100k.png')
    st.image(image)
    image = Image.open('figures/bail_paid_race_100k to 500k.png')
    st.image(image)
    image = Image.open('figures/bail_paid_race_>=500k.png')
    st.image(image)
    
    st.write("Overall, 52.5% of White defendants paid bail while the percentage of Black defendants who were able to pay bail was 50.6%.")
    st.write("However, the assigned bail amount had an impact. For bail amounts under $50K, a higher percentage of Black defendants were able to pay bail compared to White defandents. This trend reversed when the bail amount was over $50K.")
