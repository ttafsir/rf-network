# -*- coding: utf-8 -*-
import json
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
    options: Optional[Dict[str, Any]] = None,
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
def send_command_to(
    command,
    conn,
    conn_name,
    options,
):
    if conn_name == CONNECTION_PLUGIN:
        if options.get("use_genie"):
            parsed_resp = conn.send_command(command, use_genie=True)
            parsed_resp_pretty = json.dumps(parsed_resp, sort_keys=True, indent=4)
            return parsed_resp, parsed_resp_pretty
        return conn.send_command(command)
