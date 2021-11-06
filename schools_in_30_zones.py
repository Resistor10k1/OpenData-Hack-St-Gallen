
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
from shapely.geometry import Point, Polygon
import json
warnings.filterwarnings('ignore')

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
    if (i != 20) and (i != 47) and (i != 52 and (i != 58)):
        zones.append(Polygon(one_json['coordinates'][0]))
        
    i=i+1

path2="einzugsgebiet-der-primar-und-sekundarschulen-stgallen.csv"
df_schools = pd.read_csv(path2, sep=';')

schools = []
for oneSchool in df_schools['Geo Point']:
    p_e, p_n = oneSchool.split(',')
    p_e = float(p_e)
    p_n = float(p_n)
    schools.append(Point(p_n, p_e))

def pointFromString(theString):
    p_e, p_n = theString.split(',')
    p_e = float(p_e)
    p_n = float(p_n)
    return Point(p_n, p_e)

df_schools['in zone'] = False

for index, row in df_schools.iterrows():
    for pol_zones in zones:
        if pointFromString(row['Geo Point']).within(pol_zones):
            row['in zone'] = True
            break

print(df_schools)