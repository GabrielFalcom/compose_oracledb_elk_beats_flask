FROM ubuntu:16.04 AS base

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-wheel \
    openjdk-8-jdk-headless \
    wget \
    apt-transport-https \
    supervisor \
    libaio1 \
    alien

RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -

RUN echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-6.x.list

RUN apt-get update && apt-get install metricbeat

RUN apt-get update && apt-get install elasticsearch

RUN apt-get update && apt-get install kibana

RUN apt-get update && apt-get install logstash

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

RUN cp elasticsearch.yml /etc/elasticsearch/

RUN cp kibana.yml /etc/kibana/

RUN cp system.yml /etc/metricbeat/modules.d/

RUN  alien -i oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm && \
     alien -i oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm && \
     alien -i oracle-instantclient12.2-sqlplus-12.2.0.1.0-1.x86_64.rpm  && \
     echo /usr/lib/oracle/12.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient12.2.conf && \
     ldconfig
