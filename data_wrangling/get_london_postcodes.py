import pandas as pd

fp = r'data_files/postcodes_all.csv'

postcodes_raw = pd.read_csv(fp)

is_london = postcodes_raw['region'] == 'Greater London'
postcodes_ldn = postcodes_raw[is_london]

cols = ['postcode', 'eastings', 'northings', 'latitude', 'longitude', 'town', 'region']
postcodes_ldn[cols].to_csv(r'data_files/postcodes_ldn.csv', index=False)
