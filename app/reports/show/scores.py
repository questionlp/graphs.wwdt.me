# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Show Scores Retrieval Functions"""
from curses import use_default_colors
from typing import Dict

from flask import current_app
from mysql.connector import connect


def build_year_scoring_dict() -> Dict:
    """Returns an dictionary that will be used to populate panelist
    scoring data"""
    return {
        "Jan": 0,
        "Feb": 0,
        "Mar": 0,
        "Apr": 0,
        "May": 0,
        "Jun": 0,
        "Jul": 0,
        "Aug": 0,
        "Sep": 0,
        "Oct": 0,
        "Nov": 0,
        "Dec": 0,
    }


def build_all_scoring_dict(use_decimal_scores: bool = False) -> Dict:
    """Returns an dictionary that contains scoring dictionaries used to
    populate all panelist scoring data"""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    database_connection = connect(**current_app.config["database"])

    # Override session SQL mode value to unset ONLY_FULL_GROUP_BY
    query = (
        "SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,"
        "NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';"
    )
    cursor = database_connection.cursor()
    cursor.execute(query)
    _ = cursor.fetchall()
    cursor.close()

    if use_decimal_scores:
        query = """
            SELECT DISTINCT YEAR(s.showdate) AS year
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY YEAR(s.showdate)
            HAVING SUM(pm.panelistscore_decimal) IS NOT NULL
            ORDER BY YEAR(s.showdate);
            """
    else:
        query = """
            SELECT DISTINCT YEAR(s.showdate) AS year
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY YEAR(s.showdate)
            HAVING SUM(pm.panelistscore) IS NOT NULL
            ORDER BY YEAR(s.showdate);
            """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    all_scores_dict = {}
    for row in result:
        all_scores_dict[row.year] = build_year_scoring_dict()

    return all_scores_dict


def retrieve_monthly_aggregate_scores(use_decimal_scores: bool = False) -> Dict:
    """Retrieve aggregated panelist scores grouped by month for every
    available year"""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    database_connection = connect(**current_app.config["database"])

    # Override session SQL mode value to unset ONLY_FULL_GROUP_BY

    query = (
        "SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,"
        "NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';"
    )
    cursor = database_connection.cursor()
    cursor.execute(query)
    _ = cursor.fetchall()
    cursor.close()

    if use_decimal_scores:
        query = """
            SELECT YEAR(s.showdate) AS year,
            DATE_FORMAT(s.showdate, '%b') AS month,
            SUM(pm.panelistscore_decimal) AS total
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0
            AND s.repeatshowid IS NULL
            GROUP BY YEAR(s.showdate), MONTH(s.showdate)
            HAVING SUM(pm.panelistscore_decimal) IS NOT NULL
            ORDER BY YEAR(s.showdate), MONTH(s.showdate);
            """
    else:
        query = """
            SELECT YEAR(s.showdate) AS year,
            DATE_FORMAT(s.showdate, '%b') AS month,
            SUM(pm.panelistscore) AS total
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0
            AND s.repeatshowid IS NULL
            GROUP BY YEAR(s.showdate), MONTH(s.showdate)
            HAVING SUM(pm.panelistscore) IS NOT NULL
            ORDER BY YEAR(s.showdate), MONTH(s.showdate);
            """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    all_scores_dict = build_all_scoring_dict()
    for row in result:
        all_scores_dict[row.year][row.month] = int(row.total)

    return all_scores_dict


def retrieve_monthly_average_scores(use_decimal_scores: bool = False) -> Dict:
    """Retrieve average panelist scores grouped by month
    for every available year"""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    database_connection = connect(**current_app.config["database"])

    # Override session SQL mode value to unset ONLY_FULL_GROUP_BY
    query = (
        "SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,"
        "NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';"
    )
    cursor = database_connection.cursor()
    cursor.execute(query)
    _ = cursor.fetchall()
    cursor.close()

    if use_decimal_scores:
        query = """
            SELECT YEAR(s.showdate) AS year,
            DATE_FORMAT(s.showdate, '%b') AS month,
            AVG(pm.panelistscore_decimal) AS average
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0
            AND s.repeatshowid IS NULL
            GROUP BY YEAR(s.showdate), MONTH(s.showdate)
            HAVING AVG(pm.panelistscore_decimal) IS NOT NULL
            ORDER BY YEAR(s.showdate), MONTH(s.showdate);
            """
    else:
        query = """
            SELECT YEAR(s.showdate) AS year,
            DATE_FORMAT(s.showdate, '%b') AS month,
            AVG(pm.panelistscore) AS average
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0
            AND s.repeatshowid IS NULL
            GROUP BY YEAR(s.showdate), MONTH(s.showdate)
            HAVING AVG(pm.panelistscore) IS NOT NULL
            ORDER BY YEAR(s.showdate), MONTH(s.showdate);
            """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(
        query,
    )
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    all_scores_dict = build_all_scoring_dict()
    for row in result:
        all_scores_dict[row.year][row.month] = float(row.average)

    return all_scores_dict
