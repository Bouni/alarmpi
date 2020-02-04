#!/bin/bash

# Update package index
sudo apt-get update

# Upgrade system
sudo apt-get upgrade

# install packages
sudo apt install git curl

# Install docker
curl -sSL https://get.docker.com | sh

# add pi user to docker group
usermod -aG docker pi

# install pip3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && sudo python3 get-pip.py

# install docker-compose
sudo pip3 install docker-compose


