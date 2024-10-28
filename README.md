# Exploring the Potential of Big Data in Southern Europe Elections

This repository hosts the Final Degree Project (FDP) titled **"Exploring the Potential of Big Data in Southern Europe Elections."** The project investigates the correlation between electoral polls and Big Data by analyzing search data from Google and Wikipedia related to political parties and their candidates during electoral periods in Spain, Italy, Portugal, and Greece. The project has been converted into an interactive Streamlit application with two main sections:

- **Exploratory Data Analysis (EDA):** Visualize search trends by country and overall for key political entities during election periods.
- **Prediction Models:** Test models to predict election results based on search data, comparing Big Data insights with traditional polling methods.

## Abstract

This Final Engineering Project studies the correlation between electoral polls and Big Data, extracting search data on political parties and their candidates through Google and Wikipedia during the electoral period in Southern European countries. We analyzed data from the last elections of the four most populated countries in Southern Europe: Spain, Italy, Portugal, and Greece, using parliamentary elections held until 31 December 2023 as the reference point.

Our analysis revealed that while Big Data alone is insufficient for predicting electoral outcomes (yielding a Mean Absolute Error (MAE) of 7.17%), it can slightly improve the accuracy of traditional electoral polls. However, these improvements are not significant, and thus Big Data cannot replace electoral polls as a reliable prediction method.

## Streamlit Application

The Streamlit app is structured into two main pages:

1. **Exploratory Data Analysis (EDA):**
   - **By Country:** Analyze search data trends for each country individually (Spain, Italy, Portugal, Greece).
   - **Overall Trends:** Get an overview of search trends across all four countries during the electoral periods.

2. **Prediction Models:**
   - Test the performance of models trained on search data from Google and Wikipedia to predict election results.
   - Compare the predictive power of Big Data with traditional polling data.

## Features

- **Data Collection:** Aggregated search data from Google and Wikipedia, focusing on political parties and candidates during parliamentary election periods.
- **Data Visualization:** Interactive visualizations of search trends using Streamlit for easy exploration of the data.
- **Predictive Models:** Linear regression models that attempt to predict election outcomes based on search volume.

## Conclusion

While Big Data alone cannot predict election outcomes with high accuracy, it can complement traditional electoral polls to provide a slight improvement in predictive power. However, the current results indicate that the improvement is not sufficient to rely solely on Big Data for electoral predictions.

## Installation

To run the project locally:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/BigData-SouthernEurope-Elections.git
    cd BigData-SouthernEurope-Elections
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit application:
    ```bash
    streamlit run streamlit_app.py
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, feel free to reach out via [LinkedIn](https://www.linkedin.com/in/your-profile/) or open an issue on this repository.
