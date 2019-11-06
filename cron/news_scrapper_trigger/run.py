from google.cloud import pubsub_v1
from time import gmtime, strftime
import json
from pprint import pprint

PROJECT = "proxima-media"
PUBSUB_TOPIC = "scrape-urls"

links_to_visit = [
    {"url": "https://www.nation.co.ke/", "ttl" : 15, "ttl" : 15},
    {"url": "https://www.thecitizen.co.tz/", "ttl" : 15},
    {"url": "https://www.monitor.co.ug/", "ttl" : 15},
    {"url": "https://www.aljazeera.com", "ttl" : 15},
    {"url": "https://www.newvision.co.ug/", "ttl" : 15},
    {"url": "https://www.standardmedia.co.ke/", "ttl" : 15},
    {"url": "http://www.swahilihub.com/", "ttl" : 15},
    {"url": "https://www.the-star.co.ke/", "ttl" : 15},
    {"url": "https://www.bbc.com/", "ttl" : 15},
    {"url": "https://www.capitalfm.co.ke/", "ttl" : 15},
    {"url": "https://www.theguardian.com/", "ttl" : 15},
    {"url": "https://www.thesouthafrican.com/", "ttl" : 15},
    {"url": "https://www.timeslive.co.za/", "ttl" : 15},
    {"url": "https://www.iol.co.za/", "ttl" : 15},
    {"url": "https://www.sowetanlive.co.za/", "ttl" : 15},
    {"url": "http://nairobiwire.com/", "ttl" : 15},
    {"url": "https://allafrica.com/", "ttl" : 15},
    {"url": "https://www.nytimes.com/", "ttl" : 15},
    {"url": "https://borkena.com/", "ttl" : 15},
    {"url": "http://www.tigraionline.com/", "ttl" : 15},
    {"url": "https://www.ezega.com/", "ttl" : 15},
    {"url": "https://punchng.com/", "ttl" : 15},
]

def publish():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT, PUBSUB_TOPIC)

    for url_info in links_to_visit:
        message = {
            "depth" : 0,
            "max_depth" : 3,
            "ignore_cache": True
        }

        message.update(url_info)

        publisher.publish(topic_path, data=json.dumps(message).encode('utf-8'))

if __name__ == '__main__':
    publish()
