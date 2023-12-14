import logging, re
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get, napalm_configure
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_configs


def scp_archive(task):
    task.run(task=send_configs, configs=["ip scp server enable", "archive", "path flash:archive", "wr"])

def replace_ospf(task):
    data = task.run(
        task=load_yaml,
        file=f"host_vars/{task.host}.yml",
        severity_level=logging.DEBUG,
    )

    #load host yml data into task.host["facts"]
    task.host["facts"] = data.result
    config = task.run(task=napalm_get, getters=["config"], severity_level=logging.DEBUG)
    showrun = config.result["config"]["running"]
    pattern = re.compile("^router ospf([^!]+)", flags=re.I | re.M)

    ospf_template = task.run(
        task=template_file,
        name="Creating OSPF Configuration",
        template="ospf.j2",
        path="templates",
        severity_level=logging.DEBUG
    )

    load_template = ospf_template.result
    newconfig = re.sub(pattern, load_template, showrun)
    print(newconfig)
    newconfig = newconfig.replace("^C", chr(3))

    return newconfig


def replace_feature(task):
    config = replace_ospf(task)
    task.run(task=napalm_configure, configuration=config, replace=True)

nr = InitNornir(config_file="config.yml")


filtered = nr.filter(F(location="site2-dist") | F(location="site3-dist"))

scp_results = filtered.run(task=scp_archive)

results = filtered.run(task=replace_feature)
print_result(results)