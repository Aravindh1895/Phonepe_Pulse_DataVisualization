# -*- coding: utf-8 -*-
"""Display_part.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vs9e2zKcCVVVORKuWbh2rItSGP4OHPcK
"""

#installing necessary packages
!pip install plotly
!pip install geopandas
!pip install jedi
!pip install streamlit
!pip install -q streamlit
!pip install streamlit_option_menu

#establishing connection with sqlite and store the datas into sql server
import sqlite3
connection = sqlite3.connect("phonepe_pulse.db")
cursor = connection.cursor()
result_india_ins.to_sql('agg_indiatransaction',connection,if_exists='replace')
state_datas.to_sql('agg_statetransaction', connection, if_exists='replace')
ovr_state_data.to_sql('total_statetransaction', connection, if_exists='replace')
dist_data.to_sql('district_transaction', connection, if_exists='replace')
dist_user.to_sql('district_appcount', connection, if_exists='replace')
result_2.to_sql('india_user', connection, if_exists='replace')
result_state1.to_sql('state_user', connection, if_exists='replace')
result_1.to_sql('india_appcount', connection, if_exists='replace')
result_state.to_sql('state_appcount', connection, if_exists='replace')
topuser_result.to_sql('aggindia_topcount', connection, if_exists='replace')
topdist_result.to_sql('district_topcount', connection, if_exists='replace')
distreg_result.to_sql('district_topuser', connection, if_exists='replace')
topstate_reg_result.to_sql('aggindia_topuser', connection, if_exists='replace')
top_distdf.to_sql('aggdist_topcount', connection, if_exists='replace')
top_pindf.to_sql('aggpincode_topcount', connection, if_exists='replace')
dist_result.to_sql('aggdist_topuser', connection, if_exists='replace')
pin_result.to_sql('aggpin_topuser', connection, if_exists='replace')
connection.commit()

