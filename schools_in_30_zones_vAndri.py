
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
from shapely.geometry import Point, Polygon
import json
warnings.filterwarnings('ignore')

import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'

path1='tempo-30-zonen.csv'
df_zones=pd.read_csv(path1, sep=';')
print(type(df_zones['Geo Shape'][0]))

jsons = []

for x in df_zones['Geo Shape']:
    jsons.append(json.loads(x))

zones = []
i = 0
for one_json in jsons:
    #print(i)
    # for some reason, these rows don't work. Possibly, because there is a hole in the Geo Shape?
    if (i != 20) and (i != 47) and (i != 52) and (i != 58):
        zones.append(Polygon(one_json['coordinates'][0]))
        
    i=i+1

path2="data/schulhaeuser.csv"
df_schools = pd.read_csv(path2, sep=';')

schools = []
latitude = []
longitude = []
for oneSchool in df_schools['Geo Point']:
    p_e, p_n = oneSchool.split(',')
    p_e = float(p_e)
    p_n = float(p_n)
    schools.append(Point(p_n, p_e))
    latitude.append(p_e)
    longitude.append(p_n)
# for oneSchool in df_schools['Geo Point']:
#     p_n, p_e = oneSchool.split(',')
#     p_e = float(p_e)
#     p_n = float(p_n)
#     schools.append(Point(p_e, p_n))
#     latitude.append(p_n)
#     longitude.append(p_e)

def pointFromString(theString):
    p_n, p_e = theString.split(',')
    p_e = float(p_e)
    p_n = float(p_n)
    return Point(p_e, p_n)

df_schools['in zone'] = False

for index, row in df_schools.iterrows():
    for pol_zones in zones:
        if pointFromString(row['Geo Point']).within(pol_zones):
            row['in zone'] = True
            break

print(df_schools)
farb = []
for i in range(len(latitude)):
    farb.append(156)

fig = px.scatter_mapbox(lat=latitude, lon=longitude, text=df_schools['Schulhaus'],
                  size_max=15, zoom=12, mapbox_style="carto-positron", color=farb)
#fig.show()
lon, lat = zones[0].exterior.xy
# print(lon, lat)
#fig2 = px.line_mapbox(lat=lat, lon=lon, zoom=10, mapbox_style="carto-positron")

for zone in zones:
    lon, lat = zone.exterior.xy
    tmp = px.line_mapbox(lat=lat, lon=lon, zoom=12, mapbox_style="carto-positron")
    fig.add_trace(tmp.data[0])
    fig.update_layout(mapbox_style='carto-positron')
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

fig.show()

# fig.add_trace(fig2[0])
# fig.update_layout(mapbox_style='carto-positron')
# fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

# fig.show()
    
    