from google.cloud import pubsub_v1
from time import gmtime, strftime
import json
from pprint import pprint

PROJECT = "proxima-media"
PUBSUB_TOPIC = "scrape-urls"

links_to_visit = [
    "https://www.nation.co.ke/",
    "https://www.thecitizen.co.tz/",
    "https://www.monitor.co.ug/",
    "https://www.aljazeera.com",
    "https://www.newvision.co.ug/",
    "https://www.standardmedia.co.ke/",
    "http://www.swahilihub.com/",
    "https://www.the-star.co.ke/",
    "https://www.bbc.com/",
    "https://www.capitalfm.co.ke/",
    "https://www.theguardian.com/",
    "https://www.thesouthafrican.com/",
    "https://www.timeslive.co.za/",
    "https://www.iol.co.za/",
    "https://www.sowetanlive.co.za/",
    "http://nairobiwire.com/",
    "https://allafrica.com/",
    "https://www.nytimes.com/",
    "https://borkena.com/",
    "http://www.tigraionline.com/",
    "https://www.ezega.com/",
    "https://punchng.com/",
]

def publish():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT, PUBSUB_TOPIC)

    for url in links_to_visit:
        message = {
            "time" : strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            "url" : url,
            "depth" : 0,
            "max_depth" : 1,
            "ignore_cache": True
        }

        pprint(message)

        publisher.publish(topic_path, data=json.dumps(message).encode('utf-8'))

if __name__ == '__main__':
    publish()
