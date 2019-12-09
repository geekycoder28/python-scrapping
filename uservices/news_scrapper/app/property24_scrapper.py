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

links_array = []
for link in soup.find_all('a', href=True):
    links_array.append(link['href'])

# Remove the javascript links
filtered_links = []
for item in links_array:
    if 'javascript' in item:
        filtered_links.append(item)

# compare the both of the array and get the difference
diff = list(set(links_array) - set(filtered_links))

final_array = []
# Check for the links that doesn't have the base url.
for item in diff:
    element = re.search(r"^/", item)
    if element:
        new_value = 'https://www.property24.com' + item
        final_array.append(new_value)
    else:
        pass

# Insert the data in database.
table.insert({"links": final_array})


