
import streamlit as st
import pandas as pd
import plotly.express as px

# Load and preprocess the data
file_path = 'data-gas-nov-download.csv'  # Update this if needed
data = pd.read_csv(file_path)

# Convert 'Start' column to datetime
data['Start'] = pd.to_datetime(data['Start'])

# Extract date and time for filtering
data['Date'] = data['Start'].dt.date
data['Time'] = data['Start'].dt.time

# App title
st.title("Daily Energy Consumption and Cost Tracker")

# Sidebar for user inputs
st.sidebar.header("Filter Options")

# Date selection
unique_dates = sorted(data['Date'].unique())
selected_date = st.sidebar.selectbox("Select a Day", unique_dates)

# Metric selection
metric = st.sidebar.radio(
    "Select Metric to Display",
    ["Consumption (kWh)", "Estimated Cost Inc. Tax (p)"]
)

# Filter data by selected date
filtered_data = data[data['Date'] == selected_date]

# Display the filtered graph
fig = px.line(
    filtered_data,
    x="Start",
    y=metric,
    title=f"{metric} on {selected_date}",
    labels={"Start": "Time", metric: metric},
    markers=True
)

st.plotly_chart(fig)

# Display raw data if user wants
if st.sidebar.checkbox("Show Raw Data"):
    st.write(filtered_data)
