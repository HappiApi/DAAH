#!/bin/bash
REPO="https://github.com/HappiApi/DAAH.git"

echo Fresh new machine! I like!

# sudo adduser dev
# sudo passwd dev
# gpasswd -a dev wheel
# su dev

sudo yum -y install binutils gcc make patch libgomp glibc-headers glibc-devel kernel-headers kernel-devel git epel-release wget

sudo yum -y install python34 python34-devel
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.4 get-pip.py

sudo rpm -Uvh http://yum.postgresql.org/9.4/redhat/rhel-7-x86_64/pgdg-centos94-9.4-1.noarch.rpm
sudo yum -y update
sudo yum -y install postgresql94-server postgresql94-contrib postgresql94-libs postgresql94-devel
sudo /usr/pgsql-9.4/bin/postgresql94-setup initdb
sudo systemctl start postgresql-9.4
sudo systemctl enable postgresql-9.4

git clone $REPO daah
sudo chown -R `whoami` daah/
cd daah
sudo pip3 install virtualenv
virtualenv venv
echo "export APP_SETTINGS='config.DevelopmentConfig'" >> venv/bin/activate
echo "export DATABASE_URL='postgres://postgres@localhost'" >> venv/bin/activate
source venv/bin/activate
PATH=$PATH:/usr/pgsql-9.4/bin/ pip3 install -r requirements.txt

# pip3 install uwsgi
