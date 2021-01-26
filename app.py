import streamlit as st

import home
import aggregate
import magistrate
import neighborhood
import race_gender

def main():
    PAGES = {
        "Home": home,
        "Summary" : aggregate,
        "Magistrates" : magistrate,
        "Neighborhoods" : neighborhood,
        "Race": race_gender
    }
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Please select a page", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

if __name__ == '__main__':
    main()