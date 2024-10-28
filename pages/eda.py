import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit_shadcn_ui as ui
from local_components import card_container
from streamlit_shadcn_ui import slider, input, textarea, radio_group, switch

# Set page config
#st.set_page_config(page_title="Data Exploration", page_icon="🔎", layout="wide")

# Custom CSS for background

page_bg_img = """
        <style>
        [data-testid="stAppViewContainer"]{
        background-color: #fdfdfd;
        opacity: 0.8;
        background: linear-gradient(135deg, #f0f1ff55 25%, transparent 25%) -10px 0/ 20px 20px, linear-gradient(225deg, #f0f1ff 25%, transparent 25%) -10px 0/ 20px 20px, linear-gradient(315deg, #f0f1ff55 25%, transparent 25%) 0px 0/ 20px 20px, linear-gradient(45deg, #f0f1ff 25%, #fdfdfd 25%) 0px 0/ 20px 20px;
        </style>
        """
#st.markdown(page_bg_img, unsafe_allow_html=True)

# Sidebar titles
st.sidebar.title(":material/bar_chart: Data Exploration")
st.sidebar.subheader("1. Plots per Country")
st.sidebar.subheader("1.1. Plots per Political Parties Share")
st.sidebar.subheader("1.2. Plots per Candidates Political Party Share")
st.sidebar.subheader("2. Exploratory Plots")

st.title('**:material/bar_chart: Data Exploration**')

# Load dataset
data = pd.read_csv('data/datasetEDA.csv')

#st.subheader("**1. Political Parties and Their Characteristics**")
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
#st.table(charac_parties_df)

# Define political parties for different countries 
political_parties = {
    'Spain': ("PP", "PSOE", "VOX", "Sumar"),
    'Italy': ("FdI", "PD", "M5E", "Lega"),
    'Portugal': ("PSP", "PSD", "CH", "IL"),
    'Greece': ("ND", "SYRIZA", "PASOK", "KKE"),
}
country_code = {
    'Spain': "ES",
    'Italy': "IT",
    'Portugal': "PT",
    'Greece': "GR",
}

days_left_input = 1

# Functions to display bar plots per country
def calculate_means(country_name,country_prefix, is_candidate):
    """Calculate means for the given country prefix."""
    cand_data_prefix = ""
    if is_candidate:
        cand_data_prefix = "Cand"
    means = {
        f'{cand_data_prefix}WebShare': tuple(round(data[data["DaysLeft"] >= days_left_input][f'({country_prefix}) {party} {cand_data_prefix}WebShare'].mean(), 1) for party in political_parties[country_name]),
        f'{cand_data_prefix}NewsShare': tuple(round(data[data["DaysLeft"] >= days_left_input][f'({country_prefix}) {party} {cand_data_prefix}NewsShare'].mean(), 1) for party in political_parties[country_name]),
        f'{cand_data_prefix}YoutubeShare': tuple(round(data[data["DaysLeft"] >= days_left_input][f'({country_prefix}) {party} {cand_data_prefix}YoutubeShare'].mean(), 1) for party in political_parties[country_name]),
        f'{cand_data_prefix}WikipediaShare': tuple(round(data[data["DaysLeft"] >= days_left_input][f'({country_prefix}) {party} {cand_data_prefix}WikipediaShare'].mean(), 1) for party in political_parties[country_name]),
        f'Polls': tuple(round(data[data["DaysLeft"] >= days_left_input][f'({country_prefix}) {party} Polls'].mean(), 1) for party in political_parties[country_name]),
    }
    return means

