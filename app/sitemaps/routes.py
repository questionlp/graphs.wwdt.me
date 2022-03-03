# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""Sitemap Routes for Wait Wait Graphs Site"""
from flask import Blueprint, Response, render_template

from app.utility import month_names, retrieve_panelists, retrieve_show_years

blueprint = Blueprint("sitemaps", __name__)


@blueprint.route("/sitemap.xml")
def primary():
    """Site: Primary Sitemap XML"""
    panelists = retrieve_panelists()
    years = retrieve_show_years()
    sitemap = render_template(
        "sitemaps/sitemap.xml",
        months=month_names,
        panelists=panelists,
        show_years=years,
    )

    return Response(sitemap, mimetype="text/xml")
