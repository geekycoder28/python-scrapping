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
import os
import sys, traceback
from bs4.element import Comment
import time
from google.cloud import firestore
from main import get_link_info

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

firedb = firestore.Client()

coll = firedb.collection(u'articles')
links_to_visit = [
    "https://www.nation.co.ke/",
    "https://www.thecitizen.co.tz/",
    # "https://www.monitor.co.ug/",
    # "https://www.aljazeera.com",
    # "https://www.newvision.co.ug/",
    "https://www.standardmedia.co.ke/",
    # "http://www.swahilihub.com/",
    "https://www.the-star.co.ke/",
    # "https://www.bbc.com/",
    "https://www.capitalfm.co.ke/",
    # "https://www.theguardian.com/",
    # "https://www.thesouthafrican.com/",
    # "https://www.timeslive.co.za/",
    # "https://www.iol.co.za/",
    # "https://www.sowetanlive.co.za/",
    "http://nairobiwire.com/",
    # "https://allafrica.com/",
    # "https://www.nytimes.com/",
    # "https://borkena.com/",
    # "http://www.tigraionline.com/",
    # "https://www.ezega.com/",
    # "https://punchng.com/",
]

shuffle(links_to_visit)
# links_to_visit = set(links_to_visit)

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

def dfs_visit(url, depth, max_depth):

    if depth > max_depth:
        return
    crawled_link = red.hget("crawled-links", url)
    if crawled_link:
        return

    try:
        try:
            source = request.urlopen(url).read()
        except HTTPError as e:
            result = requests.get(url)
            source = result.content

        soup = BeautifulSoup(source, 'lxml')
        links = list(soup.find_all('a'))
        shuffle(links)


        print("Found {l} links in page {u}".format(l=len(links), u=url))

        count = 10
        for child_url in links:



            count -=1
            if count < 0:
                pass
                # continue

            href = child_url.get('href')
            child_url = urljoin(base_url, href)
            url_components = urlparse(child_url)

            if url_components.scheme not in ["http", "https"]:
                continue

            child_base_url = url_components.scheme + "://" + url_components.netloc

            if not base_url.startswith(child_base_url):
                continue


            dfs_visit(child_url, depth + 1, max_depth)


        link_info = get_link_info(url)

        for k, v in link_info.items():
            if isinstance(v, (str, dict, list, int)):
                continue
            print(type(k), type(v),k, v)
        # pprint(link_info)
        coll.add(link_info)
        red.hset("crawled-links", url, json.dumps(link_info))

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print(e)

    return


if __name__ == '__main__':
    pprint(links_to_visit)
    while True:
        for base_url in links_to_visit[0:4]:
            print("Attempt to crawl", base_url)
            dfs_visit(base_url, 0, 4)
        red.delete("crawled-links")