# Commented out IPython magic to ensure Python compatibility.
# #Display_part - API 
# 
# %%writefile phonepe.py
# import streamlit as st
# from PIL import Image
# import json
# from streamlit_option_menu import option_menu
# import plotly.express as px
# import pandas as pd
# import sqlite3
# from google.colab import files
# from io import BytesIO
# import numpy as np
# import matplotlib.pyplot as plt
# 
# #----------------------------------------------------------------Fetching a data from sqlite server and converting to pandas dataframe--------------------------------------------------------------------
# # Connect to the database
# conn = sqlite3.connect("phonepe_pulse.db")
# 
# # Define a function to fetch data from a table
# def fetch_table(table_name):
#     cursor = conn.execute(f"SELECT * FROM {table_name}")
#     data_df = pd.DataFrame(cursor.fetchall(), columns=[description[0] for description in cursor.description])
#     data_df = data_df.drop('index',axis = 1)
#     return data_df
# 
# #converting sql datas to dataframe for plotly chloropleth processing
# 
# #instrument based transaction
# agg_india_instru=fetch_table('agg_indiatransaction')
# agg_state_instru=fetch_table('agg_statetransaction')
# #total amount based transaction
# agg_state_total = fetch_table('total_statetransaction')
# agg_dist_total = fetch_table('district_transaction')
# #brand based user data
# india_user_brands = fetch_table('india_user')
# state_user_brands=fetch_table('state_user')
# #appcount based user data
# india_user_appcount=fetch_table('india_appcount')
# state_user_appcount=fetch_table('state_appcount')
# district_user_appcount=fetch_table('district_appcount')
# #top 10 based on transaction
# agg_state_topcount = fetch_table('aggindia_topcount')
# agg_dist_topcount = fetch_table('aggdist_topcount')
# agg_pin_topcount = fetch_table('aggpincode_topcount')
# #top 10 based on reg_users
# agg_state_topuser = fetch_table('aggindia_topuser')
# agg_dist_topuser = fetch_table('aggdist_topuser')
# agg_pin_topuser = fetch_table('aggpin_topuser')
# 
# #----------------------------------------------------------geojson file extraction and pre-processing-------------------------------------------------------------------------------------
# #for transaction dataset
# 
# #plotly geojson india state file extraction and adding id to our file(ladakh is missing)
# india_map = json.load(open('/content/states_india.geojson'))
# 
# state_id = {}
# for index, feature in enumerate(india_map['features']):
#   id_key = feature['properties']['state_code']
#   feature['id'] = id_key
#   state_name = feature['properties']['st_nm'].lower()
# 
#   state_id[state_name] = (id_key)
# 
# #pre-processing work for geojson file
# state_id['dadra & nagar haveli & daman & diu'] = state_id.pop('dadara & nagar havelli')
# state_id['andaman & nicobar islands'] = state_id.pop('andaman & nicobar island')
# state_id['arunachal pradesh'] = state_id.pop('arunanchal pradesh')
# state_id['delhi'] = state_id.pop('nct of delhi')
# 
# 
# #for user dataset
# india_map= json.load(open('/content/states_india.geojson'))
# u_state_id = {}
# for feature in india_map['features']:
#     feature['id']=feature['properties']['state_code']
#     u_state_id[feature['properties']['st_nm']]=feature['id']
# #convert all characters in dictionary small letters to avoid key error by list comprehension
#     u_state_id = {k.lower(): v for k, v in u_state_id.items()}
# #state_id
# u_state_id['dadra-&-nagar-haveli-&-daman-&-diu'] = u_state_id.pop('dadara & nagar havelli')
# u_state_id['andaman-&-nicobar-islands'] = u_state_id.pop('andaman & nicobar island')
# u_state_id['arunachal-pradesh'] = u_state_id.pop('arunanchal pradesh')
# u_state_id['andhra-pradesh'] = u_state_id.pop('andhra pradesh')
# u_state_id['himachal-pradesh'] = u_state_id.pop('himachal pradesh')
# u_state_id['madhya-pradesh'] = u_state_id.pop('madhya pradesh')
# u_state_id['uttar-pradesh'] = u_state_id.pop('uttar pradesh')
# u_state_id['west-bengal'] = u_state_id.pop('west bengal')
# u_state_id['tamil-nadu'] = u_state_id.pop('tamil nadu')
# u_state_id['jammu-&-kashmir'] = u_state_id.pop('jammu & kashmir')
# u_state_id['delhi'] = u_state_id.pop('nct of delhi')  
# 
# #-----------------------------------------------------------------------------------def-functions---------------------------------------------------------------------------------------------
# 
# #def function for transaction data
# def amount_geojson(file_name):
#    df_st =file_name
#    df_st['id'] = df_st['state'].apply(lambda x: state_id.get(x,'1'))
# # Replace 'ladakh' values with 'jammu & kashmir'
#    df_st['state'].replace({'ladakh': 'jammu & kashmir'}, inplace=True)
# # Group by 'state_name', 'year', and 'quarter', and sum up 'count' and 'amount'
#    df_group = df_st.groupby(['state', 'year', 'quarter'], as_index=False).agg({'count': 'sum', 'amount': 'sum'})
# # Drop rows where 'state_name' is 'ladakh'
#    df_group.drop(df_group[df_group['state'] == 'ladakh'].index, inplace=True)
# #merge id column to data frame
#    df_id = df_st.groupby('state')['id'].first().reset_index()
#    df_group = df_group.merge(df_id, on='state')
#    return df_group
# 
# #function for user data
# def user_geojson(file_name):
#    dfu_st = file_name
#    dfu_st['id'] = dfu_st['state'].apply(lambda x: u_state_id.get(x,'1'))
# # Replace 'ladakh' values with 'jammu & kashmir'
#    dfu_st['state'].replace({'ladakh': 'jammu-&-kashmir'}, inplace=True)   
# # Group by 'state_name', 'year', and 'quarter', and sum up 'count' and 'amount'
#    dfu_group = dfu_st.groupby(['state', 'year', 'quarter'], as_index=False).agg({'registeredUsers': 'sum', 'appOpens': 'sum'})
# # Drop rows where 'state_name' is 'ladakh'
#    dfu_group.drop(dfu_group[dfu_group['state'] == 'ladakh'].index, inplace=True)
# #merge id column to data frame
#    dfu_id = dfu_st.groupby('state')['id'].first().reset_index()
#    dfu_group = dfu_group.merge(dfu_id, on='state')
#    return dfu_group
# 
# #function for getting index of state name in geo json file
# def index_geojson(file_name):
#    df_ind = file_name
#    df_ind['id'] = df_ind['state'].apply(lambda x: state_id.get(x, '1')[1])
#    return df_ind
# 
# def top10_transaction(table_name):
#   top_am= table_name
#   new_da = top_am[(top_am['year'] == int(year)) & (top_am['quarter'] == int(quarter))].reset_index(drop=True, inplace=False)
#   new_da.index = new_da.index + 1  # add 1 to the index
#   mod_1 = new_da.drop(['year','quarter','Count'],axis=1)
# # convert amount to int (in crores) and add "Cr" at the end
#   mod_1['Amount'] = round(mod_1['Amount'] / 10000000).astype(int)#.astype(str) + ' Cr'
#   return mod_1
# 
# def user_data(column):
#   total_us=india_user_appcount
#   new_us = total_us[(total_us['year'] == int(year)) & (total_us['quarter'] == int(quarter))].reset_index(drop=True, inplace=False)
#   mod=new_us.drop(['year','quarter'],axis=1)
#   users=mod[column]
#   tot = '{:,}'.format(users.iloc[0])
#   if tot == '0':
#     return 'Unavailable'
#   else:
#     return tot
# 
# def state_user_data(column):
#   total_user=state_user_appcount
#   new_us_st = total_user[(total_user['state'] == new_st_name_1) & (total_user['year'] == int(year)) & (total_user['quarter'] == int(quarter))].reset_index(drop=True, inplace=False)
#   mod=new_us_st.drop(['state','year','quarter'],axis=1)
#   users=mod[column]
#   tot = '{:,}'.format(users.iloc[0])
#   if tot == '0':
#     return 'Unavailable'
#   else:
#     return tot    
# 
# #def for top 10district transaction
# def topdistrict_data(table_name):
#   top_dist=table_name
#   new_tot = top_dist[(top_dist['state'] ==new_st_name) & (top_dist['year'] == int(year)) & (top_dist['quarter'] == int(quarter))]#.reset_index(drop=True, inplace=False)
#   mod_tot = new_tot.drop(['state','year','quarter','count'],axis=1)
#   mod_tot['amount'] = round(mod_tot['amount'] / 10000000).astype(int)
#   dist_tot= mod_tot.sort_values('amount', ascending=False).reset_index(drop=True)
#   dist_tot.index = dist_tot.index + 1  # add 1 to the index
#   dist_tot= dist_tot.rename(columns={'amount':'Amount(in crores)'})
#   return (dist_tot)
# 
# #def for top10 district users
# def topdistrict_user(table_name):
#   dist_user=table_name
#   dist_tot = dist_user[(dist_user['State'] ==new_st_name_1) & (dist_user['Year'] == int(year)) & (dist_user['Quarter'] == int(quarter))]#.reset_index(drop=True, inplace=False)
#   mod_dist = dist_tot.drop(['State','Year','Quarter','App Opens'],axis=1)
#   mod_dist['Registered Users'] = round(mod_dist['Registered Users'] / 100000).astype(int)
#   dist_top= mod_dist.sort_values('Registered Users', ascending=False).reset_index(drop=True)
#   dist_top.index = dist_top.index + 1  # add 1 to the index
#   dist_top= dist_top.rename(columns={'Registered Users':'Registered_users(in Lakhs)'})
#   return (dist_top)
# 
# #def for instruments based transaction
# def col2_data(table_name1):
#   new_us = table_name1[(table_name1['year'] == int(year)) & (table_name1['quarter'] == int(quarter))].reset_index(drop=True, inplace=False)
#   mod_us=new_us.drop(['year','quarter'], axis=1)  
#   mod_us.index= new_us.index + 1  # add 1 to the index
#   return mod_us
# 
# #def for top 10 state reg users
# def top10_reg_users(table_name):
#   top_am = table_name[(table_name['Year'] == int(year)) & (table_name['Quarter'] == int(quarter))].reset_index(drop=True, inplace=False)
#   mod_1 = top_am.drop(['Year', 'Quarter'], axis=1)
#   mod_1.index = mod_1.index + 1  # add 1 to the index
#   mod_1['registeredUsers'] =round(mod_1['registeredUsers'] / 10000000, 2)
#   return mod_1    
# 
# #--------------------------------------------------------------------layout for side-bar----------------------------------------------------------------------------------------------------------------------
# # Set page layout to wide
# st.set_page_config(page_title="Phonepe Pulse", page_icon=":memo:", layout="wide")
# 
# #setting page_config for sidebar
# st.markdown(
#     """
#     <style>
#     .sidebar .sidebar-content {
#         width: 300px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
# 
# #------------------------------------------------------------------------Default Home-options---------------------------------------------------------------------------------------------------------------------------
# 
# phn = Image.open("/content/bannere.png")
# st.image(phn,use_column_width=True)
# select = option_menu(menu_title = None,
#                      options = ["Home","About","Get Insights","Explore Data"],
#                      icons =["house","list-task","search","toggles"],
#                      default_index=0,orientation="horizontal",
#                      styles={"container": {"padding": "0!important", "background-color": "white","size":"cover"},
#                              "icon": {"color": "black", "font-size": "20px"},
#                              "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
#                              "nav-link-selected": {"background-color": "#6F36AD"},
#                              }
#                     )
# 
# if select == "Home":
#     col1 = st.columns(1)[0]
#     #st.image(Image.open("/phonepe.png"),width = 500)
#     col1.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
#     col1.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/") 
# 
# #--------------------------------------------------------------------Display for About-option--------------------------------------------------------------------------------------------------------------------------------------------- 
# 
# elif select == "About":
#     col1,col2 = st.columns(2)
#     with col1:
#          st.title('Welcome to the dashboard|GO PHONEPE GO CASHLESS')
#         #st.video("/pulse-video.mp4")
#     with col2:
#         #st.image(Image.open("/PhonePe_Logo.jpg"),width = 600)
#         st.write("---")
#         st.subheader("The Indian digital payments story has truly captured the world's imagination."
#                  "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
#     st.write("---")
#     col1,col2 = st.columns(2)
#     with col1:
#         st.title("THE BEAT OF PHONEPE")
#         st.write("---")
#         st.subheader("DIGITAL PAYMENTS:A US$10 Tn Opportunity ")
#         #st.image(Image.open("/top.jpeg"),width = 400)
#         #with open("/annual report.pdf","rb") as f: 
#             #data = f.read()
#         #st.download_button("DOWNLOAD REPORT",data,file_name="annual report.pdf")
#         col1.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
#     #with col2:
#         st.image(Image.open("/content/report_phonepe.png"),width = 400)     
# 
# #--------------------------------------------------------------------Display for Explore-Data options-----------------------------------------------------------------------------------------------------------------------
# elif select == "Explore Data":
#   padding = 0 
#   with st.sidebar:
#     st.title("Welcome To The India's First Mobile UPI")
#     st.write("----")
#     st.subheader("Let's Explore The Data")
#     options = ['All India','State']
#     choose = st.radio("Select",options,horizontal = True,index = 0)
#   if choose == 'All India':
#      with st.sidebar:
#       select_i = option_menu(menu_title ="Choose:",
#                              options = ["Transaction Data","User Data"],
#                              icons =["wallet","people"],
#                              default_index=0,
#                              orientation="vertical",
#                              styles={"container": {"padding": "0!important", "background-color": "white","size":"cover"},
#                                      "icon": {"color": "black", "font-size": "20px"},
#                                      "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
#                                      "nav-link-selected": {"background-color": "#6F36AD"},
#                                     }
#                               )
#      if select_i == "Transaction Data":
#       with st.sidebar:
#        with st.container():
#         col1, col2 = st.columns(2)
#         with col1:
#           year = st.selectbox("Select Year", ['2018', '2019', '2020','2021','2022'])
#         with col2:
#           quarter = st.selectbox("Select Quarter", ["1", "2","3","4"])
#         search = st.button('search')
#         
#       if search:
# #data for col 1
#        col_1,col_2 = st.columns([3,1])
# # Create main page
#        with col_1:
#         st.title("Transaction Data Analysis")
# #creating the filtered data for particular year and quarter for mapping
#         amount_geo = amount_geojson(agg_state_total)
#         state_amount_geo = amount_geo[(amount_geo['year'] == int(year)) & (amount_geo['quarter'] == int(quarter))].reset_index(drop=True, inplace=False)
# #Generate map
#         fig = px.choropleth(state_amount_geo,
#                            geojson=india_map,
#                            locations='id',
#                            color='amount',
#                            hover_name='state',
#                            hover_data=['count'],
#                            projection="robinson",
#                            color_continuous_scale='rainbow'
#                            )
#         fig.update_geos(fitbounds = 'locations',visible = False )
#         fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# 
# # Display map in container
#         with st.container():
#           st.subheader("Map Analysis for Transaction Data")
#           st.write("----")
#           with st.spinner('Loading Map...'):
#             st.plotly_chart(fig,theme="streamlit", use_container_width=True)      
# #data for col 2
# #extracting totals using def 
#         total_data = col2_data(agg_india_instru)
# # calculate total amount, count, and average
#         total_sum, total_count = total_data['amount'].sum(), total_data['count'].sum()
#         total_avg = round(total_sum / total_count)
# 
# # convert amount to int (in crores) and add "Cr" at the end
#         new_total_data = total_data.copy()
#         new_total_data['amount'] = (new_total_data['amount'] / 10000000).round().astype(int).astype(str) + ' Cr'
# 
# # calculate percentage column in new_mod table
#         total_data['amount'] = (total_data['amount'] / 10000000).astype(int)
#         total_data['percentage'] = total_data['amount'].astype(int) / total_sum
#         formatted = '{:,}'.format(total_count)
#         total_sum = round(total_sum/ 10000000)
# 
# #graphical analysis part
#  # calculate percentage column in state_top10 table and insert "others"
#         state_top10 = top10_transaction(agg_state_topcount)
#         conv_top = state_top10.copy()
#         conv_top['percent'] = conv_top['Amount'] / total_sum
#         conv_top = conv_top.drop('Amount', axis=1)
#         cum = conv_top['percent'].sum()
#         others = pd.DataFrame({
#                'State': ['Others'],
#                'percent': [1 - cum]})
#         conv_top = pd.concat([conv_top, others], ignore_index=True)
# 
# #pie chart for transaction amount
#         labels = conv_top['State']
#         sizes = conv_top['percent']
# #pie chart for instruments 
#         label = total_data['name']
#         size = total_data['percentage']
#          
# # Creating pie chart_1
#         fig1 = px.pie(conv_top, values=sizes, names=labels,color_discrete_sequence=px.colors.qualitative.Set3,hole=0.25)     
# #pie chart_2
#         fig2 = px.pie(total_data, values=size, names=label,color_discrete_sequence=px.colors.qualitative.Set3,hole=0.25)
# # displaying pie chart
#         st.write('-----')
#         st.subheader('Graphical Analysis of Data') 
#         st.write("Most Potential States")
#         st.plotly_chart(fig1,theme="streamlit",use_container_width=True)
#         st.write('-----')         
#         st.write("Most Potential instrument")
#         st.plotly_chart(fig2,theme="streamlit",use_container_width=True)        
# 
#         
# #display for col 2 
#        with col_2:
#         with st.container():    
#          st.header('Transaction')
#          st.subheader("All PhonePe transactions (UPI + Cards + Wallets)")
#          st.write(formatted)
#          st.subheader('Total Payment Value')
#          st.write('₹',total_sum,'Cr')
#          st.subheader('Average Value')
#          st.write('₹',total_avg)
#          st.write('----')
#          st.header('Categories')
#          st.dataframe(total_data)
#          st.write('----')
#          st.write('Top 10 Data')
#          st.write('(Amount in crores)')
#          select_top =option_menu(menu_title = None,
#                                  options = ["State","District","Pincode"],
#                                  icons =None,
#                                  default_index=0,orientation="horizontal",
#                                  styles={"container": {"padding": "0!important", "background-color": "white", "size":"cover"},
#                                          "nav-link": {"font-size": "12px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
#                                          "nav-link-selected": {"background-color": "#6F36AD"},})
#          
#          with st.container():
#           if select_top == 'State':
#             state_top10 = top10_transaction(agg_state_topcount)
#             st.dataframe(state_top10)
#           elif select_top == 'District':
#             dist_top10 = top10_transaction(agg_dist_topcount)
#             st.dataframe(dist_top10)
#           elif select_top == 'Pincode':
#             pin_top10 = top10_transaction(agg_pin_topcount)
#             st.dataframe(pin_top10)
# 
#  #----------------------------------------------------------------------"user data"----------------------------------------------------------------
#    
#      elif select_i == 'User Data':
#       with st.sidebar:
#         with st.container():
#          col1, col2 = st.columns(2)
#          with col1:
#           year = st.selectbox("Select Year", ['2018', '2019', '2020','2021','2022'])
#          with col2:
#           quarter = st.selectbox("Select Quarter", ["1", "2","3","4"])
#         search_1 = st.button('search')
#       if search_1:
#        col_3,col_4 = st.columns([3,1])
# # Create main page
#        with col_3:
#         st.title("User Data Analysis")
# #creating the filtered data for particular year and quarter for mapping
#         user_geo = user_geojson(state_user_appcount)
#         state_user_geo = user_geo[(user_geo['year'] == int(year)) & (user_geo['quarter'] == int(quarter))].reset_index(drop=True, inplace=False)
# #Generate map
#         fig_1 = px.choropleth(state_user_geo,
#                            geojson=india_map,
#                            locations='id',
#                            color='registeredUsers',
#                            hover_name='state',
#                            hover_data=['appOpens'],
#                            projection="robinson",
#                            color_continuous_scale='rainbow'
#                            )
#         fig_1.update_geos(fitbounds = 'locations',visible = False )
#         fig_1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# # Display map in container
#         with st.container():
#           st.subheader("Map Analysis for User Data")
#           st.write("----")
#           with st.spinner('Loading Map...'):
#             st.plotly_chart(fig_1,theme="streamlit", use_container_width=True)      
#  
#   #data for col 2
#         user_datas = col2_data(india_user_brands)
#   #display portion for col2
#         us_app = user_data('appOpens')
#         us_reg = user_data('registeredUsers')
#  #top 10 state from def 
#         df_topusers = top10_reg_users(agg_state_topuser)
#  # add 'cr' to every rows at the end 
#         state_top10_= df_topusers.copy()
#         state_top10_['registeredUsers'] = state_top10_['registeredUsers'].astype(str) + ' Cr'
#  #pie chart inputs      
#         labels_1 = df_topusers['State']
#         sizes_1 = df_topusers['registeredUsers']
# #pie chart for instruments 
#         label_1 = user_datas['brand']
#         size_1 = user_datas['percentage']
#          
# # Creating pie chart_1
#         fig3 = px.pie(df_topusers, values=sizes_1, names=labels_1,color_discrete_sequence=px.colors.qualitative.Set3,hole=0.25)     
# #pie chart_2
#         fig4 = px.pie(user_datas, values=size_1, names=label_1,color_discrete_sequence=px.colors.qualitative.Set3,hole=0.25)      
# # graphical part
#         st.write('-----')
#         st.subheader('Graphical Analysis of Data') 
#         st.write("Most Potential States")
#         st.plotly_chart(fig3,theme="streamlit",use_container_width=True)
#         st.write('-----')         
#         st.write("Most used mobile brands")
#         st.plotly_chart(fig4,theme="streamlit",use_container_width=True)
# 
#  #display portion for col 4     
#        with col_4:
#         with st.container():
#          st.header("Users")                
#          st.subheader('Registered users till Q{},{}'.format(quarter, year))
#          st.write(us_reg)
#          st.subheader('Registered appopens in Q{},{}'.format(quarter, year))
#          st.write(us_app)
#          st.write('-----')
#          st.subheader("Top 10 states")
#          st.write("Based on reg users")
#          st.dataframe(state_top10_)
#          st.write('-----')
#          st.subheader("Users Based on brands")
#          st.dataframe(user_datas)
# #---------------------------------------------------------------------------choosing State option------------------------------------------------------------------------------------
#   elif choose == 'State':
#     with st.sidebar:
#      select_i = option_menu(menu_title ="Choose:",
#                              options = ["Transaction Data","User Data"],
#                              icons =["wallet","people"],
#                              default_index=0,
#                              orientation="vertical",
#                              styles={"container": {"padding": "0!important", "background-color": "white","size":"cover"},
#                                      "icon": {"color": "black", "font-size": "20px"},
#                                      "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
#                                      "nav-link-selected": {"background-color": "#6F36AD"},
#                                     }
#                               )
#     if select_i=='Transaction Data':
#      with st.container():
#         states = ['Andaman & Nicobar Islands','Andhra Pradesh', 'Arunachal Pradesh','Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
#                   'Dadra & Nagar Haveli & Daman & Diu', 'Delhi', 'Goa', 'Gujarat','Haryana','Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand',
#                   'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep','Madhya Pradesh','Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
#                   'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim','Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh','Uttarakhand','West Bengal']
#         state_lower = [state.lower() for state in states]
#         state_name=st.sidebar.selectbox('select the state:',state_lower)
# #replace gap b/w state with - for district data         
#         new_st_name = state_name.replace(" ", "-")
#         col_5, col_6 = st.columns(2)
#         with col_5:
#           year = st.sidebar.selectbox("Select Year", ['2018', '2019', '2020','2021','2022'])
#         with col_6:
#           quarter = st.sidebar.selectbox("Select Quarter", ["1", "2","3","4"])
#         search_2 = st.sidebar.button('search')
#      if search_2:
# #data for col 1
#        col_1,col_2 = st.columns([3,1])
# # Create main page
#        with col_1:
#         st.title("Transaction Data Analysis")
# #creating the filtered data for particular year and quarter for mapping
#         amount_state = amount_geojson(agg_state_total)
#         new_st_amount = amount_state[(amount_state['state'] == state_name)&(amount_state['year'] == int(year)) & (amount_state['quarter'] == int(quarter))].reset_index(drop=True, inplace=False)
# 
# # Search for the coordinate feature with matching state name using state_id
#         index_state = amount_geojson(agg_state_total)
#         new_st_index = index_state[(index_state['state'] == state_name)]
#         feature_id= new_st_index['id'].iloc[0]
# 
# # Calculate the center point of the state
#         state_lat, state_lon = np.mean(india_map['features'][feature_id]['geometry']['coordinates'][0][0], axis=0)
# #Generate map
#         fig_3 = px.choropleth(new_st_amount,
#                            geojson=india_map,
#                            locations='id',
#                            color='amount',
#                            hover_name='state',
#                            hover_data=['count'],
#                            projection="robinson",
#                            color_continuous_scale='YlGnBu'
#                            )
#         fig_3.update_geos(fitbounds = 'locations',visible = False,center={'lat': state_lat, 'lon': state_lon},scope = 'asia' )
#         fig_3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# # Display map in container
#         with st.container():
#           st.subheader("Transaction Analysis for {}".format(state_name))
#           st.write("----")
#           with st.spinner('Loading Map...'):
#             st.plotly_chart(fig_3,theme="streamlit", use_container_width=True)      
# #data for col 2
#         state_catg= new_st_amount
#         new_count = state_catg['count'].sum()
#         new_total = state_catg['amount']
#         format = '{:,}'.format(new_count)
#         new_sum = int(round(new_total / 10000000))
#         new_avg = int(new_total/new_count)
# #top 10 district for dataframe                  
#         top_district = topdistrict_data(agg_dist_total)
#         top_10_dist = top_district.head(10)
#         top10_dis=top_10_dist['Amount(in crores)'].sum()
# #creating others for pie chart
#         others = pd.DataFrame({
#                   'District': ['Others'],
#                   'Amount(in crores)': [new_sum - top10_dis] })
#         conv_top = pd.concat([top_10_dist , others], ignore_index=True)
# #df for instrument based transaction   
#         ins_state = topdistrict_data(agg_state_instru)
# 
# # convert amount to int (in crores) and add "Cr" at the end
#         #new_instru_data = ins_state.copy()
#         #new_instru_data['amount'] = (new_instru_data['amount'] / 10000000).round().astype(int).astype(str) + ' Cr'
# 
# #pie chart for districts 
#         labels_2 = conv_top['District']
#         sizes_2 = conv_top['Amount(in crores)']
# 
# #pie chart for instruments 
#         label_2 = ins_state['name']
#         size_2 = ins_state['Amount(in crores)']        
#          
# # Creating pie chart_1
#         fig5 = px.pie(conv_top, values=sizes_2, names=labels_2,color_discrete_sequence=px.colors.qualitative.Set3,hole=0.25)     
# #pie chart_2
#         fig6 = px.pie(ins_state, values=size_2, names=label_2,color_discrete_sequence=px.colors.qualitative.Set3,hole=0.25)      
# 
# # graphical part
#         st.write('-----')
#         st.subheader('Graphical Analysis of Data') 
#         st.write("Most Potential Districts")
#         st.plotly_chart(fig5,theme="streamlit",use_container_width=True)
#         st.write('-----')         
#         st.write("Most Potential Instruments")
#         st.plotly_chart(fig6,theme="streamlit",use_container_width=True)
# 
# #display for col 2 
#         with col_2:     
#          st.header('Transaction')
#          st.subheader("All PhonePe transactions (UPI + Cards + Wallets)")
#          st.write(format)
#          st.subheader('Total Payment Value')
#          st.write('₹',new_sum,'Cr')
#          st.subheader('Average Value')
#          st.write('₹',new_avg)
#          st.write('----')
#          st.header('Top 10 Districts')         
#          st.dataframe(top_10_dist)
#          st.header('Categories')         
#          st.dataframe(ins_state)
# 
#         #----------------------------------------------------------User OPtion-----------------------------------------------------------------------------------         
# 
#     elif select_i == 'User Data':
#       with st.container():
#         states_1 = ['Andaman & Nicobar Islands','Andhra Pradesh', 'Arunachal Pradesh','Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
#                   'Dadra & Nagar Haveli & Daman & Diu', 'Delhi', 'Goa', 'Gujarat','Haryana','Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand',
#                   'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep','Madhya Pradesh','Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
#                   'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim','Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh','Uttarakhand','West Bengal']
#         state_lower_1 = [state.lower() for state in states_1]
#         state_name_1=st.sidebar.selectbox('select the state:',state_lower_1)
#         new_st_name_1 = state_name_1.replace(" ", "-")
#  #replace gap b/w state with - for district data         
#         
#         with st.container():
#          col1, col2 = st.columns(2)
#          with col1:
#           year = st.sidebar.selectbox("Select Year", ['2018', '2019', '2020','2021','2022'])
#          with col2:
#           quarter = st.sidebar.selectbox("Select Quarter", ["1", "2","3","4"])
#         search_3 = st.sidebar.button('search')
#       if search_3:
#        col_3,col_4 = st.columns([3,1])
# # Create main page
#        with col_3:
#         st.title("User Data Analysis")
# #creating the filtered data for particular year and quarter for mapping
#         user_geo = user_geojson(state_user_appcount)
#         state_user_geo = user_geo[(user_geo['state']==new_st_name_1) & (user_geo['year'] == int(year)) & (user_geo['quarter'] == int(quarter))].reset_index(drop=True, inplace=False)
# 
# # Search for the coordinate feature with matching state name using state_id
#         index_user = user_geojson(state_user_appcount)
#         st_user_index = index_user[(index_user['state'] == new_st_name_1)]
#         feature_id_u= st_user_index['id'].iloc[0]
# 
# # Calculate the center point of the state
#         state_lat1, state_lon1 = np.mean(india_map['features'][feature_id_u]['geometry']['coordinates'][0][0], axis=0)
# 
# #Generate map
#         fig_1 = px.choropleth(state_user_geo,
#                            geojson=india_map,
#                            locations='id',
#                            color='registeredUsers',
#                            hover_name='state',
#                            hover_data=['appOpens'],
#                            projection="robinson",
#                            color_continuous_scale='rainbow'
#                            )
#         fig_1.update_geos(fitbounds = 'locations',visible = False,center={'lat': state_lat1, 'lon': state_lon1},scope = 'asia')
#         fig_1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# 
#   #data for col 2
#        
#         total_user=state_user_brands
#         new_user = total_user[(total_user['state'] == new_st_name_1) & (total_user['year'] == int(year)) & (total_user['quarter'] == int(quarter))].reset_index(drop=True, inplace=False)
#         mod_user=new_user.drop(['state','year','quarter'],axis=1)
#  
#  #df for top 10 districts        
#         top_districtuser = topdistrict_user(district_user_appcount)
#         top_10_distu = top_districtuser.head(10)
# 
# #data for pie chart
#  #pie chart inputs      
#         labels_3 = top_10_distu['District']
#         sizes_3 = top_10_distu['Registered_users(in Lakhs)']
# #pie chart for instruments 
#         label_3 = mod_user['brand']
#         size_3 = mod_user['percentage']
#          
# # Creating pie chart_1
#         fig7 = px.pie(top_10_distu, values=sizes_3, names=labels_3,color_discrete_sequence=px.colors.qualitative.Set3,hole=0.25)     
# #pie chart_2
#         fig8 = px.pie(mod_user, values=size_3, names=label_3,color_discrete_sequence=px.colors.qualitative.Set3,hole=0.25)          
# 
# # Display map in container
#         with st.container():
#          st.subheader("User Analysis for {}".format(state_name_1))
#          st.write("----")
#          with st.spinner('Loading Map...'):
#           st.plotly_chart(fig_1,theme="streamlit", use_container_width=True)      
#          st.write("----")
#          st.write("Most Potential Districts")
#          st.plotly_chart(fig7,theme="streamlit",use_container_width=True)
#          st.write('-----')         
#          st.write("Most used mobile brands")
#          st.plotly_chart(fig8,theme="streamlit",use_container_width=True)
# 
#   #display portion for col2
#         with col_4:
#          with st.container():
#           st.header("Users")
#           user_app = state_user_data('appOpens')
#           user_reg = state_user_data('registeredUsers')
#           st.subheader('Registered users till Q{},{}'.format(quarter, year))
#           st.write(user_reg)
#           st.subheader('Registered appopens in Q{},{}'.format(quarter, year))
#           st.write(user_app)
#           st.write('-----')
#           st.header('Top 10 Districts')         
#           st.dataframe(top_10_distu)
#           st.subheader("Users: Based on brands")
#           st.dataframe(mod_user)
#           
# 
#          
#

