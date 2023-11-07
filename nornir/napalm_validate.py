import yaml, logging
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get, napalm_validate
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result
import pathlib

def save_intf_ip(intf_ip, filename):
    with open(filename, "w") as f:
        output = yaml.dump(intf_ip.result, f, default_flow_style=False)
    
    with open(filename, "r+") as f:
        content = f.readlines()
        for n, line in enumerate(content):
            if n != 0:
                content[n] = "  " + content[n]
        content[0] = "- " + content[0]
    
    with open(filename, "r+") as f:
        f.writelines(content)
    
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write("---\n" + "\n" + content)


def check_intf_ip(task):
    intf_ip = task.run(task=napalm_get, getters=["get_interfaces_ip"])

    pathlib.Path("validate").mkdir(exist_ok=True)
    pathlib.Path("validate/intf_ip").mkdir(exist_ok=True)
    filename = f"validate/intf_ip/{task.host}_intf_ip.yml"
    if not pathlib.Path(filename).is_file():
        save_intf_ip(intf_ip=intf_ip, filename=filename)
    else:
        result = task.run(task=napalm_validate, src=filename, severity_level=logging.DEBUG)
        task.host["facts"] = result.result
        complies = task.host["facts"]["complies"]
        if complies:
            msg = "COMPLIES"
        else:
            msg = task.host["facts"]
        return Result(host=task.host, result=msg)
    

nr = InitNornir(config_file="config.yml")

results = nr.run(task=check_intf_ip)

print_result(results)