# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 19:56:07 2023

@author: GOKULNATH
"""
import wbgapi as wb
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import sklearn
import seaborn as sns
import itertools as iter
from sklearn.datasets import make_blobs
from numpy import array, exp
df=pd.read_csv(r"E:\poster\World_Data_Indicators.csv")
df.head()
df.info()
df.shape
df.describe()

#Indicators to be chosen for analysis
economy = ['NE.IMP.GNFS.ZS','NY.GDP.MKTP.CD']
country = ["JPN","AUS",'BMU','LUX','IND','BRA','ARG','ESP','GBR','CHL']
climate=['EG.CFT.ACCS.RU.ZS','EG.CFT.ACCS.UR.ZS']
df_economy  = wb.data.DataFrame(economy, country, mrv=7)
df_climate  = wb.data.DataFrame(climate, country, mrv=7)
df_economy.columns = [f.replace('YR','') for f in df_economy.columns]      
df_economy=df_economy.stack().unstack(level=1)                             
df_economy.index.names = ['Country_Name', 'Year']                           
df_economy.columns                                                     
df_economy.fillna(0)
df_economy.head()
df_climate.columns = [f.replace('YR','') for f in df_climate.columns]      
df_climate=df_climate.stack().unstack(level=1)                             
df_climate.index.names = ['Country_Name', 'Year']                           
df_climate.columns                                                     
df_climate.fillna(0)
df_climate.head()
economy1=df_economy.reset_index()
economy2=economy1.fillna(0)
climate1=df_climate.reset_index()
climate2=climate1.fillna(0)
merged_data = pd.merge(economy2, climate2)
merged_data.head()
merged_data1 = merged_data.iloc[:,2:]
merged_data.iloc[:,2:] = (merged_data1-merged_data1.min())/ (merged_data1.max() - merged_data1.min())
merged_data.head()
merged_data2 = merged_data.drop('Country_Name', axis = 1)
k_clustering = KMeans(n_clusters=3, init='k-means++', random_state=0).fit(merged_data2)

#Clean fuels access and technologies access clustering in rural areas
sns.scatterplot(data=merged_data, x="Country_Name", y="EG.CFT.ACCS.RU.ZS", hue=k_clustering.labels_)
plt.legend(loc='lower right')
plt.show()

# Association between Total imports and Total GDP of a country(Brazil)
b=merged_data[(merged_data['Country_Name']=='BRA')]
txt = b.values
x, y = txt[:, 2], txt[:, 3]
plt.scatter(x, y,color="green")
plt.title('GDP vs Total Imports')
plt.ylabel('Total Imports')
plt.xlabel('Total GDP of a country')
plt.show()
    