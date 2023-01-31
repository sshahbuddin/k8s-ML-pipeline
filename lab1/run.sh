#!/bin/bash

echo "building docker image with name lab1_fastAPI from Dockerfile"
docker build . -t lab1_hello_app:v1

echo "running built docker container in detached mode"
docker run -d -p 8000:8000 --name lab1_hello_app lab1_hello_app:v1

echo "waiting for docker container to run"
sleep 5

echo "testing '/hello' endpoint with ?name=Shehzad"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=Shehzad"

echo "testing '/hello/ endpoint with no query parameter"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello"

echo "testing '/' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/"

echo "testing '/docs' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/docs"

echo "testing '/openapi.json' endpoint "
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/openapi.json"

echo "stopping docker container"
docker stop lab1_hello_app

echo "removing docker container"
docker rm lab1_hello_app