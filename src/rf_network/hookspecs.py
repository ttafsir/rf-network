# -*- coding: utf-8 -*-
from pluggy import HookimplMarker, HookspecMarker

hookspec = HookspecMarker("rf_network")
hookimpl = HookimplMarker("rf_network")


@hookspec(firstresult=True)
def connect_to(connection, host, username, password, platform, options):
    """
    connect to device using SSH connection provider

    :param connection: name of connection plugin
    :type connection: str
    :param options: options to pass to connection plugin
    :type options: dict
    """


@hookspec(firstresult=True)
def send_command_to(command, conn, conn_name, extras):
    """Send command via SSH connection"""
