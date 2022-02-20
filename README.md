# SimplePythonRedisApp

Simple Python working with Redis on Kubernetes.

1. Build docker image: 
docker build -t my-python-web:v0.6 app/

2. Create Kubernetes namespace:
kubectl create namespace python-redis

3. Create Redis deployment & service
kubectl create -f kubernetes/redis/redis-deployment.yml 
kubectl create -f kubernetes/redis/redis-service.yml 

3. Create SimplePythonRedisApp deployment & services
kubectl create -f kubernetes/SimplePythonRedisApp/SimplePythonRedisApp-deployment.yml
kubectl create -f kubernetes/SimplePythonRedisApp/SimplePythonRedisApp-service.yml
kubectl create -f kubernetes/SimplePythonRedisApp/SimplePythonRedisApp-metrics-service.yml 

4. Create Prometheus config map, deployment & service
kubectl create -f kubernetes/prometheus/config-map.yaml
kubectl create -f kubernetes/prometheus/prometheus-deployment.yaml
kubectl create -f kubernetes/prometheus/prometheus-service.yaml

SimplePythonRedisApp How to?

Sending data to Redis:
curl -X POST -d "" "http://localhost:8080/?id=test_key"

Getting data from Redis:
curl -X GET "http://localhost:8080/?id=test_key"

Deleting data in Redis:
curl -X DELETE -d "" "http://localhost:8080/?id=test_key"

If the key does not exist in Redis, the application will return HTTP 404 Not Found.
