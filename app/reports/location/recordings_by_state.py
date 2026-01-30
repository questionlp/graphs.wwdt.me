# Copyright (c) 2018-2026 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Recordings by State Retrieval Functions."""

from flask import current_app
from mysql.connector import connect


def retrieve_states_dict() -> dict[str, dict[str | int]] | None:
    """Retrieve a dictionary of states used for recording counts.

    The state postal abbreviation is used as the key and the value
    is a dictionary with postal abbreviation, name and zero as the
    recording count value.
    """
    database_connection = connect(**current_app.config["database"])

    query = """
        SELECT postal_abbreviation, name
        FROM ww_postal_abbreviations
        WHERE country = 'United States'
        ORDER BY postal_abbreviation;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    states = {}
    for row in results:
        states[row["postal_abbreviation"]] = {
            "state": row["postal_abbreviation"],
            "name": row["name"],
            "recordings": 0,
        }

    return states


def retrieve_recordings_by_state() -> dict[str, dict[str | int]] | None:
    """Retrieve recordings counts by state."""
    database_connection = connect(**current_app.config["database"])

    query = """
        SELECT l.state, COUNT(s.showid) AS recordings
        FROM ww_showlocationmap lm
        JOIN ww_shows s ON lm.showid = s.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        JOIN ww_postal_abbreviations pa ON pa.postal_abbreviation = l.state
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND pa.country = 'United States'
        GROUP BY l.state
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    states = retrieve_states_dict()

    for row in results:
        states[row["state"]]["recordings"] = row["recordings"]

    return states
