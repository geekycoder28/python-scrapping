from bs4 import BeautifulSoup
from urllib import request
from io import BytesIO
from PIL import Image
from urllib.parse import urljoin, urlparse
from pprint import pprint
from random import shuffle
from os import path
from urllib.error import HTTPError
import requests
import redis
import json
import sys, traceback
from bs4.element import Comment
import time
from google.cloud import firestore
from main import get_link_info

red = redis.Redis(host='localhost', port=6379, db=0)
firedb = firestore.Client()

coll = firedb.collection(u'articles')
links_to_visit = set([
    "https://www.nation.co.ke/",
    "https://www.thecitizen.co.tz/",
    "https://www.monitor.co.ug/",
    # "https://www.aljazeera.com",
    # "https://www.newvision.co.ug/",
    # "https://www.standardmedia.co.ke/",
    # "http://www.swahilihub.com/",
    # "https://www.the-star.co.ke/",
    # "https://www.bbc.com/",
    # "https://www.capitalfm.co.ke/",
    # "https://www.theguardian.com/",
    # "https://www.thesouthafrican.com/",
    # "https://www.timeslive.co.za/",
    # "https://www.iol.co.za/",
    # "https://www.sowetanlive.co.za/",
    # "http://nairobiwire.com/",
    # "https://allafrica.com/",
    # "https://www.nytimes.com/",
    # "https://borkena.com/",
    # "http://www.tigraionline.com/",
    # "https://www.ezega.com/",
    # "https://punchng.com/",
])

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def getsizes(img_url):
    try:
        req  = requests.get(img_url)
        im = Image.open(BytesIO(req.content))
        return {
            "height" : im.size[0],
            "width" : im.size[1]
        }
    except Exception as e:
        print(e)

    return {
        "height" : 0,
        "width" : 0
    }

def dfs_visit(base_url, depth, max_depth, visited_links):
    if base_url in visited_links or depth > max_depth:
        return

    try:
        link_info = get_link_info(base_url)
        return visited_links
        
        visited_links[base_url]["last_visit_time"] = int(time.time())
        visited_links[base_url]["visit_count"] += 1

        if len(visible_texts_large) > 2:
            visited_links[base_url]["has_text"] = True

            link_elem = {
                "url" : base_url,
                "last_visit_time" : int(time.time())
            }

            coll.add(link_elem)
            red.hset("articles", base_url, json.dumps(link_elem))

        links = list(soup.find_all('a'))
        shuffle(links)

        count = 10
        for url in links:
            count -=1
            if count < 0:
                pass
                # continue

            href = url.get('href')
            child_url = urljoin(base_url, href)
            url_components = urlparse(child_url)

            if url_components.scheme not in ["http", "https"]:
                continue

            child_base_url = url_components.scheme + "://" + url_components.netloc

            if not base_url.startswith(child_base_url):
                continue

            dfs_visit(child_url, depth + 1, max_depth, visited_links)

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print(e)

    return visited_links


if __name__ == '__main__':
    visited_links = {}
    for base_url in links_to_visit:
        visited_links = dfs_visit(base_url, 0, 1, visited_links)


print(len(visited_links))
