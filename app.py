import streamlit as st
import pandas as pd

import home
import by_numbers
import magistrate
import price
import neighborhood
import race_gender
import by_demographics

def main():
    PAGES = {
        "Home": home,
        "By Year" : by_numbers,
        "By Actor" : magistrate,
        "By Price" : price,
        "By Neighborhood" : neighborhood,
        "By Demographics (original)": race_gender,
        "By Demographics": by_demographics
    }
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Please select a page", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

if __name__ == '__main__':
    main()