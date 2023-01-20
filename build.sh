docker build -t docker-sparkml .
docker run -it -p 8080:8080 -d docker-sparkml
