# |------------------------------------------------------------------
# | # Geospatial Data Exercise
# |------------------------------------------------------------------
# |
# | This is a notebook for the fifth lesson of the kaggle course
# | ["Geospatial Analysis"](https://www.kaggle.com/learn/geospatial-analysis)
# | offered by Alexis Cook and Jessica Li. The main goal of the lesson is
# | to get used to __Proximity Analysis__, using `geopandas` methods such as
# | `.distance`, `.contains` or `.within`. We also learn how to use
# | `.unary_union` to connect multiple `POLYGON`s into one.

# | ## 1. Task
# |
# | Every year certain amount of toxic chemicals are accidentally
# | released to the environment by industrial facilities and other.
# | Check if at least one monitoring station exists
# | within 2 miles of such events, using the historical record.
# | The information will be used to make a decision where to set up next
# | monitoring stations to fully cover the potential emission events.

# | ## 2. Data
# |
# | 1. Historical record of the releases of toxic chemicals in
# | Philadelphia, Pennsylvania documented by
# | the US Environmental Protection Agency (EPA).
# |
# | 2. Locations of the environmental monitoring stations in Philadelphia,
# | including
# |  the list of chemicals that the station is sensitive.
# |
# | 3. General underlying  map.

# | ## 3. Notebook
# -------------------------------------------------------
# | Import packages.

import folium
import numpy as np
from folium import Marker, GeoJson
from folium.plugins import HeatMap
import pandas as pd
import geopandas as gpd
import plotly.graph_objs as go
from kaggle_geospatial.kgsp import *
import os
from pathlib import Path

# -------------------------------------------------------
# | Set up some directories.

CWD = '/Users/meg/git6/distance/'
DATA_DIR = '../input/geospatial-learn-course-data/'
KAGGLE_DIR = 'alexisbcook/geospatial-learn-course-data'
GEO_DIR = 'geospatial-learn-course-data'

os.chdir(CWD)

set_cwd(CWD)
set_data_dir(DATA_DIR, KAGGLE_DIR, GEO_DIR, CWD)
show_whole_dataframe(True)

# -------------------------------------------------------
# | Read the historic record of the release of the toxic chemicals.

releases_dir = DATA_DIR + 'toxic_release_pennsylvania/toxic_release_pennsylvania/'
releases = gpd.read_file(releases_dir + 'toxic_release_pennsylvania.shp')

print(releases.info())
releases.head(3)

# -------------------------------------------------------
# | Read the locations and sensitive chemicals of monitoring stations.

stations_dir = DATA_DIR + \
    'PhillyHealth_Air_Monitoring_Stations/PhillyHealth_Air_Monitoring_Stations/'
stations = gpd.read_file(
    stations_dir + 'PhillyHealth_Air_Monitoring_Stations.shp')

print(stations.info())
stations.head(3)

# --------------------------------------------------------------------------
# | Let us first play with `releases` record to get familiar with the data.

released_chemicals = releases.groupby(['CHEMICAL', 'UNIT_OF_ME']).sum().loc[:, [
    'TOTAL_RELE']].reset_index(level=1).sort_values('TOTAL_RELE', ascending=False)

print(len(released_chemicals))

# -------------------------------------------------------
# | There are 138 different chemicals recorded in the past.
# | Except 'DIOXIN AND DIOXIN-LIKE COMPOUNDS', which is measured by Grams,
# | the units of all chemicals are Pounds.
# |
# | Let us take a look at yearly record of Dioxin release.

r_dioxin = releases[releases['CHEMICAL'] == 'DIOXIN AND DIOXIN-LIKE COMPOUNDS']
r_dioxin_yearly = r_dioxin.groupby('YEAR').sum()[['TOTAL_RELE']]

# Drop the dioxin record.
r_pounds = releases[releases['CHEMICAL'] != 'DIOXIN AND DIOXIN-LIKE COMPOUNDS']

# -------------------------------------------------------
#  Show it in bar plot.

trace = go.Bar(x=r_dioxin_yearly.index,
               y=r_dioxin_yearly['TOTAL_RELE'])

data = [trace]

layout = go.Layout(height=1024, width=1024,
                   font=dict(size=20),
                   xaxis=dict(title=dict(text='Year')),
                   yaxis=dict(title=dict(
                       text='DIOXIN AND DIOXIN-LIKE COMPOUNDS [Grams]')),
                   showlegend=False)

fig = go.Figure(data=data, layout=layout)

