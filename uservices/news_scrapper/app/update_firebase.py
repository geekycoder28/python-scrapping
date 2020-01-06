import os
import json
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
from pathlib import Path
from dotenv import load_dotenv
import sys
from datetime import datetime

env_path = Path('../../../') / '.env'
load_dotenv(dotenv_path=env_path)

FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
cred = credentials.Certificate('../../../jacaranda-app-firebase-adminsdk.json')

default_app = firebase_admin.initialize_app(cred, {
  'projectId': FIREBASE_PROJECT_ID,
})

firestore_client = firestore.client()
doc_ref = firestore_client.collection('properties')

get_data = doc_ref.stream()
test = []

for prop in get_data:

    property_data = prop.to_dict()

    # Update the price to split the currency and value
    actual_price = property_data['price']
    if type(actual_price) is str:
      price_array = actual_price.split(' ')
      price_value = ''.join(price_array[1:])
      format_price_value = price_value.replace(u'\xa0', u'')
      if len(format_price_value) == 0:
        form_price = {
          'currency': price_array[0],
          'value': 0
        }
        doc_ref.document(prop.id).update({
          'price': form_price
        })
      else:
        change_to_int = int(format_price_value)
        formatted_price = {
          'currency': price_array[0],
          'value': change_to_int
        }

        doc_ref.document(prop.id).update({
          'price': formatted_price
        })


    # Update the rest of attributes in the property info
    if not 'property_info' in property_data:
        pass
    
    elif type(property_data['property_info']) is dict:
        pass
    else:
        formated_value = {}
        for item in property_data['property_info']:
            if type(item) is str:
                pass
            else:
                formated_value[list(item.keys())[0]] = list(item.values())[0]
        
        if 'List Date' in formated_value:
            formated_value['List Date'] = datetime.strptime(formated_value['List Date'], "%d %B %Y")
        
        if 'Bathrooms' in formated_value:
            formated_value['Bathrooms'] = float(formated_value['Bathrooms'])
        
        if 'Garage' in formated_value:
            formated_value['Garage'] = float(formated_value['Garage'])

        if 'Bedroom' in formated_value:
            formated_value['Bedroom'] = float(formated_value['Bedroom']) if len(formated_value['Bedroom']) < 3 else formated_value['Bedroom']
        
        if 'Parking' in formated_value:
            formated_value['Parking'] = True if formated_value['Parking'] == 'Yes' else False
        
        if 'Pets Allowed' in formated_value:
            formated_value['Pets Allowed'] = True if formated_value['Pets Allowed'] == 'Yes' else False
        
        if 'Garden' in formated_value:
            formated_value['Garden'] = True if formated_value['Garden'] == 'Yes' else False
        
        doc_ref.document(prop.id).update({
          'property_info': formated_value
        })

