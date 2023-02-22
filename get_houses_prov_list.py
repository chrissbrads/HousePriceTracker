import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from get_requests import get_raw_properties_list

output_csv_flag = False

def get_houses_prov_list(pages=3):
    
    # urls = r"https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87490&minBedrooms=2&maxPrice=3000&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords="
    # res = requests.get(url)
    # soup = BeautifulSoup(res.content, 'lxml')
    # properties_raw = soup.find_all('div', {'class': 'l-searchResult is-list'})

    base_url = r'https://www.rightmove.co.uk'
    url = r'https://www.rightmove.co.uk/property-to-rent/find.html'

    payload = {
        'locationIdentifier': 'REGION^87490', # decoded url for 'REGION%5E87490' (Greater London)
        'minBedrooms': 2,
        'maxPrice': 3000,
        'index': None,
        'propertyTypes':'',
        'includeLetAgreed': 'false',
        'mustHave': '',
        'dontShow': '',
        'furnishTypes':'',
        'keywords': ''
    }

    properties_raw = get_raw_properties_list(url, pages, payload=payload)

    postcode_df = pd.read_csv('data_files/cleaned/postcodes_ldn_with_hd.csv')
    postcode_prfx = ['N','NE','E','SE','SW','W','NW','EC','WC','BR','CR','DA','EN','HA','IG','KT','RM','SM','TW','UB']

    detail_list = []
    for room in properties_raw:
        
        prop_det = room.find('div', {'class':'propertyCard-details'})
        title = prop_det.find('address').text.strip()
        price = room.find('span', {'class':'propertyCard-priceValue'}).text
        info = prop_det.find('h2', {'class':'propertyCard-title'}).text.strip()
        prop_desc = room.find('div', {'class':'propertyCard-description'}).text.strip()
        link = prop_det.find('a', {'class':'propertyCard-link'}).get('href')
        when_added = room.find('span', {'class':'propertyCard-contactsAddedOrReduced'}).text

        # number of bedrooms 
        try:
            num_br = int(info.split()[0])
        except Exception as e:
            num_br = e
        
        # rent per person
        price_numeric = [int(num) for num in re.findall(r'\d+', price.replace(',',''))]
        rpp = price_numeric[0] / num_br

        # find the postcode of the property from the title usign regex (postcode usually at the end of the title)
        split_title = re.findall(r"[\w']+", title)
        pattern = re.compile(r"[A-Za-z]{1,2}[0-9]{1,2}", re.IGNORECASE)

        if len(split_title) >= 1 and pattern.match(split_title[-1]):
            postcode = split_title[-1]
        elif (len(split_title) >= 2) and pattern.match(split_title[-2]):
            postcode = ' '.join(split_title[-2:])
        else:
            postcode = None
        
        if postcode and postcode.split()[0].startswith(tuple(postcode_prfx)): 
            postcode_area = postcode.split()[0]
            town = postcode_df.loc[postcode_df['postcode'] == postcode_area, 'town'].item()
        else:
            town = None

        room_info = {
            'title': title,
            'price': price,
            'info': info,
            'description': prop_desc,
            'postcode': postcode,
            'bedrooms': num_br,
            'rent_per_pers': rpp,
            'town': town,
            'url': base_url + link,
            'added_status': when_added
        }
        detail_list.append(room_info)

    return pd.DataFrame(detail_list)


if __name__ == '__main__':
    houses_prov_list = get_houses_prov_list()
    print(houses_prov_list)

    if output_csv_flag:
        houses_prov_list.to_csv(r'data_files/cleaned/property_list.csv')
    

# prop_df.to_csv(r'data_files/property_list.csv')
#print(prop_det)
# print(detail_list)
# print(prop_df)
# print(room)






