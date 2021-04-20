import streamlit as st
from PIL import Image
import plotly.graph_objs as go
from year_summary import plot_year_summary

@st.cache()
def load_data():
    fname = 'data/cleaned/app_total_number.txt'
    with open(fname, 'r') as f:
        n_cases = int(f.readline())
    
    return n_cases

def app():
    st.image('figures/PBF_logo_edit.png', use_column_width = True)
    
    # year-end summary
    fig = plot_year_summary()
    f_year = go.FigureWidget(fig)
    st.plotly_chart(f_year)

    n_cases = load_data()

    # What is this app
    st.title('Bail in Philadelphia')
    st.write("""This dashboard provides a summary of the bail situation in Philadelphia from January 2020 through March 2021. Shown at the top of each page is a summary of how people in Philadelphia have been impacted by monetary bail. Use the navigation panel on the left to view a breakdown of bail in Philly
- by year: how has 2021 compared to 2020?
- by actor: how has bail depended on the magistrate or other person setting bail?
- by price: how much bail have Philadelphians paid? 
- by demographics: how has bail differed between races, genders, and age groups?""")    
    st.write(f"Information from the **{n_cases:,d} cases** used to create this dashboard was gathered from [Philadelphia Municipal Court docket sheets.](https://ujsportal.pacourts.us/DocketSheets/MC.aspx#)")

    # What is PBF 
    st.header('The Philadelphia Bail Fund')
    st.write("The Philadelphia Bail Fund is a revolving fund that posts bail for people who are indigent and cannot afford bail.\
        Our goal is to keep families and communities together and vigorously advocate for the end to cash bail in Philadelphia. ")

    st.subheader("Get involved")
    # learn more
    pbf_link = 'Learn more at [phillybailfund.org](http://phillybailfund.org)'
    st.markdown(pbf_link, unsafe_allow_html = True)

    # donate
    donation_link = 'Take action via [donation](https://www.phillybailfund.org/donate)'
    st.markdown(donation_link, unsafe_allow_html = True)

    # contact us
    st.markdown('Contact us at <a href="mailto:info@phillybailfund.org">info@phillybailfund.org</a>', unsafe_allow_html=True)
    
    # What is Code for Philly
    st.header('Code for Philly')
    st.write("This dashboard was created by [Code for Philly](https://codeforphilly.org/), a Code For America brigade, in collaboration with the Philadelphia Bail Fund.\
    We're part of a national alliance of community organizers, developers, and designers that are putting technology to work in service of our local communities.")