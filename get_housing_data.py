import requests
from bs4 import BeautifulSoup

url = r"https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E87490&insId=1&radius=0.0&minPrice=&maxPrice=2000&minBedrooms=2&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=1&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare=#prop131430050"

res = requests.get(url)
#print(res.text[:1000])

soup = BeautifulSoup(res.text, 'lxml')


properties_raw = soup.find_all('div', {'class': 'l-searchResult is-list'})
print(properties_raw[0])
detail_list = []
for room in properties_raw:
    
    prop_det = room.find('div', {'class':'propertyCard-details'})
    title = prop_det.find('address').text.strip()
    price = room.find('span', {'class':'propertyCard-priceValue'}).text
    info = room.find('div', {'class':'property-information'})

    #info = prop_det.find('span', {'class':'text'}).text
    postcode = 12
    
    room_info = {
        'title': title,
        'price': price,
        #'info': info
    }

    detail_list.append(room_info)
print(prop_det)
print(detail_list)


tag = 'address'
addresses = soup.find_all(tag)
prices = soup.find_all('span', {'class':'propertyCard-priceValue'})
price_list = [price.text for price in prices]
titles = [title.find('meta')['content'] for title in addresses]
address_list = [address.text.strip() for address in addresses]
#print(address_list)
#print(price_list)





