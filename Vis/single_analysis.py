import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import re
import matplotlib.patches as mpatches

from utils import make_unique
from utils import get_region_and_field


# Get all files
all_files = glob.glob('.\detailed\Institutions_*_*.csv')

# Add region and field columns
df_list = []
for file in all_files:
    region, field = get_region_and_field(file)
    df = pd.read_csv(file)
    df['region'] = region
    df['field'] = field
    df_list.append(df)

# Add abbr column
for df in df_list:
    df['abbr'] = df['University'].apply(lambda name: ''.join(word[0] for word in name.split() if word[0].isupper()))

# Unique-ify abbr
for df in df_list:
    make_unique(df, 'abbr')


# Visualize the publication count by university for each file 

for i in range(
    len(df_list)
    # 2
    ):

    region = df_list[i]['region'][0]
    field = df_list[i]['field'][0]

    plt.figure(figsize=(12,12))
    ax = sns.barplot(x='abbr', y='Publication Count', data=df_list[i])
    plt.title('Publication Count by University in ' + field + ' ' + region + ' Institutions')

    # Get the unique abbreviations and corresponding university names
    abbr_names = df_list[i][['abbr', 'University']]

    # Create a legend
    patches = [mpatches.Patch(color=ax.patches[i].get_facecolor(), label=label) for i, label in enumerate(abbr_names['University'])]

    # Add a legend to the plot
    plt.legend(handles=patches, bbox_to_anchor=(0.8, 0.95), loc='upper center', borderaxespad=0.)

    # Add the exact number on top of each bar
    for p in ax.patches:
        ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()), 
                fontsize=12, color='black', ha='center', va='bottom')

    plt.savefig('./images/single_analysis/pubs_in_{}_{}.png'.format(field, region), dpi=300)

    # plt.show()

