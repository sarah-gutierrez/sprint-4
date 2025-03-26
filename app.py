import streamlit as st
import pandas as pd
import plotly.express as px
#Load the dataset
df = pd.read_csv('vehicles_us.csv')
st.header('Car Sales Advertisements Dashboard')

#Pre-processing: Missing Values and Duplicates
# Missing values
print(df.isna().sum())

# Duplicate rows
print('Number of duplcate rows:', df.duplicated().sum())

# Model_year missing value and groupby
df['model_year'] = df.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median()))

df['cylinders'] = df.groupby('model')['cylinders'].transform(lambda x: x.fillna(x.median()))

df['odometer'] = df.groupby(['model_year', 'model'])['odometer'].transform(lambda x: x.fillna(x.median()))

#Identify outliers with interquartile range IQR
# Calculate IQR for 'model_year' and 'price'
Q1_model_year = df['model_year'].quantile(0.25)
Q3_model_year = df['model_year'].quantile(0.75)
IQR_model_year = Q3_model_year - Q1_model_year

Q1_price = df['price'].quantile(0.25)
Q3_price = df['price'].quantile(0.75)
IQR_price = Q3_price - Q1_price

# Define outlier boundaries
lower_bound_model_year = Q1_model_year - 1.5 * IQR_model_year
upper_bound_model_year = Q3_model_year + 1.5 * IQR_model_year

lower_bound_price = Q1_price - 1.5 * IQR_price
upper_bound_price = Q3_price + 1.5 * IQR_price

#Remove outliers (filtering)
# Filter out the outliers
filtered_df = df[(df['model_year'] >= lower_bound_model_year) & 
                 (df['model_year'] <= upper_bound_model_year) & 
                 (df['price'] >= lower_bound_price) & 
                 (df['price'] <= upper_bound_price)]

#To ensure informative visualizations, outliers were identified and removed. This helps the reliability of data trends in the analysi. Scatterplot before for Model Year Vs. Price with outliers removed is shown below.

# Fuel type selection
fuel_options = df['fuel'].unique()  # Get unique fuel types
selected_fuels = st.multiselect("Select Fuel Types:", options=fuel_options, default=fuel_options)

# Filter dataframe based on selected fuel types
filtered_df = filtered_df[filtered_df['fuel'].isin(selected_fuels)]

# Scatterplot: Price vs Days Listed
fig_scatter1 = px.scatter(filtered_df, x='days_listed', y='price', 
                          title='Price (Outliers Removed) vs. Days Listed', 
                          labels={'days_listed': 'Number of Days Listed on Ad', 'price': 'Price (USD)'})

fig_scatter1.update_layout(yaxis=dict(range=[0, 40000]))

st.plotly_chart(fig_scatter1)
st.write('Note: Scatterplot for Price vs Days Listed: Set y-axis limit (e.g., max price is 40,000). Top edge of data appears to be cut out but this is due to outliers. Increase max of y-axis to improve visibility that plot itself is not cut off.')

# Scatterplot: Model Year vs Price
fig_scatter2 = px.scatter(filtered_df, x='model_year', y='price', 
                          title='Model Year vs Price (Outliers Removed)', 
                          labels={'model_year': 'Model Year', 'price': 'Price (USD)'})
st.plotly_chart(fig_scatter2)

# Histogram: Price Distribution
fig_hist = px.histogram(filtered_df, x='price', 
                        title='Price Distribution - Outliers Filtered Out', 
                        labels={'price': 'Price (USD)'})
st.plotly_chart(fig_hist)