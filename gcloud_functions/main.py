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
from PIL import Image
from flask import jsonify
from pprint import pprint
from bs4.element import Comment

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
        if request_json and 'url' in request_json:
            url = request_json['url']
            try:
                source = urllib.request.urlopen(url).read()
            except HTTPError as e:
                result = requests.get(url)
                source = result.content

            soup = BeautifulSoup(source, 'lxml')

            link_info = {
                "url" : url,
                "title" : soup.title.string,
            }

            texts = soup.findAll(text=True)
            visible_texts = filter(tag_visible, texts)

            visible_texts= [t.strip() for t in visible_texts]
            visible_texts = list(filter(lambda t: len(t) > 128, visible_texts))
            link_info["body_text"] = visible_texts

            largest_image_size = 0
            largest_image_url = ""
            image = {}
            logo = {}
            for tag in soup.findAll("img"):

                img_url = urljoin(url, tag['src'])
                image_props = getsizes(img_url)

                img_area = image_props["height"] * image_props["width"]

                if "url" not in logo and "logo" in img_url.lower():
                    logo = {
                        "url" : img_url,
                        "height" : image_props["height"],
                        "width" : image_props["width"]
                    }

                if img_area > largest_image_size:
                    largest_image_size = img_area
                    largest_image_url = img_url
                    image = {
                        "url" : img_url,
                        "height" : image_props["height"],
                        "width" : image_props["width"]
                    }

            link_info["image"] = image
            link_info["logo"] = logo

            return jsonify(link_info)


        elif request_args and 'name' in request_args:
            name = request_args['name']
        else:
            name = 'World'
        return 'Hello You!' + url + "\n"
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print(e)
    return 'Error'
