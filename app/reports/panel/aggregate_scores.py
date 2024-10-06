# Copyright (c) 2018-2024 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panel Aggregate Scores Data Retrieval Functions."""
from math import floor

from flask import current_app
from mysql.connector import connect


def empty_score_spread(use_decimal_scores: bool = False) -> dict | None:
    """Generate an empty score spread dictionary."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    database_connection = connect(**current_app.config["database"])
    query = (
        "SELECT MIN(pm.panelistscore_decimal) AS min, "
        "MAX(pm.panelistscore_decimal) AS max "
        "FROM ww_showpnlmap pm;"
    )
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchone()

    if not result:
        return None

    min_score = result["min"]
    max_score = result["max"]

    if use_decimal_scores:
        score_spread = {}
        for score in range(floor(min_score), floor(max_score) + 1):
            score_plus_half = score + 0.5
            score_spread[score] = 0
            score_spread[score_plus_half] = 0
    else:
        score_spread = {}
        for score in range(min_score, max_score + 1):
            score_spread[score] = 0

    return score_spread


def retrieve_score_spread(use_decimal_scores: bool = False) -> dict | None:
    """Retrieve a dictionary of grouped panelist scores from regular shows."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    database_connection = connect(**current_app.config["database"])
    if use_decimal_scores:
        query = """
            SELECT pm.panelistscore_decimal AS score,
            COUNT(pm.panelistscore_decimal) AS count
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistscore_decimal IS NOT NULL
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY pm.panelistscore_decimal
            ORDER BY pm.panelistscore_decimal ASC;
            """
    else:
        query = """
            SELECT pm.panelistscore AS score, COUNT(pm.panelistscore) AS count
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistscore IS NOT NULL
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY pm.panelistscore
            ORDER BY pm.panelistscore ASC;
            """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    score_spread = empty_score_spread(use_decimal_scores=use_decimal_scores)
    for row in result:
        score_spread[row["score"]] = row["count"]

    return {
        "scores": list(score_spread.keys()),
        "counts": list(score_spread.values()),
    }
