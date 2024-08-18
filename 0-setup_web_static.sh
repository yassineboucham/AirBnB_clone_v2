#!/usr/bin/env bash
#sets up your web servers for the deployment of web_static

sudo apt update
sudo apt install nginx
sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html
sudo echo "<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello, World!</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>" | sudo tee /data/web_static/releases/test/index.html
sudo ln -s -f "/data/web_static/releases/test/"  "/data/web_static/current"
sudo chown -R ubuntu:ubuntu  /data/
sudo sed -i '/server {/a \ \n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
sudo systemctl restart nginx
