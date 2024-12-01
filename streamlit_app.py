
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

# Get unique dates
unique_dates = sorted(data['Date'].unique())

# Session state to track current date index
if "date_index" not in st.session_state:
    st.session_state.date_index = 0

# Navigation buttons for date selection
col1, col2, col3 = st.sidebar.columns([1, 2, 1])
with col1:
    if st.button("◀ Prev"):
        st.session_state.date_index = max(0, st.session_state.date_index - 1)
with col3:
    if st.button("Next ▶"):
        st.session_state.date_index = min(len(unique_dates) - 1, st.session_state.date_index + 1)

# Display the currently selected date
selected_date = unique_dates[st.session_state.date_index]
st.sidebar.write(f"Selected Date: **{selected_date}**")

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
