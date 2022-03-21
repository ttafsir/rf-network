# -*- coding: utf-8 -*-
from pluggy import HookimplMarker, HookspecMarker

hookspec = HookspecMarker("rf_network")
hookimpl = HookimplMarker("rf_network")


@hookspec(firstresult=True)
def connect_to(connection, host, username, password, platform, **options):
    """
    connect to device using SSH connection provider

    :param connection: name of connection plugin
    :type connection: str
    :param options: options to pass to connection plugin
    :type options: dict
    """


@hookspec(firstresult=True)
def send_command(command, conn, plugin, **options):
    """Send command via SSH connection"""


@hookspec
def send_command_and_parse(command, conn, plugin, parser, **options):
    """Send command via SSH connection and parse response"""
