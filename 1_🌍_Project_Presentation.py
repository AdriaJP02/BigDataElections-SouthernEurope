import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Exploring the Potential of Big Data in Southern Europe Elections", page_icon="🌍",layout="wide")

# Custom CSS for background
page_bg_img = """
        <style>
        [data-testid="stAppViewContainer"]{
        background-color: #DFF4FE;
        opacity: 0.8;
        background-image: radial-gradient(#9ec2f4 0.5px, #DFF4FE 0.5px);
        background-size: 10px 10px;
        </style>
        """
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title with emoji
st.title("**🌍 Exploring the Potential of Big Data in Southern Europe Elections**")

# Subtitles
st.subheader("1. Introduction")
st.write("👋 Hi, I am Adrià Julià Parada, and this application explores the use of Big Data in predicting election outcomes in Southern Europe, based on my Final Degree Project called 'Exploring the Potential of Big Data in Southern Europe Elections'.")

st.subheader("2. Abstract")
st.write(
    """This Final Engineering Project studies the correlation between electoral polls and Big Data, extracting
    search data on political parties and their candidates through Google and Wikipedia during the electoral
    period in Southern European countries. We analyse data from the last elections of the four most
    populated countries in Southern Europe: Spain, Italy, Portugal, and Greece, taking as a reference the
    parliamentary elections held until 31 December 2023.
    We studied four countries and using linear regression, we found that it is not possible to predict
    surveys using Big Data alone with a Mean Absolute Error (MAE) of 7.17%, but that this data can help
    to slightly improve survey prediction.
    Big Data cannot replace polls as a method of predicting elections using linear regressions. It is true
    that it can complement polls to obtain slightly more accurate results, but even so, the improvement is
    not significant, and these results are insufficient."""
)


st.subheader("3. Study Cases & Hypotheses")
st.markdown("**3.1. Study Cases**")
st.markdown("""The elections chosen for analysis as case studies are the Spanish general elections of July 23, 2023 [22], 
         the Italian general elections of September 25, 2022 [20], the Portuguese parliamentary elections of January 30, 2022 [19], 
         and the Greek parliamentary elections of June 25, 2023 [21].
        These are the most recent parliamentary elections of the four most populous countries in the geographical region of Southern Europe [17, 18]. 
        We selected these countries due to the sociocultural similarities they share. A map of the countries 
        considered part of Southern Europe can be seen in Figure 1, and a map of the selected Southern European countries is shown in Figure 2.""")
st.markdown("**3.2. Hypotheses**")
st.markdown("""In this work, we address the following questions:

· Can we build a linear regression model using only quantitative Big Data that can improve electoral predictions provided by polls?
· Can Big Data be a complementary tool to polls for improving election predictions?""")

st.subheader("4. Links related to the project")
# Add links to presentation and project (replace with actual links)
st.write("[Link to Project](https://drive.google.com/file/d/1NhZGCeLwrRjRHC9232X3eOXJkulYNle7/view)")
st.write("[Link to Presentation](https://drive.google.com/file/d/1RScwfwsXHCiJv36pm8yDphdSBCz1rPl_/view?usp=sharing)")
st.subheader("5. Contact Me")
st.write("For any questions or feedback, feel free to reach out via:")
st.write("    - [LinkedIn](http://www.linkedin.com/in/adri%C3%A0-juli%C3%A0-parada-67b275271).")
st.write("    - [GitHub](https://github.com/AdriaJP02).")
st.write("    - Gmail: adriajuliaparada2@gmail.com")


# Uncomment the navigation code if you want to add it later
# page = st.sidebar.selectbox('Select Page', ['Exploratory Data Analysis', 'Prediction'])
# if page == 'Exploratory Data Analysis':
#     eda.run()
# else:
#     prediction.run()
