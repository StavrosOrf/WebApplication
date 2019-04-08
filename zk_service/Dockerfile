FROM vungle/base

RUN apt-get update && apt-get install -y openjdk-7-jre-headless wget jq
RUN wget -q -O - http://apache.mirrors.pair.com/zookeeper/stable/zookeeper-3.4.14.tar.gz | tar -xzf - -C /opt \
    && mv /opt/zookeeper-3.4.14 /opt/zookeeper \
    && cp /opt/zookeeper/conf/zoo_sample.cfg /opt/zookeeper/conf/zoo.cfg \
    && mkdir -p /tmp/zookeeper

ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64

ADD . /opt/scripts
RUN chmod 777 /opt/scripts/*

EXPOSE 2181

WORKDIR /opt/zookeeper

VOLUME ["/opt/zookeeper/conf", "/tmp/zookeeper"]

CMD ["/opt/scripts/run.sh"]