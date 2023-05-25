# -*- coding: utf-8 -*-
"""Data_extraction_part.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G0_Z2Hf7NHRGbGkleZk_8pZk0eN_tYOw
"""

#clone with phonepe-pulse github repo
!git clone https://github.com/phonepe/pulse.git

# overall india - transaction data based on instruments
import json
import pandas as pd

# importing transaction data of year [2018-2022]
# Create an empty list to store the dataframes
df_transaction = []

# list of years to be iterated
years = ['2018', '2019', '2020', '2021', '2022']

# Loop through all the years files in the directory
for year in years:
    for i in range(1, 5):
        # Construct the file path
        file_path = f'/content/pulse/data/aggregated/transaction/country/india/{year}/{i}.json'

        # Load the data from the file
        with open(file_path) as f:
            data = json.load(f)

        # Create a dataframe from the transaction data
        df = pd.json_normalize(data['data']['transactionData'], 'paymentInstruments', ['name'])

        # drop the unnecessary columns by mentioning its axis
        df = df.drop('type', axis=1)

        # Add the quarter column with the value of i
        df['quarter'] = int(i)
        df['year'] = int(year)
        # Add the dataframe to the list
        df_transaction.append(df)

# Concatenate all the dataframes in the list into a single dataframe
result_india_ins = pd.concat(df_transaction, ignore_index=True)
#reorder the column axis as per requirement
result_india_ins = result_india_ins[['year', 'quarter', 'name', 'count', 'amount']]

#csv file conversion
result_india_ins.to_csv('indiainstru_trans.csv', index=False)

#state wise transaction data based on instrument
import json
import pandas as pd
import os

state_trans = []

