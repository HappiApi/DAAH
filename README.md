# DAAH

A simple app in flask used for scenario week 1 to set up staging/production environment
 
## Setup
The bootstrap.sh script is used to setup the application on a clean 
server running CentOS 7.

## Run gunicorn
gunicorn --bind 127.0.0.1:8080 wsgi:app

## Run nginx
copy the nginx config file to /etc/nginx/
### Then to start
sudo systemctl enable nginx (to start nginx on reboot)
sudo systemctl start nginx 



