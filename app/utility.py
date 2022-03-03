# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2020 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""Utility functions used by the Graphs Site"""

from datetime import datetime
from dateutil import parser
from flask import current_app
from typing import Any, Dict, List
import mysql.connector
import pytz

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


def current_year(time_zone: pytz.timezone = pytz.timezone("UTC")) -> str:
    """Return the current year"""
    now = datetime.now(time_zone)
    return now.strftime("%Y")


def date_string_to_date(**kwargs) -> datetime:
    """Used to convert an ISO-style date string into a datetime object"""
    if "date_string" in kwargs and kwargs["date_string"]:
        try:
            date_object = parser.parse(kwargs["date_string"])
            return date_object

        except ValueError:
            return None

    return None


def generate_date_time_stamp(time_zone: pytz.timezone = pytz.timezone("UTC")) -> str:
    """Generate a current date/timestamp string"""
    now = datetime.now(time_zone)
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")


def redirect_url(url: str, status_code: int = 302):
    """Returns a redirect response for a given URL"""
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


def retrieve_panelists() -> List[Dict[str, Any]]:
    """Retrieve information for all panelists"""
    database_connection = mysql.connector.connect(**current_app.config["database"])
    panelist = Panelist(database_connection=database_connection)
    panelists = panelist.retrieve_all()
    database_connection.close()
    return panelists


def retrieve_show_years(reverse_order: bool = True) -> List[int]:
    """Retrieve a list of available show years"""
    database_connection = mysql.connector.connect(**current_app.config["database"])
    show = Show(database_connection=database_connection)
    years = show.retrieve_years()
    database_connection.close()
    if years and reverse_order:
        years.reverse()

    return years


def time_zone_parser(time_zone: str) -> pytz.timezone:
    """Parses a time zone name into a pytz.timezone object.

    Returns pytz.timezone object and string if time_zone is valid.
    Otherwise, returns UTC if time zone is not a valid tz value."""
    try:
        time_zone_object = pytz.timezone(time_zone)
        time_zone_string = time_zone_object.zone
    except (pytz.UnknownTimeZoneError, AttributeError, ValueError):
        time_zone_object = pytz.timezone("UTC")
        time_zone_string = time_zone_object.zone

    return time_zone_object, time_zone_string
