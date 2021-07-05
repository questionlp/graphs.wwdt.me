# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# graphs.wwdt.me is relased under the terms of the Apache License 2.0
"""Explicitly listing all reporting modules"""

from reports.panel import aggregate_scores, gender_mix
from reports.show import bluff_count, scores, show_counts

__all__ = [
    "panel",
    "show"
]
