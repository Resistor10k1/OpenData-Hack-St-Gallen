# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 10:25:44 2021

@author: Andri Trottmann
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import wgs84_ch1903
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'


def euclidean_distance(x1, y1, x2, y2):
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)


converter = wgs84_ch1903.GPSConverter()


# Wahrgenommene Sicherheit data
path = "data/wahrgenommene-sicherheit-stadt-stgallen-streetwise.csv"

df_savety = pd.read_csv(path, sep=';', usecols=['name', 'score', 'lat', 'lng'])

for i in range(len(df_savety['lat'])):
    lat = 1000000+converter.WGStoCHx(
        df_savety.loc[i, 'lat'], df_savety.loc[i, 'lng'])
    lng = 2000000+converter.WGStoCHy(
        df_savety.loc[i, 'lat'], df_savety.loc[i, 'lng'])
    df_savety.loc[i, 'lat'] = lat
    df_savety.loc[i, 'lng'] = lng

df_savety.sort_values(by=['score'], inplace=True)

sorted_pos = df_savety.groupby(['lat', 'lng']).size().sort_values(
    ascending=False)
print(f"Wahrgenommene Sicherheit: {sorted_pos}")


# Strassenunfälle
path = "data/RoadTrafficAccidentLocations.csv"

useCols = ['AccidentLocation_CHLV95_E', 'AccidentLocation_CHLV95_N',
           'MunicipalityCode', 'AccidentInvolvingPedestrian',
           'AccidentInvolvingBicycle', 'AccidentInvolvingMotorcycle']
df_accidents = pd.read_csv(path, sep=',', usecols=useCols)
# Quelle: ch.postleitzahl.org
df_accidents = df_accidents.loc[df_accidents['MunicipalityCode'] == 3203]

df_bikeAccidents = df_accidents.loc[df_accidents['AccidentInvolvingBicycle']
                                    == True]
df_pedAccidents = df_accidents.loc[df_accidents['AccidentInvolvingPedestrian']
                                   == True]

sorted_pos = df_bikeAccidents.groupby(['AccidentLocation_CHLV95_E',
                                   'AccidentLocation_CHLV95_N']
                                  ).size().sort_values(ascending=False)
print(f"Bikes accidents: {sorted_pos}")
sorted_pos = df_pedAccidents.groupby(['AccidentLocation_CHLV95_E',
                                   'AccidentLocation_CHLV95_N']
                                  ).size().sort_values(ascending=False)
print(f"Pedestrian accidents: {sorted_pos}")

# Einzugsgebiet der Schulen
path = "data/Schulhaeuser.csv"
df_school = pd.read_csv(path, sep=';')
# df_school.drop(index=[(df_school['Bezeichnun'] ==
#                        'Einzugsgebiet mehrerer Primarschulen').index])

# print(df_school['Bezeichnun'])
# schools = {
#     'Kreuzbühl': [47.40254976460495, 9.301708922917635],
#     'Hof': [47.404989652645156, 9.319475875188022],
#     'Boppartshof': [47.40394400024585, 9.337199912234537],
#     'Engelwies': [47.41187361203905, 9.333770931522256],
#     'Feldli': [47.421853101081794, 9.351804429348496],
#     'Schoren': [47.423017608437206, 9.358232106576336],
#     'Oberzil': [47.441414168607665, 9.410484378398161],
#     'Krontal': [47.43407291241994, 9.398381283952077],
#     'Grossacker': [47.42978391532983, 9.397143455115977],
#     'Riethüsli': [47.41142543322925, 9.365512432330524],
#     'Spelterini': [47.42997758124066, 9.3819920412389],
#     'Halden': [47.43469362948038, 9.411573407563768],
#     'Rotmonten': [47.437049235691575, 9.376843680620107],
#     'Gerhalde': [47.438399017198925, 9.387207736111167],
#     'St.Leonhard': [47.42087367452137, 9.369705866223992],
#     'Schönenwegen': [47.4174560133669, 9.351043664905125],
#     'Hebel-Bach': [47.41742658160127, 9.38331111016238],
#     'Bach': [47.41531396977732, 9.388890104836657],
#     'Heimat': [47.43729326013911, 9.390056519205132],
#     'Buchwald': [47.43697032490649, 9.393221525799193],
#     'Ost-Buchental': [47.43794289285501, 9.397832782157222],
#     'Ost-Zil': [47.44619391149103, 9.41412514787836],
#     'Centrum-Bürgli': [47.429846165239184, 9.384313795644339],
#     'Centrum-Blumenau': [47.42840131810485, 9.380501864744096],
#     'West-Engelwies': [47.412578546236645, 9.334951958933095],
#     'West-Schönau': [47.41705073637079, 9.348620495885072],
#     'Timeout-Schule': [47.41452415247862, 9.391390511817823]
#     }


# loc = df_school['Geo Point'][0].split(sep=',')
# print(loc)
# lat = []
# lon = []

# for col in df_school['Geo Point']:
#     loc = col.split(sep=',')
#     lat.append(float(loc[0]))
#     lon.append(float(loc[1]))

# df_school['latitude'] = lat
# df_school['longitude'] = lon

fig = px.scatter_mapbox(df_school, lat='Latitude', lon='Longitude',
                  color_continuous_scale=px.colors.cyclical.IceFire,
                  size_max=15, zoom=10, mapbox_style="carto-positron", text='Schulhaus')
# fig = px.scatter_mapbox(lat=lat, lon=lon,
#                   color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
#                   mapbox_style="carto-positron")

fig.show()


