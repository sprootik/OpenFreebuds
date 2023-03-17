import logging

from openfreebuds.device.huawei.generic.spp_handler import HuaweiSppHandler
from openfreebuds.device.huawei.generic.spp_package import HuaweiSppPackage

log = logging.getLogger("HuaweiHandlers")


class SimpleAncHandler(HuaweiSppHandler):
    """
    Simple ANC mode switching handler.

    For devices which don't have noise cancellation level option,
    provides only mode switching (off/anc/aware)
    """

    handle_props = [
        ('anc', 'mode'),
    ]
    handle_commands = [b"\x2b\x2a"]
    ignore_commands = [b"\x2b\x04"]

    def on_init(self):
        self.device.send_package(HuaweiSppPackage(b"\x2b\x2a", [
            (1, b""),
        ]), True)

    def on_package(self, pkg: HuaweiSppPackage):
        data = pkg.find_param(1)
        if len(data) == 2:
            self.device.put_property("anc", "mode", data[1])

    def on_prop_changed(self, group: str, prop: str, value):
        self.device.send_package(HuaweiSppPackage(b"\x2b\x04", [
            (1, value),
        ]))
