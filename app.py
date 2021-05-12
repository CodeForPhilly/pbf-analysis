import streamlit as st
import pandas as pd

import home
import by_numbers
import magistrate
import price
import neighborhood
import by_demographics
import interesting_finds

def main():
    PAGES = {
        "By Year" : by_numbers,
        "By Actor" : magistrate,
        "By Demographics": by_demographics,
        "By Cost to Philadelphians" : neighborhood,
        "About": home,
    }
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Please select a page", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

if __name__ == '__main__':
    main()