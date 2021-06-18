#基底作業系統
FROM ubuntu:20.04

#編碼為C.UTF-8避免中文亂碼
ENV LANG="C.UTF-8"
#安裝需要的內容
RUN apt-get update &&\
	apt-get install tor -y&&\
	apt-get install nano -y&&\
	apt-get install python3 -y&&\
	apt-get install python3-pip -y&&\
	apt-get install proxychains4  -y&&\
	apt-get install netcat  -y&&\
	echo "Done"

#把腳本啟動檔傳入
COPY ./init/init /
COPY ./etc/torrc /etc/tor/

#啟動觸發腳本
CMD bash init && bash

