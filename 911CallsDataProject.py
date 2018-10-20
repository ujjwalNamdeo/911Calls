
# coding: utf-8

# # 911 Calls data project

# #### For this capstone project we will be analyzing some 911 call data from Kaggle. The data contains the following fields:
# 
# lat : String variable, Latitude
# 
# lng: String variable, Longitude
# 
# desc: String variable, Description of the Emergency Call
# 
# zip: String variable, Zipcode
# 
# title: String variable, Title
# 
# timeStamp: String variable, YYYY-MM-DD HH:MM:SS
# 
# twp: String variable, Township
# 
# addr: String variable, Address
# 
# e: String variable, Dummy variable (always 1)

# In[3]:


# Importing numpy and pandas

import numpy as np
import pandas as pd


# In[6]:


#Importing visualization libraries and set %matplotlib inline.

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[7]:


# Read in the csv file as a dataframe called df

df = pd.read_csv('911.csv')


# In[9]:


# Checking the info() of the df

df.info()


# In[10]:


# Check the head of df

df.head()


# In[11]:


# The top 5 zipcodes for 911 calls

df['zip'].value_counts().head(5)


# In[13]:


# The top 5 townships (twp) for 911 calls

df['twp'].value_counts().head()


# In[14]:


# Taking a look at the 'title' column, how many unique title codes are there

df['title'].nunique()


# #  Creating new features

# #### In the titles column there are "Reasons/Departments" specified before the title code, using .apply() with a custom lambda expression to create a new column called "Reason" that contains this string value.

# In[15]:


df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])


# In[17]:


# The most common Reason for a 911 call based off of this new column

df['Reason'].value_counts()


# In[18]:


# Now using seaborn to create a countplot of 911 calls by Reason.

sns.countplot(x='Reason',data=df,palette='viridis')


# In[19]:


# Now let us begin to focus on time information. What is the data type of the objects in the timeStamp column?

type(df['timeStamp'].iloc[0])


# In[22]:


# These timestamps are still strings, Using pd.to_datetime to convert the column from strings to DateTime objects.

df['timeStamp'] = pd.to_datetime(df['timeStamp'])


# In[23]:


# Now grabbing specific attributes from a Datetime object by calling them, using .apply() to create 3 new columns called Hour, Month, and Day of Week
# And creating these columns based off of the timeStamp column.

df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
df['Month'] = df['timeStamp'].apply(lambda time: time.month)
df['Day of Week'] = df['timeStamp'].apply(lambda time: time.dayofweek)


# In[24]:


# Day of Week is an integer 0-6, Using the .map() with the dictionary to map the actual string names to the day of the week

dmap = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}


# In[25]:


df['Day of Week'] = df['Day of Week'].map(dmap)


# In[27]:


# Now using seaborn to create a countplot of the Day of Week column with the hue based off of the Reason column.

sns.countplot(x='Day of Week',data=df,hue='Reason',palette='viridis')

# To relocate the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[28]:


# Doing the same for Month:

sns.countplot(x='Month',data=df,hue='Reason',palette='viridis')

# To relocate the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[29]:


# It is missing some months! 9,10, and 11, creating a gropuby object called byMonth,
# where we group the DataFrame by the month column and use the count() method for aggregation.


byMonth = df.groupby('Month').count()
byMonth.head()


# In[31]:


# creating a simple plot off of the dataframe indicating the count of calls per month.

# Could be any column
byMonth['twp'].plot()


# In[32]:


# Using seaborn's lmplot() to create a linear fit on the number of calls per month and resetting the index to a column.

sns.lmplot(x='Month',y='twp',data=byMonth.reset_index())


# In[33]:


# Creating a new column called 'Date' that contains the date from the timeStamp column and 
# using apply along with the .date() method.

df['Date']=df['timeStamp'].apply(lambda t: t.date())


# In[34]:


# Using groupby in Date column with the count() aggregate and creating a plot of counts of 911 calls

df.groupby('Date').count()['twp'].plot()
plt.tight_layout()


# In[35]:


# Now recreating this plot but creating 3 separate plots with each plot representing a Reason for the 911 call

df[df['Reason']=='Traffic'].groupby('Date').count()['twp'].plot()
plt.title('Traffic')
plt.tight_layout()


# In[36]:


df[df['Reason']=='Fire'].groupby('Date').count()['twp'].plot()
plt.title('Fire')
plt.tight_layout()


# In[37]:


df[df['Reason']=='EMS'].groupby('Date').count()['twp'].plot()
plt.title('EMS')
plt.tight_layout()


# In[38]:


# Now creating heatmaps with seaborn and our data, restructuring the dataframe so that the columns become the Hours and 
# the Index becomes the Day of the Week, combining groupby with an unstack method.

dayHour = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
dayHour.head()


# In[39]:


#  Now creating a HeatMap using this new DataFrame.

plt.figure(figsize=(12,6))
sns.heatmap(dayHour,cmap='viridis')


# In[40]:


# Now creating a clustermap using this DataFrame.

sns.clustermap(dayHour,cmap='viridis')


# In[41]:


# Now repeating these same plots and operations, for a DataFrame that shows the Month as the column.

dayMonth = df.groupby(by=['Day of Week','Month']).count()['Reason'].unstack()
dayMonth.head()


# In[42]:


plt.figure(figsize=(12,6))
sns.heatmap(dayMonth,cmap='viridis')


# In[43]:


sns.clustermap(dayMonth,cmap='viridis')

