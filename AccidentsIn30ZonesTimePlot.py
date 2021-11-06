from datetime import datetime
from shapely.geometry import Point, Polygon
import pandas as pd
import json
import plotly.express as px
import os

path= "tempo-30-zonen.csv"
df_zones=pd.read_csv(path, sep=';')
df_zones.set_index('gebiet')

first_accident_year = datetime(year=2011, month=1, day=31)
last_accident_year = datetime(year=2020, month=12, day=1)
df_zones['realisiert'] = pd.to_datetime(df_zones['realisiert'])

# only keep zones, which were established during the measurement of accidents
df_zones = df_zones.loc[(df_zones['realisiert'] > first_accident_year) & (df_zones['realisiert'] < last_accident_year)]

zones_as_json = []

for index, row in df_zones.iterrows():
    zones_as_json.append(json.loads(row['Geo Shape']))

list_of_zones_as_polynoms = []

for i, zone in zip(range(len(zones_as_json)), zones_as_json):
    if(len(zone['coordinates'][0]) == 1):
        list_of_zones_as_polynoms.append(Polygon(shell=zone['coordinates'][0][0], holes=zone['coordinates'][1]))
    else:
        list_of_zones_as_polynoms.append(Polygon(shell=zone['coordinates'][0]))

df_zones['polygon'] = list_of_zones_as_polynoms

path_accidents = os.path.join("Data", "converted_Raod_Traffic_Accident_Locations.csv")

df_Accidents = pd.read_csv(
    path_accidents, sep=',')

list_of_accidents_as_points = []

for log,lat in zip(df_Accidents['Longitude'],df_Accidents['Latitude']):
    list_of_accidents_as_points.append(Point([log,lat]))

df_Accidents['point'] = list_of_accidents_as_points

all_zones_with_points = []

for i_zone, row_zone in df_zones.iterrows():
    points_in_this_zone = {"index":i_zone, "date":row_zone['realisiert'], "name":row_zone['gebiet'], "points": []}
    for i_point, row_point in df_Accidents.iterrows():
        if row_point['point'].within(row_zone['polygon']):
            points_in_this_zone['points'].append({"year":row_point['AccidentYear'], "month":row_point['AccidentMonth']})
    all_zones_with_points.append(points_in_this_zone)


def getFigFromZone(theZone):
    accidents_innenstadt = []
    date_30_innenstadt = 0

    for zone in all_zones_with_points:
        if zone['name']==theZone:
            date_30_innenstadt = zone['date']
            print(zone['name'], zone['date'])
            for point in zone['points']:
                print(point['year'], point['month'])
                accidents_innenstadt.append(datetime(year=point['year'], month=point['month'], day=1))

    amount_before_30 = len(list(filter(lambda l: l < date_30_innenstadt, accidents_innenstadt)))
    years_before_30 = date_30_innenstadt.year - first_accident_year.year
    average_before_30 = amount_before_30 / years_before_30

    amount_after_30 = len(list(filter(lambda l: l > date_30_innenstadt, accidents_innenstadt)))
    years_after_30 = last_accident_year.year - date_30_innenstadt.year
    average_after_30 = amount_after_30 / years_after_30
    print(amount_before_30, amount_after_30)

    labels={
        "y": 'Durchschnittliche Unfälle pro Jahr',
        "x": ''
    }

    fig = px.bar(y=[average_before_30, average_after_30], x=['vor Einführung 30er Zone', 'nach Einführung 30er Zone'], labels=labels)
    return fig

fig_innenstadt = getFigFromZone('Innenstadt')
fig_innenstadt.show()