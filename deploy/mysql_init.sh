#!/bin/bash

# https://github.com/moby/moby/issues/34390
find /var/lib/mysql/mysql -exec touch -c -a {} +

/usr/bin/mysqld_safe > /dev/null 2>&1 &

RET=1
while [[ RET -ne 0 ]]; do
    echo "=> Waiting for confirmation of MySQL service startup"
    sleep 5
    mysql -uroot -e "status" > /dev/null 2>&1
    RET=$?
done

echo "=> Creating MySQL ${MYSQL_USER} user with ${MYSQL_PASS} password"

mysql -uroot -e "CREATE USER '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASS'"
mysql -uroot -e "GRANT ALL PRIVILEGES ON *.* TO '$MYSQL_USER'@'%' WITH GRANT OPTION"
mysql -uroot -e "CREATE DATABASE IF NOT EXISTS sshop CHARACTER SET utf8"

echo "=> Done!"

echo "========================================================================"
echo "You can now connect to this MySQL Server using:"
echo ""
echo "    mysql -u$MYSQL_USER -p$MYSQL_PASS -h<host> -P<port>"
echo ""
echo "Please remember to change the above password as soon as possible!"
echo "MySQL user 'root' has no password but only allows local connections"
echo "========================================================================"

sed -i "s/INIT_DB_USER/$MYSQL_USER/g" /app/www/settings.py
sed -i "s/INIT_DB_PASS/$MYSQL_PASS/g" /app/www/settings.py
