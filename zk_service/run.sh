#!/bin/bash -x

ZOO_CFG="/opt/zookeeper/conf/zoo.cfg"

# Check if the config file exist before starting
while [ ! -f ${ZOO_CFG} ]
do
  echo "The ${ZOO_CFG} does not exist.  Waiting..."
  sleep 5
done

# Start Zookeeper
/opt/zookeeper/bin/zkServer.sh start-foreground