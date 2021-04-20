import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.graph_objs as go
from year_summary import plot_year_summary

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
    df = pd.read_csv('data/cleaned/app_data.csv')
    df["bail_date"] = pd.to_datetime(df["bail_date"])
    return df

@st.cache()
def preprocess_acs():
    income_df = pd.read_csv('data/external/income/cleaned_income.csv')
    income_df = income_df[['zipcode', 'households_median_income']]
    
    poverty_df = pd.read_csv('data/external/poverty/cleaned_poverty.csv')
    poverty_df = poverty_df[['zipcode', 'percent_below_poverty']]

    unemployment_df = pd.read_csv('data/external/unemployment/cleaned_unemployment.csv')
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
    # year-end summary
    fig = plot_year_summary()
    f_year = go.FigureWidget(fig)
    st.plotly_chart(f_year)

    minCount = 10 #100
    
    st.title('Breakdown by Neighborhood')
    st.write('This section provides an interactive breakdown of case counts, total amounts of bail set and paid, and bail payment rate by Philadelphia zip code, in tandem with income, poverty, and unemployment data from the American Community Survey (ACS) collected by the U.S. Census Bureau.')
    st.markdown(f"""
    Source Data: [Median Income]({INCOME}), [Poverty Level]({POVERTY}), [Unemployment Rate]({UNEMPLOYMENT})
        """)
    
    st.header('Interactive Maps')
    st.write(f'Use the dropdown menus to select a given bail and census metric associated with each map.\
    Hover over an area to view the corresponding metric value and zip code number.\
    For bail metrics other than case counts, only zip codes with at least {minCount} cases are shown.')
    st.write('Zip codes with the highest case counts, highest total bail amounts set and posted, and lowest bail posting rates tend to have lower median incomes and higher poverty and unemployment rates.')
    
    col1, col2 = st.beta_columns(2)
    
    # ------------------------------------
    # Process bail data
    # ------------------------------------
    #df = preprocess()
    df = load_data()

    # Create data assoc. w/ each metric (over all bail types) and put in dict
    case_counts = pd.DataFrame(df['zip'].value_counts()
                               .reset_index().rename(columns={'index': 'zip', 'zip': 'count'}))
    bail_amounts = df.groupby('zip').sum()[['bail_amount']].reset_index()
    bail_paid = df.groupby('zip').sum()[['bail_paid']].reset_index()
    df_monetary = df[df['bail_type'] == 'Monetary'][['zip', 'bail_paid']] 
    bail_paid_pct = (df_monetary[df_monetary['bail_paid'] > 0]['zip'].value_counts()
                     .divide(df_monetary['zip'].value_counts())
                     .mul(100).round(1)
                     .reset_index().rename(columns={'index': 'zip', 'zip': 'pct'}))
    #public_defender = (df[df['attorney_type'] == 'Public']['zipcode_clean'].value_counts()
    #                 .divide(df['zipcode_clean'].value_counts())
    #                 .mul(100).round(1)
    #                 .reset_index().rename(columns={'index': 'zipcode', 'zip': 'pct'}))
        
    # Select only zip codes with at least minCount cases to show in bail metrics map
    minZips = case_counts[case_counts['count'] >= minCount]['zip'].to_list()
    #case_counts = case_counts[case_counts['zip'].isin(minZips)]
    bail_amounts = bail_amounts[bail_amounts['zip'].isin(minZips)]
    bail_paid = bail_paid[bail_paid['zip'].isin(minZips)]
    bail_paid_pct = bail_paid_pct[bail_paid_pct['zip'].isin(minZips)]
    #public_defender = public_defender[public_defender['zip'].isin(minZips)]
    
    cases_dfs = {'Case Count': case_counts,
                 'Total Bail Set ($)': bail_amounts,
                 'Total Bail Posted ($)': bail_paid,
                 'Bail Posting Rate': bail_paid_pct}
    
    # Geo data
    # Approximate Philly lat/long
    philly = (40.0, -75.13)

    # Open geojson of philly zip code borders
    zips_geo = 'data/external/zipcodes_poly.geojson'
    with open(zips_geo) as f:
        zips_data = json.load(f)
    
    # ------------------------------------
    # Interactive map for bail metrics
    # ------------------------------------
    # Make dropdown for bail metric
    metric = col1.selectbox('Bail Metric', (tuple(cases_dfs.keys())))
    
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
    
    col11, col21 = st.beta_columns(2)
    
    zip_input = col11.text_input('Enter your zip code:')
    
    if zip_input:
        try:
            st.header('Bail Summary for ' + zip_input)
            temp_df = pd.DataFrame(
                {'Metric': ['<b>Case Count</b>', '<b>Total Bail Set</b>', '<b>Total Bail Posted</b>', '<b>Bail Posting Rate</b>'],
                 'Value': [case_counts[case_counts['zip']==int(zip_input)]['count'].values[0],
                        f"${bail_amounts[bail_amounts['zip']==int(zip_input)]['bail_amount'].values[0]:,.0f}",
                        f"${bail_paid[bail_paid['zip']==int(zip_input)]['bail_paid'].values[0]:,.0f}",
                        f"{bail_paid_pct[bail_paid_pct['zip']==int(zip_input)]['pct'].values[0]:.0f}%"]
                }
            )
            tbl_fig = go.Figure(data=[go.Table(
                columnwidth = [400,200],
                header=dict(values=['',''],
                    fill_color='white',
                    align='left'),
                cells=dict(values=[temp_df['Metric'], temp_df['Value']],
                   fill_color='lavender',
                   font = dict(color='black', family='Arial', size=24),
                   align=['left', 'right']))
            ])
            tbl_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, width=600)
            st.plotly_chart(tbl_fig)
        except IndexError:
            st.write("No information available for this zip code")