#!/bin/bash
REPO="https://github.com/HappiApi/DAAH.git"

echo Fresh new machine! I like!

# sudo adduser dev
# sudo passwd dev
# gpasswd -a dev wheel
# su dev

sudo yum -y install gcc make git epel-release wget nginx

sudo yum -y install python34 python34-devel
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.4 get-pip.py

sudo rpm -Uvh http://yum.postgresql.org/9.4/redhat/rhel-7-x86_64/pgdg-centos94-9.4-1.noarch.rpm
sudo yum -y update
sudo yum -y install postgresql94-server postgresql94-contrib postgresql94-libs postgresql94-devel
sudo /usr/pgsql-9.4/bin/postgresql94-setup initdb

git clone $REPO daah
sudo chown -R `whoami` daah/
cd daah

#copy in pgsql_hba.conf
sudo cp pg_hba.conf /var/lib/pgsql/9.4/data/pg_hba.conf

sudo systemctl start postgresql-9.4
sudo systemctl enable postgresql-9.4

sudo pip3 install virtualenv
virtualenv venv
echo "export APP_SETTINGS='config.DevelopmentConfig'" >> ~/.bash_profile
echo "export DATABASE_URL='postgres://localuser@localhost/postgres'" >> ~/.bash_profile
echo "export PATH=\$PATH:/usr/pgsql-9.4/bin/" >> ~/.bash_profile
source ~/.bash_profile

source venv/bin/activate
pip3 install -r requirements.txt

# removing the old postgres version
deactivate
# sudo yum remove postgresql

sudo /bin/bash << EOF
sudo -u postgres psql postgres -c "CREATE USER localuser WITH PASSWORD 'localuser'; GRANT ALL PRIVILEGES ON DATABASE postgres TO localuser; ALTER DATABASE postgres OWNER TO localuser; "
EOF

# schedule backup for 1 AM
sudo crontab -l > mycron
echo "0 1 * * * bash ~/DAAH/scripts/backup.sh" >> mycron
crontab mycron
rm mycron

#start the server
source venv/bin/activate
#upgrade database
python3.4 manage.py db upgrade
gunicorn --bind 127.0.0.1:8080 wsgi:app &
deactivate

#copy in nginx conf file
sudo usermod -a -G `whoami` nginx
chmod 710 /home/`whoami`
sudo cp nginx.conf /etc/nginx/nginx.conf
sudo systemctl enable nginx
sudo systemctl start nginx

# sudo cp gunicorn.service /etc/systemd/system/gunicorn.service
# sudo systemctl start gunicorn
# sudo systemctl enable gunicorn

echo Pray for the best!
