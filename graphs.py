# Copyright (c) 2018-2025 Linh Pham
# graphs.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Application Bootstrap Script for Wait Wait Graphs Site."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
