
def ShowResult():
import requests
import csv 
from flask import Flask, render_template, url_for
import os
import json
import pandas as pd
import uuid
import sys
import stat
import json
import warnings
import base64
import time
import random

import io
import base64

#plotting
from matplotlib import pyplot
import seaborn as sns

warnings.filterwarnings("ignore")


from matplotlib.pyplot import figure
import mpld3


file = "C:\\Users\\oskar\\OneDrive - Danmarks Tekniske Universitet\\Kandidat Speciale\\Programmering\\LCAbyg_API\\api_out\\result_json.json"
f = open(file)
f_load = json.load(f)

building_id = '6d766aa5-50aa-4005-ab35-29f2fb82ddad'

results = f_load['results'][building_id]['SumNew']['9999']

df = pd.DataFrame((results).items(), columns=['Impact Categories', 'Value total'])

with open("C:\\Users\\oskar\\OneDrive - Danmarks Tekniske Universitet\\Kandidat Speciale\\Programmering\\RevitQuantities\\Building.txt") as f:
    contents = f.read()

gfa = float(contents.split(",")[1])

df['Value / m2 / year'] = round(df['Value total']/(gfa*50),2)

a4_dims = (15, 5)

fig, ax = pyplot.subplots(figsize=a4_dims)

sns.barplot(ax = ax, data=df, x="Impact Categories", y="Value / m2 / year")

a4_dims = (15, 5)

fig, ax = pyplot.subplots(figsize=a4_dims)

sns.barplot(ax = ax, data=df, x="Impact Categories", y="Value total")

#set seaborn plotting aesthetics

# import matplotlib.pyplot as plt



# df['Value / m2 / year'] = round(df['Value total']/(gfa*50),2)

# df['Walls'] = df["Value / m2 / year"]/0.3
# df['Floor'] = df["Value / m2 / year"]/0.2
# df['Roof'] = df["Value / m2 / year"]/0.25
# df['Ceiling'] = df["Value / m2 / year"]/0.25

# df_new = df[['Impact Categories','Walls','Floor','Roof','Ceiling']]

# a4_dims = (15, 5)
# sns.set(style='white')

# #create stacked bar chart
# df_new.set_index('Impact Categories').plot(kind='bar', stacked=True, color=['steelblue', 'red', 'orange', 'green'],figsize= (15, 5))

# #add overall title
# plt.title('Impact by element category', fontsize=16)

# #add axis titles
# plt.xlabel('Impact Categories')
# plt.ylabel('Impact')

# #rotate x-axis labels
# plt.xticks(rotation=45)

# fig = plt.show()

def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)

    return base64.b64encode(img.getvalue())

encoded = fig_to_base64(fig)
my_html = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))
###

my_html


# a4_dims = (15, 5)

# fig = figure()

# ax = fig.gca(figsize=a4_dims)

# sns.barplot(ax = ax, data=df, x="Impact Categories", y="Value total")



