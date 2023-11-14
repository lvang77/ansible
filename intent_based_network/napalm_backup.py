import pathlib
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file
from datetime import date

def backup_configs(task):
    backup_dir = "backup_configs"
    date_dir = backup_dir + "/" + str(date.today())
    running_dir = date_dir + "/" + "running"
    startup_dir = date_dir + "/" + "startup"

    pathlib.Path(backup_dir).mkdir(exist_ok=True)
    pathlib.Path(date_dir).mkdir(exist_ok=True)
    pathlib.Path(running_dir).mkdir(exist_ok=True)
    pathlib.Path(startup_dir).mkdir(exist_ok=True)

    result = task.run(task=napalm_get, getters=["config"])

    running_config = result.result["config"]["running"]
    running_config = running_config.replace("^C", chr(3))
    task.run(task=write_file, content=running_config, filename=f"{running_dir}/{task.host}.txt")

    startup_config = result.result["config"]["startup"]
    startup_config = startup_config.replace("^C", chr(3))
    task.run(task=write_file, content=startup_config, filename=f"{startup_dir}/{task.host}.txt")


nr = InitNornir(config_file="config.yml")

results = nr.run(task=backup_configs)
#print_result(results)