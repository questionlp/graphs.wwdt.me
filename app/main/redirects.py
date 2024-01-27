# Copyright (c) 2018-2024 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Main Redirect Routes for Wait Wait Graphs Site."""
from flask import Blueprint, Response, url_for

from app.utility import redirect_url

blueprint = Blueprint("main_redirects", __name__)


@blueprint.route("/favicon.ico")
def favicon() -> Response:
    """Redirect: /favicon.ico to /static/favicon.ico."""
    return redirect_url(url_for("static", filename="favicon.ico"))


@blueprint.route("/panelist")
@blueprint.route("/panelists")
def panelist() -> Response:
    """Redirect: /panelist and /panelists to /panelists/."""
    return redirect_url(url_for("panelists.index"))


@blueprint.route("/show")
@blueprint.route("/shows")
def show() -> Response:
    """Redirect: /show and /shows to /shows/."""
    return redirect_url(url_for("shows.index"))


@blueprint.route("/show/show-counts-by-year")
def show_show_counts_by_year() -> Response:
    """Redirect: /show/show-counts-by-year to /shows/counts-by-year."""
    return redirect_url(url_for("shows.counts_by_year"))


@blueprint.route("/shows/show-counts-by-year")
def shows_show_counts_by_year() -> Response:
    """Redirect: /shows/shows-counts-by-year to /shows/counts-by-year."""
    return redirect_url(url_for("shows.counts_by_year"))
