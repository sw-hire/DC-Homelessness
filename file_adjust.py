import geopandas as gpd
import pandas as pd

########################## DEMOGRAPHICS DATA ORGANIZE
dc_acs = gpd.read_file("District_of_Columbia/ACS_5-Year_Demographic_Characteristics_DC_Ward.shp")
dc_econ = gpd.read_file("District_of_Columbia/ACS_5-Year_Economic_Characteristics_DC_Ward.shp")
#print(dc_econ.columns)
#verifying geopandas df
#print(type(dc_acs))

#couldnt find % in pov for some reason, checking column
column = dc_econ.get('DP03_0128PE')
if column is not None:
    print("Column exists!")
else:
    print("Column not found.")
    #found that column was actually under 'DPO3_0128P' not 'DP03_0128PE'

#separate percentage of pop. in poverty [DP03_0128P]
#and amt. of people unemployed/not in work force [DP03_0007E]
pov_col = dc_econ[['GEOID', 'DP03_0128P', 'DP03_0007E']]

#left join to demographics dataframe
dc_acs = dc_acs.merge(pov_col, on='GEOID', how='left')

#check crs
#print(dc_acs.crs)
#currently 3857, need to transform



#now only keeping relevant columns (geom, black/AA population, race total population, under 18, unemployed, percent of people under poverty line)
clean_dc = dc_acs[['GEOID', "geometry", 'NAMELSAD', 'DP05_0038E', 'DP05_0033E', 'DP05_0019E', 'DP03_0007E', 'DP03_0128P']]
clean_dc.columns = ['geoid', "geometry", 'ward_name', 'black_pop', 'total_pop', 'under_18', 'unemployed', 'percent_pov']

clean_dc = clean_dc.to_crs(epsg=4326)
#print(clean_dc.crs)
#print(clean_dc.bounds)


########################## SHELTER DATA ORGANIZE
shelters_dc = gpd.read_file("District_of_Columbia/Homeless_Shelter_Locations.shp")
print(shelters_dc.columns)

print(type(shelters_dc))

shelters = shelters_dc[['NAME','ADDRESS','WARD','NUMBER_OF_','LATITUDE','LONGITUDE', 'geometry']].copy()
shelters.columns = ['Name','Address','Ward','Bed Count','Latitude','Longitude', 'geometry']
print(type(shelters))

#need bed count values also cleaned for markers in streamlit
shelters.dropna(subset=['Latitude','Longitude', 'Bed Count'])
shelters['Bed Count'] = pd.to_numeric(shelters['Bed Count'], errors='coerce')

##prepping for circle markers

#only drop full coordinate duplicates:
shelters = shelters.drop_duplicates(subset=['Latitude','Longitude'])
shelters = shelters.to_crs('EPSG:4326') #just in case

########################## BATHROOM DATA ORGANIZE
import requests

# Define the URL to the ArcGIS Feature Server
url = "https://services9.arcgis.com/6EuFgO4fLTqfNOhu/arcgis/rest/services/DC_Public_Restrooms_v2/FeatureServer/0/query?where=1=1&outFields=*&f=geojson"

restrooms = gpd.read_file(url)
