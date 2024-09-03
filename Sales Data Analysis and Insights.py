#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[16]:


file_path = "C:\\Users\\Administrator\\DS Project Portfolio\\cleaned_Sales_dataset.csv"
data = pd.read_csv(file_path, encoding='latin1')
data.sample(5)


# ## DATA ANALYSIS TIME

# **1. Sales Trends by Product Line and Territory:**
# We want to analyze which product lines generate the highest sales across different territories (EMEA, APAC, Americas, Japan) and identify top-selling products within each product line.

# In[17]:


# Step 1: Filter and Aggregate by PRODUCTLINE and TERRITORY
sales_by_productline_territory = data.groupby(['PRODUCTLINE', 'TERRITORY'])['SALES'].sum().reset_index()

# Step 2: Identify top-selling products within each PRODUCTLINE
top_selling_products = sales_by_productline_territory.groupby('PRODUCTLINE').apply(lambda x: x.loc[x['SALES'].idxmax()]).reset_index(drop=True)

# Display the results
print("Top-selling products by PRODUCTLINE and TERRITORY:")
top_selling_products[['PRODUCTLINE', 'TERRITORY', 'SALES']]


# In[18]:


# Step 1: Filter and Aggregate by PRODUCTLINE and TERRITORY
sales_by_productline_territory = data.groupby(['PRODUCTLINE', 'TERRITORY'])['SALES'].sum().reset_index()

# Step 2: Identify top-selling products within each PRODUCTLINE
top_selling_products = sales_by_productline_territory.groupby('PRODUCTLINE').apply(lambda x: x.loc[x['SALES'].idxmax()]).reset_index(drop=True)

# Visualization
plt.figure(figsize=(10, 6))
colors = {'EMEA': 'tab:blue', 'APAC': 'tab:orange', 'Americas': 'tab:green', 'Japan': 'tab:red'}  # Color mapping for territories
bar_width = 0.4
padding = 0.1
index = range(len(top_selling_products))  # Index based on number of PRODUCTLINE categories

# Plotting bars for each territory
for i, territory in enumerate(['EMEA', 'APAC', 'Americas', 'Japan']):
    sales_data = top_selling_products[top_selling_products['TERRITORY'] == territory]
    # Ensure sales_data has the same length as index
    sales_data = sales_data.reindex(index, fill_value=0)  # Fill missing values with 0 if any
    plt.bar([x + i * (bar_width + padding) for x in index], sales_data['SALES'], width=bar_width, label=territory, color=colors[territory])

plt.xlabel('PRODUCTLINE')
plt.ylabel('SALES')
plt.title('Top-Selling Products by PRODUCTLINE and TERRITORY')
plt.xticks(index, top_selling_products['PRODUCTLINE'], rotation=45)
plt.legend(title='TERRITORY')
plt.tight_layout()
plt.show()


# #### This shows that most of the market sales comes from the EMEA 

# ### Lets dig a bit more:
# 1. Let's see the top regions by Sales
# 2. Let's see the top countries by Sales

# In[20]:


# Aggregate sales by City, State, Country, and Territory
geo_sales = data.groupby(['CITY', 'STATE', 'COUNTRY', 'TERRITORY'])['SALES'].sum().reset_index()

# Sort the data by Sales in descending order
geo_sales_sorted = geo_sales.sort_values(by='SALES', ascending=False)

# Let's look at the top 10 regions by sales
top_geo_sales = geo_sales_sorted.head(10)

# Plotting the top 10 regions by sales
plt.figure(figsize=(12, 8))
sns.barplot(x='SALES', y='CITY', data=top_geo_sales, palette='viridis')
plt.title('Top 10 Regions by Sales')
plt.xlabel('Total Sales')
plt.ylabel('City')
plt.show()


# In[21]:


# Additionally, we can plot by Country or State for a broader view
country_sales = data.groupby('COUNTRY')['SALES'].sum().sort_values(ascending=False).reset_index()

