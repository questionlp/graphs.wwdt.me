# Copyright (c) 2018-2026 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Sitemap Routes for Wait Wait Graphs Site."""

from typing import Any

from flask import Blueprint, Response, render_template

from app.utility import MONTH_NAMES, retrieve_panelists, retrieve_show_years

blueprint = Blueprint("sitemaps", __name__)


@blueprint.route("/sitemap.xml")
def primary() -> Response:
    """Site: Primary Sitemap XML."""
    sitemap: str = render_template("sitemaps/sitemap.xml")

    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-hosts.xml")
def hosts() -> Response | None:
    """View: Hosts Sitemap XML."""
    years: list[int] = retrieve_show_years(reverse_order=False)
    sitemap: str = render_template("sitemaps/hosts.xml", show_years=years)

    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-locations.xml")
def locations() -> Response | None:
    """View: Locations Sitemap XML."""
    years: list[int] = retrieve_show_years(reverse_order=False)
    sitemap: str = render_template("sitemaps/locations.xml", show_years=years)

    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-panelists.xml")
def panelists() -> Response | None:
    """View: Panelists Sitemap XML."""
    _panelists: list[dict[str, Any]] = retrieve_panelists()
    sitemap: str = render_template("sitemaps/panelists.xml", panelists=_panelists)

    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-scorekeepers.xml")
def scorekeepers() -> Response | None:
    """View: Scorekeepers Sitemap XML."""
    years: list[int] = retrieve_show_years(reverse_order=False)
    sitemap: str = render_template("sitemaps/scorekeepers.xml", show_years=years)

    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-shows.xml")
def shows() -> Response | None:
    """View: Shows Sitemap XML."""
    years: list[int] = retrieve_show_years(reverse_order=False)
    sitemap: str = render_template(
        "sitemaps/shows.xml", months=MONTH_NAMES, show_years=years
    )

    return Response(sitemap, mimetype="text/xml")
