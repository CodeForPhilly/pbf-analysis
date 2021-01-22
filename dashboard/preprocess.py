import ast
import datetime
import itertools
import numpy as np
import pandas as pd
import random
import regex as re
import json
import copy
import math
import streamlit as st

# load and preprocess docket/court summary data
#@st.cache
def preprocess():
    # Import and join docket and court summary csv files
    docketdf = pd.read_csv("../docket.csv", index_col=0)
    courtdf = pd.read_csv("../court_summary.csv", index_col=0)
    df = docketdf.merge(courtdf, on='docket_no', how='left', suffixes=('', '_y'))
    df = df.reset_index()
    df = df.drop(columns=['docket_no'])
    df = df.drop(df.filter(regex='_y$').columns.tolist(), axis=1)
    
    # fill empty bail_type with 'Denied'
    df[['bail_type']] = df[['bail_type']].fillna('Denied')
    
    # Correct 'Emergency Arraignment Court Magistrate' to 'E-Filing Judge'
    df['bail_set_by'] = df['bail_set_by'].apply(lambda x: 'E-Filing Judge' if x == 'Emergency Arraignment Court Magistrate' else x)
    
    # convert string to datetime
    df["offense_date"] = pd.to_datetime(df["offense_date"])
    df["arrest_dt"] = pd.to_datetime(df["arrest_dt"])
    #df["dob"] = pd.to_datetime(df["dob"])
    df["bail_date"] = pd.to_datetime(df["bail_date"])
    #df["prelim_hearing_dt"] = df["prelim_hearing_dt"].apply(
    #    lambda x: str(x).split(' ')[0] if pd.notnull(x) else x) # This is here because of a parsing issue
    #df["prelim_hearing_dt"] = pd.to_datetime(df["prelim_hearing_dt"])
    df["prelim_hearing_time"] = pd.to_datetime(df["prelim_hearing_time"])

    # age column
    #df['age'] = df['arrest_dt'] - df['dob']
    #df['age'] = df['age'].apply(lambda x: np.floor(x.days/365.2425))

    # public defender column: 1 if public defender, 0 if private defender
    # note that there is also an "attorney_type" column, with "Public", "Private", and "Court Appointed" options
    df["public_defender"] = df["attorney"].apply(lambda x: 1 if x =='Defender Association of  Philadelphia' else 0)

    # convert string representation of list to list
    #df["offenses"] = df["offenses"].apply(lambda x: ast.literal_eval(x))
    #df['offense_type'] = df['offense_type'].apply(lambda x: ast.literal_eval(x))
    #df['statute'] = df['statute'].apply(lambda x: ast.literal_eval(x))

    # zipcode: remove everything after hyphen
    df["zipcode_clean"] = df["zip"].apply(lambda x: re.sub('-.*$','',x) if type(x) == str else x)

    # column indicating whether zipcode is in Philadelphia
    philly_zipcode = list(range(19102, 19155))
    philly_zipcode = [str(item) for item in philly_zipcode]
    df['philly_zipcode'] = df['zipcode_clean'].apply(lambda x: 1 if x in philly_zipcode else 0)

    # categorical column indicating if bail is paid
    df['bail_paid_YN'] = df['bail_paid'].apply(lambda x: "no" if x == 0 else "yes")
    
    # column for bail amount bins
    df['bail_set_bin'] = df['bail_amount'].apply(lambda x: bin_bailSet(x))
    
    # column for bail amount bins
    #df['age_group'] = df['age'].apply(lambda x: bin_age(x))
    
    # drop unnecessary columns
    return df

# Define bins for bail amount
#@st.cache()
def bin_bailSet(bailSet):
    if bailSet == 0 or pd.isnull(bailSet):
        return 'None'
    elif bailSet < 1000:
        return '<1k'
    elif bailSet < 5000:
        return '1k to 5k'
    elif bailSet < 10000:
        return '5k to 10k'
    elif bailSet < 25000:
        return '10k to 25k'
    elif bailSet < 50000:
        return '25k to 50k'
    elif bailSet < 100000:
        return '50k to 100k'
    elif bailSet < 500000:
        return '100k to 500k'
    else:
        return '>=500k'

# Define bins for bail amount
#@st.cache()
def bin_age(age):
    if age < 18:
        return 'minor'
    elif age < 26:
        return '18 to 25'
    elif age < 34:
        return '26 to 33'
    elif age < 42:
        return '34 to 41'
    elif age < 50:
        return '42 to 49'
    elif age < 58:
        return '50 to 57'
    elif age < 65:
        return '58 to 64'
    else:
        return 'senior'

# load/preprocess ACS poverty/income data
#@st.cache()
def preprocess_acs():
    income_df = pd.read_csv('../data/income/cleaned_income.csv')
    income_df = income_df[['zipcode', 'households_median_income']]
    
    poverty_df = pd.read_csv('../data/poverty/cleaned_poverty.csv')
    poverty_df = poverty_df[['zipcode', 'percent_below_poverty']]

    unemployment_df = pd.read_csv('../data/unemployment/cleaned_unemployment.csv')
    unemployment_df = unemployment_df[['zipcode', 'unemployment_rate']]    
    
    acs_df = income_df.merge(poverty_df, on='zipcode', how='outer')
    acs_df = acs_df.replace('-', np.nan)
    acs_df = acs_df.set_index('zipcode')
    acs_df = acs_df.apply(pd.to_numeric).reset_index()
    
    acs_df = acs_df.merge(unemployment_df, on='zipcode', how='outer')
    acs_df = acs_df.replace('-', np.nan)
    acs_df = acs_df.set_index('zipcode')
    acs_df = acs_df.apply(pd.to_numeric).reset_index()    
    
    return acs_df