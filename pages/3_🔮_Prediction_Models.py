import streamlit as st
import pickle
import pandas as pd
# Set page config
st.set_page_config(page_title="Prediction Models", page_icon="🔮", layout="wide")

st.title('Election Outcome Prediction')

data = pd.read_csv('data/datasetSouthernEuropeElections.csv')
# Load pre-trained model
with open('models/model_PredPolls_BigData_ESP.pkl', 'rb') as f:
    model = pickle.load(f)

# User input
search_interest = st.slider('Search Interest', min_value=0, max_value=100)

# Predict using model
#prediction = model.predict([[search_interest]])

#st.write(f'Predicted election outcome: {prediction[0]}')