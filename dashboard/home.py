import streamlit as st
from PIL import Image

def app():
    st.image('figures/PBF_logo_edit.png', use_column_width = True)

    # What is this app
    st.header('Bail in Philadelphia, 2020')
    st.write("This dashboard provides a summary of the bail situation in Philadelphia in 2020. \
        We provide a general year-end summary, along with breakdown by neighborhood, magistrate, and defendant demographics.\
        Please use the navigation panel on the left to select a page.")    
    st.write("Information from the **24,221 cases** used to create this dashboard was gathered from [Philadelphia Municipal Court docket sheets.](https://ujsportal.pacourts.us/DocketSheets/MC.aspx#)")

    # What is PBF 
    st.header('The Philadelphia Bail Fund')
    st.write("The Philadelphia Bail Fund is a revolving fund that posts bail for people who are indigent and cannot afford bail.\
        Our goal is to keep families and communities together and vigorously advocate for the end to cash bail in Philadelphia. ")

    st.header("Get involved")
    # learn more
    pbf_link = 'Learn more at [phillybailfund.org](http://phillybailfund.org)'
    st.markdown(pbf_link, unsafe_allow_html = True)

    # donate
    donation_link = 'Take action via [donation](https://www.phillybailfund.org/donate)'
    st.markdown(donation_link, unsafe_allow_html = True)

    # contact us
    st.markdown('Contact us at <a href="mailto:info@phillybailfund.org">info@phillybailfund.org</a>', unsafe_allow_html=True)