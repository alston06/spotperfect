import streamlit as st
import pickle
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="SpotPerfect - Peaky blinders ",
    page_icon="📍---📍",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("<h1 style='text-align: center;'>SpotPerfect 📍</h1>", unsafe_allow_html=True)

# Get the absolute path to the current directory
current_dir = os.getcwd()

# Construct the full paths to the pickle files
model_path = os.path.join(current_dir, 'model.pkl')
scaler_path = os.path.join(current_dir, 'scaler.pkl')

# Load the model and scaler
model = pickle.load(open(model_path, 'rb'))
scaler = pickle.load(open(scaler_path, 'rb'))

# Streamlit app
st.markdown("<h1 style='text-align: center;'>City Suitability Prediction</h1>", unsafe_allow_html=True)

# Initialize session state
if 'prediction_made' not in st.session_state:
    st.session_state['prediction_made'] = False
    st.session_state['predicted_score'] = None

# Create a form for input
with st.form(key='predict_form'):
    feature_1 = st.slider('Population', min_value=100000, max_value=5000000, value=2342868)
    feature_2 = st.slider('Road Quality', min_value=100000, max_value=2000000, value=1122336)
    feature_3 = st.number_input('Tier Value', min_value=1, max_value=3, value=3, step=1)
    feature_4 = st.slider('Average Income', min_value=10000, max_value=100000, value=31009)
    feature_5 = st.number_input('Literacy Rate', min_value=1, max_value=10, value=6, step=1)
    feature_6 = st.number_input('Railways Count', min_value=1, max_value=10, value=3, step=1)
    feature_7 = st.slider('Average Land Price (per sq feet)', min_value=1, max_value=10000, value=3293)
    feature_8 = st.slider('Airport Proximity', min_value=1, max_value=100, value=30)

    # Submit button
    submit_button = st.form_submit_button(label='Predict Suitability')

if submit_button:
    # Prepare the input array for prediction
    new_input = np.array([[feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8]])
    new_input = scaler.transform(new_input)
    predicted_score = model.predict(new_input)[0]

    # Save the prediction to session state
    st.session_state['predicted_score'] = predicted_score
    st.session_state['prediction_made'] = True

