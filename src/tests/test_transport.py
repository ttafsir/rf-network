import pytest

from rf_network.library import NetworkTransportLibrary


@pytest.fixture()
def test_switch():
    return {
        "host": "10.255.70.243",
        "username": "cisco",
        "password": "cisco",
        "platform": "ios",
        "alias": "sw1",
    }


@pytest.mark.parametrize(
    "plugin, platform", [("netmiko", "ios"), ("scrapli", "cisco_iosxe")]
)
def test_create_transport_connection(plugin, platform, test_switch):
    lib = NetworkTransportLibrary()
    test_switch.update({"platform": platform})
    lib.open_connection(**test_switch, connection_plugin=plugin)
    assert lib.get_connection(alias_or_index=test_switch["alias"])


@pytest.mark.parametrize(
    "plugin, platform", [("netmiko", "ios"), ("scrapli", "cisco_iosxe")]
)
def test_send_command(plugin, platform, test_switch):
    lib = NetworkTransportLibrary()
    test_switch.update({"platform": platform})
    lib.open_connection(**test_switch, connection_plugin=plugin)
    command = "show version"
    resp = lib.send_command(command=command, alias_or_index=test_switch["alias"])
    assert "Cisco IOS XE Software" in resp


@pytest.mark.parametrize(
    "plugin, platform", [("netmiko", "ios"), ("scrapli", "cisco_iosxe")]
)
def test_send_command_and_parse_w_genie(plugin, platform, test_switch):
    lib = NetworkTransportLibrary()
    test_switch.update({"platform": platform})
    lib.open_connection(**test_switch, connection_plugin=plugin)
    command = "show version"
    resp = lib.send_command_and_parse(
        command=command, alias_or_index=test_switch["alias"], parser="genie"
    )
    assert "IOS-XE" in resp[0]["version"]["os"]