def plot_data(means, party_names, country_name, is_candidate):
    """Plot the means for the given political parties."""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Plotting
        x = np.arange(len(party_names))
        width = 0.12
        multiplier = 0
        colors = ['#FFB6C1', '#90EE90', '#FFA07A', '#FFD700', '#ADD8E6']

        fig, ax = plt.subplots()

        for attribute, measurement, color in zip(means.keys(), means.values(), colors):
            offset = width * multiplier
            rects = ax.bar(x + offset, measurement, width, label=attribute, color=color)
            multiplier += 1

            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', rotation=90)

        cand = ""
        if is_candidate:
            cand = "Candidate "
        ax.set_ylabel("Share (%)")
        ax.set_title(f"Mean Attributes per {cand}Party ({country_name})")
        ax.set_xticks(x + width * (len(means) - 1) / 2, party_names)
        ax.legend(loc='upper left', bbox_to_anchor=(0.05, 0.95))
        ax.set_ylim(0, 100)

        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)  # Display the plot in Streamlit

    with col2:
        # Cards on the right
        if country_name == "Spain":
            if not is_candidate:
                mean_google_data_right = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) PP WebShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) VOX WebShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) PP NewsShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) VOX NewsShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) PP YoutubeShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) VOX YoutubeShare'].mean(), 1)
                ) / 3, 2)

                mean_wiki_data_young = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) Sumar WikipediaShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) VOX WikipediaShare'].mean(), 1)
                ), 2)

                mean_polls_data_old = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) PP Polls'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) PSOE Polls'].mean(), 1)
                ), 2)

                ui.card(title="Google Data", content=f"{mean_google_data_right}%", description="Mean for right-wing parties (PP + VOX)", key="card1").render()
                ui.card(title="Wikipedia Data", content=f"{mean_wiki_data_young}%", description="Mean for young parties (Sumar + VOX)", key="card2").render()
                ui.card(title="Polls", content=f"{mean_polls_data_old}%", description="Mean for established parties (PP + PSOE)", key="card3").render()
            else:
                mean_google_data_old = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) PP CandWebShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) PSOE CandWebShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) PP CandNewsShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) PSOE CandNewsShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) PP CandYoutubeShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) PSOE CandYoutubeShare'].mean(), 1)
                ) / 3, 2)

                mean_wiki_data_young = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) Sumar CandWikipediaShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) VOX CandWikipediaShare'].mean(), 1)
                ), 2)

                mean_polls_data_old = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) PP Polls'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(ES) PSOE Polls'].mean(), 1)
                ), 2)

                ui.card(title="Google Data", content=f"{mean_google_data_old}%", description="Mean for established parties candidates (PP + PSOE)", key="card4").render()
                ui.card(title="Wikipedia Data", content=f"{mean_wiki_data_young}%", description="Mean for young parties (Sumar + VOX)", key="card5").render()
                ui.card(title="Polls", content=f"{mean_polls_data_old}%", description="Mean for established parties (PP + PSOE)", key="card6").render()
             
        elif country_name == "Italy":
            if not is_candidate:
                mean_google_data_not_right = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) PD WebShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) M5E WebShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) PD NewsShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) M5E NewsShare'].mean(), 1)
                ) / 2, 2)

                mean_yt_data_young = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) FdI YoutubeShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) M5E YoutubeShare'].mean(), 1)
                ), 2)

                mean_wiki_data_not_right = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) PD WikipediaShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) M5E WikipediaShare'].mean(), 1)
                ), 2)

                ui.card(title="WebShare + NewsShare", content=f"{mean_google_data_not_right}%", description="Mean for non right-wing parties (PD + M5E)", key="card1").render()
                ui.card(title="YoutubeShare", content=f"{mean_yt_data_young}%", description="Mean for young parties (FdI + M5E)", key="card2").render()
                ui.card(title="Wikipedia Data", content=f"{mean_wiki_data_not_right}%", description="Mean for non right-wing parties (PD + M5E)", key="card3").render()
            else:
                mean_google_data_young = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) FdI CandWebShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) M5E CandWebShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) FdI CandNewsShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) M5E CandNewsShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) FdI CandYoutubeShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) M5E CandYoutubeShare'].mean(), 1)
                ) / 3, 2)

                mean_wiki_data_young = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) FdI CandWikipediaShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(IT) M5E CandWikipediaShare'].mean(), 1)
                ), 2)

                ui.card(title="Google Data", content=f"{mean_google_data_young}%", description="Mean for young parties candidates (FdI + M5E)", key="card4").render()
                ui.card(title="Wikipedia Data", content=f"{mean_wiki_data_young}%", description="Mean for young parties candidates (FdI + M5E)", key="card5").render()
                
        elif country_name == "Portugal":
            if not is_candidate:
                mean_google_data_new_right = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) PSD WebShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) CH WebShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) IL WebShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) PSD YoutubeShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) CH YoutubeShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) IL YoutubeShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) PSD NewsShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) CH NewsShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) IL NewsShare'].mean(), 1)
                ) / 3, 2)

                mean_wiki_data_not_right = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) PSD WikipediaShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) CH WikipediaShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) IL WikipediaShare'].mean(), 1)
                ), 2)

                mean_polls_data_old = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) PSD Polls'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) PSP Polls'].mean(), 1)
                ), 2)

                ui.card(title="Google Data", content=f"{mean_google_data_new_right}%", description="Mean for new right-wing parties (PSD + CH + IL)", key="card1").render()
                ui.card(title="Wikipedia Data", content=f"{mean_wiki_data_not_right}%", description="Mean for right-wing parties (PSD + CH + IL)", key="card2").render()
                ui.card(title="Polls", content=f"{mean_polls_data_old}%", description="Mean for established parties (PSD + PSP)", key="card3").render()
            else:
                mean_google_data_old = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) PSP CandWebShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) PSD CandWebShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) PSP CandYoutubeShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) PSD CandYoutubeShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) PSP CandNewsShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) PSD CandNewsShare'].mean(), 1)
                ) / 3, 2)

                mean_wiki_data_young = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) CH CandWikipediaShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(PT) IL CandWikipediaShare'].mean(), 1)
                ), 2)

                ui.card(title="Google Data", content=f"{mean_google_data_old}%", description="Mean for established parties (PSP + PSD)", key="card4").render()
                ui.card(title="Wikipedia Data", content=f"{mean_wiki_data_young}%", description="Mean for new right-wing parties (CH + IL)", key="card5").render()
                
        elif country_name == "Greece":
            if not is_candidate:
                mean_news_data_left = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(GR) SYRIZA NewsShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(GR) PASOK NewsShare'].mean(), 1)
                ), 2)

                mean_wiki_data_old = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(GR) ND WikipediaShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(GR) KKE WikipediaShare'].mean(), 1)
                ), 2)


                ui.card(title="NewsShare", content=f"{mean_news_data_left}%", description="Mean for left-wing parties (SYRIZA + PASOK)", key="card1").render()
                ui.card(title="YoutubeShare", content=f"{mean_wiki_data_old}%", description="Mean for established parties (ND + KKE)", key="card2").render()
            else:
                mean_google_data_old = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(GR) ND CandNewsShare'].mean(), 1) + 
                    round(data[data["DaysLeft"] >= days_left_input]['(GR) ND CandYoutubeShare'].mean(), 1) +
                    round(data[data["DaysLeft"] >= days_left_input]['(GR) ND CandWebShare'].mean(), 1) 
                ) / 3, 2)

                mean_wiki_data_old = round((
                    round(data[data["DaysLeft"] >= days_left_input]['(GR) ND CandWikipediaShare'].mean(), 1)
                ), 2)


                ui.card(title="Google Data", content=f"{mean_google_data_old}%", description="Mean for the most established party candidate (ND)", key="card4").render()
                ui.card(title="Wikipedia Data", content=f"{mean_wiki_data_old}%", description="Mean for the most established party candidate (ND)", key="card5").render()

