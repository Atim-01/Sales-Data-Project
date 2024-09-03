#!/usr/bin/env python
# coding: utf-8

# ## DATA CLEANING TIME

# In[2]:


import os
import numpy as np
import pandas as pd


# In[3]:


# To ensure that all the data is display with no hidden column or truncated col.  
pd.set_option('display.max_columns', None)

# Loading in the data
data = pd.read_csv("C:\\Users\\Administrator\\Downloads\\sales_data_sample.csv", encoding='latin1')
data.head(5)


# In[4]:


data.tail(5)


# In[5]:


data.shape


# In[6]:


data.info()


# In[7]:


data['ORDERDATE'].unique()


# In[8]:


data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE']).dt.date


# In[9]:


data['ORDERDATE'].sample(10)


# In[10]:


data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE'], errors='coerce')


# In[11]:


data['ORDERDATE'].dtype


# In[12]:


print(data['ORDERDATE'].isna().sum())


# In[13]:


data['COUNTRY'].unique()


# In[14]:


data['STATUS'].sample(5)


# In[15]:


data['STATUS'].unique()


# In[16]:


print(data['STATUS'].isna().sum())


# In[17]:


status_counts = data['STATUS'].value_counts()
print(status_counts)


# In[18]:


status_percentages = data['STATUS'].value_counts(normalize=True) * 100
print(status_percentages)


# In[19]:


# Lets see the visuals of the STATUS column
import matplotlib.pyplot as plt
import seaborn as sns

# Creating a DataFrame to store the count and percentage
status_summary = pd.DataFrame({
    'Status': status_counts.index,  
    'Count': status_counts.values,
    'Percentage': status_percentages.values
})

# Sort by Percentage in descending order
status_summary = status_summary.sort_values(by='Percentage', ascending=False)

# Plotting
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='Status', y='Percentage', data=status_summary, palette='viridis')

# Adding percentage labels above the bars
for index, row in status_summary.iterrows():
    ax.text(row.name, row['Percentage'] + 0.5, f'{row["Percentage"]:.1f}%', ha='center')

plt.xlabel('Status')
plt.ylabel('Percentage')
plt.title('Status Distribution')
plt.show()


# In[20]:


data.sample(2)


# In[21]:


data['PRODUCTLINE'].unique()


# In[22]:


data['PRODUCTLINE'].isna().sum()


# In[23]:


# Lets see the relationship between the Productline and the Status
# Group by PRODUCTLINE and STATUS, then get the count for each combination
status_summary = data.groupby(['PRODUCTLINE', 'STATUS']).size().unstack(fill_value=0)

print(status_summary)


# This shows that most of the cancelled order is from Ships and Classic cars orders. Lets visualizing the Data:

# In[24]:


