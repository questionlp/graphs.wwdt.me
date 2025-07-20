# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Location Home vs Away Retrieval Functions."""

from flask import current_app
from mysql.connector import connect


def retrieve_home_vs_away_by_year(year: int) -> dict[str, int | None] | None:
    """Retrieve counts of home versus away shows for a given year."""
    database_connection = connect(**current_app.config["database"])

    query = """
        SELECT (
            SELECT COUNT(s.showid)
            FROM ww_shows s
            JOIN ww_showlocationmap lm ON lm.showid = s.showid
            JOIN ww_locations l ON l.locationid = lm.locationid
            WHERE YEAR(s.showdate) = %s
            AND s.bestof = 0
            AND s.repeatshowid IS NULL
            AND l.city = 'Chicago'
            AND l.state = 'IL'
        )  AS 'home', (
            SELECT COUNT(s.showid)
            FROM ww_shows s
            JOIN ww_showlocationmap lm ON lm.showid = s.showid
            JOIN ww_locations l ON l.locationid = lm.locationid
            WHERE YEAR(s.showdate) = %s
            AND s.bestof = 0
            AND s.repeatshowid IS NULL
            AND l.city <> 'Chicago'
            AND l.state <> 'IL'
        ) AS 'away', (
            SELECT COUNT(s.showid)
            FROM ww_shows s
            JOIN ww_showlocationmap lm ON lm.showid = s.showid
            JOIN ww_locations l ON l.locationid = lm.locationid
            WHERE YEAR(s.showdate) = %s
            AND s.bestof = 0
            AND s.repeatshowid IS NULL
            AND lm.locationid = 148
        ) AS 'studios';
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(
        query,
        (
            year,
            year,
            year,
        ),
    )
    result = cursor.fetchone()
    cursor.close()

    counts = {
        "home": result["home"],
        "away": result["away"],
        "studios": result["studios"],
    }

    return counts
