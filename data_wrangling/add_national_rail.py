import pandas as pd
import numpy as np

df = pd.read_csv('data_files/raw/List_of_London_railway_stations_1.csv')
cols = ['Station','Managed by',"Fare zone"]
omit_list = ['London Overground', 'Elizabeth line', 'London Underground']

new_df = df[cols].loc[~df[cols]['Managed by'].isin(omit_list)].rename(columns={'Station': 'station', 'Managed by': 'line', 'Fare zone': 'zone'})
#print(new_df.to_string())

def convert_zone(str_zone):
    try:
        splt = [int(x) for x in str_zone.split('/')]
        zone = sum(splt) / len(splt)
    except ValueError:
        zone = np.nan
    except Exception as e:
        print(e)

    return zone


new_df['zone'] = new_df['zone'].map(convert_zone)


#print(new_df)

tfl_lines = pd.read_csv('data_files/cleaned/tfl_lines.csv')

added_nr = pd.concat([tfl_lines, new_df.dropna(subset='zone')]).sort_values('station').reset_index(drop=True)

print(added_nr.to_string())

added_nr.to_csv('data_files/cleaned/all_lines.csv', index=False)