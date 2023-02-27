import requests
from bs4 import BeautifulSoup

default_payload = {
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

def get_raw_properties_list(req_url, pages ,payload=default_payload):
    properties_raw = []
    for mlt in range(pages):
        if mlt != 0:
            payload['index'] = mlt*24
        r = requests.get(req_url, params=payload)
        soup = BeautifulSoup(r.content, 'lxml')
        properties_raw += soup.find_all('div', {'class': 'l-searchResult is-list'})
    
    return properties_raw


test_url = 'https://www.rightmove.co.uk/property-to-rent/find.html'
run_def_payload = True

if __name__ == '__main__':
    if run_def_payload:
        properties_raw = get_raw_properties_list(test_url, 4, default_payload)
    else:
        test_payload = {

        }
        properties_raw = get_raw_properties_list(test_url, 4, test_payload)
    
    print(properties_raw)
    print(len(properties_raw))






    