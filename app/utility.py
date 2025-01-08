# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Utility functions used by the Graphs Site."""
from datetime import datetime
from typing import Any

import pytz
from flask import current_app
from mysql.connector import DatabaseError, connect
from wwdtm.panelist import Panelist
from wwdtm.show import Show

month_names = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


def format_umami_analytics(umami_analytics: dict = None) -> str:
    """Return formatted string for Umami Analytics."""
    if not umami_analytics:
        return None

    _enabled = bool(umami_analytics.get("_enabled", False))

    if not _enabled:
        return None

    url = umami_analytics.get("url")
    website_id = umami_analytics.get("data_website_id")
    auto_track = bool(umami_analytics.get("data_auto_track", True))
    host_url = umami_analytics.get("data_host_url")
    domains = umami_analytics.get("data_domains")

    if url and website_id:
        host_url_prop = f'data-host-url="{host_url}"' if host_url else ""
        auto_track_prop = f'data-auto-track="{str(auto_track).lower()}"'
        domains_prop = f'data-domains="{domains}"' if domains else ""

        props = " ".join([host_url_prop, auto_track_prop, domains_prop])
        return f'<script defer src="{url}" data-website-id="{website_id}" {props.strip()}></script>'

    return None


def current_year(time_zone: str = "UTC") -> str:
    """Return the current year."""
    _time_zone = pytz.timezone(time_zone)
    now = datetime.now(_time_zone)
    return now.strftime("%Y")


def date_string_to_date(**kwargs) -> datetime | None:
    """Used to convert an ISO-style date string into a datetime object."""
    if "date_string" in kwargs and kwargs["date_string"]:
        try:
            date_object = datetime.strptime(kwargs["date_string"], "%Y-%m-%d")
        except ValueError:
            return None

        return date_object

    return None


def generate_date_time_stamp(time_zone: str = "UTC") -> str:
    """Generate a current date/timestamp string."""
    _time_zone = pytz.timezone(time_zone)
    now = datetime.now(_time_zone)
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")


def redirect_url(url: str, status_code: int = 302):
    """Returns a redirect response for a given URL."""
    # Use a custom response class to force set response headers
    # and handle the redirect to prevent browsers from caching redirect
    response = current_app.response_class(
        response=None, status=status_code, mimetype="text/plain"
    )

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = 0
    response.headers["Location"] = url
    return response


def retrieve_panelists() -> list[dict[str, Any]]:
    """Retrieve information for all panelists."""
    database_connection = connect(**current_app.config["database"])
    panelist = Panelist(database_connection=database_connection)
    panelists = panelist.retrieve_all()
    database_connection.close()
    return panelists


def retrieve_show_years(reverse_order: bool = True) -> list[int]:
    """Retrieve a list of available show years."""
    database_connection = connect(**current_app.config["database"])
    show = Show(database_connection=database_connection)
    years = show.retrieve_years()
    database_connection.close()
    if years and reverse_order:
        years.reverse()

    return years


def time_zone_parser(time_zone: str) -> pytz.timezone:
    """Parses a time zone name into a pytz.timezone object.

    Returns pytz.timezone object and string if time_zone is valid.
    Otherwise, returns UTC if time zone is not a valid tz value.
    """
    try:
        time_zone_object = pytz.timezone(time_zone)
        time_zone_string = time_zone_object.zone
    except (pytz.UnknownTimeZoneError, AttributeError, ValueError):
        time_zone_object = pytz.timezone("UTC")
        time_zone_string = time_zone_object.zone

    return time_zone_object, time_zone_string


def panelist_decimal_score_exists(database_settings: dict) -> bool:
    """Validates that panelist decimal score column exists."""
    try:
        database_connection = connect(**database_settings)
        cursor = database_connection.cursor()
        query = "SHOW COLUMNS FROM ww_showpnlmap WHERE Field = 'panelistscore_decimal'"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return bool(result)
    except DatabaseError:
        return False
