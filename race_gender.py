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
    st.write("In the following analysis, only defendants who have been labeled as White or Black are considered, due to sample size concerns.\
    Note: the Philadelphia Bail Fund has observed that the Philadelphia court system appears to record most non-Black and non-Asian people, such as Latinx and Indigenous people, as White.\
    Thus, while the label \"White\" is maintained in the charts, this group is referred to as \"non-Black\" in the text.")
    st.write("**<font color='red'>Question for PBF</font>**: what disclaimer language would you like to include here? The above was informed by the language in the July 2020 report.", unsafe_allow_html=True)
    st.write("Given the low frequency of nonmonetary and nominal bail (<1% of all cases), cases where these bail types were set are excluded from consideration in this section, for ease of interpretation.")
    
    st.subheader("Bail type frequency")
    st.write("Relative to non-Black defendants, Black defendants had monetary bail set more frequently, ROR bail set less frequently, and were more frequently denied bail.")
    st.image(Image.open('figures/race_aggregate_type.png'), width=int(1.5*imgWidth))

    st.subheader("Bail amount frequency")
    st.write("When monetary bail was set, non-Black defendants were more frequently assigned a bail amount between $10,000 and $25,000, and Black defendants were more frequently assigned a bail amount between $100,000 and $500,000.")
    st.image(Image.open('figures/race_aggregate_set.png'), width=imgWidth)
    
    st.subheader("Bail posted frequency")
    st.write("Overall, slightly over half of Black and non-Black defendants posted bail (50.6% and 52.5% respsectively), and defendants posted bail at similar rates for each range of bail amounts set, independent of race. The largest difference was for bail set below $1000, for which Black defendants posted bail at around half the rate of non-Black defendants.")    
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
    
To control for offense types, we conducted a matched study where we sampled cases with identical lists of charges from cases with Black and non-Black defendants. The following results were obtained from the 10593 cases (5115 for Black defendants, 5112 for White defendants) that were sampled.

In this matched sample, bail types and amounts were set at similar rates for Black and non-Black defendants, indicating that variations in these metrics between cases with the same charged offenses may be largely attributed to factors other than the defendant's race (such as the magistrate assigned to the case). """
    )
        
    st.image(Image.open('figures/race_matched_type.png'), width=int(1.5*imgWidth))    
    st.image(Image.open('figures/race_matched_set.png'), width=imgWidth)    
