import streamlit as st
import pickle, os, re, joblib
import pandas as pd
import streamlit_shadcn_ui as ui
from streamlit_shadcn_ui import slider, input, textarea, radio_group, switch
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
# Set page config
#st.set_page_config(page_title="Prediction Models", page_icon="🔮", layout="wide")

# Sidebar titles
st.sidebar.title(":material/pattern: Prediction Models")
st.sidebar.subheader("1. Models to Predict Election Results")
st.sidebar.subheader("1.1. Political Parties Predictions")
st.sidebar.subheader("1.2. Predict via Features")
st.sidebar.subheader("2. Build your own model")

charac_parties_df = pd.DataFrame({
    'Party Name': ["PP","PSOE","VOX","Sumar","PSP","PSD","CH","IL","FdI", "PD", "M5E", "Lega", "ND", "SYRIZA","PASOK", "KKE"],
    'Country': ["Spain","Spain","Spain","Spain","Portugal","Portugal","Portugal","Portugal","Italy", "Italy", "Italy", "Italy","Greece", "Greece", "Greece", "Greece"],
    'Ideology': ["Right", "Center-Left", "Far-Right", "Left", "Center-Left", "Right", "Far-Right", "Center-Right", "Far-Right", "Center-Left", "Center-Left", "Far-Right", "Right", "Left", "Center-Left", "Far-Left"],
    'Left-wing Ideology': [0, 1, 0, 2, 1, 0, 0, 0, 0, 1, 1, 0, 0, 2, 1, 3], # 1.0 -> Center-left, 2.0 -> Left-wing, 3.0 -> Far left-wing
    'Right-wing Ideology': [2, 0, 3, 0, 0, 2, 3, 1, 3, 0, 1, 3, 2, 0, 0, 0], # 1.0 -> Center-right, 2.0 -> Right-wing, 3.0 -> Far right-wing
    'New Party': [0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0],
    'Established Party': [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
    'Party Government': [0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
    'Results': [33.06, 31.68, 12.38, 12.33, 41.37, 29.09, 7.18, 4.91, 26.00, 19.07, 15.43, 8.77, 40.56, 17.83, 11.84, 7.69]
    #Polls 
})

data = pd.read_csv('data/datasetSouthernEuropeElections.csv')

st.title(':material/pattern: Prediction Models')

st.subheader("1. Models to Predict Election Results")
# BEST MODEL: WikipediaShare, CandYoutubeShare & CandNewShare
st.subheader("1.1. Political Parties Comparision Predictions")
# Table to show the differences of predictions
table_comparision = {
    "Party": ["PSOE", "PP", "VOX", "Sumar", "FdI", "M5E", "Lega", "PD", "PSP", "PSD", "CH", "IL", "ND", "SYRIZA", "PASOK", "KKE"],
    "Election Results": ["31.68%", "33.06%", "12.38%", "12.33%", "26.00%", "15.43%", "8.77%", "19.07%", "41.37%", "29.09%", "7.18%", "4.91%", "40.56%", "17.83%", "11.84%", "7.69%"],
    "Prediction using Mean Polls": ["28.23%", "33.24%", "13.00%", "13.37%", "25.01%", "15.17%", "10.16%", "21.46%", "35.87%", "32.66%", "6.49%", "4.81%", "41.99%", "19.54%", "11.86%", "7.27%"],
    "Absolute Error predicting with Mean Polls": ["3.45%", "0.17%", "0.62%", "1.04%", "0.98%", "0.26%", "1.39%", "2.39%", "5.49%", "3.56%", "0.69%", "0.09%", "1.43%", "1.70%", "0.02%", "0.42%"],
    "Prediction using Polls & Big Data": ["31.45%", "31.65%", "11.59%", "12.69%", "25.04%", "17.73%", "11.14%", "19.05%", "38.14%", "30.62%", "5.40%", "4.17%", "42.02%", "20.12%", "11.60%", "4.87%"],
    "Absolute Error predicting with Polls & Big Data": ["0.24%", "1.41%", "0.79%", "0.36%", "0.95%", "2.30%", "2.37%", "0.02%", "3.23%", "1.53%", "1.78%", "0.73%", "1.46%", "2.29%", "0.25%", "2.82%"],
    "Prediction using only Big Data": ["33.05%", "22.92%", "9.34%", "16.38%", "24.34%", "19.89%", "24.79%", "17.15%", "31.99%", "23.39%", "11.17%", "15.12%", "35.7%", "10.38%", "19.69%", "12.17%"],
    "Absolute Error predicting with Big Data": ["1.37%", "10.14%", "3.04%", "4.05%", "1.66%", "4.45%", "16.02%", "1.92%", "9.38%", "5.70%", "3.98%", "10.21%", "4.85%", "7.45%", "7.84%", "4.48%"]
}
# Create a DataFrame
table_comparision_df = pd.DataFrame(table_comparision)
# Function to highlight specific columns
def highlight_columns(col):
    if col.name in ["Absolute Error predicting with Mean Polls"]:
        return ['background-color: #BEE9E1'] * len(col)
    elif col.name in ["Absolute Error predicting with Polls & Big Data"]:
        return ['background-color: #E2D0E9'] * len(col)
    elif col.name in ["Absolute Error predicting with Big Data"]:
        return ['background-color: #EBC6D4'] * len(col)
    elif col.name in ["Election Results"]:
        return ['background-color: #D3D3DF'] * len(col)
    else:
        return [''] * len(col)

# Function to make text bold for specific columns
def bold_columns(col):
    if col.name in ["Party", "Absolute Error predicting with Mean Polls", "Absolute Error predicting with Polls & Big Data", "Absolute Error predicting with Big Data"]:
        return ['font-weight: bold'] * len(col)
    else:
        return [''] * len(col)

# Style the DataFrame with custom table styles
table_comparision_df = table_comparision_df.style.apply(highlight_columns, axis=0) \
                    .apply(bold_columns, axis=0) \
                    .set_table_styles([
                        {'selector': 'thead th', 'props': 'font-weight: bold;'},  # Make header bold
                        {'selector': 'thead th.col0', 'props': 'background-color: #D3D3D3; font-weight: bold;'},  # Style "Party" header
                        {'selector': 'thead th.col1', 'props': 'background-color: #D3D3D3; font-weight: bold;'},   # Style "Election Results" header
                        {'selector': 'thead th.col2', 'props': 'background-color: #73CCD0; font-weight: bold;'},   # Style "Prediction using Mean Polls" header
                        {'selector': 'thead th.col3', 'props': 'background-color: #73CCD0; font-weight: bold;'},   # Style "Absolute Error predicting with Mean Polls" header
                        {'selector': 'thead th.col4', 'props': 'background-color: #C493D6; font-weight: bold;'},   # Style "Prediction using Polls & Big Data" header
                        {'selector': 'thead th.col5', 'props': 'background-color: #C493D6; font-weight: bold;'},   # Style "Absolute Error predicting with Polls & Big Data" header
                        {'selector': 'thead th.col6', 'props': 'background-color: #E47BA3; font-weight: bold;'},   # Style "Prediction using only Big Data" header
                        {'selector': 'thead th.col7', 'props': 'background-color: #E47BA3; font-weight: bold;'}   # Style "Absolute Error predicting with Big Data" header
                    ])

st.table(table_comparision_df)

st.subheader("1.2. Predict via Features")

# Directory where your files are stored
directory = "models"

# Initialize an empty dictionary to store the models
models_dict = {}

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Check if the file starts with 'model_Pred' and ends with '.pkl'
    if filename.startswith("model_Pred") and filename.endswith(".pkl"):
        # Remove the .pkl for display purposes
        filename_no_pkl = filename.replace(".pkl", "")
        
        # Create the full path to the file (without removing .pkl)
        filepath = os.path.join(directory, filename)
        
        # Open and load the pickle file
        with open(filepath, 'rb') as file:
            models_dict[filename_no_pkl] = pickle.load(file)

##### TO_DO: Put them in columns shadcn components
# Creating sliders for each key in user_input_data
wk_share_input = 50
cand_nw_share_input = 50
cand_yt_share_input = 50
party_age_input = 1
party_gov_input = 0
ideology_L_input = 1
ideology_R_input = 0
polls_input = 50
days_left_input = 7

col1, col2, col3 = st.columns([1,1,1])
dict_binary = {"Yes" : 0, "No" : 1}
dict_ideo_left = {"Not Left-wing" : 0, "Center-Left" : 1, "Left" : 2, "Far-Left" : 3}
dict_ideo_right = {"Not Right-wing" : 0, "Center-Right" : 1, "Right" : 2, "Far-Right" : 3}

with col1:
    wk_share_input = st.slider("Wikipedia Share (%)", 0, 100, 50)#slider(default_value=[50], min_value=0, max_value=100, step=1, label="Wikipedia Share (%)", key="slider1")#
    cand_nw_share_input = st.slider("Candidate News Share (%)", 0, 100, 50)#slider(default_value=[50], min_value=0, max_value=100, step=1, label="Candidate News Share (%)", key="slider2")#
    cand_yt_share_input = st.slider("Candidate Youtube Share (%)", 0, 100, 50)#slider(default_value=[50], min_value=0, max_value=100, step=1, label="Candidate Youtube Share (%)", key="slider3")#
with col2:
    party_age_input = st.selectbox("New Party", ["No", "Yes"])#switch(default_checked=False, label="New Party (0: No, 1: Yes)", key="switch1")#
    party_gov_input = st.selectbox("Party in Government", ["No", "Yes"])#switch(default_checked=False, label="Party in Government (0: No, 1: Yes)", key="switch2")#
    ideology_L_input = st.selectbox("Left Ideology", ["Not Left-wing", "Center-Left", "Left", "Far-Left"])#st.slider("Left Ideology (0: Not Left-wing, 1: Center-Left, 2: Left, 3: Far-Left)", 0, 3, 1)#slider(default_value=[1], min_value=0, max_value=3, step=1, label="Left Ideology (0: Not Left-wing, 1: Center-Left, 2: Left, 3: Far-Left)", key="slider4")#
with col3:
    polls_input = st.slider("Polls (%)", 0, 100, 50)#slider(default_value=[50], min_value=0, max_value=100, step=1, label="Polls (%)", key="slider6")#
    days_left_input = st.slider("Days Left for Election", 1, 14, 7)#slider(default_value=[7], min_value=1, max_value=14, step=1, label="Days Left for Election", key="slider7")#
    ideology_R_input = st.selectbox("Right Ideology", ["Not Right-wing", "Center-Right", "Right", "Far-Right"])#st.slider("Right Ideology (0: Not Right-wing, 1: Center-Right, 2: Right, 3: Far-Right)", 0, 3, 0)#slider(default_value=[1], min_value=0, max_value=3, step=1, label="Right Ideology (0: Not Right-wing, 1: Center-Right, 2: Right, 3: Far-Right)", key="slider5")

#Parse data
party_age_input = dict_binary[party_age_input]
party_gov_input = dict_binary[party_gov_input]
ideology_L_input = dict_ideo_left[ideology_L_input]
ideology_R_input = dict_ideo_right[ideology_R_input]

user_input_data = {
    #"WebShare": wb_share_input,
    #"NewsShare": nw_share_input,
    #"YoutubeShare": yt_share_input,
    "WikipediaShare": wk_share_input,
    #"CandWebShare": cand_wb_share_input,
    "CandNewsShare": cand_nw_share_input,
    "CandYoutubeShare": cand_yt_share_input,
    #"CandWikipediaShare": cand_wk_share_input,
    "Polls": polls_input,
    "DaysLeft": days_left_input,
    "PartitNou": party_age_input,
    "PartitAlGovern": party_gov_input,
    "IdeologiaEsq": ideology_L_input,
    "IdeologiaDre": ideology_R_input,

}
#print(models_dict)
pred_button = ui.button(text="Make Prediction", key="pred_button")

if pred_button:
    # Do the prediction for the Big Data & Polls Model
    user_input_data_df = pd.DataFrame([user_input_data])
    result_pred_ESP = models_dict["model_Pred_BigData_Polls_ESP"].predict(user_input_data_df)[0]
    result_pred_ITA = models_dict["model_Pred_BigData_Polls_ITA"].predict(user_input_data_df)[0]
    result_pred_POR = models_dict["model_Pred_BigData_Polls_POR"].predict(user_input_data_df)[0]
    result_pred_GRE = models_dict["model_Pred_BigData_Polls_GRE"].predict(user_input_data_df)[0]
    result_pred = (result_pred_ESP+result_pred_ITA+result_pred_POR+result_pred_GRE)/4
    # Do the prediction for the Big Data Model
    user_input_data_nopolls_df = user_input_data_df.drop(columns=["Polls"])
    result_pred_ESP_ = models_dict["model_Pred_BigData_ESP"].predict(user_input_data_nopolls_df)[0]
    result_pred_ITA_ = models_dict["model_Pred_BigData_ITA"].predict(user_input_data_nopolls_df)[0]
    result_pred_POR_ = models_dict["model_Pred_BigData_POR"].predict(user_input_data_nopolls_df)[0]
    result_pred_GRE_ = models_dict["model_Pred_BigData_GRE"].predict(user_input_data_nopolls_df)[0]
    result_pred_ = (result_pred_ESP_+result_pred_ITA_+result_pred_POR_+result_pred_GRE_)/4

    # Display the prediction result
    col_A, col_B = st.columns([1,1])
    with col_A:
        ui.card(title="Big Data & Polls Model Prediction", content=f"{round(result_pred,2)}%", description="Mean Absolute Error (MAE): 2.57%", key="card1").render()
    with col_B:
        ui.card(title="Big Data Model Prediction", content=f"{round(result_pred_,2)}%", description="Mean Absolute Error (MAE): 10.54%", key="card2").render()
    
    #st.write(f"Model Prediction(ESP): {round(result_pred_ESP,2)}%")
    #st.write(f"Model Prediction(ITA): {round(result_pred_ITA,2)}%")
    #st.write(f"Model Prediction(POR): {round(result_pred_POR,2)}%")
    #st.write(f"Model Prediction(GRE): {round(result_pred_GRE,2)}%")
    pred_button = False


st.subheader("2. Build your own model")

# Read the dataframe with all the data
data = pd.read_csv('data/datasetSouthernEuropeElections.csv')

st.subheader("2.1. Select the features of your model")
st.markdown("Select the Big Data you want to include in your own model and also decide if you want to keep the Polls in the model.")
# Select the features
col1, col2, col3 = st.columns([1,1,1])

wb_share_selected = False
nw_share_selected = False
yt_share_selected = False
wk_share_selected = False
cand_wb_share_selected = False
cand_nw_share_selected = False
cand_yt_share_selected = False
cand_wk_share_selected = False
polls_selected = False

with col1:
    wb_share_selected = st.checkbox("WebShare")
    nw_share_selected = st.checkbox("NewsShare")
    yt_share_selected = st.checkbox("YoutubeShare")
with col2:
    wk_share_selected = st.checkbox("WikipediaShare")
    polls_selected = st.checkbox("Polls")
    cand_wk_share_selected = st.checkbox("CandWikipediaShare")
with col3:
    cand_wb_share_selected = st.checkbox("CandWebShare")
    cand_nw_share_selected = st.checkbox("CandNewsShare")
    cand_yt_share_selected = st.checkbox("CandYoutubeShare")

selected_features = [
    feature_name
    for feature_name, selected in {
        "WebShare": wb_share_selected,
        "NewsShare": nw_share_selected,
        "YoutubeShare": yt_share_selected,
        "WikipediaShare": wk_share_selected,
        "Polls": polls_selected,
        "CandWebShare": cand_wb_share_selected,
        "CandNewsShare": cand_nw_share_selected,
        "CandYoutubeShare": cand_yt_share_selected,
        "CandWikipediaShare": cand_wk_share_selected,
    }.items()
    if selected
]
ordered_features = selected_features + ["DaysLeft", "PartitNou", "PartitAlGovern", "IdeologiaEsq", "IdeologiaDre"]
st.write("Selected features:", selected_features)

# Function to make the model with the selected features
def make_model(countrySplit, featuresList):
    # Lista de los cinco dataframes y sus respectivos nombres de variable
    #["WikipediaShare", "CandNewsShare", "CandYoutubeShare"]
    featuresList = featuresList + ["DaysLeft","PartitNou", "PartitAlGovern", "IdeologiaEsq","IdeologiaDre","PartitESP","PartitPOR", "PartitITA", "PartitGRE", "Resultats"]
    data_filtered = data[featuresList]
    
    train_data = data_filtered[data_filtered[countrySplit] == 0]
    test_data = data_filtered[data_filtered[countrySplit] == 1]

    X_train = train_data.drop(columns=['PartitITA', 'PartitPOR', 'PartitGRE', 'PartitESP', 'Resultats'])
    y_train = train_data['Resultats']
    X_test = test_data.drop(columns=['PartitITA', 'PartitPOR', 'PartitGRE', 'PartitESP', 'Resultats'])
    y_test = test_data['Resultats']

    # Inicializar y entrenar el modelo de regresión lineal
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Hacer predicciones en el conjunto de prueba
    y_pred = model.predict(X_test)

    # Evaluar el rendimiento del modelo usando Mean Absolute Deviation (MAE)
    mae = mean_absolute_error(y_test, y_pred)

    # Remove "Partit" from countrySplit to create model filename
    country_name = re.sub(r'^Partit', '', countrySplit)
    model_filename = f"models/model_Build_{country_name}.pkl"

    # Ensure the 'models' directory exists
    os.makedirs("models", exist_ok=True)

    # Save the model as a .pkl file
    joblib.dump(model, model_filename)

    return model, mae

build_mod_button = False

if selected_features: # A model cannot be built with no selected data
    build_mod_button = ui.button(text="Build Model", key="build_mod_button")

mae_model_built = 0.0
model_ESP_build = LinearRegression()
model_POR_build = LinearRegression()
model_ITA_build = LinearRegression()
model_GRE_build = LinearRegression()
model_built = False 

if build_mod_button and selected_features:
    # Make the model using the function
    
    model_ESP_build, mae_ESP = make_model('PartitESP', selected_features)
    model_POR_build, mae_POR = make_model('PartitPOR', selected_features)
    model_ITA_build, mae_ITA = make_model('PartitITA', selected_features)
    model_GRE_build, mae_GRE = make_model('PartitGRE', selected_features)
    mae_model_built = (mae_ESP + mae_POR + mae_ITA + mae_GRE) / 4
    #st.success("Your Model have been successfully built!")
    ui.card(title="Mean Absolute Error (MAE) of your Model", content=f"{round(mae_model_built,2)}%", description="", key="card3").render()
    model_built = True

    build_mod_button = False

# Predict the personalized model
#prediction = model.predict([[search_interest]])
#st.write(f'Predicted election outcome: {prediction[0]}')
st.subheader("2.2. Test your own model")                                    
# Initial inputs with default values
wb_share_input_2 = 50
nw_share_input_2 = 50
yt_share_input_2 = 50
wk_share_input_2 = 50
polls_input_2 = 50
cand_wb_share_input_2 = 50
cand_nw_share_input_2 = 50
cand_yt_share_input_2 = 50
cand_wk_share_input_2 = 50
party_age_input_2 = 1
party_gov_input_2 = 0
ideology_L_input_2 = 1
ideology_R_input_2 = 0
days_left_input_2 = 7

# Dictionaries to convert selectbox options to numeric values
#dict_binary = {"Yes": 1, "No": 0}
#dict_ideo_left = {"Not Left-wing": 0, "Center-Left": 1, "Left": 2, "Far-Left": 3}
#dict_ideo_right = {"Not Right-wing": 0, "Center-Right": 1, "Right": 2, "Far-Right": 3}

# Create columns for displaying the widgets
col1_2, col2_2, col3_2 = st.columns([1, 1, 1])

# Initialize an empty dictionary for user input data
user_input_data_2 = {}

# Display sliders/selectboxes based on `selected_features`
with col1_2:
    if "WebShare" in selected_features:
        wb_share_input_2 = st.slider("Web Share(%)", 0, 100, wb_share_input_2)
        user_input_data_2["WikipediaShare"] = wb_share_input_2
    if "NewsShare" in selected_features:
        nw_share_input_2 = st.slider("News Share(%)", 0, 100, nw_share_input_2)
        user_input_data_2["NewsShare"] = nw_share_input_2
    if "YoutubeShare" in selected_features:
        yt_share_input_2 = st.slider("Youtube Share(%)", 0, 100, yt_share_input_2)
        user_input_data_2["YoutubeShare"] = yt_share_input_2
    if "WikipediaShare" in selected_features:
        wk_share_input_2 = st.slider("Wikipedia Share(%)", 0, 100, wk_share_input_2)
        user_input_data_2["WikipediaShare"] = wk_share_input_2
    if "Polls" in selected_features:
        polls_input_2 = st.slider("Polls(%)", 0, 100, polls_input_2)
        user_input_data_2["Polls"] = polls_input_2

with col2_2:
    if "CandWebShare" in selected_features:
        cand_wb_share_input_2 = st.slider("Candidate Web Share(%)", 0, 100, cand_wb_share_input_2)
        user_input_data_2["CandWebShare"] = cand_wb_share_input_2
    if "CandNewsShare" in selected_features:
        cand_nw_share_input_2 = st.slider("Candidate News Share(%)", 0, 100, cand_nw_share_input_2)
        user_input_data_2["CandNewsShare"] = cand_nw_share_input_2
    if "CandYoutubeShare" in selected_features:
        cand_yt_share_input_2 = st.slider("Candidate Youtube Share(%)", 0, 100, cand_yt_share_input_2)
        user_input_data_2["CandYoutubeShare"] = cand_yt_share_input_2
    if "CandWikipediaShare" in selected_features:
        cand_wk_share_input_2 = st.slider("Candidate Wikipedia Share(%)", 0, 100, cand_wk_share_input_2)
        user_input_data_2["CandWikipediaShare"] = cand_wk_share_input_2

with col3_2:
    if "DaysLeft" in selected_features:
        days_left_input_2 = st.slider("Days Left for Election ", 1, 14, days_left_input_2)
        user_input_data_2["DaysLeft"] = days_left_input_2
    if "PartitNou" in selected_features:
        party_age_input_2 = st.selectbox("New Party ", ["No", "Yes"])
        user_input_data_2["PartitNou"] = dict_binary[party_age_input_2]

    if "PartitAlGovern" in selected_features:
        party_gov_input_2 = st.selectbox("Party in Government ", ["No", "Yes"])
        user_input_data_2["PartitAlGovern"] = dict_binary[party_gov_input_2]

    if "IdeologiaEsq" in selected_features:
        ideology_L_input_2 = st.selectbox("Left Ideology ", ["Not Left-wing", "Center-Left", "Left", "Far-Left"])
        user_input_data_2["IdeologiaEsq"] = dict_ideo_left[ideology_L_input_2]

    if "IdeologiaDre" in selected_features:
        ideology_R_input_2 = st.selectbox("Right Ideology ", ["Not Right-wing", "Center-Right", "Right", "Far-Right"])
        user_input_data_2["IdeologiaDre"] = dict_ideo_right[ideology_R_input_2]
    

# Display the dynamically created dictionary
st.write("User Input Data:", user_input_data_2)

pred_built_button = False

if not model_built:
    st.warning("Please build the model first before making predictions.")
else:
    pred_built_button = ui.button(text="Make Prediction of your Model", key="pred_built_button")

if pred_built_button and model_built:
    # Reorder user_input_data_2 to match ordered_features
    user_input_data_2 = {key: user_input_data_2.get(key, None) for key in ordered_features}

    # Create the DataFrame with specified column order
    user_input_data_2_df = pd.DataFrame([user_input_data_2], columns=ordered_features)
    # Load the models and predict
    model_ESP_build = joblib.load("models/model_Build_ESP.pkl")
    model_ITA_build = joblib.load("models/model_Build_ITA.pkl")
    model_POR_build = joblib.load("models/model_Build_POR.pkl")
    model_GRE_build = joblib.load("models/model_Build_GRE.pkl")

    result_pred_ESP_2 = model_ESP_build.predict(user_input_data_2_df)[0]
    result_pred_ITA_2 = model_ITA_build.predict(user_input_data_2_df)[0]
    result_pred_POR_2 = model_POR_build.predict(user_input_data_2_df)[0]
    result_pred_GRE_2 = model_GRE_build.predict(user_input_data_2_df)[0]
    result_pred_2 = (result_pred_ESP_2 + result_pred_ITA_2 + result_pred_POR_2 + result_pred_GRE_2) / 4
    # Display the prediction result
    st.write(f"Joint Model Prediction: {round(result_pred_2, 2)}%")
    ui.card(title="Personalized Model Prediction", content=f"{round(result_pred_2,2)}%", description="Mean Absolute Error (MAE): {mae_model_build}%", key="card4").render()
    #mae_ESP