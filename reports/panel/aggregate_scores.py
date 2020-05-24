# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020 Linh Pham
# graphs.wwdt.me is relased under the terms of the Apache License 2.0
"""WWDTM Panel Aggregate Scores Report Functions"""

from typing import List, Dict
import mysql.connector

#region Retrieval Functions
def retrieve_score_spread(database_connection: mysql.connector.connect
                         ) -> List[Dict]:
    """Retrieve a list of grouped panelist scores from non-Best Of and
    non-Repeat shows"""

    cursor = database_connection.cursor()
    query = ("SELECT pm.panelistscore, COUNT(pm.panelistscore) "
             "FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE pm.panelistscore IS NOT NULL "
             "AND s.bestof = 0 AND s.repeatshowid IS NULL "
             "GROUP BY pm.panelistscore "
             "ORDER BY pm.panelistscore ASC;")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    scores = []
    counts = []
    for row in result:
        scores.append(row[0])
        counts.append(row[1])

    return {"scores": scores, "counts": counts}

#endregion
