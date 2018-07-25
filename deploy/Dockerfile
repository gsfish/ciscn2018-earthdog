FROM phusion/baseimage

RUN rm -f /etc/service/sshd/down
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config

ADD ./start_sshop.sh /etc/my_init.d/
RUN chmod u+x /etc/my_init.d/start_sshop.sh

RUN groupadd ciscn && \
	useradd -g ciscn ciscn -m && \
	password=$(openssl passwd -1 -salt 'abcdefg' '123456') && \
	sed -i 's/^ciscn:!/ciscn:'$password'/g' /etc/shadow

RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
	apt-get update && \
 	apt-get install python3 -y && \
 	apt-get install python3-pip -y && \
 	apt-get install mysql-server -y && \
 	apt-get install mysql-client -y && \
 	apt-get install libmysqlclient-dev -y && \
 	apt-get install nginx -y && \
	rm -rf /var/lib/apt/lists/*

ADD nginx.conf /etc/nginx/sites-enabled/sshop
ADD requirement.pip /

RUN pip3 install -r /requirement.pip -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /home/ciscn

COPY ./www .

RUN chown -R ciscn:ciscn . && \
	chmod -R 755 .
