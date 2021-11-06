# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 10:44:03 2021

@author: Lukas
"""

# Import libraries
# %matplotlib inline

# %%

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# import data and convert Datum to a datetime value
path = 'velozahlungen-stadt-stgallen.csv'
df_velo = pd.read_csv(path, sep=';')

df_velo['Datum'] = pd.to_datetime(df_velo['Datum'], utc=True).dt.tz_localize(None)
df_velo.sort_values(by=['Datum'], inplace=True)
#print(df_velo.head(2))

# only include the location with the most data
sorted_locations = df_velo.groupby(['Bezeichnung']).size().sort_values(ascending=False)
print(sorted_locations)

max_count_bezeichnung = sorted_locations.first_valid_index()
df_velo_one_location = df_velo.loc[df_velo['Bezeichnung']==max_count_bezeichnung]
df_velo_one_location.sort_values(by=['Datum'], inplace=True)
df_velo_one_location.reset_index(drop=True, inplace=True)
print(df_velo_one_location)

# Group data by month and year
df_velo_year_template = df_velo_one_location.copy()
df_velo_one_location['month'] = df_velo_one_location['Datum'].dt.month
df_velo_one_location['year'] = df_velo_one_location['Datum'].dt.year

df_velo_one_location['Anzahl Velos'] = df_velo_one_location.groupby(['month', 'year'])['Anzahl Velos'].transform('sum')
df_velo_one_location.drop_duplicates(['month', 'year'], inplace=True)
print(df_velo_one_location)
df_velo_one_location.plot(x='Datum', y='Anzahl Velos')
#df_velo_one_location.loc[mask].plot(figsize=(15,5), ylabel='Energy Export [Wh]')
# %%




# %%
df_velo_year = df_velo_year_template
df_velo_year['year'] = df_velo_year['Datum'].dt.year
df_velo_year['Anzahl Velos'] = df_velo_year.groupby(['year'])['Anzahl Velos'].transform('sum')
df_velo_year.drop_duplicates(['year'], inplace=True)

# drop first year, since there isn't data for the whole year
df_velo_year = df_velo_year.iloc[1: , :]
ax = df_velo_year.plot(x='year', y='Anzahl Velos')

# Generate train & test data
from sklearn.model_selection import train_test_split
df_velo_year['amount_velos'] = df_velo_year['Anzahl Velos']
X_train, X_test = train_test_split(df_velo_year, test_size=0.2, random_state=42)

import statsmodels.formula.api as smf

# linear regression
mod_linear = smf.ols(formula='amount_velos ~ year', data=X_train)
res_linear = mod_linear.fit()
df_velo_year['linear regression'] = res_linear.params.Intercept + df_velo_year['year'] * res_linear.params.year
#print(res_linear.summary())
ax2 = df_velo_year.plot(x='year', y='linear regression', color='red', ax=ax)

#quadratic regression
mod_quadratic = smf.ols(formula='amount_velos ~ year + np.square(year)', data=X_train)
res_quadratic = mod_quadratic.fit()
df_velo_year['quadratic regression'] = res_quadratic.params.Intercept + df_velo_year['year'] * res_quadratic.params.year + np.square(df_velo_year['year']) * res_quadratic.params['np.square(year)']
#print(res_quadratic.summary())
df_velo_year.plot(x='year', y='quadratic regression', color='green', ax=ax2)

# %%
