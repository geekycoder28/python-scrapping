import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import json
import logging
from pprint import pprint
from time import sleep
from elasticsearch import Elasticsearch
import uuid
import time
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

FIREBASE_PROJECT_ID = os.getenv("PROPERTY_URL")
cred = credentials.Certificate('../../../jacaranda-app-firebase-adminsdk.json')

default_app = firebase_admin.initialize_app(cred, {
  'projectId': FIREBASE_PROJECT_ID,
})

firestore_client = firestore.client()
doc_ref = firestore_client.collection('properties')

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

def scraper(root, steps):
    urls = [root]
    visited = [root]
    counter = 0
    
    while counter < steps:
        step_url = scrape_step(urls, steps)
        urls = []
        for u in step_url:
            if u not in visited:
                urls.append(u)
                visited.append(u)
        counter += 1

    final_property_array = []
    for link in visited:
        property_request = requests.get(PROPERTY_URL + link)
        soup = BeautifulSoup(property_request.content, 'html5lib')
        get_individual_property = soup.find_all('div', class_ = None)
        
        display_links = []
        for item in get_individual_property:
            link_tags = item.select('a')
            links = [pt.get('href') for pt in link_tags]
            # print('links', links)

            if len(links) > 3:
                display_links = links
            else:
                pass
        
        filter_agency_links = []
        for item in display_links:
            if 'javascript' in item:
                filter_agency_links.append(item)
            if 'estate-agency' in item:
                filter_agency_links.append(item)

        property_links = list(set(display_links) - set(filter_agency_links))

        
        final_property_array.extend(property_links)
    
    print('now', final_property_array)
        
    return []

def scrape_step(root, steps):

    result_urls = []
    for url in root:
        try:

            if url == PROPERTY_URL:
                property_request = requests.get(url)
                soup = BeautifulSoup(property_request.content, 'html5lib')
                links_sections = soup.find_all('div', class_ = 'col-xs-6')
                for item in links_sections:
                    link_tags = item.select('a')
                    links = [pt.get('href') for pt in link_tags]
                    result_urls = links
            
            else:
                property_request = requests.get(PROPERTY_URL + url)
                soup = BeautifulSoup(property_request.content, 'html5lib')
                footer_links_section = soup.find_all('div', class_ = 'footPopularAreas')
                for item in footer_links_section:
                    link_tags = item.select('a')
                    links = [pt.get('href') for pt in link_tags]
                    result_urls = result_urls + links

        except Exception as e:
            print('error', e)

    return result_urls

def check_property_exists():
    all_properties = doc_ref.stream()
    current_properties = []
    for doc in all_properties:
        current_properties.append(doc.to_dict())

    return current_properties

def scrap_data(url):

    # links_array = scraper(url, 2)
    # linka = links_array[1]
    # print('linkkkka', linka)

    try:
        links = ['/vacant-land-plot-for-sale-in-kibos-108249304', '/vacant-land-plot-for-sale-in-rabuor-107811036', '/vacant-land-plot-for-sale-in-rabuor-101756435', '/apartment-flat-for-sale-in-lolwe-101736179', '/apartment-flat-for-sale-in-lolwe-107854895', '/3-bedroom-house-for-sale-in-kenya-re-107887944', '/3-bedroom-house-for-sale-in-kenya-re-101732776', '/apartment-flat-for-sale-in-dunga-101750317', '/apartment-flat-for-sale-in-dunga-107903897', '/vacant-land-plot-for-sale-in-chulaimbo-107943094', '/vacant-land-plot-for-sale-in-chulaimbo-101743318', '/commercial-property-for-sale-in-eldoret-cbd-108012966', '/3-bedroom-house-for-sale-in-eldoret-cbd-101758972', '/3-bedroom-house-for-sale-in-eldoret-cbd-107199347', '/3-bedroom-apartment-flat-for-sale-in-eldoret-cbd-106810880', '/4-bedroom-house-for-sale-in-eldoret-cbd-106607359', '/4-bedroom-house-for-sale-in-eldoret-cbd-108240733', '/5-bedroom-house-for-sale-in-eldoret-cbd-108264708', '/4-bedroom-house-for-sale-in-eldoret-cbd-108110165', '/3-bedroom-house-for-sale-in-eldoret-cbd-106611790']


        all_data = []
        for link in links:

            # if len(link) < 3:
            #     pass

            property_request = requests.get(url + link)
            soup = BeautifulSoup(property_request.content, 'html5lib')
            get_individual_property = soup.find_all('div', class_ = 'containerWrap')
            properties_pres = []
            data_dict = dict()
            current_properties = check_property_exists()

            for element in get_individual_property:

                id_section = uuid.uuid4().hex
                data_dict['uuid'] = id_section
                price_section = element.find('div', class_='pull-left sc_listingPrice primaryColor')
                if price_section is not None:
                    price = element.find('div', class_='pull-left sc_listingPrice primaryColor').text.strip().replace("   ", '')
                    data_dict['price'] = price
                
                price_range_dev = element.find('div', class_ = 'pull-left sc_listingPrice sc_listingPriceDevelopments primaryColor')
                if price_range_dev is not None:
                    price_section = element.find('div', class_ = 'pull-left sc_listingPrice sc_listingPriceDevelopments primaryColor')
                    price = price_section.find('span', class_ = None).text
                    data_dict['price'] = price

                title_section = element.find('div', class_ = 'pull-left sc_listingAddress')
                if title_section is not None:
                    title = element.find('div', class_ = 'pull-left sc_listingAddress').h1.text
                    data_dict['title'] = title

                address_section = element.find('div', class_ = 'pull-left sc_listingAddress')
                if address_section is not None:
                    address = element.find('div', class_ = 'pull-left sc_listingAddress').p.text
                    data_dict['address'] = address
                    address_array = address.split(',')
                    data_dict['district'] = address_array[-1]

                images_scraper = element.find_all('img', class_ = 'mainImage')
                if images_scraper:
                    images = []
                    for item in images_scraper:
                        images.append(item['data-original'])
                    data_dict['images'] = images

                property_details_section = element.find('div', class_ = 'sc_listingDetailsText')
                if property_details_section is not None:
                    property_details = element.find('div', class_ = 'sc_listingDetailsText').text
                    data_dict['property_details'] = property_details
                
                get_property_info = element.find_all('div', class_ = 'detailItem sc_listingSummaryRow')
                
                if get_property_info:
                    property_info = []
                    for item in get_property_info:
                        data = {
                            item.find('div', class_ = 'detailItemName').text.strip().replace("   ", '') : item.find('div', class_ = 'detailItemValues').text.strip().replace("   ", '')
                        }
                        property_info.append(data)
                    data_dict['property_info'] = property_info
            all_data.append(data_dict)
            # doc_ref.document().set(data_dict)
            # if create_index(es, 'properties'):
            #     store = store_data(es, 'properties', data)
            #     print('Data Indexed successfully', store)

            if not any(item.get('title', None) == data_dict['title'] for item in current_properties):
                doc_ref.document().set(data_dict)
            else:
                print('the property already exists')

        return []
    
    except Exception as e:
        print('something happenned', e)

if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)
    # get the property URL from .env
    PROPERTY_URL = os.getenv("PROPERTY_URL")
    request = requests.get(PROPERTY_URL)
    if request.status_code == 200:
        es = connect_el()
        sleep(2)
        scrapped_data = scrap_data(PROPERTY_URL)
