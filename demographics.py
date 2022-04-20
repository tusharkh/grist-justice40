import numpy as np
import pandas as pd
from census import Census
from us import states

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import font_manager
from matplotlib import rcParams

# get CEJST data
# path to CEJST file
cejst_path = 'data/communities-2022-03-30-0033GMT.csv'
cejst = pd.read_csv(cejst_path)

# cleaning: delete extra columns
# rename desired columns with easier names
new_column_names = {'Census tract ID':'tract', 'County Name':'county',
                    'State/Territory':'state',
#                   'Total threshold criteria exceeded':'threshold_exceeded',
#                    'Total categories exceeded':'category_exceeded',
                    'Identified as disadvantaged':'disadvantaged',
                    'Total population':'cejst_population'}

cejst.rename(columns=new_column_names, inplace=True)

# drop other columns
columns_to_drop = [column for column in cejst.columns if column not in new_column_names.values()]
cejst.drop(columns_to_drop, axis=1, inplace=True)

# format tract to get 11 digit strings
cejst['tract'] = cejst['tract'].apply('{0:0>11}'.format)

# individual census key (add yours here)
census_key = 'c76c36a59c98e34fbdc42a49c36d4a0b8f274bee'
c = Census(census_key)

# retrieve the desired census tract data and format into a dataframe
# find ACS 2019 variables here: https://api.census.gov/data/2019/acs/acs5/variables.html
# B01003_001E: Total Population
# B02001_001E: Race (total)
# B02001_002E: Race, White alone

tract_list = []
for state in (states.STATES_AND_TERRITORIES + [states.DC]):
  tracts = c.acs5.state_county_tract(fields = ('NAME', 'B01003_001E', 'B02001_002E'),
                                     state_fips = state.fips,
                                     county_fips = "*",
                                     tract = "*",
                                     year = 2019)
  tract_list += tracts
  
# createa a dataframe
race = pd.DataFrame(tract_list)

# rename columns
race_column_names = {'NAME': 'name', 'B01003_001E':'census_population', 'B02001_002E': 'white'}

# compute non-white population
race.rename(columns=race_column_names, inplace=True)

# get 11 digit tract number
race['tract'] = race['state'] + race['county'] + race['tract']

# calculate non-white population by subtracting white from total population (I think this is kosher)
race['non_white'] = race['census_population'] - race['white']
race['percent_non_white'] = race['non_white'] / race['census_population']

# drop unnecessary columns
race.drop(columns=['state', 'county', 'name'], inplace=True)

# merge CEJST data and census (race) data
merged = cejst.merge(race, how='inner', on='tract')

# bin the data to replicate figure
bins = np.append(np.append(0, np.arange(0.025, 1, 0.05)), 1)
merged['binned'] = pd.cut(merged['percent_non_white'], bins)

# compute statistics (total number of disadvanted tracts in each bin
# and percentage of tracts that are disadvantaged)
count = merged.groupby('binned')['disadvantaged'].count()
percentage = merged.groupby('binned')['disadvantaged'].sum() / merged.groupby('binned')['disadvantaged'].count()

# create indices for plot
percentage.index = np.arange(0, 1.01, 0.05)
count.index = np.arange(0, 1.01, 0.05)

# Add every font at the specified location
font_dir = ['/Users/tushar/Downloads/Open_Sans/static/']
for font in font_manager.findSystemFonts(font_dir):
  # use font_manager.FontProperties(fname=font).get_name() to get the name
  font_manager.fontManager.addfont(font)

# Set font family globally
rcParams['font.family'] = 'Open Sans'

# set global style parameters
rcParams['xtick.labelsize'] = 20
rcParams['ytick.labelsize'] = 20
rcParams['xtick.labelcolor'] = '#666666'
rcParams['ytick.labelcolor'] = '#666666'
rcParams['grid.linewidth'] = 2
rcParams['grid.color'] = '#ffffff'
rcParams['axes.facecolor'] = '#eeeeee'
rcParams['figure.facecolor'] = '#eeeeee'
rcParams['axes.labelcolor'] = '#666666'
rcParams['axes.labelsize'] = 20

DISADVANTAGED_COLOR = '#b925ba'
ADVANTAGED_COLOR = '#2ea577'

# plot figure
fig, ax = plt.subplots(figsize=(14, 9))
ax.bar(percentage.index, height=1, bottom=0, width=0.035, color=ADVANTAGED_COLOR)
ax.bar(percentage.index, height=percentage, width=0.035, color=DISADVANTAGED_COLOR)

# set tick styles and labels
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_xticks(percentage.index)
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.tick_params(axis='x', labelrotation=90)
ax.tick_params(left=False, bottom=False)

# set lable
ax.set_xlabel('Tract population percent that is non-white')

# add a grid
ax.grid(visible=True, which='major', axis='y')
ax.set_axisbelow(True)

# clear spines
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)

# title
ax.text(s='Demographic distribution', fontsize=30, y=1.16, x=-0.06, transform=ax.transAxes, fontweight=600)
ax.text(s='Percent of census tracts identified as                             and', fontsize=30, y=1.09, x=-0.06,
        transform=ax.transAxes, fontweight=100)
ax.text(s='disadvantaged', fontsize=30, y=1.09, x=0.584, color=DISADVANTAGED_COLOR,
        transform=ax.transAxes, fontweight=600)
ax.text(s='                                    by the White House screening tool', fontsize=30, y=1.02, x=-0.06,
        transform=ax.transAxes, fontweight=100)
ax.text(s='not disadvantaged', fontsize=30, y=1.02, x=-0.06, color=ADVANTAGED_COLOR,
        transform=ax.transAxes, fontweight=600)

# caption
ax.text(s='Data Source: CEJST / ACS', fontsize=15, y=-0.22, x=-0.06, transform=ax.transAxes, fontweight=100)

# set figure limits
ax.set_xlim(-0.025, 1.025)

# create filename and save
filename = 'demographic-distribution'
fig.savefig('figures/' + filename + '.jpg', bbox_inches='tight', pad_inches=0.3)