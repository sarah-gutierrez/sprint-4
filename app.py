import streamlit as st
import pandas as pd
import plotly.express as px
#Load the dataset
df = pd.read_csv('vehicles_us.csv')
st.header('Car Sales Advertisements Dashboard')
# Checkbox for fuel type
if st.checkbox('Show only gas fuel type'):
    filtered_df = df[df['fuel'] == 'gas']
else:
    filtered_df = df

# Add a plotly histogram for price distribution
fig_hist = px.histogram(filtered_df, x='price', title='Price Distribution')
st.plotly_chart(fig_hist)

# Scatterplot of price data vs days listed
fig_scatter = px.scatter(filtered_df, x='days_listed', y='price', title='Price vs Days Listed')
st.plotly_chart(fig_scatter)