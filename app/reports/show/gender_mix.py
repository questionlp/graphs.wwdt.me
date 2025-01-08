# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panel Gender Mix Data Retrieval and Reporting Functions."""
from flask import current_app
from mysql.connector import connect


def retrieve_show_years() -> list[int] | None:
    """Retrieve a list of show years available in the database."""
    database_connection = connect(**current_app.config["database"])
    years = []
    query = """
        SELECT DISTINCT YEAR(s.showdate)
        FROM ww_shows s
        ORDER BY YEAR(s.showdate) ASC;
        """
    cursor = database_connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    for row in result:
        years.append(row[0])

    return years


def retrieve_panel_gender_count_by_year(year: int, gender: str) -> dict:
    """Retrieve a count of shows with panelists of a given gender."""
    database_connection = connect(**current_app.config["database"])

    # panelistgender field only contains a single letter
    gender_tag = gender[0].upper()

    counts = {}
    for gender_count in range(0, 4):
        query = """
            SELECT s.showdate FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            AND p.panelistgender = %s
            AND year(s.showdate) = %s
            AND s.showdate <> '2018-10-27' -- Exclude 25th anniversary special
            GROUP BY s.showdate
            HAVING COUNT(p.panelistgender) = %s;
            """
        cursor = database_connection.cursor(dictionary=True)
        cursor.execute(
            query,
            (
                gender_tag,
                year,
                gender_count,
            ),
        )
        _ = cursor.fetchall()

        counts[f"{gender_count}{gender_tag}"] = cursor.rowcount

    cursor.close()
    total = sum(counts.values())
    counts["total"] = total
    return counts


def panel_gender_mix_breakdown(gender: str) -> dict:
    """Retrieve a gender mix breakdown for a given gender."""
    show_years = retrieve_show_years()

    gender_mix_breakdown = {}
    for year in show_years:
        count = retrieve_panel_gender_count_by_year(
            year=year,
            gender=gender,
        )
        gender_mix_breakdown[year] = count

    return gender_mix_breakdown