st.subheader("**1. Plots per Country**")
st.subheader("1.1. Plots per Political Parties Share")
# Tabs for Spain, Italy, Portugal, Greece
selected_country_parties = ui.tabs(options=['Spain', 'Italy', 'Portugal', 'Greece'], default_value='Spain', key="country_tabs_parties")
# Process each selected country
if selected_country_parties in political_parties:
    means = calculate_means(selected_country_parties,country_code[selected_country_parties], False) 
    plot_data(means, political_parties[selected_country_parties], selected_country_parties, False)


st.markdown("""
**Globally**, we can say that all the **political parties** we have ideologically defined as
<span style="color: blue;">**far-right**</span> are also parties we declare as <span style="color: blue;">**new**</span>. That is, we can see that in **Southern Europe**, 
the representation of <span style="color: blue;">**far-right** parties</span> has significantly <span style="color: violet;">**increased**</span> in the parliaments of **Spain**,
**Italy**, **Portugal**, and **Greece**, and at the same time, these parties were **created** in the last **fifteen years**.
            
Each country has <span style="color: violet;">**different search trends**</span> for **political parties**, although some countries share
**common** trends. However, there is **no general trend** among the four selected **European** countries.   
""", unsafe_allow_html=True)

st.subheader("1.2. Plots per Candidates Political Party Share")

selected_country_cands = ui.tabs(options=['Spain', 'Italy', 'Portugal', 'Greece'], default_value='Spain', key="country_tabs_cands")

if selected_country_cands in political_parties:
    means = calculate_means(selected_country_cands,country_code[selected_country_cands], True) 
    plot_data(means, political_parties[selected_country_cands], selected_country_cands, True)

