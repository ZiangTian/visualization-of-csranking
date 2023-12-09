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
    # len(df_list)
    0
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

    # plt.savefig('./images/single_analysis/pubs/pngs/pubs_in_{}_{}.png'.format(field, region), dpi=300)
    plt.savefig('./images/single_analysis/pubs/svgs/pubs_in_{}_{}.svg'.format(field, region), dpi=300)

    # plt.show()

# Visualize the faculty member count by university for each file
for i in range( 
    0):
    # len(df_list)):

    region = df_list[i]['region'][0]
    field = df_list[i]['field'][0]

    df_sorted = df_list[i].sort_values('Faculty Count', ascending=False)

    plt.figure(figsize=(12,12))
    ax = sns.barplot(x='abbr', y='Faculty Count', data=df_sorted)
    plt.title('Faculty Member Count by University in ' + field + ' ' + region + ' Institutions')

    # Get the unique abbreviations and corresponding university names
    abbr_names = df_sorted[['abbr', 'University']]

    # Create a legend
    patches = [mpatches.Patch(color=ax.patches[i].get_facecolor(), label=label) for i, label in enumerate(abbr_names['University'])]

    # Add a legend to the plot
    plt.legend(handles=patches, bbox_to_anchor=(0.8, 0.95), loc='upper center', borderaxespad=0.)

    # Add the exact number on top of each bar
    for p in ax.patches:
        ax.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()), 
                fontsize=12, color='black', ha='center', va='bottom')

    plt.savefig('./images/single_analysis/facs/pngs/faculty_in_{}_{}.png'.format(field, region), dpi=300)
    plt.savefig('./images/single_analysis/facs/svgs/faculty_in_{}_{}.svg'.format(field, region), dpi=300)

    # plt.show()


# Visualize the discrepancy between faculty member count and publication count by university for each file
for i in range( 
    # 2
    len(df_list)
    ):
    region = df_list[i]['region'][0]
    field = df_list[i]['field'][0]

    colors = sns.color_palette('pastel')[0:len(df_list[i]['abbr'])]
    
    # standardize the faculty memeber count and publication count, with the expecatin and standard deviation of the faculty member count
    df_list[i]['Standardized Faculty Count'] = (df_list[i]['Faculty Count'] - df_list[i]['Faculty Count'].mean()) / df_list[i]['Faculty Count'].std()

    df_list[i]['Standardized Publication Count'] = (df_list[i]['Publication Count'] - df_list[i]['Publication Count'].mean()) / df_list[i]['Publication Count'].std()

    # calculate the discrepancy
    df_list[i]['Discrepancy'] = df_list[i]['Standardized Faculty Count'] - df_list[i]['Standardized Publication Count']

    fig, ax1 = plt.subplots(figsize=(12,12))

    # Create the bar chart
    bars = ax1.bar(df_list[i]['abbr'], df_list[i]['Discrepancy'], color= colors)

    # Create a second axes for the line graph
    ax2 = ax1.twinx()


    # Create the line graph
    ax2.plot(df_list[i]['abbr'], df_list[i]['Standardized Faculty Count'], color='green', label='Standardized Pub Count')
    ax2.plot(df_list[i]['abbr'], df_list[i]['Standardized Publication Count'], color='red', label='Standardized Faculty Count')

    # Add labels and title
    ax1.set_xlabel('abbr')
    ax1.set_ylabel('Discrepancy: st_Fac -st_Pub', color='black')

    ax2.set_ylabel('Count', color='black')
    plt.title('Standardized Pub Count and Faculty Count by University in ' + field + ' ' + region + ' Institutions')

    # Add a legend
    # ax2.legend()
    # handles = [plt.Rectangle((0,0),1,1, color=bar.get_facecolor()) for bar in bars]
    # plt.legend(handles, df_list[i]['abbr'], title='University')

    # Create a legend
    abbr_names = df_list[i][['abbr', 'University']]
    patches = [mpatches.Patch(color=ax1.patches[i].get_facecolor(), label=label) for i, label in enumerate(abbr_names['University'])]


    # Add the exact number on top of each bar
    # for p in ax.patches:
    #     ax1.text(p.get_x() + p.get_width() / 2., p.get_height(), '%d' % int(p.get_height()), 
    #             fontsize=12, color='black', ha='center', va='bottom')
    
    for p in ax1.patches:
        height = float(p.get_height())
        color = 'black' if height >= 0 else 'blue'
        ax1.text(p.get_x() + p.get_width() / 2., height, '%4.3f' % height, 
                fontsize=9, color=color, ha='center', va='bottom')

    # Add a legend to the plot
    ax1.legend(handles=patches, bbox_to_anchor=(0.99, 0.02), loc='lower right', borderaxespad=0., handlelength=0.5, prop={'size': 6}, ncol = 3)
    ax2.legend(loc='upper right', handlelength=0.5, prop={'size': 7})

    plt.savefig('./images/single_analysis/discrep/pngs/dif_in_{}_{}.png'.format(field, region), dpi=300)
    plt.savefig('./images/single_analysis/discrep/svgs/dif_in_{}_{}.svg'.format(field, region), dpi=300)

    df_list[i].to_csv('./Discrepancies/Discrepancy_{}_{}.csv'.format(field, region), index=False)

    # Show the plot
    # plt.show()
    plt.close()