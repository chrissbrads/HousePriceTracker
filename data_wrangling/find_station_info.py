import pandas as pd
import numpy as np

raw_filepath = 'data_files/raw/'

routes_df = pd.read_csv(raw_filepath + 'routes_raw.csv')
stations_df = pd.read_csv(raw_filepath + 'stations_raw.csv')
line_def_df = pd.read_csv(raw_filepath + 'line_definitions_raw.csv', names=['station1', 'station2', 'line_id'])

line_df_st1 = line_def_df[['station1', 'line_id']]
line_df_st2 = line_def_df[['station2', 'line_id']].rename(columns={'station2': 'station1'})
union_stations = pd.concat([line_df_st1, line_df_st2]).drop_duplicates(inplace=False)

print(union_stations)

stations_with_line = union_stations.merge(
    stations_df,
    how='inner',
    left_on='station1', 
    right_on='id'
    ).merge(
        routes_df,
        how='inner',
        left_on='line_id',
        right_on='line'
    )


cols = ['id','name_x','line_id','name_y', 'zone']
stations_info = stations_with_line[cols].rename(
    columns={'id':'station_id', 'name_x': 'station_name', 'name_y': 'line'}
    ).sort_values(
        by='station_id'
    )
print(stations_info)

stations_info.to_csv('data_files/cleaned/station_line_table.csv', index=False)