#!/bin/bash

modprobe ifb
ip link set dev ifb0 up
python3 ./delay_insertion/insert_do.py
