from shapely.geometry import Point, Polygon
import pandas as pd
import json
import plotly.graph_objects as go

import plotly.express as px


def convertToGeoJSON(list_of_polynomes, type = "Polygon"):
    list_of_plynomes_in_GeoJson = []
    for ploynomes in list_of_polynomes:
        if type == "Polygon":
            json_as_python_struct = {"type":type,"coordinates":[]}
            json_list_of_poynomes = []
            for cordinates in ploynomes.exterior.coords:
                json_list_of_poynomes.append([cordinates[0],cordinates[1]])
            json_as_python_struct["coordinates"].append(json_list_of_poynomes)
            list_of_plynomes_in_GeoJson.append(json_as_python_struct)
        else:
            json_as_python_struct = {"type": type, "coordinates": []}
            json_as_python_struct["coordinates"].append(ploynomes.coords[0][0])
            json_as_python_struct["coordinates"].append(ploynomes.coords[0][1])
            list_of_plynomes_in_GeoJson.append(json_as_python_struct)

    return list_of_plynomes_in_GeoJson

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
    "/Users/tobiasrothlin/Downloads/OpenDataPreStudy/OpenData-Hack-St-Gallen/Data/converted_Raod_Traffic_Accident_Locations.csv", sep=',')

list_of_accidents_as_points = []



for log,lat in zip(df_Accidents['Longitude'],df_Accidents['Latitude']):
    for zones in list_of_zones_as_polynoms:
        list_of_accidents_as_points.append(Point([log, lat]))


polynome_as_GeoJSON = convertToGeoJSON(list_of_zones_as_polynoms)
points_as_GeoJSON = convertToGeoJSON(list_of_accidents_as_points, "Point")

list_of_zones = []
list_of_points = []


for zone in polynome_as_GeoJSON:
    list_of_zones.append( {
        'type': "Feature",
        'geometry': zone
    })

for accident in points_as_GeoJSON:
    list_of_points.append( {
        'type': "Feature",
        'geometry': accident
    })

with open("polys.json", "w", encoding="UTF-8") as outploy:
    outploy.write(json.dumps({
                    'type': "FeatureCollection",
                    'features': list_of_points
                }))

fig = go.Figure(go.Scattermapbox(
    mode = "markers",
    lon = [-73.605], lat = [45.51],
    marker = {'size': 20, 'color': [px.colors.cyclical.IceFire]})
)

fig.update_layout(
    mapbox = {
        'style': "open-street-map",
        'center': { 'lon': 9.357011294188844, 'lat': 47.42184687949817},
        'zoom': 12, 'layers': [{
            'source': {
                'type': "FeatureCollection",
                'features': list_of_zones
            },
            'type': "fill", 'below': "traces", 'color': "#BDCC94",'opacity':0.5},
            {
                'source': {
                    'type': "FeatureCollection",
                    'features': list_of_points
                },
                'type': "circle", 'below': "traces", 'color': "#FF665A",
                'opacity': 0.2}
        ]},
    margin = {'l':0, 'r':0, 'b':0, 't':0},
    mapbox_style =  'mapbox://styles/mapbox/light-v10',
    mapbox_accesstoken = "pk.eyJ1IjoidG9iaWlpIiwiYSI6ImNrdm54OGppazVvazgzM29rOXo0bjRuaW0ifQ.AvQNkchw1ICRC7fjhUpB4A"
)
fig.show()