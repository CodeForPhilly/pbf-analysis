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

    # ----------------------------------
    #  Description
    # ----------------------------------    
    st.title('Breakdown by Numbers')

    st.write("""During a defendant's arraignment (a hearing held shortly after they are arrested), one of several [types of bail](https://www.pacodeandbulletin.gov/Display/pacode?file=/secure/pacode/data/234/chapter5/s524.html) may be set:
- **monetary**, where a bail amount is set and the defendant is held in jail until a portion (typically 10%) is paid (\"posted\"),
- **ROR** (“released on own recognizance”), where a defendant must agree to show up to all future court proceedings,
- **unsecured**, where the defendant is liable for a set bail amount if they do not show up to future court proceedings,
- a **nonmonetary** bail condition, or
- the defendant may be **denied** bail.
The most frequently set bail type in 2020 was monetary bail.""")        
    
    # ----------------------------------
    #  Preprocessing
    # ----------------------------------
    bail_types = ['Denied', 'Monetary', 'Nonmonetary', 'ROR', 'Unsecured']
    years = [2020, 2021]
    df_month = load_data()
    df_year = df_month.groupby(['bail_year', 'bail_type'])['count'].sum()
    # TODO: update so that df is sorted according to bail_types, to match bail type colors/orders accross pages! Currently, bail_types must be set to match the groupby order by hand.

    arr_year_total = np.array([df_year[val] for val in years])
    yearly_sums = [df_year[x].sum() for x in years]
    arr_year_pct = np.array([100*df_year[val]/yearly_sums[i] for i, val in enumerate(years)])
    
    # ----------------------------------
    #  Interactive figure: Bail Type Percentages
    # ----------------------------------
    fig = go.Figure()
    
    for j, bailType in enumerate(bail_types):
        bail_pct = arr_year_pct[:, j]
        fig.add_trace(go.Bar(
                x=[0,1],
                y=bail_pct,
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailPct:.1f}% of {year} total"
                           for bailPct, year in zip(bail_pct, years)]
        ))

    fig.update_layout(
        barmode='stack',
        legend={'traceorder': 'normal'},
        legend_title="Bail Types",
        title="Breakdown of Bail Types Set: Percentages",
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

    for j, bailType in enumerate(bail_types):
        bail_total = arr_year_total[:,j]
        fig.add_trace(go.Bar(
                x=[0,1],
                y=bail_total,
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailCount:.1f}% of {year} total"
                           for bailCount, year in zip(bail_total, years)]
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
    
