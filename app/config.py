# Copyright (c) 2018-2024 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Configuration Loading and Parsing for Wait Wait Graphs Site."""
import json
from pathlib import Path
from typing import Any

from app import utility


def load_config(
    config_file_path: str = "config.json",
    connection_pool_size: int = 12,
    connection_pool_name: str = "wwdtm_graphs",
    app_time_zone: str = "UTC",
) -> dict[str, dict[str, Any]]:
    """Read configuration and database settings."""
    _config_file_path = Path(config_file_path)
    with _config_file_path.open(mode="r", encoding="utf-8") as config_file:
        app_config = json.load(config_file)

    database_config = app_config.get("database", None)
    settings_config = app_config.get("settings", None)

    # Process database configuration settings
    if database_config:
        # Set database connection pooling settings if and only if there
        # is a ``use_pool`` key and it is set to True. Remove the key
        # after parsing through the configuration to prevent issues
        # with mysql.connector.connect()
        use_pool = database_config.get("use_pool", False)

        if use_pool:
            pool_name = database_config.get("pool_name", connection_pool_name)
            pool_size = database_config.get("pool_size", connection_pool_size)
            if pool_size < connection_pool_size:
                pool_size = connection_pool_size

            database_config["pool_name"] = pool_name
            database_config["pool_size"] = pool_size
            del database_config["use_pool"]
        else:
            if "pool_name" in database_config:
                del database_config["pool_name"]

            if "pool_size" in database_config:
                del database_config["pool_size"]

            if "use_pool" in database_config:
                del database_config["use_pool"]

    # Process time zone configuration settings
    time_zone = settings_config.get("time_zone", app_time_zone)
    time_zone_object, time_zone_string = utility.time_zone_parser(time_zone)
    settings_config["app_time_zone"] = time_zone_object
    settings_config["time_zone"] = time_zone_string
    database_config["time_zone"] = time_zone_string

    return {
        "database": database_config,
        "settings": settings_config,
    }
