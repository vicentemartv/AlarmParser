import yaml
import pandas as pd
import csv
import streamlit as st
from dotenv import load_dotenv
import os
from utils import queryMachineRefs, getSources, identifySources, getsourceId, getsourceConfig

load_dotenv()
api_key = os.getenv('deacero_api_key')
st.write("Hola Perrosssss")

if api_key:
    st.write("API Key loaded successfully!")
else:
    st.write("Failed to load API Key.")

headers = {'Authorization': f'Bearer {api_key}',
           'Content-type': 'application/json'}


#File loader to upload a csv file
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    alarms = []
    alarms_df = pd.read_csv(uploaded_file,encoding='ISO-8859-1')
    #drop index
    alarms_df = alarms_df.drop(columns=['Unnamed: 4'])
    alarms_df.type = alarms_df.type.astype("category")
    alarms_df.type = alarms_df.type.cat.set_categories(["FAULT", "WARNING"], ordered=True)
    #drop index column
    #alarms_df = alarms_df.drop(columns=['index'])


    #display df in an editable table
    st.data_editor(alarms_df,num_rows="dynamic")

    for index, row in alarms_df.iterrows():
        code = row['code']
        message = row['message']
        alarm_type = row['type']
        data_key = row['value']
        fault_value = f"{data_key} == 1"

#Section Break and new Title
machineRefs_df = queryMachineRefs(headers)
st.write("Get Machine config")
#Create a Selector to choose a machine name
machine_name = st.selectbox("Select a machine", machineRefs_df['name'])
#get the machineRef for the selected machine name
machineId_selected = machineRefs_df[machineRefs_df['name'] == machine_name]['machineId'].values[0]
st.write(machineId_selected)

st.write(identifySources(machine_name, getSources(machineId_selected, headers)))

#Source Selector
st.write("Get Source config")
sources = getSources(machineId_selected, headers)
sourceNames = []
for source in sources:
    sourceId = source['adapterBinding']['adapterIntegration']['displayName']
    sourceNames.append(sourceId)

source_name = st.selectbox("Select a source", sourceNames)

#Display the config of the selected source
sourceId = getsourceId(sources, source_name)
sourceConfig = getsourceConfig(sourceId)
st.write(sourceConfig)
