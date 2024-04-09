import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Sample data for demonstration
amazon_data = {
    'Product': ['Product A', 'Product B', 'Product C', 'Product D'],
    'Price (Amazon)': ['$100', '$150', '$200', '$250'],
    'MRP (Amazon)': ['$120', '$160', '$220', '$260'],
    'Ratings (Amazon)': [4.5, 3.8, 4.2, 4.0]
}

flipkart_data = {
    'Product': ['Product A', 'Product C', 'Product E', 'Product F'],
    'Price (Flipkart)': ['$95', '$140', '$210', '$270'],
    'MRP (Flipkart)': ['$110', '$155', '$230', '$280'],
    'Ratings (Flipkart)': [4.4, 3.7, 4.0, 3.5]
}

# Create DataFrames from sample data
df_amazon = pd.DataFrame(amazon_data)
df_flipkart = pd.DataFrame(flipkart_data)

# Merge DataFrames on 'Product' column to find common products
df_common = pd.merge(df_amazon, df_flipkart, on='Product', how='inner')

# Reset index to start from 1
df_common.index = range(1, len(df_common) + 1)

# Display tables in Streamlit without scrollbars
st.set_page_config(layout="wide")
st.title('Product Comparison: Amazon vs Flipkart')

# Display common products with a bar chart
st.header('Common Products')
df_common = df_common.copy()  # Make a copy to avoid modifying the original DataFrame
df_common['Price (Amazon)'] = df_common['Price (Amazon)'].str.replace('$', '').astype(float)
df_common['Price (Flipkart)'] = df_common['Price (Flipkart)'].str.replace('$', '').astype(float)
st.dataframe(df_common.style.format({'Price (Amazon)': '${:.2f}', 'Price (Flipkart)': '${:.2f}'}))

# Create a vertical bar chart for common products
fig, ax = plt.subplots()
bar_index = df_common.index
bar_width = 0.35
amazon_prices = df_common['Price (Amazon)']
flipkart_prices = df_common['Price (Flipkart)']
ax.bar(bar_index, amazon_prices, bar_width, label='Amazon', color='blue')
ax.bar(bar_index + bar_width, flipkart_prices, bar_width, label='Flipkart', color='orange')
ax.set_xticks(bar_index + bar_width / 2)
ax.set_xticklabels(df_common['Product'], rotation=45, ha='right')
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
ax.set_ylabel('Price')
ax.set_xlabel('Product')
ax.set_title('Price Comparison of Common Products')
ax.legend()

# Adjust layout to prevent cutting off labels
plt.tight_layout()

# Display the chart
st.pyplot(fig)

# Display unique products for Amazon without scrollbars
st.header('Amazon Unique Products')
df_amazon['Price (Amazon)'] = df_amazon['Price (Amazon)'].str.replace('$', '').astype(float)
df_amazon['MRP (Amazon)'] = df_amazon['MRP (Amazon)'].str.replace('$', '').astype(float)
st.dataframe(df_amazon[~df_amazon['Product'].isin(df_common['Product'])].style.format({'Price (Amazon)': '${:.2f}', 'MRP (Amazon)': '${:.2f}'}))

# Display unique products for Flipkart without scrollbars
st.header('Flipkart Unique Products')
df_flipkart['Price (Flipkart)'] = df_flipkart['Price (Flipkart)'].str.replace('$', '').astype(float)
df_flipkart['MRP (Flipkart)'] = df_flipkart['MRP (Flipkart)'].str.replace('$', '').astype(float)
st.dataframe(df_flipkart[~df_flipkart['Product'].isin(df_common['Product'])].style.format({'Price (Flipkart)': '${:.2f}', 'MRP (Flipkart)': '${:.2f}'}))
