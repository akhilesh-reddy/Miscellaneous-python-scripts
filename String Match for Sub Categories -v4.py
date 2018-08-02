
# coding: utf-8

# ## Grouping of brands under respective Advertisers

# ### Objective:
# * To group the brands under their respective Advertisers

# ### Steps followed in the Algorithm
# 
# &nbsp;1.Trim the imported data <br/>
# &nbsp;2.Find the length of the Brands names and divide them into 2 subsets (>3 char),(<=3 char) for ease of implementation<br/>
# &nbsp;3.Perform a cross join on brand name within a sb category and scale it through looping<br/>
# &nbsp;&nbsp;&nbsp;&nbsp;a.Create a flag if one brand is present in the joined column <br/>
# &nbsp;&nbsp;&nbsp;&nbsp;b.Identify the brands that have more than one mapping within a sub category to identify the general advertisers<br/>
# &nbsp;4.Perform a **Similar** function on the resultant dataset and remove the exact matches and get the grouped brands under their advertisers<br/>
# &nbsp;5.Use find function to select the appropriate records for the respective advertisers<br/>
# &nbsp;6.Include the advertisers that had name length <=3 and had unique brand names

# In[2]:

## Importing the necessary libraries
import pandas as pd
import numpy as np


# In[9]:

## Creating a function "Similar" to be used in the subsequent process

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_fnc(a,b):
    return 1 if a in b else 0


## 1.Trim the imported data
## 2.Find the length of the Brands names and divide them into 2 subsets (>3 char),(<=3 char) for ease of implementation

    ## Importing and treating the raw data
df=pd.read_csv("Data for String_match sub_catgs.csv")

    ## Trimming and identifying the length of the brand names
catg_col = df.select_dtypes(['object'])
df[catg_col.columns] = catg_col.apply(lambda x: x.str.strip())
df['length'] = df['Brand'].apply(lambda x: len(x))

df1 = df[df['length']>3].drop(['length'],axis=1)

list_sub_cats = df1['Sub Category'].unique()
final_sub_catg = pd.DataFrame({'Sub Category': list_sub_cats})
cnt = final_sub_catg.shape[0]

df1['key'] = 1


# In[8]:

## Data with advertisers having name length <=3
df2 = df[df['length']<=3].drop(['length'],axis=1)


# In[4]:

## 3.Perform a cross join on brand name within a sb category and scale it through looping

k={}
for i in range(0,cnt):
    x=final_sub_catg.loc[i]['Sub Category']
    temp2 = df1[df1['Sub Category'] == x]
    temp2 = temp2.reset_index(drop=True)
    temp_merged = pd.merge(temp2, temp2, on=['key'])
    temp_merged1 = temp_merged.drop(['Sub Category_y','key'],axis=1)
    temp_merged1 = temp_merged1.rename(columns={'Sub Category_x': 'Sub Category'})
    row_cnt = temp_merged1.shape[0]
    k[i]=temp_merged1
    for j in range(0,row_cnt):
        if k[i].loc[j][1] in k[i].loc[j][2]:
                k[i].loc[j,'find_value']= 1
        else:
                k[i].loc[j,'find_value']= 0


# In[5]:

## Including all dataframes into one dataframe
test_list=[]
for i in range(0,cnt):
    x=k[i]
    test_list.append(x)
append_df=pd.concat(test_list)


# In[6]:

## Identifying the records which are mapped to more than one brand with a sub category,brand combination
aggt_values = append_df.groupby(['Sub Category','Brand_x'],as_index = False)['find_value'].sum()
req_recds = aggt_values[aggt_values['find_value'] >1]


# In[46]:

## 4.Perform a **Similar** function on the resultant dataset and remove the exact matches and 
##   get the grouped brands under their advertisers

inter_1 = pd.merge(req_recds,append_df,on = ['Sub Category','Brand_x'], how = 'inner')
inter_2 = inter_1.drop(['find_value_x','find_value_y'],axis = 1)
unique_rec_inter1 = inter_1
inter_2['Value'] = inter_2.apply(lambda row: similar(row['Brand_x'], row['Brand_y']), axis=1)
inter_3 = inter_2[inter_2['Value'] != 1]

## 5.Use find function to select the appropriate records for the respective advertisers
def find_fnc(a,b):
    return 1 if a in b else 0

## Identifying the matches for the appropriate brands
inter_3['find_fnc_value'] = inter_3.apply(lambda row: find_fnc(row['Brand_x'], row['Brand_y']), axis=1)
inter_5 = inter_3[inter_3['find_fnc_value'] != 0]

## All the brands with in subcategories that have a product name
inter_5

## 6.Include the advertisers that had name length <=3 and had unique brand names
## List of brands that have a brand_name
brnds_with_prdt_names = inter_5.drop(['Brand_y','Value','find_fnc_value'],axis=1)
brnds_with_prdt_names_1 = brnds_with_prdt_names.drop_duplicates()

## Total brand list
# df1
# inter_1


# In[103]:

unique_rec_inter2=unique_rec_inter1[unique_rec_inter1['find_value_y'] == 1]
unique_rec_inter3 = unique_rec_inter2.drop(['Brand_x','find_value_x','find_value_y'],axis=1)

## Performing an exception join to identify the advertisers that did not have further brand names
final_merge = pd.merge(df1,unique_rec_inter3,left_on = ['Sub Category','Brand'], right_on = ['Sub Category','Brand_y'], how ='left')


# In[118]:

k=final_merge[final_merge['Brand_y'].isnull()]
k['Brand name'] = k['Brand']
# df2['Brand name'] = df2['Brand'] ## Should not be run multiple times
unique_brnds = k.drop(['key','Brand_y'],axis=1)
unique_brnds_pdt_names = inter_5.drop(['Value','find_fnc_value'],axis=1)


# In[119]:

## Renaming the columns to append the data into one dataframe
unique_brnds = unique_brnds.rename(columns={'Brand': 'Advertiser'})
unique_brnds_pdt_names = unique_brnds_pdt_names.rename(columns={'Brand_x': 'Advertiser','Brand_y' : 'Brand name'})
df2 = df2.rename(columns={'Brand': 'Advertiser'})

## Appending all the datasets into one dataframe
final_list = pd.concat([unique_brnds_pdt_names,unique_brnds,df2])
sorted_final_list = final_list.sort_values(by=['Sub Category'], ascending=[True])
sorted_final_list = sorted_final_list.reset_index(drop=True)
sorted_final_list.to_csv('final_advertiser_list.csv')


# In[3]:

# Check
# sorted_final_list[sorted_final_list['Advertiser'] == 'KELLOGGS']


# In[5]:

## Need to treat the resultant excel for the exceptions
## Advertiser names have to be further treated
    ## Eg: In kelloggs, there is also Kelloggs special k listed as advertiser due to the detail included in ti further
    ##  Need to rename Kelloggs special K under Kellogs as Kelloggs and finally duplicates have to removed

