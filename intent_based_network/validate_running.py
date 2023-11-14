import logging, os, subprocess
from rich import print as rprint
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F

def validate_running(task):
    data = task.run(
        task=load_yaml,
        file=f"host_vars/{task.host}.yml",
        severity_level=logging.DEBUG,
    )
        
    #load host yml data into task.host["facts"]
    task.host["facts"] = data.result

    #load jinja2 template and run napalm_configure replace
    template = task.run(task=template_file, template=f"{task.host}.j2", path="templates")
    task.host["base_config"] = template.result
    config = task.host["base_config"]
    task.run(task=napalm_configure, configuration=config, replace=True)


nr = InitNornir(config_file="config.yml")
CLEAR = "clear"
CLEAN = "rm -r configs-diff current-config"

#Use pyats to check diff of golden-config and current-config
CURRENT = "pyats learn config --testbed-file testbed.yml --output current-config"
os.system(CURRENT)
command = str(subprocess.run(["pyats", "diff", "golden-config", "current-config", "--output", "configs-diff"], stdout=subprocess.PIPE))

if "Diff can be found" in command:
    os.system(CLEAR)
    rprint("[red]***CURRENT CONFIG DIFFERENT FROM GOLDEN CONFIG***[/red]")
    revert = input("Revert current configuration to golden configuration? <y/n>: ")
    if revert == "y":
        os.system(CLEAN)
        os.system(CLEAR)
        filtered = nr.filter(F(location="site2-dist") | F(location="site3-dist"))
        results = filtered.run(task=validate_running)
        print_result(results)
else:
    os.system(CLEAN)
    os.system(CLEAR)
    rprint("[green]***NO DIFFERENCES DETECTED***[/green]")


