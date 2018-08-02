
# coding: utf-8

# <div style="display:block">
#     <div style="width: 20%; display: inline-block; text-align: left;">
#         <img src="http://discoverycorp.wpengine.com/wp-content/uploads/2014/09/DISC-COMM-pos-4c.png" style="height:75px; margin-left:0px" />
#     </div>
#         <div style="width: 59%; display: inline-block">
#                 <h1  style="text-align: center">Psychographic Compatibility Score Computation  (MRI - NBI)</h1>
#         <div style="width: 100%; text-align: center; display: inline-block;"><i>Author:</i> <strong>Akhilesh N</strong>
#         <i>Created: </i> June 7th, 2017</time>
#         </div>
#     </div>
#     <div style="width: 17%; display: inline-block; text-align: right;">
#         <img src="http://upload.wikimedia.org/wikipedia/en/0/0c/Mu_Sigma_Logo.jpg" style="height:75px; margin-left:0px" />
#     </div>
#     <div style="width: 20%; text-align: right; display: inline-block;">
#         <div style="width: 100%; text-align: left; display: inline-block;">           
#         </div>
#     </div>
# </div>

# In[1]:

from IPython.display import HTML

HTML('''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the code."></form>''')


# # Objective:
# To calculate the Psychographic Compatibility Score between Networks and the relevant advertisers

# ## Key points considered in the analysis:
# 
# * Demographics : Adult 25-54
# * Time period : Q4 2016
# * Networks considered : TLC, E!, Bravo, Lifetime, HGTV, Food
# 

# ## Observations:
# #### 1.Pain Relief : Bayer Corporation
# 
# * On calculating the Compatibility Score between Brands and networks for Pain Relief Sub Category, we have observed that Bayer is highly Compatible with TLC
# 	
# * To further validate this finding, we have looked into the Revenue of Bayer in TLC and have seen an exponential increase of spend by Bayer in TLC
# 
# * This might be due to their realization that TLC is a best fit for their which is in line with our findings
# 
# #### 2.Holes 
# * Further in case of GEICO(Hole for TLC), a very low compatibility score can be observed which could have triggered their exit from TLC
# 
# #### Discovery and ID
# Beer and Malt based beverages : ANHEUSER-BUSCH
# 
# * ANHEUSER-BUSCH has increased its spend in Discovery by 5% from 2.9 MM to 3.06MM till present and by 62% in ID from 500 K to 900 K
# * Following the merger of SABMiller and AB-inbev, Miller Brewing CO has started spending a lot (~$2.5 MM in Discovery Channel for Q3 2017(might be due to the decision of AB inbev management)\
# 
# <b>Opportunity:<b>
# * Opportunity for TLC is that Miller Lite has a higher compatibility Score with TLC than ID and Discovery and can be used as a leverage point to invest more in TLC given their inclination to spend in Discovery Networks
# 
# Although the above might be influenced by multiple other factors, it stands relevant in giving us a unique signal to approach the Advertisers
# 
# 

# ### Use cases of the Analysis:
# * Favorable Brands for TLC can be selected based on Compatibility Score and Psychographics can be used aas supporting points during the negotiations(This can be obtained using the excel)
# * Talks for retaining the Brands can be strengthened using the Psychographics Results
# 

# ## Approach followed:
# 
# ### 1.Identification of Primary Psychographic Profiles for the Networks
# * I2M(PR)[Index to be considered while demogs are considered] has been extracted for each network for different Psychographics from Lake 5 front end
# * Psychographic Segments in which the selected network beats the competition have been selected as the primary Psychographic segments
# 
# ### 2.Identification of Primary Psychographic Profiles for the Brands
# * Each PersonID has been mapped to corresponding psychographic segment using MRI-NPM Fusion data
# * Distribution of audience across each segment has been analyzed at a sub-category and brand level
# * For a product, segments that are over indexing(Percentage distribution of a particular segment for a product is greater than the average percentage dist at a sub-category level) have been considered as the Primary Pscyhographics for the brands 
# 
# ### 3.Calculation of Compatibility Score
# * A comparison will be done between primary audience psychographics of a network and the brand
# * Compatibility Matrix will be calculated for each network and brand based on the number of matches between the primary psychographics of the network and the brand
# * Importance of a Network for an advertiser or importance of an advertiser for a network can be comprehended using the compatibility matrix

# ## Following are the Codes involved in the analysis
# #### Note : To Skip the code below please click on the Link [Skip](#skip)

# ### 1.Identification of Primary Psychographic Profiles for the Networks

# #### Primary Psychographic segments have been ranked based on the I2M(PR) index

