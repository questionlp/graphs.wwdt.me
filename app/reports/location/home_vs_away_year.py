# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Home vs Away by Year Retrieval Functions."""

from flask import current_app
from mysql.connector import connect

from app.reports.show.utility import retrieve_show_years

_LOCATION_ID_TBD = 3
_LOCATION_ID_HOME_REMOTE_STUDIOS = 148
_MAX_SHOWS_PER_YEAR = 53


def retrieve_home_location_ids() -> list[int] | None:
    """Retrieve a list of location IDs for locations in Chicago, Illinois."""
    database_connection = connect(**current_app.config["database"])

    query = """
        SELECT locationid FROM ww_locations
        WHERE city = 'Chicago' AND state = 'IL'
        ORDER BY locationid;
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not results:
        return None

    _ids = []
    for row in results:
        _ids.append(row[0])

    return _ids


def retrieve_all_locations_shows_by_year(year: int) -> list[int] | None:
    """Retrieve a list of all shows with corresponding values for home, remote and studio shows.

    The list contains zeroes for shows away from Chicago, IL and not from home/remote
    studios, ones for shows recorded in Chicago, IL, and twos for home/remote studios
    shows. The returned list will be padded out with zeroes in order to have 53 items.
    """
    database_connection = connect(**current_app.config["database"])

    _years = retrieve_show_years(reverse_order=False)
    if not _years or year not in _years:
        return None

    _home_location_ids = retrieve_home_location_ids()
    if not _home_location_ids:
        return None

    query = """
        SELECT lm.locationid FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
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

    _shows = []
    for row in results:
        if row[0] in _home_location_ids:
            _shows.append(1)
        elif row[0] == _LOCATION_ID_HOME_REMOTE_STUDIOS:
            _shows.append(2)
        else:
            _shows.append(0)

    _shows_locations_len = len(_shows)
    if _shows_locations_len < _MAX_SHOWS_PER_YEAR:
        _shows = _shows + ([None] * (_MAX_SHOWS_PER_YEAR - _shows_locations_len))

    return _shows


def retrieve_all_locations_shows_all_years() -> dict[int, list[int]] | None:
    """Retrieves a dictionary containing shows denoted as home, away and home/remote studios shows.

    Dictionary key is the year and each key value is a list of either
    zeroes, ones or twos noting away, home and home/remote studios shows
    respectively.
    """
    _years = retrieve_show_years(reverse_order=False)

    if not _years:
        return None

    _info = {}
    for year in _years:
        _info[year] = retrieve_all_locations_shows_by_year(year=year)

    return _info


def retrieve_home_shows_by_year(year: int) -> list[int] | None:
    """Retrieve a list of all shows noted as home shows for a given year.

    The list contains either zeroes or ones, where ones denote shows
    recorded in Chicago, IL. The returned list will be padded out with
    zeroes in order to have 53 items.
    """
    database_connection = connect(**current_app.config["database"])

    _years = retrieve_show_years(reverse_order=False)
    if not _years or year not in _years:
        return None

    _home_location_ids = retrieve_home_location_ids()
    if not _home_location_ids:
        return None

    query = """
        SELECT lm.locationid FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
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

    _shows = []
    for row in results:
        if row[0] in _home_location_ids:
            _shows.append(1)
        else:
            _shows.append(0)

    _shows_len = len(_shows)
    if _shows_len < _MAX_SHOWS_PER_YEAR:
        _shows = _shows + ([None] * (_MAX_SHOWS_PER_YEAR - _shows_len))

    return _shows


def retrieve_home_shows_all_years() -> dict[int, list[int]] | None:
    """Retrieves a dictionary containing shows noted as home shows.

    Dictionary key is the year and each key value is a list of either
    zeroes or ones, where ones denote shows recorded in Chicago, IL.
    """
    _years = retrieve_show_years(reverse_order=False)

    if not _years:
        return None

    _info = {}
    for year in _years:
        _info[year] = retrieve_home_shows_by_year(year=year)

    return _info


def retrieve_away_shows_by_year(year: int) -> list[int] | None:
    """Retrieve a list of all shows noted as away shows for a given year.

    The list contains either zeroes or ones, where ones denote shows
    recorded away from Chicago, IL, but exclude shows with Home/Remote
    Studios as their location. The returned list will be padded out with
    zeroes in order to have 53 items.
    """
    database_connection = connect(**current_app.config["database"])

    _years = retrieve_show_years(reverse_order=False)
    if not _years or year not in _years:
        return None

    _home_location_ids = retrieve_home_location_ids()
    # Excluding TBD and Home/Remote Studio location IDs
    _excluded_ids = [_LOCATION_ID_TBD, _LOCATION_ID_HOME_REMOTE_STUDIOS]
    if not _home_location_ids:
        return None

    query = """
        SELECT lm.locationid FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
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

    _shows = []
    for row in results:
        if row[0] in _home_location_ids or row[0] in _excluded_ids:
            _shows.append(0)
        else:
            _shows.append(1)

    _shows_len = len(_shows)
    if _shows_len < _MAX_SHOWS_PER_YEAR:
        _shows = _shows + ([0] * (_MAX_SHOWS_PER_YEAR - _shows_len))

    return _shows


def retrieve_away_shows_all_years() -> dict[int, list[int]] | None:
    """Retrieves a dictionary containing shows noted as away shows.

    Dictionary key is the year and each key value is a list of either
    zeroes or ones, where ones denote shows recorded away from Chicago,
    IL, but exclude shows with Home/Remote Studios as their location.
    """
    _years = retrieve_show_years(reverse_order=False)

    if not _years:
        return None

    _info = {}
    for year in _years:
        _info[year] = retrieve_away_shows_by_year(year=year)

    return _info


def retrieve_home_remote_studios_shows_by_year(year: int) -> list[int] | None:
    """Retrieve a list of all shows noted as Home/Remote Studio shows for a given year.

    The list contains either zeroes or ones, where ones denote shows
    recorded from Home/Remote Studios. The returned list will be padded
    out with zeroes in order to have 53 items.
    """
    database_connection = connect(**current_app.config["database"])

    _years = retrieve_show_years(reverse_order=False)
    if not _years or year not in _years:
        return None

    query = """
        SELECT lm.locationid FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
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

    _shows = []
    for row in results:
        if row[0] == _LOCATION_ID_HOME_REMOTE_STUDIOS:
            _shows.append(1)
        else:
            _shows.append(0)

    _shows_len = len(_shows)
    if _shows_len < _MAX_SHOWS_PER_YEAR:
        _shows = _shows + ([0] * (_MAX_SHOWS_PER_YEAR - _shows_len))

    return _shows


def retrieve_home_remote_studios_shows_all_years() -> dict[int, list[int]] | None:
    """Retrieves a dictionary containing shows noted as Home/Remote Studio shows.

    Dictionary key is the year and each key value is a list of either
    zeroes or ones, where ones denote shows recorded from Home/Remote Studios.
    """
    _years = retrieve_show_years(reverse_order=False)

    if not _years:
        return None

    _info = {}
    for year in _years:
        _info[year] = retrieve_home_remote_studios_shows_by_year(year=year)

    return _info
