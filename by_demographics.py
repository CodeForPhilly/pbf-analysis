import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from year_summary import plot_year_summary

@st.cache()
def load_race_data():
    df_race_bail_set = pd.read_csv('data/cleaned/app_race_bail_set.csv')
    df_race_bail_set = df_race_bail_set.groupby(['bail_year', 'race_group'])['bail_amount_sum'].sum().unstack(fill_value=0).stack()
    df_race_bail_type = pd.read_csv('data/cleaned/app_race_bail_type.csv')
    df_race_bail_type = df_race_bail_type.groupby(['bail_year', 'race_group', 'bail_type'])['bail_type_pct'].sum().unstack(fill_value=0).stack()
    return df_race_bail_set, df_race_bail_type

@st.cache()
def load_sex_data():
    df_bail_set = pd.read_csv('data/cleaned/app_sex_bail_set.csv')
    df_bail_set = df_bail_set.groupby(['bail_year', 'sex'])['bail_amount_sum'].sum().unstack(fill_value=0).stack()
    df_bail_type = pd.read_csv('data/cleaned/app_sex_bail_type.csv')
    df_bail_type = df_bail_type.groupby(['bail_year', 'sex', 'bail_type'])['bail_type_pct'].sum().unstack(fill_value=0).stack()
    return df_bail_set, df_bail_type