if st.session_state['prediction_made']:
    # Load your data into pandas DataFrames
    output_df = pd.read_csv('output.csv')  # Replace with your actual file path
    cleaned_df = pd.read_csv('combined_data.csv')  # Replace with your actual file path

    # Clean and prepare the location data
    for df in [output_df, cleaned_df]:
        df['location'] = df['location'].str.lstrip(',')  # Remove leading commas
        df['location'] = df['location'].str.strip()
        df['location'] = df['location'].str.replace(r'\(.*\)', '', regex=True).str.strip()  # Remove trailing characters
        df['location'] = df['location'].apply(lambda x: ', '.join([part.strip() for part in x.split(',')]) if isinstance(x, str) else x)

    # Merge the data based on city names
    merged_df = pd.merge(output_df, cleaned_df[['location', 'lats', 'longs']], on='location', how='left')

    # Apply constraints and classify
    def classify_location(row):
        if (row['population'] > 1000000 and
            row['dist_road_qual'] > 800000 and 
            row['tier_value'] in [1, 2] and (row['airport_proximity'] > 20 or
            row['airport_proximity'] < 50) or (row['literacy_rate'] > 7 and row['railways_count'] < 6) and (row['edi'] > 25000 and row['edi'] < 70000) and
            (row['average_land_price'] > 2000 and row['average_land_price'] < 5000)):
            return 'Cross-Docking Center'
        
        elif((row['population'] > 500000 and row['population'] < 3000000) or
            row['dist_road_qual'] > 800000 or 
            row['tier_value'] in [2, 3] and (row['airport_proximity'] > 30 and
            row['airport_proximity'] < 80) and (row['literacy_rate'] > 7 and row['railways_count'] > 5 and row['railways_count'] < 11) and (row['edi'] > 15000 and row['edi'] < 50000) and
            (row['average_land_price'] > 2000 and row['average_land_price'] < 5000)):
            return 'Warehouse'
        else:
            return 'Cross-Docking Center'

    merged_df['classification'] = merged_df.apply(classify_location, axis=1)
      # Convert Average Land Price to Acres
    # Calculate the difference in suitability score
    merged_df['suitability_diff'] = abs(merged_df['suitability_score'] - st.session_state['predicted_score'])

    # Get the top 10 closest cities
    top_10_cities = merged_df.nsmallest(10, 'suitability_diff')

    # Filter the cities with valid latitude and longitude
    valid_cities = top_10_cities.dropna(subset=['lats', 'longs'])

    # Display the results
    st.subheader("Top 10 cities closest to the predicted suitability score:")
    st.dataframe(top_10_cities[['location', 'suitability_score', 'classification']])

    if not valid_cities.empty:
        st.write("Rendering map...")
        # Create a folium map centered around the mean location
        m = folium.Map(location=[valid_cities['lats'].mean(), valid_cities['longs'].mean()], zoom_start=5, tiles='CartoDB positron')

        # Define color scheme for classification
        color_scheme = {
            'Cross-Docking Center': 'red',
            'Warehouse': 'blue',
            'Unclassified': 'gray'
        }

        # Add city markers to the map with popups containing all relevant information
        for idx, row in valid_cities.iterrows():
            popup_html = f"""
            <div style="width: 300px; font-family: Arial; font-size: 12px;">
                <h4 style="color: #2A9D8F;">{row['location']}</h4>
                <p><strong>Classification:</strong> {row['classification']}</p>
                <p><strong>Population:</strong> {row['population']:,}</p>
                <p><strong>Road Quality:</strong> {row['dist_road_qual']}</p>
                <p><strong>Tier Value:</strong> {row['tier_value']}</p>
                <p><strong>Literacy Rate:</strong> {row['literacy_rate']}</p>
                <p><strong>Railways Count:</strong> {row['railways_count']}</p>
                <p><strong>Average Land Price (per sqft) :</strong> {row['average_land_price']:.2f} Rs</p>
                <p><strong>Airport Proximity:</strong> {row['airport_proximity']} Km</p>
            </div>
            """

            folium.Marker(
                location=[row['lats'], row['longs']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=color_scheme[row['classification']], icon='info-sign')
            ).add_to(m)

        # Render the map in Streamlit
        st_folium(m, width=1000, height=600)
    else:
        st.write("No valid locations found for mapping.")

    # Plot graphs for each parameter across the top locations
    st.subheader("Parameter Comparisons Across Top Locations")
    parameters = {
        'Population': 'population',
        'Road Quality': 'dist_road_qual',
        'Tier Value': 'tier_value',
        'Literacy Rate': 'literacy_rate',
        'Railways Count': 'railways_count',
        'Economic Data Interchange': 'edi',
        'Average Land Price (per acre)': 'average_land_price',
        'Airport Proximity': 'airport_proximity'
    }

    # Loop through each parameter and create a horizontal bar chart for each
    for param_name, param_column in parameters.items():
        fig, ax = plt.subplots(figsize=(10, 5))  # Adjust figsize as needed for each graph
        has_data = False

        for classification in valid_cities['classification'].unique():
            data = valid_cities[valid_cities['classification'] == classification]
            if not data.empty:
                ax.barh(data['location'], data[param_column], 
                        label=classification, 
                        color=color_scheme[classification], 
                        alpha=0.7)
                has_data = True

        if has_data:
            ax.set_title(f'{param_name} Across Top Locations')
            ax.set_xlabel(param_name)
            ax.set_ylabel('Location')
            ax.tick_params(axis='y', labelsize=10)
            ax.legend()
            plt.tight_layout()
             # Rotate x-axis labels and adjust alignment
            st.pyplot(fig)  # Display the graph in Streamlit
        else:
            st.write(f"No data available for {param_name}.")