# --
embed_plot(fig, './html/p_1.html')
# --
fig.show()

# -------------------------------------------------------
# | 1. Dioxin release peaked in 2003, and is steadily
# | decreasing since then. The release in 2006 is 0.1 g in total
# | and about 1/7 of the worst year.

# -------------------------------------------------------
# | We shall look at 10 most heavily released chemicals.

released_chemicals_top = released_chemicals.iloc[:10]
r = released_chemicals_top.sort_values('TOTAL_RELE')

trace = go.Bar(y=r.index, x=r['TOTAL_RELE'], orientation='h')
data = [trace]

layout = go.Layout(height=512, width=1280,
                   font=dict(size=20),
                   xaxis=dict(title=dict(
                       text='Most Heavily Emitted Chemicals [Pounds]')),
                   showlegend=False)

fig = go.Figure(data=data, layout=layout)
# --
embed_plot(fig, './html/p_2.html')
# --
fig.show()

# -------------------------------------------------------
# | 1. All-time worst three are
# | - TOLUEN
# | - CUMENE
# | - METHYL ETHYL KETONE
# |

# -------------------------------------------------------
# | How is the trend of the total amount of release?

r_yearly = pd.DataFrame(r_pounds.groupby(['YEAR']).sum()['TOTAL_RELE'])

trace = go.Bar(x=r_yearly.index,
               y=r_yearly['TOTAL_RELE'])

data = [trace]

layout = go.Layout(height=640, width=1280,
                   font=dict(size=18),
                   xaxis=dict(title=dict(text='[Year]')),
                   yaxis=dict(title=dict(text='Total Emission of Chemicals [Pounds]')))

fig = go.Figure(data=data, layout=layout)

# --
embed_plot(fig, './html/p_3.html')
# --
fig.show()

# -------------------------------------------------------
# | 1. An anomaly is seen in 1992. The record this year is
# | apparently incomplete.

# | 2. The total amount of emission of chemicals peaked in 1988, nearly
# | reaching 10 million pounds a year.

# | 3. Since then, the release of toxic chemicals steadily decreased
# | until 2000, to 1 million pounds a year.

# | 4. Last 16 years, the total emission stays about same,
# | ~1 million pounds a year.

# -------------------------------------------------------
# | Show what chemicals were most heavily released in each year.
# | We set the cut-off amount to 10,000 Pounds.

rele_limit = 10_000
r_pounds_limit = r_pounds[r_pounds['TOTAL_RELE'] >= rele_limit]

r_chem_yearly = pd.DataFrame(r_pounds_limit.groupby(
    ['YEAR', 'CHEMICAL']).sum()['TOTAL_RELE']).reset_index()

r_chem_yearly = r_chem_yearly.pivot(
    index='YEAR', columns='CHEMICAL', values='TOTAL_RELE').fillna(0)

# -------------------------------------------------------
# | Show it in a stacked bar plot.

chem_list = r_pounds_limit['CHEMICAL'].unique()
data = []
for c in chem_list:
    trace = go.Bar(y=r_chem_yearly.index,
                   x=r_chem_yearly[c], orientation='h', name=c, hovertext=c)
    data.append(trace)

layout = go.Layout(height=1600, width=1600,
                   xaxis=dict(
                       title=dict(text='Released Chemicals [Pounds]')), barmode='stack')

fig = go.Figure(data=data, layout=layout)
# --
embed_plot(fig, './html/p_4.html')
# --
fig.show()

# -------------------------------------------------------
# | 1. Sharp decrease of
# |
# | * CUMENE
# | * TOLUENE
# | * ACETONE
# | * DICHLOROMETHANE
# | * METHYL ETHYL KETONE
# |
# | in 1980-1990 contributed the total decrease of the emitted chemicals.

# | 2. Most problematic checmicals after 2000 are
# |
# | * SULFURIC ACID
# | * PHENOL
# | * XYLENE
# |


# -------------------------------------------------------
# | We come back to the original task here, and
# | measure the distances to the monitoring stations
# | when a chemical release happened.

# -------------------------------------------------------
# | First, check CRS.

releases.crs
stations.crs
releases.crs == stations.crs

# -------------------------------------------------------
# | The units are feet.

# -------------------------------------------------------
# | Experiment with `.distance`.

stations['geometry'].distance(releases['geometry'])
len(stations)

# | Note that the above command compare the first 12 rows of `releases`
# | with the first 12 rows of `stations` (= whole length of `stations`).

