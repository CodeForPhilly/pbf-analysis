import streamlit as st
from PIL import Image

def app():
    st.title('Breakdown by Magistrate')
    st.write('In progress')

    ### Summary plots
    # number of cases

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

    ### Plots for matched sample 

    # number of cases
    # bail type
    # bail amount