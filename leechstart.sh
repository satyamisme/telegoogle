#!/bin/bash


echo yes |sudo apt install python3 python3-pip
echo yes | pip3 install -r requirements-cli.txt
echo yes | pip3 install -r requirements.txt
cp config_sample.env config.env
echo yes | sudo docker container prune
echo yes | sudo docker image prune -a
sudo dockerd
sudo docker build . -t mirror-bot
sudo docker run -p 60:60 mirror-bot
