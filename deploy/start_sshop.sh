#!/bin/bash
find /var/lib/mysql/mysql -exec touch -c -a {} +
service nginx start
service mysql start
RET=1
while [[ RET -ne 0 ]]; do
    echo "MySQL is unavailable - sleeping"
    sleep 5
    mysql -uroot -e "status" > /dev/null 2>&1
    RET=$?
done
mysql -uroot -e "CREATE USER '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD'"
mysql -uroot -e "GRANT ALL PRIVILEGES ON *.* TO '$MYSQL_USER'@'%' WITH GRANT OPTION"
mysql -uroot -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE CHARACTER SET utf8"
su ciscn -l -c "sed -i \"s/INIT_DB_USER/$MYSQL_USER/g\" /home/ciscn/www/settings.py"
su ciscn -l -c "sed -i \"s/INIT_DB_PASS/$MYSQL_PASSWORD/g\" /home/ciscn/www/settings.py"
su ciscn -l -c "python3 manage.py makemigrations sshop"
su ciscn -l -c "python3 manage.py migrate"
su ciscn -l -c "python3 set_database.py 100"
su ciscn -l -c "python3 set_admin.py"
su ciscn -l -c "python3 set_flag.py \"$INIT_FLAG\""
su ciscn -l -c "nohup gunicorn www.wsgi:application -c gunicorn.conf.py >/dev/null 2>&1 &"