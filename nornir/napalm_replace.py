from pathlib import Path
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_configure
from rich import print as rprint


def scp_archive(task):
    task.run(task=send_configs, configs=["ip scp server enable", "archive", "path flash:archive", "wr"])


def replace_config(task):
    task.run(task=napalm_configure, filename=f"backup_configs/{date}/{config}/{task.host}.txt", replace=True)

config_exit = False
date_exit = False

nr = InitNornir(config_file="config.yml")

while not date_exit:
    date = input("Which date to use for configuration restore: (YYYY-MM-DD): ")
    p = Path(f"backup_configs/{date}")
    if p.exists():
        date_exit = True
    else:
        rprint("[red]***Backup date does not exist or wrong date format used***")


while not config_exit:
    config = input("Which config to use for restore: <running/startup> ")
    if config == "running" or config == "startup":
        config_exit = True
    else:
        rprint("[red]Please enter either running or startup[/red]")

scp_results = nr.run(task=scp_archive)
replace_results = nr.run(task=replace_config)

print_result(replace_results)
