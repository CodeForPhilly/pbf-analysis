"""
Define functions to preprocess the raw data from pbf-scraping.
Include the following cell/script at the beginning of every analysis script:
    import preprocess
    df = preprocess.merge_and_clean_data(path_to_docket_csv, path_to_court_csv,
                                         outPath=path_to_output_csv)
    preprocess.trim_data_for_app(df, outPath=path_to_trimmed_csv)
"""

import os
import ast

import numpy as np
import pandas as pd
import regex as re

# =============================================================================
# Functions to be called outside of this file
# =============================================================================
def merge_and_clean_data(docketPath, courtPath, outPath='full_data.csv',
                         overwrite=False, verbose=False):
    """Preprocess raw data: merge, clean, and add columns.
    Arguments:
        docketPath: full path to docket raw data .csv file
        courtPath:  full path to court summary raw data .csv file
        outPath:    full path to output .csv file with preprocessed data
    Returns:
        df:         DataFrame containing preprocessed data
    """
    
    # Try to load existing file, if desired
    if not overwrite:
        try:
            # Load and convert dates and lists to appropriate formats
            df = pd.read_csv(outPath)
            df = convert_dates_to_datetime(df)
            df = convert_lists(df)
            print("> Loaded existing file")
            
            return df
        
        except FileNotFoundError:
            pass
    
    # Import and merge docket and court summary raw data; drop extra columns
    docketdf = pd.read_csv(docketPath, index_col=0)
    courtdf = pd.read_csv(courtPath, index_col=0)
    df = docketdf.merge(courtdf, on='docket_no', how='left', suffixes=('', '_y'))
    df.reset_index(inplace=True)
    df.drop(columns=['docket_no'], inplace=True)
    df.drop(df.filter(regex='_y$').columns.tolist(), axis=1, inplace=True)

    # =========================================================================
    # Update data formats
    # =========================================================================
    df = convert_dates_to_datetime(df)
    df = convert_lists(df)
    
    # =========================================================================
    # Clean data in existing columns
    # =========================================================================
    # Fill empty bail_type with 'Denied'
    df[['bail_type']] = df[['bail_type']].fillna('Denied')
    
    # Convert 'Emergency Arraignment Court Magistrate' to 'E-Filing Judge'
    df['bail_set_by'] = df['bail_set_by'].apply(
        lambda x: 'E-Filing Judge' if x == 'Emergency Arraignment Court Magistrate' else x)

    # Clean zipcode column: remove everything after hyphen if present
    df['zip'] = df['zip'].apply(
        lambda x: re.sub('-.*$', '', x) if type(x) == str else x)

    # Remove small number of cases for which 'prelim_hearing_dt' and
    # 'bail_date' differ by more than 4 days... why though?
    maxDays = 5
    if verbose:
        nOutliers = len(df[(df['bail_date'] - df['prelim_hearing_dt']).dt.days >= maxDays])
        print(f"Removing {nOutliers} cases for which prelim_hearing_dt - bail_date was more than {maxDays}...")
    df = df[(df['bail_date'] - df['prelim_hearing_dt']).dt.days < 5]
    df.reset_index(drop=True, inplace=True)
    
    # =========================================================================
    # Create new columns from existing column data
    # =========================================================================
    # Create boolean column indicating whether zipcode is in Philadelphia
    philly_zip = list(range(19102, 19155))
    philly_zip = [str(item) for item in philly_zip]
    df['is_philly_zipcode'] = df['zip'].apply(lambda x: 1 if x in philly_zip else 0)

    # Create column corresponding to age at time of arrest
    df['age'] = df['arrest_dt'] - df['dob']
    df['age'] = df['age'].apply(lambda x: np.floor(x.days/365.2425))
    df.drop(columns=['dob'], inplace=True)

    # Create categorial column for age group
    df['age_group'] = df['age'].apply(lambda x: bin_age(x))
    
    # Create categorical column for bail amount bins
    df['bail_set_bin'] = df['bail_amount'].apply(lambda x: bin_bailSet(x))

    # Create boolean column indicating if bail has been posted
    df['is_bail_posted'] = df['bail_paid'].apply(lambda x: 0 if x == 0 else 1) 
        
    # =========================================================================
    # Print short report
    # =========================================================================
    if verbose:
        print(f"Imported {df.shape[0]} rows with {df.shape[1]} columns:")
        print("\n\t".join(sorted(df.columns.tolist())))
    
    df.to_csv(outPath)
    print("> Saved new file")
    
    return df


