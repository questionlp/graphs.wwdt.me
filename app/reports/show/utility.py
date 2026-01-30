# Copyright (c) 2018-2026 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Shows Utility Functions."""

from flask import current_app
from mysql.connector import connect
from wwdtm.show import Show


def retrieve_show_years(reverse_order: bool = True) -> list[int]:
    """Retrieve a list of available show years."""
    database_connection = connect(**current_app.config["database"])
    show = Show(database_connection=database_connection)
    years = show.retrieve_years()
    database_connection.close()

    if years and reverse_order:
        years.reverse()

    return years
