import streamlit as st
import pandas as pd

# Set page config
#st.set_page_config(page_title="Parties Selection", page_icon="🏛️",layout="wide")
# Sidebar titles
st.sidebar.title(":material/account_balance: Parties Selection")
st.sidebar.subheader("1. Study Cases")
st.sidebar.subheader("2. Political Parties and Their Characteristics")
# 📋 🏛️ 📝
st.title(":material/account_balance: Parties Selection")
st.subheader("1. Study Cases")
st.markdown("""The elections chosen for analysis as case studies are the Spanish general elections of July 23, 2023 [22], 
         the Italian general elections of September 25, 2022 [20], the Portuguese parliamentary elections of January 30, 2022 [19], 
         and the Greek parliamentary elections of June 25, 2023 [21].
        These are the most recent parliamentary elections of the four most populous countries in the geographical region of Southern Europe [17, 18]. 
        We selected these countries due to the sociocultural similarities they share. A map of the countries 
        considered part of Southern Europe can be seen in Figure 1, and a map of the selected Southern European countries is shown in Figure 2.""")

st.subheader("2. Political Parties and Their Characteristics")
charac_parties_df = pd.DataFrame({
    'Party Name': ["PP","PSOE","VOX","Sumar","PSP","PSD","CH","IL","FdI", "PD", "M5E", "Lega", "ND", "SYRIZA","PASOK", "KKE"],
    'Country': ["Spain","Spain","Spain","Spain","Portugal","Portugal","Portugal","Portugal","Italy", "Italy", "Italy", "Italy","Greece", "Greece", "Greece", "Greece"],
    'Ideology': ["Right", "Center-Left", "Far-Right", "Left", "Center-Left", "Right", "Far-Right", "Center-Right", "Far-Right", "Center-Left", "Center-Left", "Far-Right", "Right", "Left", "Center-Left", "Far-Left"],
    'Left-wing Ideology': [0, 1, 0, 2, 1, 0, 0, 0, 0, 1, 1, 0, 0, 2, 1, 3], # 1.0 -> Center-left, 2.0 -> Left-wing, 3.0 -> Far left-wing
    'Right-wing Ideology': [2, 0, 3, 0, 0, 2, 3, 1, 3, 0, 1, 3, 2, 0, 0, 0], # 1.0 -> Center-right, 2.0 -> Right-wing, 3.0 -> Far right-wing
    'New Party': [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0],
    'Established Party': [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
    'Party Government': [0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
    'Results': ["33.06%", "31.68%", "12.38%", "12.33%", "41.37%", "29.09%", "7.18%", "4.91%", "26.00%", "19.07%", "15.43%", "8.77%", "40.56%", "17.83%", "11.84%", "7.69%"]
})
st.table(charac_parties_df)