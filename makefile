#!/bin/bash -x

# sudo docker kill "$(sudo docker ps -q)"
sudo docker-compose up --build

#sudo docker kill $(sudo docker ps -q)

#sudo docker rm $(sudo docker ps -a -q)
#sudo docker rmi $(sudo docker images -q)