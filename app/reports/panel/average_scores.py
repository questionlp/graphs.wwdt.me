# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelists Average Scores Data Retrieval Functions"""

from typing import List, Dict

from flask import current_app
import mysql.connector


def empty_years_average() -> Dict[int, int]:
    """Retrieve a dictionary containing a list of available years as
    keys and zeroes for values"""
    database_connection = mysql.connector.connect(**current_app.config["database"])
    cursor = database_connection.cursor(named_tuple=True)
    query = """
        SELECT DISTINCT YEAR(showdate) AS year
        FROM ww_shows
        ORDER BY YEAR(showdate) ASC;
        """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    return {row.year: 0 for row in result}


def retrieve_panelist_yearly_average() -> List[Dict]:
    """Retrieves a list of dictionaries for each panelist with panelist
    name, slug string and dictionary containing average scores for
    each year"""
    database_connection = mysql.connector.connect(**current_app.config["database"])
    cursor = database_connection.cursor(named_tuple=True)
    query = """
        SELECT panelistid, panelist, panelistslug
        FROM ww_panelists
        WHERE panelistslug <> 'multiple'
        ORDER BY panelistslug ASC;
        """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        database_connection.close()
        return None

    panelists = []
    for panelist in result:
        panelist_info = {
            "id": panelist.panelistid,
            "name": panelist.panelist,
            "slug": panelist.panelistslug,
        }

        cursor = database_connection.cursor(named_tuple=True)
        query = """
        SELECT YEAR(s.showdate) AS year, AVG(pm.panelistscore) AS average
        FROM ww_showpnlmap pm
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE p.panelistslug = %s
        AND s.bestof = 0 AND s.repeatshowid IS NULL
        GROUP BY YEAR(s.showdate)
        ORDER BY YEAR(s.showdate) ASC
        """
        cursor.execute(query, (panelist.panelistslug, ))
        result = cursor.fetchall()
        cursor.close()

        averages = empty_years_average().copy()
        if not result:
            panelist_info["averages"] = averages

        for row in result:
            if row.average:
                averages[row.year] = float(row.average)

        panelist_info["averages"] = averages
        panelists.append(panelist_info)

    database_connection.close()
    return panelists
