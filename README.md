# scraper-github

To build scraper type:

`docker build -t docker-scraper .`

To run docker image use command:

`sudo docker run -d -p 5000:5000 docker-scraper`


Scraper return urls searched in github. Scraper handle three types of searching:
- Repositories
- Issues
- Wikis

 To make request json body prepare http post http://127.0.0.1:5000/find_resource with header and json  body. Example post request by curl:

curl -X POST -H 'Content-Type: application/json' -i 'http://127.0.0.1:5000/find_resource' --data '{
  "keywords": [
    "openstack",
    "nova",
    "css"
  ],
  "proxies": [
    "93.152.176.225:54136",
    "185.189.211.70:8080"
  ],
  "type": "Repositories"
}'
