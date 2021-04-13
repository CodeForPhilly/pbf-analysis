import pandas as pd
import streamlit as st
import plotly.graph_objs as go

@st.cache()
def plot_year_summary():
# plot year-end summary on top of each page
    df_summary = pd.read_csv('data/cleaned/app_year_summary.csv', index_col = 0)
    
    # plot yearly summary on top
    fig = go.Figure()

    # 2020 data 
    fig.add_trace(go.Indicator(
        mode = "number",
        value = 2020,
        number={"font":{"size": 12}},
        domain = {'x': [0, 0.08], 'y': [0.4, 1]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = df_summary.at[2020,"bail_amount"],
        title = {"text": "<span style='font-size:1.6em'>Amount of bail set</span>"},
        number = {"prefix": "$",
                "font":{"size": 30}},
        domain = {'x': [0.08, 0.31], 'y': [0.4, 1]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = df_summary.at[2020,"bail_paid"],
        title = {"text": "<span style='font-size:1.6em'>Amount of bail paid</span>"},
        number = {"prefix": "$",
                "font":{"size":30}},
        domain = {'x': [0.31, 0.54], 'y': [0.4, 1]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = df_summary.at[2020, "monetary_bail_perct"]*100,
        title = {"text": "<span style='font-size:1.6em'>Percentage of bail set</span>"},
        number = {"suffix": "%",
                "font":{"size":30}},
        domain = {'x': [0.54, 0.77], 'y': [0.4, 1]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = df_summary.at[2020,"monetary_bail"],
        title = {"text": "<span style='font-size:1.6em'>Number of people impacted</span>"},
        number = {
                "font":{"size": 30}},
        domain = {'x': [0.77, 1], 'y': [0.4, 1]}))

    # 2021 data
    fig.add_trace(go.Indicator(
        mode = "number",
        value = 2021,
        number={"font":{"size": 12},
                "suffix": "YTD"},
        domain = {'x': [0, 0.08], 'y': [0, 0.6]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = df_summary.at[2021,"bail_amount"],
        number = {"prefix": "$",
                "font":{"size":30}},
        domain = {'x': [0.08, 0.31], 'y': [0, 0.6]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = df_summary.at[2021,"bail_paid"],
        number = {"prefix": "$",
                "font": {"size":30}},
        domain = {'x': [0.31, 0.54], 'y': [0, 0.6]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = df_summary.at[2021, "monetary_bail_perct"]*100,
        number = {"font": {"size":30},
                "suffix": "%"},
        domain = {'x': [0.54, 0.77], 'y': [0, 0.6]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = df_summary.at[2021,"monetary_bail"],
        number = {"font": {"size":30}},
        domain = {'x': [0.77, 1], 'y': [0, 0.6]}))

                
    fig.update_layout(
        height = 140,
        margin = dict(t = 0, b = 0, l = 0, r = 0)
    )

    return fig 
