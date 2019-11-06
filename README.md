## GKE and GCR

```
docker build -f Dockerfile -t news_scrapper .
docker tag news_scrapper:latest eu.gcr.io/proxima-media/news_scrapper
docker push eu.gcr.io/proxima-media/news_scrapper
kubectl create -f deploy.yaml
```
