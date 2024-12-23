# -*- coding: utf-8 -*-
"""streamlit_app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zjvjwDw2xJyJRGp4bcemddGlB6VoAkT7
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Grab data from the CSV file on GitHub
url = "https://raw.githubusercontent.com/bre5551/Project/main/bls_data.csv"

# Load the data
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)

    # Map period codes if necessary
    if 'period' in df.columns:
        period_map = {f"M{str(i).zfill(2)}": i for i in range(1, 13)}
        df['month'] = df['period'].map(period_map)
        df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str) + '-01')
    elif 'period_name' in df.columns:
        df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['period_name'])
    else:
        st.error("Missing required column for date construction ('period' or 'period_name').")

    return df


# Load the data
data = load_data(url)

# Breakout individual datasets for each series
nonfarm_data = data[data['series_id'] == 'CES0000000001']
unemployment_data = data[data['series_id'] == 'LNS14000000']
civilian_labor_data = data[data['series_id'] == 'LNS11000000']
hourly_earnings_data = data[data['series_id'] == 'CES0500000003']

# Create charts
st.title("BLS Data Visualizations")

# 1. Line Chart for Nonfarm Payrolls
st.subheader("Nonfarm Payrolls (CES0000000001)")
line_fig = px.line(nonfarm_data, x='date', y='value', title='Nonfarm Payrolls Over Time', labels={'value': 'Payrolls', 'date': 'Date'})
st.plotly_chart(line_fig)

# 2. Bar Chart for Unemployment Rate
st.subheader("Unemployment Rate (LNS14000000)")
bar_fig = px.bar(unemployment_data, x='date', y='value', title='Unemployment Rate Over Time', labels={'value': 'Unemployment Rate (%)', 'date': 'Date'})
st.plotly_chart(bar_fig)

# 3. Area Chart for Civilian Labor Force
st.subheader("Civilian Labor Force (LNS11000000)")
area_fig = px.area(civilian_labor_data, x='date', y='value', title='Civilian Labor Force Over Time', labels={'value': 'Labor Force', 'date': 'Date'})
st.plotly_chart(area_fig)

# 4. Scatter Plot for Avg Hourly Earnings
st.subheader("Average Hourly Earnings (CES0500000003)")
scatter_fig = px.scatter(hourly_earnings_data, x='date', y='value', title='Avg Hourly Earnings Over Time', labels={'value': 'Hourly Earnings ($)', 'date': 'Date'})
st.plotly_chart(scatter_fig)