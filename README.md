# Vizualization-Project
Israel Public Transportation Dashboard
An interactive analytics dashboard for exploring public transportation data in Israel across 2023 and 2024. This project visualizes key performance indicators such as route length, passenger volume, operational costs, and trip duration.

## Project Structure
main.py: The core application file containing the Dash web interface and visualization logic.

VisualizationProj.ipynb: A Jupyter Notebook used for data cleaning, preprocessing, and exploratory data analysis (including handling missing values with Scikit-Learn).

combined_clean_data.csv: The processed dataset resulting from merging and cleaning the raw 2023/2024 data.

data2023.csv / data2024.csv: Raw datasets containing route information and ridership statistics.

cities_coords.csv: Geographical data (latitude/longitude) for cities, used for spatial visualizations.

Features
Interactive Dashboard: Built with Dash and Plotly, allowing users to filter data dynamically.

Correlation Analysis: Visualize relationships between variables (e.g., Operating Cost per Passenger vs. Route Length) using scatter plots.

Temporal Comparison: Analyze trends and changes between 2023 and 2024.

Data Processing: Includes a robust pipeline for merging datasets and imputing missing values using Decision Tree Regressors.
