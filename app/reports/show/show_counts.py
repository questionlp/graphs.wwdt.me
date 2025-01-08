# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Counts Retrieval Functions."""
from flask import current_app
from mysql.connector import connect


def retrieve_show_counts_by_year() -> dict[int, int] | None:
    """Retrieve the number of shows broken down by year.

    Breakdown includes Regular, Best Of, Repeat and Repeat/Best Of shows.
    """
    database_connection = connect(**current_app.config["database"])

    query = """
        SELECT DISTINCT YEAR(showdate) AS 'year'
        FROM ww_shows
        ORDER BY YEAR(showdate) ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    years = []
    for row in result:
        years.append(int(row["year"]))

    show_counts = {}
    for year in years:
        query = """
            SELECT
            (
                SELECT COUNT(showid) FROM ww_shows
                WHERE YEAR(showdate) = %s AND showdate <= NOW()
                AND bestof = 0 AND repeatshowid IS NULL
            ) AS 'regular',
            (
                SELECT COUNT(showid) FROM ww_shows
                WHERE YEAR(showdate) = %s AND showdate <= NOW()
                AND bestof = 1 AND repeatshowid IS NULL
            ) AS 'bestof',
            (
                SELECT COUNT(showid) FROM ww_shows
                WHERE YEAR(showdate) = %s AND showdate <= NOW()
                AND bestof = 0 AND repeatshowid IS NOT NULL
            ) AS 'repeat',
            (
                SELECT COUNT(showid) FROM ww_shows
                WHERE YEAR(showdate) = %s AND showdate <= NOW()
                AND bestof = 1 AND repeatshowid IS NOT NULL
            ) AS 'repeat_bestof';
            """
        cursor = database_connection.cursor(dictionary=True)
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
                "regular": result["regular"],
                "best_of": result["bestof"],
                "repeat": result["repeat"],
                "repeat_best_of": result["repeat_bestof"],
                "total": result["regular"]
                + result["bestof"]
                + result["repeat"]
                + result["repeat_bestof"],
            }
            show_counts[year] = counts

    database_connection.close()
    return show_counts