st.markdown("""
**Globally**, we can say that in countries where there is a **parliamentary presence** of 
<span style="color: blue;">**far-right parties**</span>, the **candidates** of these parties are those with the most 
<span style="color: violet;">**searches on Google**</span> and <span style="color: violet;">**Wikipedia**</span>, especially in **Italy** and **Portugal**.
  
Additionally, we can observe a certain similarity between the data from **Spain** and **Greece**, 
where **established parties** have political leaders with a greater **online search presence**, 
and a different trend in **Italy** and **Portugal**, where the political leaders of far-right parties 
tend to have a greater **Internet presence**.
""", unsafe_allow_html=True)


st.subheader("**2. Exploratory Plots**")

st.write("""
    This section contains various filters to explore the election data based on party names, features, and other aspects. 
    Please use the filters on the right to customize the view and analyze the data effectively.
    """)
# Functions to the personalized bar plots
def party2country_prefix(party_name): #political_parties, country_code
    party_country_prefix = ''
    countries = ['Spain', 'Italy', 'Portugal', 'Greece']
    for country in countries:
        if party_name in political_parties[country]:
            party_country_prefix = country_code[country]
    return party_country_prefix

def extract_parties(countries_selected, ideologies_selected, party_ages_selected, party_gov_selected):
    # Extract the parties
    parties_selected = []

    # Multiple: countries_selected, ideologies_selected || Binary: party_ages_selected, party_gov_selected
    party_ages_dict = {'New' : 1, 'Established' : 0}
    party_gov_dict = {'In Government' : 1, 'Opposition' : 0}

    int_party_ages_selected = []
    for party_age in party_ages_selected:
        int_party_ages_selected.append(party_ages_dict[party_age])

    int_party_govs_selected = []
    for party_gov in party_gov_selected:
        int_party_govs_selected.append(party_gov_dict[party_gov])
    
    filtered_parties_df = charac_parties_df[
        (charac_parties_df['Country'].isin(countries_selected) if countries_selected else True) &
        (charac_parties_df['Ideology'].isin(ideologies_selected) if ideologies_selected else True) &
        (charac_parties_df['New Party'].isin(int_party_ages_selected) if int_party_ages_selected else True) &
        (charac_parties_df['Party Government'].isin(int_party_govs_selected) if int_party_govs_selected else True)
    ]


    parties_selected = filtered_parties_df['Party Name'].tolist()

    return parties_selected

def calculate_means_exp(days_left_selected, parties_selected, data_selected):
    """Calculate means for the given country prefix."""
    means = {}
    for search_data in data_selected:
        means[search_data] = tuple(round(data[data["DaysLeft"] >= days_left_selected][f'({party2country_prefix(party)}) {party} {search_data}'].mean(), 1) for party in parties_selected)
    
    return means 

def bar_plot_selected(party_names, means):
    # Plotting
        x = np.arange(len(party_names))
        width = min(0.8 / len(means.keys()), 0.12) #0.12, 0.03
        multiplier = 0
        colors = ['#FFB6C1', '#90EE90', '#FFA07A', '#FFD700', '#ADD8E6', '#FFDAB9', '#DDA0DD', '#AFEEEE', '#D2B48C']
        colors = colors[0:(len(means.keys()))]
        fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the size of the plot
        
        # Define dynamic font size for annotations based on the width of bars
        annotation_font_size = max(8 * width / 0.12, 3)  # Scale font size with width, with a minimum of 3
        for attribute, measurement, color in zip(means.keys(), means.values(), colors):
            offset = width * multiplier
            rects = ax.bar(x + offset, measurement, width, label=attribute, color=color)
            multiplier += 1

            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', rotation=90, fontsize=annotation_font_size)


        ax.set_ylabel("Share (%)")
        ax.set_title(f"Mean Attributes per Party & Candidates")
        ax.set_xticks(x + width * (len(means) - 1) / 2, party_names)
        ax.legend(loc='upper left', bbox_to_anchor=(0.05, 0.95), fontsize=8)
        ax.set_ylim(0, 100)

        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)  # Display the plot in Streamlit

# Filter vars
    # Time
days_left = 1
    # Parties
tab_parties_names_or_features = 'Names'
        #Names
party_names_es = ["PP","PSOE","VOX","Sumar"] #static
party_names_selection_es = [] 
party_names_it = ["FdI", "PD", "M5E", "Lega"] #static
party_names_selection_it = [] 
party_names_pt = ["PSP","PSD","CH","IL"] #static
party_names_selection_pt = [] 
party_names_gr = ["ND", "SYRIZA","PASOK", "KKE"] #static
party_names_selection_gr = [] 
        #Features
