import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from year_summary import plot_year_summary

@st.cache()
def load_data():
    df = pd.read_csv('data/cleaned/app_bail_type.csv')
    return df

def app():

    # ----------------------------------
    #  Year-end summary (included on every page)
    # ----------------------------------
    fig = plot_year_summary()
    f_year = go.FigureWidget(fig)
    st.plotly_chart(f_year)

    st.title('Breakdown by Numbers')

    bail_types = ['Denied', 'Monetary', 'Unsecured', 'Nonmonetary', 'ROR']
    years = [2020, 2021]
    df_month = load_data()
    df_year = df_month.groupby(['bail_year', 'bail_type'])['count'].sum()
    yearly_sums = [df_year[x].sum() for x in years]
    arr_year_pct = np.array([100*df_year[val]/yearly_sums[i] for i, val in enumerate(years)])
    print(arr_year_pct)
    
    # ----------------------------------
    #  Interactive figure: Bail Type Percentages
    # ----------------------------------
    fig = go.Figure()
    
    for j, bailType in enumerate(bail_types):
        for i, year in enumerate(years):
            bailPct = arr_year_pct[i, j]
            fig.add_trace(go.Bar(
                x=[i],
                y=[bailPct],
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailPct}% of {year} total"]
            ))

    fig.update_layout(
        barmode='stack',
        legend={'traceorder': 'normal'},
        legend_title="Bail Types",
        title="Breakdown of Bail Types Set: Totals",
        xaxis_title="Year",
        yaxis_title="Number of People",
        xaxis_tickvals=[0, 1],
        xaxis_ticktext=["2020","2021 YTD"]
    )

    f_pct = go.FigureWidget(fig)
    st.plotly_chart(f_pct)    
    
    # ----------------------------------
    #  Interactive figure: Bail Type Totals
    # ----------------------------------     
    
    fig = go.Figure()
    
    for bailType in bail_types:
        for i, year in enumerate(years):
            bailCount = df_year[year][bailType]
            fig.add_trace(go.Bar(
                x=[i],
                y=[bailCount],
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType} bail in {year}: {bailCount} people"]
            ))

    fig.update_layout(
        barmode='stack',
        legend={'traceorder': 'normal'},
        legend_title="Bail Types",
        title="Breakdown of Bail Types Set: Totals",
        xaxis_title="Year",
        yaxis_title="Number of People",
        xaxis_tickvals=[0, 1],
        xaxis_ticktext=["2020","2021 YTD"]
    )

    f_total = go.FigureWidget(fig)
    st.plotly_chart(f_total)