# Plotting the top 10 countries by sales
plt.figure(figsize=(12, 8))
sns.barplot(x='SALES', y='COUNTRY', data=country_sales.head(10), palette='viridis')
plt.title('Top 10 Countries by Sales')
plt.xlabel('Total Sales')
plt.ylabel('Country')
plt.show()


# **2. Seasonal Analysis:**
# 
# Seasonal analysis of the sales dataset, utilizing `ORDERDATE`, `QTR_ID`, `MONTH_ID`, and `YEAR_ID`, serves to uncover recurring patterns in sales across quarters, months, and years. This analysis provides critical insights for inventory management, forecasting future sales trends, optimizing marketing strategies tailored to peak seasons, and efficiently planning resources like staffing and production schedules. 
# 
# By understanding seasonal variations, businesses can benchmark performance, make informed decisions on product launches and pricing strategies, and gain deeper insights into customer behaviors and preferences throughout the year. Overall, seasonal analysis facilitates proactive decision-making that enhances operational efficiency, improves customer satisfaction, and drives sustainable business growth.

# In[22]:


monthly_sales = data.groupby(['YEAR_ID', 'MONTH_ID'])['SALES'].sum().reset_index()

# Creating a 'Year-Month' column for better visualization
monthly_sales['Year-Month'] = pd.to_datetime(monthly_sales['YEAR_ID'].astype(str) + '-' + monthly_sales['MONTH_ID'].astype(str).str.zfill(2) + '-01')

# Sorting the data by 'Year-Month'
monthly_sales = monthly_sales.sort_values('Year-Month')

