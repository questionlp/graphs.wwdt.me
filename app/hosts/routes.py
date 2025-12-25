# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Hosts Routes for Wait Wait Graphs Site."""

import json

from flask import Blueprint, render_template, url_for

from app.reports.hosts import host_years
from app.shows.routes import retrieve_show_years
from app.utility import redirect_url

blueprint = Blueprint("hosts", __name__, template_folder="templates")


@blueprint.route("/")
def index() -> str:
    """View: Hosts Index."""
    return render_template("hosts/index.html")


@blueprint.route("/show-hosts-heatmap")
def show_hosts_heatmap() -> str:
    """View: Show Hosts Heatmap."""
    _shows = host_years.retrieve_host_types_all_years()

    if not _shows:
        return redirect_url(url_for("hosts.index"))

    show_years = list(_shows.keys())
    show_numbers = [number + 1 for number in range(53)]

    _data = []
    for show_year in show_years:
        _data.append(_shows[show_year])

    return render_template(
        "hosts/show-hosts-heatmap/graph.html",
        data=json.dumps(_data),
        show_numbers=show_numbers,
        years=show_years,
    )


@blueprint.route("/show-host-types-by-year")
def show_host_types() -> str:
    """View: Show Host Types by Year."""
    show_years = retrieve_show_years()

    if not show_years:
        return redirect_url(url_for("hosts.index"))

    return render_template(
        "hosts/show-host-types-by-year/index.html", show_years=show_years
    )


@blueprint.route("/show-host-types-by-year/<int:year>")
def show_host_types_by_year(year: int) -> str:
    """View: Show Host Types by Year."""
    show_years = retrieve_show_years()
    if year not in show_years:
        return redirect_url(url_for("hosts.show_host_types"))

    _data = host_years.retrieve_host_types_by_year_with_dates(year=year)
    if not _data:
        return redirect_url(url_for("hosts.show_host_types"))

    if "show_dates" in _data and "regulars" in _data and "guests" in _data:
        return render_template(
            "hosts/show-host-types-by-year/details.html",
            year=year,
            show_dates=_data["show_dates"],
            regulars=json.dumps(_data["regulars"]),
            guests=json.dumps(_data["guests"]),
        )

    return redirect_url(url_for("hosts.show_host_types"))
