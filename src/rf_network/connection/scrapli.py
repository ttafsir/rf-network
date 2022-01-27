# -*- coding: utf-8 -*-
import json
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
    options: Optional[Dict[str, Any]] = None,
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
def send_command_to(
    command,
    conn,
    conn_name,
    options,
):
    if conn_name == CONNECTION_PLUGIN:
        response = conn.send_command(command)
        if options.get("genie_parse"):
            parsed_resp = response.genie_parse_output()
            parsed_resp_pretty = json.dumps(parsed_resp, sort_keys=True, indent=4)
            return response.result, parsed_resp_pretty
        return response.result