# -------------------------------------------------------
# | Add following information to each emission event.
# |
# | *  mean distance to the stations (over 12 stations).
# | *  name of the nearest station.
# | *  distance to the nearest station.
# |

stations.head(3)
releases.head(3)

# | We will focus on the latest records of the release, i.e., in the year 2006.
# | Note that 'YEAR' is in string.

r_recent = releases[releases['YEAR'] == '2006']
r_recent.info()
r_recent.head(3)

r_recent['NEAREST_STA'] = ''
r_recent['DISTANCE'] = 0.0
r_recent['DISTANCE_MEAN'] = 0.0

for i, r in r_recent.iterrows():
    r_recent.loc[i, 'NEAREST_STA'] = stations.iloc[stations['geometry'].distance(
        r['geometry']).idxmin()]['SITE_NAME']

    r_recent.loc[i, 'DISTANCE'] = stations['geometry'].distance(
        r['geometry']).min()

    r_recent.loc[i, 'DISTANCE_MEAN'] = stations['geometry'].distance(
        r['geometry']).mean()


print(r_recent.info())
r_recent.head(3)

# -------------------------------------------------------
# | Create 2 miles buffer around the stations. 1 mile = 5280 feet.
# | 5280 = five tomatoes = "five two m-eight oh-s".

two_mile_buffer = gpd.GeoDataFrame(geometry=stations.buffer(2*5280))

two_mile_buffer = two_mile_buffer.to_crs(epsg=4326)
type(two_mile_buffer)
two_mile_buffer.head(3)

# -------------------------------------------------------
# | `POINT` in `stations` are now converted to `POLYGON`.

# -------------------------------------------------------
# | Set up the center of the map, tiles, and the initial zoom-factor.

center = [releases['LATITUDE'].mean(), releases['LONGITUDE'].mean()]
tiles = 'openstreetmap'
tiles = 'stamen terrain'
# tiles = 'cartodbpositron'
zoom = 13

# -------------------------------------------------------
# | Show each of 2-miles buffer without combining them.


def style_function(x):

    return {'fillColor': 'salmon',
            'stroke': True, 'color': 'salmon', 'weight': 8,
            'fillOpacity': 0.2}  # 'dashArray' :  '5,5'


m_1 = folium.Map(location=center, tiles=tiles, zoom_start=zoom)
GeoJson(data=two_mile_buffer.__geo_interface__,
        style_function=style_function).add_to(m_1)

# --
embed_map(m_1, './html/m_1.html')
# --
show_on_browser(m_1, CWD + './html/m_1b.html')

# -------------------------------------------------------
# | Show `unary_union` of 2-miles buffers.
# -------------------------------------------------------

two_mile_union = two_mile_buffer['geometry'].unary_union

m_2 = folium.Map(location=center, tiles=tiles, zoom_start=zoom)
GeoJson(data=two_mile_union.__geo_interface__,
        style_function=style_function).add_to(m_2)

# --
embed_map(m_2, './html/m_2.html')
# --
show_on_browser(m_2, CWD + './html/m_2b.html')

# -------------------------------------------------------
# | Show a heatmap of the historical releases of toxic chemicals
# | with the unary union boundary we created above.

m_3 = folium.Map(location=center, tiles=tiles, zoom_start=zoom)

HeatMap(data=releases[['LATITUDE', 'LONGITUDE']],
        radius=30,
        min_opacity=0.3
        ).add_to(m_3)

junk = [Marker([s['LATITUDE'], s['LONGITUDE']], tooltip=s['SITE_NAME'],
               popup=s['ADDRESS']).add_to(m_3) for i, s in stations.iterrows()]

GeoJson(data=two_mile_union.__geo_interface__,
        style_function=style_function).add_to(m_3)

embed_map(m_3, './html/m_2.html')
# --
show_on_browser(m_3, CWD + './html/m_2b.html')

# -------------------------------------------------------
# | ## 4. Conclusion
# |
# | 1. There is a concentration of 4-5 stations in the city center
# |    Philadelphia in a densely distributed manner
# |
# | 2. However, the sources of toxic emissions, presumably factories
# | in the industrial regions, tend to be located outside a city.
# |
# | 3. At least two new monitoring stations are necessary.
# |
# |  - One on the other side of the river from Riverton.
# |  - One between the station 'NEA' (Grant Avenue and Ashton Street)
# |    and the interstate 276.
# |
# | -------------------------------------------------------
# | END
