# -*- coding: utf-8 -*-
import typing as t

from robot.api.deco import keyword, library
from robot.utils.connectioncache import ConnectionCache

try:
    from robot.api import logger
except ImportError:
    logger = None

from .version import __version__
from .plugins import plugin_manager as pm


@library(scope="GLOBAL", version=__version__)
class NetworkTransportLibrary:
    """NetworkTransportLibrary - Multi-vendor RobotFramework Library to test network devices"""

    def __init__(self):
        self._connections = ConnectionCache()
        self._connection_plugin = None
        self.pm = pm
        self._log = logger or None

    @property
    def current(self):
        """Return current connection"""
        return self._connections.current

    def log(self, msg, level="INFO"):
        msg = msg.strip()
        if self._log and msg:
            self._log.write(msg, level)
        elif msg:
            print(f"*{msg}* {level}")

    def get_connection(self, alias_or_index: t.Union[str, int] = None):
        return self._connections.get_connection(alias_or_index)

    @keyword(name="Connect To")
    def open_connection(
        self,
        host: str,
        username: str,
        password: str,
        platform: str,
        alias: t.Optional[str],
        connection_plugin: str = "netmiko",
        **kwargs,
    ):
        """Open connection to device"""
        connection_params = {
            "host": host,
            "username": username,
            "password": password,
            "platform": platform,
        }

        self.log(f"Connecting to {host}; transport: {connection_plugin}")
        print(f"Connecting to {host}; transport: {connection_plugin}")
        conn = self.pm.hook.connect_to(
            connection=connection_plugin, **connection_params, options=kwargs
        )
        print(f"{connection_params}")

        if conn is None:
            raise ValueError("connection is null")
        self._connection_plugin = connection_plugin
        return self._connections.register(conn, alias=alias)

    @keyword(name="Switch To", types={"alias_or_index": (None, int, str)})
    def switch_connection(self, alias_or_index: t.Optional[t.Union[str, int]] = None):
        """Switch To - switch the active switch for all following keywords"""
        old_index = self.current
        if alias_or_index is not None:
            self._connections.switch(alias_or_index)
        return old_index

    @keyword(
        name="Send Command",
        types={"command": str, "alias_or_index": (None, int, str)},
    )
    def send_command(
        self, command: str, alias_or_index: t.Optional[t.Union[str, int]], **kwargs
    ):
        """Send Command - Executes ``command`` on a device"""
        conn = self._connections.get_connection(alias_or_index=alias_or_index)
        return self.pm.hook.send_command(
            command=command, conn=conn, plugin=self._connection_plugin, **kwargs
        )

    @keyword(
        name="Send Command Parsed",
        types={"command": str, "alias_or_index": (None, int, str)},
    )
    def send_command_and_parse(
        self,
        command: str,
        alias_or_index: t.Optional[t.Union[str, int]],
        parser: t.Literal["genie", "textfsm"],
        **kwargs,
    ):
        """Send Command - Executes ``command`` on a device"""
        conn = self._connections.get_connection(alias_or_index=alias_or_index)
        return self.pm.hook.send_command_and_parse(
            command=command,
            conn=conn,
            plugin=self._connection_plugin,
            parser=parser,
            **kwargs,
        )

    @keyword(name="Clear Connections")
    def close_all_connections(self):
        for conn in self._connections._connections:
            self.pm.hook.close_connection(conn=conn, plugin=self._connection_plugin)
        self._connections.close_all()

    @keyword(name="Clear Connection", types={"alias_or_index": (None, int, str)})
    def close_connection(self, alias_or_index=t.Optional[t.Union[str, int]]):
        """Clear Connection - clears the currect active connection"""
        conn = self._connections.get_connection(alias_or_index=alias_or_index)

        self.current.close()
        self._connections.current = self._connections._no_current

        self.pm.hook.close_connection(conn=conn, plugin=self._connection_plugin)
