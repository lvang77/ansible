import pytest
from nornir_scrapli.tasks import send_command
from nornir.core.filter import F
from nornir import InitNornir

nr = InitNornir(config_file="config.yml")

def getospf(task):
    result = task.run(task=send_command, command="show ip ospf neighbor")
    task.host["ospf_neigh"] = result.scrapli_response.genie_parse_output()

def get_device_names():
    devices = nr.filter(F(location="site2-core") | F(location="site2-dist") | F(location="site3-core") | F(location="site3-dist")).inventory.hosts.keys()
    return devices

class Testospfneighbors:
    @pytest.fixture(scope="class", autouse=True)
    def setup_teardown(self, pytestnr):
        pytestnr_filtered = pytestnr.filter(F(location="site2-core") | F(location="site2-dist") | F(location="site3-core") | F(location="site3-dist"))
        pytestnr_filtered.run(task=getospf)
        yield
        for host in pytestnr_filtered.inventory.hosts.values():
            host.data.pop("ospf_neigh")

    @pytest.mark.parametrize(
        "device_name", get_device_names()
    )

    def test_ospf_neighbor_count(self, pytestnr, device_name):
        neigh_list = []
        nr_host = pytestnr.inventory.hosts[device_name]

        interfaces = nr_host["ospf_neigh"]["interfaces"]
        for interface in interfaces:
            ospf_neigh = interfaces[interface]["neighbors"]
            for n in ospf_neigh:
                neigh_list.append(n)
        num_neigh = len(neigh_list)
        assert num_neigh == 2


