#!/bin/bash

if [[ $(id -u) -ne 0 ]] ; then 
	echo "Please run with sudo! sudo ./setup.sh" ; 
	exit 1 ; 
fi

# update system
apt -y update
apt -y upgrade

# install handy packages
apt -y install vim git docker-compose 

# remove packets that may interfer 
apt -y remove docker docker-engine docker.io containerd runc

# install requirements
apt -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common

# install docker via script from get.docker.com
if [ $(which docker) != "/usr/bin/docker" ]; then
	curl -sSL https://get.docker.com | sh
fi

# add user pi to docker group
usermod -aG docker pi

# clone git repo if not alread present
if [ ! -d "alarmpi" ]; then
	git clone https://github.com/Bouni/alarmpi.git
fi

# change owner to pi:pi
chown -R pi:pi alarmpi

# checkout docker branch
cd alarmpi
git checkout alarmpi-docker 
