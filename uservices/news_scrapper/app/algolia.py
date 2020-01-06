import os
from algoliasearch.search_client import SearchClient
import json
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
from pathlib import Path
from dotenv import load_dotenv
import sys

env_path = Path('../../../') / '.env'
load_dotenv(dotenv_path=env_path)

FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
cred = credentials.Certificate('../../../jacaranda-app-firebase-adminsdk.json')

default_app = firebase_admin.initialize_app(cred, {
  'projectId': FIREBASE_PROJECT_ID,
})

firestore_client = firestore.client()
doc_ref = firestore_client.collection('properties')

def get_all_properties_firebase():
    all_properties = doc_ref.stream()
    current_properties = []
    for doc in all_properties:
        current_properties.append(doc.to_dict())
        
    return current_properties

def save_to_algolia():
    properties_on_firebase = get_all_properties_firebase()

    algolia_data = []
    query = '' # Empty query will match all record
    res = index.browse_objects({'query': query})

    for hit in res:
        algolia_data.append(hit)
    
    actual_properties = []
    for obj in properties_on_firebase:
        if not any(item.get('uuid', None) == obj['uuid'] for item in algolia_data):
            district = obj['district']

            data = {
                'title': obj['title'],
                'price': obj['price'],
                'uuid': obj['uuid'],
                'district': district.replace(" ", ""),
                'images': obj['images'][0],
                'property_details': obj['property_details'],
                'property_info': obj['property_info'] if 'property_info' in obj else []
            }
            actual_properties.append(data)


    chunk_size = 100
    chunks = [actual_properties[i:i+chunk_size] for i in range(0, len(actual_properties), chunk_size)]

    for chunk in chunks:
        index.save_objects(chunk, {'autoGenerateObjectIDIfNotExist': True})



if __name__ == "__main__":
    ALGOLIA_APP = os.getenv('ALGOLIA_APP_ID')
    ALGOLIA_ADMIN_API_KEY = os.getenv('ALGOLIA_ADMIN_API_KEY')
    client = SearchClient.create(ALGOLIA_APP, ALGOLIA_ADMIN_API_KEY)
    index = client.init_index('jacaranda')
    save_to_algolia()

