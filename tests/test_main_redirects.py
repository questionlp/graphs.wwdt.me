# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""Testing Main Redirects Module and Blueprint Views"""


def test_favicon(client):
    """Testing main_redirects.favicon"""
    response = client.get("/favicon.ico")
    assert response.status_code == 302
    assert response.location


def test_guest(client):
    """Testing main_redirects.panelist"""
    response = client.get("/panelist")
    assert response.status_code == 302
    assert response.location


def test_help(client):
    """Testing main_redirects.show"""
    response = client.get("/show")
    assert response.status_code == 302
    assert response.location


def test_host(client):
    """Testing main_redirects.shows_show_counts_by_year"""
    response = client.get("/shows/show-counts-by-year")
    assert response.status_code == 302
    assert response.location
