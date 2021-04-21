import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from year_summary import plot_year_summary

def app():

    # year-end summary
    fig = plot_year_summary()
    f_year = go.FigureWidget(fig)
    st.plotly_chart(f_year)

    ##### Comparison controling for offense types #####

    st.header("By actor analysis with controlled offense types")
    st.write("While the 'By Actor' page provides a useful year-end summary, it does not provide a fair comparison of the actors. \
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
