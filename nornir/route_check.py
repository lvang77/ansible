import threading
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from tqdm import tqdm
from rich import print as rprint
from ipaddress import ip_address, ip_network


def get_routes(task, progress_bar):
    results = task.run(task=send_command, command="show ip route")
    task.host["facts"] = results.scrapli_response.genie_parse_output()
    prefixes = task.host["facts"]["vrf"]["default"]["address_family"]["ipv4"]["routes"]
    for prefix in prefixes:
        network = ip_network(prefix)
        if ip in network:
            LOCK.acquire()
            rprint(f"[green]*** {ip} has a route on {task.host}'s network: {network} ***[/green]")
            found_list.append(str(ip))
            source_proto = prefixes[prefix]["source_protocol"]
            if source_proto == "connected":
                try:
                    out_intf = prefixes[prefix]["next_hop"]["outgoing_interface"]
                    for intf in out_intf:
                        exit_intf = intf
                        rprint(f"[green]{task.host} is directly connected to {str(ip)} via interface {exit_intf}\n[/green]")
                except KeyError:
                    pass
            else:
                try:
                    next_hop_list = prefixes[prefix]["next_hop"]["next_hop_list"]
                    for index in next_hop_list:
                        next_hop = next_hop_list[index]["next_hop"]
                        rprint(f"[green]{task.host} has a route to {ip} via next hop {next_hop} through {source_proto}\n[/green]")
                except KeyError:
                    pass
            LOCK.release()


    progress_bar.update()

LOCK = threading.Lock()
found_list = []

nr = InitNornir(config_file="config.yml")

ip = input("Enter the IP Address to Check: ")
ip = ip_address(ip)

with tqdm(total=len(nr.inventory.hosts)) as progress_bar:
    results = nr.run(task=get_routes, progress_bar=progress_bar)

if str(ip) not in found_list:
    rprint(f"[red]*** {str(ip)} IP ADDRESS HAS NO ROUTE ***[/red]")

#import ipdb
#ipdb.set_trace()