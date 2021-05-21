import json
import subprocess
import re
import requests

API_URL = "http://10.0.1.182:8080/json"
BRIDGE_PREFIX = "acbr-"

ideal_switchs = requests.get(API_URL).json()

ideal_switch_list = []
for switch in ideal_switchs:
    ideal_switch_list.append(switch["id"])

actual_switchs = subprocess.check_output('sudo brctl show', shell=True, encoding='utf-8')
actual_switchs = re.findall(BRIDGE_PREFIX + "\d+", actual_switchs)

actual_switch_list = []
for switch in actual_switchs:
    switch = switch.replace("acbr-", "")
    actual_switch_list.append(int(switch))



needed_switch_list = list(set(ideal_switch_list) - set(actual_switch_list))
needed_switch_list.sort()
print("ブリッジの作成が必要なセグメントID")
print(needed_switch_list)

unneeded_switch_list = list(set(actual_switch_list) - set(ideal_switch_list))
unneeded_switch_list.sort()
print("ブリッジの破棄が可能なセグメントID")
print(unneeded_switch_list)


for switch in needed_switch_list:
    name =  BRIDGE_PREFIX + str(switch)
    command = "sudo brctl addbr " + name
    subprocess.run(command, shell=True)
    print("Bridge(" + name+ ") is created")

for switch in unneeded_switch_list:
    name =  BRIDGE_PREFIX + str(switch)
    command = "sudo brctl delbr " + name
    subprocess.run(command, shell=True)
    print("Bridge(" + name+ ") is deleted")