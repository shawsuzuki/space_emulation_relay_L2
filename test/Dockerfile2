FROM ubuntu:20.04
#なんのイメージを使って作るかを指定

#RUNはコマンドを実行したいとき
EXPOSE 22 5963 5001
#EXPOSEはポート開く
#RUN ip a
#RUN which iperf3

RUN apt update
#RUN apt install build-essential -y
#RUN apt install wget -y
RUN apt-get install -y iputils-ping net-tools
RUN apt-get install -y iproute2 -y
RUN apt-get install -y iperf3
RUN apt-get install iptables -y

#RUN apt-get install tcpdump -y
#RUN chmod +s /sbin/tc

#RUN wget https://sourceforge.net/projects/ion-dtn/files/ion-open-source-4.1.2.tar.gz/download
#RUN tar xzvf download
#WORKDIR /ion-open-source-4.1.2
#RUN ./configure
#RUN make
#RUN make install
#RUN ldconfig