def convert_dates_to_datetime(df):
    """Convert strings containing dates to datetime objects"""
    df["offense_date"] = pd.to_datetime(df["offense_date"])
    df["arrest_dt"] = pd.to_datetime(df["arrest_dt"])
    df["dob"] = pd.to_datetime(df["dob"])
    df["bail_date"] = pd.to_datetime(df["bail_date"])
    df["prelim_hearing_dt"] = df["prelim_hearing_dt"].apply(
        lambda x: str(x).split(' ')[0] if pd.notnull(x) else x) # TODO: This was here because of a parsing issue - is it still necessary?
    df["prelim_hearing_dt"] = pd.to_datetime(df["prelim_hearing_dt"])
    df["prelim_hearing_time"] = pd.to_datetime(df["prelim_hearing_time"])

    return df


def convert_lists(df):
    """Convert string representations of lists to lists"""
    df["offenses"] = df["offenses"].apply(lambda x: ast.literal_eval(x))
    df['offense_type'] = df['offense_type'].apply(lambda x: ast.literal_eval(x))
    df['statute'] = df['statute'].apply(lambda x: ast.literal_eval(x))
    
    return df


def trim_data_for_app(df, outPath='app_data.csv', overwrite=False):
    """Create minimum necessary dataset for app deployment.
    Used to generate interactive figures"""
    # Try to load existing file, if desired
    if not overwrite:
        if os.path.isfile(outPath):
            print("> Loaded existing file")
            return

    columns = ['attorney_type', 'bail_date', 'bail_type', 'bail_amount',
               'bail_set_bin', 'bail_paid', 'zip']
    df_app = df[columns]
    df_app.to_csv(outPath)
    print("> Saved new file")


def get_bail_bin_labels():
    """Define labels for bail amount set bins.
    TODO: auto-generate bail_bin_labels to not have to manually update """
    bail_bin_labels = ['None', '<1k', '1k to 5k', '5k to 10k', '10k to 25k', '25k to 50k', '50k to 100k', '100k to 500k', '>=500k']
    return bail_bin_labels


def get_age_bin_labels():
    """Define labels for bail amount set bins.
    TODO: auto-generate bail_bin_labels to not have to manually update """
    age_bin_labels = ['minor', '18 to 25', '26 to 64', '65+']
    return age_bin_labels

# =============================================================================
# Helper functions
# =============================================================================
def bin_bailSet(bailSet):
    """Define bins for bail amount set.
    These are somewhat arbitrary, though roughly in order-of-magnitude increments"""
    if bailSet <= 1 or pd.isnull(bailSet):
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


def bin_age(age):
    """Define bins for age group"""
    if age < 18:
        return 'minor'
    elif age < 26:
        return '18 to 25'
    elif age < 66:
        return '26 to 64'
    else:
        return '65+'

# =============================================================================
# Main
# =============================================================================
if __name__=="__main__":
    cwd = os.path.dirname(os.path.abspath(__file__))
    root = os.path.split(cwd)[0]
    rawdir = os.path.join(root, "data/raw")
    
    fdocket = os.path.join(rawdir, "docket_test.csv")
    fcourt = os.path.join(rawdir, "court_summary_test.csv")
    
    merge_and_clean_data(fdocket, fcourt, verbose=True)