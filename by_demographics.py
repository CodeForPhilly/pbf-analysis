import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from year_summary import plot_year_summary

def format_df_amount(df, category):
    """Group bail amount set by columns (retaining "empty" groups)."""
    return df.groupby(['bail_year', category])['bail_amount_sum'].sum().unstack(fill_value=0).stack()

def format_df_type(df, category, flag):
    """Group bail types set by columns (retaining "empty" groups). 
    flag must be 'count' (for total number of people) or 'pct' (for percentage of people in a given category)"""
    return df.groupby(['bail_year', category, 'bail_type'])[f'bail_type_{flag}'].sum().unstack(fill_value=0).stack()    

@st.cache()
def load_race_data():
    category = 'race_group'
    df_bail_set = pd.read_csv('data/cleaned/app_race_bail_set.csv')
    df_bail_type = pd.read_csv('data/cleaned/app_race_bail_type.csv')
    df_bail_set = format_df_amount(df_bail_set, category)
    df_bail_type_pct = format_df_type(df_bail_type, category, 'pct')
    df_bail_type_count = format_df_type(df_bail_type, category, 'count')
    return df_bail_set, df_bail_type_pct, df_bail_type_count

@st.cache()
def load_sex_data():
    category = 'sex'
    df_bail_set = pd.read_csv('data/cleaned/app_sex_bail_set.csv')
    df_bail_type = pd.read_csv('data/cleaned/app_sex_bail_type.csv')
    df_bail_set = format_df_amount(df_bail_set, category)
    df_bail_type_pct = format_df_type(df_bail_type, category, 'pct')
    df_bail_type_count = format_df_type(df_bail_type, category, 'count')
    return df_bail_set, df_bail_type_pct, df_bail_type_count

