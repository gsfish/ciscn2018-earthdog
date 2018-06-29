FROM python:3.6

ENV DEBIAN_FRONTEND noninteractive

RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && \
    apt-get install -y nginx mysql-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./www /app

ADD requirement.pip ./
ADD mysql_init.sh ./
ADD nginx.conf /etc/nginx/sites-enabled/sshop

RUN pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install -r ./requirement.pip -i https://pypi.tuna.tsinghua.edu.cn/simple

ENV MYSQL_USER=admin MYSQL_PASS=22852abbb81f8f9f61ad2a5706f824f5

RUN ./mysql_init.sh && \
    python3 manage.py makemigrations sshop && \
    python3 manage.py migrate && \
    python3 set_database.py 100 && \
    python3 set_admin.py && \
    python3 manage.py dumpdata --format=json sshop > /app/sshop/static/backup.sql && \
    chown 777 -R /app/sshop/static && \
    python3 set_flag.py "CISCN{this_is_a_sample_flag}"

CMD find /var/lib/mysql/mysql -exec touch -c -a {} + && \
    service mysql start && \
    service nginx start && \
    gunicorn www.wsgi:application -c gunicorn.conf.py
