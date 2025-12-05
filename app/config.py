# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Configuration Loading and Parsing for Wait Wait Graphs Site."""

import json
from pathlib import Path
from typing import Any

import yaml

from app import utility

COLORWAY_LIGHT: list[str] = [
    "#6929c4",  # IBM Purple 70
    "#1192e8",  # IBM Cyan 50
    "#005d5d",  # IBM Teal 70
    "#d4bbff",  # IBM Purple 30
    "#570408",  # IBM Red 90
]
COLORWAY_DARK: list[str] = [
    "#8a3ffc",  # IBM Purple 60
    "#08bdba",  # IBM Teal 40
    "#bae6ff",  # IBM Cyan 20
    "#4589ff",  # IBM Blue 50
    "#ff7eb6",  # IBM Magenta 40
]

COLORWAY_RETRO: list[str] = [
    "#800080",  # HTML Purple
    "#00ffff",  # HTML Cyan
    "#336666",
    "#0000ff",  # HTML Blue
    "#ff00ff",
]

COLORSCALE: list[float | str] = [
    [0.0, "#000000"],  # Black
    [0.1, "#1c0f30"],  # IBM Purple 100
    [0.2, "#31135e"],  # IBM Purple 90
    [0.3, "#491d8b"],  # IBM Purple 80
    [0.4, "#6929c4"],  # IBM Purple 70
    [0.5, "#8a3ffc"],  # IBM Purple 60
    [0.6, "#a56eff"],  # IBM Purple 50
    [0.7, "#be95ff"],  # IBM Purple 40
    [0.8, "#d4bbff"],  # IBM Purple 30
    [0.9, "#e8daff"],  # IBM Purple 20
    [1.0, "#f6f2ff"],  # IBM Purple 10
]

COLORSCALE_COMPRESSED_BOTTOM: list[float | str] = [
    [0.000, "#000000"],  # Black
    [0.001, "#31135e"],  # IBM Purple 90
    [0.025, "#d4bbff"],  # IBM Purple 30
    [1.000, "#f6f2ff"],  # IBM Purple 10
]

COLORSCALE_COMPRESSED_BOTTOM_RETRO: list[float | str] = [
    [0.000, "#000000"],  # Black
    [0.001, "#330066"],
    [0.100, "#ff00ff"],
    [1.000, "#ffccff"],
]

COLORSCALE_RETRO: list[float | str] = [
    [0.0, "#000000"],  # Black
    [0.2, "#330066"],
    [0.4, "#6600cc"],
    [0.6, "#9900ff"],
    [0.8, "#ff99ff"],
    [1.0, "#ffccff"],
]

COLORSCALE_HOME: list[float | str] = [
    [0.0, "#000000"],  # Black
    [1.0, "#a56eff"],  # IBM Purple 50
]

COLORSCALE_HOME_RETRO: list[float | str] = [
    [0.0, "#000000"],  # Black
    [1.0, "#ff66ff"],
]

COLORSCALE_AWAY: list[float | str] = [
    [0.0, "#000000"],  # Black
    [1.0, "#f1c21b"],  # IBM Alert 30
]

COLORSCALE_AWAY_RETRO: list[float | str] = [
    [0.0, "#000000"],  # Black
    [1.0, "#ffff66"],
]

COLORSCALE_STUDIOS: list[float | str] = [
    [0.0, "#000000"],  # Black
    [1.0, "#007d79"],  # IBM Teal 60
]

COLORSCALE_STUDIOS_RETRO: list[float | str] = [
    [0.0, "#000000"],  # Black
    [1.0, "#00cc00"],
]

COLORSCALE_HOME_AWAY_STUDIOS: list[float | str] = [
    [0.0, "#f1c21b"],  # IBM Alert 30 (Away)
    [0.5, "#a56eff"],  # IBM Purple 50 (Home)
    [1.0, "#007d79"],  # IBM Teal 60 (Home/Remote Studios)
]

COLORSCALE_HOME_AWAY_STUDIOS_RETRO: list[float | str] = [
    [0.0, "#ffff66"],  # Away
    [0.5, "#ff66ff"],  # Home
    [1.0, "#00cc00"],  # Home/Remote Studios
]


