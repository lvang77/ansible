from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from tqdm import tqdm
from rich import print as rprint

def find_mac(task, progress_bar):
    int_result = task.run(task=send_command, command="show interfaces")
    task.host["facts"] = int_result.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]

    for interface in interfaces:
        try:
            mac_addr = interfaces[interface]["mac_address"]
            if mac == mac_addr:
                found_list.append(mac_addr)
                rprint("[green]*** SEARCH SUCCESSFUL ***[/green]")
                print(f"MAC ADDRESS: {mac} found at {task.host}'s {interface} interface")
        except KeyError:
            pass

    progress_bar.update()

found_list = []

nr = InitNornir(config_file="config.yml")

mac = input("MAC Address to find: ")

targets = nr.filter(platform="ios")

with tqdm(total=len(targets.inventory.hosts)) as progress_bar:
    results = targets.run(task=find_mac, progress_bar=progress_bar)

if mac not in found_list:
    rprint(f"[red]MAC ADDRESS: {mac} NOT FOUND[/red]")

#import ipdb
#ipdb.set_trace()