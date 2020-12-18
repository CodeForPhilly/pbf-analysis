import numpy as np
import pandas as pd
import streamlit as st

import home
import aggregate
import magistrate
import neighborhood
import race_gender

def main():
    PAGES = {
        "Home": home,
        "Aggregate" : aggregate,
        "Magistrate" : magistrate,
        "Neighborhood" : neighborhood,
        "Race & Gender": race_gender
    }
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

if __name__ == '__main__':
    main()