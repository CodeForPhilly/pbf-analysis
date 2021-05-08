import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from year_summary import plot_year_summary

@st.cache()
def load_data():
    df_2020 = pd.read_csv('data/cleaned/app_magistrate_data_2020.csv')
    df_2021 = pd.read_csv('data/cleaned/app_magistrate_data_2021.csv')
    return df_2020, df_2021

def app():

    # year-end summary
    fig = plot_year_summary()
    f_year = go.FigureWidget(fig)
    st.plotly_chart(f_year)

    st.title('Breakdown by Actor')
    st.write('This section provides a summary of how bail type and bail amount depend on the person setting the bail (hereby referred to as the actor).')

    # ----------------------------------
    #  interactive summary plots
    # ----------------------------------
    st.subheader("Comparison of bail type")
    # load data for interactive plot
    df_magistrate_2020, df_magistrate_2021 = load_data()
    # prepare data
    bail_type = ["Monetary", "ROR", "Unsecured", "Nonmonetary", "Denied"]
    bail_type_count = ["Monetary_count", "ROR_count", "Unsecured_count", "Nonmonetary_count", "Denied_count"]

    data_2020 = np.array(df_magistrate_2020[bail_type]).transpose()
    count_2020 = np.array(df_magistrate_2020[bail_type_count]).transpose()
    names_2020 = list(df_magistrate_2020['magistrate'].values)
    total_2020 = df_magistrate_2020['Total'].astype(int)
    bail_set_2020 = df_magistrate_2020['bail_amount']

    data_2021 = np.array(df_magistrate_2021[bail_type]).transpose()
    count_2021 = np.array(df_magistrate_2021[bail_type_count]).transpose()
    names_2021 = list(df_magistrate_2021['magistrate'].values)
    total_2021 = df_magistrate_2021['Total'].astype(int)
    bail_set_2021 = df_magistrate_2021['bail_amount']
    
    # Initialize figure
    fig = go.Figure()

    ##### add traces for 2020
    for i in range(5):
    
        # text
        text = [str(item)+"%"  if item > 6 else "" for item in data_2020[i]]

        # hover text
        # include monetary bail
        if i == 0: 
                hovertext = ["name: " + name + "<br>"
                        + "percentage: " + str(perct) + "%" + "<br>"
                        + "case count: " + str(case) + " / " + str(total) + "<br>"
                        + "total monetary bail amount set: " + str(amount) 
                        for name, perct, case, total, amount in zip(names_2020, data_2020[i], count_2020[i], total_2020, bail_set_2020)]
        else:
                hovertext = ["name: " + name + "<br>"
                        + "percentage: " + str(perct) + "%" + "<br>"
                        + "case count: " + str(case) + " / " + str(total)
                        for name, perct, case, total in zip(names_2020, data_2020[i], count_2020[i], total_2020)]

        fig.add_trace(go.Bar(
        y = names_2020,
        x = data_2020[i],
        text = text,
        textposition = "inside",
        name = bail_type[i],
        hoverinfo = 'text',
        hovertext = hovertext,
        orientation = 'h'))

    ##### add traces for 2021
    for i in range(5):
    
        # text
        text = [str(item)+"%"  if item > 6 else "" for item in data_2021[i]]

        # hover text
        # include monetary bail
        if i == 0: 
                hovertext = ["name: " + name + "<br>"
                        + "percentage: " + str(perct) + "%" + "<br>"
                        + "case count: " + str(case) + " / " + str(total) + "<br>"
                        + "total monetary bail amount set: " + str(amount) 
                        for name, perct, case, total, amount in zip(names_2021, data_2021[i], count_2021[i], total_2021, bail_set_2021)]
        else:
                hovertext = ["name: " + name + "<br>"
                        + "percentage: " + str(perct) + "%" + "<br>"
                        + "case count: " + str(case) + " / " + str(total)
                        for name, perct, case, total in zip(names_2021, data_2021[i], count_2021[i], total_2021)]

        fig.add_trace(go.Bar(
        y = names_2021,
        x = data_2021[i],
        text = text,
        textposition = "inside",
        name = bail_type[i],
        hoverinfo = 'text',
        hovertext = hovertext,
        orientation = 'h',
        visible = False # hide in initial plot
        ))

    fig.update_layout(barmode='stack',
                 legend = {'traceorder': 'normal'},
                 xaxis_title="percentage",
                 yaxis_title="magistrate",
                 legend_title="bail type")
    
    # update
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                x = -0.35,
                xanchor = 'left',
                y = 0.9,
                yanchor = 'top',
                buttons=list([
                    dict(label="2020",
                         method="update",
                         args=[{"visible": [True, True, True, True, True, False, False, False, False, False]},
                               {"title": "Bail type by actor in 2020"}]),
                    dict(label="2021",
                         method="update",
                         args=[{"visible": [False, False, False, False, False, True, True, True, True, True]},
                               {"title": "Bail type by actor in 2021"}])
                ]),
            )   
        ])

    fig.update_layout(
        annotations=[
            dict(text="Select year", x=-0.35, xref="paper", y=0.98, yref="paper",
                                 align="left", showarrow=False)
        ])

    # Update plot sizing
    fig.update_layout(
        margin=dict(t=100, b=0, l=0, r=0),
        title = "Bail type by actor in 2020"
    )

    f2 = go.FigureWidget(fig)
    st.plotly_chart(f2)

    st.write("The above figure summarizes the percentage of bail types set by each actors. \
            For the year 2020, we selected 10 actors that handled the highest number of cases. \
            For the year 2021, we summarize the data upto March 31, 2021. \
            Hover your mouse over the figure for further details.")

    st.write("**<font color='red'>Note to PBF</font>**: For every case in which bail was denied, there was no magistrate information found. Is this correct? ", unsafe_allow_html=True)
    ##### 2020 Summary plots #####

    # Explain selection of magistrates (Those who handled more than 500 cases)
    # Some timeline (Many were involved consistently throughout the year. Some were seasonal)
    # Explain 'Others': Those who set fewer than 500 cases. Total number of those labeled as "Others"

    # number of cases
    """
    st.header("1. Year-End Summary by Actor")
    st.subheader("Number of cases handled by each magistrate")

    _, col, _ = st.beta_columns([1,2,1])
    image = Image.open('figures/magistrate_case_count.png')
    col.image(image)
    st.write("In the year 2020, bail was set by 37 different people. We provide a summary of the bail type and bail amount for cases handled by the nine magistrates who handled more than 300 cases in the year 2020.")

    # bail type
    st.subheader("Percentage of bail type for each magistrate")
    """
    """
    st.write("**<font color='red'>Question for PBF</font>**: Would you prefer the following pie chart or the stacked bar chart?",  unsafe_allow_html=True)
    image = Image.open('figures/magistrate_type_summary.png')
    st.image(image, use_column_width=True)

    image = Image.open('figures/magistrate_type_summary_bar.png')
    st.image(image)
    """

    # bail amount
    st.subheader("Comparison of bail amount")

    df_monetary = pd.read_csv("data/cleaned/app_magistrate_amount.csv", index_col = 0)
    df_monetary_2020 = df_monetary[df_monetary["year"] == 2020]
    df_monetary_2021 = df_monetary[df_monetary["year"] == 2021]

    names_2020 = df_monetary_2020.groupby("magistrate")["bail_amount"].median().sort_values()
    names_2021 = df_monetary_2021.groupby("magistrate")["bail_amount"].median().sort_values()

    fig = go.Figure()

    # add traces for 2020
    for name in names_2020.index:
        data = df_monetary_2020[df_monetary_2020["magistrate"] == name].bail_amount
        fig.add_trace(go.Box(x = data, 
                            name = name.split(',')[0],
                            hoverinfo = 'skip'))
        
        
    # add traces for 2021
    for name in names_2021.index:
        data = df_monetary_2021[df_monetary_2021["magistrate"] == name].bail_amount
        fig.add_trace(go.Box(x = data,
                            name = name.split(',')[0],
                            hoverinfo = 'skip',
                            visible = False))

        
    # update
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                x = -0.5,
                xanchor = 'left',
                y = 0.9,
                yanchor = 'top',
                buttons=list([
                    dict(label="2020",
                        method="update",
                        args=[{"visible": [True]*len(names_2020) + [False] * len(names_2021)},
                            {"title": "Bail amount by actor in 2020"}]),
                    dict(label="2021",
                        method="update",
                        args=[{"visible": [False]*len(names_2020) + [True] * len(names_2021)},
                            {"title": "Bail amount by actor in 2021"}])
                ]),
            )
            
        ])
        
    fig.update_layout(xaxis_range=[0,300000],
                    showlegend = False,
                    title = "Bail amount by actor in 2020",
                    xaxis_title="amount",
                    yaxis_title="actor",
                    annotations=[
                                 dict(text="Select year", x=-0.5, xref="paper", y=0.98, yref="paper",
                                 align="left", showarrow=False)
        ])
    f3 = go.FigureWidget(fig)
    st.plotly_chart(f3) 
        
        
    fig.update_layout(xaxis_range=[0,300000],
                    showlegend = False,
                    title = "Bail amount by actor in 2020",
                    xaxis_title="amount",
                    yaxis_title="actor")



    #image = Image.open('figures/magistrate_amount_summary.png')
    #_, col, _ = st.beta_columns([1, 5, 1])
    #col.image(image, use_column_width = True)
    st.write("The above box plot compares the monetary bail amount set by different actors for the year 2020. \
            For each actor, the vertical line in the colored box represents the median bail amount set by that actor. \
            The colored boxes represent the 25% to 75% range of the bail amount set by the magistrate. The dots represent outliers.")
    st.write("On average (median), the bail amount set by Connor, Bernard, and Rigmaiden-DeLeon ($50k) is higher than the bail amount set by others ($25k). \
            Moreover, Connor and Bernard seem to have set a wider range of bail amounts than other actors. ")
    
        ##### Comparison controling for offense types #####

    st.header("Analysis with controlled offense types")
    st.write("While the above analysis provides a useful year-end summary, it does not provide a fair comparison of the actors. \
            In particular, the differences among actors may stem from the fact that some actors may have handled more cases with more severe charges.")
            
    st.write("We compared the bail type and bail amount set by the actors while controlling for the difference in the charges. \
            We selected size actors (Bernard, Rainey, Rigmaiden-DeLeon, Stack, E-Filing Judge, and O'Brien) that handled more than 1000 cases in the year 2020. \
            We then conducted a matched study where we sampled cases with the same charges that were handled by the six actors.")
            
    st.write("The following results were obtained from the 3264 cases (544 per magistrate) that were sampled. Ideally, there shouldn't be any noticeable difference across actors.")
    st.write("Note that due to the sampling nature of the matched study, the matched dataset will vary across samples. However, the general trends observed below were consistent across multiple samples.")
    # bail type
    st.subheader("Percentage of bail type for each magistrate")
    #st.write("**<font color='red'>Question for PBF</font>**: Would you prefer the pie chart or the bar chart?",  unsafe_allow_html=True)
    image = Image.open('figures/magistrate_matched_type.png')
    st.image(image, use_column_width=True)

    #image = Image.open('figures/magistrate_matched_type_bar.png')
    #st.image(image)
    st.write("When we control for the offense types, all actors set monetary bail to 31%-44% of their cases.")

    # bail amount
    st.subheader("Monetary bail amount set by each magistrate")
    st.write("In the box plot, the colored bars represent the 25% to 75% range of the bail amount set by the magistrate.",  unsafe_allow_html=True) 
    _, col, _ = st.beta_columns([1, 5, 1])
    image = Image.open('figures/magistrate_matched_amount.png')
    col.image(image, use_column_width = True)
    """
    _, col, _ = st.beta_columns([1, 10, 1])
    image = Image.open('figures/magistrate_matched_amount_countplot.png')
    col.image(image, use_column_width = True)
    """
    st.write("Even when we control for offense types, we see a difference in the monetary bail amount across actors.\
            While the median bail amounts are similar, comparing the colored boxes (which indicates the 25% - 75% range of bail amounts) show that Bernard, Rainey, and Rigmaiden-DeLeon tend to set higher bail amounts than the others.")

    st.write("**<font color='red'>Note to PBF</font>**: The dashboard mockup contained two extrafigures: `DAO bail request breakdown` and `DAO vs magistrates`. However, we currently don't have the data.", unsafe_allow_html=True)

