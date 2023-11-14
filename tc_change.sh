#!/bin/bash

# コンテナのネットワークインターフェース名をホスト側で特定
# 例: コンテナIDを使用して仮想インターフェース名を取得
CONTAINER_ID=$(docker ps | grep moon_orbit_1 | awk '{print $1}')
INTERFACE_NAME=$(docker exec $CONTAINER_ID ifconfig | grep -o "eth0")

# 初期遅延 (ミリ秒)
DELAY=200

# 遅延増減のフラグ（1で増加、-1で減少）
INCREMENT=1

docker exec moon_orbit_1 tc qdisc add dev $INTERFACE_NAME root netem delay ${DELAY}ms

# 繰り返しで遅延を変更
while true; do
    sleep 1
    DELAY=$(($DELAY + $INCREMENT * 100))

    # 遅延をtcコマンドで設定
    docker exec $CONTAINER_ID tc qdisc change dev $INTERFACE_NAME root netem delay ${DELAY}ms

    # 遅延が2600msに達した場合
    if [ "$DELAY" -ge 2600 ]; then
        # パケットロスを100%に設定
        docker exec $CONTAINER_ID tc qdisc change dev $INTERFACE_NAME root netem loss 100%
        sleep 20

        # 遅延を2600msに戻し、パケットロスを0%に設定
        docker exec $CONTAINER_ID tc qdisc change dev $INTERFACE_NAME root netem delay ${DELAY}ms loss 0%
        INCREMENT=-1
    elif [ "$DELAY" -le 200 ]; then
        INCREMENT=1
    fi
done

# スクリプトが終了する際（通常はしないが）、遅延設定を削除
docker exec $CONTAINER_ID tc qdisc del dev $INTERFACE_NAME root
