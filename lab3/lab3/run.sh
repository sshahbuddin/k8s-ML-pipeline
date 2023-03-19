#!/bin/bash
IMAGE_NAME=predict-api
APP_NAME=predict-api

echo "training model using training script train.py"
python ./trainer/train.py

echo "moving pkl file to src directory"
mv model_pipeline.pkl ./src/

echo "starting minikube"
minikube start --kubernetes-version=v1.25.4

echo "setup docker daemon to minikube"
eval $(minikube docker-env)

echo "building docker image with name predict-api from Dockerfile"
docker build ./ -t ${IMAGE_NAME}:v1

echo "apply k8s namespace and set subsequent k8s commands to namespace"
kubectl apply -f infra/namespace.yaml
kubectl config set-context --current --namespace=w255


echo "apply deployments and services"
kubectl apply -f infra

echo "check infra"
kubectl get all

echo "pod readiness test"
while kubectl get pods -o jsonpath='{.items[0].status.conditions[1].status}' | grep False; do echo "Pod not ready, waiting...";sleep 5;done

echo "check infra again"
kubectl get all

echo "port forward predict-api deployment"
kubectl port-forward deployment/predict-api 8000:8000 &

echo "port forward redis to check cache"
kubectl port-forward deployment/predict-api 6379:6379 &

echo "liveness check"
while ! nc -z localhost 8000; do echo "Service is not yet running on port 8000, waiting...";sleep 5;done

echo "check infra again"
kubectl get all

echo "check infra again"
kubectl get all

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
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "homes": [
    {
      "MedInc": 0,
      "HouseAge": 0,
      "AveRooms": 0,
      "AveBedrms": 0,
      "Population": 0,
      "AveOccup": 0,
      "Latitude": 0,
      "Longitude": 0
    }
  ]
}'

echo "testing prediction endpoint multiple predictions"
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "homes": [
    {
      "MedInc": 0,
      "HouseAge": 0,
      "AveRooms": 0,
      "AveBedrms": 0,
      "Population": 0,
      "AveOccup": 0,
      "Latitude": 0,
      "Longitude": 0
    },
    {
      "MedInc": 8.3252,
      "HouseAge": 41.0,
      "AveRooms": 6.98412698,
      "AveBedrms": 1.02380952,
      "Population": 322.0,
      "AveOccup": 2.55555556,
      "Latitude": 37.88,
      "Longitude": -122.23
    }
  ]
}'

echo "\\n"

echo "check keys in redis"
redis-cli --scan --pattern '*'


echo "delete all services"  
kubectl delete --all services

echo "delete all deployments"
kubectl delete --all deployments

echo "delete w255 namespace"
kubectl delete namespace w255

echo "stop minikube"
minikube stop