# Copyright (c) 2018-2026 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Types by Year Retrieval Functions."""

from flask import current_app
from mysql.connector import connect

from app.reports.location.home_vs_away_year import _MAX_SHOWS_PER_YEAR
from app.reports.show.utility import retrieve_show_years


def retrieve_show_types_by_year(year: int) -> list[int] | None:
    """Retrieve a list of all shows with corresponding values for show types.

    The list contains zeroes for regular shows, ones for Best Of shows,
    twos for repeat shows, and threes for repeat Best Of shows. The
    returned list will be padded out with None in order to have 53
    items.
    """
    database_connection = connect(**current_app.config["database"])

    _years: list[int] | None = retrieve_show_years(reverse_order=False)
    if not _years or year not in _years:
        return None

    query = """
        SELECT bestof, repeatshowid FROM ww_shows
        WHERE YEAR(showdate) = %s
        ORDER BY showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (year,))
    results = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not results:
        return None

    _shows: list[int | None] = []
    for row in results:
        best_of = bool(row[0])
        repeat = bool(row[1])

        if best_of and repeat:
            _shows.append(3)
        elif repeat:
            _shows.append(2)
        elif best_of:
            _shows.append(1)
        elif not best_of and not repeat:
            _shows.append(0)

    _shows_len: int = len(_shows)
    if _shows_len < _MAX_SHOWS_PER_YEAR:
        _shows = _shows + ([None] * (_MAX_SHOWS_PER_YEAR - _shows_len))

    return _shows


def retrieve_show_types_by_year_with_dates(
    year: int,
) -> dict[str, list[int | None]] | None:
    """Retrieves all shows for a given year with values denoting show types.

    The returned dictionary contains a list of show dates and a list
    of each regular, Best Of, repeat and repeat Best Of shows where
    one denotes the corresponding show type.
    """
    database_connection = connect(**current_app.config["database"])

    _years = retrieve_show_years(reverse_order=False)
    if not _years or year not in _years:
        return None

    query = """
        SELECT showdate, bestof, repeatshowid FROM ww_shows
        WHERE YEAR(showdate) = %s
        ORDER BY showdate ASC;
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
    _best_ofs = []
    _repeats = []
    _repeat_best_ofs = []

    for row in results:
        best_of = bool(row[1])
        repeat = bool(row[2])

        _show_dates.append(row[0].isoformat())
        if best_of and repeat:
            _regulars.append(None)
            _best_ofs.append(None)
            _repeats.append(None)
            _repeat_best_ofs.append(1)
        elif best_of:
            _regulars.append(None)
            _best_ofs.append(1)
            _repeats.append(None)
            _repeat_best_ofs.append(None)
        elif repeat:
            _regulars.append(None)
            _best_ofs.append(None)
            _repeats.append(1)
            _repeat_best_ofs.append(None)
        elif not best_of and not repeat:
            _regulars.append(1)
            _best_ofs.append(None)
            _repeats.append(None)
            _repeat_best_ofs.append(None)

    return {
        "show_dates": _show_dates,
        "regulars": _regulars,
        "best_ofs": _best_ofs,
        "repeats": _repeats,
        "repeat_best_ofs": _repeat_best_ofs,
    }


def retrieve_show_types_all_years() -> dict[int, list[int | None]] | None:
    """Retrieves a dictionary containing show types across all years.

    Dictionary key is the year and the key value is a list of zeroes,
    ones, twos and threes for regular, Best Of, repeat and repeat Best
    Of shows respectively. Lists are padded with None values at the end
    to have consistent list length.
    """
    _years: list[int] | None = retrieve_show_years(reverse_order=False)

    if not _years:
        return None

    _info = {}
    for year in _years:
        _info[year] = retrieve_show_types_by_year(year=year)

    return _info
