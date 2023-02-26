#!/bin/bash
IMAGE_NAME=lab2_predict_app
APP_NAME=lab2_predict_app

echo "training model using training script train.py"
python ./trainer/train.py

echo "moving pkl file to src directory"
mv model_pipeline.pkl ./src/

echo "building docker image with name lab2_predict_app from Dockerfile"
docker build ./ -t ${IMAGE_NAME}:v1

echo "running built docker container in detached mode"
docker run -d -p 8000:8000 --name ${APP_NAME} ${IMAGE_NAME}:v1

echo "confirming docker container health status before continuing"
finished=false
while ! $finished; do
    health_status=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/health")
    if [ $health_status == "200" ]; then
        finished=true
        echo "API is ready"
    else
        echo "API not responding yet"
        sleep 1
    fi
done


echo "testing '/hello' endpoint with ?name=Shehzad"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=Shehzad"

echo "testing '/hello/ endpoint with no query parameter"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello"

echo "testing '/' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/"

echo "testing '/docs' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/docs"

echo "testing '/openapi.json' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/openapi.json"

echo "testing health endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/health"

echo "testing prediction endpoint"
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
    {
        "AveBedrms": 0,
        "Population": 0,
        "MedInc": 0,
        "HouseAge": 0,
        "AveRooms": 0,
        "Latitude": 0,
        "Longitude": 0,
        "AveOccup": 0
    }
]'

echo "\\n"
echo "stopping and remove docker container"
docker stop ${APP_NAME}
docker rm ${APP_NAME}

echo "delete image"
docker image rm ${APP_NAME}:v1