def load_age_data():
    df_bail_set = pd.read_csv('data/cleaned/app_age_bail_set.csv')
    df_bail_set = df_bail_set.groupby(['bail_year', 'age_group'])['bail_amount_sum'].sum().unstack(fill_value=0).stack()
    df_bail_type = pd.read_csv('data/cleaned/app_age_bail_type.csv')
    df_bail_type = df_bail_type.groupby(['bail_year', 'age_group', 'bail_type'])['bail_type_pct'].sum().unstack(fill_value=0).stack()
    return df_bail_set, df_bail_type

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
    st.title('Breakdown by Demographics')
    
    # ----------------------------------
    #  Preprocessing
    # ----------------------------------
    bail_types = ['Denied', 'Monetary', 'Nonmonetary', 'ROR', 'Unsecured']
    years = [2020, 2021]
    races = ['Black', 'White', 'Other']
    sexes = ['Male', 'Female']
    age_groups = ['minor', '18 to 25', '26 to 64', '65+']
                           
    df_race_bail_set, df_race_bail_type = load_race_data()
    df_sex_bail_set, df_sex_bail_type = load_sex_data()
    df_age_bail_set, df_age_bail_type = load_age_data()  
    print(df_age_bail_type)
    
    arr_race_pct_2020 = np.array([df_race_bail_type[2020][race] for race in races], dtype=object)
    arr_race_pct_2021 = np.array([df_race_bail_type[2021][race] for race in races], dtype=object)

    arr_sex_pct_2020 = np.array([df_sex_bail_type[2020][sex] for sex in sexes], dtype=object)
    arr_sex_pct_2021 = np.array([df_sex_bail_type[2021][sex] for sex in sexes], dtype=object)

    arr_age_pct_2020 = np.array([df_age_bail_type[2020][age] for age in age_groups], dtype=object)
    arr_age_pct_2021 = np.array([df_age_bail_type[2021][age] for age in age_groups], dtype=object)    
    
    # ----------------------------------
    #  Interactive figure: Bail Type Percentages by Race
    # ----------------------------------
    fig = go.Figure()
    
    for j, bailType in enumerate(bail_types):
        bail_pct = arr_race_pct_2020[:, j]#[row[row['bail_type'] == bailType] for row in arr_race_pct_2020]
        fig.add_trace(go.Bar(
                x=list(range(len(races))),
                y=bail_pct,
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailPct:.1f}% of 2020 total, {race}"
                           for bailPct, race in zip(bail_pct, races)]
        ))
    
    for j, bailType in enumerate(bail_types):
        bail_pct = arr_race_pct_2021[:, j]
        fig.add_trace(go.Bar(
                x=list(range(len(races))),
                y=bail_pct,
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailPct:.1f}% of 2021 total for {race}"
                           for bailPct, race in zip(bail_pct, races)],
                visible=False
        ))

    fig.update_layout(
        barmode='stack',
        legend={'traceorder': 'normal'},
        legend_title="Bail Types",
        title="Breakdown of Bail Types Set by Race: Percentages",
        xaxis_title="Race",
        yaxis_title="Percent",
        xaxis_tickvals=list(range(len(races))),
        xaxis_ticktext=races
    )
    
    fig.update_layout(
        updatemenus=[
            dict(active=0,
                 x=-0.35,
                 xanchor='left',
                 y=0.9,
                 yanchor='top',
                 buttons=list([
                     dict(label="2020",
                          method="update",
                          args=[{"visible": [True, True, True, True, True, False, False, False, False, False]},
                                {"title": "Bail type by race in 2020"}]),
                     dict(label="2021",
                          method="update",
                          args=[{"visible": [False, False, False, False, False, True, True, True, True, True]},
                                {"title": "Bail type by race in 2021"}])
                               ])
                     )
                ])
    
    fig.update_layout(
        annotations=[
            dict(text="Select year", x=-0.35, xref="paper", y=0.98, yref="paper",
                                 align="left", showarrow=False)
        ])
    
    f_pct = go.FigureWidget(fig)
    st.plotly_chart(f_pct)    
    
    # ----------------------------------
    #  Interactive figure: Bail Type Percentages by Sex
    # ----------------------------------    
    fig = go.Figure()
    
    for j, bailType in enumerate(bail_types):
        bail_pct = arr_sex_pct_2020[:, j]
        fig.add_trace(go.Bar(
                x=list(range(len(sexes))),
                y=bail_pct,
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailPct:.1f}% of 2020 total, {sex}"
                           for bailPct, sex in zip(bail_pct, sexes)]
        ))

    for j, bailType in enumerate(bail_types):
        bail_pct = arr_sex_pct_2021[:, j]
        fig.add_trace(go.Bar(
                x=list(range(len(sexes))),
                y=bail_pct,
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailPct:.1f}% of 2021 total for {sex}"
                           for bailPct, sex in zip(bail_pct, sexes)],
                visible=False
        ))

    fig.update_layout(
        barmode='stack',
        legend={'traceorder': 'normal'},
        legend_title="Bail Types",
        title="Breakdown of Bail Types Set by Sex: Percentages",
        xaxis_title="Race",
        yaxis_title="Sex",
        xaxis_tickvals=list(range(len(sexes))),
        xaxis_ticktext=sexes
    )
    
    fig.update_layout(
        updatemenus=[
            dict(active=0,
                 x=-0.35,
                 xanchor='left',
                 y=0.9,
                 yanchor='top',
                 buttons=list([
                     dict(label="2020",
                          method="update",
                          args=[{"visible": [True, True, True, True, True, False, False, False, False, False]},
                                {"title": "Bail type by sex in 2020"}]),
                     dict(label="2021",
                          method="update",
                          args=[{"visible": [False, False, False, False, False, True, True, True, True, True]},
                                {"title": "Bail type by sex in 2021"}])
                               ])
                     )
                ])
    
    fig.update_layout(
        annotations=[
            dict(text="Select year", x=-0.35, xref="paper", y=0.98, yref="paper",
                                 align="left", showarrow=False)
        ])

    f_pct_sex = go.FigureWidget(fig)
    st.plotly_chart(f_pct_sex)    

    # ----------------------------------
    #  Interactive figure: Bail Type Percentages by Age
    # ----------------------------------    
    fig = go.Figure()
    
    for j, bailType in enumerate(bail_types):
        bail_pct = arr_age_pct_2020[:, j]
        fig.add_trace(go.Bar(
                x=list(range(len(age_groups))),
                y=bail_pct,
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailPct:.1f}% of 2020 total, {age}"
                           for bailPct, age in zip(bail_pct, age_groups)]
        ))

    for j, bailType in enumerate(bail_types):
        bail_pct = arr_age_pct_2021[:, j]
        fig.add_trace(go.Bar(
                x=list(range(len(age_groups))),
                y=bail_pct,
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailPct:.1f}% of 2021 total for {age}"
                           for bailPct, age in zip(bail_pct, age_groups)],
                visible=False
        ))

    fig.update_layout(
        barmode='stack',
        legend={'traceorder': 'normal'},
        legend_title="Bail Types",
        title="Breakdown of Bail Types Set by Age: Percentages",
        xaxis_title="Race",
        yaxis_title="Age Group",
        xaxis_tickvals=list(range(len(age_groups))),
        xaxis_ticktext=age_groups
    )
    
    fig.update_layout(
        updatemenus=[
            dict(active=0,
                 x=-0.35,
                 xanchor='left',
                 y=0.9,
                 yanchor='top',
                 buttons=list([
                     dict(label="2020",
                          method="update",
                          args=[{"visible": [True, True, True, True, True, False, False, False, False, False]},
                                {"title": "Bail type by age in 2020"}]),
                     dict(label="2021",
                          method="update",
                          args=[{"visible": [False, False, False, False, False, True, True, True, True, True]},
                                {"title": "Bail type by age in 2021"}])
                               ])
                     )
                ])
    
    fig.update_layout(
        annotations=[
            dict(text="Select year", x=-0.35, xref="paper", y=0.98, yref="paper",
                                 align="left", showarrow=False)
        ])

    f_pct_age = go.FigureWidget(fig)
    st.plotly_chart(f_pct_age)   
    