# In[2]:

import pandas as pd
import numpy as np


# In[5]:

# For ranking
c=pd.read_csv("Collated data for Network Psychographics-all 3 networks.csv")
c["rank"] = c.groupby(["Demo","Network","Type of Segment","Segment"])["C3_I2M (PR)"].rank(method='dense', ascending=False)

#Primary Segments for each network
nwt_psyc=c[c["rank"].isin(['1','2'])]
nwt_psyc=nwt_psyc.drop(nwt_psyc.columns[5:15],axis=1)
# c.to_csv('Psychographics of Nets with ranks-2.csv')
nwt_psyc=nwt_psyc.rename(columns = {'Type of Segment' : 'Type_segments'})


# ### 3.Calculation of Compatibility Score

# #### Import the Primary Psychographics for both Networks and Brands

# In[8]:

brnd_psyc = pd.read_csv("Primary Psychographics for Brands -3.csv")
mri_definitions= pd.read_csv("Data Dictionary.csv",encoding = "ISO-8859-1")
relevant_psych_catg = pd.read_csv("Relevant Psychographic segments for Categories.csv")
# spend_data = pd.read_csv("Spend Data of the Advertisers - v3.csv")


# #### Removing the lead and trial spaces from all the values in the data imported

# In[9]:

nwt_psyc_col = nwt_psyc.select_dtypes(['object'])
brnd_psyc_col = brnd_psyc.select_dtypes(['object'])
mri_definitions_col = mri_definitions.select_dtypes(['object'])
relevant_psych_catg_col = relevant_psych_catg.select_dtypes(['object'])
# spend_data_col = spend_data.select_dtypes(['object'])

nwt_psyc[nwt_psyc_col.columns] = nwt_psyc_col.apply(lambda x: x.str.strip())
brnd_psyc[brnd_psyc_col.columns] = brnd_psyc_col.apply(lambda x: x.str.strip())
mri_definitions[mri_definitions_col.columns] = mri_definitions_col.apply(lambda x: x.str.strip())
relevant_psych_catg[relevant_psych_catg_col.columns] = relevant_psych_catg_col.apply(lambda x: x.str.strip())
# spend_data[spend_data_col.columns] = spend_data_col.apply(lambda x: x.str.strip())


# In[224]:

# spend_data['Sub Category']=spend_data['Sub Category'].str.title()
# spend_data['Category']=spend_data['Category'].str.title()


# In[225]:

# temp = spend_data.loc[(spend_data['Sub Category']== 'Pain Relief')]
# temp


# #### Data treatment on the imported datasets

# In[10]:

# Merging both the datasets to identify the compatibility from both sides
merged = pd.merge(nwt_psyc, brnd_psyc, on=['Demo','Type_segments', 'Segment'], how='inner')

# Assigning weights to the relevant Psychographics
merged1 = pd.merge(merged, relevant_psych_catg, on=['Type_segments', 'Category'], how='inner')
merged1['Sub Category']=merged1['Sub Category'].str.title()
merged1['Category']=merged1['Category'].str.title()

# Removing unwanted columns
merged2 = merged1.drop(['rank_x','perc_sub_catg','perc_product','indices','rank_y'], axis=1)


# In[11]:

merged2.head()


# #### Calculation of the Compatibility Score after aggregation

# In[12]:

# Calculating the weights after aggregation
aggt_merged = merged2.groupby(['Demo','Network','Category','Sub Category','Brand','Group'],as_index = False)['Weight'].sum()

# Ranking the Top Networks and Brands based on the Compatibility Score
aggt_merged['rank_brand'] = aggt_merged.groupby(['Demo','Network','Category','Sub Category','Group'])['Weight'].rank(method='dense', ascending=False)
aggt_merged['rank_network'] = aggt_merged.groupby(['Demo','Network','Category','Sub Category','Brand'])['Weight'].rank(method='dense', ascending=False)


# #### Identifying the Target Advertisers for TLC and mapping data definitions

# In[13]:

target=aggt_merged[(aggt_merged['rank_network'].isin([1,2,3])) & (aggt_merged['Group'].isin(['DISCOVERY','TLC','ID']))]
target = target.drop(['rank_brand'],axis = 1)

# Observing the Psychographics that got mapped for each brand with TLC
merged3 = pd.merge(target, merged2, on=['Demo','Network','Category', 'Sub Category','Brand','Group'], how='inner')
deliverable = pd.merge(merged3, mri_definitions, on=['Type_segments','Segment'], how='inner')
deliverable1 = deliverable.drop(['Network'],axis = 1)


# In[14]:

# QC with the original data
aggt_merged_test = aggt_merged[aggt_merged['Demo']== 'A']
# aggt_merged_test['Demo'].unique()


# <a name="skip">
# </a>

# In[231]:

# temp = merged3.loc[(merged3['Category'] == 'Alcohol') & (merged3['Sub Category'] == 'Beer And Malt Based Beverages')]


# ## Visualizing the output for the Compatibility Scores through a Compatibility Matrix

# #### Note : Sub Category can be searched by typing manually 

# In[244]:

import ipywidgets as widgets
from ipywidgets import interactive
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display
get_ipython().magic('matplotlib inline')

fig_size = [20,7]
plt.rcParams["figure.figsize"] = fig_size


# In[245]:

items_category = sorted(aggt_merged_test['Category'].unique().tolist())
items =sorted(aggt_merged_test['Sub Category'].unique().tolist())
brands =sorted(deliverable['Brand'].unique().tolist())


# In[246]:

search_text = widgets.Text(description = 'Type in Network') 
search_result = widgets.Select(description = 'Select Sub Category')

def search_action(sender):
    phrase = search_text.value
    heat=aggt_merged_test[aggt_merged_test['Network']== phrase]
    items = sorted(heat['Sub Category'].unique().tolist())
    with search_result.hold_trait_notifications():
        search_result.options = items
        
def view(Sub_Category=''):
            phrase = search_text.value
            z=aggt_merged_test[(aggt_merged_test['Network']== phrase) & (aggt_merged_test['Sub Category']==Sub_Category)]
#             spend_data1=spend_data[(spend_data['Network']== phrase) & (spend_data['Sub Category']==Sub_Category)]
#             y1=target[(target['Sub Category']==Sub_Category) & (target['Network']== phrase)]
#             sorted_spend = spend_data1.sort_values(by=['YoY Revenue'], ascending=[False])
            #sorted_target = y1.sort_values(by=['rank_network'], ascending=[True])
            x=z.pivot("Group","Brand","Weight")
            a=sns.heatmap(x,linewidths=.5,annot=True,annot_kws={"size": 15})
            plt.yticks(rotation=0)
            plt.show(a)
#             display('Spend Data of the Advertisers that are present in Nielsen data',sorted_spend)
#             display('Target Advertisers',y1)
            

search_text.on_submit(search_action)
display(search_text)
interactive(view, Sub_Category=search_result)


# In[235]:

def view1(Brand=''):       
            z=deliverable[deliverable['Brand']==Brand]
            z1 = z.drop(['Brand','Category','Group','Category','Sub Category','Weight_x'],axis = 1)
            sorted_z1 = z1.sort_values(by=['rank_network','Network'])
            display('Mapped Psychographics',sorted_z1)


# #### Mapped Psychographics for a particular Brand can be identified from the below table 

# In[236]:

w1 = widgets.Select(options=brands,description = 'Brand')
interactive(view1, Brand=w1)


# In[237]:

brnd_psyc.head()


# In[11]:

#Renaming the columns to facilitate integration of front end with back end
deliverable2=deliverable1.rename(columns={'Demo':'Demographics','Weight_x':'Cumulative_weight','Weight_y':'Segment_weight'})
aggt_merged2=aggt_merged.rename(columns={'Demo':'Demographics'})

nwt_psyc2=nwt_psyc[nwt_psyc['Group'].isin(['DISCOVERY','TLC','ID'])]
nwt_psyc2=nwt_psyc2.drop(['Group'],axis=1)
nwt_psyc2=nwt_psyc2.rename(columns={'Demo':'Demographics','Type_segments':'Type_of_Segment','rank':'Ranking_based_on_Index'})


# Data for Copmatibility Matrix in Excel
aggt_merged2.to_csv('Matrix_data-VF.csv')

# Spend Data
# spend_data.to_csv('spend_Data-VF.csv')

# Data for Compatibility Score tab
deliverable2.to_csv('Compatibility Score-VF.csv')

# Primary Psychographics for Networks
nwt_psyc2.to_csv('Primary Psychographics for Nets-VF.csv')

#Primary Pscyhographics for Brands
brnd_psyc.to_csv('Primary Psychoraphics for Brands-VF.csv')


# In[8]:

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# In[23]:

similar("Coors","Coors light")


# ### 4.Challenges:
# * Delay in Collation of data from lake 5 front end due to high execution time
# * Scaling the process for multiple networks would be a challenge given the dependency on lake 5 front end

# ### 5.Next Steps:
# * Findings to be tested across quarters to check the validity across time
# * Use the signals generated from this module to gain directions while proceeding with other modules
# 