@st.cache()
def load_age_data():
    category = 'age_group'
    df_bail_set = pd.read_csv('data/cleaned/app_age_bail_set.csv')
    df_bail_type = pd.read_csv('data/cleaned/app_age_bail_type.csv')
    df_bail_set = format_df_amount(df_bail_set, category)
    df_bail_type_pct = format_df_type(df_bail_type, category, 'pct')
    df_bail_type_count = format_df_type(df_bail_type, category, 'count')
    return df_bail_set, df_bail_type_pct, df_bail_type_count

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
    years = [2020, 2021]
    bail_types = ['Denied', 'Monetary', 'Nonmonetary', 'ROR', 'Unsecured']
    races = ['Black', 'White', 'Other']
    sexes = ['Male', 'Female']
    age_groups = ['minor', '18 to 25', '26 to 64', '65+']
                           
    df_race_bail_set, df_race_bail_type, df_race_bail_type_count = load_race_data()
    df_sex_bail_set, df_sex_bail_type, df_sex_bail_type_count = load_sex_data()
    df_age_bail_set, df_age_bail_type, df_age_bail_type_count = load_age_data()  
    
    arr_race_pct_2020 = np.array([df_race_bail_type[2020][race] for race in races], dtype=object)
    arr_race_pct_2021 = np.array([df_race_bail_type[2021][race] for race in races], dtype=object)
    arr_race_count_2020 = np.array([df_race_bail_type_count[2020][race] for race in races], dtype=object)
    arr_race_count_2021 = np.array([df_race_bail_type_count[2021][race] for race in races], dtype=object)
    
    arr_sex_pct_2020 = np.array([df_sex_bail_type[2020][sex] for sex in sexes], dtype=object)
    arr_sex_pct_2021 = np.array([df_sex_bail_type[2021][sex] for sex in sexes], dtype=object)
    arr_sex_count_2020 = np.array([df_sex_bail_type_count[2020][sex] for sex in sexes], dtype=object)
    arr_sex_count_2021 = np.array([df_sex_bail_type_count[2021][sex] for sex in sexes], dtype=object)
    
    arr_age_pct_2020 = np.array([df_age_bail_type[2020][age] for age in age_groups], dtype=object)
    arr_age_pct_2021 = np.array([df_age_bail_type[2021][age] for age in age_groups], dtype=object)    
    arr_age_count_2020 = np.array([df_age_bail_type_count[2020][age] for age in age_groups], dtype=object)
    arr_age_count_2021 = np.array([df_age_bail_type_count[2021][age] for age in age_groups], dtype=object)

    # ----------------------------------
    #  Interactive figure formatting
    # ----------------------------------
    
    dropdown_content = dict(active=0,
                            x=-0.35,
                            y=0.9,
                            xanchor='left',
                            yanchor='top',
                            buttons=list([
                                dict(label="2020",
                                     method="update",
                                     args=[{"visible": [True, True, True, True, True,
                                                        False, False, False, False, False]}]),
                                dict(label="2021",
                                     method="update",
                                     args=[{"visible": [False, False, False, False, False,
                                                        True, True, True, True, True]}])
                                ])
                           )
    
    dropdown_title = dict(text="Select year:",
                          x=-0.35, 
                          y=0.98,
                          xref="paper",
                          yref="paper",
                          align="left",
                          showarrow=False)
    
    common_layout = dict(barmode='stack',
                         legend={'traceorder': 'normal'},
                         legend_title="Bail Types",
                         yaxis_title="Percent")
    
    # ----------------------------------
    #  Interactive figure: Bail Type Percentages by Race
    # ----------------------------------
    st.write("In 2020, monetary bail was set more frequently for people identified by the court system as Black than those identified as non-Black (White or Other).")    
    
    fig = go.Figure()
    
    for j, bailType in enumerate(bail_types):
        bail_pct = arr_race_pct_2020[:, j]
        bail_count = arr_race_count_2020[:, j]
        fig.add_trace(go.Bar(
                x=list(range(len(races))),
                y=bail_pct,
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailPct:.1f}% of 2020 total, {race} ({count:,d} people)"
                           for bailPct, race, count in zip(bail_pct, races, bail_count)]
        ))
    
    for j, bailType in enumerate(bail_types):
        bail_pct = arr_race_pct_2021[:, j]
        bail_count = arr_race_count_2020[:, j]
        fig.add_trace(go.Bar(
                x=list(range(len(races))),
                y=bail_pct,
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailPct:.1f}% of 2021 total, {race} ({count:,d} people)"
                           for bailPct, race, count in zip(bail_pct, races, bail_count)],
                visible=False
        ))

    fig.update_layout(title="Breakdown of Bail Type by Race",
                      xaxis_title="Race",
                      xaxis_tickvals=list(range(len(races))),
                      xaxis_ticktext=races)
    
    fig.update_layout(updatemenus=[dropdown_content],
                      annotations=[dropdown_title],
                      **common_layout)
    
    f_pct = go.FigureWidget(fig)
    st.plotly_chart(f_pct)    

    st.write("Note: While additional race categories beyond \"White\" and \"Black\" are recognized by the Pennsylvania court system, these are grouped together as \"Other\" out of anonymization concerns. The Philadelphia Bail Fund has observed that the Philadelphia court system appears to record most non-Black and non-Asian people, such as Latinx and Indigenous people, as White.")
    st.write("**<font color='red'>Question for PBF</font>**: what disclaimer language would you like to include here? The above was informed by the language in the July 2020 report.", unsafe_allow_html=True)    
    
    # ----------------------------------
    #  Interactive figure: Bail Type Percentages by Sex
    # ----------------------------------    
    st.write("In 2020, monetary bail was set more frequently for people identified by the court system as male than those identified as female.")
    
    fig = go.Figure()
    
    for j, bailType in enumerate(bail_types):
        bail_pct = arr_sex_pct_2020[:, j]
        bail_count = arr_sex_count_2020[:, j]
        fig.add_trace(go.Bar(
                x=list(range(len(sexes))),
                y=bail_pct,
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailPct:.1f}% of 2020 total, {sex} ({count:,d} people)"
                           for bailPct, sex, count in zip(bail_pct, sexes, bail_count)]
        ))

    for j, bailType in enumerate(bail_types):
        bail_pct = arr_sex_pct_2021[:, j]
        bail_count = arr_sex_count_2021[:, j]
        fig.add_trace(go.Bar(
                x=list(range(len(sexes))),
                y=bail_pct,
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailPct:.1f}% of 2021 total for {sex} ({count:,d} people)"
                           for bailPct, sex, count in zip(bail_pct, sexes, bail_count)],
                visible=False
        ))

    fig.update_layout(title="Breakdown of Bail Type by Sex",
                      xaxis_title="Sex",
                      xaxis_tickvals=list(range(len(sexes))),
                      xaxis_ticktext=sexes)
    
    fig.update_layout(updatemenus=[dropdown_content],
                      annotations=[dropdown_title],
                      **common_layout)

    f_pct_sex = go.FigureWidget(fig)
    st.plotly_chart(f_pct_sex)    


    
    # ----------------------------------
    #  Interactive figure: Bail Type Percentages by Age
    # ----------------------------------    
    st.write("In 2020, the frequency of monetary bail decreased with increasing age group.")
    
    fig = go.Figure()
    
    for j, bailType in enumerate(bail_types):
        bail_pct = arr_age_pct_2020[:, j]
        bail_count = arr_age_count_2020[:, j]
        fig.add_trace(go.Bar(
                x=list(range(len(age_groups))),
                y=bail_pct,
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailPct:.1f}% of 2020 total, {age} ({count:,d} people)"
                           for bailPct, age, count in zip(bail_pct, age_groups, bail_count)]
        ))

    for j, bailType in enumerate(bail_types):
        bail_pct = arr_age_pct_2021[:, j]
        bail_count = arr_age_count_2021[:, j]
        fig.add_trace(go.Bar(
                x=list(range(len(age_groups))),
                y=bail_pct,
                orientation="v",
                text="",
                textposition="inside",
                name=bailType,
                hoverinfo="text",
                hovertext=[f"{bailType}: {bailPct:.1f}% of 2021 total for {age} ({count:,d} people)"
                           for bailPct, age, count in zip(bail_pct, age_groups, bail_count)],
                visible=False
        ))

    fig.update_layout(title="Breakdown of Bail Type by Age",
                      xaxis_title="Age Group",
                      xaxis_tickvals=list(range(len(age_groups))),
                      xaxis_ticktext=age_groups)
    
    fig.update_layout(updatemenus=[dropdown_content],
                      annotations=[dropdown_title],
                      **common_layout)

    f_pct_age = go.FigureWidget(fig)
    st.plotly_chart(f_pct_age)   
    
 