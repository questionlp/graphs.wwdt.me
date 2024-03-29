# -*- coding: utf-8 -*-
# Copyright (c) 2018-2023 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Show Scores Retrieval Functions"""

from collections import OrderedDict
from typing import Dict
import mysql.connector

#region Utility Functions
def build_year_scoring_dict() -> Dict:
    """Returns an OrderedDict that will be used to populate
    panelist scoring data"""

    score_dict = OrderedDict(Jan=0, Feb=0, Mar=0, Apr=0,
                             May=0, Jun=0, Jul=0, Aug=0,
                             Sep=0, Oct=0, Nov=0, Dec=0)

    return score_dict

def build_all_scoring_dict(database_connection: mysql.connector.connect
                          ) -> Dict:
    """Returns an OrderedDict that contains scoring dictionaries
    used to populate all panelist scoring data"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT DISTINCT YEAR(s.showdate) AS year "
             "FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE s.bestof = 0 "
             "AND s.repeatshowid IS NULL "
             "GROUP BY YEAR(s.showdate) "
             "HAVING SUM(pm.panelistscore) IS NOT NULL "
             "ORDER BY YEAR(s.showdate);")
    cursor.execute(query, )
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    all_scores_dict = OrderedDict()
    for row in result:
        all_scores_dict[row["year"]] = build_year_scoring_dict()

    return all_scores_dict

#endregion

#region Retrieval Functions
def retrieve_monthly_aggregate_scores(database_connection: mysql.connector.connect
                                     ) -> Dict:
    """Retrieve aggregated panelist scores grouped by month
    for every available year"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT YEAR(s.showdate) AS year, "
             "DATE_FORMAT(s.showdate, '%b') AS month, "
             "SUM(pm.panelistscore) AS total "
             "FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE s.bestof = 0 "
             "AND s.repeatshowid IS NULL "
             "GROUP BY YEAR(s.showdate), MONTH(s.showdate) "
             "HAVING SUM(pm.panelistscore) IS NOT NULL "
             "ORDER BY YEAR(s.showdate), MONTH(s.showdate);")
    cursor.execute(query, )
    result = cursor.fetchall()

    if not result:
        return None

    all_scores_dict = build_all_scoring_dict(database_connection)
    for row in result:
        all_scores_dict[row["year"]][row["month"]] = int(row["total"])

    return all_scores_dict

def retrieve_monthly_average_scores(database_connection: mysql.connector.connect
                                   ) -> Dict:
    """Retrieve average panelist scores grouped by month
    for every available year"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT YEAR(s.showdate) AS year, "
             "DATE_FORMAT(s.showdate, '%b') AS month, "
             "AVG(pm.panelistscore) AS average "
             "FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE s.bestof = 0 "
             "AND s.repeatshowid IS NULL "
             "GROUP BY YEAR(s.showdate), MONTH(s.showdate) "
             "HAVING AVG(pm.panelistscore) IS NOT NULL "
             "ORDER BY YEAR(s.showdate), MONTH(s.showdate);")
    cursor.execute(query, )
    result = cursor.fetchall()

    if not result:
        return None

    all_scores_dict = build_all_scoring_dict(database_connection)
    for row in result:
        all_scores_dict[row["year"]][row["month"]] = float(row["average"])

    return all_scores_dict

#endregion
