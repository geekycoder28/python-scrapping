from PIL import Image
from bs4 import BeautifulSoup
from bs4.element import Comment
from google.cloud import pubsub_v1, firestore
from io import BytesIO
from pprint import pprint
from random import shuffle
from selenium import webdriver
from selenium.webdriver import firefox
from time import gmtime, strftime
from urllib import request
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
import json
import os
import redis
import requests
import signal
import sys, traceback
import time
import tldextract

TIMEOUT = 15
MAX_URL_LENGTH = 200
PROJECT = "proxima-media"
PUBSUB_TOPIC = "scrape-urls"
subscription_name = "url-scrapper-sub"

firedb = firestore.Client()
coll = firedb.collection(u'articles')
dirpath = os.getcwd()
chrome_driver_path = ".app/webdrivers/chromedriver"
chrome_driver_path = os.path.join(dirpath, "app/webdrivers/chromedriver")
driver_binary_path = os.path.join(dirpath, "app/webdrivers")
os.environ["PATH"] += os.pathsep + driver_binary_path


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT, PUBSUB_TOPIC)


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

def getsizes(img_url, ignore_cache=False):
    try:
        img_info = red.hget("image-cache", img_url)
        if not ignore_cache and img_info:
            img_info = json.loads(img_info)
            return img_info
        else:
            req  = requests.get(img_url, timeout=TIMEOUT)
            im = Image.open(BytesIO(req.content))
            img_info = {
                "height" : im.size[0],
                "width" : im.size[1]
            }
            red.hset("image-cache", img_url,  json.dumps(img_info))
            return img_info
    except Exception as e:
        print(img_url, e)

    img_info = {
        "height" : 0,
        "width" : 0
    }
    red.hset("image-cache", img_url,  json.dumps(img_info))
    return img_info

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
        source = request.urlopen(url, timeout=TIMEOUT).read()
    except HTTPError as e:
        result = requests.get(url, timeout=TIMEOUT)
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
    visible_texts_256 = list(filter(lambda t: len(t) > 256, visible_texts))
    link_info["body_text"] = visible_texts
    link_info["body_text_256"] = visible_texts_256

    largest_image_size = 0
    largest_image_url = ""
    primary_image_props = {}
    logo = {}

    try:
        with webdriver.Chrome(chrome_driver_path, options=chrome_options) as driver:

            print("Start loading url", url)
            driver.get(url)
            print("Done loading url", url)


            images = driver.find_elements_by_tag_name('img')
            print("Found ", len(images), " Images for url ", url)
            for image in images:
                img_url = image.get_attribute('src')

                if not img_url:
                    continue

                image_props = getsizes(img_url, ignore_cache)

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
    except Exception as e:
        print("Error!", e)
        traceback.print_exc(file=sys.stdout)
    return link_info



def filter_domain_urls(child_url_list, base_url):
    damain_urls = []
    for child_url in child_url_list:
        href = child_url.get('href')
        child_url = urljoin(base_url, href)

        url_components = urlparse(child_url)

        if url_components.scheme not in ["http", "https"]:
            continue

        child_url_extract = tldextract.extract(child_url)
        base_url_extract = tldextract.extract(base_url)

        if child_url_extract.domain != base_url_extract.domain:
            continue

        damain_urls.append(child_url)

    return damain_urls


def callback(message):
    try:
        data = json.loads(message.data.decode("utf-8"))
        url = data["url"]
        # print("Processing url: ", url)

        depth = data["depth"]
        max_depth = data["max_depth"]
        if depth > max_depth:
            message.ack()
            return

        if len(url) > MAX_URL_LENGTH:
            message.ack()
            return

        ignore_cache = "ignore_cache" in data and \
            data['ignore_cache'] in ["True", "true", "1", "T", "t", True]

        if ignore_cache:
            print("Ignoring Cache for url: ", url)
        else:
            crawled_link = red.hget("crawled-links", url)
            if crawled_link:
                message.ack()
                return

        try:
            source = request.urlopen(url, timeout=TIMEOUT).read()
        except HTTPError as e:
            result = requests.get(url, timeout=TIMEOUT)
            source = result.content
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print(e)
            message.ack()
            return


        soup = BeautifulSoup(source, 'lxml')
        links = list(soup.find_all('a'))
        links = filter_domain_urls(links, url)
        shuffle(links)
        # print("Found {l} links in page {u}".format(l=len(links), u=url))

        for link in links:

            pub_data = {
                "time" : strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                "url" : link,
                "depth" : depth + 1,
                "max_depth" : max_depth,
                "ignore_cache": False
            }
            publisher.publish(topic_path, data=json.dumps(pub_data).encode('utf-8'))

        link_info = get_link_info(url, ignore_cache)

        if len(link_info["body_text_256"]) > 3:
            coll.add(link_info)
        red.hset("crawled-links", url, json.dumps(link_info))
        message.ack()
    except Exception as e:
        if url:
            print("Error in url: ", url)
        traceback.print_exc(file=sys.stdout)
        print(e)
        message.ack()


if __name__ == '__main__':
    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print("Starting Webscrapper Application")
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        PROJECT, subscription_name)
    subscriber.subscribe(subscription_path, callback=callback)
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)
