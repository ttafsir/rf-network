# -*- coding: utf-8 -*-
from typing import Any, Dict, Optional

from netmiko import ConnectHandler

from rf_network.hookspecs import hookimpl

CONNECTION_PLUGIN = "netmiko"
DRIVERS = {
    "ios": "cisco_ios",
    "nxos": "cisco_nxos",
    "nxos_ssh": "cisco_nxos",
    "eos": "arista_eos",
    "junos": "juniper_junos",
    "iosxr": "cisco_xr",
}


@hookimpl
def connect_to(
    connection: str,
    host: Optional[str],
    username: Optional[str],
    password: Optional[str],
    platform: Optional[str],
    port: Optional[int] = 22,
    **options: Optional[Dict[str, Any]],
) -> None:
    if connection != CONNECTION_PLUGIN:
        return

    parameters = {
        "host": host,
        "username": username,
        "password": password,
        "port": port,
    }

    if platform is not None:
        platform = DRIVERS.get(platform, platform)
        parameters["device_type"] = platform

    options = options or {}
    parameters.update(options)
    return ConnectHandler(**parameters)


@hookimpl
def send_command(
    command: str,
    conn: Any,
    plugin: str,
    **options: Optional[Dict[str, Any]],
):
    if plugin == CONNECTION_PLUGIN:
        return conn.send_command(command, **options)


@hookimpl
def send_command_and_parse(
    command,
    conn,
    plugin,
    parser: str = "genie",
    **options: Optional[Dict[str, Any]],
):
    if plugin == CONNECTION_PLUGIN:
        if parser == "genie":
            return conn.send_command(command, use_genie=True, **options)
        elif parser == "textfsm":
            return conn.send_command(command, use_textfsm=True, **options)
        return
