import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from year_summary import plot_year_summary

@st.cache()
def load_data():
    df_bail_type = pd.read_csv('data/cleaned/app_bail_type.csv')
    df_by_numbers = pd.read_csv('data/cleaned/app_by_numbers.csv')
    
    df_by_numbers['Percentage of Cases'] = df_by_numbers['Percentage of Cases'].map('{:.1f}%'.format)
    df_by_numbers['People Impacted'] = df_by_numbers['People Impacted'].map('{:,.0f}'.format)
    df_by_numbers['Total Bail Set'] = df_by_numbers['Total Bail Set'].map('${:,.0f}'.format)
    df_by_numbers['Median Bail Set'] = df_by_numbers['Median Bail Set'].map('${:,.0f}'.format)
    df_by_numbers['Median Bail Paid (all cases)'] = df_by_numbers['Median Bail Paid (all cases)'].map('${:,.0f}'.format)
    df_by_numbers['Median Bail Paid (when more than $0 was paid)'] = df_by_numbers['Median Bail Paid (when more than $0 was paid)'].map('${:,.0f}'.format)
    df_by_numbers.set_index('Year', inplace=True)
    
    return df_bail_type, df_by_numbers

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
    st.title('Breakdown by Year')

    st.subheader("Bail Types")
    
    st.write("""During a defendant's arraignment (a hearing held shortly after they are arrested), one of several [types of bail](https://www.pacodeandbulletin.gov/Display/pacode?file=/secure/pacode/data/234/chapter5/s524.html) may be set:
- **monetary**, where a bail amount is set and the defendant is held in jail until a portion (typically 10%) is paid (\"posted\"),
- **ROR** (“released on own recognizance”), where a defendant must agree to show up to all future court proceedings,
- **unsecured**, where the defendant is liable for a set bail amount if they do not show up to future court proceedings,
- a **nonmonetary** bail condition, or
- the defendant may be **denied** bail.""")    
    
    st.write("Monetary bail is the most frequently set bail type.")  
    
    # ----------------------------------
    #  Preprocessing
    # ----------------------------------
    bail_types = ['Denied', 'Monetary', 'Nonmonetary', 'ROR', 'Unsecured']
    years = [2020, 2021]
    df_month, df_by_numbers = load_data()
    df_year = df_month.groupby(['bail_year', 'bail_type'])['count'].sum()
    df_monetary = df_month[df_month['bail_type'] == 'Monetary']
    
    # TODO: update so that df is sorted according to bail_types, to match bail type colors/orders accross pages! Currently, bail_types must be set to match the groupby order by hand.

    arr_year_total = np.array([df_year[val] for val in years])
    yearly_sums = [df_year[x].sum() for x in years]
    arr_year_pct = np.array([100*df_year[val]/yearly_sums[i] for i, val in enumerate(years)])
    gb_month = df_month.groupby(['bail_year', 'bail_month'])['count'].sum()
    df_monetary['pct'] = df_monetary.apply(lambda row:
                                           100*row['count']/gb_month[row['bail_year']][row['bail_month']],
                                           axis=1)
    
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
                           for bailPct, year in zip(bail_pct, years)],
                visible=True
        ))

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
                hovertext=[f"{bailType}: {bailCount:,d} people in {year}"
                           for bailCount, year in zip(bail_total, years)],
                visible=False
        ))             

    fig.update_layout(
        barmode='stack',
        legend={'traceorder': 'normal'},
        legend_title="Bail Types",
        title="Breakdown of bail types set",
        yaxis_title="Percentage of cases",
        xaxis_title="Year",
        xaxis_tickvals=[0, 1],
        xaxis_ticktext=["2020, total","2021, YTD"]
    )        
        
    fig.update_layout(
        updatemenus=[dict(
            active=0,
            x=-0.5,
            y=1,
            xanchor='left',
            yanchor='top',
            buttons=list([
                dict(label="Percentage of cases",
                     method="update",
                     args=[{"visible": [True, True, True, True, True,
                                        False, False, False, False, False]},
                           {'yaxis': {'title': 'Percentage of cases'}}
                          ]
                    ),
                dict(label="Number of people",
                     method="update",
                     args=[{"visible": [False, False, False, False, False,
                                        True, True, True, True, True]},
                           {'yaxis': {'title': 'Number of people'}}
                          ]
                    )                        
                ]),
            )]
        )        
        

    
    f_pct = go.FigureWidget(fig)
    st.plotly_chart(f_pct)    
    
  
    '''
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
                hovertext=[f"{bailType}: {bailCount:,d} people in {year}"
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
    '''

    # ----------------------------------
    #  Interactive figure: monetary bail totals
    # ----------------------------------     

    st.subheader("Monetary Bail")
    
    st.write("""So far in 2021, the percentage of cases each month for which monetary bail is set is slightly higher than for the same month in 2020.""")

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig = go.Figure()

    # As percentage of total cases
    for i, year in enumerate(years):
        month_data = df_monetary[df_monetary['bail_year'] == year]['pct']
        fig.add_trace(go.Bar(
            y=month_data,
            name=year,
            hoverinfo="text",
            hovertext=[f"{m} {year}: {bailPct:.1f}% of cases"
                       for m, bailPct in zip(months, month_data)],
            visible=True
            ))         
    
    # As total counts
    for i, year in enumerate(years):
        month_data = df_monetary[df_monetary['bail_year'] == year]['count']
        fig.add_trace(go.Bar(
            y=month_data,
            name=year,
            hoverinfo="text",
            hovertext=[f"{m} {year}: {bailCount:,d} people"
                       for m, bailCount in zip(months, month_data)],
            visible=False
            ))   
    
    # Layout
    fig.update_layout(
        title="Monetary bail cases per month",
        legend_title="Year",
        xaxis_title="Month",
        xaxis_tickvals=list(range(12)),
        xaxis_ticktext=months
    )
    
    fig.update_layout(
        annotations=[
            dict(text="Select data to view:",
                 x=-0.5,
                 y=1.08,
                 xref="paper",
                 yref="paper",
                 align="left",
                 showarrow=False
                )
        ]
    )
    
    fig.update_layout(
        updatemenus=[dict(
            active=0,
            x=-0.5,
            y=1,
            xanchor='left',
            yanchor='top',
            buttons=list([
                dict(label="Percentage of cases",
                     method="update",
                     args=[{"visible": [True, True, False, False]},
                           {'yaxis': {'title': 'Percentage of cases'}}
                          ]
                    ),
                dict(label="Number of people",
                     method="update",
                     args=[{"visible": [False, False, True, True]},
                           {'yaxis': {'title': 'Number of people'}}
                          ]
                    )                        
                ]),
            )]
        )
    
    f_total = go.FigureWidget(fig)
    st.plotly_chart(f_total)    
    
    # ----------------------------------
    #  Summary table
    # ----------------------------------  

    st.write("""In 2020 and 2021, the median payment of $0 means that over half of people did not post bail: **a majority of people have not been able to pay the amount required to be released from jail**.""") #bail was posted in only 44% of monetary bail cases
    
    st.table(df_by_numbers)
    
    