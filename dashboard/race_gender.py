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
    st.image(Image.open('figures/race_aggregate_set.png'), width=imgWidth)
    
    st.subheader("Bail posted frequency")
    st.write("Overall, slightly over half of White and Black defendants posted bail (52.5% and 50.6% respsectively). White and Black defendants posted bail at similar rates for each range of bail amounts set.")    
    st.image(Image.open('figures/race_aggregate_bailPosted.png'), width=imgWidth)
    """
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
    """
    
    # ----------------------------------------
    # Matched analysis
    # ----------------------------------------
    st.header("Controlling for offense types")
    st.write(
    """While the above figures provide a useful year-end summary, they include variation in bail types and amounts that may be attributed to factors other than race, such as offense types. 
    
To control for offense types, we conducted a matched study where we sampled cases with identical lists of charges from cases with White and Black defendants. The following results were obtained from the 10593 cases (5115 for Black defendants, 5112 for White defendants) that were sampled. """
    )
        
    st.image(Image.open('figures/race_matched_type.png'), width=int(1.5*imgWidth))    
    st.image(Image.open('figures/race_matched_set.png'), width=imgWidth)    

    st.write("When comparing matched cases, there was no difference between bail types or bail amounts set for Black and White defendants.")
