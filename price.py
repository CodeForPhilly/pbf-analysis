import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from year_summary import plot_year_summary

@st.cache()
def load_data():
    df_month = pd.read_csv('data/cleaned/app_bail_paid.csv')
    return df_month

def app():
    # year-end summary
    fig = plot_year_summary()
    f_year = go.FigureWidget(fig)
    st.plotly_chart(f_year)

    st.title('Breakdown by Price')
    st.write("In progress")

    # prepare data
    df_month = load_data()
    month_data = df_month['bail_paid']

    df_year = df_month.groupby(['bail_year'])['bail_paid'].sum()
    bail_paid_2020 = df_year[2020]
    bail_paid_2021 = df_year[2021]

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # plot figure
    fig = go.Figure()

    ### Add traces for yearly summary
    # 2020
    fig.add_trace(go.Bar(
    x = [0],
    y = [bail_paid_2020],
    orientation = "v",
    text = ["$"+f'{bail_paid_2020:,.0f}'],
    textposition = "inside",
    hoverinfo = "text",
    hovertext = ["2020 <br>$"+f'{bail_paid_2020:,.0f}'],
    showlegend = False
    ))

    # 2021
    fig.add_trace(go.Bar(
        x = [1],
        y = [bail_paid_2021],
        orientation = "v",
        text = ["$"+f'{bail_paid_2021:,.0f}'],
        textposition = "inside",
        hoverinfo = "text",
        hovertext = ["2021 <br>$"+f'{bail_paid_2021:,.0f}'],
        showlegend = False

        ))

    ### add traces for monthly summary
    # 2020 data
    hovertext_2020 = [m + " 2020 <br>" + "$"+f'{v:,.0f}'  
                    for (m,v) in zip(months, month_data[:12])]
    fig.add_trace(go.Bar(
        y = month_data[:12],
        name = "2020",
        hoverinfo = "text",
        hovertext = hovertext_2020,
        visible = False
        ))

    # 2021 data
    hovertext_2021 = [m + " 2021 <br>" + "$"+f'{v:,.0f}'
                    for (m,v) in zip(months,month_data[12:])]
    fig.add_trace(go.Bar(
        y = month_data[12:],
        name = "2021",
        hoverinfo = "text",
        hovertext = hovertext_2021,
        visible = False   
        ))


    fig.update_layout(
        title="Bail paid by year",
        xaxis_title="year",
        yaxis_title="bail amount paid ($)",
        xaxis_tickvals = [0, 1],
        xaxis_ticktext = ["2020","2021 YTD"]
    )

    # update
    fig.update_layout(
        annotations=[
            dict(text="Summary", x=-0.28, xref="paper", y=1.1, yref="paper",
                                align="left", showarrow=False)
        ])

    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                x = -0.3,
                xanchor = 'left',
                y = 1,
                yanchor = 'top',
                buttons=list([
                    dict(label="by year",
                        method="update",
                        args=[{"visible": [True, True, False, False]},
                            {"title": "Bail paid by year",
                            'xaxis': {'title': 'year',
                                        'tickvals' : [0,1],
                                        'ticktext' : ["2020", "2021 YTD"]
                            }}]),
                    dict(label="by month",
                        method="update",
                        args=[{"visible": [False, False, True, True]},
                            {"title": "Bail paid by month",
                            'xaxis': {'title': 'month',
                                        'tickvals' : list(range(12)),
                                        'ticktext' : months
                                        }}
                            ])
                        
                ]),
            )
            
        ])

    f2 = go.FigureWidget(fig)
    st.plotly_chart(f2)