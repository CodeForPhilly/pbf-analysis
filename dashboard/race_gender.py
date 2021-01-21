import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from PIL import Image

imgWidth = 450

def app():
    st.title('Breakdown by Race')
    
    # ----------------------------------------
    # Aggregate race statistics
    # ----------------------------------------
    st.header("Year-end Summary")

    st.image(Image.open('figures/race_aggregate_frequency.png'), width=500)      
    st.write("In the following analysis, we consider only defendants who have been labeled as White or Black due to sample size concerns.")
    
    st.subheader("Bail type frequency")
    st.image(Image.open('figures/race_aggregate_type.png'), width=int(1.5*imgWidth))
    st.write("Compared to White defendants, Black defendants were less frequently granted ROR bail, which has no monetary payment stipulation, and were more frequently denied bail.")

    st.subheader("Bail amount frequency")
    st.write("When monetary bail is set, White defendants were more frequently assigned a bail amount between $10,000 and $25,000, and Black defendants were more frequently assigned a bail amount between $100,000 and $500,000.")
    st.image(Image.open('figures/bail_set_bin.png'), width=imgWidth)
    
    st.subheader("Bail posted frequency")
    
    st.image(Image.open('figures/bail_paid_race.png'), width=imgWidth)
    
    st.image(Image.open('figures/bail_paid_race_1k to 5k.png'), width=imgWidth)
    st.image(Image.open('figures/bail_paid_race_5k to 10k.png'), width=imgWidth)
    st.image(Image.open('figures/bail_paid_race_10k to 25k.png'), width=imgWidth)
    st.image(Image.open('figures/bail_paid_race_25k to 50k.png'), width=imgWidth)
    st.image(Image.open('figures/bail_paid_race_50k to 100k.png'), width=imgWidth)
    st.image(Image.open('figures/bail_paid_race_100k to 500k.png'), width=imgWidth)
    st.image(Image.open('figures/bail_paid_race_>=500k.png'), width=imgWidth)
    
    st.write("Overall, 52.5% of White defendants paid bail while the percentage of Black defendants who were able to pay bail was 50.6%.")
    st.write("However, the assigned bail amount had an impact. For bail amounts under $50K, a higher percentage of Black defendants were able to pay bail compared to White defandents. This trend reversed when the bail amount was over $50K.")

    # ----------------------------------------
    # Matched analysis
    # ----------------------------------------
    st.header("Controlling for offense types")

    st.image(Image.open('figures/race_matched_type.png'), width=int(1.5*imgWidth))    
    st.image(Image.open('figures/race_matched_set.png'), width=imgWidth)    

    st.write("When comparing matched cases, there was no difference between bail types or bail amounts set for Black and White defendants.")
