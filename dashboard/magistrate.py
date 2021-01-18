import streamlit as st
from PIL import Image

def app():

    st.title('Breakdown by Magistrate')
    st.write('This section provides a summary of how bail type and bail amount depend on the person setting the bail (hereby referred to as magistrate).')

    ### 2020 Summary plots

    # Explain selection of magistrates (Those who handled more than 500 cases)
    # Some timeline (Many were involved consistently throughout the year. Some were seasonal)
    # Explain 'Others': Those who set fewer than 500 cases. Total number of those labeled as "Others"

    # number of cases
    st.header("1. Year-End Summary by Magistrate")
    st.subheader("Number of cases handled by each magistrate")

    _, col, _ = st.beta_columns([1,2,1])
    image = Image.open('figures/magistrate_case_count.png')
    col.image(image)
    st.write("In the year 2020, bail was set by 673 different people. We provide a summary of the bail type and bail amount for cases handled by the nine magistrates who handled more than 300 cases in year 2020.")

    # bail type
    st.subheader("Percentage of bail type for each magistrate")
    image = Image.open('figures/magistrate_type_summary.png')
    st.image(image, use_column_width=True)

    image = Image.open('figures/magistrate_type_summary_bar.png')
    st.image(image)
    st.write("The above pie chart shows the percentage of bail types set by each magistrate. \
            While there isn't a huge variability across magistrates, we can see that E-filing judges set fewer monetary bail than other magistrates.")


    # bail amount
    st.subheader("Monetary bail amount set by each magistrate")
    image = Image.open('figures/magistrate_amount_summary.png')
    _, col, _ = st.beta_columns([1, 5, 1])
    col.image(image, use_column_width = True)
    st.write("The above box plot compares the monetary bail amount set by different magistrates. \
            For each magistrate, the vertical line in the colored box represents the median bail amount set by that magistrate. \
            The colored boxes represent the 25% to 75% range of the bail amount set by the magistrate. The dots represent outliers.")
    st.write("On average (median), the bail amount set by Connor, Bernard, and Rigmaiden-DeLeon ($50k) is higher than bail amount set by others ($25k). \
            Moreover, Connor and Bernard seem to have set a wider range of bail amounts than other magistrates. ")
    

    ### Comparison controling for offense types 
    st.header("2. Analysis while controlling for offense types")
    st.write("While the above figures provide a useful year-end summary, they do not provide a fair comparison of the magistrates. \
            In particular, the differences among magistrates may stem from the fact that some magistrates may have handled more cases with more severe charges.")
            
    st.write("We compared the bail type and bail amount set by the magistrates while controlling for the difference in the charges. \
            We selected size magistrates (Bernard, Rainey, Rigmaiden-DeLeon, Stack, E-Filing Judge, and O'Brien) that handled more than 1000 cases in year 2020. \
            We then conducted a matched study where we sampled cases with the same charges that were handled by the six magistrates.")
            
    st.write("The following results were obtained from the 3186 cases (531 per magistrate) that were sampled. Ideally, there shouldn't be any noticable difference across magistrates.")
    st.write("Note that due to the sampling nature of the matched study, the matched dataset will vary across samples. However, the general trends observed below were consistent across multiple samples.")
    # bail type
    st.subheader("Percentage of bail type for each magistrate")
    image = Image.open('figures/magistrate_matched_type.png')
    st.image(image, use_column_width=True)
    st.write("When we control for the offense types, all magistrates set monetary bail to 27%-37% of their cases.")

    # bail amount
    st.subheader("Monetary bail amount set by each magistrate")
    _, col, _ = st.beta_columns([1, 5, 1])
    image = Image.open('figures/magistrate_matched_amount.png')
    col.image(image, use_column_width = True)
    st.write("Even when we control for offense types, we see a difference in the monetary bail amount across magistrates.\
            While the median bail amount are similar, comparing the colored boxes (which indicates the 25% - 75% range of bail amounts) show that Bernard, Rainey, and Rigmaiden-DeLeon tend to set higher bail amounts than Stack, E-filing Judge, and O'Brien.")
           