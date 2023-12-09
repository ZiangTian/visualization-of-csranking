import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import re


def make_unique(df # dataframe
                , col_name # column name to make unique
                ):
    for i, ab in enumerate(df[col_name]):
        cnt = df[col_name].to_list().count(ab)
        if cnt > 1:
            df[col_name][i] = ab + '-'+ str(cnt)


def get_region_and_field(file_name):
    # Get region
    region = re.search('Institutions_(.*?)_', file_name).group(1)
    # Get field
    field = re.search('_(.*?)\.csv', file_name).group(1).split('_')[-1]
    return region, field