# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""Main Redirect Routes for Wait Wait Graphs Site"""
from flask import Blueprint, url_for

from app.utility import redirect_url

blueprint = Blueprint("main_redirects", __name__)


@blueprint.route("/favicon.ico")
def favicon():
    """Redirect: /favicon.ico to /static/favicon.ico"""
    return redirect_url(url_for("static", filename="favicon.ico"))


@blueprint.route("/panelist")
def panelist():
    """Redirect: /panelist to /panelists"""
    return redirect_url(url_for("panelists.index"))


@blueprint.route("/show")
def show():
    """Redirect: /show to /shows"""
    return redirect_url(url_for("shows.index"))


@blueprint.route("/shows/show-counts-by-year")
def shows_show_counts_by_year():
    """Redirect: /shows/show-counts-by-year to /show/counts-by-year"""
    return redirect_url(url_for("shows.counts_by_year"))