state_years = ['2018','2019','2020','2021','2022']
states_list = ['andaman-&-nicobar-islands','andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar', 'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala','ladakh','lakshadweep', 'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha','puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 'tripura','uttar-pradesh', 'uttarakhand', 'west-bengal']


# Loop through all the years files in the directory
for state in states_list:
  for year in state_years: 
    for i in range(1, 5):
      path = f'/content/pulse/data/aggregated/transaction/country/india/state/{state}/{year}/{i}.json'
      if os.path.exists(path):
         with open(path) as f:
             data_state = json.load(f)
#normalize the required part 
         df_s = pd.json_normalize(data_state['data']['transactionData'],'paymentInstruments',['name'])
         df_s = df_s.drop('type',axis = 1)
         df_s['state'] = str(state)
         df_s['year'] = int(year)
         df_s['quarter'] = int(i)
         state_trans.append(df_s)
state_datas = pd.concat(state_trans, ignore_index=True)

#reorder the column axis as per requirement
state_datas = state_datas[['state', 'year', 'quarter', 'name', 'count', 'amount']]

print(state_datas.head())


#get count details of missing_state
lakshadweep_data = state_datas[state_datas['state'] == 'lakshadweep'].groupby('year').count()
print(lakshadweep_data)

#csv file conversion
state_datas.to_csv('stateinstru_trans.csv', index=False)

#state wise transaction data - overall count and amount
import json
import pandas as pd

ovr_state_trans = []

state_years = ['2018','2019','2020','2021','2022']
#states_list = ['andaman-&-nicobar-islands','andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar', 'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala','ladakh','lakshadweep', 'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha','puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 'tripura','uttar-pradesh', 'uttarakhand', 'west-bengal']

# Loop through all the years files in the directory
for year in state_years: 
  for i in range(1, 5):
         path = f'/content/pulse/data/map/transaction/hover/country/india/{year}/{i}.json'
         with open(path) as f:
             ovr_data_state = json.load(f)

#normalize the required part 
         df_st = pd.json_normalize(ovr_data_state['data']['hoverDataList'],'metric',['name'])
         df_st = df_st.drop('type',axis = 1)
         df_st['year'] = int(year)
         df_st['quarter'] = int(i)
         ovr_state_trans.append(df_st)

#concat collected files
ovr_state_data = pd.concat(ovr_state_trans, ignore_index=True)

#renmaing the column name
ovr_state_data = ovr_state_data.rename(columns={'name': 'state'})

#reorder the column axis as per requirement
ovr_state_data = ovr_state_data[['state', 'year', 'quarter', 'count', 'amount']]
ovr_state_data
#print(ovr_state_data.head())

#csv file conversion
ovr_state_data.to_csv('state_amount_trans.csv', index=False)

#transaction data based on each district in a state
import json
import pandas as pd


dist_trans = []

state_years = ['2018','2019','2020','2021','2022']
states_list = ['andaman-&-nicobar-islands','andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar', 'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala','ladakh','lakshadweep', 'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha','puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 'tripura','uttar-pradesh', 'uttarakhand', 'west-bengal']


# Loop through all the years files in the directory
for state in states_list:
  for year in state_years: 
    for i in range(1, 5):
         path = f'/content/pulse/data/map/transaction/hover/country/india/state/{state}/{year}/{i}.json'
         with open(path) as f:
             data_dist = json.load(f)
#normalize the required part 
         df_dist = pd.json_normalize(data_dist['data']['hoverDataList'],'metric',['name'])
         df_dist = df_dist.drop('type',axis = 1)
         df_dist['state'] = str(state)
         df_dist['year'] = int(year)
         df_dist['quarter'] = int(i)
         dist_trans.append(df_dist)

#concat collected datas
dist_data = pd.concat(dist_trans, ignore_index=True)

#renmaing the column name
dist_data = dist_data.rename(columns={'name': 'District'})
#reorder the column axis as per requirement
dist_data = dist_data[['District','state', 'year', 'quarter', 'count', 'amount']]
dist_data
#print(state_datas.head())
#csv file conversion
dist_data.to_csv('dist_trans.csv', index=False)

#district wise user data
import json
import pandas as pd

state_years = ['2018', '2019', '2020', '2021', '2022']
states_list = ['andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar', 'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal']

districts = []
registered_users = []
app_opens = []
years = []
states = []
quart = []
for state in states_list:
    for year in state_years:
        for quarter in range(1, 5):
            path = f'/content/pulse/data/map/user/hover/country/india/state/{state}/{year}/{quarter}.json'
            with open(path) as f:
                data = json.load(f)
            for district, values in data['data']['hoverData'].items():
                districts.append(district)
                registered_users.append(values['registeredUsers'])
                app_opens.append(values['appOpens'])
                years.append(int(year))
                quart.append(int(quarter))
                states.append(state)


dist_user = pd.DataFrame({'State': states, 'Year': years,'Quarter':quart, 'District': districts, 'Registered Users': registered_users, 'App Opens': app_opens})
dist_user=dist_user[['District','State','Year','Quarter','Registered Users','App Opens']]
#csv file conversion
dist_user.to_csv('dist_user.csv', index=False)

#overall india user data

import json
import pandas as pd

#importing transaction data of year [2018-2022]
# Create an empty list to store the dataframes
df_users = []
df1_users = []

#list of years to be itterated
user_years = ['2018','2019','2020','2021','2022']


# Loop through all the years files in the directory
for year in user_years: 
  for i in range(1, 5):
    # Construct the file path
    file_path = f'/content/pulse/data/aggregated/user/country/india/{year}/{i}.json'
    
    # Load the data from the file
    with open(file_path) as f:
        data = json.load(f)
        keys = data['data'].keys()
        #print(keys)
# Create a dataframe from the transaction data
    df = pd.json_normalize(data['data'],'usersByDevice')
    df1 = pd.json_normalize(data['data']['aggregated'])
# Add the quarter column with the value of i
    df['quarter'] = int(i)
    df['year'] = int(year)
    df1['quarter'] = int(i)
    df1['year'] = int(year)
# Add the dataframe to the list
    df_users.append(df)
    df1_users.append(df1)
result_1 = pd.concat(df1_users,ignore_index=True)    
result_2 = pd.concat(df_users, ignore_index=True)
result_1 = result_1[['year','quarter','appOpens','registeredUsers']]
result_2 = result_2[['year','quarter','brand','count','percentage']]
print(result_1)
print(result_2)

#covert it to csv file format
result_2.to_csv('0vr_brand_data.csv', index=False)
#covert it to csv file format
result_1.to_csv('ovr_reguser_data.csv', index=False)

#state wise - user data
import json
import pandas as pd
import os
#importing transaction data of year [2018-2022]
# Create an empty list to store the dataframes
state_users = []
state1_users = []

#list of years to be itterated
user_years = ['2018','2019','2020','2021','2022']
state_list = ['andaman-&-nicobar-islands','andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar', 'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala','ladakh','lakshadweep', 'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha','puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 'tripura','uttar-pradesh', 'uttarakhand', 'west-bengal']


# Loop through all the years files in the directory
for state in state_list:
  for year in user_years: 
    for i in range(1, 5):
# Construct the file path
      file_path_statewise = f'/content/pulse/data/aggregated/user/country/india/state/{state}/{year}/{i}.json'
    
    # Load the data from the file
    #if os.path.exists(file_path_statewise):
      with open(file_path_statewise) as f:
        data_users = json.load(f)
        
        #keys = data_users['data'].keys()
        #print(keys)
# Create a dataframe from the transaction data
      df_state = pd.json_normalize(data_users['data'],'usersByDevice')
      df1_state = pd.json_normalize(data_users['data']['aggregated'])
# Add the quarter column with the value of i
      df_state['state'] = str(state)
      df_state['quarter'] = int(i)
      df_state['year'] = int(year)
      df1_state['state'] = str(state)
      df1_state['quarter'] = int(i)
      df1_state['year'] = int(year)
# Add the dataframe to the list
      state_users.append(df_state)
      state1_users.append(df1_state)
result_state1 = pd.concat(state_users,ignore_index=True)    
result_state = pd.concat(state1_users, ignore_index=True)
result_state1 = result_state1[['state','year','quarter','brand','count','percentage']]
result_state = result_state[['year','quarter','state','registeredUsers','appOpens']]
#result_state1- sate wise mob brand count data
#result_state - state wise reg users and app open details

#covert it to csv file format
result_state1.to_csv('state_brand_data.csv', index=False)
#covert it to csv file format
result_state.to_csv('state_user_data.csv', index=False)

#overall india top_count data(statewise)

import json
import pandas as pd

#importing transaction data of year [2018-2022]
# Create an empty list to store the dataframes

top_users = []
top_dist_df = []
top_pin_df = []


#list of years to be itterated
user_years = ['2018','2019','2020','2021','2022']


# Loop through all the years files in the directory
for year in user_years: 
  for i in range(1, 5):
    # Construct the file path
    file_path = f'/content/pulse/data/top/transaction/country/india/{year}/{i}.json'
    
    # Load the data from the file
    with open(file_path) as f:
        topuser_data = json.load(f)
        
# Create a dataframe from the transaction data
    top_df = pd.json_normalize(topuser_data['data'],'states')#,['metric'])
    top_dist = pd.json_normalize(topuser_data['data'],'districts')
    top_pin = pd.json_normalize(topuser_data['data'],'pincodes')
# Add the quarter column with the value of i
    top_df = top_df.drop('metric.type',axis=1)
    top_df['quarter'] = int(i)
    top_df['year'] = int(year)
    top_dist = top_dist.drop('metric.type',axis=1)
    top_dist['quarter'] = int(i)
    top_dist['year'] = int(year)
    top_pin = top_pin.drop('metric.type',axis=1)
    top_pin['quarter'] = int(i)
    top_pin['year'] = int(year)
# Add the dataframe to the list
    top_users.append(top_df)
    top_dist_df.append(top_dist)
    top_pin_df.append(top_pin)
  
topuser_result = pd.concat(top_users,ignore_index=True)    
top_distdf = pd.concat(top_dist_df,ignore_index=True)
top_pindf =  pd.concat(top_pin_df,ignore_index=True)
#renmaing the column name
topuser_result = topuser_result.rename(columns={'entityName':'State','metric.count': 'Count','metric.amount':'Amount'})
top_distdf = top_distdf.rename(columns={'entityName':'District','metric.count': 'Count','metric.amount':'Amount'})
top_pindf = top_pindf.rename(columns={'entityName':'Pincode','metric.count': 'Count','metric.amount':'Amount'})

#arranging the order of column
topuser_result =topuser_result[['State','year','quarter','Count','Amount']]
top_distdf =top_distdf[['District','year','quarter','Count','Amount']]
top_pindf =top_pindf[['Pincode','year','quarter','Count','Amount']]

#csv file conversion
topuser_result.to_csv('india_topcount.csv', index=False)
top_distdf.to_csv('agg_dist_topcount.csv',index = False)
top_pindf.to_csv('agg_pin_topcount.csv',index=False)

print(topuser_result)
print(top_distdf)
print(top_pindf)

#overall india top count data(district wise)

import json
import pandas as pd

#importing transaction data of year [2018-2022]
# Create an empty list to store the dataframes

top_dist_users = []


#list of years to be itterated
user_years = ['2018','2019','2020','2021','2022']
state_list = ['andaman-&-nicobar-islands','andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar', 'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala','ladakh','lakshadweep', 'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha','puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 'tripura','uttar-pradesh', 'uttarakhand', 'west-bengal']



# Loop through all the years files in the directory
for state in state_list:
 for year in user_years: 
   for i in range(1, 5):
    # Construct the file path
    file_path = f'/content/pulse/data/top/transaction/country/india/state/{state}/{year}/{i}.json'
    
    # Load the data from the file
    with open(file_path) as f:
        topuser_dist_data = json.load(f)
        
# Create a dataframe from the transaction data
    top_dist_df = pd.json_normalize(topuser_dist_data['data'],'districts')
    
# Add the quarter column with the value of i
    top_dist_df = top_dist_df.drop('metric.type',axis=1)
    top_dist_df['Quarter'] = int(i)
    top_dist_df['Year'] = int(year)
    top_dist_df['State'] = str(state)
    
# Add the dataframe to the list
    top_dist_users.append(top_dist_df)
  
topdist_result = pd.concat(top_dist_users,ignore_index=True)    

#renmaing the column name
topdist_result = topdist_result.rename(columns={'entityName':'District','metric.count': 'Count','metric.amount':'Amount'})

topdist_result =topdist_result[['District','State','Year','Quarter','Count','Amount']]

#csv file conversion
topdist_result.to_csv('dist_topcount.csv', index=False)

#overall india top_user data(districtwise)

import json
import pandas as pd

#importing transaction data of year [2018-2022]
# Create an empty list to store the dataframes

top_distreg_users = []


#list of years to be itterated
user_years = ['2018','2019','2020','2021','2022']
state_list = ['andaman-&-nicobar-islands','andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar', 'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala','ladakh','lakshadweep', 'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha','puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 'tripura','uttar-pradesh', 'uttarakhand', 'west-bengal']



# Loop through all the years files in the directory
for state in  state_list: 
 for year in user_years: 
  for i in range(1, 5):
    # Construct the file path
    file_path = f'/content/pulse/data/top/user/country/india/state/{state}/{year}/{i}.json'
    
    # Load the data from the file
    with open(file_path) as f:
        reg_distuser_data = json.load(f)
        
# Create a dataframe from the transaction data
    top_distreg_df = pd.json_normalize(reg_distuser_data['data'],'districts')
    
#append year,quarter
    top_distreg_df['Quarter'] = int(i)
    top_distreg_df['Year'] = int(year)
    
    
# Add the dataframe to the list
    top_distreg_users.append(top_distreg_df)
    
distreg_result = pd.concat(top_distreg_users,ignore_index=True)
    
distreg_result = distreg_result.rename(columns={'name':'District'})

distreg_result = distreg_result[['District','Year','Quarter','registeredUsers']]
#csv file conversion
distreg_result.to_csv('dist_topreguser.csv', index=False)

#overall india top10_user data(statewise)

import json
import pandas as pd

#importing transaction data of year [2018-2022]
# Create an empty list to store the dataframes

top_statereg_users = []
top_dist_us = []
top_pin_us = []


#list of years to be itterated
user_years = ['2018','2019','2020','2021','2022']


# Loop through all the years files in the directory
for year in user_years: 
  for i in range(1, 5):
    # Construct the file path
    file_path = f'/content/pulse/data/top/user/country/india/{year}/{i}.json'
    
    # Load the data from the file
    with open(file_path) as f:
        reguser_data = json.load(f)
        
# Create a dataframe from the transaction data
    state_reg_df = pd.json_normalize(reguser_data['data'],'states')
    top_dist_user = pd.json_normalize(reguser_data['data'],'districts')
    top_pin_user = pd.json_normalize(reguser_data['data'],'pincodes')
# Add the quarter column with the value of i
    state_reg_df['Quarter'] = int(i)
    state_reg_df['Year'] = int(year)
    top_dist_user['Quarter'] = int(i)
    top_dist_user['Year'] = int(year)
    top_pin_user['Quarter'] = int(i)
    top_pin_user['Year'] = int(year)
    
# Add the dataframe to the list
    top_statereg_users.append(state_reg_df)
    top_dist_us.append(top_dist_user)
    top_pin_us.append(top_pin_user)
#concat the files together
topstate_reg_result = pd.concat(top_statereg_users,ignore_index=True)
dist_result = pd.concat(top_dist_us,ignore_index = False)
pin_result = pd.concat(top_pin_us,ignore_index=True)
#renaming the column
topstate_reg_result = topstate_reg_result.rename(columns={'name':'State'})
dist_result = dist_result.rename(columns={'name':'District'})
pin_result = pin_result.rename(columns={'name':'Pincode'})

#arraning the order
topstate_reg_result =topstate_reg_result[['State','Year','Quarter','registeredUsers']]
dist_result =dist_result[['District','Year','Quarter','registeredUsers']]
pin_result =pin_result[['Pincode','Year','Quarter','registeredUsers']]
#csv file conversion
topstate_reg_result.to_csv('india_topreguser.csv', index=False)
dist_result.to_csv('dist_topreguser.csv', index=False)
pin_result.to_csv('pin_topreguser.csv', index=False)