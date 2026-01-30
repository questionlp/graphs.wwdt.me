# Copyright (c) 2018-2026 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Scorekeepers Module and Blueprint Views."""

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing scorekeepers.index."""
    response: TestResponse = client.get("/scorekeepers/")
    assert response.status_code == 200
    assert b"Scorekeepers" in response.data
    assert b"Show Scorekeepers Heatmap" in response.data


def test_all_show_scorekeepers_heatmap(client: FlaskClient) -> None:
    """Testing scorekeepers.show_scorekeepers_heatmap."""
    response: TestResponse = client.get("/scorekeepers/show-scorekeepers-heatmap")
    assert response.status_code == 200
    assert b"Show Scorekeepers Heatmap" in response.data
    assert b"plotly" in response.data


def test_show_scorekeeper_types(client: FlaskClient) -> None:
    """Testing scorekeepers.show_scorekeeper_types."""
    response: TestResponse = client.get("/scorekeepers/show-scorekeeper-types-by-year")
    assert response.status_code == 200
    assert b"Show Scorekeeper Types by Year" in response.data


@pytest.mark.parametrize("year", [2006, 2020, 2025])
def test_show_host_types_by_year(client: FlaskClient, year: int) -> None:
    """Testing scorekeepers.show_host_types_by_year."""
    response: TestResponse = client.get(
        f"/scorekeepers/show-scorekeeper-types-by-year/{year}"
    )
    assert response.status_code == 200
    assert b"Show Scorekeeper Types by Year" in response.data
    assert b"Regular" in response.data
    assert b"Guest" in response.data
    assert b"plotly" in response.data
