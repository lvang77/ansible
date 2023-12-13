from flask import Flask, render_template
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F

app = Flask(__name__)

@app.route("/")
def homepage():
    return "Hello World"

@app.route("/hosts/inventory")
def inventory():
    nr = InitNornir(config_file="config.yml")
    return render_template("inventory.html", hosts=nr.inventory.hosts.values())

@app.route("/all/running")
def run_config():
    nr = InitNornir(config_file="config.yml")
    results = nr.run(task=send_command, command="show run")
    run_list = [v.scrapli_response.result for v in results.values()]
    return render_template("running.html", run_list=run_list)

@app.route("/all/version")
def version():
    nr = InitNornir(config_file="config.yml")
    results = nr.run(task=send_command, command="show version")
    ver_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
    return render_template("version.html", ver_list=ver_list)

@app.route("/hosts/<hostname>/version")
def host_version(hostname):
    nr = InitNornir(config_file="config.yml")
    filtered = nr.filter(F(hostname=hostname))
    results = filtered.run(task=send_command, command="show version")
    ver_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
    return render_template("version.html", ver_list=ver_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)