import streamlit as st
from PIL import Image

def app():
    st.image('figures/PBF_logo_edit.png', use_column_width = True)
    st.write("*** THIS PAGE IS IN PROGRESS***")

    # What is this app
    st.header('Bail in Philadelphia 2020.')
    st.write("This dashboard provides a summary of the bail situation in Philadelphia in 2020")
    st.write("We provide a general year-end summary, along with breakdown by neighborhood, magistrate, and race and gender. ")
    st.write("Please use the navigation panel on the left to select a page.")

    # What is PBF 
    st.header('The Philadelphia Bail Fund')
    st.write("The Philadelphia Bail Fund is a revolving fund that posts bail for people who are indigent and cannot afford bail.\
        Our goal is to keep families and communities together and vigorously advocate for the end to cash bail in Philadelphia. ")

    st.header("Get involved")
    # learn more
    pbf_link = '[Learn more](http://phillybailfund.org)'
    st.markdown(pbf_link, unsafe_allow_html = True)

    # donate
    donation_link = '[Take action via donation](https://www.phillybailfund.org/donate)'
    st.markdown(donation_link, unsafe_allow_html = True)

    # contact us
    st.markdown("Contact us at info@phillybailfund.org")