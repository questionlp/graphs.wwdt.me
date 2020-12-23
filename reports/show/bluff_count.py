# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020 Linh Pham
# graphs.wwdt.me is relased under the terms of the Apache License 2.0
"""WWDTM Show Bluff the Listener Data Retrieval Functions"""

from collections import OrderedDict
from typing import Dict, List
import mysql.connector

#region Utility Functions
def build_bluff_data_dict() -> Dict:
    """Returns an OrderedDict that will be used to populate
    Bluff the Listener data"""

    bluff_data_dict = OrderedDict(Jan={"correct": 0, "incorrect": 0},
                                  Feb={"correct": 0, "incorrect": 0},
                                  Mar={"correct": 0, "incorrect": 0},
                                  Apr={"correct": 0, "incorrect": 0},
                                  May={"correct": 0, "incorrect": 0},
                                  Jun={"correct": 0, "incorrect": 0},
                                  Jul={"correct": 0, "incorrect": 0},
                                  Aug={"correct": 0, "incorrect": 0},
                                  Sep={"correct": 0, "incorrect": 0},
                                  Oct={"correct": 0, "incorrect": 0},
                                  Nov={"correct": 0, "incorrect": 0},
                                  Dec={"correct": 0, "incorrect": 0})

    return bluff_data_dict

def build_bluff_data_year_month_dict(database_connection: mysql.connector.connect
                                    ) -> List[Dict]:
    """Returns an OrderedDict that will be used to populate
    Bluff the Listener data for all years and months"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT date_format(s.showdate, '%b %Y') AS date "
             "FROM ww_shows s "
             "JOIN ww_showbluffmap blm ON blm.showid = s.showid "
             "WHERE blm.correctbluffpnlid IS NOT NULL "
             "OR blm.chosenbluffpnlid IS NOT NULL "
             "GROUP BY YEAR(s.showdate), MONTH(s.showdate) "
             "ORDER BY s.showdate ASC;")
    cursor.execute(query, )
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    year_month = OrderedDict()
    for row in result:
        year_month[row["date"]] = {"correct": 0, "incorrect": 0}

    return year_month

#endregion

#region Retrieval Functions
def retrieve_all_bluff_counts(database_connection: mysql.connector.connect):
    """Retrieve an OrderedDict containing Bluff the Listener all counts
    broken down by month"""

    bluff_data = build_bluff_data_year_month_dict(database_connection)

    # Retrieve counts where listener contestant chose the
    # correct Bluff story
    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT date_format(s.showdate, '%b %Y') AS date, "
             "COUNT(s.showdate) AS correct "
             "FROM ww_showbluffmap blm "
             "JOIN ww_shows s ON s.showid = blm.showid "
             "WHERE s.repeatshowid IS NULL "
             "AND chosenbluffpnlid IS NOT NULL "
             "AND correctbluffpnlid IS NOT NULL "
             "AND ((s.bestof = 0) OR "
             "     (s.bestof = 1 AND s.bestofuniquebluff = 1)) "
             "AND chosenbluffpnlid = correctbluffpnlid "
             "GROUP BY year(s.showdate), month(s.showdate) "
             "ORDER BY s.showdate ASC")
    cursor.execute(query)
    correct_result = cursor.fetchall()

    # Retrieve counts where listener contestant chose the
    # incorrect Bluff story
    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT date_format(s.showdate, '%b %Y') AS date, "
             "COUNT(s.showdate) AS incorrect "
             "FROM ww_showbluffmap blm "
             "JOIN ww_shows s ON s.showid = blm.showid "
             "WHERE s.repeatshowid IS NULL "
             "AND chosenbluffpnlid IS NOT NULL "
             "AND correctbluffpnlid IS NOT NULL "
             "AND ((s.bestof = 0) OR "
             "     (s.bestof = 1 AND s.bestofuniquebluff = 1)) "
             "AND chosenbluffpnlid <> correctbluffpnlid "
             "GROUP BY year(s.showdate), month(s.showdate) "
             "ORDER BY s.showdate ASC")
    cursor.execute(query)
    incorrect_result = cursor.fetchall()
    cursor.close()

    if not correct_result and not incorrect_result:
        return None

    for row in correct_result:
        bluff_data[row["date"]]["correct"] = row["correct"]

    for row in incorrect_result:
        bluff_data[row["date"]]["incorrect"] = row["incorrect"]

    return bluff_data

def retrieve_bluff_count_year(year: int,
                              database_connection: mysql.connector.connect
                             ) -> Dict:
    """Retrieve an OrderedDict containing Bluff the Listener counts
    broken down by month"""

    bluff_data = build_bluff_data_dict()

    # Retrieve counts where listener contestant chose the
    # correct Bluff story
    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT YEAR(s.showdate) as year, "
             "DATE_FORMAT(s.showdate, '%b') AS month, "
             "COUNT(s.showdate) AS correct "
             "FROM ww_showbluffmap blm "
             "JOIN ww_shows s ON s.showid = blm.showid "
             "WHERE YEAR(s.showdate) = %s "
             "AND s.repeatshowid IS NULL "
             "AND chosenbluffpnlid IS NOT NULL "
             "AND correctbluffpnlid IS NOT NULL "
             "AND ((s.bestof = 0) OR "
             "     (s.bestof = 1 AND s.bestofuniquebluff = 1)) "
             "AND chosenbluffpnlid = correctbluffpnlid "
             "GROUP BY YEAR (s.showdate), MONTH(s.showdate) "
             "ORDER BY s.showdate ASC;")
    cursor.execute(query, (year, ))
    correct_result = cursor.fetchall()

    # Retrieve counts where listener contestant chose the
    # incorrect Bluff story
    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT YEAR(s.showdate) as year, "
             "DATE_FORMAT(s.showdate, '%b') AS month, "
             "COUNT(s.showdate) AS incorrect "
             "FROM ww_showbluffmap blm "
             "JOIN ww_shows s ON s.showid = blm.showid "
             "WHERE YEAR(s.showdate) = %s "
             "AND s.repeatshowid IS NULL "
             "AND chosenbluffpnlid IS NOT NULL "
             "AND correctbluffpnlid IS NOT NULL "
             "AND ((s.bestof = 0) OR "
             "     (s.bestof = 1 AND s.bestofuniquebluff = 1)) "
             "AND chosenbluffpnlid <> correctbluffpnlid "
             "GROUP BY YEAR (s.showdate), MONTH(s.showdate) "
             "ORDER BY s.showdate ASC;")
    cursor.execute(query, (year, ))
    incorrect_result = cursor.fetchall()
    cursor.close()

    if not correct_result and not incorrect_result:
        return None

    for row in correct_result:
        bluff_data[row["month"]]["correct"] = row["correct"]

    for row in incorrect_result:
        bluff_data[row["month"]]["incorrect"] = row["incorrect"]

    return bluff_data

#endregion
