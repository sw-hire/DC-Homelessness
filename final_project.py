import streamlit as st
import geopandas as gpd
import pandas as pd
#from shapely.geometry import Point
import folium
from streamlit_folium import folium_static
from file_adjust import clean_dc as dc
from file_adjust import shelters



## Setup
st.header("Tracking Homelessness and Access to Resources")
tab1, tab2, tab3 = st.tabs(["Context", "Interactive Map", "Next Steps"])

## PAGE 1: Intro
with tab1:
    st.write("Intro about homelessness, DC, how hard it is to track it")


## PAGE 2: Map
with tab2:
    dc_center = [38.9072, -77.0369]
    m = folium.Map(location=dc_center, zoom_start=11)
    folium_static(m)

## PAGE 3: Next
with tab3:
    st.write("Potential ways to 'find' homelessness")
