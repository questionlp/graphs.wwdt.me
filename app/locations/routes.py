# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Location Routes for Wait Wait Graphs Site."""

import json

from flask import Blueprint, render_template, url_for

from app.reports.location import home_vs_away as home_away
from app.reports.location import home_vs_away_year as home_away_year
from app.reports.location import recordings_by_state as recordings_state
from app.shows.routes import retrieve_show_years
from app.utility import redirect_url

blueprint = Blueprint("locations", __name__, template_folder="templates")


@blueprint.route("/")
def index() -> str:
    """View: Locations Index."""
    return render_template("locations/index.html")


@blueprint.route("/all-locations-shows-heatmap")
def all_locations_shows_heatmap() -> str:
    """View: All Locations Shows Heatmap."""
    _shows = home_away_year.retrieve_all_locations_shows_all_years()

    if not _shows:
        return redirect_url(url_for("locations.index"))

    show_years = list(_shows.keys())
    show_numbers = [number + 1 for number in range(53)]

    _data = []
    for show_year in show_years:
        _data.append(_shows[show_year])

    return render_template(
        "locations/all-locations-shows-heatmap/graph.html",
        data=json.dumps(_data),
        show_numbers=show_numbers,
        years=show_years,
    )


@blueprint.route("/away-shows-heatmap")
def away_shows_heatmap() -> str:
    """View: Away Shows Heatmap."""
    _away_shows = home_away_year.retrieve_away_shows_all_years()

    if not _away_shows:
        return redirect_url(url_for("locations.index"))

    show_years = list(_away_shows.keys())
    show_numbers = [number + 1 for number in range(53)]

    _data = []
    for show_year in show_years:
        _data.append(_away_shows[show_year])

    return render_template(
        "locations/away-shows-heatmap/graph.html",
        data=json.dumps(_data),
        show_numbers=show_numbers,
        years=show_years,
    )


@blueprint.route("/home-shows-heatmap")
def home_shows_heatmap() -> str:
    """View: Home Shows Heatmap."""
    _home_shows = home_away_year.retrieve_home_shows_all_years()

    if not _home_shows:
        return redirect_url(url_for("locations.index"))

    show_years = list(_home_shows.keys())
    show_numbers = [number + 1 for number in range(53)]

    _data = []
    for show_year in show_years:
        _data.append(_home_shows[show_year])

    return render_template(
        "locations/home-shows-heatmap/graph.html",
        data=json.dumps(_data),
        show_numbers=show_numbers,
        years=show_years,
    )


@blueprint.route("/home-remote-studios-shows-heatmap")
def home_remote_studios_shows_heatmap() -> str:
    """View: Home/Remote Studios Shows Heatmap."""
    _home_remote_studios_shows = (
        home_away_year.retrieve_home_remote_studios_shows_all_years()
    )

    if not _home_remote_studios_shows:
        return redirect_url(url_for("locations.index"))

    show_years = list(_home_remote_studios_shows.keys())
    show_numbers = [number + 1 for number in range(53)]

    _data = []
    for show_year in show_years:
        _data.append(_home_remote_studios_shows[show_year])

    return render_template(
        "locations/home-remote-studios-shows-heatmap/graph.html",
        data=json.dumps(_data),
        show_numbers=show_numbers,
        years=show_years,
    )


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


@blueprint.route("/show-location-types-by-year")
def show_location_types() -> str:
    """View: Show Location Types."""
    show_years = retrieve_show_years()

    if not show_years:
        return redirect_url(url_for("locations.index"))

    return render_template(
        "locations/show-location-types-by-year/index.html", show_years=show_years
    )


@blueprint.route("/show-location-types-by-year/<int:year>")
def show_location_types_by_year(year: int) -> str:
    """View: Show Location Types by Year."""
    show_years = retrieve_show_years()
    if year not in show_years:
        return redirect_url(url_for("locations.show_location_types"))

    _data = home_away_year.retrieve_home_away_studios_shows_by_year(year=year)
    if not _data:
        return redirect_url(url_for("locations.show_location_types"))

    if (
        "show_dates" in _data
        and "home" in _data
        and "away" in _data
        and "studios" in _data
        and "tbd_na" in _data
    ):
        return render_template(
            "locations/show-location-types-by-year/details.html",
            year=year,
            show_dates=_data["show_dates"],
            home=json.dumps(_data["home"]),
            away=json.dumps(_data["away"]),
            home_remote_studios=json.dumps(_data["studios"]),
            tbd_na=json.dumps(_data["tbd_na"]),
        )

    return redirect_url(url_for("locations.show_location_types"))
