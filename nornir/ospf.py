import requests, ipaddress
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_command
from collections import defaultdict
from rich import print as rprint

requests.packages.urllib3.disable_warnings()

def rest_ospf(task):
    if task.host["restconf"] == True and str(task.host) != "dc-core1" and task.host["ospf"] == True:
        ospf_url = f"https://{task.host.hostname}:443/restconf/data/ospf-oper-data"
        ospf_response = requests.get(url=ospf_url, headers=headers, auth=(f"{task.host.username}", f"{task.host.password}"), verify=False)  
        task.host["ospfrest-data"] = ospf_response.json()

        ospf_data = task.host["ospfrest-data"]["Cisco-IOS-XE-ospf-oper:ospf-oper-data"]["ospf-state"]["ospf-instance"]
        for inst in ospf_data:
            areas = inst["ospf-area"]
            for area in areas:
                try:
                    area_id = area["area-id"]
                    ospf_intfs = area["ospf-interface"]
                    for ospf_intf in ospf_intfs:
                        name = ospf_intf["name"]
                        dead_timer = ospf_intf["dead-interval"]
                        hello_timer = ospf_intf["hello-interval"]
                        auth = ospf_intf["authentication"]
                        ospf_dict[f"{task.host}"][name] = [area_id, dead_timer, hello_timer, auth]
                        print(f"{task.host} Name: {name} Dead Timer: {dead_timer} Hello Timer: {hello_timer} Auth: {auth}")
                except KeyError:
                    pass
                

        intf_url = f"https://{task.host.hostname}:443/restconf/data/native/interface"
        intf_response = requests.get(url=intf_url, headers=headers, auth=(f"{task.host.username}", f"{task.host.password}"), verify=False)
        task.host["intfrest-data"] = intf_response.json()

        ospf_interfaces = task.host["intfrest-data"]["Cisco-IOS-XE-native:interface"]
        for intf_type in ospf_interfaces:
            interfaces = ospf_interfaces[intf_type]
            for intf in interfaces:
                try:
                    name = intf["name"]
                    ip = intf["ip"]["address"]["primary"]["address"]
                    mask = intf["ip"]["address"]["primary"]["mask"]
                    intf_dict[f"{task.host}"][intf_type+name] = [ip, mask]
                    #print(f"{task.host} {intf_type}{name} - {ip}/{mask}")
                except KeyError:
                    pass
    
    elif task.host["restconf"] is not True and task.host["ospf"] == True:
        ospf_result = task.run(task=send_command, command="show ip ospf neighbor")
        #print(ospf_result.result)
        #print(ospf_result.scrapli_response.genie_parse_output())
        task.host["ospf-data"] = ospf_result.scrapli_response.genie_parse_output()
        print(task.host["ospf-data"])



def get_cdp(task):
    
    url = f"https://{task.host.hostname}:443/restconf/data/cdp-neighbor-details"
    response = requests.get(url=url, headers=headers, auth=(f"{task.host.username}", f"{task.host.password}"), verify=False)
    task.host["cdp-facts"] = response.json()

    cdp_neighbors = task.host["cdp-facts"]["Cisco-IOS-XE-cdp-oper:cdp-neighbor-details"]["cdp-neighbor-detail"]
    for neighbor in cdp_neighbors:
        name = neighbor["device-name"]
        local_intf = neighbor["local-intf-name"]
        port_id = neighbor["port-id"]
        if local_intf.startswith("Gi"):
            try:
                local_ip = intf_dict[f"{task.host}"][local_intf][0]
                local_mask = intf_dict[f"{task.host}"][local_intf][1]
                rprint(f"{task.host} {local_intf} has IP {local_ip}/{local_mask}")
            except KeyError:
                pass

ospf_dict = defaultdict(dict)
intf_dict = defaultdict(dict)

headers = {'Accept': 'application/yang-data+json'}

nr = InitNornir(config_file="config.yml")

ospf_results = nr.run(task=rest_ospf)

nr = InitNornir(config_file="config.yml")
target = nr.filter(restconf=True, ospf=True)
cdp_results = target.run(task=get_cdp)


#print_result(cdp_results)

#rprint(ospf_dict)
#rprint(intf_dict)
#print_result(results)

import ipdb
#ipdb.set_trace()