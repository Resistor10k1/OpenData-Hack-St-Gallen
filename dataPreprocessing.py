# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 10:25:44 2021

@author: Andri Trottmann
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


path = "data/velozaehlungen-stadt-stgallen.csv"

df_bikes = pd.read_csv(path, sep=';')
df_bikes['Datum'] = pd.to_datetime(df_bikes['Datum'])
df_bikes.sort_values(by=['Datum'], inplace=True)

sorted_locations = df_bikes.groupby(['Bezeichnung']).size().sort_values(ascending=False)
print(sorted_locations)
