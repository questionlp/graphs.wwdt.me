# Copyright (c) 2018-2026 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Hosts Module and Blueprint Views."""

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing hosts.index."""
    response: TestResponse = client.get("/hosts/")
    assert response.status_code == 200
    assert b"Hosts" in response.data
    assert b"Show Hosts Heatmap" in response.data


def test_all_show_hosts_heatmap(client: FlaskClient) -> None:
    """Testing hosts.show_hosts_heatmap."""
    response: TestResponse = client.get("/hosts/show-hosts-heatmap")
    assert response.status_code == 200
    assert b"Show Hosts Heatmap" in response.data
    assert b"plotly" in response.data


def test_show_host_types(client: FlaskClient) -> None:
    """Testing hosts.show_host_types."""
    response: TestResponse = client.get("/hosts/show-host-types-by-year")
    assert response.status_code == 200
    assert b"Show Host Types by Year" in response.data


@pytest.mark.parametrize("year", [2006, 2020, 2025])
def test_show_host_types_by_year(client: FlaskClient, year: int) -> None:
    """Testing hosts.show_host_types_by_year."""
    response: TestResponse = client.get(f"/hosts/show-host-types-by-year/{year}")
    assert response.status_code == 200
    assert b"Show Host Types by Year" in response.data
    assert b"Regular" in response.data
    assert b"Guest" in response.data
    assert b"plotly" in response.data
