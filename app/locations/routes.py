# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Location Routes for Wait Wait Graphs Site."""

from flask import Blueprint, render_template, url_for

from app.reports.location import home_vs_away as home_away
from app.reports.location import recordings_by_state as recordings_state
from app.shows.routes import retrieve_show_years
from app.utility import redirect_url

blueprint = Blueprint("locations", __name__, template_folder="templates")


@blueprint.route("/")
def index() -> str:
    """View: Locations Index."""
    return render_template("locations/index.html")


@blueprint.route("/home-vs-away")
def home_vs_away() -> str:
    """View: Home vs Away."""
    show_years = retrieve_show_years(reverse_order=False)

    if not show_years:
        return redirect_url(url_for("locations.index"))

    _home = []
    _away = []
    _studios = []
    for show_year in show_years:
        _counts = home_away.retrieve_home_vs_away_by_year(year=show_year)
        if not _counts:
            _home.append(0)
            _away.append(0)
            _studios.append(0)
        else:
            _home.append(_counts["home"])
            _away.append(_counts["away"])
            _studios.append(_counts["studios"])

    return render_template(
        "locations/home-vs-away/graph.html",
        years=show_years,
        home=_home,
        away=_away,
        studios=_studios,
    )


@blueprint.route("/recordings-by-state")
def recordings_by_state() -> str:
    """View: Recordings by State."""
    recording_counts = recordings_state.retrieve_recordings_by_state()

    if not recording_counts:
        return render_template("locations/recordings-by-state/graph.html")

    states = []
    names = []
    recordings = []

    for state in recording_counts:
        states.append(recording_counts[state]["state"])
        names.append(recording_counts[state]["name"])
        recordings.append(recording_counts[state]["recordings"])

    return render_template(
        "locations/recordings-by-state/graph.html",
        states=states,
        names=names,
        recordings=recordings,
    )
