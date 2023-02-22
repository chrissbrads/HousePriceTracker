import pandas as pd
import numpy as np

extra_postcodes_raw = pd.read_csv('data_files/raw/head_districts.csv')
extra_postcodes_raw[['eastings','northings','latitude','longitude']] = np.nan
extra_postcodes_raw[['region']] = 'Greater London'

london_postcodes = pd.read_csv('data_files/cleaned/postcodes_ldn.csv')

all_postcodes = pd.concat([extra_postcodes_raw, london_postcodes])\
    .sort_values(['postcode', 'eastings'])\
    .drop_duplicates(subset=['postcode'])\
    .reset_index(drop=True)

print(all_postcodes)

all_postcodes.to_csv('data_files/cleaned/postcodes_ldn_with_hd.csv')
