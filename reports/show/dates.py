# -*- coding: utf-8 -*-
# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Show Dates Retrieval Functions"""

from collections import OrderedDict
from typing import Dict
import mysql.connector

#region Utility Functions
def build_days_of_month_dict(month: int) -> Dict:
    """Returns an OrderedDict containing a key for each day for a given
    month, each containing an OrderedDict used to store counts by show
    type"""

    # Validate that the month number is valid
    if not month in range(1, 13):
        return None

    if month == 2:
        days_in_month = 29
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        days_in_month = 31
    else:
        days_in_month = 30

    month = OrderedDict()
    for day in range(1, days_in_month + 1):
        show_info = OrderedDict()
        show_info["regular"] = 0
        show_info["best_of"] = 0
        show_info["repeat"] = 0
        show_info["best_of_repeat"] = 0
        month[day] = show_info

    return month

def build_days_of_months_all_dict(database_connection: mysql.connector.connect
                                 ) -> Dict:
    """Returns an OrderedDict containing a key for each day for all
    months, each containing an OrderedDict used to store counts by show
    type"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT DATE_FORMAT(showdate, '%d %b') AS date, bestof, repeatshowid "
             "FROM ww_shows "
             "WHERE showdate <= NOW() "
             "ORDER BY MONTH(showdate) ASC, DAY(showdate) ASC;")
    cursor.execute(query, )
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    days = OrderedDict()
    for row in results:
        show_info = OrderedDict()
        show_info["regular"] = 0
        show_info["best_of"] = 0
        show_info["repeat"] = 0
        show_info["best_of_repeat"] = 0
        days[row["date"]] = show_info

    return days

#endregion

#region Retrieval Functions
def retrieve_show_counts_by_month_day(month: int,
                                      database_connection: mysql.connector.connect
                                     ) -> Dict:
    """Retrieves an OrderedDict containing a count of regular shows,
    Best Of shows, repeat shows and repeat Best Of shows for each day
    of the requested month"""

    # Validate that the month number is valid
    if not month in range(1, 13):
        return None

    show_month = build_days_of_month_dict(month)
    if not show_month:
        return None

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT DAY(showdate) AS day, bestof, repeatshowid FROM ww_shows "
             "WHERE MONTH(showdate) = %s "
             "AND showdate <= NOW() "
             "ORDER BY DAY(showdate) ASC;")
    cursor.execute(query, (month, ))
    results = cursor.fetchall()
    cursor.close()

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

def retrieve_show_counts_by_month_day_all(database_connection: mysql.connector.connect
                                         ) -> Dict:
    """Retrieves an OrderedDict containing a count of regular shows,
    Best Of shows, repeat shows and repeat Best Of shows by day for all
    calendar months"""

    shows = build_days_of_months_all_dict(database_connection)

    if not shows:
        return None

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT DATE_FORMAT(showdate, '%d %b') AS date, bestof, repeatshowid "
             "FROM ww_shows "
             "WHERE showdate <= NOW() "
             "ORDER BY MONTH(showdate) ASC, DAY(showdate) ASC;")
    cursor.execute(query, )
    results = cursor.fetchall()
    cursor.close()

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

#endregion
