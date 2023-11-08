import json, logging
from pyats import aetest
from pyats.log.utils import banner
from genie.conf import Genie
from genie.abstract import Lookup
from genie.libs import ops
from tabulate import tabulate

log = logging.getLogger(__name__)

# ---------------
# AE Test Setup
# ---------------

class common_setup(aetest.CommonSetup):
    #Connect to devices
    @aetest.subsection
    def connect_devices(self, testbed):
        genie_testbed = Genie.init(testbed)
        self.parent.parameters["testbed"] = genie_testbed
        device_list = []
        for device in genie_testbed.devices.values():
            log.info(banner(f"Connecting to {device.name}"))
            try:
                device.connect(log_stdout=False)
            except Exception as e:
                self.failed(f"Failed to connect to {device.name}")
            
            device_list.append(device)
        #Pass list of successfully connected devices
        self.parent.parameters.update(dev=device_list)

class bgp_neighbors(aetest.Testcase):
    #Learn BGP info
    @aetest.test
    def learn_bgp(self):
        self.bgp_sessions = {}

        for device in self.parent.parameters["dev"]:
            log.info(banner(f"Learning BGP from {device.name}"))
            abstract = Lookup.from_device(device)
            bgp = abstract.ops.bgp.bgp.Bgp(device)
            bgp.learn()
            self.bgp_sessions[device.name] = bgp.info

    @aetest.test
    def check_bgp(self):
        #Check BGP neighbor established
        failed_list = {}
        devices_tabular = []

        for device, bgp in self.bgp_sessions.items():
            bgp_info = bgp["instance"]["default"]["vrf"]["default"]
            neighbors = bgp_info["neighbor"]
            for neigh, info in neighbors.items():
                state = info.get("session_state")
                if state:
                    tab = []
                    tab.append(device)
                    tab.append(neigh)
                    tab.append(state)
                    if state.lower() == "established":
                        tab.append("PASSED")
                    else:
                        failed_list[device] = {}
                        failed_list[device][neigh] = info
                        tab.append("FAILED")
                
                devices_tabular.append(tab)

        log.info(tabulate(devices_tabular, headers=["Device", "Peer", "State", "Pass/Fail"], tablefmt='orgtbl'))

        if failed_list:
            log.error(json.dumps(failed_list, indent=2))
            self.failed("FOUND BGP NEIGHBORS NOT CONNECTED")
        else:
            self.passed("ALL BGP NEIGHBORS CONNECTED")

class common_cleanup(aetest.CommonCleanup):
    #Disconnect from devices
    @aetest.subsection
    def clean(self):
        log.info(banner("Cleanup"))
        self.parent.parameters["testbed"].disconnect()

if __name__ == '__main__':
    aetest.main()