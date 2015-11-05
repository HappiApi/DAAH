#!/bin/bash
echo Fresh new machine! I like!

sudo rpm -Uvh http://yum.postgresql.org/9.4/redhat/rhel-7-x86_64/pgdg-centos94-9.4-1.noarch.rpm
sudo yum update
sudo yum install postgresql94-server postgresql94-contrib postgresql94-libs postgresql94-devel
sudo /usr/pgsql-9.4/bin/postgresql94-setup initdb
sudo systemctl start postgresql-9.4
sudo systemctl enable postgresql-9.4
git clone https://github.com/HappiApi/DAAH.git daah
cd daah
virtualenv venv
echo "export APP_SETTINGS='config.DevelopmentConfig'" >> venv/bin/activate
echo "export DATABASE_URL='postgres://postgres@localhost'" >> venv/bin/activate
source venv/bin/activate
pip install uwsgi
pip install -r requirements.txt
python app.py

