# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Host Types Retrieval Functions."""

from flask import current_app
from mysql.connector import connect

from app.reports.location.home_vs_away_year import _MAX_SHOWS_PER_YEAR
from app.reports.show.utility import retrieve_show_years


def retrieve_host_types_by_year(year: int) -> list[int] | None:
    """Retrieve a list of all shows for a given year with corresponding value for normal or guest hosts.

    The list contains zeroes for regular hosts and ones for guest hosts. The
    returned list will be padded out with zeroes in order to have 53 items.
    """
    database_connection = connect(**current_app.config["database"])

    _years = retrieve_show_years(reverse_order=False)
    if not _years or year not in _years:
        return None

    query = """
        SELECT hm.guest FROM ww_showhostmap hm
        JOIN ww_shows s ON s.showid = hm.showid
        WHERE YEAR(s.showdate) = %s
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (year,))
    results = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not results:
        return None

    _hosts = []
    for row in results:
        if bool(row[0]):
            _hosts.append(1)
        else:
            _hosts.append(0)

    _hosts_len = len(_hosts)
    if _hosts_len < _MAX_SHOWS_PER_YEAR:
        _hosts = _hosts + ([None] * (_MAX_SHOWS_PER_YEAR - _hosts_len))

    return _hosts


def retrieve_host_types_by_year_with_dates(
    year: int,
) -> dict[str, list[int | None]] | None:
    """Retrieve all shows for a given year with values for normal or guest hosts.

    The dictionary contains two lists, one with show dates and a list each
    denoting regular and guest hosts with ones denoting the corresponding type.
    """
    database_connection = connect(**current_app.config["database"])

    _years = retrieve_show_years(reverse_order=False)
    if not _years or year not in _years:
        return None

    query = """
        SELECT s.showdate, hm.guest FROM ww_showhostmap hm
        JOIN ww_shows s ON s.showid = hm.showid
        WHERE YEAR(s.showdate) = %s
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (year,))
    results = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not results:
        return None

    _show_dates = []
    _regulars = []
    _guests = []

    for row in results:
        _show_dates.append(row[0].isoformat())
        if bool(row[1]):
            _regulars.append(None)
            _guests.append(1)

        else:
            _regulars.append(1)
            _guests.append(None)

    return {
        "show_dates": _show_dates,
        "regulars": _regulars,
        "guests": _guests,
    }


def retrieve_host_types_all_years() -> dict[int, list[int]] | None:
    """Retrieves a dictionary containing show hosts noted as regular or guest hosts.

    Dictionary key is the year and each key value is a list of either
    zeroes or ones, where ones denote guest hosts.
    """
    _years = retrieve_show_years(reverse_order=False)

    if not _years:
        return None

    _info = {}
    for year in _years:
        _info[year] = retrieve_host_types_by_year(year=year)

    return _info
