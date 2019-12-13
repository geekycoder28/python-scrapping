import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from bs4 import BeautifulSoup
import re
import json
import logging
from pprint import pprint
from time import sleep
from elasticsearch import Elasticsearch

def search(es_object, index_name, search):
    response = es_object.search(index=index_name, body=search)
    pprint(response)


def create_index(es_object, index_name):
    created = False

    # make up the Index(storage) settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties_listings": {
                "dynamics": "strict",
                "properties": {
                    "link": { "type": "text"},
                    "prop_type": { "type": "text"},
                    "agent": { "type": "text"},
                    "images": { "type": "text"},
                    "price": { "type": "text"},
                    "location": { "type": "text"},
                    "bedrooms": { "type": "text"},
                    "bathrooms": { "type": "text"},
                }
            } 
        }
    }

    try:
        # Check if the index is already created
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as e:
        print(str(e))
    finally:
        return created

def store_data(elastic_object, index_name, data):
    is_stored = True

    try:
        store = elastic_object.index(index = index_name, doc_type='properties_listings', body=data) 
        print(store)
    except Exception as e:
        print('Something went wrong while indexing data')
        print(str(e))
        is_stored = False
    finally:
        return is_stored

def connect_el():
    _el = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('ElasticSearch connected Successfully')
    else:
        print('Something went wrong while connecting')

    return _es

env_path = Path('../../../') / '.env'
load_dotenv(dotenv_path=env_path)

def scrap_data(URL):

    try:
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
                'prop_type': property_type,
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
                'prop_type': property_type,
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
    except Exception as e:
        print('Error when parsing data')
        print(str(e))
    finally:
        return json.dumps(data_container2)

if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)
    # get the property URL from .env
    PROPERTY_URL = os.getenv("PROPERTY_URL")
    request = requests.get(PROPERTY_URL)
    if request.status_code == 200:
        es = connect_el()
        sleep(2)
        scrapped_data = scrap_data(PROPERTY_URL)
        if es is not None:
            if create_index(es, 'properties'):
                data = store_data(es, 'properties', scrapped_data)
                print('Data Indexed successfully')
    
    es = connect_el()
    if es is not None:
        search_is_forsale = { '_source': ['link'], 'query': {'range': {'prop_type': {'gte': 'is forsale'}}}}
