# Copyright (c) 2018-2026 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Dates Retrieval Functions."""

from flask import current_app
from mysql.connector import connect


def build_days_of_month_dict(month: int) -> dict:
    """Return a dictionary used to store counts by show type."""
    # Validate that the month number is valid
    if month not in range(1, 13):
        return None

    if month == 2:
        days_in_month = 29
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        days_in_month = 31
    else:
        days_in_month = 30

    month = {}
    for day in range(1, days_in_month + 1):
        show_info = {
            "regular": 0,
            "best_of": 0,
            "repeat": 0,
            "best_of_repeat": 0,
        }
        month[day] = show_info

    return month


def build_days_of_months_all_dict() -> dict | None:
    """Return a dictionary used to store counts by show type."""
    database_connection = connect(**current_app.config["database"])
    query = """
        SELECT DATE_FORMAT(showdate, '%d %b') AS date, bestof, repeatshowid
        FROM ww_shows
        WHERE showdate <= NOW()
        ORDER BY MONTH(showdate) ASC, DAY(showdate) ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not results:
        return None

    days = {}
    for row in results:
        show_info = {
            "regular": 0,
            "best_of": 0,
            "repeat": 0,
            "best_of_repeat": 0,
        }
        days[row["date"]] = show_info

    return days


def retrieve_show_counts_by_month_day(month: int) -> dict | None:
    """Retrieve a dictionary containing a count of show types."""
    # Validate that the month number is valid
    if month not in range(1, 13):
        return None

    show_month = build_days_of_month_dict(month)
    if not show_month:
        return None

    database_connection = connect(**current_app.config["database"])
    query = """
        SELECT DAY(showdate) AS day, bestof, repeatshowid FROM ww_shows
        WHERE MONTH(showdate) = %s
        AND showdate <= NOW()
        ORDER BY DAY(showdate) ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (month,))
    results = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not results:
        return None

    for row in results:
        day = row["day"]
        best_of = bool(row["bestof"])
        repeat_show = bool(row["repeatshowid"])

        if not best_of and not repeat_show:
            show_month[day]["regular"] += 1
        elif best_of and not repeat_show:
            show_month[day]["best_of"] += 1
        elif not best_of and repeat_show:
            show_month[day]["repeat"] += 1
        elif best_of and repeat_show:
            show_month[day]["best_of_repeat"] += 1

    return show_month


def retrieve_show_counts_by_month_day_all() -> dict | None:
    """Retrieve a dictionary containing a count of show types."""
    shows = build_days_of_months_all_dict()

    if not shows:
        return None

    database_connection = connect(**current_app.config["database"])
    query = """
        SELECT DATE_FORMAT(showdate, '%d %b') AS date, bestof, repeatshowid
        FROM ww_shows
        WHERE showdate <= NOW()
        ORDER BY MONTH(showdate) ASC, DAY(showdate) ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not results:
        return None

    for row in results:
        date = row["date"]
        best_of = bool(row["bestof"])
        repeat_show = bool(row["repeatshowid"])

        if not best_of and not repeat_show:
            shows[date]["regular"] += 1
        elif best_of and not repeat_show:
            shows[date]["best_of"] += 1
        elif not best_of and repeat_show:
            shows[date]["repeat"] += 1
        elif best_of and repeat_show:
            shows[date]["best_of_repeat"] += 1

    return shows
