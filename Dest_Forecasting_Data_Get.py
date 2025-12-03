import streamlit as st
import pandas as pd
from datetime import date

# Model Exc File
from arima_model import ARIMA_MD 
from knn_model import KNN_MD

def Dest_Forecastig_Data_Get(dfs_comb:pd.DataFrame,flights:pd.DataFrame): # Get users destination data once orgin and data have been specified
    if st.session_state['sel_org'] != None and st.session_state['sel_Arv_dte'] != None:
        
        # Grab Past Location Data from Data Set
        LocData = dfs_comb[dfs_comb['Location_Name'] == st.session_state['sel_locN']]
        
        # Building Meta data used for KNN and ARIMA models 
        MetaData = LocData[['Country','City','Location_ID','Location_Name','Type_of_Attraction','Attraction_Category','Latitude','Longitude']].drop_duplicates().reset_index(drop=True).loc[0]
        
        # Get Forcast data for th enext 180 day from trim point Sept 30 2025 to 180 days later from today
        FC = ARIMA_MD(MetaData['Location_ID'],MetaData['Latitude'],MetaData['Longitude']) # Get Forecast for POI
        
        FC['Date'] = FC['Date'].apply(lambda x : pd.Timestamp(x).date())#datetime.date(YYYY, MM, DD)
        
        st.session_state['FC_sel_Dest'] = FC # save to sesssion state]
        
        # Filter fligth paths with FC in mind     
        flgData1 = flights[(flights['City_dp'] == st.session_state['sel_org']) & 
                          (flights['City_ds'] == MetaData['City']) & 
                          (flights['apt_time_dt_ds'] >= date.today()) & 
                          (flights['apt_time_dt_ds'] <= FC['Date'].loc[len(FC)-1])]
        st.session_state['Flght_sel_Dest'] = flgData1 # save to sesssion state
        
        #Buidling the new row for KNN model, needed for building input
        NEwR = [MetaData['Country'],
                MetaData['City'],
                '-', # What we are predicting for recommending
                MetaData['Location_Name'],
                MetaData['Type_of_Attraction'],
                MetaData['Attraction_Category'],
                MetaData['Latitude'],
                MetaData['Longitude'],
                st.session_state['sel_Arv_dte'],
                FC['Avg_Daily_Pedestrian_Count'].loc[FC['Date'] == st.session_state['sel_Arv_dte']],
                FC['Holiday'].loc[FC['Date'] == st.session_state['sel_Arv_dte']],
                FC['Weather_Temperature_Avg'].loc[FC['Date'] == st.session_state['sel_Arv_dte']],
                FC['Weather_Wind_Speed_Avg'].loc[FC['Date'] == st.session_state['sel_Arv_dte']],
                FC['Weather_Precipitation_Sum'].loc[FC['Date'] == st.session_state['sel_Arv_dte']],
                FC['Weather_Relative_Humidity_Avg'].loc[FC['Date'] == st.session_state['sel_Arv_dte']]]
        RC = KNN_MD(NEwR,dfs_comb,MetaData['Location_ID']) # Get recommended areas with less crowd
        
        st.session_state['RC_alt_Dest'] = RC # save to sesssion state

        # Filter fligth paths with RC in mind
        flgData2 = flights[(flights['City_dp'] == st.session_state['sel_org']) & 
                          (flights['City_ds'] == RC['City']) & 
                          (flights['apt_time_dt_ds'] >= date.today()) & 
                          (flights['apt_time_dt_ds'] <= RC['Date'])]
        st.session_state['Flght_alt_Dest'] = flgData2 # save to session state
    else: # If user deselects one of the options reset save states 
        st.session_state['FC_sel_Dest'] = pd.DataFrame()
        st.session_state['Flght_sel_Dest'] = pd.DataFrame()
        st.session_state['RC_alt_Dest'] = pd.DataFrame()
        st.session_state['Flght_alt_Dest'] = pd.DataFrame()