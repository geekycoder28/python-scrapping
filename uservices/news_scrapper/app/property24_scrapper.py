import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from bs4 import BeautifulSoup
import re
import pymongo
from pymongo import MongoClient

env_path = Path('../../../') / '.env'
load_dotenv(dotenv_path=env_path)

# create connection with mongoDB
DATABASE = os.getenv('DATABASE')
client = MongoClient()
db = client[DATABASE]
table = db['proper24_links']

# get the property URL from .env
PROPERTY_URL = os.getenv("PROPERTY_URL")

# Make the request to the URL to get the page content
propert_request = requests.get(PROPERTY_URL)

# Pass the HTML text to an HTML tree-based structure
soup = BeautifulSoup(propert_request.content, 'html5lib')
properties_container1 = soup.find_all(
    'div', class_='p24_promotedTile')
data_container1 = []
for element in properties_container1:
    property_link = element.a['href']
    property_agent = element.find('div', class_="p24_promotedImage").img['src']
    property_price = element.find(
        'div', class_='p24_price').text.strip().replace("   ", '')
    property_location = element.find('span', class_='p24_location').text
    property_bedrooms = element.find(
        'span', class_='p24_featureDetails', title='Bedrooms').span.text
    property_bathrooms = element.find(
        'span', class_='p24_featureDetails', title='Bathrooms').span.text
    property_images = element.find('img', class_='js_rollover_target')['src']

    property_type = ''
    if '/for-sale' in property_link:
        property_type = 'for sale'
    elif '/to-rent' in property_link:
        property_type = 'for rent'
    else:
        property_type = 'land'

    data = {
        'link': 'https://www.property24.com' + property_link,
        'type': property_type,
        'agent': property_agent,
        'images': property_images,
        'price': property_price,
        'location': property_location,
        'bedrooms': property_bedrooms,
        'bathrooms': property_bathrooms,
    }

    data_container1.append(data)

properties_container2 = soup.find_all(
    'div', class_='p24_regularTile')
data_container2 = []
for element in properties_container2:
    property_link = element.a['href']
    property_images = element.find('img', class_='js_rollover_target js_rollover_default js_P24_listingImage js_lazyLoadImage')['lazy-src']
    property_price = element.find('span', class_='p24_price').text.strip().replace("   ", '')
    property_bedrooms = element.find('span', class_ = 'p24_title').text[:2]
    property_location = element.find('span', class_ = 'p24_location').text
    property_bathrooms = element.find('span', class_='p24_featureDetails', title='Bathrooms').span.text
    property_agent = element.find('span', class_ ='p24_content').img['src']

    property_type = ''
    if '/for-sale' in property_link:
        property_type = 'for sale'
    elif '/to-rent' in property_link:
        property_type = 'for rent'
    else:
        property_type = 'land'

    data = {
        'link': 'https://www.property24.com' + property_link,
        'type': property_type,
        'agent': property_agent,
        'images': property_images,
        'price': property_price,
        'location': property_location,
        'bedrooms': property_bedrooms,
        'bathrooms': property_bathrooms,
    }

    data_container2.append(data)


for item in data_container1:
    data_container2.append(item)

table.insert({"links": data_container2})
