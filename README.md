
# space_emulater

現在shawが作成中です。

## ファイルの説明

emulation_configure.config：このファイルに衛星の種類と数、開始IPアドレスを入力します。
docker_maker.py：emulation_configure.configの内容に応じたdocker-compose.ymlファイルを生成します。
docker-compose.yml：自動で生成
dockerfile：もともとION動かすように作ったものを流用しているので、現在はION関係の部分などはコメントアウトさせています。

## 使い方

①  emulation_configure.configの、衛星数、開始IPアドレスを調整（現在は使えるアドレス空間はとりあえず172.20.0.0/16になっていますのでその内部でお願いします）
②　python3 docker_maker.py
③　docker compose build --no-cache
④　docker compose up -d

## 遅延の挿入