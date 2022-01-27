from pluggy import PluginManager

from rf_network.library import NetworkTransportLibrary


class TestLibrary:
    def test_create_library(self):
        lib = NetworkTransportLibrary()
        assert isinstance(lib.pm, PluginManager)
