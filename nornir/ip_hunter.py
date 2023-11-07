import threading
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from tqdm import tqdm
from rich import print as rprint
from collections import Counter
from ipaddress import ip_address

def find_ip(task, progress_bar):
    results = task.run(task=send_command, command="show ip interface brief")
    task.host["facts"] = results.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]["interface"]

    for interface in interfaces:
        try:
            ip_add = interfaces[interface]["ip_address"]
            
            if ip_add != "unassigned":
                ip_list.append(ip_add)

            if str(ip) == ip_add:
                found_list.append(ip_add)
                LOCK.acquire()
                rprint("[green]*** SEARCH SUCCESSFUL ***[/green]")
                print(f"IP ADDRESS: {ip} found at {task.host}'s {interface} interface")
                LOCK.release()
        except:
            pass
    
    progress_bar.update()

def find_dup(task):
    results = task.run(task=send_command, command="show ip interface brief")
    task.host["facts"] = results.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]["interface"]

    for ip_add in duplicates:
        for interface in interfaces:
            try:
                int_ip = interfaces[interface]["ip_address"]

                if ip_add == int_ip:
                    found_list.append(ip_add)
                    LOCK.acquire()
                    rprint("[red]\n*** DUPLICATE IP SEARCH SUCCESSFUL ***[/red]")
                    print(f"IP ADDRESS: {ip_add} found at {task.host}({task.host.hostname}) {interface} interface")
                    LOCK.release()
            except:
                pass

filtered = False
filter_exit = False
filter_type_exit = False
found_list = []
ip_list = []
LOCK = threading.Lock()

nr = InitNornir(config_file="config.yml")

ip = input("IP Address to find: ")
ip = ip_address(ip)

while filter_exit == False:
    filter = input("Would you like to apply a location filter to this script? <y/n? ")
    if filter == "y":
        filter_exit = True
        filtered = True
        location = input("Select A Location to Target: ")
        while filter_type_exit == False:
            filter_type = input("Include or exclude this location? <include/exclude> ")
            if filter_type == "include":
                filter_type_exit = True
                targets = nr.filter(F(location=location))
            elif filter_type == "exclude":
                filter_type_exit = True
                targets = nr.filter(F(location=location))
    elif filter == "n":
        filter_exit = True

if filtered:
    with tqdm(total=len(targets.inventory.hosts)) as progress_bar:
        results = targets.run(task=find_ip, progress_bar=progress_bar)
else:
    with tqdm(total=len(nr.inventory.hosts)) as progress_bar:
        results = nr.run(task=find_ip, progress_bar=progress_bar)

if str(ip) not in found_list:
    rprint(f"[red]IP ADDRESS: {ip} NOT FOUND[/red]")

duplicates = [k for k, v in Counter(ip_list).items() if v > 1]

if duplicates:
    rprint(f"\n[red]*** DUPLICATE IP ADDRESSES FOUND ***\n{duplicates} [/red]")
    if filtered:
        dup_results = targets.run(task=find_dup)
    else:
        dup_results = nr.run(task=find_dup)
else:
    rprint("[green]No Duplicate IP Addresses Found[/green]")

#import ipdb
#ipdb.set_trace()