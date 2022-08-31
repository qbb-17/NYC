# Importamos las librerías 
import pandas as pd
import streamlit as st
import numpy as np
import codecs

st.title('City bike Proyect')
# Cargamos nuestra base de datos

DATA_URL = ('citibike-tripdata.csv')
DATE_COLUMN = 'started_at'
LAT = 'start_lat'
LON = 'start_lng'

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename({'start_lat': 'lat', 'start_lng': 'lon'}, axis=1, inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(500)
data_load_state.text("Done! (using st.cache)")
st.dataframe(data)

if st.sidebar.checkbox("Show row data"): 
    st.subheader("Raw data")
    st.write(data)

if st.sidebar.checkbox("Recorridos por hora"):
    st.subheader("Número de recorridos por hora")

    hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins = 24, range = (0, 24)) [0]
    st.bar_chart(hist_values)

# Creamos el slider 
hour_to_filter = st.sidebar.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)

map_data = pd.DataFrame(
    columns=["lat", "lon"])
st.map(filtered_data)


