import pandas as pd
import streamlit as st
import plotly.graph_objs as go

@st.cache()
def plot_year_summary():
# plot year-end summary on top of each page
    # load data
    df_summary = pd.read_csv('data/cleaned/app_year_summary.csv', index_col = (0,1))

    ##### get summary data for 2020, 2020 YTM, 2021 YTM #####
    # get most recent month in 2021 YTD
    last_month = df_summary.loc[2021].index.max()

    # get summary information
    summary_2020 = df_summary.loc[(2020,)].sum()
    summary_2021 = df_summary.loc[(2021,)].sum()
    idx = pd.IndexSlice
    summary_2020_YTM = df_summary.loc[idx[2020, range(last_month + 1)], idx[:]].sum()

    # add monetary bail percentage for all summaries
    summary_2020["monetary_bail_perct"] = summary_2020["monetary_bail"]/summary_2020["count"]
    summary_2020_YTM["monetary_bail_perct"] = summary_2020_YTM["monetary_bail"] / summary_2020_YTM["count"]
    summary_2021["monetary_bail_perct"] = summary_2021["monetary_bail"]/summary_2021["count"]
    
    ##### plot yearly summary on top #####
    fig = go.Figure()
    # find string corresponding to last month
    month = {1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec"}
    month_str = month[last_month]

    # assign heights of rows
    y1_2020 = 0.5
    y2_2020 = 0.75

    y1_2020_YTM = 0.25
    y2_2020_YTM = 0.5

    y1_2021 = 0
    y2_2021 = 0.25

    # assign columns
    c0 = 0.12
    c1 = 0.34
    c2 = 0.56
    c3 = 0.78

    # 2020 data 
    fig.add_trace(go.Indicator(
        mode = "number",
        value = 2020,
        number={"font":{"size": 12}},
        domain = {'x': [0, c0], 'y': [y1_2020, y2_2020]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = summary_2020["bail_amount"],
        title = {"text": "<span style='font-size:1.4em'>Amount of bail set</span>"},
        number = {"prefix": "$",
                "font":{"size": 30}},
        domain = {'x': [c0, c1], 'y': [y1_2020, y2_2020]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = summary_2020["bail_paid"],
        title = {"text": "<span style='font-size:1.4em'>Amount of bail paid</span>"},
        number = {"prefix": "$",
                "font":{"size":30}},
        domain = {'x': [c1, c2], 'y': [y1_2020, y2_2020]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = summary_2020["monetary_bail_perct"]*100,
        title = {"text": "<span style='font-size:1.4em'>Percentage of bail set</span>"},
        number = {"suffix": "%",
                "font":{"size":30}},
        domain = {'x': [c2, c3], 'y': [y1_2020, y2_2020]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = summary_2020["monetary_bail"],
        title = {"text": "<span style='font-size:1.4em'>Number of people impacted</span>"},
        number = {
                "font":{"size": 30}},
        domain = {'x': [c3, 1], 'y': [y1_2020, y2_2020]}))

    # 2020 YTM data 
    fig.add_trace(go.Indicator(
        mode = "number",
        value = 2020,
        number={"font":{"size": 12},
                "suffix": " Jan-"+month_str},
        domain = {'x': [0, c0], 'y': [y1_2020_YTM, y2_2020_YTM]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = summary_2020_YTM["bail_amount"],
        number = {"prefix": "$",
                "font":{"size": 30}},
        domain = {'x': [c0, c1], 'y': [y1_2020_YTM, y2_2020_YTM]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = summary_2020_YTM["bail_paid"],
        number = {"prefix": "$",
                "font":{"size":30}},
        domain = {'x': [c1, c2], 'y': [y1_2020_YTM, y2_2020_YTM]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = summary_2020_YTM["monetary_bail_perct"]*100,
        number = {"suffix": "%",
                "font":{"size":30}},
        domain = {'x': [c2, c3], 'y': [y1_2020_YTM, y2_2020_YTM]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = summary_2020_YTM["monetary_bail"],
        number = {
                "font":{"size": 30}},
        domain = {'x': [c3, 1], 'y': [y1_2020_YTM, y2_2020_YTM]}))

    # 2021 data
    fig.add_trace(go.Indicator(
        mode = "number",
        value = 2021,
        number={"font":{"size": 12},
                "suffix": " Jan-"+month_str},
        domain = {'x': [0, c0], 'y': [y1_2021, y2_2021]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = summary_2021["bail_amount"],
        number = {"prefix": "$",
                "font":{"size":30}},
        domain = {'x': [c0, c1], 'y': [y1_2021, y2_2021]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = summary_2021["bail_paid"],
        number = {"prefix": "$",
                "font": {"size":30}},
        domain = {'x': [c1, c2], 'y': [y1_2021, y2_2021]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = summary_2021["monetary_bail_perct"]*100,
        number = {"font": {"size":30},
                "suffix": "%"},
        domain = {'x': [c2, c3], 'y': [y1_2021, y2_2021]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = summary_2021["monetary_bail"],
        number = {"font": {"size":30}},
        domain = {'x': [c3, 1], 'y': [y1_2021, y2_2021]}))

                
    fig.update_layout(
        height = 160,
        margin = dict(t = 0, b = 0, l = 0, r = 0)
    )

    return fig 
