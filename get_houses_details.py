import pandas as pd
from get_houses_prov_list import get_houses_prov_list
import requests
from bs4 import BeautifulSoup
import re
from IPython.display import display
from statistics import mean
from itertools import repeat


def get_qualifying_houses():
    houses_prov_list = get_houses_prov_list()
    conditions = (houses_prov_list['rent_per_pers'] <= 1000) 
    # & (houses_prov_list['added_status'] == 'Added today')
    return houses_prov_list.loc[conditions]

qualifying_houses = get_qualifying_houses()
print(qualifying_houses)
qualifying_houses.to_csv('data_files/results/qualifying.csv', index=False)

def get_house_details():
    house_df = get_qualifying_houses()
    room_list = []
    stn_line_df = pd.read_csv('data_files/cleaned/all_lines.csv')

    for room in house_df.itertuples():
        url = room.url
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')

        letting_details_raw = soup.find('dl', {'class': '_2E1qBJkWUYMJYHfYJzUb_r'})
        station_raw = soup.find('ul', {'class':'_2f-e_tRT-PqO8w8MBRckcn'})
        stations = list(map(station_info, station_raw.find_all('li'), repeat(stn_line_df)))
        let_available = letting_details_raw.find('div', {'class':'_2RnXSVJcWbWv4IpBC1Sng6'}).find('dd').text
        furnished = letting_details_raw.find('div', {'class': '_2RnXSVJcWbWv4IpBC1Sng6'}).find('dd').text
        info_reel = soup.find('div', {'class': '_4hBezflLdgDMdFtURKTWh'})

        key_info = [item.text for item in info_reel.find_all('dd', {'class': '_1hV1kqpVceE9m-QrX_hWDN'})]
        info_name = [item.text.lower() for item in info_reel.find_all('dt', {'class':'ZBWaPR-rIda6ikyKpB_E2'})]
        info_dict = dict(zip(info_name, key_info))
        
        house_type = info_dict.get('property type')
        
        bathrooms = convert_nums(info_dict, 'bathrooms')
        bedrooms = convert_nums(info_dict, 'bedrooms')

        z_ls = [i['zone'] for i in stations if i['zone'] is not None]
        
        if z_ls:
            zone = mean(z_ls)
        else:
            zone = None

        details = {
            'house_type': house_type,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'available': let_available,
            # 'furnished': furnished,
            'stations': stations,
            'zone': zone
        }

        room_list.append(details)
    
    return pd.DataFrame(room_list, index=house_df.index.copy())


def convert_nums(my_dict, dict_field):
    val = my_dict.get(dict_field)
    if val:
        val = int(my_dict[dict_field][1:])

    return val


def station_info(station, df):
    stn_name = station.find('span', {'class':'cGDiWU3FlTjqSs-F1LwK4'}).text
    stn_dist_str = station.find('span', {'class':'_1ZY603T1ryTT3dMgGkM7Lg'}).text
    stn_network = station.find('svg').get('data-testid').split('-')[-1]

    # stn_name = patt.sub('', stn_name)
    stop_words = ['station', 'underground']
    stn_name = ' '.join([word.title() for word in stn_name.lower().split() if word not in stop_words])

    stn_dist = float(stn_dist_str.replace(' miles', ''))
    station_mask = df['station'] == stn_name
    stn_inf = df.loc[station_mask]
    stn_line = stn_inf['line'].tolist()
    
    if stn_line:
        stn_zone = max(stn_inf['zone'].tolist())
    else:
        stn_line = None
        stn_zone = None

    return {'station_name': stn_name, 'distance (miles)': stn_dist, 'network':stn_network, 'line': stn_line, 'zone': stn_zone}


merged = pd.merge(get_qualifying_houses(), get_house_details(), how='inner', left_index=True, right_index=True).rename(columns={'bedrooms_y':'bedrooms'})
print(merged.columns)
cols = ['id','title','price', 'postcode','rent_per_pers','town','zone','url','added_status','house_type','bedrooms','bathrooms','available','stations','description']

display(merged[cols])

merged[cols].to_csv('data_files/results/results_list.csv')