# Plotting
status_summary.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
plt.xlabel('Product Line')
plt.ylabel('Count')
plt.title('Status Distribution by Product Line')
plt.legend(title='Status', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[25]:


productline_counts = data['PRODUCTLINE'].value_counts()
print(productline_counts)


# In[26]:


data['MONTH_ID'].isna().sum()


# In[27]:


data['MONTH_ID'].unique()


# In[28]:


# I want the months to be more identifiable, instead of 1, it should be Jan
# Create a dictionary mapping month IDs to month names
month_mapping = {
    1: 'Jan', 2:'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}
# Rename the column to remove any trailing spaces
data = data.rename(columns = lambda x: x.strip())

# Map the month IDs to month names
data['MONTH_ID'] = data['MONTH_ID'].map(month_mapping)

# Ensure the column is of object type
data['MONTH_ID'] = data['MONTH_ID'].astype('object')

print(data['MONTH_ID'].head())


# In[29]:


data.sample(3)


# In[30]:


data['MSRP'].isna().sum()


# In[31]:


data['MSRP'].dtype


# In[32]:


data['MSRP'].unique()


# In[33]:


data['PRODUCTCODE'].isna().sum()


# In[34]:


data['CUSTOMERNAME'].unique()


# In[35]:


data['CUSTOMERNAME'].isna().sum()


# In[36]:


# Step 1: Count the occurrences of each customer name
customer_counts = data['CUSTOMERNAME'].value_counts()

# Filter to find repeated customer names
repeated_customers = customer_counts[customer_counts > 1].index

# Step 2: Group by CUSTOMERNAME and aggregate the purchases and average quantities
repeated_customers_data = data[data['CUSTOMERNAME'].isin(repeated_customers)]

# Assuming there are columns 'PRODUCTNAME' and 'QUANTITYORDERED'
grouped_data = repeated_customers_data.groupby('CUSTOMERNAME').agg({
    'PRODUCTLINE': lambda x: ', '.join(x.unique()),  # Join unique product names
    'QUANTITYORDERED': 'mean'  # Calculate the average quantity ordered
}).reset_index()

# Rename columns for clarity
grouped_data = grouped_data.rename(columns={'PRODUCTLINE': 'Products Bought', 'QUANTITYORDERED': 'Average Quantity'})

# Output the result
grouped_data


# In[37]:


grouped_data.head(5)


# In[38]:


data['ADDRESSLINE2'].isna().sum()


# In[39]:


data = data.drop(columns=['ADDRESSLINE2'])


# In[40]:


data['CITY'].isna().sum()


# In[41]:


data['CITY'].unique()


# In[42]:


data['STATE'].isna().sum()


# In[43]:


data['COUNTRY'].isna().sum()


# In[44]:


data.info()


# In[45]:


data['TERRITORY'].unique()


# In[46]:


data['COUNTRY'].unique()


# In[47]:


# Time to fill the missing values of the State column using the data from the City and Country column

city_country_to_state = {
    ('NYC', 'USA'): 'NY',
    ('Reims', 'France'): 'Grand Est',
    ('Paris', 'France'): 'Île-de-France',
    ('Pasadena', 'USA'): 'CA',
    ('San Francisco', 'USA'): 'CA',
    ('Burlingame', 'USA'): 'CA',
    ('Lille', 'France'): 'Hauts-de-France',
    ('Bergen', 'Norway'): 'Hordaland',
    ('Melbourne', 'Australia'): 'Victoria',
    ('Newark', 'USA'): 'NJ',
    ('Bridgewater', 'USA'): 'NJ',
    ('Nantes', 'France'): 'Pays de la Loire',
    ('Cambridge', 'USA'): 'MA',
    ('Helsinki', 'Finland'): 'Uusimaa',
    ('Stavern', 'Norway'): 'Vestfold og Telemark',
    ('Madrid', 'Spain'): 'Community of Madrid',
    ('Osaka', 'Japan'): 'Osaka',
    ('Toronto', 'Canada'): 'Ontario',
    ('Milan', 'Italy'): 'Lombardy',
    ('Copenhagen', 'Denmark'): 'Capital Region of Denmark',
    ('Brussels', 'Belgium'): 'Brussels',
    ('Manila', 'Philippines'): 'Metro Manila',
    ('Munich', 'Germany'): 'Bavaria',
    ('Zurich', 'Switzerland'): 'Zurich',
    ('Dublin', 'Ireland'): 'Dublin',
     ('Salzburg', 'Austria'): 'Salzburg',
    ('Liverpool', 'UK'): 'Merseyside',
    ('Lule', 'Sweden'): 'Norrbotten',
    ('Singapore', 'Singapore'): 'Singapore',  
    ('Lyon', 'France'): 'Auvergne-Rhône-Alpes',
    ('Torino', 'Italy'): 'Piedmont',
    ('Boras', 'Sweden'): 'Västra Götaland',
    ('Versailles', 'France'): 'Île-de-France',
    ('Kobenhavn', 'Denmark'): 'Capital Region',
    ('London', 'UK'): 'Greater London',
    ('Toulouse', 'France'): 'Occitanie',
    ('Barcelona', 'Spain'): 'Catalonia',
    ('Bruxelles', 'Belgium'): 'Brussels-Capital Region',
    ('Oulu', 'Finland'): 'Northern Ostrobothnia',
    ('Graz', 'Austria'): 'Styria',
    ('Makati City', 'Philippines'): 'Metro Manila',
    ('Marseille', 'France'): "Provence-Alpes-Côte d'Azur",
    ('Koln', 'Germany'): 'North Rhine-Westphalia',
    ('Gensve', 'Switzerland'): 'Geneva',
    ('Reggio Emilia', 'Italy'): 'Emilia-Romagna',
    ('Frankfurt', 'Germany'): 'Hesse',
    ('Espoo', 'Finland'): 'Uusimaa',
    ('Manchester', 'UK'): 'Greater Manchester',
    ('Aaarhus', 'Denmark'): 'Central Denmark Region',
    ('Sevilla', 'Spain'): 'Andalusia',
    ('Strasbourg', 'France'): 'Grand Est',
    ('Oslo', 'Norway'): 'Oslo',
    ('Bergamo', 'Italy'): 'Lombardy',
    ('Charleroi', 'Belgium'): 'Wallonia',
}

# Function to fill missing STATE values based on CITY and COUNTRY
def fill_state(row):
    city_country_key = (row['CITY'], row['COUNTRY'])
    return city_country_to_state.get(city_country_key, row['STATE'])

# Apply the function to fill missing values in STATE column
data['STATE'] = data.apply(fill_state, axis=1)

# Verify the updated DataFrame
data.head(5)


# In[48]:


data['STATE'].isna().sum()


# In[49]:


data['TERRITORY'].isna().sum()


# In[50]:


data['TERRITORY'].unique()


# **EMEA:** Stands for Europe, the Middle East, and Africa. It is a geographical region that encompasses countries from Europe, the Middle East (Western Asia), and Africa.
# 
# **APAC:** Stands for Asia-Pacific. It is a geographical region that includes countries from Asia and the Pacific Ocean. This region typically covers countries from East Asia, Southeast Asia, South Asia, and Oceania.
# 
# **Japan** as a country does not fall under a broader regional acronym like EMEA or APAC. Instead, when categorizing territories or regions for business purposes, Japan is typically considered as its own distinct entity due to its unique cultural, economic, and geographical characteristics. Therefore, in the context of categorizing territories based on broader regional divisions, Japan would be listed separately rather than being grouped under a regional acronym.

# In[51]:


# Dealing with missing values in the Territory Column
country_to_territory = {
    'USA': 'Americas',        
    'France': 'EMEA',
    'Norway': 'EMEA',
    'Australia': 'APAC',
    'Finland': 'EMEA',
    'Austria': 'EMEA',
    'UK': 'EMEA',
    'Spain': 'EMEA',
    'Sweden': 'EMEA',
    'Singapore': 'APAC',
    'Canada': 'Americas',
    'Japan': 'Japan',
    'Italy': 'EMEA',
    'Denmark': 'EMEA',
    'Belgium': 'EMEA',
    'Philippines': 'APAC',
    'Germany': 'EMEA',
    'Switzerland': 'EMEA',
    'Ireland': 'EMEA',
}

# Function to fill missing TERRITORY values based on COUNTRY
def fill_territory(row):
    return country_to_territory.get(row['COUNTRY'], row['TERRITORY'])

# Apply the function to fill missing values in TERRITORY column
data['TERRITORY'] = data.apply(lambda row: fill_territory(row) if pd.isna(row['TERRITORY']) else row['TERRITORY'], axis=1)
data['TERRITORY'].unique()


# In[52]:


data['TERRITORY'].isna().sum()


# In[53]:


data.info()


# In[54]:


data['POSTALCODE'].isna().sum()


# Dataset Succesfull Cleaned

# In[55]:


data.columns


# In[56]:


data.sample(5)


# In[57]:


# Save the cleaned dataset to a CSV file
data.to_csv("cleaned_Sales_dataset.csv", index = False)
print ("Successful")


# In[ ]:




