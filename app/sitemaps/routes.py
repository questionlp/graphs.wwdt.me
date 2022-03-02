# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""Sitemap Routes for Wait Wait Graphs Site"""
from flask import Blueprint, Response, render_template

blueprint = Blueprint("sitemaps", __name__)


@blueprint.route("/sitemap.xml")
def primary():
    """Site: Primary Sitemap XML"""
    sitemap = render_template("sitemaps/sitemap.xml")
    return Response(sitemap, mimetype="text/xml")
