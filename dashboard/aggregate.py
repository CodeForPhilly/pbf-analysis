import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from PIL import Image
from preprocess import preprocess


# st.set_page_config(layout="wide")
def app():
    st.title('Year-end Summary')
    st.write('This section provides a general year-end summary of bail in Philadelphia in 2020, including trends and aggregate-level information for case counts, bail types, and monetary bail set and posted.')
    
    # Get bail data
    df = preprocess()
    
    # ----------------------------------------------------
    # Summary numbers 
    # ----------------------------------------------------
    #st.header('Year-end Summary')
    
    # Get range of dates and create slider to select date range (workaround since Streamlit doesn't have a date range slider)
    df['bail_date'] = df['bail_date'].map(datetime.datetime.date)
    all_dates = sorted(df['bail_date'].unique())
    start_date = df['bail_date'].min()
    end_date = df['bail_date'].max()
    # Slider
    date_range = st.slider('Date Range', 1, (end_date-start_date).days + 1, (1,(end_date-start_date).days + 1),  1)
    st.write(all_dates[date_range[0]-1].strftime('%b %d, %Y'), '-', all_dates[date_range[1]-1].strftime('%b %d, %Y'))  
    
    # Get data based on selected date range
    df = df[(df['bail_date'] >= all_dates[date_range[0]-1])&(df['bail_date'] <= all_dates[date_range[1]-1])]
    df_bail = df['bail_type'].value_counts()
    df_monetary = df[df['bail_type'] == "Monetary"]
    series_monetary = df_monetary['bail_set_bin'].value_counts()
    df_defender = df['attorney_type'].value_counts()
    
    # Card for Case Count
    cases = go.Indicator(
        mode = 'number',
        value = len(df),
        domain = {'row': 0, 'column': 0 }, 
        title = {'text': 'Total Cases'})

    # Card for Monetary Bail Frequency
    frequency = go.Indicator(
        mode = 'number',
        value = len(df[df['bail_type'] == 'Monetary']) / len(df[df['bail_type'].notnull()]) * 100.,
        number = {'suffix': '%'},
        domain = {'row': 0, 'column': 1 }, 
        title = {'text': 'Monetary Bail Frequency'})

    # Card for Total Bail Amt
    amount = go.Indicator(
        mode = 'number',
        value = df[df['bail_type'] == 'Monetary']['bail_amount'].sum(),
        number = {'prefix': '$'},
        domain = {'row': 1, 'column': 0 }, 
        title = {'text': 'Total Bail Set'})

    # Card for Total Bail Paid
    paid = go.Indicator(
        mode = 'number',
        value = df[df['bail_type'] == 'Monetary']['bail_paid'].sum(),
        number = {'prefix': '$'},
        domain = {'row': 1, 'column': 1 }, 
        title = {'text': 'Total Bail Paid'})

    # Set up figure as 2x2 grid of the cards in the order specified
    card_fig = go.FigureWidget()
    card_fig.add_trace(cases)
    card_fig.add_trace(frequency)
    card_fig.add_trace(amount)
    card_fig.add_trace(paid)
    card_fig.update_layout(
        grid = {'rows': 2, 'columns': 2, 'pattern': "independent"})
    
    st.plotly_chart(card_fig)
    
    # ----------------------------------------------------
    # Summary charts 
    # ----------------------------------------------------
    #st.header('Bail type and monetary bail summary')

    st.subheader('Bail type')
    st.write("""During a defendant's arraignment (a hearing held shortly after they are arrested), one of several [types of bail](https://www.pacodeandbulletin.gov/Display/pacode?file=/secure/pacode/data/234/chapter5/s524.html) may be set:
- **monetary**, where a bail amount is set and the defendant is held in jail until a portion (typically 10%) is paid (\"posted\"),
- **unsecured**, where the defendant is liable for a set bail amount if they do not show up to future court proceedings,
- **ROR** (“released on own recognizance”), where a defendant must agree to show up to all future court proceedings,
- other **nonmonetary** or **nominal** bail conditions, or
- the defendant may be **denied** bail.""")
    
    # By Bail Type
    pie1_fig = go.FigureWidget()
    pie1_fig.add_trace(go.Pie(labels=df_bail.index.tolist(), values=df_bail.values.tolist()))
    pie1_fig.update_traces(hole=.4, hoverinfo="label+percent+value")
    pie1_fig.update_layout(showlegend=True, title_text='Bail Type', title_x=0.45)
    pie1_fig.update_layout(margin={"r":0,"t":100,"l":0,"b":0}, height=400, width=400)
    st.plotly_chart(pie1_fig)    
    #st.image(Image.open('figures/aggregate_bailType.png'), width=400)
    
    st.write("The most frequently set bail type in 2020 was monetary bail. Together, nominal or nonmonetary bail were set in under 1% of cases.")
    
    st.subheader('Monetary bail set')
    st.write("For cases where monetary bail was set, the median bail set was $30,000, and the most frequently set bail amount was $25,000. However, a bail amount of at least $100,000 was set in more than 25% of cases.") 
    st.image(Image.open('figures/aggregate_bailSet.png'), width=400)      
    #st.write("Note that the bail amount bins in this chart are increasing roughly by order-of-magnitude, rather than evenly divided.")
    
    st.subheader('Monetary bail posted')
    st.write("In nearly half (49%) of cases where monetary bail was set, bail was not posted, meaning that the defendant was not released from jail. When bail was posted, the median and most frequently paid amount was $2,500 (corresponding to 10% of bail set at $25,000). Out of the cases where bail was at least $100,000, less than a quarter of defendants posted bail. Though infrequently set, bail amounts below $1000 were also infrequently posted.")
    st.image(Image.open('figures/aggregate_bailPosted.png'), width=400)          

    """
    # By Bail Set
    pie2_fig = go.FigureWidget()
    pie2_fig.add_trace(go.Pie(labels=series_monetary.index.tolist(), values=series_monetary.values.tolist()))
    pie2_fig.update_traces(hole=.4, hoverinfo="label+percent+value")
    pie2_fig.update_layout(showlegend=True, title_text='Bail Set', title_x=0.45)
    pie2_fig.update_layout(margin={"r":0,"t":100,"l":0,"b":0}, height=400, width=40)
    st.plotly_chart(pie2_fig)
    """

    st.subheader('Attorney types')
    # By Atty Type
    st.write("Public defendants were assigned in more than two thirds of cases.")    
    pie3_fig = go.FigureWidget()
    pie3_fig.add_trace(go.Pie(labels=df_defender.index.tolist(), values=df_defender.values.tolist()))
    pie3_fig.update_traces(hole=.4, hoverinfo="label+percent+value")
    pie3_fig.update_layout(showlegend=True, title_text='Attorney Type', title_x=0.45)
    pie3_fig.update_layout(margin={"r":0,"t":100,"l":0,"b":0}, height=400, width=400)
    st.plotly_chart(pie3_fig)

    # TODO: fix these figures such that the same colors/order are used for each bail type
    st.subheader('Charged offenses and bail type') 
    st.write("The frequency of bail types set was dependent on the types of charges associated with each case.\
    For cases involving a charge of assault, monetary bail was most frequently set.\
    For cases involving a drug-related charge, monetary bail and ROR were set at similar rates.\
    For cases involving a charge of DUI, ROR bail was most frequently set.")
    st.image(Image.open('figures/aggregate_bailType_byOffense.png'), use_column_width=True)    
    
    # ----------------------------------------------------
    # Moving average plots 
    # ----------------------------------------------------
    st.subheader('Bail trends over the year')
    st.write("Use the dropdown menu to view trends in the average bail amount set, number of monetary bail cases, and frequency of monetary bail set. Use the slider to change the number of days over which the moving average is calculated.")    
    # Make data for each metric + data to initialize the chart
    ma_dfs = {'Bail Amount': df.groupby('bail_date').mean()['bail_amount'], 
              'Monetary Bail Cases': df_monetary.groupby('bail_date').size(),
              'Monetary Bail Frequency': df[df['bail_type'].notnull()].groupby('bail_date').size()
              }
    
    # Dropdown for metric
    metric = st.selectbox('Metric', ('Bail Amount', 'Monetary Bail Cases', 'Monetary Bail Frequency'))
    
    # Slider for window size
    window = st.slider('Window Size (days)', 1, 60, 5, 1)
    
    # Initialize figure
    ma_fig = go.FigureWidget()
    ma_fig.layout.title.text = 'Mean '+ metric + ' ' + str(window) + '-Day Moving Average'
    ma_fig.layout.title.x = 0.5
    ma_fig.layout.xaxis.title = 'Date'
    ma_fig.layout.yaxis.title = metric
    
    # Add traces and finalize figure, make sure to get data from selected metric and window size
    if metric != 'Monetary Bail Frequency':
        tmp = ma_dfs[metric].rolling(window=window, min_periods=1).mean()
    else:
        tmp_denom = ma_dfs[metric].rolling(window=window, min_periods=1).sum()
        tmp_num = ma_dfs['Monetary Bail Cases'].rolling(window=window, min_periods=1).sum()
        tmp = tmp_num.div(tmp_denom)
    ma_fig.add_trace(go.Scatter(x=tmp.index,
                                y=tmp.values,
                        mode='lines+markers',
                        name='lines+markers'))
    st.plotly_chart(ma_fig)