def load_colors(colors_file_path: str = "colors.yaml") -> dict[str, list[str]]:
    """Read colors YAML configuration file."""
    _colors_file_path = Path(colors_file_path)
    if _colors_file_path.exists():
        with _colors_file_path.open(mode="r", encoding="utf-8") as colors_file:
            colors_config: dict[str, list[str | int | float]] = yaml.safe_load(
                colors_file
            )

        _config = {
            "colorway_light": colors_config.get("colorway_light", COLORWAY_LIGHT),
            "colorway_dark": colors_config.get("colorway_dark", COLORWAY_DARK),
            "colorway_retro": colors_config.get("colorway_retro", COLORWAY_RETRO),
            "colorscale": colors_config.get("colorscale", COLORSCALE),
            "colorscale_bold": colors_config.get("colorscale_bold", COLORSCALE),
            "colorscale_compressed_bottom": colors_config.get(
                "colorscale_compressed_bottom", COLORSCALE_COMPRESSED_BOTTOM
            ),
            "colorscale_compressed_bottom_retro": colors_config.get(
                "colorscale_compressed_bottom_retro", COLORSCALE_COMPRESSED_BOTTOM_RETRO
            ),
            "colorscale_retro": colors_config.get("colorscale_retro", COLORSCALE_RETRO),
            "colorscale_home": colors_config.get("colorscale_home", COLORSCALE_HOME),
            "colorscale_home_retro": colors_config.get(
                "colorscale_home_retro", COLORSCALE_HOME_RETRO
            ),
            "colorscale_away": colors_config.get("colorscale_away", COLORSCALE_AWAY),
            "colorscale_away_retro": colors_config.get(
                "colorscale_away_retro", COLORSCALE_AWAY_RETRO
            ),
            "colorscale_studios": colors_config.get(
                "colorscale_studios", COLORSCALE_STUDIOS
            ),
            "colorscale_studios_retro": colors_config.get(
                "colorscale_studios_retro", COLORSCALE_STUDIOS_RETRO
            ),
            "colorscale_home_away_studios": colors_config.get(
                "colorscale_home_away_studios", COLORSCALE_HOME_AWAY_STUDIOS
            ),
            "colorscale_home_away_studios_retro": colors_config.get(
                "colorscale_home_away_studios_retro", COLORSCALE_HOME_AWAY_STUDIOS_RETRO
            ),
        }
    else:
        _config = {
            "colorway_light": COLORWAY_LIGHT,
            "colorway_dark": COLORWAY_DARK,
            "colorway_retro": COLORWAY_RETRO,
            "colorscale": COLORSCALE,
            "colorscale_bold": COLORSCALE,
            "colorscale_compressed_bottom": COLORSCALE_COMPRESSED_BOTTOM,
            "colorscale_compressed_bottom_retro": COLORSCALE_COMPRESSED_BOTTOM_RETRO,
            "colorscale_retro": COLORSCALE_RETRO,
            "colorscale_home": COLORSCALE_HOME,
            "colorscale_home_retro": COLORSCALE_HOME_RETRO,
            "colorscale_away": COLORSCALE_AWAY,
            "colorscale_away_retro": COLORSCALE_AWAY_RETRO,
            "colorscale_studios": COLORSCALE_STUDIOS,
            "colorscale_studios_retro": COLORSCALE_STUDIOS_RETRO,
            "colorscale_home_away_studios": COLORSCALE_HOME_AWAY_STUDIOS,
            "colorscale_home_away_studios_retro": COLORSCALE_HOME_AWAY_STUDIOS_RETRO,
        }

    return _config


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
            pool_name: str = str(database_config.get("pool_name", connection_pool_name))
            pool_size: int = int(database_config.get("pool_size", connection_pool_size))
            _pool_size = max(pool_size, connection_pool_size)

            database_config["pool_name"] = pool_name
            database_config["pool_size"] = _pool_size
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

    # Read in Umami Analytics settings
    if "umami_analytics" in settings_config:
        _umami = dict(settings_config["umami_analytics"])
        settings_config["umami"] = {
            "enabled": bool(_umami.get("enabled", False)),
            "url": _umami.get("url"),
            "website_id": _umami.get("data_website_id"),
            "auto_track": bool(_umami.get("data_auto_track", True)),
            "host_url": _umami.get("data_host_url"),
            "domains": _umami.get("data_domains"),
        }

        del settings_config["umami_analytics"]
    else:
        settings_config["umami"] = {
            "enabled": False,
        }

    return {
        "database": database_config,
        "settings": settings_config,
    }
