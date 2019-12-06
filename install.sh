#!/bin/bash

# Install git and Ansible
apt -y install git ansible curl

# Copy ansible playbook script from github
https://raw.githubusercontent.com/Bouni/alarmpi/master/ansible/playbooks/alarmpi.yaml -O /home/pi/alarmpi.yaml

# Run playbook
ansible-playbook /home/pi/alarmpi.yaml

# Delete playbook
rm /home/pi/alarmpi.yaml
