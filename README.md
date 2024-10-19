# Spot Perfect - README

## Project Name: Spot Perfect  
**Team Name:** Peaky Blinders

### Overview
**Spot Perfect** is a location suitability prediction tool designed to help businesses, especially in logistics and supply chain management, identify optimal cities in India for warehousing, distribution hubs, and cross-docking centers. It leverages a combination of census data, geospatial analysis, and web scraping to deliver accurate insights. By using **linear regression** techniques, the tool predicts the top 10 most suitable cities based on user-input factors such as population, literacy rate, rail network, airport proximity, and land prices.

### Features
- **Census Data Integration**: Uses census data including population, literacy rate, and Economic Data Interchange (EDI) index.
- **Geospatial Data**: Integrated with **Google Maps API** to retrieve and analyze proximity to rail networks and airports.
- **Land Price Scraping**: Real-time land price data collected from **99 Acres** and **Magic Bricks** websites via web scraping.
- **Linear Regression Model**: Achieves a 90% accuracy rate in predicting city suitability based on input factors.
- **Top 10 City Prediction**: Provides users with the top 10 cities ranked by suitability.
- **Geospatial Visualization**: Users can view the results on a map with detailed information and bar chart visualizations.

### Data Sources
1. **Census Data**: Official census data for population, literacy rate, and EDI index from government and public sources.
2. **Land Price Data**: Scraped from the following websites:
   - [99acres.com](https://www.99acres.com/)
   - [MagicBricks.com](https://www.magicbricks.com/)
3. **Google Maps API**: Used to gather geospatial data, such as:
   - Rail network proximity
   - Airport proximity
   - Road quality and distance analysis

### How It Works
1. **Data Collection**:  
   The project collects and processes data from a variety of sources:
   - Census data for population, literacy rate, and EDI index.
   - Web scraping techniques are used to fetch land prices from **99 Acres** and **Magic Bricks**.
   - **Google Maps API** is used to fetch proximity to airports and rail networks.
   
2. **Data Processing**:  
   The data is then cleaned, organized, and processed using a **linear regression model** to predict city suitability based on the parameters entered by the user.

3. **Prediction and Visualization**:  
   - Users enter details like population size, literacy rate, proximity to major infrastructure, and land prices.
   - The model predicts and returns the top 10 cities based on the provided inputs.
   - Results are displayed through a geospatial map and bar chart visualization, making it easy to compare different cities.

### Setup and Installation

#### Requirements
To run this project, you need the following:
- **Python 3.x**
- **Flask** (for the web app interface)
- **BeautifulSoup** (for web scraping)
- **Requests** (for fetching data from APIs)
- **Pandas** (for data processing)
- **Google Maps API Key** (for geospatial data)

#### Steps to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/spot-perfect.git
   cd spot-perfect
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your **Google Maps API Key**:
   - Visit [Google Cloud Console](https://console.cloud.google.com/), generate an API key, and enable the Maps API for geocoding and distance matrix.

4. Add your API key in the `config.py` file:
   ```python
   GOOGLE_MAPS_API_KEY = "your_google_maps_api_key"
   ```

5. Run the Flask server:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to `http://localhost:5000`.

### Usage
- On the web interface, input the required data fields such as population, literacy rate, rail network proximity, airport proximity, and land price.
- The model will process the inputs and display the top 10 cities for warehousing or logistics centers.
- Results are shown through:
  - A **geospatial map** showing the location of each city.
  - A **bar chart** comparing the suitability scores of the top 10 cities.

### References
- **Land Price Data**:
  - [99 Acres](https://www.99acres.com/)
  - [Magic Bricks](https://www.magicbricks.com/)
- **Google Maps API**:  
  For rail network, airport proximity, and geospatial data:
  - [Google Maps API Documentation](https://developers.google.com/maps/documentation)

### Accuracy and Performance
The linear regression model was trained on data from 45 cities across India, using the input parameters mentioned above. The model was validated and achieved an accuracy of **90%**, ensuring reliable predictions.

### License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

### Contact Information
**Team Peaky Blinders**  
For more information or questions, you can reach us at:  
- Email: ganeshsriramulu2@gmail.com
- GitHub: [GitHub Repository](https://github.com/Ganesh-73005/blank-app)



# 🎈 Blank app template

A simple Streamlit app template for you to modify!
[App link](spotperfect.streamlit.app)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
