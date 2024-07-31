# Copyright (c) 2018-2024 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Scores Retrieval Functions."""
from flask import current_app
from mysql.connector import connect


def month_mapping_dict() -> dict:
    """Return a dictionary with month number as key and abbreviation as value."""
    return {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }


def build_year_scoring_dict() -> dict:
    """Return a dictionary that will be used to populate panelist scoring data."""
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


def build_all_scoring_dict(use_decimal_scores: bool = False) -> dict | None:
    """Return a dictionary used to populate all panelist scoring data."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    database_connection = connect(**current_app.config["database"])

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


def retrieve_monthly_aggregate_scores(use_decimal_scores: bool = False) -> dict | None:
    """Retrieve aggregated panelist scores grouped by month for every available year."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    database_connection = connect(**current_app.config["database"])

    if use_decimal_scores:
        query = """
            SELECT YEAR(s.showdate) AS year, MONTH(s.showdate) AS month,
            SUM(pm.panelistscore_decimal) AS total
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY YEAR(s.showdate), MONTH(s.showdate)
            HAVING SUM(pm.panelistscore_decimal) IS NOT NULL
            ORDER BY YEAR(s.showdate) ASC, MONTH(s.showdate) ASC;
            """
    else:
        query = """
            SELECT YEAR(s.showdate) AS year, MONTH(s.showdate) AS month,
            SUM(pm.panelistscore) AS total
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY YEAR(s.showdate), MONTH(s.showdate)
            HAVING SUM(pm.panelistscore) IS NOT NULL
            ORDER BY YEAR(s.showdate) ASC, MONTH(s.showdate) ASC;
            """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    _months = month_mapping_dict()
    all_scores_dict = build_all_scoring_dict()
    for row in result:
        all_scores_dict[row.year][_months[row.month]] = int(row.total)

    return all_scores_dict


def retrieve_monthly_average_scores(use_decimal_scores: bool = False) -> dict | None:
    """Retrieve average panelist scores grouped by month for every available year."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    database_connection = connect(**current_app.config["database"])

    if use_decimal_scores:
        query = """
            SELECT YEAR(s.showdate) AS year, MONTH(s.showdate) AS month,
            AVG(pm.panelistscore_decimal) AS average
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY YEAR(s.showdate), MONTH(s.showdate)
            HAVING AVG(pm.panelistscore_decimal) IS NOT NULL
            ORDER BY YEAR(s.showdate) ASC, MONTH(s.showdate) ASC;
            """
    else:
        query = """
            SELECT YEAR(s.showdate) AS year, MONTH(s.showdate) AS month,
            AVG(pm.panelistscore) AS average
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY YEAR(s.showdate), MONTH(s.showdate)
            HAVING AVG(pm.panelistscore) IS NOT NULL
            ORDER BY YEAR(s.showdate) ASC, MONTH(s.showdate) ASC;
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

    _months = month_mapping_dict()
    all_scores_dict = build_all_scoring_dict()
    for row in result:
        all_scores_dict[row.year][_months[row.month]] = float(row.average)

    return all_scores_dict
