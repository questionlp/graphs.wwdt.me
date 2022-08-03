# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
"""Testing Main Redirects Module and Blueprint Views"""
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_favicon(client: FlaskClient) -> None:
    """Testing main_redirects.favicon"""
    response: TestResponse = client.get("/favicon.ico")
    assert response.status_code == 302
    assert response.location
    assert "/static/favicon.ico" in response.location


def test_guest(client: FlaskClient) -> None:
    """Testing main_redirects.panelist"""
    response: TestResponse = client.get("/panelist")
    assert response.status_code == 302
    assert response.location
    assert "/panelists" in response.location

    response: TestResponse = client.get("/panelists")
    assert response.status_code == 302
    assert response.location
    assert "/panelists" in response.location


def test_help(client: FlaskClient) -> None:
    """Testing main_redirects.show"""
    response: TestResponse = client.get("/show")
    assert response.status_code == 302
    assert response.location
    assert "/shows" in response.location

    response: TestResponse = client.get("/shows")
    assert response.status_code == 302
    assert response.location
    assert "/shows" in response.location


def test_show_show_counts_by_year(client: FlaskClient) -> None:
    """Testing main_redirects.show_show_counts_by_year"""
    response: TestResponse = client.get("/show/show-counts-by-year")
    assert response.status_code == 302
    assert response.location
    assert "/shows/counts-by-year" in response.location


def test_show_counts_by_year(client: FlaskClient) -> None:
    """Testing main_redirects.shows_show_counts_by_year"""
    response: TestResponse = client.get("/shows/show-counts-by-year")
    assert response.status_code == 302
    assert response.location
    assert "/shows/counts-by-year" in response.location
