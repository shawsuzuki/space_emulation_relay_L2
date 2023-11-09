import json

def determine_delay(sender, recvr):
    # SenderとRecvrの2個目のアンダーバーまでの値を取得
    sender_prefix = "_".join(sender.split("_")[:2])
    recvr_prefix = "_".join(recvr.split("_")[:2])
    
    # 指定された条件に基づいてdelayを決定
    if (sender_prefix, recvr_prefix) in [("earth_surface", "earth_orbit"), ("earth_orbit", "earth_surface")]:
        return 500
    elif (sender_prefix, recvr_prefix) in [("moon_surface", "moon_orbit"), ("moon_orbit", "moon_surface")]:
        return 300
    elif (sender_prefix, recvr_prefix) in [("earth_orbit", "moon_orbit"), ("moon_orbit", "earth_orbit")]:
        return 2600
    else:
        return None

def update_json_with_delay(json_data):
    for section in json_data:
        delay_value = determine_delay(section["Sender"], section["Recvr"])
        if delay_value:
            section["delay"] = delay_value
    return json_data

if __name__ == "__main__":
    with open("./input/contact-graph.json", "r") as file:
        data = json.load(file)
    
    updated_data = update_json_with_delay(data)
    
    with open("./contactgraph/contact-revised.json", "w") as file:
        json.dump(updated_data, file, indent=4)