countries = []
ideologies = []
party_ages = []
party_gov = []
    # Data
news_data = True
web_data = True
yt_data = True
cand_news_data = False
cand_web_data = False
cand_yt_data = False
wiki_data = True
cand_wiki_data = False
polls_data = True
    # List of parties to be selected in order
parties_selected = []
means_to_display = {}

# Section: Time
with st.expander(":material/timer: Time", expanded=True): #:material/hourglass_top:
    st.markdown("Select Time Range")
    days_left = st.slider("Days Left for Election Date", 1, 14, 1)#slider(default_value=[1], min_value=1, max_value=14, step=1, label="Days Left for Election Date", key="slider1")

# Column layout: left for text, right for filters
col1, col2, col3 = st.columns([3, 1, 1])

# Filters Column (col2): to save changes
with col2:
    
    # Section: Parties
    with st.expander(":material/business_center: Parties", expanded=True): 
        # Custom tabs-like behavior using radio buttons
        tab_parties_names_or_features = ui.tabs(options=['Names', 'Features'], default_value='Names', key="features_tabs_parties")

        if tab_parties_names_or_features == 'Names':
            st.markdown("Filter by **Party Names**")
            party_names_selection_es = st.multiselect("Spanish Parties", party_names_es)
            party_names_selection_it = st.multiselect("Italian Parties", party_names_it)
            party_names_selection_pt = st.multiselect("Portuguese Parties", party_names_pt)
            party_names_selection_gr = st.multiselect("Greek Parties", party_names_gr)

        elif tab_parties_names_or_features == 'Features':
            st.markdown("Filter by **Party Features**")
            countries = st.multiselect("Country", ["Spain", "Italy", "Portugal", "Greece"], default=["Spain", "Italy", "Portugal", "Greece"])
            ideologies = st.multiselect("Ideology", ["Far-Left","Left", "Center-Left","Center-Right","Right", "Far-Right"])
            party_ages = st.multiselect("Party Age", ["New", "Established"])
            party_gov = st.multiselect("Party Government", ["In Government", "Opposition"])
with col3:
    # Section: Data
    with st.expander(":material/database: Data", expanded=True): 
        #💼👤
        st.markdown("**Parties Data**")
        news_data = st.checkbox("NewsShare")
        web_data = st.checkbox("WebShare")
        yt_data = st.checkbox("YoutubeShare")
        wiki_data = st.checkbox("WikipediaShare")
        polls_data = st.checkbox("Polls")
        st.markdown("**Candidates Data**")
        cand_news_data = st.checkbox("CandNewsShare")
        cand_web_data = st.checkbox("CandWebShare")
        cand_yt_data = st.checkbox("CandYoutubeShare")
        cand_wiki_data = st.checkbox("CandWikipediaShare")
        
    
    # Filter the selected parties
    if tab_parties_names_or_features == 'Names':
        # If the user selects the political parties to be displayed then when merge them
        parties_selected = party_names_selection_es + party_names_selection_it + party_names_selection_pt + party_names_selection_gr
    elif tab_parties_names_or_features == 'Features':
        # Else, we extract the parties from the features selected by the user
        parties_selected = extract_parties(countries, ideologies, party_ages, party_gov)

    data_selected = []
    if news_data: data_selected.append("NewsShare")
    if web_data: data_selected.append("WebShare")
    if yt_data: data_selected.append("YoutubeShare")
    if wiki_data: data_selected.append("WikipediaShare")
    if polls_data: data_selected.append("Polls")
    if cand_news_data: data_selected.append("CandNewsShare")
    if cand_web_data: data_selected.append("CandWebShare")
    if cand_yt_data: data_selected.append("CandYoutubeShare")
    if cand_wiki_data: data_selected.append("CandWikipediaShare")

    # Check that user have selected parties and data
    if (parties_selected != [] and data_selected != []):
        means_to_display = calculate_means_exp(days_left, parties_selected, data_selected)
    

# Text Column (col1)
with col1:
    st.markdown("""
    <style>
    .section-text {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check that user have selected parties and data
    if (parties_selected != [] and data_selected != []):
        bar_plot_selected(parties_selected, means_to_display)



# Styling components (modern look-and-feel inspired by shadcn)
st.markdown("""
    <style>
    .st-expander {
        background-color: #f0f0f0 !important;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 16px;
        margin-top: 10px;
    }
    .st-checkbox, .st-slider {
        margin: 0 !important;
    }
    .st-markdown {
        margin-top: -10px;
    }
    .st-radio {
        padding-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

