import requests
import json
import pandas as pd
import plotly.express as px

def convert(ost,nord):
    url = "https://geodesy.geo.admin.ch/reframe/navref?format=json&easting="+ str(ost)+"&northing="+str(nord)+"&altitude=NaN&input=lv95&output=etrf93-ed"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    res = json.loads(response.text)
    print(ost,res['easting'],sep="->", end="    |   ")
    print(nord,res['northing'],sep="->")
    return (float(res['easting']),float(res['northing']))


convert(2682382.000,1246980.000)

easting = []
northing = []
road_traffic_accident_locations = pd.read_csv("RoadTrafficAccidentLocations.csv")
road_traffic_accident_locations_in_stGallen = road_traffic_accident_locations[road_traffic_accident_locations["MunicipalityCode"] == 3203]


for east,north in zip(road_traffic_accident_locations_in_stGallen['AccidentLocation_CHLV95_E'],road_traffic_accident_locations_in_stGallen['AccidentLocation_CHLV95_N']):
    print(east,north, sep="|")
    res = convert(float(east),float(north))
    easting.append(res[0])
    northing.append(res[1])

fig = px.scatter_mapbox(lat=northing, lon=easting,
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                  mapbox_style="carto-positron")

fig.show()

new_CSV_Columns = ['AccidentUID','AccidentType','AccidentType_en','AccidentSeverityCategory','AccidentSeverityCategory_en','AccidentInvolvingPedestrian','AccidentInvolvingBicycle','AccidentInvolvingMotorcycle','RoadType','AccidentYear','AccidentMonth','AccidentMonth_en','AccidentWeekDay','AccidentWeekDay_en','AccidentHour','AccidentHour_text', 'Longitude','Latitude']

with open('converted_Raod_Traffic_Accident_Locations.csv', 'w', encoding='UTF-8') as output_file:
    for header_name in new_CSV_Columns[:-1]:
        output_file.write(header_name + ",")

    output_file.write(new_CSV_Columns[-1] + "\n")

    for i in range(len(easting)):
        for header_name in new_CSV_Columns[:-2]:
            output_file.write(str(road_traffic_accident_locations_in_stGallen[header_name].tolist()[i])+ ",")
        output_file.write(str(easting[i]) + "," + str(northing[i]) + "\n")