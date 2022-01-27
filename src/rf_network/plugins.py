# -*- coding: utf-8 -*-
import importlib
import sys

import pluggy

from . import hookspecs

DEFAULT_PLUGINS = (
    "rf_network.connection.netmiko",
    "rf_network.connection.scrapli",
)

plugin_manager = pluggy.PluginManager("rf_network")
plugin_manager.add_hookspecs(hookspecs)

if not hasattr(sys, "_called_from_test"):
    # Only load plugins if not running tests
    plugin_manager.load_setuptools_entrypoints("rf_network")

# Load default plugins
for plugin in DEFAULT_PLUGINS:
    mod = importlib.import_module(plugin)
    plugin_manager.register(mod, plugin)
