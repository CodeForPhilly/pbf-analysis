import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.graph_objs as go
#from preprocess import preprocess, preprocess_acs

INCOME = '''
https://data.census.gov/cedsci/table?g=8600000US19102,19103,19104,19106,19107,19109,19111,19112,19114,19115,19116,19118,19119,19120,19121,19122,19123,19124,19125,19126,19127,19128,19129,19130,19131,19132,19133,19134,19135,19136,19137,19138,19139,19140,19141,19142,19143,19144,19145,19146,19147,19148,19149,19150,19151,19152,19153,19154&tid=ACSST5Y2018.S1901&hidePreview=true
'''
POVERTY = '''
https://data.census.gov/cedsci/table?q=S1701&g=0400000US42_8600000US19102,19103,19104,19106,19107,19109,19111,19112,19113,19114,19115,19116,19118,19119,19120,19121,19122,19123,19124,19125,19126,19127,19128,19129,19130,19131,19132,19133,19134,19135,19136,19137,19138,19139,19140,19141,19142,19143,19144,19145,19146,19147,19148,19149,19150,19151,19152,19153,19154&tid=ACSST5Y2018.S1701&hidePreview=true
'''

UNEMPLOYMENT = '''
https://data.census.gov/cedsci/table?q=S2301&g=0400000US42_8600000US19102,19103,19104,19106,19107,19109,19111,19112,19113,19114,19115,19116,19118,19119,19120,19121,19122,19123,19124,19125,19126,19127,19128,19129,19130,19131,19132,19133,19134,19135,19136,19137,19138,19139,19140,19141,19142,19143,19144,19145,19146,19147,19148,19149,19150,19151,19152,19153,19154&tid=ACSST5Y2018.S2301&hidePreview=true
'''
@st.cache()
def load_data():
    df = pd.read_csv('data.csv')
    df["bail_date"] = pd.to_datetime(df["bail_date"])
    return df

@st.cache()
def preprocess_acs():
    income_df = pd.read_csv('../data/income/cleaned_income.csv')
    income_df = income_df[['zipcode', 'households_median_income']]
    
    poverty_df = pd.read_csv('../data/poverty/cleaned_poverty.csv')
    poverty_df = poverty_df[['zipcode', 'percent_below_poverty']]

    unemployment_df = pd.read_csv('../data/unemployment/cleaned_unemployment.csv')
    unemployment_df = unemployment_df[['zipcode', 'unemployment_rate']]    
    
    acs_df = income_df.merge(poverty_df, on='zipcode', how='outer')
    acs_df = acs_df.replace('-', np.nan)
    acs_df = acs_df.set_index('zipcode')
    acs_df = acs_df.apply(pd.to_numeric).reset_index()
    
    acs_df = acs_df.merge(unemployment_df, on='zipcode', how='outer')
    acs_df = acs_df.replace('-', np.nan)
    acs_df = acs_df.set_index('zipcode')
    acs_df = acs_df.apply(pd.to_numeric).reset_index()    
    
    return acs_df

def app():
    st.title('Breakdown by Neighborhood')
    st.write('This section provides an interactive breakdown of case counts and amounts of bail set and paid by Philadelphia zip code, in tandem with income, poverty, and unemployment data from the American Community Survey (ACS), collected by the U.S. Census Bureau.')
    st.write('Use the dropdown menus to select a given bail and census metric associated with each map.')
    st.write('Zip codes with the highest case loads and total bail amounts set and paid tend to have lower median incomes and higher poverty and unemployment rates.')
    st.markdown(f"""
    Source Data: [Median Income]({INCOME}), [Poverty Level]({POVERTY}), [Unemployment Rate]({UNEMPLOYMENT})
        """)
    
    col1, col2 = st.beta_columns(2)
    
    # Get bail data
    #df = preprocess()
    df = load_data()

    # Create data assoc. w/ each metric (over all bail types) and put in dict
    case_counts = pd.DataFrame(df['zipcode_clean'].value_counts().reset_index().rename(columns={'index': 'zip', 'zipcode_clean': 'count'}))
    bail_amounts = df.groupby('zipcode_clean').sum()[['bail_amount']].reset_index()
    bail_paid = df.groupby('zipcode_clean').sum()[['bail_paid']].reset_index()
    bail_paid_pct = df[df['bail_paid'] > 0].groupby('zipcode_clean').size().div(df['zipcode_clean'].value_counts()).mul(100).round(1).reset_index().rename(columns={'index':'zip', 0:'pct'})
    cases_dfs = {'Case Count': case_counts, 'Total Bail Set': bail_amounts, 'Total Bail Posted': bail_paid, 'Percent of Cases where Bail Paid': bail_paid_pct}
    
    # Geo data
    # Approximate Philly lat/long
    philly = (40.0, -75.13)

    # Open geojson of philly zip code borders
    zips_geo = '../Zipcodes_Poly.geojson'
    with open(zips_geo) as f:
        zips_data = json.load(f)
    
    # Interactive map for bail metrics
    # Make dropdown for bail metric
    metric = col1.selectbox('Bail Metric', ('Case Count', 'Total Bail Set', 'Total Bail Posted', 'Percent of Cases where Bail Paid'))
    
    # Get data for the selected metric
    data = cases_dfs[metric]
    z = data[data.columns[1]]
    locations = data[data.columns[0]]

    # Set up figure object (choropleth map) with our geo data
    map_fig = go.FigureWidget(go.Choroplethmapbox(geojson=zips_data, # geojson data
                                          z=z, # what colors will rep. in map from our data
                                          locations=locations, # zip codes in our data
                                          featureidkey="properties.CODE", # key index in geojson for zip
                                          colorscale='YlOrRd'
                                         ))
    map_fig.update_layout(mapbox_style="carto-positron",
                   mapbox_zoom=8.8, mapbox_center = {"lat": philly[0], "lon": philly[1]})
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=450, width=350)
    
    col1.plotly_chart(map_fig)
    
    # Interactive map for ACS metrics
    # Get ACS data
    acs_df = preprocess_acs()
    
    # Dropdown for ACS metrics
    acs_metric = col2.selectbox('Census Metric', ('Households Median Income', 'Percent Below Poverty', 'Unemployment Rate'))
    
    # Set up figure object (choropleth map) with geo data, make sure z gets the selected metric
    acs_map_fig = go.FigureWidget(go.Choroplethmapbox(geojson=zips_data, # geojson data
                                          z=acs_df['_'.join([w.lower() for w in acs_metric.split(' ')])], # what colors will rep. in map from our data
                                          locations=acs_df['zipcode'], # zip codes in our data
                                          featureidkey="properties.CODE", # key index in geojson for zip
                                          colorscale='YlOrRd'
                                         ))
    acs_map_fig.update_layout(mapbox_style="carto-positron",
                   mapbox_zoom=8.8, mapbox_center = {"lat": philly[0], "lon": philly[1]})
    acs_map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=450, width=350)
    
    col2.plotly_chart(acs_map_fig)
    