import json
from rich import print as rprint
from genie.testbed import load
from genie.utils import Dq
from pyats.async_ import pcall

def ospf_intf(testbed_value):
    #Check OSPF hello and dead timers
    if testbed_value.hostname not in ["dc-core1", "site1-core1", "site1-dist1", "site1-dist2"]:
        ospf = testbed_value.parse("show ip ospf interface")
        hello_timer = (Dq(ospf).contains("hello_interval").get_values("hello_interval"))
        dead_timer = (Dq(ospf).contains("dead_interval").get_values("dead_interval"))
        rprint(f"{testbed_value.hostname} hello timer: {hello_timer}")
        rprint(f"{testbed_value.hostname} dead timer: {dead_timer}")

        return ospf


testbed = load("testbed.yml")
testbed.connect(log_stdout=False)
results = pcall(ospf_intf, testbed_value=testbed.devices.values())

import ipdb
#ipdb.set_trace()