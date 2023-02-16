import pandas as pd

parent = 'data_files/raw/'
cols = ['Station', 'Zone']
liz_line_df = pd.read_csv(parent + 'Elizabeth_line_tube_stations.csv')[cols]
liz_line_df['line'] = 'Elizabeth Line'
overground_df = pd.read_csv(parent + 'Overground_line_tube_stations.csv')[cols]
overground_df['line'] = 'London Overground'

both_lines_df = pd.concat([liz_line_df, overground_df])\
    .sort_values('Station')\
    .reset_index(drop=True)\
    .rename(columns={'Station':'station', 'Zone':'zone'})

def trans_zone(zone):
    if len(zone) > 1:
        zones = [int(i) for i in zone.split(',')]
        new_zone = sum(zones) / len(zones)
    else:
        new_zone = int(zone)
    return new_zone

both_lines_df['zone'] = both_lines_df['zone'].apply(lambda x: trans_zone(x) if isinstance(x, str) else x)

underground_df = pd.read_csv('data_files/cleaned/station_line_table.csv')[['station_name', 'line', 'zone']].rename(columns={'station_name':'station'})
remove_ELL = underground_df['line'] != 'East London Line'
underground_df = underground_df.loc[remove_ELL]
all_lines_df = pd.concat([underground_df, both_lines_df])\
    .sort_values('station')\
    .reset_index(drop=True)


all_lines_df.to_csv('data_files/cleaned/tfl_lines.csv', index=False)