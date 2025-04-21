import streamlit as st
#import geopandas as gpd
#import pandas as pd
#from shapely.geometry import Point
import folium
from streamlit_folium import folium_static
from file_adjust import clean_dc as dc
from file_adjust import shelters
from file_adjust import restrooms

##makes a choropleth for each demographic charactersitic


## Setup
st.header("Tracking Homelessness and Access to Resources")
tab1, tab2 = st.tabs(["Context", "Interactive Map"])

## PAGE 1: Intro
with tab1:
    st.write("Hello! I'm Swasti Hiremani, and this is my final project for UT535.")
    st.write(
        "Homelessness can be really hard to measure because it often doesn’t look the same for everyone. Some people might live in shelters, while others stay with friends, in cars, or on the streets, so it's easy to miss them in official counts.")
    st.write(
        "This model used demographic data that ranks high in relating to experiencing homelessness (especially in Washington D.C.), but the fact is that even with all the population metrics, there is a lack of data around tracking the general locations of homeless people. Most of this data is information you'd only have if you were a resident familiar with the neighborhood; otherwise, its harder to find. Initially, this project wanted to examine the proximity of public resources (like bathrooms) to homeless populations, but noticing proximity is hard when you don't have an initial location.")
    st.write(
        "Location data on homelessness could be an incredibly powerful tool for planners and policy makers to have a bigger impact. However, there is still the obvious moral dilemma of tracking the location of these people. Should we prioritize the policy or individual privacy? This question is a tricky one, but it also cannot be answered with numbers alone, and requires an understanding of the community, first and foremost.")

## PAGE 2: Map
with tab2:

    dc_center = [38.9072, -77.0369]
    m = folium.Map(location=dc_center, zoom_start=11)

    show_restrooms = st.checkbox("Show Public Restrooms", value=False)

    gradient_layer = st.selectbox(
        "Select Demographic:",
        ("", "Black Population per Ward", "Unemployed Population", "Percent of Population in Poverty")
    )

    url = "https://www.thepermanentejournal.org/doi/10.7812/TPP/22.096#abstract"
    st.write("According to an [article](%s) in the Permanente Journal, some of the strongest geographic-level variables positively associated with homelessness risk include: percent of the population Black, unemployed, and in poverty." % url)

    if gradient_layer == "Black Population per Ward":
        blackpop_map = folium.Choropleth(
            geo_data=dc,
            data=dc,
            columns=['ward_name', 'black_pop'],
            key_on='feature.properties.ward_name',
            fill_color='PuRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Black Population per Ward',
            show=True
        )
        blackpop_map.add_to(m)
        folium.GeoJson(
            dc,
            name='Black Population Data',
            style_function=lambda feature: {
                'fillColor': 'transparent',
                'color': 'black',
                'weight': 1
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['ward_name', 'black_pop'],
                aliases=['Ward:', 'Black Population:'],
                localize=True
            )
        ).add_to(m)
    if gradient_layer == "Unemployed Population":
        employment_map = folium.Choropleth(
            geo_data=dc,
            data=dc,
            columns=['ward_name', 'unemployed'],
            key_on='feature.properties.ward_name',
            fill_color='Reds',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Unemployment Rate per Ward',
            show=True
        )
        employment_map.add_to(m)
        folium.GeoJson(
            dc,
            name='Unemployment Data',
            style_function=lambda feature: {
                'fillColor': 'transparent',
                'color': 'black',
                'weight': 1
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['ward_name', 'unemployed'],
                aliases=['Ward:', 'Unemployed #:'],
                localize=True
            )
        ).add_to(m)

    if gradient_layer == "Percent of Population in Poverty":
        poverty_map = folium.Choropleth(
            geo_data=dc,
            data=dc,
            columns=['ward_name', 'percent_pov'],
            key_on='feature.properties.ward_name',
            fill_color='Blues',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Percentage of Population in Poverty',
            show=True
        )
        poverty_map.add_to(m)

        folium.GeoJson(
            dc,
            name='Poverty Data',
            style_function=lambda feature: {
                'fillColor': 'transparent',
                'color': 'blue',
                'weight': 1
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['ward_name', 'percent_pov'],
                aliases=['Ward:', 'Poverty %:'],
                localize=True
            )
        ).add_to(m)


    ##create circle markers for every shelter in dataframe
    #goes through the shelter data set and makes marker for every shelter
    ##also! radius is number of beds
    for i, row in shelters.iterrows():
        lat = row['Latitude']
        lon = row['Longitude']
        name = row['Name']
        address = row['Address']
        bed_count = row['Bed Count']
        radius = bed_count * 0.025 #5 meters per bed, trying to measure "spread" but keep it within bounds of map


        #create tag for each shelter for interactivity
        tagtext = f"{name}\n{address}\nBeds: {bed_count}"
        shelter_tag = folium.Popup(tagtext)


        #create tag for i shelter in df and attach to OG map
        folium.CircleMarker(
            location=[lat, lon],
            popup=shelter_tag,
            radius=radius,
            fill_color='blue',
            fill_opacity=0.7,
        ).add_to(m)

    ##repeating the process for every restroom
    if show_restrooms:
        for _, r in restrooms.iterrows():
            lat, lon = r.geometry.y, r.geometry.x
            name = r["NAME"]
            address = r["ADDRESS"]

            popup_html = (
                f"<b>{name}</b><br>"
                f"{address}<br>"
            )
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=250),
                icon=folium.Icon(color='blue', icon='info-sign'),
            ).add_to(m)
    st.title("Map Homelessness and Access to Resources in D.C.")

    folium_static(m)

    st.write("Note: Shelter locations were used as a point of reference for homelessness. The radius for each shelter is the number of beds in that shelter; this was done to essentially 'estimate' where homeless people will likely be.")
    st.write("However, as you might be able to tell, there are more homeless people than there are beds in shelters. So, where can we find them on this map?")
    st.write()
