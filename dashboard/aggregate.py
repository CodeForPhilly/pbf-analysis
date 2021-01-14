import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from preprocess import preprocess


# st.set_page_config(layout="wide")
def app():
    st.title('Aggregate Information')
    st.write('This section provides a general year-end summary of bail in Philadelphia in 2020, including trends and aggregate-level information for cases and bail amounts and types.')
    
    # Get bail data
    df = preprocess()
    
    # Aggregate Summary
    st.header('1. Year-end Aggregate Summary')
    
    # Get range of dates and create slider to select date range (workaround since Streamlit doesn't have a date range slider)
    df['bail_date'] = df['bail_date'].map(datetime.datetime.date)
    all_dates = sorted(df['bail_date'].unique())
    start_date = df['bail_date'].min()
    end_date = df['bail_date'].max()
    date_range = st.slider('Dates', 1, (end_date-start_date).days + 1, (1,(end_date-start_date).days + 1),  1)
    st.write(all_dates[date_range[0]-1].strftime('%b %d %Y'), '-', all_dates[date_range[1]-1].strftime('%b %d %Y'))
    
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
    
    # Pie charts for Breakdown by Bail Type/Set/By Atty Type
    st.header('2. Summary of Cases by Bail Type, Bail Set, and Attorney Type')
    # Create subplots: use 'domain' type for Pie subplot
    col1, col2, col3 = st.beta_columns([2,2,2])
    
    # By Bail Type
    pie1_fig = go.FigureWidget()
    pie1_fig.add_trace(go.Pie(labels=df_bail.index.tolist(), values=df_bail.values.tolist()))
    pie1_fig.update_traces(hole=.4, hoverinfo="label+percent+value")
    pie1_fig.update_layout(showlegend=False, title_text='Bail Type', title_x=0.45)
    pie1_fig.update_layout(margin={"r":0,"t":100,"l":0,"b":0}, height=250, width=250)
    col1.plotly_chart(pie1_fig)
    
    # By Bail Set
    pie2_fig = go.FigureWidget()
    pie2_fig.add_trace(go.Pie(labels=series_monetary.index.tolist(), values=series_monetary.values.tolist()))
    pie2_fig.update_traces(hole=.4, hoverinfo="label+percent+value")
    pie2_fig.update_layout(showlegend=False, title_text='Bail Set', title_x=0.45)
    pie2_fig.update_layout(margin={"r":0,"t":100,"l":0,"b":0}, height=250, width=250)
    col2.plotly_chart(pie2_fig)
    
    # By Atty Type
    pie3_fig = go.FigureWidget()
    pie3_fig.add_trace(go.Pie(labels=df_defender.index.tolist(), values=df_defender.values.tolist()))
    pie3_fig.update_traces(hole=.4, hoverinfo="label+percent+value")
    pie3_fig.update_layout(showlegend=False, title_text='Attorney Type', title_x=0.45)
    pie3_fig.update_layout(margin={"r":0,"t":100,"l":0,"b":0}, height=250, width=250)
    col3.plotly_chart(pie3_fig)
    
    st.write("The median bail set was $30,000, and the most frequently set bail amount was $25,000.")
    st.write("In 48.8% of cases with monetary bail, bail has not been posted. Including these cases, the median amount of bail paid was $250. ")    
    
    
    
    # Moving average plot
    st.header('3. Philadelphia Bail Trends over 2020')
    # Make data for each metric + data to initialize the chart
    ma_dfs = {'Bail Amount': df.groupby('bail_date').mean()['bail_amount'], 
              'Monetary Bail Cases': df_monetary.groupby('bail_date').size(),
             'Monetary Bail Frequency': df[df['bail_type'].notnull()].groupby('bail_date').size()
             }
    
    # Dropdown for metric
    metric = st.selectbox('Metric', ('Bail Amount', 'Monetary Bail Cases', 'Monetary Bail Frequency'))
    
    # Slider for window size
    window = st.slider('Window Size', 1, 60, 5, 1)
    
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
