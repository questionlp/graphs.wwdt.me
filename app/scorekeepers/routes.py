# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Scorekeepers Routes for Wait Wait Graphs Site."""

import json

from flask import Blueprint, render_template, url_for

from app.reports.scorekeepers import scorekeeper_years
from app.shows.routes import retrieve_show_years
from app.utility import redirect_url

blueprint = Blueprint("scorekeepers", __name__, template_folder="templates")


@blueprint.route("/")
def index() -> str:
    """View: Scorekeepers Index."""
    return render_template("scorekeepers/index.html")


@blueprint.route("/show-scorekeepers-heatmap")
def show_scorekeepers_heatmap() -> str:
    """View: Show Scorekeepers Heatmap."""
    _shows = scorekeeper_years.retrieve_scorekeeper_types_all_years()

    if not _shows:
        return redirect_url(url_for("scorekeepers.index"))

    show_years = list(_shows.keys())
    show_numbers = [number + 1 for number in range(53)]

    _data = []
    for show_year in show_years:
        _data.append(_shows[show_year])

    return render_template(
        "scorekeepers/show-scorekeepers-heatmap/graph.html",
        data=json.dumps(_data),
        show_numbers=show_numbers,
        years=show_years,
    )


@blueprint.route("/show-scorekeeper-types-by-year")
def show_scorekeeper_types() -> str:
    """View: Show Scorekeeper Types by Year."""
    show_years = retrieve_show_years()

    if not show_years:
        return redirect_url(url_for("scorekeepers.index"))

    return render_template(
        "scorekeepers/show-scorekeeper-types-by-year/index.html", show_years=show_years
    )


@blueprint.route("/show-scorekeeper-types-by-year/<int:year>")
def show_scorekeeper_types_by_year(year: int) -> str:
    """View: Show Scorekeeper Types by Year."""
    show_years = retrieve_show_years()
    if year not in show_years:
        return redirect_url(url_for("scorekeepers.show_scorekeeper_types"))

    _data = scorekeeper_years.retrieve_scorekeeper_types_by_year_with_dates(year=year)
    if not _data:
        return redirect_url(url_for("scorekeepers.show_scorekeeper_types"))

    if "show_dates" in _data and "regulars" in _data and "guests" in _data:
        return render_template(
            "scorekeepers/show-scorekeeper-types-by-year/details.html",
            year=year,
            show_dates=_data["show_dates"],
            regulars=json.dumps(_data["regulars"]),
            guests=json.dumps(_data["guests"]),
        )

    return redirect_url(url_for("scorekeepers.show_scorekeeper_types"))
