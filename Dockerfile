FROM amazoncorretto:8

RUN yum update -y

RUN yum install gcc openssl-devel bzip2-devel libffi-devel gzip make procps -y
RUN yum install wget tar -y
WORKDIR /opt
RUN wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz
RUN tar xzf Python-3.9.6.tgz
WORKDIR /opt/Python-3.9.6
RUN ./configure --enable-optimizations
RUN make altinstall
RUN rm -f /opt/Python-3.9.6.tgz
RUN ln -s /opt/Python-3.9.6/python /opt/Python-3.9.6/python3


ENV PATH="$PATH:/opt/Python-3.9.6/"


# Install libraries
COPY ./requirements.txt ./
RUN ./python -m pip install -r requirements.txt && \
    rm ./requirements.txt

# Setup container directories
RUN mkdir /sparkml

# Copy local code to the container
WORKDIR /
COPY ./sparkml /sparkml
COPY ./main.py main.py

# launch server with gunicorn
EXPOSE 8080
CMD ["gunicorn", "main:app", "--timeout=0", "--preload", \
    "--workers=1", "--threads=4", "--bind=0.0.0.0:8080"]
