from gettext import install
from re import M
import pandas as pd
import csv
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
marketing= pd.read_csv(r'C:\Users\user\Downloads\KAG_conversion_data.csv')
print(marketing.head())
print(marketing.describe())
print(marketing.info())

# Plot for frequency of people in each age group and gender
fig, ax = plt.subplots()
marketing['age'].value_counts().plot(ax=ax, kind='bar', xlabel='Age', ylabel='Frequency')
plt.show()
sns.countplot(x=marketing['gender'])
plt.show()

#creating dataframe for correlation analysis
marketing_cor=marketing[['revenue','Impressions','Clicks', 'Total_Conversion', 'Spent', 'profit', 'age', 'gender']]
plt.suptitle("Correlation between variables", y=1.05,weight='bold')
sns.pairplot(marketing_cor, height=1.5)
plt.show()

# Plot for CTR with Age & Gender
sns.barplot(x=marketing['age'],y=marketing['CTR'],hue=marketing.gender)
plt.show()
# Plot for Conversion & Click to Impression with Age & Gender
sns.scatterplot(x = marketing['Clicks'], y = marketing['Total_Conversion'], hue=marketing["age"], style=marketing["gender"])
plt.show()
#plot the new variables with age, gender, campaign
plt.rcParams['figure.figsize']=(10,6)
a = pd.pivot_table(data=marketing_cor, index='age',values=['revenue','Spent', 'profit'], aggfunc='mean').plot(kind='bar')
plt.show()

marketing2 = marketing.groupby(['age','gender'],as_index=False)[['interest','Impressions','Spent','Total_Conversion','Clicks']].mean()

age1 = marketing.groupby(['age'],as_index=False)[['interest','Impressions','Spent','Total_Conversion','Clicks']].mean()
print(age1)
gender1 = marketing.groupby(['gender'],as_index=False)[['interest','Impressions','Spent','Total_Conversion','Clicks']].mean()
print(gender1)
campaign_id_1=marketing.groupby("fb_campaign_id")[["interest","Impressions","Spent","Total_Conversion","Clicks"]].mean()
print(campaign_id_1)

#heatmap
plt.figure(figsize=(18,6))
x=sns.heatmap(marketing_cor.corr(),annot=True ,fmt=".2f",cmap="coolwarm")
plt.show()

#unique campaigns
camp_id_unique = len(marketing["xyz_campaign_id"].unique())
print(camp_id_unique)
# construct the campaign data
camp_id_list = marketing["xyz_campaign_id"].unique()
camp_data = {'xyz_campaign_id': [], 'Impressions': [], 'Clicks': [], 'Spent': [], 'Total_Conversion': [], 'Approved_Conversion': []}
for id in camp_id_list:
    camp_data['xyz_campaign_id'].append(id)
    camp_data['Impressions'].append(sum(marketing[marketing['xyz_campaign_id'] == id]['Impressions']))
    camp_data['Clicks'].append(sum(marketing[marketing['xyz_campaign_id'] == id]['Clicks']))
    camp_data['Spent'].append(sum(marketing[marketing['xyz_campaign_id'] == id]['Spent']))
    camp_data['Total_Conversion'].append(sum(marketing[marketing['xyz_campaign_id'] == id]['Total_Conversion']))
    camp_data['Approved_Conversion'].append(sum(marketing[marketing['xyz_campaign_id'] == id]['Approved_Conversion']))
camp_data = pd.DataFrame(camp_data)
print(camp_data)

camp_data['CPM']= camp_data['Spent']/camp_data['Impressions']*1000
camp_data['CPC']= camp_data['Spent']/camp_data['Clicks']
camp_data['CPA']= camp_data['Spent']/camp_data['Total_Conversion']
camp_data['CTR']= (camp_data['Clicks']/camp_data['Impressions'])*100
camp_data['CVR']= (camp_data['Approved_Conversion']/camp_data['Total_Conversion'])*100
camp_data['revenue']=camp_data['Approved_Conversion']*100
camp_data['profit']= camp_data.revenue-camp_data.Spent
camp_data

# metrics by campaign
plt.figure(figsize=(5,5))
a = pd.pivot_table(data=camp_data, index='xyz_campaign_id',values=['CPA','CPC']).plot(kind='bar')
plt.suptitle("CPA vs CPC by campaign")
plt.show()

a = pd.pivot_table(data=camp_data, index='xyz_campaign_id',values=['revenue','profit']).plot(kind='bar')
plt.suptitle("Revenue vs Profit by campaign")
plt.show()

a = pd.pivot_table(data=camp_data, index='xyz_campaign_id',values=['Total_Conversion','Approved_Conversion']).plot(kind='bar')
plt.suptitle("Total_Conversion vs Approved_Conversion by campaign")
plt.show()
