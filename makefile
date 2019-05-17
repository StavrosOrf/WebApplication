#!/bin/bash -x

# sudo docker kill "$(sudo docker ps -q)"
#sudo docker swarm leave --force
# sudo docker swarm init
# sudo docker-compose build
# sudo docker stack deploy -c docker-compose.yml WebApplication
sudo docker-compose up --build 

#--scale web_service=5

#sudo docker kill $(sudo docker ps -q)

#sudo docker rm $(sudo docker ps -a -q)
#sudo docker rmi $(sudo docker images -q)