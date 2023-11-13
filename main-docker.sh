#以前のコンテナ、イメージ、ボリューム、ネットワーク全て削除
docker rm -f `docker ps -a -q`
docker rmi `docker images -q`
docker volume rm `docker volume ls -q`
docker network rm `docker network ls -q`

#python3 container-maker.py
docker compose build --no-cache 
docker compose up -d 
docker images
docker ps