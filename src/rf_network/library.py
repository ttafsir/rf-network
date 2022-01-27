# -*- coding: utf-8 -*-
from robot.api.deco import library
from robot.utils.connectioncache import ConnectionCache

from .plugins import plugin_manager as pm
from .version import __version__


@library(scope="GLOBAL", version=__version__)
class NetworkTransportLibrary:
    """rf_network - Multi-vendor RobotFramework Library to test network devices"""

    def __init__(self):
        self._cache = ConnectionCache()
        self._active_connections = {}
        self._connection_plugin = None
        self.pm = pm

    def connect_to(
        self,
        host: str,
        username: str,
        password: str,
        platform: str,
        alias: str = None,
        connection_plugin: str = None,
        **kwargs
    ):
        params = {
            "host": host,
            "username": username,
            "password": password,
            "platform": platform,
        }
        conn = self.pm.hook.connect_to(
            connection=connection_plugin, **params, options=kwargs
        )
        if conn is None:
            raise ValueError("connection is null")
        self._connection_plugin = connection_plugin
        index = self._cache.register(conn, alias=alias)
        self._active_connections[index] = conn

    def switch_connection_to(self, alias_or_index):
        """SSH Switch To - switch the active switch for all following keywords"""
        self._cache.switch(alias_or_index)
        return self._cache.current_index

    def send_command_to(self, command, ssh_alias_or_index=None, **kwargs):
        """SSH Send Command - Executes ``command`` on a device"""
        conn = self._cache.get_connection(alias_or_index=ssh_alias_or_index)
        return self.pm.hook.send_command_to(
            command=command, conn=conn, conn_name=self._connection_plugin, extras=kwargs
        )

    def get_connections(self):
        return [v for _, v in self._active_connections.items()]

    def clear_connections(self):
        self._active_connections = {}
        self._cache.empty_cache()
