import json
import subprocess
import re


BRIDGE_PREFIX = "acbr-"
VXLAN_PREFIX = "acvxlan-"
OVERLAY_INTERFACE = "eth0"
MUTICAST_GROUP = "239.0.0.1"


## 実際に存在するブリッジのIDをリストで取得
actual_switchs = subprocess.check_output('sudo brctl show', shell=True, encoding='utf-8')
actual_switchs = re.findall(BRIDGE_PREFIX + "\d+", actual_switchs)

actual_switch_list = []
for switch in actual_switchs:
    switch = switch.replace(BRIDGE_PREFIX, "")
    actual_switch_list.append(int(switch))

## 実際に存在するVXLANのIDをリストで取得
actual_vxlans = subprocess.check_output('sudo ip link show', shell=True, encoding='utf-8')
actual_vxlans = re.findall(VXLAN_PREFIX + "\d+", actual_vxlans)

actual_vxlan_list = []
for vxlan in actual_vxlans:
    vxlan = vxlan.replace(VXLAN_PREFIX, "")
    actual_vxlan_list.append(int(vxlan))

## 作成処理が必要なVXLANをリストで取得
needed_vxlan_list = list(set(actual_switch_list) - set(actual_vxlan_list))
needed_vxlan_list.sort()
## 破棄が可能なVXLANをリストで取得
unneeded_vxlan_list = list(set(actual_vxlan_list) - set(actual_switch_list))
unneeded_vxlan_list.sort()
print("VXLANの作成が必要なセグメントID")
print(needed_vxlan_list)
print("VXLANの破棄が可能なセグメントID")
print(unneeded_vxlan_list)

for vxlan in needed_vxlan_list:
    vxlan_name =  VXLAN_PREFIX + str(vxlan)
    bridge_name = BRIDGE_PREFIX + str(vxlan)
    command = "sudo ip link add " + vxlan_name + " type vxlan id " + str(vxlan) + " group 239.0.0.1 dev " + OVERLAY_INTERFACE + " dstport 4789"
    subprocess.run(command, shell=True)
    command = "sudo ip link set up " + vxlan_name
    subprocess.run(command, shell=True)
    command = " sudo brctl addif " + bridge_name + " " + vxlan_name
    subprocess.run(command, shell=True)
    print("VXLAN(" + vxlan_name+ ") is created")

for vxlan in unneeded_vxlan_list:
    vxlan_name =  VXLAN_PREFIX + str(vxlan)
    command = "sudo ip link del " + vxlan_name
    subprocess.run(command, shell=True)
    print("VXLAN(" + vxlan_name+ ") is deleted")