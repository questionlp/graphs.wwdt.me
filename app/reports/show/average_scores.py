# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Shows Average Scores Data Retrieval Functions"""
from typing import List, Dict, Union

from flask import current_app
import mysql.connector


def empty_years_average() -> Dict[int, int]:
    """Retrieve a dictionary containing a list of available years as
    keys and zeroes for values"""
    database_connection = mysql.connector.connect(**current_app.config["database"])

    # Retrieve available show years
    cursor = database_connection.cursor(named_tuple=True)
    query = """
        SELECT DISTINCT YEAR(showdate) AS year
        FROM ww_shows
        ORDER BY YEAR(showdate) ASC;
        """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    database_connection.close()
    return {row.year: 0 for row in result}
