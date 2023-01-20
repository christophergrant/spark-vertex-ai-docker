docker build -t docker-sparkml .
docker kill $(docker ps -q)
docker run -it -p 8080:8080 -d docker-sparkml