# Plotting the Monthly Sales Trend
plt.figure(figsize=(14, 6))
plt.plot(monthly_sales['Year-Month'], monthly_sales['SALES'], marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# It is obvious that the peak time is around the last quarter of the year

# **3. Top Performing Products**

# In[23]:


# Aggregate sales by product line
product_line_sales = data.groupby('PRODUCTLINE')['SALES'].sum().reset_index()
product_line_sales = product_line_sales.sort_values(by='SALES', ascending=False)

# Display results
print("Top Sales by Product Line:")
print(product_line_sales)

# Plot the results
plt.figure(figsize=(10, 6))
plt.bar(product_line_sales['PRODUCTLINE'], product_line_sales['SALES'], color='brown')
plt.xlabel('Product Line')
plt.ylabel('Total Sales')
plt.title('Total Sales by Product Line')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()  # Adjust layout to fit labels
plt.show()


# Based on the dataset given, from the visual above Classic cars are the top performing product in this company. Hence, most capital should be invested the order of sales for each product as seen in the chart above

# **4. Customer Segmentation**
# Customer Lifetime Value (CLV) is a crucial metric that estimates the total revenue a company can expect from a customer over their entire relationship. Analyzing CLV helps businesses to:
# 
# - Identify High-Value Customers: Focus marketing efforts and resources on customers who generate the most revenue.
# - Improve Customer Retention: Develop strategies to increase the longevity and value of customer relationships.
# - Optimize Marketing Spend: Allocate budget more effectively by understanding which customer segments are most profitable.
# - Enhance Customer Segmentation: Segment customers based on their value, enabling more personalized and targeted approaches.

# In[24]:


data_copy = data.copy()

# Calculate total sales per customer
customer_sales = data_copy.groupby('CUSTOMERNAME')['SALES'].sum().reset_index()

# Calculate first and last purchase dates for each customer
customer_dates = data_copy.groupby('CUSTOMERNAME')['ORDERDATE'].agg(['min', 'max']).reset_index()
customer_dates.columns = ['CUSTOMERNAME', 'FirstPurchaseDate', 'LastPurchaseDate']

# Merge sales and dates data
customer_lifetime = pd.merge(customer_sales, customer_dates, on='CUSTOMERNAME')

# Calculate Customer Lifetime Value (CLV)
customer_lifetime['CLV'] = customer_lifetime['SALES']

# Display results
print("Customer Lifetime Value (CLV):")
customer_lifetime


# In[25]:


# Sorting by CLV and displaying the top customers
top_customers = customer_lifetime.sort_values(by='CLV', ascending=False)
print("\nTop Customers by CLV:")
top_customers


# In[26]:


# Summing total sales per customer to get CLV
customer_lifetime = data_copy.groupby('CUSTOMERNAME')['SALES'].sum().reset_index()
customer_lifetime.columns = ['CUSTOMERNAME', 'CLV']

# Sort customers by CLV in descending order
customer_lifetime = customer_lifetime.sort_values(by='CLV', ascending=False)

total_revenue = customer_lifetime['CLV'].sum()

# Calculate cumulative revenue percentage
customer_lifetime['Cumulative_Rev'] = customer_lifetime['CLV'].cumsum() / total_revenue * 100

# Define the threshold for top X% customers (e.g., top 10%)
threshold = 10

# Get the index where the cumulative revenue crosses the threshold
top_customers_index = customer_lifetime[customer_lifetime['Cumulative_Rev'] <= threshold].index.max()

# Calculate X% and Y%
top_X_percent_customers = (top_customers_index + 1) / len(customer_lifetime) * 100
top_Y_percent_revenue = customer_lifetime.iloc[top_customers_index]['Cumulative_Rev']

top_customer = customer_lifetime.iloc[0]
low_clv_customer = customer_lifetime.iloc[-1]

# Extract details
top_customer_name = top_customer['CUSTOMERNAME']
top_clv_value = top_customer['CLV']

low_customer_name = low_clv_customer['CUSTOMERNAME']
low_clv_value = low_clv_customer['CLV']


# In[27]:


print(f"The CLV analysis of {len(customer_lifetime)} customers reveals that the top {round(top_X_percent_customers, 1)}% of customers contribute {round(top_Y_percent_revenue, 1)}% to the total revenue. {top_customer_name}, with a CLV of ${top_clv_value:,.2f}, is the highest contributor. Focusing on these high-value customers with targeted retention strategies can further boost their impact.")

print(f"On the other hand, customers like {low_customer_name}, with a CLV of ${low_clv_value:,.2f}, present growth opportunities. By implementing personalized offers, their lifetime value could be increased, contributing to overall profitability.")


# **Report on the CLV analysis:**
# 
# The CLV analysis of 92 customers reveals that the top 37.0% of customers contribute 59.6% to the total revenue. 
# 
# Euro Shopping Channel, with a CLV of $912,294.11, is the highest contributor. Focusing on these high-value customers with targeted retention strategies can further boost their impact.
# 
# On the other hand, customers like Boards & Toys Co., with a CLV of $9,129.35, present growth opportunities. By implementing personalized offers, their lifetime value could be increased, contributing to overall profitability.

# **5. Profitability Analysis**

# In[28]:


# Calculate Gross Margin for each product
data['GROSS_MARGIN'] = ((data['PRICEEACH'] - data['MSRP']) / data['PRICEEACH']) * 100

# Aggregate gross margin by PRODUCTCODE and PRODUCTLINE (or any other relevant columns)
gross_margin_summary = data.groupby(['PRODUCTCODE', 'PRODUCTLINE'])['GROSS_MARGIN'].mean().reset_index()

# Sort by Gross Margin in descending order
gross_margin_summary_sorted = gross_margin_summary.sort_values(by='GROSS_MARGIN', ascending=False)

# Plotting the top products by Gross Margin
plt.figure(figsize=(12, 8))
ax = sns.barplot(x='GROSS_MARGIN', y='PRODUCTCODE', data=gross_margin_summary_sorted.head(10), palette='coolwarm')

# Adding percentage labels above the bars
for index, row in gross_margin_summary_sorted.head(10).iterrows():
    ax.text(row['GROSS_MARGIN'] + 0.5, index, f'{row["GROSS_MARGIN"]:.1f}%', ha='left', va='center')

plt.title('Top 10 Products by Gross Margin')
plt.xlabel('Gross Margin (%)')
plt.ylabel('Product Code')
plt.show()


# In[ ]:




