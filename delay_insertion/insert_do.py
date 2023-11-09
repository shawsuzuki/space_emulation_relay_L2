import json
import time
import subprocess

def exec_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

def apply_delay(sender, delay, rate):
    # Egress遅延の適用
    exec_command(f"docker exec {sender} tc qdisc add dev eth0 root netem delay {delay}ms rate {rate}kbps")
    
    # Ingress遅延の設定
    # IFBデバイスの起動と設定
    exec_command(f"docker exec {sender} tc qdisc add dev eth0 handle ffff: ingress")
    exec_command(f"docker exec {sender} tc filter add dev eth0 parent ffff: protocol ip u32 match u32 0 0 action mirred egress redirect dev ifb0")
    exec_command(f"docker exec {sender} tc qdisc add dev ifb0 root netem delay {delay}ms rate {rate}kbps")

def remove_delay(sender):
    exec_command(f"docker exec {sender} tc qdisc del dev eth0 root")
    exec_command(f"docker exec {sender} tc qdisc del dev eth0 handle ffff: ingress")
    exec_command(f"docker exec {sender} tc qdisc del dev ifb0 root")

def main():
    with open("./contactgraph/contact-revised.json", "r") as f:
        data = json.load(f)

    for entry in data:
        sender = entry["Sender"]
        from_time = int(entry["From"])
        until_time = int(entry["Until"])
        delay = entry["delay"]
        rate = entry["Rate"]

        # 遅延の適用
        time.sleep(from_time)
        apply_delay(sender, delay, rate)
        time.sleep(until_time - from_time)

        # 遅延の削除
        remove_delay(sender)

if __name__ == "__main__":
    main()
