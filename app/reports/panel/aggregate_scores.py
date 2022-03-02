# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panel Aggregate Scores Data Retrieval Functions"""

from typing import List, Dict

from flask import current_app
import mysql.connector


def retrieve_score_spread() -> List[Dict]:
    """Retrieve a list of grouped panelist scores from non-Best Of and
    non-Repeat shows"""
    database_connection = mysql.connector.connect(**current_app.config["database"])
    cursor = database_connection.cursor(dictionary=False)
    query = (
        "SELECT pm.panelistscore, COUNT(pm.panelistscore) "
        "FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "WHERE pm.panelistscore IS NOT NULL "
        "AND s.bestof = 0 AND s.repeatshowid IS NULL "
        "GROUP BY pm.panelistscore "
        "ORDER BY pm.panelistscore ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    scores = []
    counts = []
    for row in result:
        scores.append(row[0])
        counts.append(row[1])

    return {"scores": scores, "counts": counts}
