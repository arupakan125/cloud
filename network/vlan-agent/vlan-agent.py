import json
import subprocess
import re
import requests

API_URL = "http://10.0.1.182:8080/vlan"
OVERLAY_INTERFACE = "ens19"
BRIDGE_PREFIX = "acbr-"

command = "sudo ip link set up " + OVERLAY_INTERFACE
subprocess.run(command, shell=True)

ideal_vlan_interfaces = requests.get(API_URL).json()
ideal_vlan_interfaces_list =[]

for vlan_interface in ideal_vlan_interfaces:
     ideal_vlan_interfaces_list.append(str(vlan_interface["vlan"]) + "-" + str(vlan_interface["switch"]))

print(ideal_vlan_interfaces_list)

actual_vlan_interfaces = subprocess.check_output('sudo ip link', shell=True, encoding='utf-8')
actual_vlan_interfaces = re.findall(OVERLAY_INTERFACE + "\.\d+-\d+" , actual_vlan_interfaces)

actual_vlan_interface_list = []
for vlan_interface in actual_vlan_interfaces:
    vlan_interface = vlan_interface.replace(OVERLAY_INTERFACE + ".", "")
    actual_vlan_interface_list.append(vlan_interface)

print(actual_vlan_interface_list)

needed_vlan_interface_list = list(set(ideal_vlan_interfaces_list) - set(actual_vlan_interface_list))
needed_vlan_interface_list.sort()
print("VLANインタフェースの作成が必要")
print(needed_vlan_interface_list)

unneeded_vlan_interface_list = list(set(actual_vlan_interface_list) - set(ideal_vlan_interfaces_list))
unneeded_vlan_interface_list.sort()
print("VLANインタフェースの破棄が必要")
print(unneeded_vlan_interface_list)


for vlan_interface in unneeded_vlan_interface_list:
    name = OVERLAY_INTERFACE + "." + vlan_interface
    command = "sudo ip link del " + name
    subprocess.run(command, shell=True)
    print("VLAN Interface(" + name + " )is deleted")

for vlan_interface in needed_vlan_interface_list:
    name = OVERLAY_INTERFACE + "." + vlan_interface
    vlan_id = vlan_interface.split("-")[0]
    switch_id = vlan_interface.split("-")[1]
    bridge_name = BRIDGE_PREFIX + switch_id
    command = "ip link add link " + OVERLAY_INTERFACE + " name " + name + " type vlan id " + vlan_id
    subprocess.Popen(command, shell=True)
    command = "sudo ip link set up " + name
    subprocess.run(command, shell=True)
    command = " sudo brctl addif " + bridge_name + " " + name
    subprocess.Popen(command, shell=True)
    print("VLAN Interface(" + name + ") is created")