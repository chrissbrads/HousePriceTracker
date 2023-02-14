import pandas as pd
from get_houses_prov_list import get_houses_prov_list
import requests
from bs4 import BeautifulSoup
import re

def get_qualifying_houses():
    houses_prov_list = get_houses_prov_list()
    conditions = (houses_prov_list['rent_per_pers'] <= 1000) 
    # & (houses_prov_list['added_status'] == 'Added today')
    return houses_prov_list.loc[conditions]

print(get_qualifying_houses())

def get_house_details():
    house_df = get_qualifying_houses()
    room_list = []


    def station_info(station):
        stn_name = station.find('span', {'class':'cGDiWU3FlTjqSs-F1LwK4'}).text
        stn_dist = station.find('span', {'class':'_1ZY603T1ryTT3dMgGkM7Lg'}).text
        stn_network = station.find('svg').get('data-testid').split('-')[-1]

        stn_line_df = pd.read_csv('data_files/cleaned/tfl_lines.csv')
        patt = re.compile('(\s*)Station$')
        stn_name = patt.sub('', stn_name)

        # if stn_network == 'underground' or stn_network == 'overground':
        #     tube_station = stn_line_df['station_name'] == stn_name
        #     stn_line = stn_line_df.loc[tube_station,'line'].tolist()
        # elif stn_network == 'networkrail':
        #     rail_station = stn_line_df['line'] == 'Elizabeth Line' & stn_line_df['station_name'] == stn_name
        #     stn_line = stn
        # else:
        #     stn_line = None

        station_mask = stn_line_df['station'] == stn_name
        stn_inf = stn_line_df.loc[station_mask]
        stn_line = stn_inf['line'].tolist()
        
        if stn_line:
            stn_zone = max(stn_inf['zone'].tolist())
        else:
            stn_line = None
            stn_zone = None

        return {'station_name': stn_name, 'distance': stn_dist, 'network':stn_network, 'line': stn_line, 'zone': stn_zone}
    
    loop = 0
    for room in house_df.itertuples():
        url = room.url
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')

        letting_details_raw = soup.find('dl', {'class': '_2E1qBJkWUYMJYHfYJzUb_r'})
        station_raw = soup.find('ul', {'class':'_2f-e_tRT-PqO8w8MBRckcn'})
        
        # stn_name = [item.text for item in station_raw.find_all('span', {'class':'cGDiWU3FlTjqSs-F1LwK4'})]
        # stn_dist = [item.text for item in station_raw.find_all('span', {'class':'_1ZY603T1ryTT3dMgGkM7Lg'})]
        # stn_network = [item.get('data-testid').split('-')[-1] for item in station_raw.find_all('svg')]

        # stations = list(zip(stn_name, stn_dist, stn_network))

        stations = list(map(station_info, station_raw.find_all('li')))
        # stations = {item.find('span', {'class':'cGDiWU3FlTjqSs-F1LwK4'}).text: item.find('span', {'class':'_1ZY603T1ryTT3dMgGkM7Lg'}).text for item in station_raw.find_all('li')}
        let_available = letting_details_raw.find()

        loop += 1

        details = {
            'stations': stations
        }

        room_list.append(details)


        # stations = []
        # for item in station_raw.find_all('li'):
        #     stn_name = item.find('span', {'class':'cGDiWU3FlTjqSs-F1LwK4'}).text
        #     stn_dist = item.find('span', {'class':'_1ZY603T1ryTT3dMgGkM7Lg'}).text
        #     stn_network = item.find('svg').get('data-testid').split('-')[-1]

        #     info = {'station_name': stn_name, 'distance': stn_dist, 'network':stn_network}

        #     stations.append(info)



    return room_list, loop

print(get_house_details())



