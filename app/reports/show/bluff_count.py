# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Bluff the Listener Data Retrieval Functions."""
from flask import current_app
from mysql.connector import connect

from app.reports.show.scores import month_mapping_dict


def build_bluff_data_dict() -> dict:
    """Return a dictionary used to populate Bluff the Listener data."""
    return {
        "Jan": {"correct": 0, "incorrect": 0},
        "Feb": {"correct": 0, "incorrect": 0},
        "Mar": {"correct": 0, "incorrect": 0},
        "Apr": {"correct": 0, "incorrect": 0},
        "May": {"correct": 0, "incorrect": 0},
        "Jun": {"correct": 0, "incorrect": 0},
        "Jul": {"correct": 0, "incorrect": 0},
        "Aug": {"correct": 0, "incorrect": 0},
        "Sep": {"correct": 0, "incorrect": 0},
        "Oct": {"correct": 0, "incorrect": 0},
        "Nov": {"correct": 0, "incorrect": 0},
        "Dec": {"correct": 0, "incorrect": 0},
    }


def build_bluff_data_year_month_dict() -> dict | None:
    """Return a dictionary used to populate Bluff the Listener data."""
    database_connection = connect(**current_app.config["database"])

    query = """
        SELECT MONTH(s.showdate) AS month, YEAR(s.showdate) AS year
        FROM ww_shows s
        JOIN ww_showbluffmap blm ON blm.showid = s.showid
        WHERE blm.correctbluffpnlid IS NOT NULL
        OR blm.chosenbluffpnlid IS NOT NULL
        GROUP BY YEAR(s.showdate), MONTH(s.showdate)
        ORDER BY YEAR(s.showdate) ASC, MONTH(s.showdate) ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    _months = month_mapping_dict()
    year_month = {}

    for row in result:
        year_month[f"{_months[row['month']]} {row['year']}"] = {
            "correct": 0,
            "incorrect": 0,
        }

    return year_month


def retrieve_all_bluff_counts() -> dict | None:
    """Retrieve a dictionary containing Bluff the Listener all counts broken down by month."""
    bluff_data = build_bluff_data_year_month_dict()
    database_connection = connect(**current_app.config["database"])

    # Retrieve counts where listener contestant chose the
    # correct Bluff story
    query = """
        SELECT MONTH(s.showdate) AS month, YEAR(s.showdate) AS year,
        COUNT(s.showdate) AS correct
        FROM ww_showbluffmap blm
        JOIN ww_shows s ON s.showid = blm.showid
        WHERE s.repeatshowid IS NULL
        AND chosenbluffpnlid IS NOT NULL
        AND correctbluffpnlid IS NOT NULL
        AND (
            (s.bestof = 0) OR
            (s.bestof = 1 AND s.bestofuniquebluff = 1)
        )
        AND chosenbluffpnlid = correctbluffpnlid
        GROUP BY year(s.showdate), month(s.showdate)
        ORDER BY YEAR(s.showdate) ASC, MONTH(s.showdate) ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    correct_result = cursor.fetchall()

    # Retrieve counts where listener contestant chose the
    # incorrect Bluff story
    query = """
        SELECT MONTH(s.showdate) AS month, YEAR(s.showdate) AS year,
        COUNT(s.showdate) AS incorrect
        FROM ww_showbluffmap blm
        JOIN ww_shows s ON s.showid = blm.showid
        WHERE s.repeatshowid IS NULL
        AND chosenbluffpnlid IS NOT NULL
        AND correctbluffpnlid IS NOT NULL
        AND (
            (s.bestof = 0) OR
            (s.bestof = 1 AND s.bestofuniquebluff = 1)
        )
        AND chosenbluffpnlid <> correctbluffpnlid
        GROUP BY year(s.showdate), month(s.showdate)
        ORDER BY YEAR(s.showdate) ASC, MONTH(s.showdate) ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    incorrect_result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not correct_result and not incorrect_result:
        return None

    _months = month_mapping_dict()
    for row in correct_result:
        bluff_data[f"{_months[row['month']]} {row['year']}"]["correct"] = row["correct"]

    for row in incorrect_result:
        bluff_data[f"{_months[row['month']]} {row['year']}"]["incorrect"] = row[
            "incorrect"
        ]

    return bluff_data


def retrieve_bluff_count_year(year: int) -> dict | None:
    """Retrieve a dictionary containing Bluff the Listener counts broken down by month."""
    bluff_data = build_bluff_data_dict()
    database_connection = connect(**current_app.config["database"])

    # Retrieve counts where listener contestant chose the
    # correct Bluff story
    query = """
        SELECT YEAR(s.showdate) as year, MONTH(s.showdate) AS month,
        COUNT(s.showdate) AS correct
        FROM ww_showbluffmap blm
        JOIN ww_shows s ON s.showid = blm.showid
        WHERE YEAR(s.showdate) = %s
        AND s.repeatshowid IS NULL
        AND chosenbluffpnlid IS NOT NULL
        AND correctbluffpnlid IS NOT NULL
        AND (
            (s.bestof = 0) OR
            (s.bestof = 1 AND s.bestofuniquebluff = 1)
        )
        AND chosenbluffpnlid = correctbluffpnlid
        GROUP BY YEAR(s.showdate), MONTH(s.showdate)
        ORDER BY YEAR(s.showdate) ASC, MONTH(s.showdate) ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (year,))
    correct_result = cursor.fetchall()

    # Retrieve counts where listener contestant chose the
    # incorrect Bluff story
    query = """
        SELECT YEAR(s.showdate) as year, MONTH(s.showdate) AS month,
        COUNT(s.showdate) AS incorrect
        FROM ww_showbluffmap blm
        JOIN ww_shows s ON s.showid = blm.showid
        WHERE YEAR(s.showdate) = %s
        AND s.repeatshowid IS NULL
        AND chosenbluffpnlid IS NOT NULL
        AND correctbluffpnlid IS NOT NULL
        AND (
            (s.bestof = 0) OR
            (s.bestof = 1 AND s.bestofuniquebluff = 1)
        )
        AND chosenbluffpnlid <> correctbluffpnlid
        GROUP BY YEAR (s.showdate), MONTH(s.showdate)
        ORDER BY YEAR(s.showdate) ASC, MONTH(s.showdate) ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (year,))
    incorrect_result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not correct_result and not incorrect_result:
        return None

    _months = month_mapping_dict()
    for row in correct_result:
        bluff_data[_months[row["month"]]]["correct"] = row["correct"]

    for row in incorrect_result:
        bluff_data[_months[row["month"]]]["incorrect"] = row["incorrect"]

    return bluff_data
