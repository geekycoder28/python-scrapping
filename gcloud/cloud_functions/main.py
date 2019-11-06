from bs4 import BeautifulSoup
import urllib
from urllib.parse import urljoin, urlparse
from pprint import pprint
from random import shuffle
from os import path
from io import BytesIO
from urllib.error import HTTPError
import requests
import json
import sys, traceback
import time
import os
import redis
from selenium import webdriver
from selenium.webdriver import firefox
from PIL import Image
from flask import jsonify
from pprint import pprint
from bs4.element import Comment
import signal

dirpath = os.getcwd()
driver_binary_path = os.path.join(dirpath, "webdrivers")

os.environ["PATH"] += os.pathsep + driver_binary_path

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

class TimeoutError(Exception):
    pass

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)


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

def get_link_info(url, ignore_cache=False):
    print("Getting Link info url: ", url)
    cached_url_info = red.hget("articles", url)

    if ignore_cache:
        print("Ignoring Cache")
    elif cached_url_info:
        cached_url_info = json.loads(cached_url_info)
        print("Found url in cache: ")
        return cached_url_info
    else:
        print("Url not found in cache: ")



    try:
        source = urllib.request.urlopen(url).read()
    except HTTPError as e:
        result = requests.get(url)
        source = result.content

    soup = BeautifulSoup(source, 'lxml')

    link_info = {
        "url" : url,
        "title" : str(soup.title.string),
        "last_visit_time" : int(time.time())
    }

    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)

    visible_texts= [t.strip() for t in visible_texts]
    visible_texts = list(filter(lambda t: len(t) > 128, visible_texts))
    link_info["body_text"] = visible_texts

    largest_image_size = 0
    largest_image_url = ""
    primary_image_props = {}
    logo = {}


    with webdriver.Chrome("./webdrivers/chromedriver", chrome_options=chrome_options) as driver:

        print("Start loading url", url)
        try:
            with timeout(seconds=15):
                driver.get(url)
        except TimeoutError as te:
            print("Timeout Error for url", url)
            return {}
        print("Done loading url", url)


        images = driver.find_elements_by_tag_name('img')
        for image in images:
            img_url = image.get_attribute('src')

            image_props = getsizes(img_url)

            img_area = image_props["height"] * image_props["width"]

            if img_url and "url" not in logo and "logo" in img_url.lower():
                logo = {
                    "url" : img_url,
                    "height" : image_props["height"],
                    "width" : image_props["width"]
                }

            if img_area > largest_image_size:
                largest_image_size = img_area
                largest_image_url = img_url
                primary_image_props = {
                    "url" : img_url,
                    "height" : image_props["height"],
                    "width" : image_props["width"]
                }



    link_info["image"] = primary_image_props
    link_info["logo"] = logo

    red.hset("articles", url, json.dumps(link_info))
    print("Wrote url to cache: ", url)
    return link_info

def process_link(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args
    try:
         # Set CORS headers for the preflight request
        if request.method == 'OPTIONS':
            # Allows GET requests from any origin with the Content-Type
            # header and caches preflight response for an 3600s
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }

            return ('', 204, headers)

        # Set CORS headers for the main request
        headers = {
            'Access-Control-Allow-Origin': '*'
        }


        if request_json and 'url' in request_json:
            url = request_json['url']

            ignore_cache = "ignore_cache" in request_json and request_json['ignore_cache'] in ["True", "true", "1", "T", "t", True]

            link_info = get_link_info(url, ignore_cache)

            return (jsonify(link_info), 200, headers)


        elif request_args and 'name' in request_args:
            name = request_args['name']
        else:
            name = 'World'
        return 'Hello You!' + request.method + "\n"
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print(e)

    return 'Error'
