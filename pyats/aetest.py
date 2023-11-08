from pyats import aetest
from genie.conf import Genie

class DeviceTest(aetest.Testcase):
    @aetest.setup
    def setup(self):
        self.parameters["testbed"].connect(log_stdout=True)

    @aetest.test
    def show_version(self):
        for device in self.parameters["testbed"].devices.values():
            show_ver = device.parse("show version")
            assert show_ver["version"]["version_short"] == "15.1"

    @aetest.cleanup
    def cleanup(self):
        self.parameters["testbed"].disconnect()

topology = Genie.init("testbed.yml")
aetest.main(testbed=topology)