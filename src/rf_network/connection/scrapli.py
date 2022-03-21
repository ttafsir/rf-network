# -*- coding: utf-8 -*-
from typing import Any, Dict, Optional

from scrapli import Scrapli

from rf_network.hookspecs import hookimpl

CONNECTION_PLUGIN = "scrapli"


@hookimpl
def connect_to(
    connection: str,
    host: Optional[str],
    username: Optional[str],
    password: Optional[str],
    platform: Optional[str],
    port: Optional[int] = 22,
    **options: Optional[Dict[str, Any]],
) -> Scrapli:

    if connection != CONNECTION_PLUGIN:
        return

    device = {
        "host": host,
        "auth_username": username,
        "auth_password": password,
        "auth_strict_key": False,
        "platform": platform,
    }
    ssh = Scrapli(**device)
    ssh.open()
    return ssh


@hookimpl
def send_command(
    command,
    conn,
    plugin,
    **options: Optional[Dict[str, Any]],
):
    if plugin == CONNECTION_PLUGIN:
        response = conn.send_command(command, **options)
        return response.result


@hookimpl
def send_command_and_parse(
    command,
    conn,
    plugin,
    parser: str = "genie",
    **options: Optional[Dict[str, Any]],
):
    if plugin == CONNECTION_PLUGIN:
        response = conn.send_command(command)
        if parser == "genie":
            return response.genie_parse_output()
        elif parser == "textfsm":
            return response.textfsm_parse_output()
        return response.result
