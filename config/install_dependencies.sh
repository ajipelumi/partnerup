#!/bin/bash

# Install pip
apt-get update
apt-get install -y python3-pip

# Install Flask
pip install flask

# Install Gunicorn
pip install gunicorn

# Install PyGithub
pip install pygithub

# Install Matplotlib
pip install matplotlib

# Install Flask-Cors
pip install flask-cors

# Install SQLAlchemy
pip install sqlalchemy

# Install SQLClient
sudo apt install -y python3-dev default-libmysqlclient-dev build-essential

# Install MySQL
sudo apt install -y mysql-server

# Install Nginx
sudo apt install -y nginx

# Install Dotenv
pip install python-dotenv