import streamlit as st
import pandas as pd
import plotly.express as px
#Load the dataset
df = pd.read_csv('vehicles_us.csv')
st.header('Car Sales Advertisements Dashboard')

# Pre-processing: Missing Values and Duplicates
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

fig1 = px.histogram(filtered_df , x='price', title='Price Distribution - Outliers Filtered Out', labels={'price': 'Price (USD)'})
fig1.show()

#Check all types of available fuel options
print(df['fuel'].unique())

#Scatterplot of price data vs days listed
fig_scatter = px.scatter(df, x='days_listed', y='price', title='Price (Outliers Removed) vs. Days Listed', labels={'days_listed': 'Number of Days Listed on Ad', 'price': 'Price (USD)' })
fig_scatter.show()

#Scatterplot with outliers removed for price
fig_scatter2 = px.scatter(filtered_df, x='model_year', y='price', title='Model Year vs Price (Outliers Removed)', labels={'days_listed': 'Number of Days Listed on Ad', 'price': 'Price (USD)' })
fig_scatter2.show()

# Checkbox for fuel type
if st.checkbox('Show only gas fuel type'):
    filtered_df_gas = df[df['fuel'] == 'gas']
else:
    filtered_df = df

# Add a plotly histogram for price distribution
fig_hist = px.histogram(filtered_df, x='price', title='Price Distribution')
st.plotly_chart(fig_hist)

# Scatterplot of price data vs days listed
fig_scatter = px.scatter(filtered_df, x='days_listed', y='price', title='Price vs Days Listed')
st.plotly_chart(fig_scatter)