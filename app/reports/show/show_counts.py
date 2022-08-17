# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Show Counts Retrieval Functions"""

from typing import Dict

from flask import current_app
import mysql.connector


def retrieve_show_counts_by_year() -> Dict[int, int]:
    """Retrieve the number of Regular, Best Of, Repeat and Repeat/Best
    Of shows broken down by year"""
    database_connection = mysql.connector.connect(**current_app.config["database"])

    # Override session SQL mode value to unset ONLY_FULL_GROUP_BY
    cursor = database_connection.cursor(dictionary=False)
    query = (
        "SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,"
        "NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';"
    )
    cursor.execute(query)
    _ = cursor.fetchall()
    cursor.close()

    years = []
    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT DISTINCT YEAR(showdate) AS 'year' FROM ww_shows "
        "ORDER BY showdate ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    for row in result:
        years.append(int(row.year))

    show_counts = {}
    for year in years:
        cursor = database_connection.cursor(named_tuple=True)
        query = (
            "SELECT "
            "(SELECT COUNT(showid) FROM ww_shows "
            " WHERE YEAR(showdate) = %s AND showdate <= NOW() "
            " AND bestof = 0 AND repeatshowid IS NULL) AS 'regular', "
            "(SELECT COUNT(showid) FROM ww_shows "
            " WHERE YEAR(showdate) = %s AND showdate <= NOW() "
            " AND bestof = 1 AND repeatshowid IS NULL) AS 'bestof', "
            "(SELECT COUNT(showid) FROM ww_shows "
            " WHERE YEAR(showdate) = %s AND showdate <= NOW() "
            " AND bestof = 0 AND repeatshowid IS NOT NULL) AS 'repeat', "
            "(SELECT COUNT(showid) FROM ww_shows "
            " WHERE YEAR(showdate) = %s AND showdate <= NOW() "
            " AND bestof = 1 AND repeatshowid IS NOT NULL) AS 'repeat_bestof';"
        )
        cursor.execute(
            query,
            (
                year,
                year,
                year,
                year,
            ),
        )
        result = cursor.fetchone()
        cursor.close()

        if not result:
            show_counts[year] = None
        else:
            counts = {
                "regular": result.regular,
                "best_of": result.bestof,
                "repeat": result.repeat,
                "repeat_best_of": result.repeat_bestof,
                "total": result.regular
                + result.bestof
                + result.repeat
                + result.repeat_bestof,
            }
            show_counts[year] = counts

    database_connection.close()
    return show_counts
