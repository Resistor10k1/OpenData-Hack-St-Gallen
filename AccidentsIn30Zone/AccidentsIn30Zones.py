from shapely.geometry import Point, Polygon
import pandas as pd
import json
import geopandas
import plotly.express as px

path= "tempo-30-zonen.csv"
df_zones=pd.read_csv(path, sep=';')

zones_as_json = []
for x in df_zones['Geo Shape']:
    zones_as_json.append(json.loads(x))

list_of_zones_as_polynoms = []

for i, zone in zip(range(len(zones_as_json)), zones_as_json):
    print(i, len(zone['coordinates'][0]),zone['coordinates'][0])
    if(len(zone['coordinates'][0]) == 1):
        list_of_zones_as_polynoms.append(Polygon(shell=zone['coordinates'][0][0], holes=zone['coordinates'][1]))
    else:
        list_of_zones_as_polynoms.append(Polygon(shell=zone['coordinates'][0]))

df_Accidents = pd.read_csv(
    "/OpenData-Hack-St-Gallen/Data/converted_Raod_Traffic_Accident_Locations.csv", sep=',')

list_of_accidents_as_points = []

for log,lat in zip(df_Accidents['Longitude'],df_Accidents['Latitude']):
    list_of_accidents_as_points.append(Point([log,lat]))

geoJason = geopandas.GeoSeries([list_of_zones_as_polynoms[0]]).__geo_interface__

with open("Test.json", 'w') as file_out:
    file_out.write(str(geoJason).replace('\'','\"'))
print(geoJason)
