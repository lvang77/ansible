import threading
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint
from ipaddress import ip_address, ip_network


def ping_test(task):
    for ip in ip_addrs:
        result = task.run(task=send_command, command="ping " + ip)
        response = result.result
        if not "!!!" in response:
            rprint(f"[red]{task.host} failed to ping {ip}[/red]")
            fail_list.append(f"{task.host} can't ping {ip}")
        else:
            rprint(f"[green]{task.host} successful ping to {ip}[/green]")

def get_loop(task):
    result = task.run(task=send_command, command="show ip interface brief")
    task.host["facts"] = result.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]["interface"]
    for intf in interfaces:
        if intf.startswith("Loop") and interfaces[intf]["ip_address"] != "unassigned":
            ip_addrs.append(interfaces[intf]["ip_address"])


LOCK = threading.Lock()
fail_list = []
ip_addrs = []
ip_test_exit = False

nr = InitNornir(config_file="config.yml")
targets = nr.filter(location="site1-dist")

while not ip_test_exit:
    ip_test = input("Loopback or text file ping: <loopback/file> ")
    if ip_test == "loopback":
        ip_test_exit = True
        results = targets.run(task=get_loop)
    elif ip_test == "file":
        ip_test_exit = True
        with open('ping.txt', 'r') as f:
            ip_addrs = f.read().splitlines()


results = targets.run(task=ping_test)

if fail_list:
    sort = sorted(fail_list)
    rprint(sort)
else:
    rprint("[green]*** All pings successful ***[/green]")

