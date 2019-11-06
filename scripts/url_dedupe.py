from google.cloud import firestore
from pprint import pprint

firedb = firestore.Client()

def dedupe():
    coll = firedb.collection(u'articles')

    docs = coll.stream()

    url_set = set()

    for doc in docs:
        _doc = doc.to_dict()
        same_docs = coll.where(u'url', u'==', _doc["url"]).stream()

        if len(list(same_docs)):
            print("Found existing document. Updating : ", _doc["url"])


        continue


        if "url" in _doc:
            if _doc["url"] in url_set:
                print("Found duplicate!", _doc["url"])
                coll.document(doc.id).delete()
            else:
                # print(u'{} => {}'.format(doc.id, _doc["url"]))
                url_set.add(_doc["url"])
        else:
            print(doc.id)
            pprint(_doc)
            coll.document(doc.id).delete()
            print("Delete Document without url")

if __name__ == '__main__':
    print("Starting Deduplication")
    dedupe()
