# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Sitemaps Module and Blueprint Views."""

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_primary(client: FlaskClient) -> None:
    """Testing sitemaps.primary."""
    response: TestResponse = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert "Content-Type" in response.headers
    assert response.headers["Content-Type"] == "text/xml; charset=utf-8"
    assert b"?xml" in response.data
    assert b"urlset" in response.data
