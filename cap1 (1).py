#!/usr/bin/env python
# coding: utf-8

# Import numpy and pandas

# In[1]:


import numpy as np


# In[2]:


import pandas as pd


# Import visualization libraries and set %matplotlib inline.

# In[3]:


import matplotlib.pyplot as plt 


# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')


# Read in the csv file as a dataframe called df

# In[5]:


df = pd.read_csv(r'C:\Users\abi3c\Pictures\911\911.csv')


# 
# Check the info() of the df

# In[6]:


df


# Check the head of df

# In[7]:


df.head()


# In[ ]:





# # Basic Questions¶

# What are the top 5 zipcodes for 911 calls?

# In[8]:


df['zip'].head(5)


# In[ ]:





# 
# What are the top 5 townships (twp) for 911 calls?

# In[9]:


df['twp'].head(5)


# In[ ]:





# Take a look at the 'title' column, how many unique title codes are there?

# In[10]:


df['title'].nunique()


# In[ ]:





# 
# # Creating new features

# 
# In the titles column there are "Reasons/Departments" specified before the title code. These are EMS, Fire, and Traffic. Use .apply() with a custom lambda expression to create a new column called "Reason" that contains this string value.
# 
# For example, if the title column value is EMS: BACK PAINS/INJURY , the Reason column value would be EMS.

# In[11]:


df['reason'] = df['title'].apply(lambda reason: reason.split(':')[0])


# In[12]:


df['reason'].head()


# In[ ]:





# What is the most common Reason for a 911 call based off of this new column?

# In[13]:


df['reason'].value_counts()


# In[ ]:





# Now use seaborn to create a countplot of 911 calls by Reason.

# In[14]:


import seaborn as sns


# In[15]:


sns.countplot(df['reason'])
sns.set_style('whitegrid')


# In[16]:


df.head()


# Now let us begin to focus on time information. What is the data type of the objects in the timeStamp column?

# In[17]:


type('timeStamp')


# In[ ]:





# 
# You should have seen that these timestamps are still strings. Use pd.to_datetime to convert the column from strings to DateTime objects.

# In[18]:



df['timeStamp']= pd.to_datetime(df['timeStamp'])
df.head()


# In[ ]:





# 
# You can now grab specific attributes from a Datetime object by calling them. For example:
# 
# time = df['timeStamp'].iloc[0]
# time.hour
# 
# You can use Jupyter's tab method to explore the various attributes you can call. Now that the timestamp column are actually DateTime objects, use .apply() to create 3 new columns called Year, Month, and Day of Week. You will create these columns based off of the timeStamp column, reference the solutions if you get stuck on this step.

# In[19]:


#just trying
df['timeStamp'].iloc[0].hour


# In[20]:


df['year'] = df['timeStamp'].apply(lambda x : x.year)


# In[21]:


df['month'] = df['timeStamp'].apply(lambda x : x.month)


# In[22]:


df['day of week'] = df['timeStamp'].apply(lambda x : x.dayofweek)


# In[ ]:





# In[ ]:





# Notice how the Day of Week is an integer 0-6. Use the .map() with this dictionary to map the actual string names to the day of the week:
# 
# dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

# In[24]:


# just testing
df['day of week'].map( {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'})


# In[25]:


df['week'] = df['day of week'].map( {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'})


# In[26]:


df.head()


# In[27]:


df['month'].unique()


# In[ ]:





# Now use seaborn to create a countplot of the Day of Week column with the hue based off of the Reason column.

# In[28]:


import seaborn as sns
sns.countplot( df['week'],hue = df['reason'])
plt.legend(bbox_to_anchor=(0.75,0.5, 0.5, 0.5))


# In[ ]:





# In[ ]:





# 
# Now do the same for Month:

# In[29]:


import seaborn as sns


# In[30]:


sns.countplot(df['month'],hue = df['reason'])
plt.legend(bbox_to_anchor = (1,1))


# In[ ]:





# In[ ]:





# 
# Did you notice something strange about the Plot?
# 
# You should have noticed it was missing some Months, let's see if we can maybe fill in this information by plotting the information in another way, possibly a simple line plot that fills in the missing months, in order to do this, we'll need to do some work with pandas...
# 
# Now create a gropuby object called byMonth, where you group the DataFrame by the month column and use the count() method for aggregation. Use the head() method on this returned DataFrame.

# In[31]:


byMonth = df.groupby('month').count()
byMonth.head()


# In[32]:


df.head()


# In[ ]:





# 
# Now create a simple plot off of the dataframe indicating the count of calls per month.

# In[33]:


plt.plot( byMonth['twp'])


# In[34]:


byMonth.head()


# In[ ]:





# Now see if you can use seaborn's lmplot() to create a linear fit on the number of calls per month. Keep in mind you may need to reset the index to a column.

# In[35]:



byMonth.reset_index()


# In[36]:


#this plot gives the month VS twp . Reset_index is just needed for the leveling both of them . 
sns.lmplot(x='month',y='twp',data=byMonth.reset_index())


# In[ ]:





# 
# Create a new column called 'Date' that contains the date from the timeStamp column. You'll need to use apply along with the .date() method.

# In[37]:


df.head()


# In[38]:


df['date'] = df['timeStamp'].apply(lambda x : x.date())


# In[39]:


df.head()


# In[ ]:





# Now groupby this Date column with the count() aggregate and create a plot of counts of 911 calls.

# In[40]:


df['date'].count()


# In[41]:


df.groupby('date').count()['twp'].plot()
plt.tight_layout()


# In[83]:





# In[ ]:





# 
# Now recreate this plot but create 3 separate plots with each plot representing a Reason for the 911 call

# In[42]:


df[df['reason']=='EMS'].groupby('date').count()['twp'].plot()
plt.tight_layout()
plt.title('EMS')


# In[ ]:





# In[43]:


df[df['reason']=='Fire'].groupby('date').count()['twp'].plot()
plt.tight_layout()
plt.title('Fire')


# In[44]:


df[df['reason']=='Traffic'].groupby('date').count()['twp'].plot()
plt.tight_layout()
plt.title('Traffic')


# In[ ]:





# In[ ]:





# 
# Now let's move on to creating heatmaps with seaborn and our data. We'll first need to restructure the dataframe so that the columns become the Hours and the Index becomes the Day of the Week. There are lots of ways to do this, but I would recommend trying to combine groupby with an unstack method. Reference the solutions if you get stuck on this!

# In[45]:


df.head()


# In[46]:


df['hour'] = df['timeStamp'].apply(lambda x : x.hour)


# In[48]:


df.head()


# In[64]:


data = df.groupby(by =['day of week','hour']).count()['reason'].unstack()


# In[65]:


data.head()


# In[ ]:





# Now create a HeatMap using this new DataFrame.

# In[66]:


sns.heatmap(data)


# In[ ]:





# In[ ]:





# Now create a clustermap using this DataFrame.

# In[80]:


sns.clustermap(data,cmap = 'cividis')


# In[ ]:





# Now repeat these same plots and operations, for a DataFrame that shows the Month as the column.

# In[70]:


data1 = df.groupby(['month','day of week']).count()['reason'].unstack()


# In[71]:


data1.head()


# In[75]:


sns.heatmap(data1,cmap= 'viridis')


# In[79]:


sns.clustermap(data1,cmap= 'magma')


# In[ ]:





# 
# Continue exploring the Data however you see fit!
# 
# # Great Job!

# * Thanks
