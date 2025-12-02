import streamlit as st
import pandas as pd


def poisUpdate(dfs_comb:pd.DataFrame) -> pd.DataFrame: # Function handles itinerary changes 
    Query = st.session_state['user_sel'] # grab user current itinerary selection 
    Query = Query[2:] # Date and Orgin not needed 

    # Used for converting text selection options used for crowd and temp levels
    MaxC,MedC,MinC = dfs_comb['Avg_Daily_Pedestrian_Count'].max(),dfs_comb['Avg_Daily_Pedestrian_Count'].median(),dfs_comb['Avg_Daily_Pedestrian_Count'].min()
    MaxT,MedT,MinT = dfs_comb['Weather_Temperature_Avg'].max(),dfs_comb['Weather_Temperature_Avg'].median(),dfs_comb['Weather_Temperature_Avg'].min()
    if Query[2] == None or Query[2] == 'HIGH': 
        Query[2] = MaxC

    if Query[2] == 'MEDIUM' : 
        Query[2] = MedC

    if Query[2] == 'LOW' : 
        Query[2] = (MedC - MinC)/2 + MinC

    if Query[3] == None or Query[3] == 'HIGH': 
        Query[3] = MaxT

    if Query[3] == 'MEDIUM' : 
        Query[3] = MedT

    if Query[3] == 'LOW' : 
        Query[3] = (MedT - MinT)/2 + MinT
    
    # Building the logic needed to get data based on user itinerary selection 
    if Query[0] == None and Query[1] == None: #00
        dfs_c = dfs_comb[(dfs_comb['Avg_Daily_Pedestrian_Count'] <= Query[2]) & 
                         (dfs_comb['Weather_Temperature_Avg'] <= Query[3])]
    
    if Query[0] == None and Query[1] != None: #01
        dfs_c = dfs_comb[(dfs_comb['Type_of_Attraction'] == Query[1]) & 
                         (dfs_comb['Avg_Daily_Pedestrian_Count'] <= Query[2]) & 
                         (dfs_comb['Weather_Temperature_Avg'] <= Query[3])]
        
    if Query[0] != None and Query[1] == None: #10
        dfs_c = dfs_comb[(dfs_comb['Attraction_Category'] == Query[0]) & 
                         (dfs_comb['Avg_Daily_Pedestrian_Count'] <= Query[2]) & 
                         (dfs_comb['Weather_Temperature_Avg'] <= Query[3])]
    
    if Query[0] != None and Query[1] != None: #11
        dfs_c = dfs_comb[(dfs_comb['Attraction_Category'] == Query[0]) &
                         (dfs_comb['Type_of_Attraction'] == Query[1]) &  
                         (dfs_comb['Avg_Daily_Pedestrian_Count'] <= Query[2]) & 
                         (dfs_comb['Weather_Temperature_Avg'] <= Query[3])]
    return dfs_c