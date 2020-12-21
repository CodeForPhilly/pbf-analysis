import streamlit as st
from PIL import Image

def app():
    st.title('Breakdown by Magistrate')
    st.write('In progress')

    ### 2020 Summary plots

    # !!!!! TODO !!!!!
    # Explain selection of magistrates (Those who handled more than 500 cases)
    # Some timeline (Many were involved consistently throughout the year. Some were seasonal)
    # Explain 'Others': Those who set fewer than 500 cases. Total number of those labeled as "Others"

    # number of cases
    st.header("Year End Summary by Magistrate")
    st.subheader("Number of cases handled by each magistrate")
    image = Image.open('figures/magistrate_case_count.png')
    st.image(image)
    # bail type
    st.subheader("Percentage of bail type for each magistrate")
    image = Image.open('figures/magistrate_type_summary.png')
    st.image(image, use_column_width=True)
    # bail amount
    st.subheader("Monetary bail amount set by each magistrate")
    image = Image.open('figures/magistrate_amount_summary.png')
    st.image(image)

    ### Comparison controling for offense types 
    st.header("Analysis while controling for offense types")

    # !!!!! TODO !!!!!
    # Explain the matched analysis. How many cases are sampled for the analysis
    # Explain the selection of 5 magistrates (those who handled more than 1000 cases)
    # Write interpretations
    
    # bail type
    st.subheader("Percentage of bail type for each magistrate")
    image = Image.open('figures/magistrate_matched_type.png')
    st.image(image, use_column_width=True)
    # bail amount
    st.subheader("Monetary bail amount set by each magistrate")
    image = Image.open('figures/magistrate_matched_amount.png')
    st.image(image)